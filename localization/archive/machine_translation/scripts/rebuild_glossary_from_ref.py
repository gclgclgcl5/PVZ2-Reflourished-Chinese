#!/usr/bin/env python3
"""Rebuild glossary_pvz2.py WORLD/PLANTS/ZOMBIES/MODES/STAT phrases from ParaTranz参考.

Authority: localization/参考翻译/utf8/LawnStrings-ParaTranz.json
Keeps build_exact_map / apply_phrases API compatible with apply_translation.py.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
REF_PATH = ROOT / "参考翻译" / "utf8" / "LawnStrings-ParaTranz.json"
EN_PATH = ROOT / "LawnStrings_en.json"
OUT_PATH = SCRIPTS / "glossary_pvz2.py"

CJK_RE = re.compile(r"[\u4e00-\u9fff]")

# Preferred ref keys for world display names
WORLD_NAME_KEYS = [
    "WORLD_NAME_EGYPT",
    "WORLD_NAME_PIRATE",
    "WORLD_NAME_COWBOY",
    "WORLD_NAME_FUTURE",
    "WORLD_NAME_DARK",
    "WORLD_NAME_BEACH",
    "WORLD_NAME_ICEAGE",
    "WORLD_NAME_LOSTCITY",
    "WORLD_NAME_EIGHTIES",
    "WORLD_NAME_DINO",
    "WORLD_NAME_MODERN",
    "EGYPT",
    "PIRATE",
    "COWBOY",
    "FUTURE",
    "ICEAGE",
]

# Keys that are plant display names (ALLCAPS, no underscore) — exclude UI junk
NOT_PLANT = {
    "APPLIES", "ASH", "BONUS", "BUTTER", "CHILL", "COST", "COWBOY", "EGYPT",
    "PIRATE", "FUTURE", "DARKAGES", "BEACH", "ICEAGE", "LOSTCITY", "EIGHTIES",
    "DINO", "MODERNDAY", "PLAYERSHOUSE", "OK", "HP", "YES", "NO", "BACK",
    "DARK", "MODERN",
}


def has_cjk(s: str) -> bool:
    return bool(CJK_RE.search(s or ""))


def norm(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return (
        s.replace("\r\n", "\n")
        .replace("/r\n", "\n")
        .replace("\r", "\n")
        .strip()
    )


def py_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def fmt_dict(name: str, d: dict[str, str], comment: str = "") -> str:
    lines = [f"{name} = {{"]
    if comment:
        lines.insert(0, f"# {comment}")
    for k in sorted(d.keys(), key=lambda x: x.lower()):
        lines.append(f"    {py_str(k)}: {py_str(d[k])},")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    ref_list = json.loads(REF_PATH.read_text(encoding="utf-8"))
    en: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))
    ref = {x["key"]: x for x in ref_list}

    # English original -> Chinese (prefer key-aligned where en matches)
    by_en: dict[str, str] = {}
    for x in ref_list:
        o = (x.get("original") or "").strip()
        t = (x.get("translation") or "").strip()
        if not o or not t or not has_cjk(t):
            continue
        key = x["key"]
        if key in en and norm(o) != norm(en[key]):
            # still allow as phrase map for English text matching
            by_en.setdefault(o, t)
            continue
        by_en[o] = t  # overwrite with aligned

    world: dict[str, str] = {}
    for key in WORLD_NAME_KEYS:
        x = ref.get(key)
        if not x:
            continue
        t = (x.get("translation") or "").strip()
        o = (x.get("original") or "").strip()
        if t and has_cjk(t) and o:
            world[o] = t
    for eng in (
        "Steam Ages",
        "Holiday Mashup",
        "Tutorial",
        "Modern Day",
        "Player's House",
        "Ancient Egypt",
        "Pirate Seas",
        "Wild West",
        "Far Future",
        "Dark Ages",
        "Big Wave Beach",
        "Frostbite Caves",
        "Lost City",
        "Neon Mixtape Tour",
        "Jurassic Marsh",
    ):
        if eng in by_en:
            world[eng] = by_en[eng]

    plants: dict[str, str] = {}
    zombies: dict[str, str] = {}
    zombie_solo = {
        "Gargantuar",
        "Imp",
        "Zomboni",
        "Dr. Zomboss",
        "Zombot",
        "Troglobite",
        "Weasel Hoarder",
        "Ice Weasel",
        "Zombie Chicken",
        "Zombie Bull",
        "Zombie Parrot",
        "Zombie King",
        "King Zombie",
    }
    for key, x in ref.items():
        t = (x.get("translation") or "").strip()
        o = (x.get("original") or "").strip()
        if not t or not has_cjk(t) or not o:
            continue
        if key in en and norm(o) != norm(en[key]):
            continue
        # Credits VA lines are clean zombie display names
        if key.startswith("CREDITS_VA_") and len(o) <= 40 and o.count(" ") <= 4:
            if "Zombie" in o or o in zombie_solo or o.endswith("Imp") or "Gargantuar" in o:
                zombies[o] = t
                continue
        if "_" in key:
            continue
        if not key.isupper() or key in NOT_PLANT:
            continue
        if len(o) > 48:
            continue
        ol = o.lower()
        if "zombie" in ol or o in zombie_solo or "gargantuar" in ol:
            zombies[o] = t
        else:
            plants[o] = t

    for key, ev in en.items():
        if key not in ref:
            continue
        x = ref[key]
        t = (x.get("translation") or "").strip()
        o = (x.get("original") or "").strip()
        if not t or not has_cjk(t):
            continue
        if norm(o) != norm(ev):
            continue
        if key.startswith("ZOMBIE_") and key.endswith("_NAME"):
            zombies[ev] = t
        if ev in world:
            world[ev] = t

    modes: dict[str, str] = {}
    mode_keys = [
        "Last Stand",
        "Locked and Loaded",
        "Save Our Seeds",
        "Special Delivery",
        "Mummy Memory",
        "Cannons Away",
        "Vase Breaker",
        "Danger Room",
        "Travel Log",
        "Zen Garden",
        "Plant Food",
        "Piñata",
        "Pinata",
    ]
    for eng in mode_keys:
        if eng in by_en:
            modes[eng] = by_en[eng]

    # STAT / short UI exact values from aligned keys
    ui_values: dict[str, str] = {}
    phrases: dict[str, str] = {
        "Plants vs. Zombies 2": "植物大战僵尸2",
        "Plants vs Zombies 2": "植物大战僵尸2",
        "Plant - ": "植物 - ",
        "Zombie - ": "僵尸 - ",
        "{KEYWORD}Health:": "{KEYWORD}生命值:",
        "{KEYWORD}Speed:": "{KEYWORD}速度:",
        "{KEYWORD}Damage:": "{KEYWORD}伤害:",
        "{KEYWORD}Range:": "{KEYWORD}范围:",
        "{KEYWORD}Special:": "{KEYWORD}特殊:",
        "{KEYWORD}Plant Food:": "{KEYWORD}植物养料:",
        "{KEYWORD}Holiday Spirit:": "{KEYWORD}节日精神:",
        "seed packets": "种子包",
        "Seed Packets": "种子包",
        "Seed Packet": "种子包",
        " Seeds": " 种子",
        "Limit 1 per player": "每位玩家限购 1 次",
        "Dr. Zomboss": by_en.get("Dr. Zomboss", "僵王博士"),
        "Crazy Dave": by_en.get("Crazy Dave", "疯狂戴夫"),
        "Reflourished": "返茂",
        " Bundle": " 礼包",
        " Arena": " 竞技场",
    }

    for key, x in ref.items():
        if key not in en:
            continue
        t = (x.get("translation") or "").strip()
        o = (x.get("original") or "").strip()
        if not t or not has_cjk(t):
            continue
        if norm(o) != norm(en[key]):
            continue
        if key.startswith("STAT_") and len(o) < 60:
            ui_values[o] = t
            phrases[o] = t
        # Short UI buttons / labels
        if key.startswith(("BUTTON_", "DIALOG_STRING_", "OPTIONS_", "ALMANAC_")) and len(o) < 40:
            ui_values[o] = t

    # Merge world/plant into phrases for safe long replacements
    for eng, zh in sorted(world.items(), key=lambda kv: -len(kv[0])):
        phrases[eng] = zh
    for eng, zh in list(modes.items()):
        phrases[eng] = zh

    header = '''# -*- coding: utf-8 -*-
"""PvZ2 Reflourished glossary — authority is ParaTranz 参考翻译.

