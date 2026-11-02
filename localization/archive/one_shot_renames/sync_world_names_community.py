# -*- coding: utf-8 -*-
"""Unify WORLD_NAME_* and in-text world mentions to community Chinese names."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"F:\othergit\Reverse Engineer Anything")
ZH_PATH = ROOT / "localization" / "LawnStrings_zh.json"

WORLD = {
    "WORLD_NAME_CARNIVAL": "昏暗嘉年华",
    "WORLD_NAME_FAIRYTALE": "童话森林",
    "WORLD_NAME_HOLIDAY": "节日串烧",
    "WORLD_NAME_HOLLOWS": "低温空洞",
    "WORLD_NAME_SKYCITY": "侵袭空域",
    "WORLD_NAME_STEAM": "蒸汽时代",
    "WORLD_NAME_TRAVELLOG": "旅行日志的游客陷阱",
    "WORLD_NAME_TRAVELLOG_MARKET": "月虹市场",
    "WORLD_NAME_COMING_SOON": "？？？",
}

PREVIEW = {
    "WORLD_PREVIEW_CARNIVAL_TITLE": "昏暗嘉年华！",
    "WORLD_PREVIEW_FAIRYTALE_TITLE": "童话森林！",
    "WORLD_PREVIEW_HOLIDAY_TITLE": "节日串烧！",
    "WORLD_PREVIEW_HOLLOWS_TITLE": "低温空洞！",
    "WORLD_PREVIEW_SKYCITY_TITLE": "侵袭空域！",
    "WORLD_PREVIEW_STEAM_TITLE": "蒸汽时代！",
    "WORLD_PREVIEW_TRAVELLOG_TITLE": "旅行日志的游客陷阱！",
    "WORLD_PREVIEW_TRAVELLOG_MARKET_TITLE": "月虹市场！",
    "WORLD_PREVIEW_DINO_TITLE": "侏罗纪沼泽！",
    "WORLD_PREVIEW_EIGHTIES_TITLE": "炫光魔音游！",
    "WORLD_PREVIEW_MODERN_TITLE": "现代年华！",
}

# Longer / more specific first
PHRASES: list[tuple[str, str]] = [
    ("Caliginous Carnival", "昏暗嘉年华"),
    ("Caliginous嘉年华", "昏暗嘉年华"),
    ("Caliginous 嘉年华", "昏暗嘉年华"),
    ("卡利吉诺斯嘉年华", "昏暗嘉年华"),
    ("卡利金努斯嘉年华", "昏暗嘉年华"),
    ("卡里吉诺斯嘉年华", "昏暗嘉年华"),
    ("卡利吉尼斯嘉年华", "昏暗嘉年华"),
    ("卡里吉尼斯嘉年华", "昏暗嘉年华"),
    ("卡利吉努斯嘉年华", "昏暗嘉年华"),
    ("嗜食嘉年华", "昏暗嘉年华"),
    ("邪恶嘉年华", "昏暗嘉年华"),
    ("疯狂的嘉年华", "昏暗嘉年华"),
    ("疯狂嘉年华", "昏暗嘉年华"),
    ("Fairytale Forest", "童话森林"),
    ("Holiday Mashup", "节日串烧"),
    ("节假日串烧", "节日串烧"),
    ("节庆串烧", "节日串烧"),
    ("Assault Airspace", "侵袭空域"),
    ("突击空域", "侵袭空域"),
    ("Lunar Rainbow Market", "月虹市场"),
    ("农历彩虹市场", "月虹市场"),
    ("Hypothermic Hollows", "低温空洞"),
    ("Steam Ages", "蒸汽时代"),
    ("旅行日志的旅游陷阱", "旅行日志的游客陷阱"),
    ("Travel Log's Tourist Trap", "旅行日志的游客陷阱"),
    ("农历彩虹市集", "月虹市场"),
    ("农历彩虹集市", "月虹市场"),
    ("The Lunar Rainbow Market arrives!", "月虹市场来啦！"),
    ("Caliginous 狂欢之夜", "昏暗嘉年华"),
    ("Caliginous 挑战", "昏暗嘉年华挑战"),
    ("Caliginous挑战", "昏暗嘉年华挑战"),
    ("昏暗狂欢节", "昏暗嘉年华"),
    ("卡里吉尼斯狂欢节", "昏暗嘉年华"),
    ("卡利吉努斯狂欢节", "昏暗嘉年华"),
    ("卡里吉斯狂欢节", "昏暗嘉年华"),
    ("卡利吉尼斯狂欢节", "昏暗嘉年华"),
    ("卡利金努斯狂欢节", "昏暗嘉年华"),
    ("\u201c\u5361\u91cc\u5409\u65af\u201d\u72c2\u6b22\u8282", "\u201c\u660f\u6697\u5609\u5e74\u534e\u201d"),
]


def apply_phrases(text: str, phrase_hits: dict[str, int]) -> str:
    nv = text
    for old, new in PHRASES:
        if old in nv:
            phrase_hits[old] = phrase_hits.get(old, 0) + nv.count(old)
            nv = nv.replace(old, new)
    return nv


def main() -> None:
    zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    phrase_hits: dict[str, int] = {}
    changed_keys = 0
    updates = {**WORLD, **PREVIEW}

    for k, v in list(zh.items()):
        if not isinstance(v, str):
            continue
        if k in updates:
            nv = updates[k]
        else:
            nv = apply_phrases(v, phrase_hits)
        if nv != v:
            zh[k] = nv
            changed_keys += 1

    ZH_PATH.write_text(
        json.dumps(zh, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("keys changed", changed_keys)
    print("phrase hits:")
    for old, new in PHRASES:
        n = phrase_hits.get(old, 0)
        if n:
            print(f"  {n:4d} {old!r} -> {new!r}")

    print("\nWORLD_NAME_*:")
    for k in sorted(zh):
        if k.startswith("WORLD_NAME_"):
            print(f"  {k}: {zh[k]}")

    sen_paths = [
        ROOT / "localization" / "current" / "LawnStrings_zh_sen.json",
        Path(r"F:\sen_work\LawnStrings_zh_penny_sen.json"),
        Path(r"F:\sen_work\LawnStrings_zh_good_almanac_sen.json"),
        Path(r"F:\sen_work\current\LawnStrings_zh_sen.json"),
    ]
    for sp in sen_paths:
        if not sp.exists():
            continue
        sen = json.loads(sp.read_text(encoding="utf-8"))
        vals = sen["objects"][0]["objdata"]["LocStringValues"]
        n = 0
        for i in range(0, len(vals), 2):
            key = vals[i]
            val = vals[i + 1]
            if not isinstance(val, str):
                continue
            if key in updates:
                nv = updates[key]
            else:
                nv = apply_phrases(val, {})
            if nv != val:
                vals[i + 1] = nv
                n += 1
        sp.write_text(
            json.dumps(sen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("sen", sp.name, "entries", n)

    flat_targets = [
        ROOT / "localization" / "current" / "LawnStrings_zh.json",
        Path(r"F:\sen_work\LawnStrings_zh.json"),
        Path(r"F:\sen_work\current\LawnStrings_zh.json"),
    ]
    payload = json.dumps(zh, ensure_ascii=False, indent=2) + "\n"
    for p in flat_targets:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(payload, encoding="utf-8")
    print("flat synced")


if __name__ == "__main__":
    main()
