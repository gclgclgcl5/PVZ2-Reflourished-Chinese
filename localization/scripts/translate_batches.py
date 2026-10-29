#!/usr/bin/env python3
"""Translate export_for_ai/batch_XXX.json -> batch_XXX.zh.json with tag/entity protection.

Uses `translators` (Bing) with packed multi-line requests for speed.
Caches under export_for_ai/.mt_cache.jsonl for resume.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from glossary_mods import MOD_NAMES  # noqa: E402
from glossary_pvz2 import PLANTS, WORLD, ZOMBIES, build_exact_map  # noqa: E402

OUT_DIR = ROOT / "export_for_ai"
CACHE_PATH = OUT_DIR / ".mt_cache.jsonl"

MACRO_RE = re.compile(r"\{[^{}]+\}")
PLACEHOLDER_RE = re.compile(r"%\d*\$?[sd]|%\d+\$[sd]|\{[0-9]+\}")
LINE_MARK_RE = re.compile(r"⟦L(\d+)⟧")


def build_entity_map() -> dict[str, str]:
    m: dict[str, str] = {}
    m.update(MOD_NAMES)
    m.update(PLANTS)
    m.update(ZOMBIES)
    m.update(WORLD)
    return m


def protect(text: str, entities: dict[str, str]) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    idx = 0

    def add(final: str) -> str:
        nonlocal idx
        tok = f"⟦T{idx}⟧"
        mapping[tok] = final
        idx += 1
        return tok

    out = text
    parts: list[str] = []
    last = 0
    for m in MACRO_RE.finditer(out):
        parts.append(out[last : m.start()])
        parts.append(add(m.group(0)))
        last = m.end()
    parts.append(out[last:])
    out = "".join(parts)

    parts = []
    last = 0
    for m in PLACEHOLDER_RE.finditer(out):
        parts.append(out[last : m.start()])
        parts.append(add(m.group(0)))
        last = m.end()
    parts.append(out[last:])
    out = "".join(parts)

    for eng in sorted(entities.keys(), key=len, reverse=True):
        if eng and eng in out:
            zh = entities[eng]
            while eng in out:
                out = out.replace(eng, add(zh), 1)
    return out, mapping


def restore(text: str, mapping: dict[str, str]) -> str:
    out = text
    for tok, final in sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True):
        loose = tok[0] + r"\s*".join(map(re.escape, tok[1:-1])) + tok[-1]
        out = re.sub(loose, lambda _m, f=final: f, out)
        out = out.replace(tok, final)
    # Collapse spaces introduced around restored CJK tokens.
    out = re.sub(r"([\u4e00-\u9fff])\s+([\u4e00-\u9fff])", r"\1\2", out)
    out = re.sub(r"([\u4e00-\u9fff])\s+([，。！？；：、])", r"\1\2", out)
    out = re.sub(r"([，。！？；：、])\s+([\u4e00-\u9fff])", r"\1\2", out)
    return out


def preserve_newlines(en: str, zh: str) -> str:
    if "\r\n" in en:
        return zh.replace("\r\n", "\n").replace("\n", "\r\n")
    return zh


def needs_mt(s: str) -> bool:
    return bool(re.search(r"[A-Za-z]", s))


class Cache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._data: dict[str, str] = {}
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    self._data[obj["k"]] = obj["v"]
                except Exception:
                    continue

    def get(self, k: str) -> str | None:
        return self._data.get(k)

    def put(self, k: str, v: str) -> None:
        if k in self._data and self._data[k] == v:
            return
        self._data[k] = v
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"k": k, "v": v}, ensure_ascii=False) + "\n")


class PackedMT:
    def __init__(self, cache: Cache, pack_chars: int = 1800) -> None:
        import translators as ts

        self._ts = ts
        self.cache = cache
        self.pack_chars = pack_chars

    def translate_many(self, texts: list[str]) -> list[str]:
        """Translate list of protected strings; uses cache; packs misses."""
        out: list[str | None] = [None] * len(texts)
        miss_idx: list[int] = []
        for i, t in enumerate(texts):
            if not t.strip() or not needs_mt(t):
                out[i] = t
                continue
            hit = self.cache.get(t)
            if hit is not None:
                out[i] = hit
            else:
                miss_idx.append(i)

        # Pack misses
        pack: list[tuple[int, str]] = []
        pack_len = 0

        def flush() -> None:
            nonlocal pack, pack_len
            if not pack:
                return
            blob = "\n".join(f"⟦L{j}⟧{txt}" for j, (_i, txt) in enumerate(pack))
            translated = self._translate_blob(blob)
            parsed = self._parse_pack(translated, len(pack))
            for j, (orig_i, src) in enumerate(pack):
                zh = parsed.get(j)
                if zh is None or not str(zh).strip():
                    zh = self._translate_blob(src)
                self.cache.put(src, zh)
                out[orig_i] = zh
            pack = []
            pack_len = 0

        for i in miss_idx:
            t = texts[i]
            # Single huge line: translate alone
            if len(t) > self.pack_chars:
                flush()
                zh = self._translate_blob(t)
                self.cache.put(t, zh)
                out[i] = zh
                continue
            extra = len(t) + 10
            if pack and pack_len + extra > self.pack_chars:
                flush()
            pack.append((i, t))
            pack_len += extra
        flush()
        return [x if x is not None else texts[i] for i, x in enumerate(out)]

    def _parse_pack(self, translated: str, n: int) -> dict[int, str]:
        # Split on markers; tolerate MT altering newlines.
        found: dict[int, str] = {}
        matches = list(LINE_MARK_RE.finditer(translated))
        if not matches:
            return found
        for i, m in enumerate(matches):
            idx = int(m.group(1))
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(translated)
            found[idx] = translated[start:end].strip("\n")
        return found

    def _translate_blob(self, text: str) -> str:
        for attempt in range(8):
            try:
                out = self._ts.translate_text(
                    text,
                    translator="bing",
                    to_language="zh",
                    from_language="en",
                )
                time.sleep(0.2)
                if isinstance(out, str) and out.strip():
                    return out
            except Exception as e:
                wait = min(30.0, 1.2 * (2**attempt))
                print(f"  mt-retry {attempt+1}: {e!r}; sleep {wait:.1f}s", flush=True)
                time.sleep(wait)
                try:
                    out = self._ts.translate_text(
                        text,
                        translator="google",
                        to_language="zh-CN",
                        from_language="en",
                    )
                    if isinstance(out, str) and out.strip():
                        return out
                except Exception:
                    pass
        return text


def finalize(en: str, protected: str, mapping: dict[str, str], mt_out: str) -> str:
    if not needs_mt(protected):
        zh = restore(protected, mapping)
    else:
        zh = restore(mt_out, mapping)
    return preserve_newlines(en, zh)


def translate_batch(
    path: Path,
    mt: PackedMT,
    exact: dict[str, str],
    entities: dict[str, str],
    force: bool,
) -> Path:
    out_path = path.with_name(path.stem + ".zh.json")
    if out_path.exists() and not force:
        print(f"skip existing {out_path.name}", flush=True)
        return out_path

    data: dict[str, str] = json.loads(path.read_text(encoding="utf-8"))
    keys = list(data.keys())
    n = len(keys)
    print(f"translating {path.name} ({n} entries)", flush=True)

    protected_list: list[str] = []
    mappings: list[dict[str, str]] = []
    skip_mt_final: list[str | None] = []

    for k in keys:
        v = data[k]
        if (
            v.startswith("http://")
            or v.startswith("https://")
            or v.startswith("@@BADCACHE:")
            or v.endswith(".RTON")
            or v.endswith(".json")
        ):
            protected_list.append("")
            mappings.append({})
            skip_mt_final.append(v)
            continue
        if v in exact:
            protected_list.append("")
            mappings.append({})
            skip_mt_final.append(exact[v])
            continue
        if not re.search(r"[A-Za-z]", v):
            protected_list.append("")
            mappings.append({})
            skip_mt_final.append(v)
            continue
        prot, mapping = protect(v, entities)
        protected_list.append(prot)
        mappings.append(mapping)
        skip_mt_final.append(None)

    need_idx = [i for i, s in enumerate(skip_mt_final) if s is None]
    mt_inputs = [protected_list[i] for i in need_idx]
    print(f"  MT needed: {len(mt_inputs)} / {n}", flush=True)
    mt_outputs = mt.translate_many(mt_inputs) if mt_inputs else []
    mt_map = {need_idx[j]: mt_outputs[j] for j in range(len(need_idx))}

    out: dict[str, str] = {}
    for i, k in enumerate(keys):
        if skip_mt_final[i] is not None:
            out[k] = skip_mt_final[i]  # type: ignore
        else:
            out[k] = finalize(data[k], protected_list[i], mappings[i], mt_map[i])

    out_path.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {out_path.name}", flush=True)
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=OUT_DIR)
    ap.add_argument("--batch", type=str)
    ap.add_argument("--from", dest="from_idx", type=int, default=1)
    ap.add_argument("--to", dest="to_idx", type=int, default=999)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pack-chars", type=int, default=1800)
    args = ap.parse_args()

    exact = build_exact_map()
    entities = build_entity_map()
    cache = Cache(CACHE_PATH)
    mt = PackedMT(cache, pack_chars=args.pack_chars)

    if args.batch:
        name = args.batch
        if name.isdigit():
            name = f"batch_{int(name):03d}.json"
        files = [args.dir / name]
    else:
        files = sorted(args.dir.glob("batch_[0-9][0-9][0-9].json"))
        files = [
            p for p in files if args.from_idx <= int(p.stem.split("_")[1]) <= args.to_idx
        ]

    for p in files:
        if not p.exists():
            raise SystemExit(f"missing {p}")
        translate_batch(p, mt, exact, entities, args.force)


if __name__ == "__main__":
    main()
