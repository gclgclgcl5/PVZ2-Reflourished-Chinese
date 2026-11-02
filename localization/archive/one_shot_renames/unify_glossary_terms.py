# -*- coding: utf-8 -*-
"""Unify conflicting term translations to 参考译 / glossary_pvz2 canon."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"F:\othergit\Reverse Engineer Anything")
ZH_PATH = ROOT / "localization" / "LawnStrings_zh.json"
EN = json.loads((ROOT / "localization" / "LawnStrings_en.json").read_text(encoding="utf-8"))

# Global phrase replacements (longer first). Safe opposites → 参考译.
GLOBAL: list[tuple[str, str]] = [
    # Taco
    ("华夫饼的炸玉米饼", "华夫饼的玉米卷"),
    ("夹着华夫饼的炸玉米饼", "夹着华夫饼的玉米卷"),
    ("炸玉米饼", "玉米卷"),
    ("塔可印象", "玉米卷小鬼"),
    ("塔可小鬼僵尸", "玉米卷小鬼僵尸"),
    ("塔可小鬼", "玉米卷小鬼"),
    # Plant Food / Ghost Pepper / Modern / plants
    ("植物食物", "植物养料"),
    ("幽灵辣椒", "断魂椒"),
    ("现代世界", "现代年华"),
    ("弹跳秋海棠", "一品轰"),
    ("心花怒放", "铃儿草"),
    ("花椰菜武帝", "超能花菜"),
    ("瓷砖萝卜", "地砖芜菁"),
    ("地砖萝卜", "地砖芜菁"),
    ("冰地刺", "冰刺草"),
    ("回旋镖射手", "回旋花"),
    ("穴居人僵尸", "穴居僵尸"),
    ("法师僵尸", "巫师僵尸"),
    ("疯狂的戴夫", "疯狂戴夫"),
    # World MT aliases
    ("霓虹旋音游", "炫光魔音游"),
    ("未来世界", "遥远未来"),
    ("神秘埃及", "上古埃及"),
]

# Far Future shorthand: 远未来 but not already 遥远未来
FAR_FUTURE_RE = re.compile(r"(?<!遥)远未来")


def fix_text(text: str, key: str | None = None) -> str:
    nv = text
    for old, new in GLOBAL:
        if old in nv:
            nv = nv.replace(old, new)
    nv = FAR_FUTURE_RE.sub("遥远未来", nv)

    # EN-aware: Citron mistranslated as 柠檬
    if key and key in EN and isinstance(EN[key], str):
        en = EN[key]
        if re.search(r"\bcitron\b", en, re.I) and "柠檬" in nv:
            # family list / unlock lines: 柠檬 → 等离子香橼
            nv = nv.replace("柠檬", "等离子香橼")
        # taco-shaped / Taco Imp using 墨西哥卷饼
        if re.search(r"\btaco", en, re.I) and "墨西哥卷饼" in nv:
            nv = nv.replace("墨西哥卷饼", "玉米卷")
        # leftover English Taco map wording
        if re.search(r"\btaco\s*map\b", en, re.I):
            nv = re.sub(r"\bTaco\s*地图\b", "玉米卷地图", nv, flags=re.I)
            nv = re.sub(r"\bTaco\b", "玉米卷", nv)
        # Taco tickets / plain Taco left in Chinese strings when EN has taco
        if re.search(r"\btaco", en, re.I):
            nv = re.sub(r"\bTaco\b", "玉米卷", nv)
            nv = re.sub(r"\btaco\b", "玉米卷", nv)

    return nv


def main() -> None:
    zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    changed = 0
    hit_counter: dict[str, int] = {}
    for k, v in list(zh.items()):
        if not isinstance(v, str):
            continue
        before = v
        nv = fix_text(v, k)
        if nv != before:
            # count which rules fired roughly
            for old, new in GLOBAL:
                if old in before and old not in nv:
                    hit_counter[old] = hit_counter.get(old, 0) + before.count(old)
            if FAR_FUTURE_RE.search(before) and "遥远未来" in nv:
                c0 = len(FAR_FUTURE_RE.findall(before))
                if c0:
                    hit_counter["(?<!遥)远未来"] = hit_counter.get("(?<!遥)远未来", 0) + c0
            zh[k] = nv
            changed += 1

    payload = json.dumps(zh, ensure_ascii=False, indent=2) + "\n"
    ZH_PATH.write_text(payload, encoding="utf-8")
    print("keys changed", changed)
    for old, n in sorted(hit_counter.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {old}")

    # residual checks
    checks = [
        "炸玉米饼",
        "植物食物",
        "现代世界",
        "幽灵辣椒",
        "弹跳秋海棠",
        "心花怒放",
        "花椰菜武帝",
        "霓虹旋音游",
        "未来世界",
        "神秘埃及",
        "塔可",
    ]
    print("residuals:")
    for s in checks:
        n = sum(1 for v in zh.values() if isinstance(v, str) and s in v)
        if n:
            print(f"  {n}  {s}")
    # 远未来 residual (not 遥远)
    far = sum(
        1
        for v in zh.values()
        if isinstance(v, str) and FAR_FUTURE_RE.search(v)
    )
    print(f"  {far}  bare 远未来")

    sen_paths = [
        ROOT / "localization" / "current" / "LawnStrings_zh_sen.json",
        Path(r"F:\sen_work\LawnStrings_zh_penny_sen.json"),
        Path(r"F:\sen_work\LawnStrings_zh_good_almanac_sen.json"),
        Path(r"F:\sen_work\LawnStrings_zh_almanac_sen.json"),
        Path(r"F:\sen_work\current\LawnStrings_zh_sen.json"),
        Path(r"F:\sen_work\LawnStrings_zh_sen.json"),
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
            nv = fix_text(val, key if isinstance(key, str) else None)
            if nv != val:
                vals[i + 1] = nv
                n += 1
        sp.write_text(
            json.dumps(sen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("sen", sp.name, n)

    for p in [
        ROOT / "localization" / "current" / "LawnStrings_zh.json",
        Path(r"F:\sen_work\LawnStrings_zh.json"),
        Path(r"F:\sen_work\current\LawnStrings_zh.json"),
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(payload, encoding="utf-8")
    print("flat synced")


if __name__ == "__main__":
    main()
