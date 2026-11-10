#!/usr/bin/env python3
"""Patch libPVZ2.so: on PrimeGlyphCache full, clear via global mesh and retry.

Target: PvZ2 Reflourished 1.4.2 arm64-v8a libPVZ2.so
(VA == file offset for the first ELF LOAD)

When PrimeGlyphMesh_General::BuildPart cannot place a glyph (atlas full),
the stock code logs WARNING and emits blank metrics. This patch:

1) Clears a per-invocation retry flag at BuildPart entry (stock NOP site)
2) Hooks the warn site (0x16b67f8)
3) Loads the *global* glyph mesh via 0x16b706c, then calls clear 0x16b7e7c
   so the shared atlas is wiped AND global generation (+0x24) is bumped.
   HUD widgets snapshot that generation at +0x100 and rebuild on mismatch
   (avoids stale UV → wrong glyphs / corrupted gem-coin counters).
4) Resets the current BuildPart part cursor, zeroes w26 and mesh+0x44
   (draw count; stock entry does mov w26,wzr — without this, mid-retry
   leaves an inflated count → almanac description ghosting), reloads the
   string walk registers, and restarts the glyph loop
5) Retries only once (flag on BuildPart stack [sp,#0x70] — NEVER store into RX)

Must be applied AFTER patch_cdn_lawnstrings_skip.py. Re-apply from
libPVZ2.so.bak_pre_glyphclear (CDN-patched, pre-glyph) for a clean rebuild.

Glyph cave: CAVE_GLYPH=0x1B52980 (after CDN caves). Execute-only; no RX writes.

Usage:
  python patch_glyph_cache_clear.py path/to/libPVZ2.so
  python patch_glyph_cache_clear.py path/to/libPVZ2.so --dry-run
"""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

# --- version-pinned addresses (Reflourished 1.4.2 arm64) ---
HOOK_WARN = 0x16B67F8  # ldr x3, [sp, #0x30]
HOOK_ENTRY_NOP = 0x16B64F0  # stock NOP inside BuildPart prologue
GET_GLOBAL_MESH = 0x16B706C  # returns global mesh singleton
CLEAR_MESH = 0x16B7E7C  # clear atlas via [mesh+8], bump mesh+0x24
LOOP_HEAD = 0x16B65E0
WARN_CONT = 0x16B67FC

CAVE_GLYPH = 0x1B52980  # after CDN caves (~ends 0x1B52920)

# Unused in BuildPart frame (see disasm): retry flag byte/word
SP_FLAG = 0x70

EXPECTED_WARN = bytes.fromhex("e31b40f9")  # ldr x3, [sp, #0x30]
EXPECTED_ENTRY_NOP = bytes.fromhex("1f2003d5")
NOP = b"\x1f\x20\x03\xd5"


