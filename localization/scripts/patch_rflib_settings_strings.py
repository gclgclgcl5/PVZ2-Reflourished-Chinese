#!/usr/bin/env python3
"""Localize Reflourished settings checkbox labels in libRFLib.so.

RFLib copies hardcoded English into std::string, then builds SexyString via a
codecvt facet that treats bytes as Latin-1. UTF-8 Chinese either aborts
(SIGABRT on opening Settings) or would not render.

This patch:
  1) Replaces the five English C strings with equal-length UTF-8 Chinese
     (space-padded; no interior NUL — sized copies bake English lengths).
  2) Hooks the SexyString codecvt call (blr x8 @ 0x1eefa4) to a small
     UTF-8→UTF-32 converter overwritten onto the old error path @ 0x1ef07c.

Usage:
  python patch_rflib_settings_strings.py path/to/libRFLib.so
  python patch_rflib_settings_strings.py path/to/libRFLib.so --dry-run
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

REPLACEMENTS: list[tuple[str, str]] = [
    ("Always Use Max Lawn Zoom", "始终最大草坪缩放"),
    ("Center Lawn Camera", "草坪镜头居中"),
    ("Target 60 FPS", "目标 60 帧"),
    ("Always Replay Level Dialogue", "总是重播关卡对话"),
    ("Disable Power-Up and Plant Food Purchases", "禁用金手指和叶绿素购买"),
]

BACKUP_SUFFIX = ".bak_pre_settings_zh"

# VA == file+0x1000 in RX LOAD for these addresses.
CODECVT_BLR_VA = 0x1EEFA4
CAVE_VA = 0x1EF07C
EXPECTED_BLR = bytes.fromhex("00 01 3f d6")  # blr x8


def _va_to_file(va: int) -> int:
    if va < 0x198F14:
        return va
    if va < 0x481530:
        return va - 0x1000
    if va < 0x4E0218:
        return va - 0x2000
    return va - 0x3000


def _enc_bl(pc: int, target: int) -> bytes:
    imm = (target - pc) // 4
    if not (-0x2000000 <= imm < 0x2000000):
        raise SystemExit(f"bl out of range {pc:#x} -> {target:#x}")
    return struct.pack("<I", 0x94000000 | (imm & 0x3FFFFFF))


def _enc_b(pc: int, target: int) -> bytes:
    imm = (target - pc) // 4
    if not (-0x2000000 <= imm < 0x2000000):
        raise SystemExit(f"b out of range {pc:#x} -> {target:#x}")
    return struct.pack("<I", 0x14000000 | (imm & 0x3FFFFFF))


def _u32(x: int) -> bytes:
    return struct.pack("<I", x & 0xFFFFFFFF)


def _lsl_w(rd: int, rn: int, sh: int) -> int:
    immr = (-sh) % 32
    imms = 31 - sh
    return 0x53000000 | (immr << 16) | (imms << 10) | (rn << 5) | rd


def _orr_w_lsl(rd: int, rn: int, rm: int, sh: int) -> int:
    return 0x2A000000 | (sh << 10) | (rm << 16) | (rn << 5) | rd


def build_utf8_codecvt_cave_v2() -> bytes:
    """UTF-8→UTF-32 codecvt-compatible 'in'; success returns w0=1.

    Args: x2=from, x3=from_end, x4=&from_next, x5=to, x6=to_end, x7=&to_next
    """
    parts: list[bytes] = []

    def R(w: int) -> None:
        parts.append(_u32(w))

    def here() -> int:
        return sum(len(p) for p in parts)

    labels: dict[str, int] = {}
    fixups: list[tuple[int, str, str]] = []

    def B_cond(cond: int, label: str) -> None:
        fixups.append((here(), "bcond", label))
        R(0x54000000 | (cond & 0x1F))

    def B(label: str) -> None:
        fixups.append((here(), "b", label))
        R(0x14000000)

    # prologue (0x40 frame so [sp,#0x30] is in-range)
    R(0xA9BC7BFD)  # stp x29,x30,[sp,#-0x40]!
    R(0xA9010FE2)  # stp x2,x3,[sp,#0x10]
    R(0xA90217E4)  # stp x4,x5,[sp,#0x20]
    R(0xA9031FE6)  # stp x6,x7,[sp,#0x30]
    R(0xAA0203E9)  # mov x9,x2
    R(0xAA0503EA)  # mov x10,x5

    labels["loop"] = here()
    R(0xEB03013F)  # cmp x9,x3
    B_cond(2, "done")  # hs
    R(0xEB06015F)  # cmp x10,x6
    B_cond(2, "done")  # hs
    R(0x3940012B)  # ldrb w11,[x9]
    R(0x7102017F)  # cmp w11,#0x80
    B_cond(3, "ascii")  # lo
    R(0x7103817F)  # cmp w11,#0xe0
    B_cond(3, "two")
    R(0x7103C17F)  # cmp w11,#0xf0
    B_cond(3, "three")

    # four-byte
    R(0x528000EC)  # mov w12,#7
    R(0x0A0C016C)  # and w12,w11,w12
    R(0x3940052D)  # ldrb w13,[x9,#1]
    R(0x3940092E)
    R(0x39400D2F)
    R(0x528007F0)  # mov w16,#0x3f
    R(0x0A1001AD)  # and w13,w13,w16
    R(0x0A1001CE)  # and w14,w14,w16
    R(0x0A1001EF)  # and w15,w15,w16
    R(_lsl_w(12, 12, 18))
    R(_orr_w_lsl(12, 12, 13, 12))
    R(_orr_w_lsl(12, 12, 14, 6))
    R(0x2A0F018C)  # orr w12,w12,w15
    R(0x91001129)  # add x9,#4
    B("store")

    labels["three"] = here()
    R(0x528001EC)  # mov w12,#0xf
    R(0x0A0C016C)
    R(0x3940052D)
    R(0x3940092E)
    R(0x528007F0)
    R(0x0A1001AD)
    R(0x0A1001CE)
    R(_lsl_w(12, 12, 12))
    R(_orr_w_lsl(12, 12, 13, 6))
    R(0x2A0E018C)
    R(0x91000D29)
    B("store")

    labels["two"] = here()
    R(0x528003EC)  # mov w12,#0x1f
    R(0x0A0C016C)
    R(0x3940052D)
    R(0x528007F0)
    R(0x0A1001AD)
    R(_lsl_w(12, 12, 6))
    R(0x2A0D018C)
    R(0x91000929)
    B("store")

    labels["ascii"] = here()
    R(0x2A0B03EC)  # mov w12,w11
    R(0x91000529)

    labels["store"] = here()
    R(0xB900014C)  # str w12,[x10]
    R(0x9100114A)  # add x10,#4
    B("loop")

    labels["done"] = here()
    R(0xF94013E4)  # ldr x4,[sp,#0x20]
    R(0xF9401BE7)  # ldr x7,[sp,#0x30]
    R(0xF9000089)  # str x9,[x4]
    R(0xF90000EA)  # str x10,[x7]
    R(0x52800020)  # mov w0,#1
    R(0xA8C47BFD)  # ldp x29,x30,[sp],#0x40
    R(0xD65F03C0)  # ret

    blob = bytearray(b"".join(parts))
    for off, kind, lab in fixups:
        target = labels[lab]
        if kind == "b":
            imm = (target - off) // 4
            struct.pack_into("<I", blob, off, 0x14000000 | (imm & 0x3FFFFFF))
        else:
            old = struct.unpack_from("<I", blob, off)[0]
            cond = old & 0x1F
            imm = (target - off) // 4
            if not (-0x4000 <= imm < 0x4000):
                raise SystemExit(f"b.cond imm out of range for {lab}")
            struct.pack_into(
                "<I", blob, off, 0x54000000 | ((imm & 0x7FFFF) << 5) | cond
            )
    return bytes(blob)


def _count_occurrences(data: bytes, needle: bytes) -> list[int]:
    offs: list[int] = []
    start = 0
    while True:
        i = data.find(needle, start)
        if i < 0:
            break
        offs.append(i)
        start = i + 1
    return offs


def _exact_slot(en: str, zh: str) -> bytes:
    en_b = en.encode("ascii")
    zh_b = zh.encode("utf-8")
    if len(zh_b) > len(en_b):
        raise SystemExit(
            f"Chinese too long for slot: {en!r} ({len(en_b)}B) -> "
            f"{zh!r} ({len(zh_b)}B)"
        )
    body = zh_b + (b" " * (len(en_b) - len(zh_b)))
    assert len(body) == len(en_b) and b"\x00" not in body
    return body + b"\x00"


def patch(so_path: Path, *, dry_run: bool = False) -> None:
    bak = Path(str(so_path) + BACKUP_SUFFIX)
    raw = bak.read_bytes() if bak.is_file() else so_path.read_bytes()
    if bak.is_file():
        print(f"source <- {bak}")
    data = bytearray(raw)

    # --- string replacements ---
    for en, zh in REPLACEMENTS:
        en_b = en.encode("ascii")
        new_slot = _exact_slot(en, zh)
        offs = _count_occurrences(bytes(data), en_b)
        if len(offs) != 1:
            raise SystemExit(f"expected 1 hit for {en!r}, found {offs}")
        off = offs[0]
        if data[off + len(en_b)] != 0:
            raise SystemExit(f"missing NUL after {en!r}")
        data[off : off + len(new_slot)] = new_slot
        print(
            f"{off:#x}: {en!r} -> {zh!r} "
            f"(pad {len(en_b) - len(zh.encode('utf-8'))} spaces)"
        )

    # --- UTF-8 codecvt hook ---
    blr_off = _va_to_file(CODECVT_BLR_VA)
    cave_off = _va_to_file(CAVE_VA)
    if bytes(data[blr_off : blr_off + 4]) != EXPECTED_BLR:
        raise SystemExit(
            f"unexpected bytes at codecvt site {CODECVT_BLR_VA:#x}: "
            f"{data[blr_off:blr_off+4].hex()} (want {EXPECTED_BLR.hex()})"
        )
    cave = build_utf8_codecvt_cave_v2()
    # Ensure we do not run into the next function's ret too aggressively;
    # original error path to ret is ~0x350-sized func, cave is small.
    if cave_off + len(cave) > _va_to_file(0x1EF1E0):
        raise SystemExit(f"cave too large: {len(cave)} bytes")
    bl = _enc_bl(CODECVT_BLR_VA, CAVE_VA)
    print(
        f"hook {CODECVT_BLR_VA:#x}: blr x8 -> bl {CAVE_VA:#x} "
        f"(cave {len(cave)} bytes)"
    )

    if dry_run:
        print("dry-run: no file written")
        return

    if not bak.exists():
        bak.write_bytes(so_path.read_bytes())
        print(f"backup -> {bak}")

    data[blr_off : blr_off + 4] = bl
    data[cave_off : cave_off + len(cave)] = cave
    so_path.write_bytes(data)
    print(f"patched {so_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("so", type=Path, help="path to arm64 libRFLib.so")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    bak = Path(str(args.so) + BACKUP_SUFFIX)
    if not args.so.is_file() and bak.is_file():
        args.so.write_bytes(bak.read_bytes())
    if not args.so.is_file() and not bak.is_file():
        print(f"not found: {args.so}", file=sys.stderr)
        raise SystemExit(1)
    patch(args.so, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
