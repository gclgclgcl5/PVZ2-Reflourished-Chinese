#!/usr/bin/env python3
"""Replace all LawnStrings slots inside OBB Packages section and recompress with zstd.

For PvZ2 Reflourished 1.4.2 main.675.com.ea.game.pvz2_rfl.obb:
  - Packages RSG data is zstd (magic 28 B5 2F FD)
  - Original frame header descriptor is 0x80 (non-single-segment)
  - Use streaming compressobj at level 19 so the frame matches the game decoder

Workflow:
  1. Extract packages_section.bin via obb_layout_142.extract_packages_section
  2. Encode Chinese LawnStrings_zh.rton (build_zh_rton.py)
  3. python repack_obb_packages.py packages_section.bin LawnStrings_zh.rton out_section.bin
  4. Write back with obb_layout_142.write_packages_section
"""
from __future__ import annotations

import argparse
from pathlib import Path

from obb_layout_142 import (
    LAWNSTRINGS_SLOT,
    LAWNSTRINGS_STARTS,
    ORIG_CSIZE,
    PACKAGES_CSIZE,
    compress_packages_section,
    compress_packages_zstd,
    pad_to_csize,
)

# Re-export for callers that import from this module
__all__ = [
    "LAWNSTRINGS_SLOT",
    "LAWNSTRINGS_STARTS",
    "ORIG_CSIZE",
    "PACKAGES_CSIZE",
    "compress_packages_section",
    "compress_packages_zstd",
    "pad_to_csize",
    "patch_section",
]


def patch_section(section: bytes, zh_rton: bytes) -> bytes:
    if len(zh_rton) > LAWNSTRINGS_SLOT:
        raise SystemExit(
            f"RTON too large: {len(zh_rton)} > slot {LAWNSTRINGS_SLOT}"
        )
    padded = zh_rton + b"\x00" * (LAWNSTRINGS_SLOT - len(zh_rton))
    sec = bytearray(section)
    for start in LAWNSTRINGS_STARTS:
        if start + LAWNSTRINGS_SLOT > len(sec):
            raise SystemExit(f"section too small for slot at {start}")
        sec[start : start + LAWNSTRINGS_SLOT] = padded
    return bytes(sec)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("section", type=Path, help="decompressed packages_section.bin")
    ap.add_argument("zh_rton", type=Path, help="Chinese LawnStrings RTON")
    ap.add_argument("out_section", type=Path, help="output patched section")
    ap.add_argument(
        "--out-zstd",
        type=Path,
        default=None,
        help="also write compressed Packages payload (padded to csize)",
    )
    args = ap.parse_args()

    section = args.section.read_bytes()
    zh = args.zh_rton.read_bytes()
    patched = patch_section(section, zh)
    args.out_section.write_bytes(patched)
    print(f"wrote section {args.out_section} ({len(patched)} bytes)")

    if args.out_zstd:
        blob = pad_to_csize(compress_packages_zstd(patched))
        args.out_zstd.write_bytes(blob)
        print(f"wrote zstd {args.out_zstd} ({args.out_zstd.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