def enc_b(pc: int, target: int) -> int:
    return 0x14000000 | (((target - pc) // 4) & 0x3FFFFFF)


def enc_bl(pc: int, target: int) -> int:
    return 0x94000000 | (((target - pc) // 4) & 0x3FFFFFF)


def enc_ldr_x_imm(rt: int, rn: int, imm: int) -> int:
    assert imm % 8 == 0 and 0 <= imm // 8 < 0x1000
    return 0xF9400000 | ((imm // 8) << 10) | (rn << 5) | rt


def enc_str_x_imm(rt: int, rn: int, imm: int) -> int:
    assert imm % 8 == 0 and 0 <= imm // 8 < 0x1000
    return 0xF9000000 | ((imm // 8) << 10) | (rn << 5) | rt


def enc_str_w_imm(rt: int, rn: int, imm: int) -> int:
    assert imm % 4 == 0 and 0 <= imm // 4 < 0x1000
    return 0xB9000000 | ((imm // 4) << 10) | (rn << 5) | rt


def enc_ldrb(rt: int, rn: int, imm: int = 0) -> int:
    assert 0 <= imm < 0x1000
    return 0x39400000 | (imm << 10) | (rn << 5) | rt


def enc_strb(rt: int, rn: int, imm: int = 0) -> int:
    assert 0 <= imm < 0x1000
    return 0x39000000 | (imm << 10) | (rn << 5) | rt


def enc_movz_w(rd: int, imm16: int) -> int:
    return 0x52800000 | ((imm16 & 0xFFFF) << 5) | rd


def enc_orr_mov_x(rd: int, rm: int) -> int:
    return 0xAA0003E0 | (rm << 16) | rd


def enc_mov_w_imm0(rd: int) -> int:
    return 0x2A1F03E0 | rd


def enc_cbz_x(pc: int, target: int, rt: int) -> int:
    imm = (target - pc) // 4
    if not (-0x40000 <= imm < 0x40000):
        raise ValueError("cbz out of range")
    return 0xB4000000 | ((imm & 0x7FFFF) << 5) | rt


def enc_cbnz_x(pc: int, target: int, rt: int) -> int:
    imm = (target - pc) // 4
    if not (-0x40000 <= imm < 0x40000):
        raise ValueError("cbnz out of range")
    return 0xB5000000 | ((imm & 0x7FFFF) << 5) | rt


def enc_cbnz_w(pc: int, target: int, rt: int) -> int:
    imm = (target - pc) // 4
    if not (-0x40000 <= imm < 0x40000):
        raise ValueError("cbnz out of range")
    return 0x35000000 | ((imm & 0x7FFFF) << 5) | rt


def pack(words: list[int]) -> bytes:
    return b"".join(struct.pack("<I", w) for w in words)


def build_warn_cave(cave: int) -> bytes:
    """Warn-path cave; retry flag at [sp, #SP_FLAG]. Clear via global mesh."""
    # 0  ldrb w9, [sp, #SP_FLAG]
    # 1  cbnz w9, original            -> 21
    # 2  movz w9, #1
    # 3  strb w9, [sp, #SP_FLAG]
    # 4  bl   GET_GLOBAL_MESH
    # 5  cbnz x0, do_clear            -> 7
    # 6  mov  x0, x19                 # fallback if global null
    # 7  bl   CLEAR_MESH              # do_clear
    # 8  ldr  x8, [x19, #0x48]
    # 9  str  x8, [x19, #0x50]
    # 10 ldr  x8, [x19, #0x18]
    # 11 cbz  x8, original            -> 21
    # 12 ldr  x20, [x8, #0x278]
    # 13 ldr  x27, [x8, #0x228]
    # 14 ldr  x22, [x8, #0x280]
    # 15 mov  x21, x20
    # 16 mov  w28, wzr
    # 17 mov  w26, wzr                # match BuildPart entry
    # 18 str  wzr, [x19, #0x44]       # clear draw count immediately
    # 19 b    LOOP_HEAD
    # 20 nop                          # pad
    # 21 strb wzr, [sp, #SP_FLAG]     # original / second fail
    # 22 ldr  x3, [sp, #0x30]
    # 23 b    WARN_CONT
    # 24 nop
    w = [0] * 25

    def pc(i: int) -> int:
        return cave + 4 * i

    w[0] = enc_ldrb(9, 31, SP_FLAG)
    w[1] = enc_cbnz_w(pc(1), pc(21), 9)
    w[2] = enc_movz_w(9, 1)
    w[3] = enc_strb(9, 31, SP_FLAG)
    w[4] = enc_bl(pc(4), GET_GLOBAL_MESH)
    w[5] = enc_cbnz_x(pc(5), pc(7), 0)
    w[6] = enc_orr_mov_x(0, 19)  # mov x0, x19
    w[7] = enc_bl(pc(7), CLEAR_MESH)
    w[8] = enc_ldr_x_imm(8, 19, 0x48)
    w[9] = enc_str_x_imm(8, 19, 0x50)
    w[10] = enc_ldr_x_imm(8, 19, 0x18)
    w[11] = enc_cbz_x(pc(11), pc(21), 8)
    w[12] = enc_ldr_x_imm(20, 8, 0x278)
    w[13] = enc_ldr_x_imm(27, 8, 0x228)
    w[14] = enc_ldr_x_imm(22, 8, 0x280)
    w[15] = enc_orr_mov_x(21, 20)
    w[16] = enc_mov_w_imm0(28)
    w[17] = enc_mov_w_imm0(26)
    w[18] = enc_str_w_imm(31, 19, 0x44)
    w[19] = enc_b(pc(19), LOOP_HEAD)
    w[20] = 0xD503201F
    w[21] = enc_strb(31, 31, SP_FLAG)
    w[22] = enc_ldr_x_imm(3, 31, 0x30)
    w[23] = enc_b(pc(23), WARN_CONT)
    w[24] = 0xD503201F
    return pack(w)


def patch(so_path: Path, dry_run: bool = False) -> None:
    data = bytearray(so_path.read_bytes())

    if data[HOOK_WARN : HOOK_WARN + 4] != EXPECTED_WARN:
        cur = data[HOOK_WARN : HOOK_WARN + 4].hex()
        raise SystemExit(
            f"unexpected bytes at warn hook {hex(HOOK_WARN)}: {cur} "
            f"(need {EXPECTED_WARN.hex()}). Wrong SO version, or already patched. "
            f"Restore from {so_path.name}.bak_pre_glyphclear then re-run."
        )
    if data[HOOK_ENTRY_NOP : HOOK_ENTRY_NOP + 4] != EXPECTED_ENTRY_NOP:
        cur = data[HOOK_ENTRY_NOP : HOOK_ENTRY_NOP + 4].hex()
        raise SystemExit(
            f"unexpected bytes at entry NOP {hex(HOOK_ENTRY_NOP)}: {cur} "
            f"(need {EXPECTED_ENTRY_NOP.hex()})."
        )

    warn_cave = build_warn_cave(CAVE_GLYPH)
    end = CAVE_GLYPH + len(warn_cave)
    region = bytes(data[CAVE_GLYPH:end])
    if region != NOP * (len(region) // 4):
        raise SystemExit(f"NOP cave busy at {hex(CAVE_GLYPH)}-{hex(end)}")

    clear_flag = enc_str_w_imm(31, 31, SP_FLAG)

    print(f"entry NOP     {hex(HOOK_ENTRY_NOP)} -> str wzr, [sp, #{hex(SP_FLAG)}]")
    print(f"warn hook     {hex(HOOK_WARN)} -> cave {hex(CAVE_GLYPH)}")
    print(f"global getter {hex(GET_GLOBAL_MESH)}")
    print(f"clear target  {hex(CLEAR_MESH)}")
    print(f"warn cave     {len(warn_cave)} bytes (no RX stores)")

    if dry_run:
        print("dry-run: no file written")
        return

    bak = so_path.with_suffix(so_path.suffix + ".bak_pre_glyphclear")
    if not bak.exists():
        bak.write_bytes(so_path.read_bytes())
        print(f"backup -> {bak}")

    data[HOOK_ENTRY_NOP : HOOK_ENTRY_NOP + 4] = struct.pack("<I", clear_flag)
    data[HOOK_WARN : HOOK_WARN + 4] = struct.pack("<I", enc_b(HOOK_WARN, CAVE_GLYPH))
    data[CAVE_GLYPH : CAVE_GLYPH + len(warn_cave)] = warn_cave
    so_path.write_bytes(data)
    print(f"patched {so_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("so", type=Path, help="path to arm64-v8a libPVZ2.so")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    patch(args.so, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
