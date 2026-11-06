#!/usr/bin/env python3
"""Shared apktool / build-tools / debug-keystore helpers for ZH APK builds."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

KS_ALIAS = "androiddebugkey"
KS_PASS = "android"


def run(cmd: list[str], **kwargs) -> None:
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True, **kwargs)


def require_cmd(*names: str) -> str:
    """Return first resolvable executable name (supports Windows .bat/.cmd)."""
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    listed = " / ".join(names)
    raise SystemExit(
        f"找不到命令: {listed}\n"
        "请安装后重试：apktool（如 choco install apktool）、"
        "JDK（keytool）、Android SDK build-tools。"
    )


def find_build_tools() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Android" / "Sdk" / "build-tools"
    if not base.is_dir():
        # Also try ANDROID_HOME / ANDROID_SDK_ROOT
        for env in ("ANDROID_HOME", "ANDROID_SDK_ROOT"):
            root = os.environ.get(env)
            if root:
                cand = Path(root) / "build-tools"
                if cand.is_dir():
                    base = cand
                    break
    if not base.is_dir():
        raise SystemExit(
            f"找不到 Android build-tools（期望 {base} 或 ANDROID_HOME/build-tools）。\n"
            "请安装 Android Studio / cmdline-tools 并确保含 zipalign 与 apksigner。"
        )
    versions = sorted(
        [p for p in base.iterdir() if p.is_dir()],
        key=lambda p: p.name,
        reverse=True,
    )
    for p in versions:
        zipalign = p / "zipalign.exe" if os.name == "nt" else p / "zipalign"
        apksigner = p / "apksigner.bat" if os.name == "nt" else p / "apksigner"
        if zipalign.is_file() and apksigner.is_file():
            return p
    raise SystemExit(f"No build-tools with zipalign/apksigner under {base}")


def ensure_debug_keystore(path: Path) -> Path:
    """Create Android debug keystore if missing (教程 §1.3)."""
    path = Path(path)
    if path.is_file():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    keytool = require_cmd("keytool")
    run(
        [
            keytool,
            "-genkeypair",
            "-v",
            "-keystore",
            str(path),
            "-alias",
            KS_ALIAS,
            "-keyalg",
            "RSA",
            "-keysize",
            "2048",
            "-validity",
            "10000",
            "-storepass",
            KS_PASS,
            "-keypass",
            KS_PASS,
            "-dname",
            "CN=Android Debug,O=Android,C=US",
        ]
    )
    print(f"created keystore {path}")
    return path


def apktool_decode(apk: Path, out_dir: Path, *, force: bool = True) -> Path:
    apktool = require_cmd("apktool", "apktool.bat")
    if out_dir.exists() and force:
        shutil.rmtree(out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    cmd = [apktool, "d"]
    if force:
        cmd.append("-f")
    cmd.extend([str(apk), "-o", str(out_dir)])
    run(cmd)
    return out_dir


def apktool_build(decoded: Path, unsigned: Path) -> None:
    apktool = require_cmd("apktool", "apktool.bat")
    unsigned.parent.mkdir(parents=True, exist_ok=True)
    if unsigned.exists():
        unsigned.unlink()
    run([apktool, "b", str(decoded), "-o", str(unsigned)])


def zipalign_sign(
    unsigned: Path,
    aligned: Path,
    signed: Path,
    keystore: Path,
    bt: Path | None = None,
) -> None:
    bt = bt or find_build_tools()
    if os.name == "nt":
        zipalign = bt / "zipalign.exe"
        apksigner = bt / "apksigner.bat"
    else:
        zipalign = bt / "zipalign"
        apksigner = bt / "apksigner"
    if aligned.exists():
        aligned.unlink()
    if signed.exists():
        signed.unlink()
    run([str(zipalign), "-f", "-p", "4", str(unsigned), str(aligned)])
    run(
        [
            str(apksigner),
            "sign",
            "--ks",
            str(keystore),
            "--ks-key-alias",
            KS_ALIAS,
            "--ks-pass",
            f"pass:{KS_PASS}",
            "--key-pass",
            f"pass:{KS_PASS}",
            "--out",
            str(signed),
            str(aligned),
        ]
    )
    run([str(apksigner), "verify", "--verbose", str(signed)])


def check_apk_deps() -> list[str]:
    """Return human-readable missing dependency messages (empty if OK)."""
    msgs: list[str] = []
    if not shutil.which("apktool") and not shutil.which("apktool.bat"):
        msgs.append("缺少 apktool（如: choco install apktool）")
    if not shutil.which("keytool"):
        msgs.append("缺少 keytool（安装 JDK 并加入 PATH）")
    try:
        find_build_tools()
    except SystemExit as e:
        msgs.append(str(e).split("\n")[0])
    return msgs
