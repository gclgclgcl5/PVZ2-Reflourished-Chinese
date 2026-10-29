#!/usr/bin/env python3
"""Replace English plant-almanac display literals in Packages.

PvZ2 Reflourished stores many almanac attribute titles/values as raw RTON
ASCII strings (0x90 length-prefixed) instead of [STAT_xxx] LawnStrings refs.
Those stay English after LawnStrings-only localization.

Preferred fix (``--stat-refs``): rewrite each literal to an equal-length
``[STAT_…]`` token and emit Chinese values to merge into LawnStrings. The
almanac UI resolves bracketed keys via LawnStrings (CJK works). Putting UTF-8
Chinese directly into 0x90 slots shows as missing-glyph underscores.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# Display label / value → Chinese (will be fit to exact original byte length)
TRANSLATIONS: dict[str, str] = {
    # Zen garden / sun production (user-reported)
    "ZEN GARDEN BOOST": "禅境加持",  # 16 bytes with padding; full phrase too long
    "SUN PRODUCTION RATE": "阳光产出速率",
    "Sun Production Rate": "阳光产出速率",
    "Sun Production": "阳光产量",
    "ZOMBIE SUN PRODUCTION": "僵尸阳光产量",
    "ZOMBIE SUN PRODUCTION RATE": "僵尸产阳速率",
    "ZOMBIE ILLUMINATES OTHERS CHANCE": "僵尸开悟他人概率",
    "MISSING INFO": "暂无信息",
    "[MISSING INFO]": "[暂无信息]",
    "Plant Food": "植物养料",
    # Boost values
    "Explodes when Shoveled": "铲除时发生爆炸",
    "x3 Toughness": "生命值×3",
    "x2 Toughness": "生命值×2",
    "x1.5 Toughness": "生命值×1.5",
    "-50 Sun Cost": "阳光消耗-50",
    "-75 Sun Cost": "阳光消耗-75",
    "-100 Sun Cost": "阳光消耗-100",
    "-5s Recharge": "冷却-5秒",
    "-10s Recharge": "冷却-10秒",
    "-15s Recharge": "冷却-15秒",
    "-20s Recharge": "冷却-20秒",
    "-2.5s Recharge": "冷却-2.5秒",
    # Common ALL-CAPS almanac titles
    "DAMAGE PER SECOND": "每秒伤害",
    "ATTACK DAMAGE PER SECOND": "每秒攻击伤害",
    "POISON DAMAGE PER SECOND": "每秒毒素伤害",
    "LAVA DAMAGE PER SECOND": "每秒岩浆伤害",
    "LEAF DAMAGE PER SECOND": "每秒叶片伤害",
    "TIGER DAMAGE PER SECOND": "每秒老虎伤害",
    "BUTTER DAMAGE": "黄油伤害",
    "SPLASH DAMAGE": "溅射伤害",
    "SLAP DAMAGE": "拍击伤害",
    "RUSH DAMAGE": "冲锋伤害",
    "MELEE DAMAGE": "近战伤害",
    "PROJECTILE DAMAGE": "弹道伤害",
    "EXPLOSION DAMAGE": "爆炸伤害",
    "SPIKE DAMAGE": "尖刺伤害",
    "GRAPE DAMAGE": "葡萄伤害",
    "SEED DAMAGE": "种子伤害",
    "BOLT DAMAGE": "闪电伤害",
    "BUD DAMAGE": "花蕾伤害",
    "POTION DAMAGE": "药水伤害",
    "POPCORN DAMAGE": "爆米花伤害",
    "POPCORN SPLASH DAMAGE": "爆米花溅射伤",
    "TORPEDO DAMAGE": "鱼雷伤害",
    "TORPEDO EXPLOSION DAMAGE": "鱼雷爆炸伤害",
    "CORROSIVE DAMAGE": "腐蚀伤害",
    "LEMON SLICE DAMAGE": "柠檬片伤害",
    "PILOT DAMAGE": "飞行员伤害",
    "GIANT PEA DAMAGE": "巨型豌豆伤害",
    "POUNCE DAMAGE": "扑击伤害",
    "SPRING DAMAGE": "弹簧伤害",
    "ROLLING DAMAGE": "滚压伤害",
    "BURST DAMAGE": "爆发伤害",
    "CRIT DAMAGE": "暴击伤害",
    "CRITICAL DAMAGE": "暴击伤害",
    "FROSTY PEA DAMAGE": "寒冰豌豆伤害",
    "PLASMA PEA DAMAGE": "等离子豌豆伤害",
    "PLASMA PEA SPLASH DAMAGE": "等离子溅射伤害",
    "SMALL GEAR DAMAGE": "小齿轮伤害",
    "LARGE GEAR DAMAGE": "大齿轮伤害",
    "CANDY PIECE DAMAGE": "糖果块伤害",
    "FIRE SPIKE LEAF DAMAGE": "火焰尖叶伤害",
    "ICE SPIKE LEAF DAMAGE": "寒冰尖叶伤害",
    "GAS DAMAGE": "毒气伤害",
    "POWERED GAS DAMAGE": "强化毒气伤害",
    "DAMAGE (STRAIGHT)": "伤害（直线）",
    "DAMAGE (LOBBED)": "伤害（抛射）",
    "DAMAGE MIRRORED": "镜像伤害",
    "DAMAGE DECREASE PER BOUNCE": "每次弹跳伤害降低",
    "DAMAGE INCREASE PER BOUNCE": "每次弹跳伤害提升",
    "DAMAGE INCREASE PERCENTAGE": "伤害提升百分比",
    "SHRINK DAMAGE MULTIPLIER": "缩小伤害倍率",
    "SUN PRODUCTION (STRAIGHT)": "阳光产量（直线）",
    "SUN PRODUCTION (LOBBED)": "阳光产量（抛射）",
    "SUN CARD SUN PRODUCTION": "阳光卡产阳量",
    "SUN CARD CHANCE": "阳光卡概率",
    "SUN CARD DURATION": "阳光卡持续",
    "SUN BOOST": "阳光强化",
    "ZOMBIE HP BOOST": "僵尸生命强化",
    "FIRING RATE (LOBBED)": "射速（抛射）",
    "FIRING RATE (POWERED)": "射速（充能）",
    "FIRING RATE (STRAIGHT)": "射速（直线）",
    "FIRING RATE (UNPOWERED)": "射速（未充能）",
    "ATTACKING RATE": "攻击速率",
    "SPIKE ATTACKING RATE": "尖刺攻击速率",
    "FIRE SPIKE LEAF FIRING RATE": "火焰尖叶射速",
    "ICE SPIKE LEAF FIRING RATE": "寒冰尖叶射速",
    "AREA (LAND)": "范围（陆地）",
    "AREA (WATER)": "范围（水面）",
    "RANGE (LAND)": "射程（陆地）",
    "RANGE (WATER)": "射程（水面）",
    "RANGE (LOBBED)": "射程（抛射）",
    "RANGE (POWERED)": "射程（充能）",
    "RANGE (STRAIGHT)": "射程（直线）",
    "RANGE (UNPOWERED)": "射程（未充能）",
    "AMMO RECHARGE": "弹药冷却",
    "BULB RECHARGE": "球茎冷却",
    "EMPTY FUEL RECHARGE": "空燃料冷却",
    "PUFFING RECHARGE": "喷气冷却",
    "RAGE RECHARGE": "狂暴冷却",
    "MAGIC CARD RECHARGE": "魔法卡冷却",
    "SHIELD SLAM RECHARGE": "盾击冷却",
    "LEAF TOUGHNESS": "叶片生命值",
    "TIGER TOUGHNESS": "老虎生命值",
    "BIRD TOUGHNESS": "飞鸟生命值",
    "GRAVITY SPHERE TOUGHNESS": "重力球生命值",
    "HEALTH HEALED": "回复生命值",
    "MURK HEALTH HEALED": "雾气回复生命",
    "HEAL COOLDOWN": "治疗冷却",
    "MURK HEAL COOLDOWN": "雾气治疗冷却",
    "MAX MURK ARMOR": "最大雾气护甲",
    "GROWTH SPEED": "生长速度",
    "REGENERATION SPEED": "再生速度",
    "MELT SPEED": "融化速度",
    "BUST SPEED": "破坏速度",
    "FLAMETHROWER DPS": "火焰喷射DPS",
    "BIRD EAT DPS": "飞鸟啃食DPS",
    "TURKEY EAT DPS": "火鸡啃食DPS",
    "FLAME LENGTH": "火焰长度",
    "FOG AREA": "迷雾范围",
    "SPLASH AREA": "溅射范围",
    "POPCORN AREA": "爆米花范围",
    "FROSTY PEA AREA": "寒冰豌豆范围",
    "CHEW TIME": "咀嚼时间",
    "HOLD TIME": "保持时间",
    "BOMB ARMING TIME": "炸弹装填时间",
    "DECOMPOSING TIME": "分解时间",
    "TIGER REGEN TIME": "老虎再生时间",
    "STUN DURATION": "眩晕持续",
    "STUN CHANCE": "眩晕概率",
    "BUTTER CHANCE": "黄油概率",
    "BUTTER DURATION": "黄油持续",
    "BUTTER SPLAT DURATION": "黄油溅开持续",
    "CHILL DURATION": "寒冷持续",
    "FREEZE DURATION": "冰冻持续",
    "FREEZE CARD CHANCE": "冰冻卡概率",
    "STALL DURATION": "阻滞持续",
    "SLOWDOWN DURATION": "减速持续",
    "SLOWDOWN PERCENTAGE": "减速百分比",
    "STACKABLE SLOWDOWN": "可叠加减速",
    "SAP DURATION": "树脂持续",
    "OIL DURATION": "油渍持续",
    "OIL SLOWDOWN PERCENTAGE": "油渍减速百分比",
    "LAVA DURATION": "岩浆持续",
    "PUDDLE DURATION": "水洼持续",
    "PUFFING DURATION": "喷气持续",
    "DISABLE DURATION": "禁用持续",
    "TORNADO DURATION": "龙卷风持续",
    "RANK DURATION": "等级持续",
    "ALLERGIC DURATION": "过敏持续",
    "BLOW DURATION": "吹飞持续",
    "HEARTBREAK DURATION": "心碎持续",
    "HEARTBROKEN DURATION": "心碎状态持续",
    "LOVESICK DURATION": "相思持续",
    "PLANTFOOD CARD DURATION": "植物养料卡持续",
    "SPEED BOOST DURATION": "加速强化持续",
    "SPEED BOOST PERCENTAGE": "加速强化百分比",
    "PROJECTILE STALL DURATION": "弹道阻滞持续",
    "SPIKE STALL DURATION": "尖刺阻滞持续",
    "POTION STALL DURATION": "药水阻滞持续",
    "BOLT MAX STALL DURATION": "闪电最大阻滞",
    "POPCORN SAP DURATION": "爆米花树脂持续",
    "POISON AND SLOW DURATION": "中毒与减速持续",
    "REDUCED EAT DPS DURATION": "降低啃食持续",
    "REDUCED EAT DPS PERCENTAGE": "降低啃食百分比",
    "HEARTBREAK SLOWDOWN PERCENTAGE": "心碎减速百分比",
    "HEARTBROKEN SLOWDOWN PERCENTAGE": "心碎态减速百分比",
    "HEARTBROKEN REDUCED DPS PERCENTAGE": "心碎态降伤百分比",
    "LOVESICK REDUCED DPS PERCENTAGE": "相思降伤百分比",
    "POTION SLOWDOWN PERCENTAGE": "药水减速百分比",
    "SPIKE SLOWDOWN PERCENTAGE": "尖刺减速百分比",
    "BLOW AWAY ZOMBIE CHANCE": "吹飞僵尸概率",
    "KNOCKBACK CHANCE": "击退概率",
    "KNOCKBACK DISTANCE": "击退距离",
    "LEMON SLICE CHANCE": "柠檬片概率",
    "LEMON SLICE KNOCKBACK DISTANCE": "柠檬片击退距离",
    "CRIT CHANCE": "暴击概率",
    "BASIC CHANCE": "基础概率",
    "DUPLICATE CHANCE": "复制概率",
    "REBOUND CHANCE": "反弹概率",
    "PLANTFOOD CARD CHANCE": "植物养料卡概率",
    "FROSTY PEA CHANCE": "寒冰豌豆概率",
    "PLASMA PEA CHANCE": "等离子豌豆概率",
    "POPCORN CHANCE": "爆米花概率",
    "POTION CHANCE": "药水概率",
    "CARROTHEAD CHANCE": "萝卜头概率",
    "MELONHEAD CHANCE": "瓜头概率",
    "ZOMBIE EXPLOSION CHANCE": "僵尸爆炸概率",
    "ABDUCT THRESHOLD": "绑架阈值",
    "CARROTHEAD HP THRESHOLD": "萝卜头生命阈值",
    "MELONHEAD HP THRESHOLD": "瓜头生命阈值",
    "BALLOON MAX STACKS": "气球最大层数",
    "MAX STACKS": "最大层数",
    "MAX BOUNCES": "最大弹跳",
    "MAX PIERCE": "最大穿透",
    "MAX TARGET": "最大目标",
    "MAX TOSSES": "最大投掷",
    "SHOT BOUNCES": "射击弹跳",
    "TRAP COUNT": "陷阱数量",
    "DART COUNT": "飞镖数量",
    "GRAPE COUNT": "葡萄数量",
    "LEAF COUNT": "叶片数量",
    "CANDY PIECE COUNT": "糖果块数量",
    "PIT CAPACITY": "坑容量",
    "BOMB CHAIN MULTIPLIER": "炸弹连锁倍率",
    "COST INCREASE": "费用增加",
    "AMMO": "弹药",
    "ANIMATION": "动画",
    "ANIMATION2": "动画2",
    "ANIMATION3": "动画3",
    "ANIMATION4": "动画4",
    "10% of Health": "生命值的10%",
    "FIRE SPIKE LEAF MAX PIERCE": "火焰尖叶最大穿透",
    "ICE SPIKE LEAF MAX PIERCE": "寒冰尖叶最大穿透",
    "BIRD LIFETIME": "飞鸟存活时间",
    "TURKEY LIFETIME": "火鸡存活时间",
    "SPRING LIFETIME": "弹簧存活时间",
    "PLANTS DEBUFFS REMOVAL AREA": "植物减益清除范围",
    "PLANTS DEBUFFS REMOVAL COOLDOWN": "植物减益清除冷却",
    "ZOMBIE TO TELEPORT": "传送僵尸数",
    "ZOMBIES BUFFS STOLEN TO RANK": "偷取增益至等级",
    "POWERED DRAG": "强化拖拽",
    "HEATH PERCENTAGE LOSE FROM TRANSFOMATION": "变形损失生命百分比",
}


def fit_bytes(zh: str, nbytes: int) -> bytes:
    """Encode zh to exactly nbytes (truncate chars or pad ASCII spaces).

    WARNING: PvZ2 almanac UI treats 0x90 slots as Latin/glyph-mapped text.
    UTF-8 Chinese here renders as missing-glyph underscores. Prefer STAT refs.
    """
    chars = list(zh)
    while chars and len("".join(chars).encode("utf-8")) > nbytes:
        chars.pop()
    out = "".join(chars).encode("utf-8")
    if len(out) < nbytes:
        out = out + b" " * (nbytes - len(out))
    if len(out) != nbytes:
        out = (zh.encode("ascii", "ignore") + b" " * nbytes)[:nbytes]
    return out


def _slug_body(eng: str) -> str:
    """ASCII body for STAT key from English label."""
    s = re.sub(r"[^A-Za-z0-9]+", "_", eng.strip())
    s = re.sub(r"_+", "_", s).strip("_").upper()
    return s or "X"


def make_stat_ref(eng: str, used_keys: set[str]) -> tuple[str, str]:
    """Build equal-length ``[KEY]`` and bare LawnStrings KEY for eng."""
    n = len(eng)
    if n < 4:
        raise ValueError(f"label too short for [STAT] ref: {eng!r}")
    inner_n = n - 2  # account for [ ]
    # Prefer STAT_ + slug; fit exactly to inner_n
    slug = _slug_body(eng)
    if inner_n >= 5 + 1:
        base = "STAT_" + slug
    else:
        base = slug
    if len(base) > inner_n:
        body = base[:inner_n]
    else:
        body = base + ("_" * (inner_n - len(base)))
    # uniquify if collision
    if body in used_keys:
        for i in range(1, 1000):
            suffix = str(i)
            cand = body[: inner_n - len(suffix)] + suffix
            if len(cand) == inner_n and cand not in used_keys:
                body = cand
                break
        else:
            raise SystemExit(f"cannot uniquify STAT key for {eng!r}")
    used_keys.add(body)
    ref = f"[{body}]"
    if len(ref) != n:
        raise SystemExit(f"STAT ref length mismatch: {eng!r} -> {ref!r}")
    return ref, body


def build_stat_rewrites(
    translations: dict[str, str],
) -> dict[str, tuple[str, str]]:
    """eng → ([STAT_…], KEY) for every label that fits."""
    used: set[str] = set()
    out: dict[str, tuple[str, str]] = {}
    # longer first so shorter substrings don't steal uniqueness prefer
    for eng in sorted(translations.keys(), key=len, reverse=True):
        if len(eng) < 4:
            continue
        ref, key = make_stat_ref(eng, used)
        out[eng] = (ref, key)
    return out


def patch_section(
    section: bytes,
    *,
    use_stat_refs: bool,
    lawn_zh: dict[str, str] | None,
) -> tuple[bytes, dict[str, int], dict[str, str]]:
    data = bytearray(section)
    counts: dict[str, int] = {}
    new_keys: dict[str, str] = {}

    stat_map = build_stat_rewrites(TRANSLATIONS) if use_stat_refs else {}

    # Prefer longer originals first
    items = sorted(TRANSLATIONS.items(), key=lambda kv: len(kv[0]), reverse=True)
    for eng, zh in items:
        needle = eng.encode("ascii")
        if use_stat_refs:
            if eng not in stat_map:
                continue  # too short — leave English
            repl_s, key = stat_map[eng]
            repl = repl_s.encode("ascii")
            new_keys[key] = zh
            if lawn_zh is not None:
                lawn_zh[key] = zh
        else:
            repl = fit_bytes(zh, len(needle))

        start = 0
        n = 0
        while True:
            i = data.find(needle, start)
            if i < 0:
                break
            # Only replace RTON length-prefixed occurrences (0x90 + len).
            if i >= 2 and data[i - 2] == 0x90 and data[i - 1] == len(needle):
                data[i : i + len(needle)] = repl
                n += 1
                start = i + len(needle)
            else:
                start = i + 1
        if n:
            counts[eng] = n
    return bytes(data), counts, new_keys


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("section", type=Path, help="packages_section.bin (decompressed)")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument(
        "--stat-refs",
        action="store_true",
        help="rewrite selected labels to [STAT_…] and emit keys JSON",
    )
    ap.add_argument(
        "--lawnstrings-zh",
        type=Path,
        default=None,
        help="optional LawnStrings_zh.json to merge new STAT keys into",
    )
    ap.add_argument(
        "--keys-out",
        type=Path,
        default=None,
        help="write newly added STAT key map JSON",
    )
    args = ap.parse_args()

    lawn = None
    if args.lawnstrings_zh:
        lawn = json.loads(args.lawnstrings_zh.read_text(encoding="utf-8"))

    section = args.section.read_bytes()
    out, counts, new_keys = patch_section(
        section, use_stat_refs=args.stat_refs, lawn_zh=lawn
    )
    args.out.write_bytes(out)
    print(f"wrote {args.out} ({len(out)} bytes)")
    print(f"patched {sum(counts.values())} occurrences across {len(counts)} literals")
    for eng, n in sorted(counts.items(), key=lambda kv: -kv[1])[:40]:
        print(f"  {n:3d}  {eng!r}")
    if len(counts) > 40:
        print(f"  ... {len(counts) - 40} more")

    if args.stat_refs and new_keys:
        if args.keys_out:
            args.keys_out.write_text(
                json.dumps(new_keys, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"wrote keys {args.keys_out}")
        if lawn is not None and args.lawnstrings_zh:
            args.lawnstrings_zh.write_text(
                json.dumps(lawn, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"updated {args.lawnstrings_zh} (+{len(new_keys)} keys)")


if __name__ == "__main__":
    main()
