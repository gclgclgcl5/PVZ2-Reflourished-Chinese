#!/usr/bin/env python3
"""Force all NPC / dialogue typefaces onto CJK-capable BLACK_* faces.

PvZ2 conversation bubbles pick a per-NPC typeface (FontName / DialogStyle).
Latin faces (PICO, ASHLEY, Brianne, …) have no CJK → horizontal bars.
BLACK_* uses fbUsv8C5eI and already renders UI Chinese (e.g. 点击继续).

This script rewrites those typeface *name strings* inside fixed RTON slots
(shrink + zero-pad so later Packages offsets stay valid), aliases
BrianneTod.ttf → fbUsv8C5eI.ttf in LoadingFonts, recompresses Packages,
and patches the OBB in place.
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from obb_layout_142 import (  # noqa: E402
    LF_OFF,
    ORIG_CSIZE,
    PACK_OFF,
    PACKAGES_OFF,
    compress_packages_zstd,
    pad_to_csize,
)

NPC_SHEET0 = 0x38BA000
NPC_SHEET1 = 0x38BD000
BRIANNE_OFF = 0x1D000
BRIANNE_SIZE = 0xEA2C
CJK_OFF = 0x48000
CJK_SIZE = 0x3E4330

# (old_typeface, new_typeface) — applied inside NPCDataSheet RTON slot
NPC_FONT_REMAP = [
    (b"BRIANNE_CONVERSATION_32", b"BLACK_32"),
    (b"BRIANNE_CONVERSATION_36", b"BLACK_36"),
    (b"PICO_30", b"BLACK_28"),  # Penny
    (b"PICO_34", b"BLACK_32"),  # WinnieIcon
    (b"ASHLEY_36", b"BLACK_36"),
    (b"ROGFONTS_32", b"BLACK_32"),
    (b"ROCKWELL_36", b"BLACK_36"),
    (b"INFORMALROMAN_36", b"BLACK_36"),
    (b"CROMAGNUM_36", b"BLACK_36"),
    (b"UNMASKEDBB_36", b"BLACK_36"),
    (b"NEWSFLASHBB_36", b"BLACK_36"),
    (b"BLACKADDER_36", b"BLACK_36"),
    (b"CENTURY751_36", b"BLACK_36"),
]

# Other fixed-size RTON slots: (slot_start, slot_end, remaps)
EXTRA_SLOT_REMAPS = [
    # CalendarStreakRetentionDialog @ 0x9b000, size 0x1000
    (0x9B000, 0x9C000, [(b"BRIANNE_32", b"BLACK_32")]),
]


def replace_rton_string(data: bytes, old: bytes, new: bytes) -> bytes:
    if not (1 <= len(old) <= 127 and 1 <= len(new) <= 127):
        raise ValueError("string length out of range")
    pat = bytes([0x90, len(old)]) + old
    rep = bytes([0x90, len(new)]) + new
    if pat not in data:
        raise SystemExit(f"pattern not found: {old!r}")
    count = data.count(pat)
    out = data.replace(pat, rep)
    print(f"  {old.decode()} -> {new.decode()} x{count} delta={len(out) - len(data)}")
    return out


def patch_rton_slot(
    section: bytearray, lo: int, hi: int, remaps: list[tuple[bytes, bytes]]
) -> None:
    slot = bytes(section[lo:hi])
    done = slot.find(b"\xffDONE")
    if done < 0:
        raise SystemExit(f"DONE missing in slot {lo:#x}")
    body = slot[: done + 5]
    for old, new in remaps:
        pat = bytes([0x90, len(old)]) + old
        if pat in body:
            body = replace_rton_string(body, old, new)
        elif (bytes([0x90, len(new)]) + new) in body:
            print(f"  skip {old.decode()} (already {new.decode()})")
        else:
            print(f"  warn missing {old.decode()} in slot {lo:#x}")
    pad = (hi - lo) - len(body)
    if pad < 0:
        raise SystemExit(f"slot {lo:#x} overflow by {-pad}")
    section[lo:hi] = body + b"\x00" * pad


def remap_dialogue_fonts_in_section(section: bytes) -> bytes:
    """Apply BLACK_* FontName remaps; return new decompressed Packages section."""
    buf = bytearray(section)
    print("patch NPCDataSheet fonts")
    patch_rton_slot(buf, NPC_SHEET0, NPC_SHEET1, NPC_FONT_REMAP)
    for lo, hi, remaps in EXTRA_SLOT_REMAPS:
        print(f"patch extra slot {lo:#x}")
        patch_rton_slot(buf, lo, hi, remaps)

    sheet = bytes(buf[NPC_SHEET0:NPC_SHEET1])
    leftover = []
    for old, _new in NPC_FONT_REMAP:
        if old in sheet:
            leftover.append(old.decode())
    if leftover:
        raise SystemExit(f"leftover Latin fonts in NPC sheet: {leftover}")
    print("NPC sheet Latin fonts cleared")
    return bytes(buf)


def alias_brianne_in_obb(obb: bytearray) -> None:
    hits = []
    for i in range(0, 0x1000 - 8, 4):
        a, b = struct.unpack_from("<II", obb, LF_OFF + i)
        if a == BRIANNE_OFF and b == BRIANNE_SIZE:
            hits.append(i)
    if hits:
        struct.pack_into("<II", obb, LF_OFF + hits[0], CJK_OFF, CJK_SIZE)
        print(f"  LoadingFonts: BrianneTod -> fbUsv8C5eI @{hits[0]:#x}")
        return
    cjk_hits = [
        i
        for i in range(0, 0x1000 - 8, 4)
        if struct.unpack_from("<II", obb, LF_OFF + i) == (CJK_OFF, CJK_SIZE)
    ]
    if len(cjk_hits) >= 2:
        print(f"  LoadingFonts: BrianneTod already aliased ({len(cjk_hits)} CJK refs)")
        return
    raise SystemExit(f"BrianneTod table entry not found (hits={hits})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--section", type=Path, required=True)
    ap.add_argument("--obb", type=Path, required=True, nargs="+")
    ap.add_argument("--out-section", type=Path, default=None)
    ap.add_argument("--out-zstd", type=Path, default=None)
    args = ap.parse_args()

    section = remap_dialogue_fonts_in_section(args.section.read_bytes())

    out_section = args.out_section or args.section.with_name(
        args.section.stem + "_allnpc.bin"
    )
    out_section.write_bytes(section)
    print(f"wrote {out_section}")

    print("compress Packages")
    padded = pad_to_csize(compress_packages_zstd(section))
    out_zstd = args.out_zstd or out_section.with_suffix(".zst")
    out_zstd.write_bytes(padded)
    print(f"wrote {out_zstd} ({len(padded)})")

    for obb_path in args.obb:
        obb = bytearray(obb_path.read_bytes())
        if obb[PACKAGES_OFF : PACKAGES_OFF + 4] != b"\x28\xb5\x2f\xfd":
            raise SystemExit(f"bad Packages magic in {obb_path}")
        obb[PACKAGES_OFF : PACKAGES_OFF + ORIG_CSIZE] = padded
        print("alias BrianneTod in", obb_path.name)
        alias_brianne_in_obb(obb)
        obb_path.write_bytes(obb)
        print(f"patched {obb_path}")


if __name__ == "__main__":
    main()
