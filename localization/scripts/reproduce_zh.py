#!/usr/bin/env python3
"""One-shot: stock Reflourished 1.4.2 OBB -> Chinese OBB + CDN LawnStrings RTON.

Uses in-repo translations / STAT / OBJ keys. Dialogue fonts: BLACK_* remap
(no fonts_cjk required). Pair the output OBB+RTON with a ZH APK that has the
CDN skip patch (Releases or 汉化教程 §6).

Example:
  python localization/scripts/reproduce_zh.py \\
    --obb F:\\path\\main.675.com.ea.game.pvz2_rfl.obb \\
    --out-dir F:\\out_zh
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
LOC = SCRIPTS.parent
REPO = LOC.parent
sys.path.insert(0, str(SCRIPTS))

from lawnstrings_rton import LAWNSTRINGS_SLOT, encode_rton_to_file  # noqa: E402
from obb_layout_142 import (  # noqa: E402
    OBB_MAGIC,
    OBB_NAME,
    OBB_VERSION,
    extract_packages_section,
    write_packages_section,
)
from patch_dialogue_font_compat import (  # noqa: E402
    alias_brianne_in_obb,
    remap_dialogue_fonts_in_section,
)
from patch_packages_almanac_literals import (  # noqa: E402
    patch_section as patch_almanac_section,
)
from patch_packages_objective_literals import (  # noqa: E402
    build_translation_table,
    discover_objective_literals,
)
from patch_packages_objective_literals import (  # noqa: E402
    patch_section as patch_objective_section,
)
from repack_obb_packages import patch_section as patch_lawnstrings_section  # noqa: E402
from sync_lawnstrings import sync  # noqa: E402


def _encode_current_rton(out_rton: Path, *, release_rton: Path | None) -> Path:
    flat = LOC / "LawnStrings_zh.json"
    if not flat.is_file():
        raise SystemExit(f"missing translations: {flat}")
    pairs = sync(
        flat_path=flat,
        current_dir=LOC / "current",
        order_from_rton=LOC / "current" / "LawnStrings_zh.rton",
        order_from_sen=LOC / "current" / "LawnStrings_zh_sen.json",
        stat_path=LOC / "almanac_stat_keys.json",
        obj_path=LOC / "objective_keys.json",
    )
    data = encode_rton_to_file(pairs, out_rton, slot_limit=LAWNSTRINGS_SLOT)
    # Keep localization/LawnStrings_zh.rton in sync
    root_rton = LOC / "LawnStrings_zh.rton"
    if out_rton.resolve() != root_rton.resolve():
        shutil.copy2(out_rton, root_rton)
    if release_rton is not None:
        release_rton.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out_rton, release_rton)
    print(
        f"RTON {out_rton} size={len(data)} "
        f"headroom={LAWNSTRINGS_SLOT - len(data)} pairs={len(pairs)}"
    )
    return out_rton


def _merge_keys_file(path: Path, new_keys: dict[str, str]) -> None:
    existing: dict[str, str] = {}
    if path.is_file():
        existing = json.loads(path.read_text(encoding="utf-8"))
    existing.update(new_keys)
    path.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"merged {len(new_keys)} keys -> {path} (total {len(existing)})")


def reproduce(obb: Path, out_dir: Path) -> None:
    if not obb.is_file():
        raise SystemExit(f"OBB not found: {obb}")
    raw_head = obb.read_bytes()[:4]
    if raw_head != OBB_MAGIC:
        raise SystemExit(f"not an RSB OBB (magic={raw_head!r}): {obb}")

    out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / "work"
    work.mkdir(parents=True, exist_ok=True)

    print("== 1/8 extract Packages ==")
    section = extract_packages_section(obb)
    stock_section = work / "packages_stock.bin"
    stock_section.write_bytes(section)
    print(f"section {len(section)} bytes -> {stock_section}")

    print("== 2/8 encode LawnStrings (pass 1) ==")
    out_rton = out_dir / "LawnStrings_zh.rton"
    cdn_rton = out_dir / "LawnStrings-en-us.rton"
    _encode_current_rton(out_rton, release_rton=cdn_rton)

    print("== 3/8 patch almanac STAT literals ==")
    section, counts, new_stat = patch_almanac_section(
        section, use_stat_refs=True, lawn_zh=None
    )
    print(
        f"almanac patched {sum(counts.values())} hits / {len(counts)} literals; "
        f"new STAT keys={len(new_stat)}"
    )
    _merge_keys_file(LOC / "almanac_stat_keys.json", new_stat)
    (work / "almanac_stat_keys_new.json").write_text(
        json.dumps(new_stat, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("== 4/8 patch objective OBJ literals ==")
    zh_map = json.loads((LOC / "LawnStrings_zh.json").read_text(encoding="utf-8"))
    en_path = LOC / "LawnStrings_en.json"
    en_map = (
        json.loads(en_path.read_text(encoding="utf-8")) if en_path.is_file() else {}
    )
    if not en_map:
        print(f"note: {en_path.name} missing — OBJ table uses EXTRA_ZH + zh only")
    discovered = discover_objective_literals(section)
    translations = build_translation_table(discovered, en=en_map, zh=zh_map)
    section, ocounts, new_obj = patch_objective_section(
        section, translations, None
    )
    print(
        f"objectives patched {sum(ocounts.values())} hits / {len(ocounts)} literals; "
        f"new OBJ keys={len(new_obj)}"
    )
    _merge_keys_file(LOC / "objective_keys.json", new_obj)
    (work / "objective_keys_new.json").write_text(
        json.dumps(new_obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    almanac_section = work / "packages_almanac_obj.bin"
    almanac_section.write_bytes(section)

    print("== 5/8 encode LawnStrings (pass 2, with STAT/OBJ) ==")
    _encode_current_rton(out_rton, release_rton=cdn_rton)

    print("== 6/8 inject LawnStrings x6 ==")
    section = patch_lawnstrings_section(section, out_rton.read_bytes())
    (work / "packages_with_lawn.bin").write_bytes(section)

    print("== 7/8 BLACK dialogue font remap ==")
    section = remap_dialogue_fonts_in_section(section)
    (work / "packages_final.bin").write_bytes(section)

    print("== 8/8 write OBB + obbVersion ==")
    out_obb = out_dir / OBB_NAME
    write_packages_section(obb, section, out_obb, already_compressed=False)
    obb_buf = bytearray(out_obb.read_bytes())
    alias_brianne_in_obb(obb_buf)
    out_obb.write_bytes(obb_buf)
    (out_dir / "obbVersion").write_text(OBB_VERSION, encoding="ascii")
    print(f"wrote {out_dir / 'obbVersion'!s} = {OBB_VERSION}")

    print()
    print("DONE")
    print(f"  OBB : {out_obb}")
    print(f"  RTON: {cdn_rton}")
    print(f"  ver : {out_dir / 'obbVersion'}")
    print()
    print("Install (pair with a ZH APK that has CDN skip patch):")
    print(f"  adb install -r <PvZ2_Reflourished_1.4.2_zh.apk>")
    print(
        f"  adb push \"{out_obb}\" "
        f"/sdcard/Android/obb/com.ea.game.pvz2_rfl/{OBB_NAME}"
    )
    print(
        f"  adb push \"{out_dir / 'obbVersion'}\" "
        f"/sdcard/Android/obb/com.ea.game.pvz2_rfl/obbVersion"
    )
    print(
        f"  adb push \"{cdn_rton}\" "
        "/sdcard/Android/data/com.ea.game.pvz2_rfl/files/No_Backup/"
        "CDN.1.4.2/LawnStrings-en-us.rton"
    )
    print(
        "  # Prefer launching the desktop icon (BootstrapActivity), "
        "not PvZ2GameActivity directly."
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--obb",
        type=Path,
        required=True,
        help="stock Reflourished 1.4.2 main.675….obb",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="output directory for zh OBB + CDN RTON",
    )
    args = ap.parse_args()
    reproduce(args.obb, args.out_dir)


if __name__ == "__main__":
    main()
