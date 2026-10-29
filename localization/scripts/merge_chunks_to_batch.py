#!/usr/bin/env python3
"""Merge export_for_ai/chunks/batch_XXX_pYY.zh.json into batch_XXX.zh.json."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

EXPORT = Path(__file__).resolve().parents[1] / "export_for_ai"
CHUNK_DIR = EXPORT / "chunks"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, nargs="*", help="batch numbers e.g. 33 34")
    args = ap.parse_args()
    batches = args.batch or list(range(33, 38))
    for b in batches:
        src = EXPORT / f"batch_{b:03d}.json"
        en = json.loads(src.read_text(encoding="utf-8"))
        merged: dict[str, str] = {}
        parts = sorted(CHUNK_DIR.glob(f"batch_{b:03d}_p*.zh.json"))
        if not parts:
            raise SystemExit(f"no chunks for batch {b}")
        for part in parts:
            obj = json.loads(part.read_text(encoding="utf-8"))
            merged.update(obj)
        missing = [k for k in en if k not in merged]
        extra = [k for k in merged if k not in en]
        if missing or extra:
            raise SystemExit(
                f"batch {b}: missing {len(missing)} extra {len(extra)} "
                f"have {len(merged)} need {len(en)}"
            )
        ordered = {k: merged[k] for k in en}
        out = EXPORT / f"batch_{b:03d}.zh.json"
        out.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out.name} ({len(ordered)})")


if __name__ == "__main__":
    main()
