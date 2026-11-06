#!/usr/bin/env python3
"""One-shot: sync LawnStrings -> encode RTON (-> optional Packages section)."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from lawnstrings_rton import LAWNSTRINGS_SLOT, encode_rton_to_file
from sync_lawnstrings import sync

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CURRENT = ROOT / "current"
DEFAULT_RELEASE_RTON = ROOT.parent / "release_zh" / "LawnStrings-en-us.rton"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--current", type=Path, default=DEFAULT_CURRENT)
    ap.add_argument(
        "--out-rton",
        type=Path,
        default=None,
        help="default: current/LawnStrings_zh.rton",
    )
    ap.add_argument(
        "--release-rton",
        type=Path,
        default=DEFAULT_RELEASE_RTON,
        help="also copy CDN-named RTON here (empty string to skip)",
    )
    ap.add_argument(
        "--no-release-copy",
        action="store_true",
        help="do not copy to release_zh/LawnStrings-en-us.rton",
    )
    ap.add_argument(
        "--repack-section",
        nargs=2,
        metavar=("SECTION_IN", "SECTION_OUT"),
        help="run repack_obb_packages.py SECTION_IN OUT_RTON -> SECTION_OUT",
    )
    ap.add_argument(
        "--skip-sync",
        action="store_true",
        help="encode from existing current sen/flat without rewriting",
    )
    args = ap.parse_args()

    current = args.current
    out_rton = args.out_rton or (current / "LawnStrings_zh.rton")

    if args.skip_sync:
        from lawnstrings_rton import decode_rton_pairs, load_json_pairs

        # Prefer re-encoding the existing RTON (stable). Fall back to sen/flat JSON.
        existing = out_rton if out_rton.is_file() else (current / "LawnStrings_zh.rton")
        sen_path = current / "LawnStrings_zh_sen.json"
        flat_path = current / "LawnStrings_zh.json"
        if existing.is_file():
            pairs = decode_rton_pairs(existing)
            print(f"skip-sync: loaded {len(pairs)} pairs from RTON {existing}")
        else:
            src = sen_path if sen_path.is_file() else flat_path
            pairs = load_json_pairs(src)
            print(f"skip-sync: loaded {len(pairs)} pairs from {src}")
    else:
        pairs = sync(current_dir=current)

    data = encode_rton_to_file(pairs, out_rton, slot_limit=LAWNSTRINGS_SLOT)

    # Sidecar baseline for tests / audits
    meta = {
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
        "strings": len(pairs) * 2,
        "ordered_pairs": len(pairs),
        "unique_keys_dict": len(dict(pairs)),
    }
    (out_rton.parent / (out_rton.name + ".golden.json")).write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )

    # Keep repo root localization/LawnStrings_zh.rton in sync when writing current/
    root_rton = ROOT / "LawnStrings_zh.rton"
    if out_rton.resolve() != root_rton.resolve():
        shutil.copy2(out_rton, root_rton)
        print(f"copied {root_rton}")

    if not args.no_release_copy and args.release_rton is not None:
        args.release_rton.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out_rton, args.release_rton)
        print(f"copied {args.release_rton}")

    print(
        f"RTON {out_rton} size={len(data)} "
        f"headroom={LAWNSTRINGS_SLOT - len(data)} pairs={len(pairs)}"
    )

    if args.repack_section:
        section_in, section_out = map(Path, args.repack_section)
        cmd = [
            sys.executable,
            str(Path(__file__).with_name("repack_obb_packages.py")),
            str(section_in),
            str(out_rton),
            str(section_out),
        ]
        print("repack:", " ".join(cmd))
        subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
