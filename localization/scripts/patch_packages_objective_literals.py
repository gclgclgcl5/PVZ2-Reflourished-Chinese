#!/usr/bin/env python3
"""Replace English level-objective Description literals in Packages.

StarChallengeBeatTheLevelProps stores many player-facing objectives as raw
RTON ``0x90`` ASCII (e.g. ``Survive and protect the endangered plants``)
instead of LawnStrings keys. Headers like ``OBJECTIVE_CHALLENGE_HEADER_*``
are already Chinese; the bullet body stays English until these literals are
rewritten to equal-length ``[OBJ_…]`` tokens and Chinese is merged into
LawnStrings (same pattern as ``--stat-refs`` for almanac attributes).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

PROP = b"StarChallengeBeatTheLevelProps"
SKIP_EXACT = {
    "StarChallengeBeatTheLevelProps",
    "Description",
    "DescriptiveName",
    "Objective",
    "aliases",
    "objclass",
    "objdata",
    "Class",
    "Props",
    "Custom Objective",
}

# Extra custom / near-miss English → Chinese (beyond exact STARCHALLENGE values)
EXTRA_ZH: dict[str, str] = {
    "Survive and protect the endangered plant": "生存并保护濒危植物",
    "Survive and protect the endangered plants with the given plants": "使用选定植物生存并保护濒危植物",
    "Survive while the zombies are invisible": "在僵尸隐身时生存下来",
    "Plan your defense and defeat the zombies with the given plants": "使用选定植物规划防线并击败僵尸",
    "Survive without the shovel and Plant Food": "在没有铲子和叶绿素时生存",
    "Survive with a special seed bank": "使用特殊种子栏生存下来",
    "Survive without the shovel": "在没有铲子的情况下生存下来",
    "Survive with a special seedbank": "使用特殊种子栏生存下来",
    "Survive against giant but slow zombies": "对抗巨大但缓慢的僵尸并生存",
    "Survive with limited seed slots": "以有限的种子槽生存下来",
    "Survive with 8 seed slots": "使用 8 个种子槽生存下来",
    "Defeat 70 Electric Boogaloos": "击败 70 个电子布加洛",
    "Survive the zombie attack with the given plants with extra starting sun": "使用选定植物并携带额外初始阳光生存",
    "Survive and protect the endangered plant with the given plants": "使用选定植物生存并保护濒危植物",
    "Sit back, relax and enjoy the show!": "放松坐下，好好欣赏表演吧！",
    "Survive the zombie attack with the given plant": "使用选定植物抵挡僵尸进攻",
    "Survive with a special Seed Chooser": "使用特殊选种界面生存下来",
    "Survive a massive attack during Feastivus": "在盛宴节的大规模进攻中生存",
    "Survive with extra starting sun": "携带额外初始阳光生存下来",
    "Survive while Power Tiles change locations every flag wave": "在能量地砖每波换位时生存",
    "Survive while speed boosting potions & holiday drinks boost the zombies": "在加速药水与节日饮品强化僵尸时生存",
    "Survive with only 11000 sun and without sun producers": "仅用 11000 阳光且不用产阳植物生存",
    "Survive with a special seed bank with extra starting sun": "使用特殊种子栏并携带额外初始阳光生存",
    "Survive and protect at least 5 Moonflowers": "生存并至少保护 5 株月光花",
    "Survive while Sun Bombs fall with the given plants": "使用选定植物并在阳光炸弹坠落时生存",
    "Unthaw 13 plants": "解冻 13 株植物",
    "Survive and protect atleast 6 endangered plants": "生存并至少保护 6 株濒危植物",
    "Survive without Blover, Hurrikale, Draftodil and Spikeweeds.": "禁止使用三叶草、飓风甘蓝、气流水仙与地刺",
    "Don't let the zombies trample the flowers without flowers": "在没有花朵标记时也不让僵尸践踏花坛",
    "Sit back and relax at Zomboss' party": "在僵王派对上放松休息",
    "Survive while evil potions and seasonal greetings boost zombies": "在邪恶药水与节日问候强化僵尸时生存",
    "Survive a massive Imp attack with extra starting sun.": "携带额外初始阳光抵挡大规模小鬼进攻",
    "Survive while some imps are faster and have increased eating speed": "在部分加速、啃食更快的小鬼进攻下生存",
    "Survive a well-cooked attack by ZCorp.": "抵挡 ZCorp 精心炮制的进攻",
    "Survive while imps come in various conditions": "在各种状态的小鬼进攻下生存",
    "Survive while only being able to store up to 500 sun with the given plants": "使用选定植物且阳光上限 500 时生存",
    "Survive with a nostalgic seed bank": "使用怀旧种子栏生存下来",
    "Survive while the conveyor speeds up the more plants that are in it": "传送带植物越多速度越快时生存",
    "Survive with plant food powered cauldrons supplying plants": "用叶绿素驱动的坩埚供应植物并生存",
    "Survive an execution order by Greedy Zomtarani with extra starting sun.": "携带额外初始阳光抵挡贪婪僵塔拉尼的处决令",
    "Survive a terrifying death report from Zcorp with extra starting sun.": "携带额外初始阳光抵挡 ZCorp 死亡报告",
    "Survive and protect at least 6 endangered plants with extra starting sun": "携带额外初始阳光并至少保护 6 株濒危植物",
    "Survive a massive attack during Feastivus": "在盛宴节的大规模进攻中生存",
    # Lower-frequency custom Reflourished lines
    "Survive with extra prep time while most waves are taken from previous challenges!": "额外准备时间，多数波次来自先前挑战！",
    "Survive with extra starting sun while only being able to store up to 650 sun without primary sun producers": "额外初始阳光，无主产阳植物且阳光上限 650",
    "Plan your defense and defeat the zombies without the shovel, frozen zombies will be released when you start": "无铲子规划防线；开局将放出冰冻僵尸",
    "Plan your defense and defeat the zombies with 8 seed slots and 25% faster cooldown on plants": "8 种子槽且植物冷却加快 25% 时规划防线",
    "Survive and protect the endangered plants with the given plants with much longer recharge times": "使用选定植物保护濒危植物（冷却大幅延长）",
    "Survive the zombie attack with the given plants while only being able to hold up to 500 sun": "使用选定植物且阳光上限 500 时生存",
    "Survive and protect the endangered plants with some plants recommended by Crazy Dave": "按疯狂戴夫推荐的部分植物保护濒危植物",
    "Plan your defense and defeat the zombies with a special seedbank": "使用特殊种子栏规划防线并击败僵尸",
    "Survive while all Tarot Cards are harmful with extra starting sun": "塔罗牌全为有害时，携带额外初始阳光生存",
    "Defeat 10 Carnie Teddies": "击败 10 个嘉年华泰迪",
    "Survive while the tarot cards constantly shuffle!": "在塔罗牌不断洗牌时生存下来！",
    "Survive with a limited plant selection": "在有限的植物选择下生存下来",
    "Plant the Repeater to begin": "种植双发射手以开始",
    "Defeat 20 Clockwork Zombies!": "击败 20 个发条僵尸！",
    "Never have more than 3 plants": "场上植物不得超过 3 株",
    "Survive the collision with the Alternate UniverZ!": "在与平行宇宙的碰撞中存活！",
    "Survive and protect the endangered plants with the given plants and with a sizeable amount of sun": "使用选定植物与充足阳光保护濒危植物",
    "Let 15 Ghosts scare plants": "让 15 个幽灵吓到植物",
    "Survive and endure Penny's simulation for 9 minutes!": "在潘妮的模拟中坚持 9 分钟！",
    "Survive a massive attack from another Alternate UniverZ with almost every plants and seed slots available": "几乎全植物全槽位下抵挡平行宇宙的大规模进攻",
    "Survive the ultimate attack during the Jester Takeover": "在小丑接管期间抵挡终极进攻",
    "Survive a familiar battleground...": "在熟悉的战场上生存下来……",
    "Survive while gravestones spawn and evil potions boost zombies": "在墓碑不断生成且邪恶药水强化僵尸时生存",
    "Survive and protect the endangered Plants with the given plants": "使用选定植物生存并保护濒危植物",
    "Survive and protect the endangered plants with the given plants while only being able to store up to 500 sun": "使用选定植物保护濒危植物（阳光上限 500）",
    "Survive a massive attack in Present Tense": "在「现在时」的大规模进攻中生存",
    "Defeat 35 imps!": "击败 35 个小鬼！",
    "Defeat 125 Carthead Zombies": "击败 125 个推车头僵尸",
    "Don't let backwards zombies reach the blueprints": "不要让倒走僵尸抵达蓝图",
    "Survive and protect the endangered plants with the most plants picked for you": "使用已为你选好的大部分植物，生存并保护濒危植物",
    "Survive the zombie attack with the given plants while evil potions boost the zombies": "使用选定植物抵挡僵尸进攻，且邪恶药水会强化僵尸",
    "Plan your defense with the given plants and defeat the zombies": "使用选定植物规划防线并击败僵尸",
    "Plan your defense and defeat the zombies": "规划防线并击败僵尸",
    "Extra tombstones complicate your planting": "额外墓碑使种植更困难",
    "Survive without using any sun producers": "不使用任何产阳植物时生存",
    "Never have more than {COUNT} plants": "场上同时不超过 {COUNT} 株植物",
    "Survive without planting on Dave's mold colonies": "不要把植物种在戴夫的霉菌落上",
    "Survive and protect the endangered plants": "生存并保护濒危植物",
    "Survive the zombie attack with the given plants": "使用选定植物抵挡僵尸进攻",
    "Survive while evil potions boost zombies": "在邪恶药水强化僵尸时生存",
}


def discover_objective_literals(section: bytes) -> collections.Counter[str]:
    hits: collections.Counter[str] = collections.Counter()
    i = 0
    while True:
        j = section.find(PROP, i)
        if j < 0:
            break
        window = section[j : j + 360]
        k = 0
        while k < len(window) - 2:
            if window[k] == 0x90:
                ln = window[k + 1]
                s = window[k + 2 : k + 2 + ln]
                if len(s) == ln and all(32 <= b < 127 for b in s):
                    txt = s.decode("ascii")
                    if (
                        txt not in SKIP_EXACT
                        and " " in txt
                        and len(txt) >= 12
                        and not txt.startswith("#")
                    ):
                        hits[txt] += 1
                    k += 2 + ln
                    continue
            k += 1
        i = j + 1
    return hits


def starchallenge_en_to_zh(en: dict[str, str], zh: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in en.items():
        if not k.startswith("STARCHALLENGE_"):
            continue
        if not isinstance(v, str) or " " not in v or len(v) < 12:
            continue
        z = zh.get(k)
        if isinstance(z, str) and z and z != v:
            out[v] = z
    return out


def _slug_body(eng: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", eng.strip())
    s = re.sub(r"_+", "_", s).strip("_").upper()
    return s or "X"


def make_obj_ref(eng: str, used_keys: set[str]) -> tuple[str, str]:
    """Equal-length ``[OBJ_…]`` and bare LawnStrings KEY."""
    n = len(eng)
    if n < 6:
        raise ValueError(f"too short for [OBJ] ref: {eng!r}")
    inner_n = n - 2
    slug = _slug_body(eng)
    base = "OBJ_" + slug if inner_n >= 6 else slug
    body = base[:inner_n] if len(base) > inner_n else base + ("_" * (inner_n - len(base)))
    if body in used_keys:
        for i in range(1, 10000):
            suffix = str(i)
            if len(suffix) >= inner_n:
                break
            cand = body[: inner_n - len(suffix)] + suffix
            if cand not in used_keys:
                body = cand
                break
        else:
            raise SystemExit(f"cannot uniquify OBJ key for {eng!r}")
    used_keys.add(body)
    ref = f"[{body}]"
    if len(ref) != n:
        raise SystemExit(f"OBJ ref length mismatch: {eng!r} -> {ref!r}")
    return ref, body


def build_translation_table(
    discovered: collections.Counter[str],
    *,
    en: dict[str, str],
    zh: dict[str, str],
) -> dict[str, str]:
    table = dict(starchallenge_en_to_zh(en, zh))
    table.update(EXTRA_ZH)
    # Only keep strings that actually appear (or EXTRA for safety)
    out: dict[str, str] = {}
    for eng in discovered:
        if eng in table:
            out[eng] = table[eng]
    # Also include exact STARCHALLENGE values even if discover missed (global 0x90)
    for eng, zhs in table.items():
        if eng.encode("ascii", "ignore") == eng.encode("ascii") and len(eng) <= 255:
            out.setdefault(eng, zhs)
    return out


def patch_section(
    section: bytes,
    translations: dict[str, str],
    lawn_zh: dict[str, str] | None,
) -> tuple[bytes, dict[str, int], dict[str, str]]:
    data = bytearray(section)
    counts: dict[str, int] = {}
    new_keys: dict[str, str] = {}
    used: set[str] = set()
    # longer first
    items = sorted(translations.items(), key=lambda kv: len(kv[0]), reverse=True)
    rewrites: dict[str, tuple[str, str]] = {}
    for eng, zhs in items:
        if len(eng) < 6:
            continue
        try:
            eng.encode("ascii")
        except UnicodeEncodeError:
            continue
        ref, key = make_obj_ref(eng, used)
        rewrites[eng] = (ref, key)

    for eng, zhs in items:
        if eng not in rewrites:
            continue
        needle = eng.encode("ascii")
        repl_s, key = rewrites[eng]
        repl = repl_s.encode("ascii")
        new_keys[key] = zhs
        if lawn_zh is not None:
            lawn_zh[key] = zhs
        start = 0
        n = 0
        while True:
            i = data.find(needle, start)
            if i < 0:
                break
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
    ap.add_argument("section", type=Path, help="decompressed packages_section.bin")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument(
        "--lawnstrings-en",
        type=Path,
        default=None,
        help="LawnStrings_en.json for STARCHALLENGE value→key map",
    )
    ap.add_argument(
        "--lawnstrings-zh",
        type=Path,
        required=True,
        help="LawnStrings_zh.json to merge new OBJ keys into",
    )
    ap.add_argument("--keys-out", type=Path, default=None)
    ap.add_argument(
        "--discover-only",
        action="store_true",
        help="print discovered literals and exit",
    )
    args = ap.parse_args()

    section = args.section.read_bytes()
    discovered = discover_objective_literals(section)
    en = (
        json.loads(args.lawnstrings_en.read_text(encoding="utf-8"))
        if args.lawnstrings_en
        else {}
    )
    zh = json.loads(args.lawnstrings_zh.read_text(encoding="utf-8"))

    if args.discover_only:
        table = build_translation_table(discovered, en=en, zh=zh)
        for txt, c in discovered.most_common(80):
            flag = "OK" if txt in table else "MISS"
            print(f"{flag} n={c:4d} len={len(txt):3d} {txt}")
        miss = [t for t in discovered if t not in table]
        print(f"discovered={len(discovered)} translated={len(discovered)-len(miss)} miss={len(miss)}")
        return

    translations = build_translation_table(discovered, en=en, zh=zh)
    out, counts, new_keys = patch_section(section, translations, zh)
    args.out.write_bytes(out)
    print(f"wrote {args.out} ({len(out)} bytes)")
    print(f"patched {sum(counts.values())} occurrences across {len(counts)} literals")
    for eng, n in sorted(counts.items(), key=lambda kv: -kv[1])[:30]:
        print(f"  {n:3d}  {eng!r}")
    if len(counts) > 30:
        print(f"  ... {len(counts) - 30} more")
    miss = sorted(t for t in discovered if t not in translations)
    if miss:
        print(f"WARNING: {len(miss)} discovered literals still untranslated (left English)")
        for t in miss[:20]:
            print(f"  MISS n={discovered[t]} {t}")

    if args.keys_out:
        args.keys_out.write_text(
            json.dumps(new_keys, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote keys {args.keys_out} ({len(new_keys)})")
    args.lawnstrings_zh.write_text(
        json.dumps(zh, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"updated {args.lawnstrings_zh} (+{len(new_keys)} keys)")


if __name__ == "__main__":
    main()
