# -*- coding: utf-8 -*-
"""Audit & align LawnStrings_zh to PvZ Wiki 译名对照 (zh-CN 建议使用名)."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"F:\othergit\Reverse Engineer Anything")
WIKI_TXT = Path(
    r"C:\Users\Administrator\.cursor\projects\f-othergit-Reverse-Engineer-Anything\agent-tools\19bfa697-8caa-4978-840f-87ba159d5b40.txt"
)
ZH_PATH = ROOT / "localization" / "LawnStrings_zh.json"
OUT_REPORT = ROOT / "localization" / "wiki_name_audit_report.txt"


def parse_zh_cn(cell: str) -> str | None:
    cell = cell.strip()
    if not cell or cell in ("（无）", "(无)", "无"):
        return None
    cell = re.sub(r"\s*\[\d+\]", "", cell).strip()
    m = re.search(r"([^\s`（(]+)\s*（\s*`?zh-CN`?\s*）", cell)
    if m:
        return m.group(1)
    # drop trailing empty markers
    cell = re.sub(r"\s*（无）\s*$", "", cell).strip()
    if not cell:
        return None
    # first whitespace-separated token (Chinese names)
    return cell.split()[0]


def parse_wiki(path: Path) -> tuple[dict[str, str], dict[str, set[str]]]:
    """Return en->wiki_zh and wiki_zh->{alts from old/CN columns}."""
    text = path.read_text(encoding="utf-8")
    en_to_wiki: dict[str, str] = {}
    alts: dict[str, set[str]] = defaultdict(set)
    for line in text.splitlines():
        if not line.startswith("| ") or line.startswith("| ---") or "英文原名" in line:
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        en, zh_cn, zh_tw, old, cn = parts[0], parts[1], parts[2], parts[3], parts[4]
        if en in ("英文原名",):
            continue
        wiki = parse_zh_cn(zh_cn)
        if not wiki:
            continue
        en_to_wiki[en] = wiki
        for col in (old, cn, zh_tw):
            # collect alternate Chinese names from other columns
            col = re.sub(r"\s*\[\d+\]", "", col).strip()
            if not col or col in ("（无）", "(无)", "无"):
                continue
            # strip zh-CN annotations for alt harvest
            col2 = re.sub(r"（\s*`?zh-(?:CN|TW|HK|MO|MY|SG)`?\s*）", "", col)
            for tok in re.split(r"\s+", col2.strip()):
                tok = tok.strip(".“”\"'")
                if not tok or tok == wiki:
                    continue
                if re.search(r"[\u4e00-\u9fff]", tok):
                    alts[wiki].add(tok)
        # also alts from zh_cn cell when dual names without consuming wiki pick
        raw = re.sub(r"\s*\[\d+\]", "", zh_cn)
        raw = re.sub(r"（\s*`?zh-CN`?\s*）", "", raw)
        for tok in re.split(r"\s+", raw.strip()):
            if tok and tok != wiki and re.search(r"[\u4e00-\u9fff]", tok):
                alts[wiki].add(tok)
    return en_to_wiki, alts


def main() -> None:
    en_to_wiki, alts = parse_wiki(WIKI_TXT)
    zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    en = json.loads((ROOT / "localization" / "LawnStrings_en.json").read_text(encoding="utf-8"))

    # Extra known wrong forms → wiki (glossary / prior MT / ref pack)
    EXTRA_WRONG: list[tuple[str, str]] = [
        ("断魂椒", "幽灵辣椒"),
        ("铃儿草投手", "绽放之心"),
        ("铃儿草", "绽放之心"),
        ("超能花菜", "超能力花椰菜"),
        ("花椰菜武帝", "超能力花椰菜"),
        ("一品轰", "弹跳一品红"),
        ("弹跳秋海棠", "弹跳一品红"),
        ("啵嘤一品红", "弹跳一品红"),
        ("冰刺草", "冰地刺"),
        ("等离子香橼", "香橼"),
        ("保鳞茎", "保龄鳞茎"),
        ("节拍甜菜", "绝佳甜菜"),
        ("动感甜菜", "绝佳甜菜"),
        ("魔音甜菜", "绝佳甜菜"),
        ("阿开木-木", "阿开木"),
        ("阿.开.木.木.", "阿开木"),
        ("阿开木木", "阿开木"),
        ("薄暮掷手", "薄暮投手"),
        ("幽暮投手", "薄暮投手"),
        ("炙鞭山葵", "山葵鞭"),
        ("炙热山葵", "山葵鞭"),
        ("爆冰槲寄生", "导弹槲寄生"),
        ("槲寄冰仙子", "导弹槲寄生"),
        ("巫术金缕梅", "金缕梅"),
        ("金缕梅女巫", "金缕梅"),
        ("夜影茄", "夜影花"),
        ("夜影龙葵", "夜影花"),
        ("暗影蘑菇", "暗影菇"),
        ("毒影菇", "暗影菇"),
        ("逃脱树根", "逃脱根"),
        ("墓碑玫瑰", "阴沉报春"),
        ("暗樱草", "阴沉报春"),
        ("黄金蓓蕾", "黄金花"),
        ("电能豌豆射手", "电豌豆射手"),
        ("电力豌豆射手", "电豌豆射手"),
        # Mint short ParaTranz names → wiki (only as full token / family labels)
        ("衰薄家族", "疾病薄荷家族"),
        ("喷薄家族", "豌豆薄荷家族"),
        ("重荷家族", "军械薄荷家族"),
        ("爆薄家族", "轰炸薄荷家族"),
        ("蔽薄家族", "隐藏薄荷家族"),
        ("负荷家族", "限制薄荷家族"),
        ("魔荷家族", "施法薄荷家族"),
        ("搏荷家族", "强迫薄荷家族"),
        ("祝荷家族", "供光薄荷家族"),
        ("电荷家族", "灯丝薄荷家族"),
        ("暖荷家族", "辣椒薄荷家族"),
        ("载荷家族", "加固薄荷家族"),
        ("挑薄家族", "尖刺薄荷家族"),
        ("寒薄家族", "冬季薄荷家族"),
        ("衰薄", "疾病薄荷"),
        ("喷薄", "豌豆薄荷"),
        ("重荷", "军械薄荷"),
        ("爆薄", "轰炸薄荷"),
        ("蔽薄", "隐藏薄荷"),
        ("魔荷", "施法薄荷"),
        ("搏荷", "强迫薄荷"),
        ("祝荷", "供光薄荷"),
        ("暖荷", "辣椒薄荷"),
        ("载荷", "加固薄荷"),
        ("挑薄", "尖刺薄荷"),
        ("寒薄", "冬季薄荷"),
        ("榴镰", "榴梿"),
        ("香水蘑菇", "香水菇"),
        ("冰西瓜投手", "冬瓜"),
        ("冰西瓜", "冬瓜"),  # careful after 冬瓜
        ("窝瓜", "倭瓜"),
        ("双胞向日葵", "双子向日葵"),
        ("双重射手", "双发射手"),
        ("三重射手", "三线射手"),
        ("回旋镖射手", "回旋花"),
        ("充能柚子", "香橼"),
        ("脉冲黄桃", "电磁脉冲桃"),
        ("星星果", "杨桃"),
        ("全息坚果", "无穷坚果"),
        ("棱镜草", "放大草"),
        ("瓷砖萝卜", "地砖芜菁"),
        ("地砖萝卜", "地砖芜菁"),
        ("甜薯", "红薯"),
        ("树脂投手", "树液投手"),
        ("烤马铃薯", "热马铃薯"),
        ("辣椒投手", "甜椒投手"),
        ("爆炸草莓", "爆裂草莓"),
        ("逆时草", "逆时百里香"),
        ("复活萝卜", "加护胡萝卜"),
        ("杰克南瓜", "南瓜灯"),
        ("爆裂葡萄", "葡萄弹"),
        ("缩小紫罗兰", "缩小堇菜"),
        ("腐尸豆荚", "僵尸豆荚"),
        ("豌豆迫击炮", "投掷豌豆"),
        ("食人花豌豆", "大嘴豌豆"),
        ("毒液豌豆射手", "黏液豌豆射手"),
        ("电力绿茶", "电能茶"),
        ("尖刺秋葵", "戳刺秋葵"),
        ("小黄梨", "小鬼梨"),
        ("橄榄坑", "油橄榄坑"),
        ("黏弹糯米", "黏弹糯稻"),
        ("魔法番红花", "魔术番红花"),
        ("气流水仙花", "气流水仙"),
        ("爆炸桔梗", "爆炸气球花"),
        ("烈焰火蕨", "地狱蕨"),
        ("电能藤蔓", "电力藤蔓"),
        ("石楠探索者", "欧石南导引头"),
        ("斯巴达竹", "斯巴达竹子"),
        ("斯笆达", "斯巴达竹子"),
        ("弄臣僵尸", "小丑僵尸"),
        ("僵尸王", "僵尸国王"),  # may over-replace 僵王博士? 僵尸王 as substring of 僵尸国王 only if exact
        ("渔夫僵尸", "钓鱼僵尸"),
        ("鸡贼僵尸", "牧鸡僵尸"),
        ("闪动僵尸", "闪光僵尸"),
        ("说唱僵尸", "饶舌僵尸"),
        ("魔法师僵尸", "巫师僵尸"),
        ("国王僵尸", "僵尸国王"),
        ("浮潜僵尸", "潜水僵尸"),
        ("录音机僵尸", "音响僵尸"),
        # worlds (wiki 建议使用名)
        ("上古埃及", "神秘埃及"),
        ("极寒冰窟", "冻伤洞穴"),
        ("眩光魔音游", "霓虹灯混音带巡演"),
        ("炫光魔音游", "霓虹灯混音带巡演"),
        ("霓虹旋音游", "霓虹灯混音带巡演"),
        ("霓虹混音游", "霓虹灯混音带巡演"),
        ("现代年华", "现代时光"),
        ("现代世界", "现代时光"),
        ("摩登时代", "现代时光"),
        ("摩登世界", "现代时光"),
        ("恐龙危机", "侏罗纪沼泽"),
        ("巨浪沙滩", "巨浪海滩"),
        ("冰河世界", "冻伤洞穴"),
        ("未来世界", "遥远未来"),
    ]

    # Build replace list: EXTRA + (alt -> wiki) from table, longer first
    repl: dict[str, str] = {}
    for wrong, right in EXTRA_WRONG:
        repl[wrong] = right
    for wiki, altset in alts.items():
        for a in altset:
            if a == wiki:
                continue
            # skip overly short / dangerous
            if len(a) < 2:
                continue
            if a in ("无", "现代", "普通", "中", "近身"):
                continue
            # don't map 坚果 -> 坚果墙 globally (too broad); Wall-nut handled via longer forms
            if a == "坚果" and wiki == "坚果墙":
                continue
            if a == "花生" and wiki == "花生":
                continue
            if a == "南瓜" and wiki == "南瓜":
                continue
            # 负荷/电荷 alone too dangerous as mint-only — already in EXTRA with care
            if a in ("负荷", "电荷") and wiki.endswith("薄荷"):
                continue
            repl[a] = wiki

    # Dangerous globals to remove
    for bad in ("负荷", "电荷", "僵尸王"):
        repl.pop(bad, None)

    # Special: 僵尸王 -> 僵尸国王 only as whole word-ish (not inside 僵王博士)
    # handled separately

    ordered = sorted(repl.items(), key=lambda kv: -len(kv[0]))

    # --- Audit before ---
    lines: list[str] = []
    lines.append(f"Wiki entries parsed: {len(en_to_wiki)}")
    lines.append(f"Replacement rules: {len(ordered)}")

    # Presence of wiki name vs known alts
    mismatch_examples: list[str] = []
    for en_name, wiki_name in sorted(en_to_wiki.items(), key=lambda x: x[0].lower()):
        wiki_n = sum(1 for v in zh.values() if isinstance(v, str) and wiki_name in v)
        alt_hits = []
        for a in sorted(alts.get(wiki_name, []), key=len, reverse=True):
            if a == wiki_name or len(a) < 2:
                continue
            n = sum(1 for v in zh.values() if isinstance(v, str) and a in v)
            if n:
                alt_hits.append((a, n))
        # also check EXTRA wrongs targeting this wiki
        for w, r in EXTRA_WRONG:
            if r == wiki_name and w != wiki_name:
                n = sum(1 for v in zh.values() if isinstance(v, str) and w in v)
                if n and (w, n) not in alt_hits:
                    alt_hits.append((w, n))
        if alt_hits and (wiki_n == 0 or any(n > 0 for _, n in alt_hits)):
            # report if alts present
            if any(n > 0 for _, n in alt_hits):
                mismatch_examples.append(
                    f"{en_name} => wiki「{wiki_name}」x{wiki_n}; alts "
                    + ", ".join(f"「{a}」x{n}" for a, n in alt_hits[:6])
                )

    lines.append(f"\nTerms with alternate forms still in corpus: {len(mismatch_examples)}")
    for row in mismatch_examples[:80]:
        lines.append("  " + row)
    if len(mismatch_examples) > 80:
        lines.append(f"  ... +{len(mismatch_examples)-80} more")

    # --- Apply ---
    changed = 0
    hit_counter: Counter[str] = Counter()

    def apply_one(text: str) -> str:
        nv = text
        for old, new in ordered:
            if old in nv:
                c = nv.count(old)
                nv2 = nv.replace(old, new)
                if nv2 != nv:
                    hit_counter[f"{old}->{new}"] += c
                    nv = nv2
        # 僵尸王 not inside 僵王/僵尸国王
        nv2 = re.sub(r"(?<!僵)僵尸王(?!国)", "僵尸国王", nv)
        if nv2 != nv:
            hit_counter["僵尸王->僵尸国王"] += len(re.findall(r"(?<!僵)僵尸王(?!国)", nv))
            nv = nv2
        # mint family suffixes: 疾病薄荷家族 already ok; fix 「衰薄家族」 etc. after 衰薄->疾病薄荷
        return nv

    for k, v in list(zh.items()):
        if not isinstance(v, str):
            continue
        nv = apply_one(v)
        if nv != v:
            zh[k] = nv
            changed += 1

    # Post-check dangerous doubles
    for bad in ("疾病疾病薄荷", "遥遥远未来", "僵尸僵尸国王", "霓虹灯霓虹灯"):
        n = sum(1 for v in zh.values() if isinstance(v, str) and bad in v)
        lines.append(f"double-check {bad}: {n}")

    payload = json.dumps(zh, ensure_ascii=False, indent=2) + "\n"
    ZH_PATH.write_text(payload, encoding="utf-8")

    lines.append(f"\nkeys changed: {changed}")
    lines.append("top replacements:")
    for h, n in hit_counter.most_common(60):
        lines.append(f"  {n:4d}  {h}")

    # sync sen + flats
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
            val = vals[i + 1]
            if not isinstance(val, str):
                continue
            nv = apply_one(val)
            if nv != val:
                vals[i + 1] = nv
                n += 1
        sp.write_text(json.dumps(sen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        lines.append(f"sen {sp.name}: {n}")

    for p in [
        ROOT / "localization" / "current" / "LawnStrings_zh.json",
        Path(r"F:\sen_work\LawnStrings_zh.json"),
        Path(r"F:\sen_work\current\LawnStrings_zh.json"),
    ]:
        p.write_text(payload, encoding="utf-8")

    # save wiki map for reuse
    map_path = ROOT / "localization" / "wiki_zh_cn_names.json"
    map_path.write_text(
        json.dumps(en_to_wiki, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:100]))
    print("...")
    print(f"full report: {OUT_REPORT}")
    print(f"wiki map: {map_path}")


if __name__ == "__main__":
    main()
