#!/usr/bin/env python3
"""Rebuild LoadingFonts RSG with CJK dialogue fonts and patch into OBB.

Appends a new pgsr at EOF (original slot is too small) and updates the RSB
group record for LoadingFonts (offset/csize/usize).
"""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

import zstandard as zstd
from fontTools.ttLib import TTFont

LF_GROUP_NAME_OFF = 0x2A9E68
# Group size fields (see dump around LoadingFonts)
LF_FILE_OFF_AT = 0x2A9EE8
LF_TOTAL_AT = 0x2A9EEC  # 0x1000 + csize
LF_CSIZE_AT = 0x2A9F00
LF_USIZE_AT = 0x2A9F04
LF_USIZE2_AT = 0x2A9F08
LF_TOTAL2_AT = 0x2A9F0C

# Map original path basename (upper) -> fonts_cjk file
FONT_FILES = {
    "ASHLEYSCRIPTMTSTD.TTF": "Ashley_Script_MT_Std.ttf",
    "BRIANNETOD.TTF": "BrianneTod.ttf",
    "CENTURY751.TTF": "Century751_SeBd_BT.ttf",
    "CROMAGNUMCONDENSED.TTF": "Cro-Magnum_Condensed.ttf",
    "FBUSV8C5EI.TTF": "fbUsv8C5eI.ttf",
    "HOUSE OF TERROR.TTF": "MonsterFonts-HouseofTerror.ttf",
    "INFROMAN.TTF": "Informal_Roman.ttf",
    "ITCBLKAD.TTF": "Blackadder_ITC.ttf",
    "NEWSFLASHBB.TTF": "Newsflash_BB.ttf",
    "PICO12__.TTF": "Pico12.ttf",
    "ROCKWELLCONDENSED.TTF": "Rockwell_Condensed.ttf",
    "ROGFONTS.TTF": "ROG_Fonts.ttf",
    "UNMASKEDBB.TTF": "Unmasked_BB.ttf",
}


def align(n: int, a: int = 0x1000) -> int:
    return (n + a - 1) & ~(a - 1)


def encode_path_u32(path: str) -> bytes:
    out = bytearray()
    for ch in path:
        out += struct.pack("<I", ord(ch))
    out += struct.pack("<I", 0)
    return bytes(out)


def build_payload(fonts_dir: Path) -> tuple[bytes, list[tuple[str, int, int]]]:
    """Return (raw font blob, [(path, offset, size), ...])."""
    # Preserve original path order from stock LoadingFonts
    paths = [
        r"\PRIMEFONTS\ASHLEYSCRIPTMTSTD.TTF",
        r"\PRIMEFONTS\BRIANNETOD.TTF",
        r"\PRIMEFONTS\CENTURY751.TTF",
        r"\PRIMEFONTS\CROMAGNUMCONDENSED.TTF",
        r"\PRIMEFONTS\FBUSV8C5EI.TTF",
        r"\PRIMEFONTS\HOUSE OF TERROR.TTF",
        r"\PRIMEFONTS\INFROMAN.TTF",
        r"\PRIMEFONTS\ITCBLKAD.TTF",
        r"\PRIMEFONTS\NEWSFLASHBB.TTF",
        r"\PRIMEFONTS\PICO12__.TTF",
        r"\PRIMEFONTS\ROCKWELLCONDENSED.TTF",
        r"\PRIMEFONTS\ROGFONTS.TTF",
        r"\PRIMEFONTS\UNMASKEDBB.TTF",
    ]
    blob = bytearray()
    entries: list[tuple[str, int, int]] = []
    for path in paths:
        base = path.rsplit("\\", 1)[-1].upper()
        src_name = FONT_FILES[base]
        data = (fonts_dir / src_name).read_bytes()
        # verify name table briefly
        try:
            TTFont(fonts_dir / src_name)
        except Exception as e:
            raise SystemExit(f"bad font {src_name}: {e}")
        while len(blob) % 0x1000:
            blob.append(0)
        off = len(blob)
        blob += data
        entries.append((path, off, len(data)))
        print(f"  {path} off={off:#x} size={len(data)}")
    return bytes(blob), entries


