#!/usr/bin/env python3
"""Parse LoadingFonts RSG file list from a PvZ2 Reflourished 1.4.2 OBB.

The name pool is a prefix-compressed uint32 stream (not plain UTF-32 paths).
This tool locates file records by (offset, size) meta triples and maps them to
known PRIMEFONTS basenames for 1.4.2.
"""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

import zstandard as zstd

LF_FILE_OFF_AT = 0x2A9EE8
LF_TOTAL_AT = 0x2A9EEC
LF_CSIZE_AT = 0x2A9F00
LF_USIZE_AT = 0x2A9F04
LF_USIZE2_AT = 0x2A9F08
LF_TOTAL2_AT = 0x2A9F0C
INFO_AT = 0x48
HDR_SIZE = 0x1000

# Stock LoadingFonts payload layout (1.4.2), basename upper -> (off, size)
STOCK_FONTS: dict[str, tuple[int, int]] = {
    "ASHLEYSCRIPTMTSTD.TTF": (0x0, 0x1C594),
    "BRIANNETOD.TTF": (0x1D000, 0xEA2C),
    "CENTURY751.TTF": (0x2C000, 0xD57C),
    "CROMAGNUMCONDENSED.TTF": (0x3A000, 0xD0E0),
    "FBUSV8C5EI.TTF": (0x48000, 0x3E4330),
    "HOUSE OF TERROR.TTF": (0x42D000, 0x2B7A0),
    "INFROMAN.TTF": (0x459000, 0x124D8),
    "ITCBLKAD.TTF": (0x46C000, 0x20514),
    "NEWSFLASHBB.TTF": (0x48D000, 0x6868),
    "PICO12__.TTF": (0x494000, 0x5D04),
    "ROCKWELLCONDENSED.TTF": (0x49A000, 0xDA10),
    "ROGFONTS.TTF": (0x4A8000, 0x281C),
    "UNMASKEDBB.TTF": (0x4AB000, 0xBFE4),
}


def find_meta(hdr: bytes, off: int, size: int) -> int | None:
    """Return absolute offset in hdr of the uint32 'off' field, or None."""
    needle = struct.pack("<II", off, size)
    # Prefer occurrences that look like pad=0, off, size (12 bytes)
    start = INFO_AT
    pos = start
    while True:
        idx = hdr.find(needle, pos)
        if idx < 0:
            return None
        if idx >= 4 and struct.unpack_from("<I", hdr, idx - 4)[0] == 0:
            return idx
        pos = idx + 4


def list_entries(hdr: bytes) -> list[dict]:
    out: list[dict] = []
    for name, (off, size) in STOCK_FONTS.items():
        at = find_meta(hdr, off, size)
        if at is None:
            # try scan any page-aligned off with this size only (already patched)
            out.append(
                {
                    "name": name,
                    "offset": off,
                    "size": size,
                    "off_field_at": None,
                    "size_field_at": None,
                    "found": False,
                }
            )
            continue
        out.append(
            {
                "name": name,
                "offset": off,
                "size": size,
                "off_field_at": at,
                "size_field_at": at + 4,
                "found": True,
            }
        )
    return out


def scan_all_metas(hdr: bytes) -> list[tuple[int, int, int]]:
    """Return (off_field_at, offset, size) for pad==0 metas in info region."""
    hits: list[tuple[int, int, int]] = []
    for i in range(INFO_AT, HDR_SIZE - 12, 4):
        pad, off, size = struct.unpack_from("<III", hdr, i)
        if (
            pad == 0
            and 0x1000 <= size <= 0x800000
            and off <= 0x800000
            and off % 0x1000 == 0
            and i >= INFO_AT + 4
            and struct.unpack_from("<I", hdr, i - 4)[0] == 0
        ):
            # i points at pad; off field at i+4
            hits.append((i + 4, off, size))
    return hits


def read_pgsr(obb: bytes, file_off: int) -> tuple[bytes, bytes, bytes]:
    hdr = obb[file_off : file_off + HDR_SIZE]
    if hdr[:4] != b"pgsr":
        raise SystemExit(f"no pgsr at {file_off:#x}")
    (csize,) = struct.unpack_from("<I", hdr, 0x1C)
    (usize,) = struct.unpack_from("<I", hdr, 0x20)
    zblob = obb[file_off + HDR_SIZE : file_off + HDR_SIZE + csize]
    payload = zstd.ZstdDecompressor().decompress(zblob, max_output_size=max(usize, 1) + 0x200000)
    return hdr, zblob, payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("obb", type=Path)
    ap.add_argument("--file-off", type=lambda x: int(x, 0), default=None)
    ap.add_argument(
        "--out-info",
        type=Path,
        default=Path(r"F:\sen_work\loadingfonts_stock_info.bin"),
    )
    ap.add_argument(
        "--out-header",
        type=Path,
        default=Path(r"F:\sen_work\loadingfonts_stock_header.bin"),
    )
    args = ap.parse_args()

    obb = args.obb.read_bytes()
    cat_off = struct.unpack_from("<I", obb, LF_FILE_OFF_AT)[0]
    cat_csize = struct.unpack_from("<I", obb, LF_CSIZE_AT)[0]
    cat_usize = struct.unpack_from("<I", obb, LF_USIZE_AT)[0]
    cat_total = struct.unpack_from("<I", obb, LF_TOTAL_AT)[0]
    print(f"obb={args.obb}")
    print(
        f"catalog: file_off={cat_off:#x} csize={cat_csize:#x} "
        f"usize={cat_usize:#x} total={cat_total:#x}"
    )

    file_off = args.file_off if args.file_off is not None else cat_off
    hdr, zblob, payload = read_pgsr(obb, file_off)
    print(f"using file_off={file_off:#x} zstd={len(zblob)} payload={len(payload)}")
    for off in (0x04, 0x10, 0x14, 0x18, 0x1C, 0x20, 0x28):
        (v,) = struct.unpack_from("<I", hdr, off)
        print(f"  hdr+{off:#x} = {v:#x}")

    (declared,) = struct.unpack_from("<I", hdr, INFO_AT)
    print(f"info+0 declared_u32={declared:#x} ({declared})")

    print("stock-mapped entries:")
    for e in list_entries(hdr):
        status = "OK" if e["found"] else "MISSING"
        at = e["off_field_at"]
        at_s = f"{at:#x}" if at is not None else "-"
        print(
            f"  [{status}] {e['name']:28s} off={e['offset']:#08x} "
            f"size={e['size']:#08x} off_field@{at_s}"
        )

    print("scanned metas (pad=0):")
    for at, off, size in scan_all_metas(hdr):
        print(f"  off_field@{at:#x} off={off:#x} size={size:#x}")

    # Export info from INFO_AT through last non-zero-ish region
    end = HDR_SIZE
    while end > INFO_AT + 16 and hdr[end - 16 : end] == b"\x00" * 16:
        end -= 16
    info = hdr[INFO_AT:end]
    args.out_info.write_bytes(info)
    args.out_header.write_bytes(hdr)
    print(f"wrote {args.out_info} ({len(info)} bytes)")
    print(f"wrote {args.out_header} ({len(hdr)} bytes)")


if __name__ == "__main__":
    main()
