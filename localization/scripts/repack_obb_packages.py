#!/usr/bin/env python3
"""Replace all LawnStrings slots inside OBB Packages section and recompress with zstd.

For PvZ2 Reflourished 1.4.2 main.675.com.ea.game.pvz2_rfl.obb:
  - Packages RSG data is zstd (magic 28 B5 2F FD)
  - Original frame header descriptor is 0x80 (non-single-segment)
  - Use streaming compressobj at level 19 so the frame matches the game decoder

Workflow:
  1. Extract packages_section.bin from OBB (see 汉化教程.md)
  2. Encode Chinese LawnStrings_zh.rton with Sen
  3. python repack_obb_packages.py packages_section.bin LawnStrings_zh.rton out_section.bin
  4. Paste out_section.bin back into OBB / rebuild with Sen

This script only patches the decompressed Packages *section* and writes a new
zstd blob + updated section file. Pasting into the OBB is documented separately.
"""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

import zstandard as zstd

# Offsets of the 6 identical LawnStrings blobs inside packages_section.bin (1.4.2)
LAWNSTRINGS_STARTS = [1540096, 4206592, 6873088, 9539584, 12206080, 14872576]
LAWNSTRINGS_SLOT = 2666496  # bytes reserved per copy
# Original Packages compressed payload size in this OBB build
ORIG_CSIZE = 3522560


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


def compress_packages_zstd(section: bytes) -> bytes:
    """Match original non-single-segment L19 frame (desc 0x80)."""
    params = zstd.ZstdCompressionParameters.from_level(
        19, write_content_size=True, write_checksum=False
    )
    cctx = zstd.ZstdCompressor(compression_params=params)
    cobj = cctx.compressobj(size=len(section))
    out = cobj.compress(section) + cobj.flush()
    if out[:4] != b"\x28\xb5\x2f\xfd":
        raise SystemExit("not a zstd frame")
    fd = out[4]
    single = (fd >> 5) & 1
    print(
        f"zstd size={len(out)} desc=0x{fd:02x} single_segment={single} "
        f"delta_vs_orig={len(out) - ORIG_CSIZE:+d}"
    )
    if single != 0:
        print("WARNING: single_segment=1; game may SIGSEGV. Prefer streaming L19.")
    if len(out) > ORIG_CSIZE:
        print(
            "WARNING: compressed larger than original slot; "
            "in-place OBB patch may fail — use Sen full rebuild."
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("section", type=Path, help="decompressed packages_section.bin")
    ap.add_argument("zh_rton", type=Path, help="Chinese LawnStrings RTON")
    ap.add_argument("out_section", type=Path, help="output patched section")
    ap.add_argument(
        "--out-zstd",
        type=Path,
        default=None,
        help="also write compressed Packages payload",
    )
    args = ap.parse_args()

    section = args.section.read_bytes()
    zh = args.zh_rton.read_bytes()
    patched = patch_section(section, zh)
    args.out_section.write_bytes(patched)
    print(f"wrote section {args.out_section} ({len(patched)} bytes)")

    if args.out_zstd:
        blob = compress_packages_zstd(patched)
        if len(blob) < ORIG_CSIZE:
            blob = blob + b"\x00" * (ORIG_CSIZE - len(blob))
        args.out_zstd.write_bytes(blob[:ORIG_CSIZE] if len(blob) >= ORIG_CSIZE else blob)
        print(f"wrote zstd {args.out_zstd} ({args.out_zstd.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
