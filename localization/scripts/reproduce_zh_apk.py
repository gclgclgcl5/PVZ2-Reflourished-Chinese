#!/usr/bin/env python3
"""One-shot: stock Reflourished 1.4.2 APK -> ZH signed APK (CDN skip + Glyph).

Does NOT embed OBB. Pair with reproduce_zh.py output (OBB + CDN RTON).

Example:
  python localization/scripts/reproduce_zh_apk.py \\
    --apk path\\to\\PvZ2_Reflourished_1.4.2.apk \\
    --out-dir F:\\out_zh
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from apk_toolchain import (  # noqa: E402
    apktool_build,
    apktool_decode,
    check_apk_deps,
    ensure_debug_keystore,
    find_build_tools,
    zipalign_sign,
)
from patch_cdn_lawnstrings_skip import patch as patch_cdn  # noqa: E402
from patch_glyph_cache_clear import patch as patch_glyph  # noqa: E402

ZH_APK_NAME = "PvZ2_Reflourished_1.4.2_zh.apk"
APP_NAME_ZH = "植物大战僵尸2：返茂"
SO_REL = Path("lib") / "arm64-v8a" / "libPVZ2.so"


def _set_app_name(decoded: Path, name: str = APP_NAME_ZH) -> None:
    strings = decoded / "res" / "values" / "strings.xml"
    if not strings.is_file():
        print(f"WARNING: missing {strings}; skip app_name")
        return
    text = strings.read_text(encoding="utf-8")
    pat = re.compile(
        r'(<string\s+name="app_name">)(.*?)(</string>)',
        re.DOTALL,
    )
    if not pat.search(text):
        print("WARNING: app_name not found in strings.xml; skip")
        return
    new_text, n = pat.subn(rf"\g<1>{name}\g<3>", text, count=1)
    if n:
        strings.write_text(new_text, encoding="utf-8")
        print(f"app_name -> {name}")


def reproduce(
    apk: Path,
    out_dir: Path,
    *,
    keystore: Path | None = None,
    force_decode: bool = True,
) -> Path:
    if not apk.is_file():
        raise SystemExit(f"APK not found: {apk}")

    missing = check_apk_deps()
    if missing:
        raise SystemExit("依赖检查失败:\n- " + "\n- ".join(missing))

    out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / "apk_work"
    decoded = work / "apk_decoded"
    ks = ensure_debug_keystore(keystore or (out_dir / "debug.keystore"))
    bt = find_build_tools()
    print(f"build-tools: {bt}")

    print("== 1/5 apktool decode ==")
    apktool_decode(apk, decoded, force=force_decode)

    so = decoded / SO_REL
    if not so.is_file():
        raise SystemExit(f"missing {so} (need arm64-v8a Reflourished 1.4.2 APK)")

    print("== 2/5 CDN LawnStrings skip ==")
    patch_cdn(so)

    print("== 3/5 Glyph cache clear ==")
    patch_glyph(so)

    print("== 4/5 app_name ==")
    _set_app_name(decoded)

    print("== 5/5 build + zipalign + sign ==")
    unsigned = work / "PvZ2_RFL_zh_unsigned.apk"
    aligned = work / "PvZ2_RFL_zh_aligned.apk"
    signed = out_dir / ZH_APK_NAME
    apktool_build(decoded, unsigned)
    zipalign_sign(unsigned, aligned, signed, ks, bt)

    print()
    print("DONE")
    print(f"  APK: {signed}")
    print()
    print("Install notes:")
    print("  - 若设备上已有不同签名的同包名，先卸载 com.ea.game.pvz2_rfl")
    print(f'  adb install -r "{signed}"')
    print("  - 仍需汉化 OBB + CDN RTON（reproduce_zh.py / GUI）")
    return signed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--apk",
        type=Path,
        required=True,
        help="stock Reflourished 1.4.2 APK",
    )
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument(
        "--keystore",
        type=Path,
        default=None,
        help="default: out-dir/debug.keystore (auto-create)",
    )
    ap.add_argument(
        "--keep-decoded",
        action="store_true",
        help="do not force-delete existing apk_decoded before decode",
    )
    args = ap.parse_args()
    reproduce(
        args.apk,
        args.out_dir,
        keystore=args.keystore,
        force_decode=not args.keep_decoded,
    )


if __name__ == "__main__":
    main()
