#!/usr/bin/env python3
"""Smoke tests for apk_toolchain (skip when SDK / keytool absent)."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from apk_toolchain import (  # noqa: E402
    check_apk_deps,
    ensure_debug_keystore,
    find_build_tools,
)


class TestApkToolchain(unittest.TestCase):
    def test_check_apk_deps_returns_list(self) -> None:
        msgs = check_apk_deps()
        self.assertIsInstance(msgs, list)

    def test_find_build_tools(self) -> None:
        try:
            bt = find_build_tools()
        except SystemExit as e:
            raise unittest.SkipTest(str(e))
        self.assertTrue(bt.is_dir())

    def test_ensure_debug_keystore(self) -> None:
        if not shutil.which("keytool"):
            raise unittest.SkipTest("keytool not on PATH")
        with tempfile.TemporaryDirectory() as td:
            ks = Path(td) / "debug.keystore"
            ensure_debug_keystore(ks)
            self.assertTrue(ks.is_file())
            # second call is no-op
            ensure_debug_keystore(ks)
            self.assertTrue(ks.is_file())


if __name__ == "__main__":
    unittest.main()
