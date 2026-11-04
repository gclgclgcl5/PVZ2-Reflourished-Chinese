#!/usr/bin/env python3
"""QA AI almanac translation batches against EN + name lock.

Checks:
  - key set matches the paired EN batch (same stem without .zh)
  - macro bags ({KEYWORD}/{STAT}/{FLAVOR}/…) match EN
  - \\r\\n counts roughly aligned
  - short-name keys in ZH batch must equal almanac_name_lock (reject mismatch)
  - warn if locked English display names still appear in DESCRIPTION/HEADER

Usage:
  python qa_almanac_baokai.py path/to/almanac_001.zh.json
  python qa_almanac_baokai.py --dir localization/export_for_ai/almanac
Exit code 1 if hard failures; warnings alone exit 0.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "export_for_ai" / "almanac"
EN_PATH = ROOT / "LawnStrings_en.json"
LOCK_PATH = OUT_DIR / "almanac_name_lock.json"

MACRO_RE = re.compile(r"\{[A-Za-z_][^}]*\}")
# Prefer longer English names first when scanning leftovers
WORD_BOUNDARY_OK = re.compile(r"[A-Za-z]")


def load_obj(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: root must be a JSON object")
    out: dict[str, str] = {}
    for k, v in data.items():
        if isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out


def macro_bag(s: str) -> list[str]:
    return MACRO_RE.findall(s)


def crlf_count(s: str) -> int:
    return s.count("\r\n")


def resolve_en_batch(zh_path: Path) -> Path | None:
    name = zh_path.name
    if name.endswith(".zh.json"):
        cand = zh_path.with_name(name[: -len(".zh.json")] + ".json")
        if cand.is_file():
            return cand
    # almanac_pilot.zh.json -> almanac_pilot.json
    if name.endswith("_zh.json"):
        cand = zh_path.with_name(name[: -len("_zh.json")] + ".json")
        if cand.is_file():
            return cand
    return None


def is_short_name_key(key: str) -> bool:
    if key.endswith(("_DESCRIPTION", "_DESCRIPTION_HEADER", "_TOOLTIP")):
        return False
    if key.startswith(("ALMANAC_", "STAT_", "[STAT_")):
        return False
    return True


def english_name_hits(text: str, en_name: str) -> bool:
    """True if en_name appears as a distinct English phrase in text."""
    if not en_name or len(en_name) < 3:
        return False
    # Skip purely symbolic / acronym-only very short
    idx = 0
    lower_text = text
    target = en_name
    while True:
        pos = lower_text.find(target, idx)
        if pos < 0:
            return False
        before = lower_text[pos - 1] if pos > 0 else ""
        after_i = pos + len(target)
        after = lower_text[after_i] if after_i < len(lower_text) else ""
        # Require non-letter boundaries so "Pea" does not match inside longer words badly;
        # allow punctuation/space/CJK around the phrase.
        left_ok = not before or not WORD_BOUNDARY_OK.match(before)
        right_ok = not after or not WORD_BOUNDARY_OK.match(after)
        if left_ok and right_ok:
            return True
        idx = pos + 1


def entity_base_from_text_key(key: str) -> str | None:
    for suffix in ("_DESCRIPTION_HEADER", "_DESCRIPTION", "_TOOLTIP"):
        if key.endswith(suffix):
            return key[: -len(suffix)]
    return None


def qa_one(
    zh_path: Path,
    en_full: dict[str, str],
    lock: dict[str, str],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    zh = load_obj(zh_path)
    en_batch_path = resolve_en_batch(zh_path)
    if en_batch_path is None:
        errors.append(f"{zh_path.name}: missing paired EN batch")
        return errors, warnings
    en_batch = load_obj(en_batch_path)

    zh_keys = set(zh.keys())
    en_keys = set(en_batch.keys())
    missing = sorted(en_keys - zh_keys)
    extra = sorted(zh_keys - en_keys)
    if missing:
        errors.append(f"{zh_path.name}: missing {len(missing)} keys (e.g. {missing[:5]})")
    if extra:
        for k in extra:
            if k in lock and is_short_name_key(k):
                if zh[k] != lock[k]:
                    errors.append(
                        f"{zh_path.name}: short name {k!r} must equal lock "
                        f"({lock[k]!r}), got {zh[k]!r}"
                    )
                else:
                    warnings.append(
                        f"{zh_path.name}: extra locked short name {k!r} (ignored on import)"
                    )
            else:
                errors.append(f"{zh_path.name}: unexpected extra key {k!r}")

    for k in sorted(en_keys & zh_keys):
        ev = en_batch[k]
        zv = zh[k]
        if is_short_name_key(k) and k in lock and zv != lock[k]:
            errors.append(
                f"{zh_path.name}: locked short name {k!r} changed "
                f"(want {lock[k]!r}, got {zv!r})"
            )
            continue

        em = sorted(macro_bag(ev))
        zm = sorted(macro_bag(zv))
        if em != zm:
            errors.append(
                f"{zh_path.name}: macro mismatch on {k}: en={em} zh={zm}"
            )

        ec, zc = crlf_count(ev), crlf_count(zv)
        if ec and abs(ec - zc) > max(2, ec // 3):
            warnings.append(
                f"{zh_path.name}: \\r\\n count diverge on {k}: en={ec} zh={zc}"
            )

        if k.endswith(("_DESCRIPTION", "_DESCRIPTION_HEADER")):
            base = entity_base_from_text_key(k)
            if base and base in lock:
                en_disp = en_full.get(base, "")
                zh_disp = lock[base]
                if (
                    isinstance(en_disp, str)
                    and en_disp
                    and re.search(r"[\u4e00-\u9fff]", zh_disp)
                    and english_name_hits(zv, en_disp)
                    and zh_disp not in zv
                ):
                    warnings.append(
                        f"{zh_path.name}: {k} may still use English "
                        f"{en_disp!r}; prefer lock {zh_disp!r}"
                    )

    return errors, warnings


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--dir", type=Path, default=None)
    args = ap.parse_args()

    paths: list[Path] = list(args.files)
    if args.dir:
        paths.extend(sorted(args.dir.glob("*.zh.json")))
    seen: set[Path] = set()
    uniq: list[Path] = []
    for p in paths:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        uniq.append(p)
    if not uniq:
        raise SystemExit("no .zh.json files; pass paths or --dir")

    if not LOCK_PATH.is_file():
        raise SystemExit(f"missing name lock: {LOCK_PATH} (run export_almanac_for_ai.py)")
    lock: dict[str, str] = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    en_full: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))

    all_err: list[str] = []
    all_warn: list[str] = []
    for p in uniq:
        e, w = qa_one(p, en_full, lock)
        all_err.extend(e)
        all_warn.extend(w)

    for w in all_warn:
        print(f"WARN: {w}")
    for e in all_err:
        print(f"ERROR: {e}")
    print(
        f"qa done: {len(uniq)} file(s), {len(all_err)} error(s), {len(all_warn)} warning(s)"
    )
    if all_err:
        sys.exit(1)


if __name__ == "__main__":
    main()
