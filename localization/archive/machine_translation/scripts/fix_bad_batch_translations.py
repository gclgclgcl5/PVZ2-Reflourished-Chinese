#!/usr/bin/env python3
"""Re-translate bad entries in export_for_ai/batch_*.zh.json.

Priority:
  1) ParaTranz reference (same key / same English)
  2) Bing/Google MT via translate_batches helpers (entity/macro protect)

Only rewrites entries classified as identical/english/mixed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
EXPORT = ROOT / "export_for_ai"
REF_PATH = ROOT / "参考翻译" / "utf8" / "LawnStrings-ParaTranz.json"

sys.path.insert(0, str(SCRIPTS))
from glossary_pvz2 import build_exact_map  # noqa: E402
from translate_batches import (  # noqa: E402
    CACHE_PATH,
    Cache,
    PackedMT,
    build_entity_map,
    finalize,
    needs_mt,
    protect,
)

CJK = re.compile(r"[\u4e00-\u9fff]")
STRIP = re.compile(
    r"\{[^{}]+\}|%\d*\$?[sd]|https?://\S+|@@\S+|\.RTON|[0-9]+|[xX]\d+"
)


def is_technical(value: str) -> bool:
    if value.startswith(("http://", "https://", "@@BADCACHE:")):
        return True
    if value.endswith((".RTON", ".json")):
        return True
    return False


# Broken MT from single-letter glossary pollution (h/s/d/m/or).
CORRUPT_RE = re.compile(
    r"小时e|秒[a-zA-Z]|[a-zA-Z]秒|天[a-zA-Z]|[a-zA-Z]天|分[a-zA-Z]|[a-zA-Z]分|"
    r"或者[a-zA-Z]|[a-zA-Z]或者|斯佩天|洒红节|Healt小时|ti分e|boo秒t|i分分une|秒econ"
)


def classify(en: str, zh: str) -> str:
    if not isinstance(zh, str):
        return "bad"
    if is_technical(en):
        return "ok"
    # Macro / placeholder-only strings (no prose to translate)
    if re.fullmatch(r"(?:\{[^{}]+\}|\.|\?|\s)+", en or ""):
        return "ok"
    if zh == en and re.search(r"[A-Za-z]{3,}", en or ""):
        return "identical"
    if CORRUPT_RE.search(zh):
        return "corrupt"
    plain = STRIP.sub(" ", zh)
    has_cjk = bool(CJK.search(zh))
    en_residue = re.findall(r"\b[A-Za-z][a-z]{2,}\b", plain)
    skip = {"ok", "hp", "dps", "npc", "the", "and", "for", "with"}
    en_residue = [w for w in en_residue if w.lower() not in skip]
    if not has_cjk and en_residue:
        return "english"
    if has_cjk and len(en_residue) >= 2:
        return "mixed"
    if has_cjk or not en_residue:
        return "ok"
    return "other"


def norm(s: str) -> str:
    return (
        s.replace("\r\n", "\n")
        .replace("/r\n", "\n")
        .replace("\\r\\n", "\n")
        .replace("\r", "\n")
        .strip()
    )


def load_ref() -> tuple[dict[str, str], dict[str, str]]:
    """Return (by_key, by_en_norm) maps of usable Chinese translations."""
    raw = json.loads(REF_PATH.read_text(encoding="utf-8"))
    by_key: dict[str, str] = {}
    by_en: dict[str, str] = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        original = item.get("original") or ""
        translation = item.get("translation") or ""
        if not key or not isinstance(translation, str):
            continue
        if not CJK.search(translation):
            continue
        t = translation.replace("/r\n", "\r\n").replace("/r", "\r")
        by_key[key] = t
        if isinstance(original, str) and original.strip():
            by_en.setdefault(norm(original), t)
    return by_key, by_en


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="from_idx", type=int, default=1)
    ap.add_argument("--to", dest="to_idx", type=int, default=999)
    ap.add_argument("--batch", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-mt", action="store_true", help="only apply ParaTranz/exact")
    args = ap.parse_args()

    by_key, by_en = load_ref()
    exact = build_exact_map()
    entities = build_entity_map()
    mt = None
    if not args.no_mt:
        cache = Cache(CACHE_PATH)
        # Drop polluted cache rows (failed MT / single-letter glossary corruption).
        purged = 0
        for ck, cv in list(cache._data.items()):
            if classify(ck, cv) in ("identical", "english", "mixed", "corrupt"):
                del cache._data[ck]
                purged += 1
        if purged:
            with CACHE_PATH.open("w", encoding="utf-8") as f:
                for ck, cv in cache._data.items():
                    f.write(json.dumps({"k": ck, "v": cv}, ensure_ascii=False) + "\n")
            print(f"purged {purged} bad MT cache entries", flush=True)
        mt = PackedMT(cache, pack_chars=1600)

    files = sorted(EXPORT.glob("batch_[0-9][0-9][0-9].json"))
    if args.batch is not None:
        files = [EXPORT / f"batch_{args.batch:03d}.json"]
    else:
        files = [
            p
            for p in files
            if args.from_idx <= int(p.stem.split("_")[1]) <= args.to_idx
        ]

    grand = {
        "scanned": 0,
        "bad": 0,
        "fixed_ref": 0,
        "fixed_exact": 0,
        "fixed_mt": 0,
        "still_bad": 0,
    }

    for en_path in files:
        zh_path = en_path.with_name(en_path.stem + ".zh.json")
        if not zh_path.exists():
            print(f"missing {zh_path.name}, skip", flush=True)
            continue
        en_data: dict[str, str] = json.loads(en_path.read_text(encoding="utf-8"))
        zh_data: dict[str, str] = json.loads(zh_path.read_text(encoding="utf-8"))

        bad_keys: list[str] = []
        for k, ev in en_data.items():
            zv = zh_data.get(k, ev)
            cls = classify(ev, zv)
            grand["scanned"] += 1
            if cls in ("identical", "english", "mixed", "other", "corrupt"):
                if cls == "other" and not needs_mt(ev):
                    continue
                bad_keys.append(k)
        grand["bad"] += len(bad_keys)
        print(f"{en_path.name}: {len(bad_keys)} bad / {len(en_data)}", flush=True)
        if not bad_keys:
            continue

        # Pass 1: ref / exact
        need_mt: list[str] = []
        for k in bad_keys:
            ev = en_data[k]
            if is_technical(ev):
                zh_data[k] = ev
                continue
            if ev in exact:
                zh_data[k] = exact[ev]
                grand["fixed_exact"] += 1
                continue
            if k in by_key and classify(ev, by_key[k]) == "ok":
                zh_data[k] = by_key[k]
                grand["fixed_ref"] += 1
                continue
            ref = by_en.get(norm(ev))
            if ref and classify(ev, ref) == "ok":
                zh_data[k] = ref
                grand["fixed_ref"] += 1
                continue
            need_mt.append(k)

        # Pass 2: MT
        if need_mt and mt is not None and not args.dry_run:
            protected_list: list[str] = []
            mappings: list[dict[str, str]] = []
            for k in need_mt:
                prot, mapping = protect(en_data[k], entities)
                protected_list.append(prot)
                mappings.append(mapping)
            print(f"  MT {len(need_mt)} entries...", flush=True)
            mt_outs = mt.translate_many(protected_list)
            for i, k in enumerate(need_mt):
                zh = finalize(en_data[k], protected_list[i], mappings[i], mt_outs[i])
                zh_data[k] = zh
                if classify(en_data[k], zh) == "ok":
                    grand["fixed_mt"] += 1
                else:
                    grand["still_bad"] += 1
        else:
            grand["still_bad"] += len(need_mt)
            if need_mt and args.no_mt:
                print(f"  left for MT: {len(need_mt)}", flush=True)

        if not args.dry_run:
            # keep key order of en batch
            ordered = {k: zh_data.get(k, en_data[k]) for k in en_data}
            zh_path.write_text(
                json.dumps(ordered, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"  wrote {zh_path.name}", flush=True)

    print(json.dumps(grand, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
