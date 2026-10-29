#!/usr/bin/env python3
"""Translate batch_036 chunk JSON files to zh."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from glossary_mods import MOD_NAMES  # noqa: E402
from glossary_pvz2 import PLANTS, WORLD, apply_phrases, build_exact_map  # noqa: E402
from glossary_ui_visible import UI_VISIBLE  # noqa: E402

CHUNK_DIR = SCRIPTS.parent / "export_for_ai" / "chunks"

# Plants not in glossary_pvz2.PLANTS — keep established batch_032 style where no CN official name.
EXTRA_PLANTS: dict[str, str] = {
    **PLANTS,
    "Magnet-shroom": "磁力菇",
    "Spring Bean": "弹簧豆",
    "Sun Bean": "阳光豆",
    "Tangle Kelp": "缠绕水草",
    "Apple Mortar": "Apple Mortar",
    "Bombegranate": "炸弹榴",
    "Cactus": "仙人掌",
    "Strawburst": "Strawburst",
    "Hot Date": "Hot Date",
    "Grapeshot": "Grapeshot",
    "Homing Thistle": "Homing Thistle",
    "Electric Currant": "Electric Currant",
    "Sling Pea": "Sling Pea",
    "Snap Pea": "Snap Pea",
    "Solar Sage": "Solar Sage",
    "Ultomato": "Ultomato",
    "Zoybean": "Zoybean",
    "Zoybean Pod": "Zoybean Pod",
    "Puffball": "Puffball",
    "Pea Vine": "Pea Vine",
    "Peanut": "Peanut",
    "Squash": "Squash",
    "Jalapeno": "Jalapeno",
    "Dandelion": "Dandelion",
    "Power Mint": "Power Mint",
    "Jack O’ Lantern": "南瓜灯",
    "Jack O' Lantern": "南瓜灯",
    "Spear-mint Plants": "Spear-mint 植物",
    "Spear-mint": "长矛薄荷",
    "PepperMint": "辣椒薄荷",
    "Valenbrainz": "Valenbrainz",
    "Springening": "Springening",
    "Filamint": "Filamint",
    "Pirate Starter Bundle": "海盗新手礼包",
    "Shadow Peashooter Event": "暗影豌豆活动",
    "Modern Day Packets": "现代世界种子包",
    "Packets": "种子包",
    "Pinata Seeds": "皮纳塔种子",
    "Piñata Seeds": "皮纳塔种子",
    "Premium Piñata": "高级皮纳塔",
    "Premium Pinata": "高级皮纳塔",
    "Premium Piñatas": "高级皮纳塔",
    "Premium Pinatas": "高级皮纳塔",
    "Nut Plant": "坚果类植物",
    "Nut Plants": "坚果类植物",
    "Sun Plant": "阳光植物",
    "Sun Plants": "阳光植物",
    "Mushroom": "蘑菇",
    "Mushrooms": "蘑菇",
    "Cold Plant": "寒冰植物",
    "Electric Plant": "电力植物",
    "Fruit Plant": "果实植物",
    "Greens": "绿色蔬菜",
    "Shadow Plant": "暗影植物",
    "Electric Peashooter Bundle": "Electric Peashooter 礼包",
    "Coins": "金币",
    "Gems": "宝石",
    "Gauntlets": "护手",
    "Level 2!": "2 级！",
}

WORLDS_EXT = {
    **WORLD,
    "Frostbite Cave": "冰河世界",
    "Frostbite Caves": "冰河世界",
}

STATIC: dict[str, str] = {
    "Gift": "礼物",
    "Daily Gift!": "每日礼物！",
    "Community Challenge Reward": "社区挑战奖励",
    "Piñata Party seeds": "皮纳塔派对种子",
    "Pinata - Luck O the Zombie x 15": "皮纳塔 - 僵尸好运 x 15",
    "Luck o' the Zombie": "僵尸好运",
    "Pinata - Pirate Starter Bundle": "皮纳塔 - 海盗新手礼包",
    "Filamint Test ": "Filamint 测试 ",
    "Filamint Pinata": "Filamint 皮纳塔",
    "Shadow Plant Seed Packet Test": "暗影植物种子包测试",
    "2 PepperMint pinatas": "2 个辣椒薄荷皮纳塔",
    "5 PepperMint pinatas": "5 个辣椒薄荷皮纳塔",
    "One piñata - Level up your Pirate Seas plants!": "一个皮纳塔 - 升级你的海盗港湾植物！",
    "Three times the size of a normal piñata! Level up your Pirate Seas plants!": "普通皮纳塔的三倍大小！升级你的海盗港湾植物！",
    "Large Pirate Seas Piñata": "大型海盗港湾皮纳塔",
    "35 Peashooter Seed Packets + 9000 Coins + 20 Gems": "35 个豌豆射手种子包 + 9000 金币 + 20 宝石",
    "35 Peashooter Seed Packets": "35 个豌豆射手种子包",
    "35 Wall-nut Seed Packets": "35 个坚果墙种子包",
    "Electric Peashooter + 25 Electric Peashooter seed packets (Level 2!) + 1 Premium Piñata": "Electric Peashooter + 25 个 Electric Peashooter 种子包（2 级！）+ 1 个高级皮纳塔",
    "Bring two of the same plant into a level": "在同一关卡带入两株相同植物",
    "Mimics a seed packet.": "模仿一张种子包。",
    "Cold Snapdragon: Cold Snapdragons breathe icy mist into 6 adjacent tiles.": "寒冰龙草：寒冰龙草向相邻 6 格喷吐冰雾。",
    "Grapeshot: Explodes and scatters bouncing projectiles!": "Grapeshot：爆炸并散射弹跳弹体！",
    "Escape Root: Explodes and can be swapped!": "遁地根：爆炸并可以换位！",
    "TEST - Snap Pea Piñata": "测试 - Snap Pea 皮纳塔",
    "10 Snap Pea Packets": "10 个 Snap Pea 种子包",
    "50 Zoybean Packets": "50 个 Zoybean 种子包",
    "100 Zoybean Seed Packets": "100 个 Zoybean 种子包",
    "200 Zoybean Packets": "200 个 Zoybean 种子包",
    "Pinata – Pirate Seas": "皮纳塔 – 海盗港湾",
    "Pinata – Valenbrainz Plants": "皮纳塔 – Valenbrainz 植物",
    "10 Modern Day Packets - Shadow Peashooter Event": "10 个现代世界种子包 - 暗影豌豆活动",
    "80 Modern Day Seed Packets": "80 个现代世界种子包",
    "Shadow Peashooter seed packets!": "暗影豌豆种子包！",
    "Shadow Peashooter Packets": "暗影豌豆种子包",
    "Sling Pea seed packets!": "Sling Pea 种子包！",
    "Sling Pea Piñata": "Sling Pea 皮纳塔",
    "Snap Pea seed packets!": "Snap Pea 种子包！",
    "400 Piñata Seeds + 60 Toadstool seed packets": "400 个皮纳塔种子 + 60 个蟾蜍菇种子包",
    "1000 Piñata Seeds + 200 Toadstool seed packets": "1000 个皮纳塔种子 + 200 个蟾蜍菇种子包",
    "400 Piñata Seeds + 60 Strawburst seed packets": "400 个皮纳塔种子 + 60 个 Strawburst 种子包",
    "1000 Piñata Seeds + 200 Strawburst seed packets": "1000 个皮纳塔种子 + 200 个 Strawburst 种子包",
    "100 Pinata Seeds": "100 个皮纳塔种子",
    "1000 seed packets + BONUS 500 Gold Bloom seed packets!": "1000 个种子包 + 额外奖励 500 个金色绽放种子包！",
    "400 seed packets + BONUS 60 seed packets for Toadstool": "400 个种子包 + 额外奖励 60 个蟾蜍菇种子包",
    "1000 seed packets + BONUS 200 seed packets for Toadstool": "1000 个种子包 + 额外奖励 200 个蟾蜍菇种子包",
    "1000 seed packets + BONUS 500 Apple Mortar seed packets!": "1000 个种子包 + 额外奖励 500 个 Apple Mortar 种子包！",
    "400 seed packets + BONUS 60 Electric Blueberry seed packets!": "400 个种子包 + 额外奖励 60 个电力蓝莓种子包！",
    "1000 seed packets + BONUS 200 Electric Blueberry seed packets!": "1000 个种子包 + 额外奖励 200 个电力蓝莓种子包！",
    "1000 seed packets + BONUS 500 Parsnip seed packets!": "1000 个种子包 + 额外奖励 500 个欧防风种子包！",
    "400 seed packets + BONUS 60 Snow Pea seed packets!": "400 个种子包 + 额外奖励 60 个寒冰射手种子包！",
    "1000 seed packets + BONUS 200 Snow Pea seed packets!": "1000 个种子包 + 额外奖励 200 个寒冰射手种子包！",
    "400 seed packets + BONUS 60 Electric Peashooter seed packets!": "400 个种子包 + 额外奖励 60 个电力豌豆种子包！",
    "1000 seed packets + BONUS 200 Electric Peashooter seed packets!": "1000 个种子包 + 额外奖励 200 个电力豌豆种子包！",
    "1000 seed packets + BONUS 500 Sap-fling seed packets!": "1000 个种子包 + 额外奖励 500 个树汁苗种子包！",
    "400 seed packets + BONUS 60 seed packets for Strawburst": "400 个种子包 + 额外奖励 60 个 Strawburst 种子包",
    "1000 seed packets + BONUS 200 seed packets for Strawburst": "1000 个种子包 + 额外奖励 200 个 Strawburst 种子包",
    "400 seed packets + BONUS 60 Hot Date seed packets!": "400 个种子包 + 额外奖励 60 个 Hot Date 种子包！",
    "1000 seed packets + BONUS 200 Hot Date seed packets!": "1000 个种子包 + 额外奖励 200 个 Hot Date 种子包！",
    "1000 seed packets + BONUS 500 Bombegranate seed packets!": "1000 个种子包 + 额外奖励 500 个炸弹榴种子包！",
    "2000 seed packets for Premium and World plants": "2000 个高级和世界植物种子包",
    "800 seed packets for Premium and World plants": "800 个高级和世界植物种子包",
    "300 seed packets for Premium and World plants": "300 个高级和世界植物种子包",
    "120 seed packets for Premium and World plants": "120 个高级和世界植物种子包",
    "200 seed packets for Premium and World plants": "200 个高级和世界植物种子包",
    "100 seed packets for Premium and World plants": "100 个高级和世界植物种子包",
    "50 seed packets for Premium and World plants": "50 个高级和世界植物种子包",
    "10 seed packets for World plants": "10 个世界植物种子包",
    "2 Premium Piñata. Limit 1 per player.": "2 个高级皮纳塔。每位玩家限购 1 次。",
    "1 Premium Piñata. Limit 1 per player.": "1 个高级皮纳塔。每位玩家限购 1 次。",
    "3 Premium Piñatas. Limit 1 per player.": "3 个高级皮纳塔。每位玩家限购 1 次。",
    "50 Pirate Seas seed packets!": "50 个海盗港湾种子包！",
    # Plant store blurbs
    "Boosts poison plants and fungi!": "强化毒性植物与蘑菇！",
    "Aloes heal injured plants to their immediate right.": "芦荟治疗右侧受伤的植物。",
    "Boosts straight shooters!": "强化直线射手！",
    "Lobs stunning cores down three lanes!": "向三行投掷可眩晕的核心！",
    "Boosts cannon and lobbing plants!": "强化大炮与投掷植物！",
    "Does increasing damage the more it hits!": "命中次数越多，伤害越高！",
    "Boosts explosive plants!": "强化爆炸植物！",
    "Explodes and leaves exploding seeds!": "爆炸并留下会爆炸的种子！",
    "Fires a penetrating thorn, hides for ground damage": "发射穿透尖刺，潜地造成地面伤害",
    "Cactus fires a penetrating thorn that can damage multiple enemies!": "仙人掌发射可伤害多个敌人的穿透尖刺！",
    "Hypnotizes random zombies!": "魅惑随机僵尸！",
    "Devours a zombie in one bite!": "一口吞掉一只僵尸！",
    "Cold Snapdragons breathe icy mist into 6 adjacent tiles.": "寒冰龙草向相邻 6 格喷吐冰雾。",
    "Boosts shadow plants!": "强化暗影植物！",
    "Boosts slowing plants!": "强化减速植物！",
    "Dandelions send explosive seeds down three different lanes, one lane at a time.": "蒲公英逐行向三条路线投下爆炸种子，每次一行。",
    "Randomly electrocutes zombies!": "随机电击僵尸！",
    "Electric Currants create electrical fences between ones planted on the same row or column.": "电流醋栗在同一行或同一列之间形成电网。",
    "Boosts magical plants!": "强化魔法植物！",
    "Boosts melee plants!": "强化近战植物！",
    "Boosts sun plants!": "强化阳光植物！",
    "Explodes and can be swapped!": "爆炸并可以换位！",
    "Explodes when eaten!": "被吃掉时爆炸！",
    "Boosts electricity plants!": "强化电力植物！",
    "Shoots flaming peas and warms nearby plants!": "发射火焰豌豆并温暖附近植物！",
    "Haunts all zombies that pass by.": "纠缠所有经过的僵尸。",
    "Produce a burst of sun all at once!": "一次性爆发大量阳光！",
    "Explodes and scatters bouncing projectiles!": "爆炸并散射弹跳弹体！",
    "Damage attacking zombies and launch prickly barriers to knock them back!": "伤害进攻的僵尸并发射尖刺屏障将其击退！",
    "Fires on zombie closest to house!": "攻击最靠近房子的僵尸！",
    "Attracts and burns zombies": "吸引并灼烧僵尸",
    "Push back and chill all zombies in lane!": "击退并冰冻整行僵尸！",
    "Turns zombies into allies!": "把僵尸变成友军！",
    "Fires jets of flame over a short distance!": "在短距离内喷射火焰！",
    "Ignites a whole row of zombies.": "点燃整行僵尸。",
    "Becomes more powerful as it's hurt!": "受伤越多变得越强！",
}

MINTS = {k: v for k, v in UI_VISIBLE.items() if k.endswith("-mint")}


def _plant_replacements(text: str) -> str:
    out = text
    for eng, zh in sorted({**EXTRA_PLANTS, **MINTS}.items(), key=lambda x: len(x[0]), reverse=True):
        if eng in out:
            out = out.replace(eng, zh)
    for eng, zh in sorted(WORLDS_EXT.items(), key=lambda x: len(x[0]), reverse=True):
        if eng in out:
            out = out.replace(eng, zh)
    for eng, zh in MOD_NAMES.items():
        if eng in out:
            out = out.replace(eng, zh)
    return out


def _zh_plant(eng: str) -> str:
    return EXTRA_PLANTS.get(eng.strip(), eng.strip())


def _polish_zh(s: str) -> str:
    out = s.replace("!", "！").replace("?", "？")
    out = re.sub(r"([\u4e00-\u9fffA-Za-z\-'’]+) 种子包", r"\1种子包", out)
    out = re.sub(r"([\u4e00-\u9fff]+) 皮纳塔", r"\1皮纳塔", out)
    out = re.sub(r"  +", " ", out)
    return out.strip()


def translate_commerce_en(en: str) -> str:
    out = en.replace("BONUS ", "额外奖励 ")
    num = r"(\d+(?:,\d+)?)"

    for eng, zh in sorted(WORLDS_EXT.items(), key=lambda x: len(x[0]), reverse=True):
        if eng not in out:
            continue
        esc = re.escape(eng)
        out = re.sub(rf"{num} seed packets for {esc} plants", rf"\1 个{zh}植物种子包", out)
        out = re.sub(rf"{esc} - {num} seed packets", rf"{zh} - \1 个种子包", out)
        out = re.sub(rf"{esc} Piñata", rf"{zh}皮纳塔", out)
        out = re.sub(rf"{num} {esc} seed packets!", rf"\1 个{zh}种子包！", out)

    out = re.sub(
        rf"{num} seed packets for Premium and World plants",
        r"\1 个高级和世界植物种子包",
        out,
    )
    out = re.sub(rf"{num} seed packets for World plants", r"\1 个世界植物种子包", out)

    categories = {
        "Nut Plant": "坚果类植物",
        "Nut Plants": "坚果类植物",
        "Sun Plant": "阳光植物",
        "Sun Plants": "阳光植物",
        "Mushroom": "蘑菇",
        "Mushrooms": "蘑菇",
        "Cold Plant": "寒冰植物",
        "Electric Plant": "电力植物",
        "Fruit Plant": "果实植物",
        "Greens": "绿色蔬菜",
        "Valenbrainz": "Valenbrainz",
        "Summer Nights": "夏夜",
        "Springening": "Springening",
    }
    for eng, zh in categories.items():
        esc = re.escape(eng)
        out = re.sub(rf"{num} {esc} seed packets!", rf"\1 个{zh}种子包！", out)
        out = re.sub(rf"Piñata – {esc}", rf"皮纳塔 – {zh}", out)
        out = re.sub(rf"{esc} Piñata", rf"{zh}皮纳塔", out)

    skip_names = {"Packets", "Pinata Seeds", "Piñata Seeds", "Premium Piñata", "Premium Pinata"}
    for eng, zh in sorted(EXTRA_PLANTS.items(), key=lambda x: len(x[0]), reverse=True):
        if eng in skip_names or not eng or not eng[0].isascii():
            continue
        if eng not in out:
            continue
        esc = re.escape(eng)
        out = re.sub(rf"{num} seed packets for {esc}", rf"\1 个{zh}种子包", out)
        out = re.sub(
            rf"{num} {esc} seed packets! Limit 1 per player\.?",
            rf"\1 个{zh}种子包！每位玩家限购 1 次。",
            out,
        )
        out = re.sub(rf"{num} {esc} seed packets!", rf"\1 个{zh}种子包！", out)
        out = re.sub(rf"{num} {esc} seed packets", rf"\1 个{zh}种子包", out)
        out = re.sub(rf"{num} {esc} Seed Packets", rf"\1 个{zh}种子包", out)
        out = re.sub(rf"{num} {esc} Packets", rf"\1 个{zh}种子包", out)
        out = re.sub(rf"Packets - {esc}", rf"种子包 - {zh}", out)
        out = re.sub(rf"Piñata - {esc}", rf"皮纳塔 - {zh}", out)
        out = re.sub(rf"Pinata - {esc}", rf"皮纳塔 - {zh}", out)

    out = re.sub(r"Premium Piñatas", "高级皮纳塔", out)
    out = re.sub(r"Premium Piñata", "高级皮纳塔", out)
    out = re.sub(r"Premium Pinatas", "高级皮纳塔", out)
    out = re.sub(r"Premium Pinata", "高级皮纳塔", out)
    out = re.sub(r"Limit 1 per player\.?", "每位玩家限购 1 次。", out)
    out = re.sub(r"Piñata – ", "皮纳塔 – ", out)
    out = re.sub(r"Pinata – ", "皮纳塔 – ", out)
    out = re.sub(r"Piñata - ", "皮纳塔 - ", out)
    out = re.sub(r"Pinata - ", "皮纳塔 - ", out)
    out = re.sub(r"Piñata", "皮纳塔", out)
    out = re.sub(r"Pinata", "皮纳塔", out)
    out = re.sub(r"Seed Packets", "种子包", out)
    out = re.sub(r"Seed Packet", "种子包", out)
    out = re.sub(r"One piñata", "一个皮纳塔", out, flags=re.I)
    out = re.sub(
        r"Three times the size of a normal piñata!",
        "普通皮纳塔的三倍大小！",
        out,
        flags=re.I,
    )
    out = re.sub(
        r"Level up your ([A-Za-z ]+?) plants!",
        lambda m: f"升级你的{_zh_plant(m.group(1))}植物！",
        out,
    )
    out = re.sub(r"Large ([A-Za-z ]+?) Piñata", lambda m: f"大型{_zh_plant(m.group(1))}皮纳塔", out)
    out = re.sub(r"Packets - ", "种子包 - ", out)

    if out != en:
        return _polish_zh(out)
    return en


def translate_value(en: str) -> str:
    if en in STATIC:
        return STATIC[en]
    exact = build_exact_map()
    if en in exact:
        return exact[en]
    if en in UI_VISIBLE:
        return UI_VISIBLE[en]
    # Glossary entries without trailing punctuation
    if en.rstrip("!.") in exact:
        base = exact[en.rstrip("!.")]
        if en.endswith("!"):
            return base + "！"
        if en.endswith("."):
            return base + "。"
        return base

    if en in EXTRA_PLANTS:
        return EXTRA_PLANTS[en]
    if en in MINTS:
        return MINTS[en]

    commerce = translate_commerce_en(en)
    if commerce != en:
        return commerce

    step = _polish_zh(_plant_replacements(apply_phrases(en)))
    if step != en:
        return step

    return en


def process_file(path: Path) -> tuple[int, list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    zh: dict[str, str] = {}
    untranslated: list[str] = []
    for k, v in data.items():
        t = translate_value(v)
        zh[k] = t
        if t == v and re.search(r"[A-Za-z]{4,}", v):
            untranslated.append(v)
    out = path.with_name(path.stem + ".zh.json")
    with out.open("w", encoding="utf-8") as f:
        json.dump(zh, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(data), untranslated


def main() -> None:
    parts = [f"batch_036_p{i:02d}.json" for i in range(6)]
    total = 0
    all_miss: list[str] = []
    for name in parts:
        p = CHUNK_DIR / name
        n, miss = process_file(p)
        en = json.loads(p.read_text(encoding="utf-8"))
        zh = json.loads((p.with_name(p.stem + ".zh.json")).read_text(encoding="utf-8"))
        assert list(en.keys()) == list(zh.keys()), name
        assert len(en) == len(zh) == n, name
        total += n
        all_miss.extend(miss)
        print(f"{name}: {n} keys, {len(miss)} maybe-untranslated")
    print(f"total keys: {total}")
    if all_miss:
        print("--- samples needing review ---")
        for s in sorted(set(all_miss))[:30]:
            print(s)


if __name__ == "__main__":
    main()
