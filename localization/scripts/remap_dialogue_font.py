#!/usr/bin/env python3
"""Remap PvZ2 dialogue typefaces from BrianneTod → fbUsv8C5eI Regular.

Root cause
----------
Conversation UI uses typefaces BRIANNE_CONVERSATION_32/36 whose Font is
\"BrianneTod\". That TTF has only ~170 Latin glyphs (0 CJK). Missing CJK
code points render as horizontal bars / tofu.

Evidence (Reflourished 1.4.2 OBB)
---------------------------------
- Packages section RTON ``typefaces`` @ 0x4e000 (slot 0x2000)
- Font RSG ``LoadingFonts`` pgsr @ OBB 0xb17b000, zstd payload @ +0x1000
  → decompresses to ~4.94MB blob with 13 TTFs:
    BrianneTod          @ 0x1d000  size 59948   cmap 170   CJK 0
    fbUsv8C5eI Regular  @ 0x48000  size ~4.08MB cmap 7318  CJK 6766  (UI 黑体)

Recommended fix (Scheme A — this script)
----------------------------------------
RTON string-pool surgical patch: change Font refs for
BRIANNE_CONVERSATION_32/36 from pool index 53 (BrianneTod) to 74
(fbUsv8C5eI Regular). Bytes ``91 35`` → ``91 4a`` at offsets 0x604 / 0x635
inside typefaces.rton. Slot size unchanged; no Sen re-encode required.

Alternative (Scheme B — not automated)
---------------------------------------
Replace BrianneTod.ttf inside the LoadingFonts RSG with a CJK font whose
name table still says BrianneTod. The stock face is only 60KB while the
UI CJK face is ~4MB, so in-place overwrite cannot work; requires full
RSG rebuild / recompress and is higher risk.

Usage
-----
  python remap_dialogue_font.py typefaces.rton -o typefaces_dialogue_cjk.rton
  python remap_dialogue_font.py packages_section_zh.bin --section -o packages_section_fontfix.bin
"""
from __future__ import annotations

import argparse
from pathlib import Path

# Offsets inside typefaces.rton (1.4.2 / current Packages dump)
CONV32_FONT_REF = 0x604
CONV36_FONT_REF = 0x635
TYPEFACES_IN_SECTION = 0x4E000
REF_BRIANNE = bytes((0x91, 0x35))  # cached string index 53
REF_CJK = bytes((0x91, 0x4A))  # cached string index 74


def patch_typefaces_rton(data: bytearray) -> None:
    for off in (CONV32_FONT_REF, CONV36_FONT_REF):
        cur = bytes(data[off : off + 2])
        if cur == REF_CJK:
            continue
        if cur != REF_BRIANNE:
            raise SystemExit(
                f"unexpected Font ref at 0x{off:x}: {cur.hex()} "
                f"(want {REF_BRIANNE.hex()} or already {REF_CJK.hex()})"
            )
        data[off : off + 2] = REF_CJK


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path, help="typefaces.rton OR packages_section.bin")
    ap.add_argument("-o", "--output", type=Path, required=True)
    ap.add_argument(
        "--section",
        action="store_true",
        help="input is full Packages section; patch typefaces at 0x4e000",
    )
    args = ap.parse_args()

    blob = bytearray(args.input.read_bytes())
    if args.section:
        slot = TYPEFACES_IN_SECTION
        if blob[slot : slot + 4] != b"RTON":
            raise SystemExit(f"no RTON at section 0x{slot:x}")
        face = bytearray(blob[slot : slot + 8192])
        patch_typefaces_rton(face)
        blob[slot : slot + len(face)] = face
        print(f"patched typefaces inside section @ 0x{slot:x}")
    else:
        if blob[:4] != b"RTON":
            raise SystemExit("not an RTON file (missing magic)")
        patch_typefaces_rton(blob)
        print("patched standalone typefaces.rton")

    args.output.write_bytes(blob)
    print(f"wrote {args.output} ({len(blob)} bytes)")
    print("BRIANNE_CONVERSATION_32/36 Font → fbUsv8C5eI Regular")


if __name__ == "__main__":
    main()
