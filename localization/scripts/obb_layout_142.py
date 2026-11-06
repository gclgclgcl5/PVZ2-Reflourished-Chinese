#!/usr/bin/env python3
"""PvZ2 Reflourished 1.4.2 OBB slot layout + Packages extract/write helpers.

Centralizes offsets previously scattered across scripts and docs.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import zstandard as zstd

# ---------------------------------------------------------------------------
# Version / file identity
# ---------------------------------------------------------------------------

OBB_NAME = "main.675.com.ea.game.pvz2_rfl.obb"
OBB_VERSION = "1.4.2-r01"
OBB_MAGIC = b"1bsr"
ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"

# ---------------------------------------------------------------------------
# Packages RSG (compressed payload slot inside OBB)
# ---------------------------------------------------------------------------

PACKAGES_OFF = 0xCF55000
PACKAGES_CSIZE = 3522560  # in-place compressed slot size
# Aliases used by older scripts
PACK_OFF = PACKAGES_OFF
ORIG_CSIZE = PACKAGES_CSIZE

# Six identical LawnStrings blobs inside decompressed packages_section.bin
LAWNSTRINGS_STARTS = [1540096, 4206592, 6873088, 9539584, 12206080, 14872576]
LAWNSTRINGS_SLOT = 2666496

# ---------------------------------------------------------------------------
# LoadingFonts RSG
# ---------------------------------------------------------------------------

LOADINGFONTS_OFF = 0xB17B000
LOADINGFONTS_USIZE = 0x4B7000
LF_OFF = LOADINGFONTS_OFF


def _obb_bytes(obb: Path | bytes) -> bytes:
    if isinstance(obb, Path):
        return obb.read_bytes()
    return obb


def extract_packages_zstd(obb: Path | bytes) -> bytes:
    """Return the raw compressed Packages payload (length PACKAGES_CSIZE)."""
    data = _obb_bytes(obb)
    if data[:4] != OBB_MAGIC:
        raise ValueError(f"not an RSB/OBB (magic={data[:4]!r})")
    end = PACKAGES_OFF + PACKAGES_CSIZE
    if end > len(data):
        raise ValueError(
            f"OBB too small for Packages slot: len={len(data)} need>={end}"
        )
    blob = data[PACKAGES_OFF:end]
    if blob[:4] != ZSTD_MAGIC:
        raise ValueError(
            f"bad Packages magic at {PACKAGES_OFF:#x}: {blob[:4]!r}"
        )
    return blob


def extract_packages_section(obb: Path | bytes) -> bytes:
    """Decompress Packages RSG payload from OBB."""
    blob = extract_packages_zstd(obb)
    return zstd.ZstdDecompressor().decompress(blob)


def compress_packages_section(section: bytes) -> bytes:
    """Match original non-single-segment L19 frame (descriptor 0x80)."""
    params = zstd.ZstdCompressionParameters.from_level(
        19, write_content_size=True, write_checksum=False
    )
    cctx = zstd.ZstdCompressor(compression_params=params)
    cobj = cctx.compressobj(size=len(section))
    out = cobj.compress(section) + cobj.flush()
    if out[:4] != ZSTD_MAGIC:
        raise ValueError("compress_packages_section: not a zstd frame")
    fd = out[4]
    single = (fd >> 5) & 1
    print(
        f"zstd size={len(out)} desc=0x{fd:02x} single_segment={single} "
        f"delta_vs_orig={len(out) - PACKAGES_CSIZE:+d}"
    )
    if single != 0:
        print(
            "WARNING: single_segment=1; game may SIGSEGV. Prefer streaming L19."
        )
    return out


# Back-compat name used by older imports
compress_packages_zstd = compress_packages_section


def pad_to_csize(blob: bytes, csize: int = PACKAGES_CSIZE) -> bytes:
    if len(blob) > csize:
        raise ValueError(
            f"compressed Packages too large: {len(blob)} > slot {csize}"
        )
    if len(blob) < csize:
        return blob + b"\x00" * (csize - len(blob))
    return blob


def write_packages_section(
    obb_in: Path | bytes,
    section_or_zst: Path | bytes,
    obb_out: Path,
    *,
    already_compressed: bool = False,
) -> Path:
    """Write Packages payload back into a copy of the OBB.

    ``section_or_zst`` is decompressed section bytes unless
    ``already_compressed`` is True (then it must be a zstd blob ≤ csize).
    """
    if isinstance(obb_in, Path):
        data = bytearray(obb_in.read_bytes())
    else:
        data = bytearray(obb_in)

    if data[:4] != OBB_MAGIC:
        raise ValueError(f"not an RSB/OBB (magic={data[:4]!r})")

    raw = (
        section_or_zst.read_bytes()
        if isinstance(section_or_zst, Path)
        else section_or_zst
    )
    if already_compressed:
        blob = pad_to_csize(raw)
    else:
        blob = pad_to_csize(compress_packages_section(raw))

    end = PACKAGES_OFF + PACKAGES_CSIZE
    if end > len(data):
        raise ValueError(f"OBB too small for Packages slot: len={len(data)}")
    if data[PACKAGES_OFF : PACKAGES_OFF + 4] not in (ZSTD_MAGIC, blob[:4]):
        # Allow overwrite even if previous was corrupt, but warn
        if data[PACKAGES_OFF : PACKAGES_OFF + 4] != ZSTD_MAGIC:
            print(
                f"WARNING: Packages magic was "
                f"{bytes(data[PACKAGES_OFF:PACKAGES_OFF+4])!r}"
            )

    data[PACKAGES_OFF:end] = blob
    obb_out.parent.mkdir(parents=True, exist_ok=True)
    obb_out.write_bytes(data)
    print(f"wrote {obb_out} ({len(data)} bytes) Packages@{PACKAGES_OFF:#x}")
    return obb_out


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ex = sub.add_parser("extract", help="OBB -> decompressed packages_section.bin")
    p_ex.add_argument("obb", type=Path)
    p_ex.add_argument("-o", "--output", type=Path, required=True)
    p_ex.add_argument(
        "--zstd",
        type=Path,
        default=None,
        help="also write raw compressed Packages payload",
    )

    p_wr = sub.add_parser("write", help="write section or zstd back into OBB copy")
    p_wr.add_argument("obb_in", type=Path)
    p_wr.add_argument("payload", type=Path, help="decompressed section or .zst")
    p_wr.add_argument("-o", "--output", type=Path, required=True)
    p_wr.add_argument(
        "--compressed",
        action="store_true",
        help="payload is already zstd (skip recompress)",
    )

    args = ap.parse_args(argv)

    if args.cmd == "extract":
        section = extract_packages_section(args.obb)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(section)
        print(f"wrote section {args.output} ({len(section)} bytes)")
        if args.zstd:
            z = extract_packages_zstd(args.obb)
            args.zstd.write_bytes(z)
            print(f"wrote zstd {args.zstd} ({len(z)} bytes)")
        return

    if args.cmd == "write":
        write_packages_section(
            args.obb_in,
            args.payload,
            args.output,
            already_compressed=args.compressed,
        )
        return


if __name__ == "__main__":
    main()
