"""Extract LocStringValues key/value pairs from LawnStrings RTON.

Thin CLI wrapper around lawnstrings_rton.decode.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lawnstrings_rton import (
    RTONReader,
    decode_rton,
    pairs_from_strings,
    read_varint,
)

__all__ = [
    "RTONReader",
    "decode_rton",
    "pairs_from_strings",
    "read_varint",
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("rton", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()
    pairs = decode_rton(args.rton)
    args.output.write_text(
        json.dumps(pairs, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(pairs)} keys -> {args.output}")


if __name__ == "__main__":
    main()