def build_info_section(entries: list[tuple[str, int, int]]) -> bytes:
    """Build RSG name pool (u32 codepoints + offset/size)."""
    body = bytearray()
    for path, off, size in entries:
        body += encode_path_u32(path)
        body += struct.pack("<III", 0, off, size)
    # Prefixed by pool size (bytes of body)
    return struct.pack("<I", len(body)) + bytes(body)


def build_pgsr(payload: bytes, info: bytes) -> tuple[bytes, int, int]:
    """Return (full pgsr bytes including header, csize, usize)."""
    # Info lives in first 0x1000 header page after 0x48-byte pgsr head
    header = bytearray(0x1000)
    # magic + ver
    header[0:4] = b"pgsr"
    struct.pack_into("<I", header, 4, 4)
    # compression flag 2 (zstd), header size fields like stock
    struct.pack_into("<I", header, 0x10, 2)
    struct.pack_into("<I", header, 0x14, 0x1000)
    struct.pack_into("<I", header, 0x18, 0x1000)
    # place info at 0x48
    if 0x48 + len(info) > 0x1000:
        raise SystemExit(f"info too large: {len(info)}")
    header[0x48 : 0x48 + len(info)] = info

    usize = len(payload)
    params = zstd.ZstdCompressionParameters.from_level(
        19, write_content_size=True, write_checksum=False
    )
    cctx = zstd.ZstdCompressor(compression_params=params)
    cobj = cctx.compressobj(size=usize)
    zblob = cobj.compress(payload) + cobj.flush()
    csize = len(zblob)
    # fill csize/usize into header like stock layout
    struct.pack_into("<I", header, 0x1C, csize)
    struct.pack_into("<I", header, 0x20, usize)
    struct.pack_into("<I", header, 0x28, csize + 0x1000)  # total approx

    pgsr = bytes(header) + zblob
    # pad total to 0x1000
    pad = (-len(pgsr)) % 0x1000
    pgsr += b"\x00" * pad
    return pgsr, csize, usize


def patch_obb(obb_path: Path, pgsr: bytes, csize: int, usize: int) -> None:
    data = bytearray(obb_path.read_bytes())
    new_off = len(data)
    # align append
    align_pad = (-new_off) % 0x1000
    data += b"\x00" * align_pad
    new_off = len(data)
    data += pgsr
    total = 0x1000 + csize
    # Prefer store unpadded logical total in catalog (stock used 0x255000 = 0x1000+0x254000)
    # Keep catalog total as 0x1000+csize; on-disk pgsr may have pad.
    struct.pack_into("<I", data, LF_FILE_OFF_AT, new_off)
    struct.pack_into("<I", data, LF_TOTAL_AT, total)
    struct.pack_into("<I", data, LF_CSIZE_AT, csize)
    struct.pack_into("<I", data, LF_USIZE_AT, usize)
    struct.pack_into("<I", data, LF_USIZE2_AT, usize)
    struct.pack_into("<I", data, LF_TOTAL2_AT, total)
    # Also patch embedded pgsr header copies of sizes already in pgsr
    obb_path.write_bytes(data)
    print(
        f"patched {obb_path.name}: LoadingFonts -> off={new_off:#x} "
        f"csize={csize:#x} usize={usize:#x} file_size={len(data)}"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts-dir", type=Path, default=Path(r"F:\sen_work\fonts_cjk"))
    ap.add_argument("--obb", type=Path, nargs="+", required=True)
    ap.add_argument(
        "--out-pgsr",
        type=Path,
        default=Path(r"F:\sen_work\LoadingFonts_cjk.pgsr"),
    )
    args = ap.parse_args()

    print("pack fonts")
    payload, entries = build_payload(args.fonts_dir)
    info = build_info_section(entries)
    print(f"payload {len(payload)} info {len(info)}")
    pgsr, csize, usize = build_pgsr(payload, info)
    args.out_pgsr.write_bytes(pgsr)
    print(f"wrote {args.out_pgsr} ({len(pgsr)}) csize={csize} usize={usize}")

    for obb in args.obb:
        patch_obb(obb, pgsr, csize, usize)


if __name__ == "__main__":
    main()
