#!/usr/bin/env python3
"""Prepare flavor/header rewrite work packs from EN batches.

Each pack item:
  key, en_full, en_prefix, en_flavor, lock_name, old_zh_flavor (reference only)
Writes under export_for_ai/almanac/baokai_rewrite/
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "export_for_ai" / "almanac" / "baokai_rewrite"
EN = json.loads((ROOT / "LawnStrings_en.json").read_text(encoding="utf-8"))
ZH = json.loads((ROOT / "LawnStrings_zh.json").read_text(encoding="utf-8"))
LOCK = json.loads(
    (ROOT / "export_for_ai" / "almanac" / "almanac_name_lock.json").read_text(
        encoding="utf-8"
    )
)
CHUNK = 80


def split_flavor(text: str) -> tuple[str, str]:
    idx = text.find("{FLAVOR}")
    if idx < 0:
        return text, ""
    return text[:idx], text[idx:]


def entity_base(key: str) -> str:
    for suf in ("_DESCRIPTION_HEADER", "_DESCRIPTION", "_TOOLTIP"):
        if key.endswith(suf):
            return key[: -len(suf)]
    return key


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    flavors: list[dict] = []
    headers: list[dict] = []

    for bn in ("almanac_001", "almanac_002", "almanac_003"):
        batch = json.loads(
            (ROOT / "export_for_ai" / "almanac" / f"{bn}.json").read_text(
                encoding="utf-8"
            )
        )
        for k, ev in batch.items():
            base = entity_base(k)
            lock_name = LOCK.get(base, EN.get(base, base))
            if k.endswith("_DESCRIPTION") and not k.endswith("_HEADER") and "{FLAVOR}" in ev:
                pre, flav = split_flavor(ev)
                old = ZH.get(k, "")
                _, old_flav = split_flavor(old) if "{FLAVOR}" in old else ("", old)
                flavors.append(
                    {
                        "key": k,
                        "lock_name": lock_name,
                        "en_prefix": pre,
                        "en_flavor": flav,
                        "old_zh_flavor_ref_only": old_flav,
                        "old_zh_full_ref_only": old,
                    }
                )
            elif k.endswith("_DESCRIPTION_HEADER"):
                headers.append(
                    {
                        "key": k,
                        "lock_name": lock_name,
                        "en": ev,
                        "old_zh_ref_only": ZH.get(k, ""),
                    }
                )

    (OUT / "flavors_all.json").write_text(
        json.dumps(flavors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "headers_all.json").write_text(
        json.dumps(headers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    for i in range(0, len(flavors), CHUNK):
        chunk = flavors[i : i + CHUNK]
        idx = i // CHUNK + 1
        (OUT / f"flavor_chunk_{idx:03d}.json").write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    for i in range(0, len(headers), CHUNK):
        chunk = headers[i : i + CHUNK]
        idx = i // CHUNK + 1
        (OUT / f"header_chunk_{idx:03d}.json").write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(
        f"flavors={len(flavors)} headers={len(headers)} "
        f"flavor_chunks={(len(flavors)+CHUNK-1)//CHUNK} "
        f"header_chunks={(len(headers)+CHUNK-1)//CHUNK} -> {OUT}"
    )


if __name__ == "__main__":
    main()
