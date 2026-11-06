#!/usr/bin/env python3
"""Packages slot extract/write roundtrip for obb_layout_142."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from obb_layout_142 import (  # noqa: E402
    OBB_MAGIC,
    PACKAGES_CSIZE,
    PACKAGES_OFF,
    ZSTD_MAGIC,
    compress_packages_section,
    extract_packages_section,
    extract_packages_zstd,
    pad_to_csize,
    write_packages_section,
)

STOCK_OBB = Path(os.environ.get("PVZ2_STOCK_OBB", r"F:\sen_work\main.675.com.ea.game.pvz2_rfl.obb"))


def _fake_obb(section: bytes) -> bytes:
    blob = pad_to_csize(compress_packages_section(section))
    size = PACKAGES_OFF + PACKAGES_CSIZE
    data = bytearray(size)
    data[0:4] = OBB_MAGIC
    data[PACKAGES_OFF : PACKAGES_OFF + PACKAGES_CSIZE] = blob
    return bytes(data)


class TestObbLayout142(unittest.TestCase):
    def test_synthetic_extract_write_roundtrip(self) -> None:
        # Minimal section large enough to decompress roundtrip
        section = b"pvr3" + b"\x00" * 4092 + b"RTON" + b"\x00" * 1020
        obb = _fake_obb(section)
        got = extract_packages_section(obb)
        self.assertEqual(got, section)
        zst = extract_packages_zstd(obb)
        self.assertEqual(zst[:4], ZSTD_MAGIC)
        self.assertEqual(len(zst), PACKAGES_CSIZE)

        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out.obb"
            write_packages_section(obb, section, out, already_compressed=False)
            again = extract_packages_section(out)
            self.assertEqual(again, section)
            # Slot payload identical after write
            a = obb[PACKAGES_OFF : PACKAGES_OFF + PACKAGES_CSIZE]
            b = out.read_bytes()[PACKAGES_OFF : PACKAGES_OFF + PACKAGES_CSIZE]
            self.assertEqual(a, b)

    def test_pad_overflow(self) -> None:
        with self.assertRaises(ValueError):
            pad_to_csize(b"\x00" * (PACKAGES_CSIZE + 1))

    def test_stock_obb_slot_roundtrip(self) -> None:
        if not STOCK_OBB.is_file():
            raise unittest.SkipTest(f"no stock OBB at {STOCK_OBB}")
        zst = extract_packages_zstd(STOCK_OBB)
        section = extract_packages_section(STOCK_OBB)
        self.assertGreater(len(section), 1_000_000)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "roundtrip.obb"
            # Write already-compressed stock blob — slot bytes must match
            write_packages_section(
                STOCK_OBB, zst, out, already_compressed=True
            )
            again = extract_packages_zstd(out)
            self.assertEqual(again, zst)
            self.assertEqual(extract_packages_section(out), section)


if __name__ == "__main__":
    unittest.main()
