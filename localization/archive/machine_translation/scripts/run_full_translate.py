#!/usr/bin/env python3
"""Translate all batches then import into LawnStrings_zh.json."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
EXPORT = ROOT / "export_for_ai"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.check_call(cmd)


def main() -> None:
    py = sys.executable
    # Translate all
    run([py, str(SCRIPTS / "translate_batches.py"), "--from", "1", "--to", "999"])
    # Import all zh
    zh_files = sorted(EXPORT.glob("batch_*.zh.json"))
    if not zh_files:
        raise SystemExit("no batch_*.zh.json produced")
    run([py, str(SCRIPTS / "import_ai_translations.py"), "--dir", str(EXPORT)])
    run([py, str(SCRIPTS / "qa_translations.py")])


if __name__ == "__main__":
    main()
