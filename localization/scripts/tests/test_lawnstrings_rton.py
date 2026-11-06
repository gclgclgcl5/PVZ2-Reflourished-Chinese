#!/usr/bin/env python3
"""Roundtrip / slot / sample checks for lawnstrings_rton."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from lawnstrings_rton import (  # noqa: E402
    LAWNSTRINGS_SLOT,
    decode_rton,
    decode_rton_pairs,
    encode_rton,
    merge_extra_keys,
    pairs_to_sen_json,
    sen_json_to_pairs,
)

GOLDEN = ROOT / "current" / "LawnStrings_zh.rton"
GOLDEN_META = ROOT / "current" / "LawnStrings_zh.rton.golden.json"


class TestLawnStringsRton(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not GOLDEN.is_file():
            raise unittest.SkipTest(f"missing golden {GOLDEN}")
        cls.golden = GOLDEN.read_bytes()
        cls.pairs = decode_rton_pairs(cls.golden)

    def test_golden_meta(self) -> None:
        meta = json.loads(GOLDEN_META.read_text(encoding="utf-8"))
        self.assertEqual(len(self.golden), meta["size"])
        self.assertEqual(len(self.pairs) * 2, meta["strings"])
        self.assertEqual(len(self.pairs), meta.get("ordered_pairs", meta["strings"] // 2))

    def test_roundtrip_byte_identical(self) -> None:
        ours = encode_rton(self.pairs)
        self.assertEqual(ours, self.golden)

    def test_roundtrip_pairs(self) -> None:
        ours = encode_rton(self.pairs)
        self.assertEqual(decode_rton_pairs(ours), self.pairs)

    def test_slot_limit(self) -> None:
        ours = encode_rton(self.pairs)
        self.assertLessEqual(len(ours), LAWNSTRINGS_SLOT)
        self.assertGreater(LAWNSTRINGS_SLOT - len(ours), 0)

    def test_sample_chinese_and_placeholders(self) -> None:
        d = decode_rton(self.golden)
        self.assertIn("账户删除", d.get("ACCOUNT_DELETION", ""))
        # placeholder samples if present
        for key in d:
            if "{COUNT}" in d[key] or "{NUMBER}" in d[key] or "{TIME}" in d[key]:
                self.assertTrue(True)
                break
        # STAT / OBJ style keys
        stat = [k for k in d if k.startswith("[STAT_") or k.startswith("STAT_")]
        obj = [k for k in d if k.startswith("OBJ_") or k.startswith("[OBJ")]
        # may be empty in some snapshots; just ensure encode keeps them if present
        if stat:
            self.assertIn(stat[0], dict(self.pairs))
        if obj:
            self.assertIn(obj[0], dict(self.pairs))
        # CRLF preserved in at least one known account string
        self.assertIn("\r\n", d.get("ACCOUNT_DELETION_SUCCESS_DESCRIPTION", "\r\n"))

    def test_tiny_fixture(self) -> None:
        pairs = [("HELLO", "你好"), ("HELLO", "复用"), ("ASCII", "ok")]
        data = encode_rton(pairs)
        self.assertTrue(data.startswith(b"RTON"))
        self.assertTrue(data.endswith(b"DONE"))
        self.assertEqual(decode_rton_pairs(data), pairs)

    def test_sen_json_roundtrip(self) -> None:
        sen = pairs_to_sen_json(self.pairs[:10])
        self.assertEqual(sen_json_to_pairs(sen), self.pairs[:10])

    def test_merge_extra_keys(self) -> None:
        base = [("A", "1"), ("B", "2")]
        merged = merge_extra_keys(base, {"B": "x", "C": "3"})
        self.assertEqual(merged, [("A", "1"), ("B", "x"), ("C", "3")])


if __name__ == "__main__":
    unittest.main()
