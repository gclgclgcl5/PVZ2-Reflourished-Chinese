#!/usr/bin/env python3
"""Replace English plant/zombie display-name leftovers in almanac intro text.

Uses almanac_name_lock.json Chinese names. Applies:
  - full EN display name
  - simple plurals / possessives
  - multi-word trailing fragments (e.g. Peagle Pod from P-15 Peagle Pod)
  - a small manual alias table for known leftovers

Rewrites LawnStrings_zh.json in place (and syncs export_for_ai almanac *.zh.json
for DESCRIPTION/HEADER/TOOLTIP keys that change).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = ROOT / "LawnStrings_en.json"
ZH_PATH = ROOT / "LawnStrings_zh.json"
LOCK_PATH = ROOT / "export_for_ai" / "almanac" / "almanac_name_lock.json"
OUT_DIR = ROOT / "export_for_ai" / "almanac"

# Known leftovers that are not exact EN short-name strings
MANUAL_ALIASES: list[tuple[str, str]] = [
    ("Dazey Chains", "迷乱雏菊"),
    ("Dazey Chain", "迷乱雏菊"),
    ("Peagle Pod", "P-15鹰式战豆机"),
    ("Peagle Pods", "P-15鹰式战豆机"),
    ("Ultomates", "终极番茄"),
    ("Ultomate", "终极番茄"),
    ("Crazy Dave", "疯狂戴夫"),
    ("Dr. Zomboss", "僵王博士"),
    ("Lily of Alchemy", "炼金百合"),
    ("Lotus Root", "莲藕"),
    ("Cattail", "香蒲"),
    ("Fanilla", "法尼拉"),
    ("Saucer Squash", "飞碟瓜"),
    ("Berry Blaster", "浆果冲击波"),
    ("Hot Date", "热辣海枣"),
    ("Cherry Bomb", "樱桃炸弹"),
    ("Cherry Bombs", "樱桃炸弹"),
    ("Laser Bean", "激光豆"),
    ("Laser Beans", "激光豆"),
]


def bounded_replace(text: str, old: str, new: str) -> tuple[str, int]:
    if not old or old == new or old not in text:
        return text, 0
    count = 0
    parts: list[str] = []
    i = 0
    while True:
        pos = text.find(old, i)
        if pos < 0:
            parts.append(text[i:])
            break
        before = text[pos - 1] if pos else ""
        after_i = pos + len(old)
        after = text[after_i] if after_i < len(text) else ""
        left_ok = not before or not re.match(r"[A-Za-z]", before)
        right_ok = not after or not re.match(r"[A-Za-z]", after)
        parts.append(text[i:pos])
        if left_ok and right_ok:
            parts.append(new)
            count += 1
        else:
            parts.append(old)
        i = after_i
    return "".join(parts), count


def plural_variants(en_name: str) -> list[str]:
    out = [en_name]
    if en_name.endswith("y") and len(en_name) > 3 and en_name[-2].lower() not in "aeiou":
        out.append(en_name[:-1] + "ies")
    elif not en_name.endswith("s"):
        out.append(en_name + "s")
    out.append(en_name + "'s")
    # unique preserve order, longest first later
    seen: set[str] = set()
    uniq: list[str] = []
    for x in out:
        if x and x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def fragment_variants(en_name: str) -> list[str]:
    """Trailing multi-word fragments for names like 'P-15 Peagle Pod'."""
    frags: list[str] = []
    spaced = en_name.replace("-", " ")
    toks = spaced.split()
    if len(toks) >= 2:
        frags.append(" ".join(toks[-2:]))
    # skip single-token fragments shorter than 6 to avoid Pea/Mint damage
    if len(toks) >= 1 and len(toks[-1]) >= 6:
        frags.append(toks[-1])
    return frags


def build_pairs(
    en: dict[str, str],
    lock: dict[str, str],
    zh: dict[str, str] | None = None,
) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen_old: set[str] = set()

    def add(old: str, new: str) -> None:
        if not old or not new or old == new:
            return
        # Never replace with something that would eat shorter locks incorrectly:
        # prefer first registration of an 'old' string (longer zh resolved by sort)
        if old in seen_old:
            return
        # Skip tiny / generic English tokens
        if len(old) < 4:
            return
        if old.lower() in {
            "plant",
            "mint",
            "leaf",
            "vine",
            "nut",
            "bean",
            "seed",
            "pod",
            "rose",
            "pea",
            "sun",
            "imp",
            "lava",
            "fire",
            "ice",
            "gold",
            "dark",
            "moon",
        }:
            return
        seen_old.add(old)
        pairs.append((old, new))

    # Lock table first
    name_sources: list[tuple[str, str]] = []
    for k, zh_name in lock.items():
        en_name = en.get(k)
        if not isinstance(en_name, str) or not isinstance(zh_name, str):
            continue
        if not re.search(r"[\u4e00-\u9fff]", zh_name) and en_name == zh_name:
            continue
        name_sources.append((en_name, zh_name))

    # Also include plant short keys missing from lock (e.g. CHERRY_BOMB, LASER_BEAN)
    if zh is not None:
        for k, zh_name in zh.items():
            if k in lock or k.startswith("ZOMBIE_"):
                continue
            if not isinstance(zh_name, str) or not re.search(r"[\u4e00-\u9fff]", zh_name):
                continue
            if (k + "_DESCRIPTION") not in zh and (k + "_DESCRIPTION") not in en:
                continue
            if k.endswith(
                (
                    "_DESCRIPTION",
                    "_DESCRIPTION_HEADER",
                    "_TOOLTIP",
                    "_PLANTFOOD",
                    "_HEADER",
                    "_DESC",
                    "_TITLE",
                    "_INFO",
                )
            ):
                continue
            if k.startswith(
                (
                    "ACHIEVE",
                    "ADVICE_",
                    "NARRATIVE_",
                    "PRODUCT",
                    "product_",
                    "POWERUP_",
                    "UPGRADE_",
                    "UNLOCK_",
                    "FEATURE_",
                    "PERK_",
                    "UTILITY_",
                )
            ):
                continue
            en_name = en.get(k)
            if not isinstance(en_name, str) or not re.search(r"[A-Za-z]", en_name):
                continue
            name_sources.append((en_name, zh_name))

    for en_name, zh_name in name_sources:
        for var in plural_variants(en_name):
            add(var, zh_name)
        for frag in fragment_variants(en_name):
            if frag.lower() in {"pod", "vine", "mint", "nut", "bean", "leaf", "plant"}:
                continue
            add(frag, zh_name)

    for old, new in MANUAL_ALIASES:
        add(old, new)

    # longest English first
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    return pairs


def is_almanac_text_key(key: str) -> bool:
    return key.endswith(("_DESCRIPTION", "_DESCRIPTION_HEADER", "_TOOLTIP")) or key.startswith(
        "ALMANAC_"
    )


def main() -> None:
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    pairs = build_pairs(en, lock, zh)
    print(f"replacement pairs: {len(pairs)}")

    changed_keys = 0
    total_repl = 0
    samples: list[str] = []
    for k, v in list(zh.items()):
        if not isinstance(v, str) or not is_almanac_text_key(k):
            continue
        new = v
        local = 0
        for old, repl in pairs:
            new, n = bounded_replace(new, old, repl)
            local += n
        if local and new != v:
            zh[k] = new
            changed_keys += 1
            total_repl += local
            if len(samples) < 15:
                samples.append(f"{k}: {local} repl")

    ZH_PATH.write_text(
        json.dumps(zh, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"updated {changed_keys} keys, {total_repl} replacements -> {ZH_PATH}")
    for s in samples:
        print(" ", s)

    # Refresh export batches for consistency
    for batch in ("almanac_001", "almanac_002", "almanac_003", "almanac_pilot"):
        path = OUT_DIR / f"{batch}.zh.json"
        if not path.is_file():
            continue
        obj = json.loads(path.read_text(encoding="utf-8"))
        n = 0
        for k in list(obj.keys()):
            if k in zh and obj[k] != zh[k]:
                obj[k] = zh[k]
                n += 1
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"synced {path.name}: {n} keys")


if __name__ == "__main__":
    main()
