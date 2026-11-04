#!/usr/bin/env python3
"""Patch English StarChallenge Description literals inside level .rton files.

CDN downloads under files/No_Backup/CDN.*/levels/** override OBB Packages levels.
Those RTONs often embed raw ``0x90`` English Description strings. Rewrite them to
equal-length ``[OBJ_…]`` tokens using the same map as
``patch_packages_objective_literals.py`` (requires matching LawnStrings keys).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Reuse translation / token helpers from packages patcher
sys.path.insert(0, str(Path(__file__).resolve().parent))
from patch_packages_objective_literals import (  # noqa: E402
    EXTRA_ZH,
    make_obj_ref,
    starchallenge_en_to_zh,
)


def build_rewrites(en: dict, zh: dict) -> dict[str, tuple[bytes, str, str]]:
    """eng → (ascii_repl_including_brackets, bare_key, chinese)."""
    table = starchallenge_en_to_zh(en, zh)
    table.update(EXTRA_ZH)
    used: set[str] = set()
    out: dict[str, tuple[bytes, str, str]] = {}
    for eng in sorted(table.keys(), key=len, reverse=True):
        try:
            eng.encode("ascii")
        except UnicodeEncodeError:
            continue
        if len(eng) < 6:
            continue
        ref, key = make_obj_ref(eng, used)
        out[eng] = (ref.encode("ascii"), key, table[eng])
    return out


def patch_file(path: Path, rewrites: dict[str, tuple[bytes, str, str]]) -> int:
    data = bytearray(path.read_bytes())
    n = 0
    for eng, (repl, _key, _zh) in rewrites.items():
        needle = eng.encode("ascii")
        if len(needle) != len(repl):
            continue
        start = 0
        while True:
            i = data.find(needle, start)
            if i < 0:
                break
            if i >= 2 and data[i - 2] == 0x90 and data[i - 1] == len(needle):
                data[i : i + len(needle)] = repl
                n += 1
                start = i + len(needle)
            else:
                start = i + 1
    if n:
        path.write_bytes(data)
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=Path, help="directory of level .rton files")
    ap.add_argument("--lawnstrings-en", type=Path, required=True)
    ap.add_argument("--lawnstrings-zh", type=Path, required=True)
    args = ap.parse_args()

    en = json.loads(args.lawnstrings_en.read_text(encoding="utf-8"))
    zh = json.loads(args.lawnstrings_zh.read_text(encoding="utf-8"))
    rewrites = build_rewrites(en, zh)

    files = list(args.root.rglob("*.rton"))
    total = 0
    touched = 0
    for p in files:
        c = patch_file(p, rewrites)
        if c:
            touched += 1
            total += c
            print(f"  {c:3d}  {p}")
    print(f"patched {total} literals in {touched}/{len(files)} files")


if __name__ == "__main__":
    main()
