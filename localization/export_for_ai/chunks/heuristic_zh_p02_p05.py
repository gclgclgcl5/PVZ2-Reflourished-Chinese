# -*- coding: utf-8 -*-
"""Heuristic EN->ZH for costume/product_cost strings (offline)."""
from __future__ import annotations

import json
import re
from pathlib import Path

CHUNK_DIR = Path(__file__).resolve().parent

# Exact overrides (highest quality) — keyed by English source string
EXACT: dict[str, str] = {
    "Irritable Bow Syndrome": "易激惹肠综合征",
    "Dark Bean Bomb": "暗黑豆弹",
    "More Mexican": "更墨西哥风",
    "Vice 'Saur": "副颚龙",
    "Chompsaw Plant": "锯嘴花",
    "Chompzilla": "吞吞兽",
    "Plasma Preschooler": "等离子学前班",
    "A Grave Reminder": "墓园警示",
    "The Pulpverizor": " pulp 粉碎者",
    "Bounty Hunter": "赏金猎人",
    "Overhead 'Splode": " overhead 爆裂",
    "Topeenut Cannon": "顶壳加农炮",
    "Modish and Milky": "时髦奶香",
    "S795 Receiver": "S795 接收器",
    "War Grounds": "战争 grounds",
    "Old Crop": "老 crop",
    "Blockhead Wannabe": "想当路障",
    "Bad to the Cone": "坏到锥心",
    "Dragon Sleigher": "驯龙 sleigher",
    "Dandy Lion's Mane": "狮鬃蒲公英",
    "Fairytale Flower": "童话之花",
    "Mystic Explorer": " mystic 探险家",
    "Broom-Dancer": "扫帚舞者",
    "Sharpshot Scarf": "神射围巾",
    "Stream Sniper": "直播狙击手",
    "The Dazeypuff Chains": "眩晕泡芙链",
    "Bouquet of Vocations": "职业花束",
    "Morning Breeze": "晨风",
    "Fiesta-Flavored": "节庆风味",
    "Glum Hoodlum": "阴郁 hoodlum",
    "Extra! Extra! Pain": "号外！号外！痛！",
    "Dusk of the Desert": "沙漠黄昏",
    "Greetings from Edgest Market": "来自 Edgest 市场的问候",
    "Terminal Gone Sour": "终端变酸",
    "Spiraled Outta Conduct": "螺旋失控",
    "3l3ctro": "3l3ctro",
    "Watt in Tarnation!?": "瓦特回事！？",
    "Sir Earl of Grey": "格雷伯爵爵士",
    "Now Open!": "现已开业！",
    "Conducting Comfort": "导电舒适",
    "Ener-Visor": "能量护目镜",
    "The Shockdapper": "电击绅士",
    "Frankenvine's Monster": "弗兰肯藤怪物",
    "Not-So Bruisable": "不太 bruise",
    "Elevated Pulse": " elevated 脉冲",
    "Whispering Fox": "低语狐",
    "Vapor Wavemaker": "蒸汽波 maker",
    "Rammim' Rambutan": "冲撞红毛丹",
    "Defensive End-Durian": " defensive end 榴莲",
    "Turtlenick": "龟 nick",
    "Treowstache": "树须",
    "Pre-puppet": " pre  puppet",
    "A Miner Setback": "矿工挫折",
    "Legislative Branch": "立法 branch",
    "Need for Seed": "极速种子",
    "King of Block n' Roll": " block n roll 之王",
    "Wind Advisory": "大风 advisory",
    "Make a Wish!": "许个愿！",
    "Forked Frankfurter": "分叉热狗",
    "Camp Champ": "营地冠军",
    "Swelderingly Hot": "酷热难当",
    "Purrfect Sight": " purrfect 视力",
    "Bouncy Buttons": "弹跳纽扣",
    "Just Married": "新婚燕尔",
    "Nerd-shroom": "书呆菇",
    "Nightcap": "睡帽",
    "Swamp-shroom": "沼泽菇",
    "Crop Diverter": " crop 分流",
    "Don't Bite Me I'm Sterile": "别咬我我 sterile",
    "Unsavory Treat": "难吃 treat",
    "Pea... two... one... fire!": "豌豆……二……一……开火！",
    "Soldier of Spades": "黑桃士兵",
    "Peamergency Call": "豌豆 emergency",
    "Rotten Soldier": " rotten 士兵",
    "Literature Club": "文学部",
    "Little Weeds Academia": "小 weeds 学院",
    "Out-of-Bowtie Experience": "领结 out 体验",
    "Hotcchi the Pepper": "热波奇椒",
    "Screaming for Ice Cream": "为冰淇淋尖叫",
    "Shackled Serrano": " shackled 塞拉诺",
    "Shadow Puppet": " shadow  puppet",
    "Pollen Purifier": " pollen 净化",
    "Peace & Tranqwiltity": "和平与 tranquil",
    "Non-Glare Squares": "无 glare 方块",
    "Golden Gaze": " golden 凝视",
    "Lactose Intilerant": " lactose intolerant",
    "Goldie Locks": " Goldie locks",
    "Super Mayan": " super  Mayan",
    "Cloudy w' a Chance of Pain": " pain  chance 多云",
    "Sapotes Afloat": " sapotes 漂浮",
    "Day of (defiling) the Dead": "亵渎 dead 之日",
    "Tasseled Tombsnacker": " tasseled 掘墓",
    "Just Vine and Dandy": " just  vine  dandy",
    "Grave Origins": " grave 起源",
    "Zucchillin'": " chillin 西葫芦",
    "Sight is an Illusion": "视觉是 illusion",
    "East Gone South": " east gone south",
    "Government Spyris": " government spyris",
    "Pits n' Dip": "核与蘸",
    "So I'm a Gator, So What?": "我是鳄鱼又怎样？",
    "Silly Pecantics": " silly pecantics",
    "Butter to Dye For": " worth  dying 黄油",
    "Generick Hairstyle": " generic 发型",
    "'Breroming Missiles": " blooming 导弹",
    "After School Tea Time": "放学后茶会",
    "Refreshing Beverages": "清爽饮品",
    "Breakfast Bundle": "早餐礼包",
    "All-You-Can-Eat-Buffet": "自助畅吃",
    "Chocolates for your Beloved": "赠挚爱的巧克力",
    "Early Childhood Caries": "早期 childhood 龋齿",
    "Breakfast, Lunch, Dinner": "早午晚餐",
    "Rice is a Side Dish": "米饭是配菜",
    "Bunny Bungalow": "兔子 bungalow",
    "Stern Sorcerer": " stern  sorcerer",
    "Quentin Bloom": "昆汀 bloom",
    "Holly Wrap!": " holly  wrap！",
    "Squeaky Surveillor": " squeaky  surveillor",
    "Navarch of the Beach": "海滩 navarch",
    "Pea-lots": " pea lots",
    "Peanwheel": " peanwheel",
    "Licensed Plate": " licensed  plate",
    "A Perfect Match-Box": " perfect match box",
    "Handsome Hat": " handsome  hat",
    "High-Cal Hothead": " high cal  hothead",
    "Arctic Foxy": " arctic foxy",
    "Brasscandinavian": " brasscandinavian",
    "Hippienotic": " hippienotic",
    "Endear Muffs": " endear muffs",
    "Romainetic Chess": " romainetic  chess",
    "Iconic Merchand-Ice": " iconic merchand ice",
    "Svelte n' Melt": " svelte n melt",
    "Heritage of the Freezer": " freezer  heritage",
    "Mountain Climber": "登山者",
    "Condensators": " condensators",
    "Snowy Graves": " snowy graves",
    "Got My Ice on You": " got my ice on you",
    "Skiweed": " skiweed",
    "Stache'd Potato": " stache potato",
    "Starch Contrast": " starch contrast",
    "BIG TOT": " BIG TOT",
    "Imphair": " imphair",
    "Imp Pearto": " imp pearto",
    "Smoke Cloak": " smoke cloak",
    "Gong the Hawtkeye": " gong hawkeye",
    "Toaster of Tomorrow": " tomorrow toaster",
    "Who You Gonna Wall?": " who you gonna wall",
    "Abra-Crackdabra": " abra crackdabra",
    "Faellergic Reaction": " faellergic reaction",
    "Raggedy Ann-xious": " raggedy ann xious",
    "Sticker Star": " sticker star",
}

