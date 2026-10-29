#!/usr/bin/env python3
"""Export ALL LawnStrings_en entries into export_for_ai/batch_XXX.json for full retranslation."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = ROOT / "LawnStrings_en.json"
OUT_DIR = ROOT / "export_for_ai"

# Soft target: entries per batch; also soft char budget for long narrative batches.
TARGET_ENTRIES = 800
CHAR_BUDGET = 52000


def should_skip(key: str, value: str) -> bool:
    if not isinstance(value, str):
        return True
    if value.startswith("http://") or value.startswith("https://"):
        return True
    if value.startswith("@@BADCACHE:"):
        return True
    if value.endswith(".RTON") or value.endswith(".json"):
        return True
    return False


def main() -> None:
    en: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))
    items = [(k, v) for k, v in sorted(en.items()) if not should_skip(k, v)]
    skipped = len(en) - len(items)

    # Remove old batch_*.json (keep STYLE/README); leave *.zh.json alone if any.
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in OUT_DIR.glob("batch_*.json"):
        if p.name.endswith(".zh.json") or re.match(r"batch_\d+\.zh\.json$", p.name):
            continue
        if re.match(r"batch_\d+\.json$", p.name):
            p.unlink()

    batches: list[dict] = []
    cur: dict[str, str] = {}
    cur_chars = 0
    batch_idx = 1

    def flush() -> None:
        nonlocal cur, cur_chars, batch_idx
        if not cur:
            return
        name = f"batch_{batch_idx:03d}.json"
        path = OUT_DIR / name
        path.write_text(
            json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        keys = list(cur.keys())
        batches.append(
            {
                "file": name,
                "entries": len(cur),
                "chars": cur_chars,
                "first_key": keys[0],
                "last_key": keys[-1],
            }
        )
        batch_idx += 1
        cur = {}
        cur_chars = 0

    for k, v in items:
        v_len = len(v)
        if cur and (
            len(cur) >= TARGET_ENTRIES or (cur_chars + v_len > CHAR_BUDGET and len(cur) >= 400)
        ):
            flush()
        cur[k] = v
        cur_chars += v_len
    flush()

    manifest = {
        "total_to_translate": len(items),
        "skipped_technical": skipped,
        "batch_count": len(batches),
        "format": (
            'Each batch_XXX.json is an object: { "KEY": "English source string" }. '
            "Return the SAME keys with Chinese values."
        ),
        "batches": batches,
    }
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "remaining_keys.txt").write_text(
        "\n".join(k for k, _ in items) + "\n", encoding="utf-8"
    )
    print(
        f"exported {len(items)} keys into {len(batches)} batches "
        f"(skipped {skipped} technical) -> {OUT_DIR}"
    )


if __name__ == "__main__":
    main()
