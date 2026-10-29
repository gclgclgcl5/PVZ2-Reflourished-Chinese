#!/usr/bin/env python3
"""Patch libPVZ2.so so CDN untar/apply will not overwrite LawnStrings-*.

Target: PvZ2 Reflourished 1.4.2 arm64-v8a libPVZ2.so
(VA == file offset for the first ELF LOAD)

What it does:
1) Untar loop (0x16ad6c8): rename LawnStrings-* members to ._cdn_lawn_skip
   so English CDN text is discarded while tar stream stays in sync.
2) Apply loop (0xd17c30): skip apply-body for LawnStrings-* filenames.

Usage:
  python patch_cdn_lawnstrings_skip.py path/to/libPVZ2.so
  python patch_cdn_lawnstrings_skip.py path/to/libPVZ2.so --dry-run
"""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

LAWN_STR = 0x1BCB381  # "LawnStrings-%s"
HOOK_APPLY = 0xD17CC8  # original: cbz w8, type0
HOOK_UNTAR = 0x16AD718  # original: tbz w8, #1, ...
CAVE_APPLY = 0x1B52838  # NOP cave in RX
EXPECTED_APPLY = bytes.fromhex("c8040034")
EXPECTED_UNTAR = bytes.fromhex("68000836")
DISCARD_NAME = b"._cdn_lawn_skip\x00"
NOP = b"\x1f\x20\x03\xd5"