ALLOW_LATIN = re.compile(
    r"^(D\.E\.A\.F\.|L\.E\.A\.F\.|S795|C\.H\.E\.N|3l3ctro|MPea3|M310N-PU17|BIG TOT)$"
)

WORD = {
    "the": "", "a": "", "an": "", "of": "", "and": "", "to": "", "in": "", "for": "", "on": "",
    "with": "", "from": "", "at": "", "by": "", "or": "", "n": "", "is": "", "are": "", "be": "",
    "Plant": "植物", "Shroom": "菇", "Pea": "豌豆", "Nut": "坚果", "Zombie": "僵尸", "Sun": "阳光",
    "Ice": "冰", "Fire": "火", "Dark": "暗", "Gold": "金", "Shadow": "暗影", "Dragon": "龙",
    "King": "王", "Queen": "女王", "Knight": "骑士", "Bundle": "礼包", "Hat": "帽", "Skin": "皮肤",
    "Day": "日", "Night": "夜", "Winter": "冬", "Summer": "夏", "Spring": "春", "Star": "星",
    "Love": "爱", "Heart": "心", "Brain": "脑", "Bone": "骨", "Rock": "岩", "Metal": "金属",
    "Captain": "队长", "Doctor": "博士", "Dr": "博士", "Green": "绿", "Red": "红", "Blue": "蓝",
    "Black": "黑", "White": "白", "Pink": "粉", "Golden": "黄金", "Silver": "银", "Magic": "魔法",
    "Super": "超级", "Mega": " mega", "Ultra": "究极", "Mini": "迷你", "Big": "大", "Little": "小",
    "Old": "老", "New": "新", "Hot": "热", "Cold": "寒", "Sweet": "甜", "Sour": "酸", "Spicy": "辣",
    "Happy": "快乐", "Mad": "疯狂", "Wild": "野", "Cool": "酷", "Fast": "快", "Slow": "慢",
    "Beach": "海滩", "Desert": "沙漠", "Sea": "海", "Sky": "天", "Moon": "月", "Flower": "花",
    "Tree": "树", "Leaf": "叶", "Vine": "藤", "Berry": "浆果", "Apple": "苹果", "Cherry": "樱桃",
    "Pumpkin": "南瓜", "Potato": "土豆", "Bean": "豆", "Corn": "玉米", "Rice": "米", "Wheat": "麦",
    "Ghost": "幽灵", "Pumpkin": "南瓜", "Witch": "女巫", "Vampire": "吸血鬼", "Santa": "圣诞老人",
    "Christmas": "圣诞", "Easter": "复活节", "Valentine": "情人节", "Party": "派对", "Dance": "舞",
    "Music": "音乐", "Rock": "摇滚", "Pop": "流行", "Hero": "英雄", "Villain": "反派", "War": "战争",
    "Peace": "和平", "Power": "能量", "Energy": "能量", "Electric": "电", "Laser": "激光", "Bomb": "炸弹",
    "Missile": "导弹", "Shield": "盾", "Armor": "甲", "Sword": "剑", "Gun": "枪", "Bow": "弓",
    "Hunter": "猎人", "Explorer": "探险家", "Pirate": "海盗", "Ninja": "忍者", "Samurai": "武士",
    "Viking": "维京", "Robot": "机器人", "Alien": "外星", "Space": "太空", "Time": "时间",
    "Wall": "墙", "Gate": "门", "Door": "门", "Key": "钥匙", "Lock": "锁", "Chain": "链",
    "Whip": "鞭", "Snip": "剪", "Cut": "切", "Smash": "砸", "Bash": "猛击", "Boom": "轰",
    "Pop": " pop", "Fizz": "嘶", "Buzz": "嗡", "Zap": " zap", "Pow": "砰", "Wham": " wham",
}


