# -*- coding: utf-8 -*-
"""Align contested terms to 参考翻译2 plant names + selected system terms."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZH_PATH = ROOT / "localization" / "LawnStrings_zh.json"

# Longer / more specific first. Targets = 参考翻译2 植物短名 + 用户选定系统词。
GLOBAL: list[tuple[str, str]] = [
    # --- system / user-selected ---
    ("植物养料", "叶绿素"),
    ("升级道具", "强化道具"),
    ("幼芽", "幼苗"),
    ("催眠", "魅惑"),
    ("壁球", "窝瓜"),
    ("倭瓜", "窝瓜"),
    # Neon world
    ("眩光魔音游", "炫光魔音游"),
    ("霓虹旋音游", "炫光魔音游"),
    # --- plant names → 参考翻译2（含旧别名）---
    ("超能力花椰菜", "超能花菜"),
    ("花椰菜武帝", "超能花菜"),
    ("超能花菜", "超能花菜"),  # no-op keep
    ("弹跳一品红", "一品红"),
    ("弹跳秋海棠", "一品红"),
    ("啵嘤一品红", "一品红"),
    ("一品轰", "一品红"),
    ("铃儿草投手", "心之蕊"),
    ("绽放之心", "心之蕊"),
    ("铃儿草", "心之蕊"),
    ("断魂椒", "幽灵鬼椒"),
    ("幽灵辣椒", "幽灵鬼椒"),
    ("等离子香橼", "充能柚子"),
    ("香橼", "充能柚子"),
    ("保鳞茎", "保龄泡泡"),
    ("保龄鳞茎", "保龄泡泡"),
    ("节拍甜菜", "魔音甜菜"),
    ("动感甜菜", "魔音甜菜"),
    ("绝佳甜菜", "魔音甜菜"),
    ("薄暮掷手", "幽暮投手"),
    ("薄暮投手", "幽暮投手"),
    ("拳击卷心菜", "菜问"),
    ("拳击白菜", "菜问"),
    ("回旋花", "回旋镖射手"),
    ("地砖芜菁", "瓷砖萝卜"),
    ("烟雾菇", "大喷菇"),
    ("雪花豌豆", "寒冰射手"),
    ("无穷坚果", "全息坚果"),
    ("土豆地雷", "土豆雷"),
    ("原始土豆地雷", "原始土豆雷"),
    ("传送土豆地雷", "传送土豆雷"),
    ("变身洋芋", "变身茄子"),
    ("蟾蜍毒菌", "金蟾菇"),
    ("墓碑吞噬者", "墓碑苔藓"),
    ("电能茶", "电力绿茶"),
    ("电力豌豆射手", "电能豌豆"),
    ("电磁脉冲桃", "脉冲黄桃"),
    ("榴镰", "榴莲"),
    ("猕猴桃野兽", "野兽猕猴桃"),
    ("岩浆番石榴", "熔岩番石榴"),
    ("睡莲叶", "莲叶"),
    ("磁铁菇", "磁力菇"),
    ("透镜草", "棱镜草"),
    ("爆冰槲寄生", "槲寄冰仙子"),
    ("黑暗夏威夷果", "暗影夏威夷果"),
    ("夜影茄", "夜影龙葵"),
    ("欧防锋", "防风草"),
    ("顽斗花生", "花生"),
    ("戳刺秋葵", "尖刺秋葵"),
    ("能量百合", "能量花"),
    ("双发豌豆", "双发射手"),
    ("树脂抛手", "树脂投手"),
    ("暗影菇", "毒影菇"),
    ("闪耀藤蔓", "阳光藤蔓"),
    ("缩小堇菜", "缩小紫罗兰"),
    ("投掷豌豆", "豌豆迫击炮"),
    ("地刺石", "钢地刺"),
    ("地刺草", "地刺"),
    ("裂荚豌豆", "分裂豌豆"),
    ("杨桃", "星星果"),
    ("缠绕海带", "缠绕海草"),
    ("三线豌豆", "三线射手"),
    ("逆时百里香", "逆时草"),
    ("巫术金缕梅", "金缕梅女巫"),
    ("冰瓜投手", "冰西瓜投手"),
    ("旋转洋芜菁", "旋转芜菁"),
    ("终级番茄", "终极番茄"),
    ("冰山生菜", "冰冻生菜"),
    ("医护胡萝卜", "复活萝卜"),
    ("潜伏芹菜", "潜袭芹菜"),
    ("辣豆", "巴豆"),
    ("炸弹石榴", "爆破石榴"),
    ("爆炸气球花", "爆炸桔梗"),
    ("莓棘灌木丛", "荆莓灌木"),
    ("迷乱雏菊束", "迷乱雏菊"),
    ("树胶桉果", "黏液桉果"),
    ("石南导引头", "石楠探索者"),
    ("魔术番红花", "魔法番红花"),
    ("冬青屏障", "冬青骑士"),
    # 勿加「南瓜灯→杰克南瓜灯」或「南瓜→南瓜头」：后者会把前者结果改成「杰克南瓜头灯」
    ("葬火藤蔓", "烈焰藤蔓"),
    ("报丧花", "暗樱草"),
    ("阿开木-木", "阿.开.木.木."),
    # --- 阶段性 A 组（明显优于旧译）---
    ("耳鼻喉科", "树灵护卫"),
    ("尼斯帕雷奥", "漩涡枇杷"),
    ("虹膜", "鸢尾花"),
    ("导弹吐司", "槲寄火仙子"),
    # 勿全局替换「海棠」→屏胀菠萝（会误伤秋海棠）；短名键已定点写入
    ("加特林豌豆", "机枪豌豆"),
    ("伟大的西葫芦", "大师葫迪尼"),
    ("酸液柠檬", "强酸柠檬"),
    ("灰飞烟灭", "化灰"),
    ("奶酪草莓", "芝芝莓莓"),
    ("冷冻梨", "冻梨"),
    ("P-15 小鹰吊舱", "P-15鹰式战豆机"),
    ("雾霾蘑菇", "朦雾菇"),
    ("帽子蘑菇", "疯帽菇"),
    ("碟形南瓜头", "飞碟瓜"),
    ("太阳豌豆", "禅宗豌豆"),
    ("春公主", "公主弹簧草"),
    ("甜豌豆", "糖豌豆"),
    ("毒缓", "失速"),
]


def fix_text(text: str, key: str | None = None) -> str:
    nv = text
    for old, new in GLOBAL:
        if old == new:
            continue
        if old in nv:
            nv = nv.replace(old, new)
    return nv


def main() -> None:
    zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    changed = 0
    hits: dict[str, int] = {}
    for k, v in list(zh.items()):
        if not isinstance(v, str):
            continue
        before = v
        nv = fix_text(v, k)
        if nv != before:
            for old, new in GLOBAL:
                if old == new:
                    continue
                if old in before:
                    hits[f"{old}->{new}"] = hits.get(f"{old}->{new}", 0) + before.count(
                        old
                    )
            zh[k] = nv
            changed += 1

    payload = json.dumps(zh, ensure_ascii=False, indent=2) + "\n"
    ZH_PATH.write_text(payload, encoding="utf-8")
    print("keys changed", changed)
    for h, n in sorted(hits.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {h}")

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