def enc_b(pc: int, target: int) -> int:
    return 0x14000000 | (((target - pc) // 4) & 0x3FFFFFF)


def enc_bcond(pc: int, target: int, cond: int) -> int:
    imm = (target - pc) // 4
    if not (-0x40000 <= imm < 0x40000):
        raise ValueError(f"b.cond out of range {hex(pc)} -> {hex(target)}")
    return 0x54000000 | ((imm & 0x7FFFF) << 5) | (cond & 0x1F)


def enc_adrp(pc: int, target: int, rd: int) -> int:
    imm = ((target & ~0xFFF) - (pc & ~0xFFF)) >> 12
    return 0x90000000 | ((imm & 3) << 29) | (((imm >> 2) & 0x1FFFFF) << 5) | rd


def enc_add(rd: int, rn: int, imm12: int) -> int:
    return 0x91000000 | ((imm12 & 0xFFF) << 10) | (rn << 5) | rd


def pack(words: list[int]) -> bytes:
    return b"".join(struct.pack("<I", w) for w in words)


def build_apply_cave(cave: int) -> bytes:
    w = [0] * 30

    def pc(i: int) -> int:
        return cave + 4 * i

    w[0] = 0x39400389
    w[1] = 0x7200013F
    w[2] = 0x9100078A
    w[3] = 0xF9400B8B
    w[4] = 0x9A8B014A
    w[5] = 0x39400389
    w[6] = 0x7200013F
    w[7] = enc_bcond(pc(7), pc(12), 1)
    w[8] = 0x53017D2C
    w[9] = 0x7100319F
    w[10] = enc_bcond(pc(10), pc(26), 0xB)
    w[11] = enc_b(pc(11), pc(15))
    w[12] = 0xF940078C
    w[13] = 0xF100319F
    w[14] = enc_bcond(pc(14), pc(26), 0xB)
    w[15] = enc_adrp(pc(15), LAWN_STR, 11)
    w[16] = enc_add(11, 11, LAWN_STR & 0xFFF)
    w[17] = 0xF940014C
    w[18] = 0xF940016D
    w[19] = 0xEB0D019F
    w[20] = enc_bcond(pc(20), pc(26), 1)
    w[21] = 0xB940094C
    w[22] = 0xB940096D
    w[23] = 0x6B0D019F
    w[24] = enc_bcond(pc(24), pc(26), 1)
    w[25] = enc_b(pc(25), 0xD17EE8)
    w[26] = 0x7100011F
    w[27] = enc_bcond(pc(27), pc(29), 1)
    w[28] = enc_b(pc(28), 0xD17D60)
    w[29] = enc_b(pc(29), 0xD17CCC)
    return pack(w)


def build_untar_cave(cave: int, discard_addr: int) -> bytes:
    u = [0] * 17

    def pc(i: int) -> int:
        return cave + 4 * i

    u[0] = 0xF94002CC
    u[1] = enc_adrp(pc(1), LAWN_STR, 11)
    u[2] = enc_add(11, 11, LAWN_STR & 0xFFF)
    u[3] = 0xF940016D
    u[4] = 0xEB0D019F
    u[5] = enc_bcond(pc(5), pc(13), 1)
    u[6] = 0xB9400ACC
    u[7] = 0xB940096D
    u[8] = 0x6B0D019F
    u[9] = enc_bcond(pc(9), pc(13), 1)
    u[10] = enc_adrp(pc(10), discard_addr, 22)
    u[11] = enc_add(22, 22, discard_addr & 0xFFF)
    u[12] = 0xD503201F
    u[13] = 0x721F011F
    u[14] = enc_bcond(pc(14), pc(16), 1)
    u[15] = enc_b(pc(15), 0x16AD724)
    u[16] = enc_b(pc(16), 0x16AD71C)
    return pack(u)


def patch(so_path: Path, dry_run: bool = False) -> None:
    data = bytearray(so_path.read_bytes())
    if data[HOOK_APPLY : HOOK_APPLY + 4] != EXPECTED_APPLY:
        raise SystemExit(
            f"unexpected bytes at apply hook {hex(HOOK_APPLY)}: "
            f"{data[HOOK_APPLY:HOOK_APPLY+4].hex()} (need {EXPECTED_APPLY.hex()}). "
            "Wrong SO version, or already patched."
        )
    if data[HOOK_UNTAR : HOOK_UNTAR + 4] != EXPECTED_UNTAR:
        raise SystemExit(
            f"unexpected bytes at untar hook {hex(HOOK_UNTAR)}: "
            f"{data[HOOK_UNTAR:HOOK_UNTAR+4].hex()} (need {EXPECTED_UNTAR.hex()})."
        )

    cave_apply = build_apply_cave(CAVE_APPLY)
    cave_untar_addr = (CAVE_APPLY + len(cave_apply) + 16 + 3) & ~3
    discard_addr = (cave_untar_addr + 80 + 3) & ~3
    cave_untar = build_untar_cave(cave_untar_addr, discard_addr)
    end = (discard_addr + len(DISCARD_NAME) + 16 + 3) & ~3

    region = bytes(data[CAVE_APPLY:end])
    if region != NOP * (len(region) // 4):
        raise SystemExit(f"NOP cave busy at {hex(CAVE_APPLY)}-{hex(end)}")

    print(f"apply cave  {hex(CAVE_APPLY)} ({len(cave_apply)} bytes)")
    print(f"untar cave  {hex(cave_untar_addr)} ({len(cave_untar)} bytes)")
    print(f"discard str {hex(discard_addr)} {DISCARD_NAME!r}")

    if dry_run:
        print("dry-run: no file written")
        return

    bak = so_path.with_suffix(so_path.suffix + ".bak_pre_lawnskip")
    if not bak.exists():
        bak.write_bytes(so_path.read_bytes())
        print(f"backup -> {bak}")

    data[HOOK_APPLY : HOOK_APPLY + 4] = struct.pack("<I", enc_b(HOOK_APPLY, CAVE_APPLY))
    data[CAVE_APPLY : CAVE_APPLY + len(cave_apply)] = cave_apply
    data[HOOK_UNTAR : HOOK_UNTAR + 4] = struct.pack(
        "<I", enc_b(HOOK_UNTAR, cave_untar_addr)
    )
    data[cave_untar_addr : cave_untar_addr + len(cave_untar)] = cave_untar
    data[discard_addr : discard_addr + len(DISCARD_NAME)] = DISCARD_NAME
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
