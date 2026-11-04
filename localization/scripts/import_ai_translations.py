#!/usr/bin/env python3
"""Merge AI-translated batch JSON files into LawnStrings_zh.json.

Each input file must be a JSON object: { \"KEY\": \"中文\" }.
Unknown keys are reported; empty values are skipped.
Keys listed in export_for_ai/almanac/almanac_name_lock.json (plant/zombie
short names) are never overwritten.

Usage:
  python import_ai_translations.py path/to/batch_001.zh.json [more.json ...]
  python import_ai_translations.py --dir path/to/folder_with_zh_json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = ROOT / "LawnStrings_en.json"
ZH_PATH = ROOT / "LawnStrings_zh.json"
PROGRESS_PATH = ROOT / "progress.json"
NAME_LOCK_PATH = ROOT / "export_for_ai" / "almanac" / "almanac_name_lock.json"


def looks_chinese(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def categorize(key: str) -> str:
    k = key.lower()
    if "plant" in k:
        return "plant"
    if "zombie" in k or "zomb" in k:
        return "zombie"
    if "narrative" in k:
        return "narrative"
    if any(x in k for x in ("ui", "button", "menu", "setting", "dialog", "tutorial")):
        return "ui"
    return "other"


def load_obj(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: root must be a JSON object")
    out: dict[str, str] = {}
    for k, v in data.items():
        if not isinstance(k, str):
            continue
        if v is None:
            continue
        if not isinstance(v, str):
            v = str(v)
        if not v.strip():
            continue
        out[k] = v
    return out


def update_progress(en: dict[str, str], zh: dict[str, str]) -> dict:
    changed = 0
    by_cat = {"ui": 0, "plant": 0, "zombie": 0, "narrative": 0, "other": 0}
    for k, ev in en.items():
        zv = zh.get(k, ev)
        if zv != ev:
            changed += 1
            by_cat[categorize(k)] += 1
    total = len(en)
    prog = {
        "total_keys": total,
        "changed_from_english": changed,
        "remaining_english": total - changed,
        "changed_by_category": by_cat,
        "pct_changed": round(100.0 * changed / total, 2) if total else 0.0,
    }
    PROGRESS_PATH.write_text(
        json.dumps(prog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return prog


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*", type=Path, help="translated JSON files")
    ap.add_argument(
        "--dir",
        type=Path,
        help="import all *.zh.json / *_zh.json / batch_*.zh.json under directory",
    )
    args = ap.parse_args()

    paths: list[Path] = list(args.files)
    if args.dir:
        for pat in ("*.zh.json", "*_zh.json", "batch_*.zh.json"):
            paths.extend(sorted(args.dir.glob(pat)))
    # unique preserve order
    seen = set()
    uniq: list[Path] = []
    for p in paths:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        uniq.append(p)
    if not uniq:
        raise SystemExit("no input files; pass paths or --dir")

    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    name_lock: dict[str, str] = {}
    if NAME_LOCK_PATH.is_file():
        raw = json.loads(NAME_LOCK_PATH.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            name_lock = {k: v for k, v in raw.items() if isinstance(k, str) and isinstance(v, str)}

    applied = 0
    skipped_unknown = 0
    skipped_same = 0
    skipped_name_lock = 0
    for path in uniq:
        obj = load_obj(path)
        local_apply = 0
        for k, v in obj.items():
            if k in name_lock:
                # Plant/zombie short names are frozen; never overwrite from AI batches
                skipped_name_lock += 1
                continue
            if k not in en:
                skipped_unknown += 1
                continue
            if v == en[k]:
                skipped_same += 1
                continue
            zh[k] = v
            local_apply += 1
        applied += local_apply
        print(f"{path.name}: applied {local_apply} / {len(obj)}")

    ZH_PATH.write_text(
        json.dumps(zh, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    prog = update_progress(en, zh)
    print(
        f"done: wrote {ZH_PATH}\n"
        f"  newly applied this run: {applied}\n"
        f"  unknown keys skipped: {skipped_unknown}\n"
        f"  identical-to-en skipped: {skipped_same}\n"
        f"  name-lock short names skipped: {skipped_name_lock}\n"
        f"  progress: {prog['changed_from_english']}/{prog['total_keys']} "
        f"({prog['pct_changed']}%), remaining {prog['remaining_english']}"
    )


if __name__ == "__main__":
    main()
