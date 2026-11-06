#!/usr/bin/env python3
"""Build a single installable ZH APK with embedded OBB + CDN LawnStrings seed.

Pipeline:
  1) apktool b work/apk_decoded  (bootstrap Activity, no large assets)
  2) ZIP_STORED inject OBB + RTON + version marker into unsigned APK
  3) zipalign + apksigner

Does NOT place the ~1.3GB OBB into the apktool project tree.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

from apk_toolchain import (
    apktool_build,
    find_build_tools,
    zipalign_sign,
)

REPO = Path(__file__).resolve().parents[2]
DEFAULT_DECODED = REPO / "work" / "apk_decoded"
DEFAULT_OBB = Path(r"F:\sen_work\main_schemeA_almanac.obb")
DEFAULT_RTON_CANDIDATES = [
    Path(r"F:\sen_work\current\LawnStrings-en-us.rton"),
    Path(r"F:\sen_work\LawnStrings_zh.rton"),
]
DEFAULT_KEYSTORE = Path(r"F:\sen_work\debug.keystore")
DEFAULT_OUT = Path(r"F:\sen_work\PvZ2_Reflourished_1.4.2_zh_allinone.apk")
OBB_ASSET = "assets/obb/main.675.com.ea.game.pvz2_rfl.obb"
RTON_ASSET = "assets/cdn/LawnStrings-en-us.rton"
VERSION_ASSET = "assets/pvz2_zh_payload.version"


def resolve_rton(explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.is_file():
            raise SystemExit(f"RTON not found: {explicit}")
        return explicit
    for p in DEFAULT_RTON_CANDIDATES:
        if p.is_file():
            return p
    raise SystemExit("No LawnStrings RTON found (current/ or LawnStrings_zh.rton)")


def file_md5(path: Path, chunk: int = 8 * 1024 * 1024) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def inject_stored_assets(
    unsigned_in: Path,
    unsigned_out: Path,
    obb: Path,
    rton: Path,
    version: str,
) -> None:
    if unsigned_out.exists():
        unsigned_out.unlink()
    with zipfile.ZipFile(unsigned_in, "r") as zin, zipfile.ZipFile(
        unsigned_out, "w", compression=zipfile.ZIP_DEFLATED
    ) as zout:
        for info in zin.infolist():
            if info.filename in (OBB_ASSET, RTON_ASSET, VERSION_ASSET):
                continue
            data = zin.read(info.filename)
            out_info = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
            out_info.compress_type = info.compress_type
            out_info.external_attr = info.external_attr
            out_info.create_system = info.create_system
            zout.writestr(out_info, data)

        def add_stored(
            arcname: str, path: Path | None = None, data: bytes | None = None
        ) -> None:
            info = zipfile.ZipInfo(arcname)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            if path is not None:
                print(f"  + STORED {arcname} ({path.stat().st_size} bytes)", flush=True)
                with path.open("rb") as f, zout.open(info, "w") as dest:
                    shutil.copyfileobj(f, dest, length=8 * 1024 * 1024)
            else:
                assert data is not None
                print(f"  + STORED {arcname} ({len(data)} bytes)", flush=True)
                zout.writestr(info, data)

        add_stored(VERSION_ASSET, data=(version + "\n").encode("utf-8"))
        add_stored(RTON_ASSET, path=rton)
        add_stored(OBB_ASSET, path=obb)


def verify_embedded(signed: Path, obb: Path, rton: Path) -> None:
    with zipfile.ZipFile(signed, "r") as z:
        for name, expected in (
            (OBB_ASSET, obb.stat().st_size),
            (RTON_ASSET, rton.stat().st_size),
            (VERSION_ASSET, None),
        ):
            info = z.getinfo(name)
            if info.compress_type != zipfile.ZIP_STORED:
                raise SystemExit(
                    f"{name} is not STORED (compress_type={info.compress_type})"
                )
            if expected is not None and info.file_size != expected:
                raise SystemExit(
                    f"{name} size mismatch: apk={info.file_size} file={expected}"
                )
            print(f"OK embedded {name} size={info.file_size} stored", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--decoded", type=Path, default=DEFAULT_DECODED)
    ap.add_argument("--obb", type=Path, default=DEFAULT_OBB)
    ap.add_argument("--rton", type=Path, default=None)
    ap.add_argument("--keystore", type=Path, default=DEFAULT_KEYSTORE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument(
        "--version",
        default=None,
        help="payload version string (default: md5 of OBB+RTON sizes)",
    )
    ap.add_argument(
        "--skip-apktool",
        action="store_true",
        help="reuse existing unsigned base APK next to --out",
    )
    args = ap.parse_args()

    if not args.decoded.is_dir():
        raise SystemExit(f"decoded APK dir missing: {args.decoded}")
    if not args.obb.is_file():
        raise SystemExit(f"OBB missing: {args.obb}")
    rton = resolve_rton(args.rton)
    if not args.keystore.is_file():
        raise SystemExit(f"keystore missing: {args.keystore}")

    version = args.version
    if not version:
        version = f"1.4.2-almanac-{file_md5(rton)[:12]}-obb{args.obb.stat().st_size}"

    work = args.out.parent
    unsigned_base = work / "PvZ2_RFL_zh_allinone_base_unsigned.apk"
    unsigned_fat = work / "PvZ2_RFL_zh_allinone_unsigned.apk"
    aligned = work / "PvZ2_RFL_zh_allinone_aligned.apk"

    print(f"decoded : {args.decoded}")
    print(f"obb     : {args.obb} ({args.obb.stat().st_size})")
    print(f"rton    : {rton} ({rton.stat().st_size})")
    print(f"version : {version}")
    print(f"out     : {args.out}")

    if not args.skip_apktool:
        apktool_build(args.decoded, unsigned_base)
    elif not unsigned_base.is_file():
        raise SystemExit(f"--skip-apktool but missing {unsigned_base}")

    print("Injecting STORED assets…", flush=True)
    inject_stored_assets(unsigned_base, unsigned_fat, args.obb, rton, version)

    bt = find_build_tools()
    print(f"build-tools: {bt}", flush=True)
    zipalign_sign(unsigned_fat, aligned, args.out, args.keystore, bt)
    verify_embedded(args.out, args.obb, rton)
    print(f"DONE {args.out} ({args.out.stat().st_size} bytes)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