Generated/updated by rebuild_glossary_from_ref.py from:
  localization/参考翻译/utf8/LawnStrings-ParaTranz.json

Do not reintroduce old 官中习惯译名 that conflict with the reference pack.
Exact English value -> Chinese. Longer phrases preferred when applying (sorted by length).
"""
'''

    body = "\n\n".join(
        [
            fmt_dict("WORLD", world, "World / map names from reference"),
            fmt_dict("PLANTS", plants, "Plant display names from reference"),
            fmt_dict("ZOMBIES", zombies, "Zombie display names from reference"),
            fmt_dict("MODES", modes, "Game modes / features from reference"),
            fmt_dict("UI_VALUES", ui_values, "STAT labels & short UI from reference (exact match)"),
            fmt_dict("PHRASES", phrases, "Safe in-sentence phrase replacements"),
        ]
    )

    footer = '''


def build_exact_map() -> dict[str, str]:
    from glossary_extra import EXTRA

    m: dict[str, str] = {}
    m.update(UI_VALUES)
    m.update(EXTRA)
    m.update(MODES)
    for eng, zh in PLANTS.items():
        m[eng] = zh
        m[f"Plant - {eng}"] = f"植物 - {zh}"
        m[f"{eng} Seeds"] = f"{zh} 种子"
        m[f"{eng} Bundle"] = f"{zh} 礼包"
    for eng, zh in ZOMBIES.items():
        m[eng] = zh
        m[f"Zombie - {eng}"] = f"僵尸 - {zh}"
    for eng, zh in WORLD.items():
        m[eng] = zh
        m[f"Survive a massive attack during the {eng}"] = f"在{zh}中抵挡一波大规模进攻"
        m[f"20 seed packets for {eng} plants"] = f"20 个{zh}植物种子包"
    return m


def _named_entities() -> dict[str, str]:
    base = {**PLANTS, **ZOMBIES, **WORLD}
    out: dict[str, str] = {}
    for eng, zh in base.items():
        out[eng + "s"] = zh
        out[eng] = zh
    # Common plural / group labels if present in reference phrase map
    for eng, zh in (
        ("Ra Zombies", "太阳神僵尸"),
        ("Camel Zombies", "骆驼僵尸"),
        ("Bikini Zombies", "比基尼僵尸"),
        ("Egypt Zombies", "埃及僵尸"),
        ("Pirate Zombies", "海盗僵尸"),
        ("Wild West Zombies", "西部僵尸"),
        ("Dark Ages Zombies", "黑暗时代僵尸"),
        ("Lost City Zombies", "失落之城僵尸"),
        ("Jurassic Marsh Zombies", "侏罗纪沼泽僵尸"),
        ("Lawn Zombies", "草坪僵尸"),
    ):
        out[eng] = PHRASES.get(eng, zh)
    return out


def apply_phrases(text: str) -> str:
    out = text
    for eng, zh in sorted(_named_entities().items(), key=lambda kv: len(kv[0]), reverse=True):
        if eng in out:
            out = out.replace(eng, zh)
    for eng, zh in sorted(PHRASES.items(), key=lambda kv: len(kv[0]), reverse=True):
        if eng in out:
            out = out.replace(eng, zh)
    return out
'''

    OUT_PATH.write_text(header + "\n" + body + footer, encoding="utf-8")
    print(
        f"wrote {OUT_PATH} world={len(world)} plants={len(plants)} "
        f"zombies={len(zombies)} modes={len(modes)} ui={len(ui_values)} phrases={len(phrases)}"
    )
    for eng in ("Ancient Egypt", "Wild West", "Sunflower", "Snow Pea", "RECHARGE", "SUN COST"):
        src = world.get(eng) or plants.get(eng) or ui_values.get(eng) or phrases.get(eng)
        print(f"  sample {eng!r} -> {src!r}")


if __name__ == "__main__":
    main()
