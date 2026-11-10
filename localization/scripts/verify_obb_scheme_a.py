#!/usr/bin/env python3
"""Fail if an OBB's LoadingFonts is not a complete Scheme A (full-coverage) pack.

Blocks shipping / adb of \"packages-only\" OBBs that still have Latin Pico or a
half-broken Brianne→UI alias without Pico replaced (dashes / all-BLACK UI).

Usage:
  python localization/scripts/verify_obb_scheme_a.py path/to/main.675….obb
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

from inspect_loadingfonts import (
    HDR_SIZE,
    LF_FILE_OFF_AT,
    LF_USIZE_AT,
    STOCK_FONTS,
    find_meta,
    list_entries,
    read_pgsr,
    scan_all_metas,
)

STOCK_USIZE = 0x4B7000
STOCK_PICO = STOCK_FONTS["PICO12__.TTF"]  # (0x494000, 0x5d04)
STOCK_BRIANNE = STOCK_FONTS["BRIANNETOD.TTF"]  # (0x1d000, 0xea2c)
STOCK_ASHLEY = STOCK_FONTS["ASHLEYSCRIPTMTSTD.TTF"]
STOCK_UI = STOCK_FONTS["FBUSV8C5EI.TTF"]  # (0x48000, 0x3e4330)


def _current_sizes(hdr: bytes) -> dict[str, tuple[int, int]]:
    """Best-effort current off/size per stock basename.

    If stock (off,size) still present -> that pair.
    Else leave unresolved here; caller uses scan + heuristics for Brianne slot.
    """
    cur: dict[str, tuple[int, int]] = {}
    for e in list_entries(hdr):
        if e["found"]:
            cur[e["name"]] = (e["offset"], e["size"])
    return cur


def verify(obb_path: Path) -> list[str]:
    errors: list[str] = []
    obb = obb_path.read_bytes()
    if obb[:4] != b"1srb" and obb[:4] != b"rsb1":
        # PvZ2 RSB magic is often b'1srb' little-endian of rsb1 — accept either
        magic = obb[:4]
        if magic not in (b"1srb", b"rsb1"):
            # obb_layout uses OBB_MAGIC — check common
            from obb_layout_142 import OBB_MAGIC

            if magic != OBB_MAGIC:
                errors.append(f"not an RSB/OBB (magic={magic!r})")
                return errors

    file_off = struct.unpack_from("<I", obb, LF_FILE_OFF_AT)[0]
    usize_cat = struct.unpack_from("<I", obb, LF_USIZE_AT)[0]
    try:
        hdr, _z, payload = read_pgsr(obb, file_off)
    except Exception as e:
        errors.append(f"cannot decompress LoadingFonts: {e}")
        return errors

    if usize_cat != STOCK_USIZE:
        errors.append(
            f"LoadingFonts catalog usize={usize_cat:#x} != {STOCK_USIZE:#x}"
        )
    if len(payload) != STOCK_USIZE:
        errors.append(
            f"LoadingFonts payload len={len(payload):#x} != {STOCK_USIZE:#x}"
        )

    cur = _current_sizes(hdr)
    metas = scan_all_metas(hdr)

    pico = cur.get("PICO12__.TTF")
    brianne = cur.get("BRIANNETOD.TTF")
    ashley = cur.get("ASHLEYSCRIPTMTSTD.TTF")
    ui = cur.get("FBUSV8C5EI.TTF")

    # Pico still stock Latin → Scheme A incomplete (Winnie / specialty dashes)
    if pico == STOCK_PICO:
        errors.append(
            "PICO12__.TTF still stock Latin "
            f"(off={STOCK_PICO[0]:#x} size={STOCK_PICO[1]:#x}); "
            "run reproduce_zh / LoadingFonts --full-coverage"
        )

    # Brianne still stock Latin
    if brianne == STOCK_BRIANNE:
        errors.append(
            "BRIANNETOD.TTF still stock Latin "
            f"(off={STOCK_BRIANNE[0]:#x} size={STOCK_BRIANNE[1]:#x})"
        )

    # Half-broken: Brianne stock meta gone, but slot points at UI blob while Pico stock
    brianne_missing = brianne is None and find_meta(hdr, *STOCK_BRIANNE) is None
    if brianne_missing and pico == STOCK_PICO:
        # Look for a meta that is exactly the UI blob in a non-UI name slot
        ui_pairs = [m for m in metas if (m[1], m[2]) == STOCK_UI]
        if len(ui_pairs) >= 2 or (
            len(ui_pairs) >= 1 and ui == STOCK_UI
        ):
            errors.append(
                "half-broken Scheme A: BRIANNETOD no longer stock but "
                "PICO12__ still Latin (Brianne likely aliased to UI/BLACK only)"
            )

    if ashley == STOCK_ASHLEY:
        errors.append(
            "ASHLEYSCRIPTMTSTD.TTF still stock Latin "
            f"(off={STOCK_ASHLEY[0]:#x} size={STOCK_ASHLEY[1]:#x})"
        )

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("obb", type=Path, help="main.675….obb to check")
    args = ap.parse_args()
    if not args.obb.is_file():
        print(f"FAIL: missing {args.obb}", file=sys.stderr)
        return 2

    print(f"verify Scheme A LoadingFonts: {args.obb}")
    errors = verify(args.obb)
    # Always print current mapped sizes when possible
    try:
        obb = args.obb.read_bytes()
        file_off = struct.unpack_from("<I", obb, LF_FILE_OFF_AT)[0]
        hdr, _z, _p = read_pgsr(obb, file_off)
        cur = _current_sizes(hdr)
        for name in (
            "BRIANNETOD.TTF",
            "PICO12__.TTF",
            "ASHLEYSCRIPTMTSTD.TTF",
            "FBUSV8C5EI.TTF",
        ):
            pair = cur.get(name)
            if pair:
                print(f"  {name}: off={pair[0]:#x} size={pair[1]:#x}")
            else:
                print(f"  {name}: (not stock pair — changed)")
        print("  scanned metas:")
        for at, off, size in scan_all_metas(hdr):
            print(f"    @{at:#x} off={off:#x} size={size:#x}")
    except Exception as e:
        print(f"  (status dump skipped: {e})")

    if errors:
        print("FAIL:")
        for e in errors:
            print(f"  - {e}")
        print(
            "Do NOT adb push / release_zh / all-in-one this OBB until "
            "reproduce_zh (Scheme A full-coverage) succeeds."
        )
        return 1

    print("OK: Scheme A LoadingFonts checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
