#!/usr/bin/env python3
"""Merge baokai_rewrite flavor/header outputs into LawnStrings_zh and batch zh files.

Expects:
  export_for_ai/almanac/baokai_rewrite/flavor_chunk_XXX.out.json
    { "KEY_DESCRIPTION": "{FLAVOR}...." }   # flavor body only OR full description
  export_for_ai/almanac/baokai_rewrite/header_chunk_XXX.out.json
    { "KEY_DESCRIPTION_HEADER": "..." }
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "export_for_ai" / "almanac" / "baokai_rewrite"
ZH_PATH = ROOT / "LawnStrings_zh.json"
EN_PATH = ROOT / "LawnStrings_en.json"
BATCH_DIR = ROOT / "export_for_ai" / "almanac"
MACRO_RE = re.compile(r"\{[A-Za-z_][^}]*\}")


def split_flavor(text: str) -> tuple[str, str]:
    idx = text.find("{FLAVOR}")
    if idx < 0:
        return text, ""
    return text[:idx], text[idx:]


def ensure_flavor_tag(body: str) -> str:
    body = body.strip()
    if not body.startswith("{FLAVOR}"):
        body = "{FLAVOR}" + body
    return body


def macros(s: str) -> list[str]:
    return sorted(MACRO_RE.findall(s))


def main() -> None:
    zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))

    flavor_outs = sorted(OUT.glob("flavor_chunk_*.out.json"))
    header_outs = sorted(OUT.glob("header_chunk_*.out.json"))
    if not flavor_outs:
        raise SystemExit(f"no flavor_chunk_*.out.json under {OUT}")

    flav_applied = 0
    for path in flavor_outs:
        obj = json.loads(path.read_text(encoding="utf-8"))
        for k, v in obj.items():
            if k not in en:
                print("WARN unknown", k)
                continue
            en_pre, _ = split_flavor(en[k])
            # Keep Chinese mechanism prefix if macros match; else keep EN prefix structure
            # translated prefix: prefer existing zh prefix when macro bag matches
            old = zh.get(k, en[k])
            old_pre, _ = split_flavor(old) if "{FLAVOR}" in old else (old, "")
            if macros(old) == macros(en[k]) and "{FLAVOR}" in old:
                prefix = old_pre
            else:
                # fall back: keep old_pre if it has CJK else empty+use en structure note
                prefix = old_pre if re.search(r"[\u4e00-\u9fff]", old_pre) else en_pre
            flav = ensure_flavor_tag(v if "{FLAVOR}" in v or not v.startswith("{") else v)
            # If value is full description with prefix, take only flavor part
            if "{KEYWORD}" in v or (v.count("{STAT}") > 0 and "{FLAVOR}" in v):
                _, flav = split_flavor(v)
                flav = ensure_flavor_tag(flav)
            # normalize newlines in join
            if prefix and not prefix.endswith(("\r\n", "\n")):
                joined = prefix.rstrip("\n") + "\r\n\r\n" + flav
            elif prefix:
                joined = prefix.rstrip("\r\n") + "\r\n\r\n" + flav
            else:
                joined = flav
            # Prefer CRLF like game strings
            joined = joined.replace("\r\n", "\n").replace("\n", "\r\n")
            zh[k] = joined
            flav_applied += 1

    hdr_applied = 0
    for path in header_outs:
        obj = json.loads(path.read_text(encoding="utf-8"))
        for k, v in obj.items():
            if k not in en:
                print("WARN unknown header", k)
                continue
            zh[k] = v.replace("\r\n", "\n").replace("\n", "\r\n")
            hdr_applied += 1

    ZH_PATH.write_text(
        json.dumps(zh, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {ZH_PATH}: flavors={flav_applied} headers={hdr_applied}")

    # refresh batch zh files from full zh for almanac keys
    for bn in ("almanac_001", "almanac_002", "almanac_003", "almanac_pilot"):
        en_batch_path = BATCH_DIR / f"{bn}.json"
        if not en_batch_path.is_file():
            continue
        en_batch = json.loads(en_batch_path.read_text(encoding="utf-8"))
        out = {k: zh.get(k, en_batch[k]) for k in en_batch}
        (BATCH_DIR / f"{bn}.zh.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"refreshed {bn}.zh.json ({len(out)})")


if __name__ == "__main__":
    main()