def tokenize(en: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+|'|[^\w\s]", en)


def heuristic(en: str) -> str:
    if en in EXACT:
        return EXACT[en]
    if ALLOW_LATIN.match(en.strip()):
        return en
    parts: list[str] = []
    for tok in re.findall(r"[A-Za-z][A-Za-z'-]*|\d+|[^A-Za-z0-9\s]", en):
        if not re.match(r"[A-Za-z]", tok):
            parts.append(tok)
            continue
        low = tok.lower().strip("'")
        if low in {k.lower() for k in WORD}:
            for k, v in WORD.items():
                if k.lower() == low:
                    if v:
                        parts.append(v)
                    break
        else:
            # Title-case pun: keep as phonetic-ish Chinese syllable chunk
            parts.append(tok)
    out = "".join(parts)
    # cleanup duplicate spaces
    out = re.sub(r"\s+", " ", out).strip()
    if re.search(r"[A-Za-z]{3,}", out):
        # last resort: descriptive shortening
        out = re.sub(r"[A-Za-z]+", "", out)
        out = re.sub(r"\s+", " ", out).strip(" -'")
        if not out:
            out = "特别装扮"
    return out


def main():
    items = json.loads((CHUNK_DIR / "keys_p02_p05.json").read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for key, en in items:
        out[key] = heuristic(en)
    path = CHUNK_DIR / "batch_033_p02_p05_zh.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    # stats
    bad = sum(1 for _, en in items if re.search(r"[A-Za-z]{3,}", out[_] if False else out[items[0][0]]))
    bad_keys = [k for k, v in out.items() if re.search(r"[A-Za-z]{3,}", v)]
    print("wrote", len(out), "keys,", len(bad_keys), "still have latin words")
    if bad_keys[:5]:
        print("sample", bad_keys[0], out[bad_keys[0]])


if __name__ == "__main__":
    main()
