# -*- coding: utf-8 -*-
"""Build _batch033_rest.py from embedded translation tables."""
from __future__ import annotations

import json
from pathlib import Path

CHUNK_DIR = Path(__file__).resolve().parent

P02 = {
    "product_cost_chilibean_custom3_name": "易激惹肠综合征",
    "product_cost_chilibean_skin_darkbeanbomb_name": "暗黑豆弹",
    "product_cost_chilibean_skin_superchilibean_name": "更墨西哥风",
    "product_cost_chomper_custom1_name": "副颚龙",
    "product_cost_chomper_skin_chompsaw_name": "锯嘴花",
    "product_cost_chomper_skin_chompzilla_name": "吞吞兽",
    "product_cost_citron_custom1_name": "等离子学前班",
    "product_cost_citron_custom2_name": "墓园警示",
    "product_cost_citron_custom3_name": " pulp 粉碎者",
    "product_cost_citron_skin_heroes_name": "赏金猎人",
    "product_cost_coconut_custom1_name": " overhead 爆裂",
    "product_cost_coconut_custom2_name": "顶壳加农炮",
    "product_cost_coconut_custom3_name": "时髦奶香",
    "product_cost_coffeebean_custom1_name": "S795 接收器",
    "product_cost_coffeebean_custom2_name": "战争 grounds",
    "product_cost_coffeebean_skin_pvz1_name": "老 crop",
    "product_cost_coldsnap_custom1_name": "想当路障",
    "product_cost_coldsnap_custom2_name": "坏到锥心",
    "product_cost_coldsnap_skin_rudolph_name": "驯龙 sleigher",
    "product_cost_dandelion_custom1_name": "狮鬃蒲公英",
    "product_cost_dandelion_custom2_name": "童话之花",
    "product_cost_dandelion_skin_snarkel_name": " mystic 探险家",
    "product_cost_dartichoke_amanda_name": "扫帚舞者",
    "product_cost_dartichoke_custom1_name": "神射围巾",
    "product_cost_dartichoke_ninja_name": "直播狙击手",
    "product_cost_dazeychain_skin_dazeypuff_name": "眩晕泡芙链",
    "product_cost_dazeychain_skin_steam_name": "职业花束",
    "product_cost_draftodil_custom1_name": "晨风",
    "product_cost_draftodil_skin_fiesta_name": "节庆风味",
    "product_cost_dusklobber_custom1_name": "阴郁 hoodlum",
    "product_cost_dusklobber_custom2_name": "号外！号外！痛！",
    "product_cost_dusklobber_skin_desert_name": "沙漠黄昏",
    "product_cost_edgest_bundle_name": "来自 Edgest 市场的问候",
    "product_cost_electriccurrant_custom1_name": "终端变酸",
    "product_cost_electriccurrant_custom2_name": "螺旋失控",
    "product_cost_electriccurrant_skin_3l3ctro_name": "3l3ctro",
    "product_cost_electricitea_custom1_name": "瓦特回事！？",
    "product_cost_electricitea_skin_steam_name": "格雷伯爵爵士",
    "product_cost_electricpea_custom1_name": "现已开业！",
    "product_cost_electricpea_custom2_name": "导电舒适",
    "product_cost_electricpea_custom3_name": "能量护目镜",
    "product_cost_electricpea_skin_shockdapper_name": "电击绅士",
    "product_cost_empea_custom1_name": "弗兰肯藤怪物",
    "product_cost_empea_custom2_name": "不太 bruise",
    "product_cost_empea_custom3_name": " elevated 脉冲",
    "product_cost_empea_custom4_name": "低语狐",
    "product_cost_empea_skin_steam_name": "蒸汽波 maker",
    "product_cost_endurian_custom1_name": "冲撞红毛丹",
    "product_cost_endurian_custom2_name": " defensive end 榴莲",
    "product_cost_endurian_skin_turtleneck_name": "龟 nick",
    "product_cost_ents_custom1_name": "树须",
    "product_cost_ents_custom2_name": " pre  puppet",
    "product_cost_escaperoot_custom1_name": "矿工挫折",
    "product_cost_escaperoot_custom2_name": "立法 branch",
    "product_cost_explodeonut_custom1_name": "极速种子",
    "product_cost_explodeonut_skin_blocknroll_name": " block n roll 之王",
    "product_cost_fanilla_297_name": "大风 advisory",
    "product_cost_fanilla_custom2_name": "许个愿！",
    "product_cost_firepea_custom1_name": "分叉热狗",
    "product_cost_firepea_custom2_name": "营地冠军",
    "product_cost_flameweed_custom1_name": "酷热难当",
    "product_cost_frozenpear_custom1_name": " purrfect 视力",
    "product_cost_frozenpear_custom2_name": "弹跳纽扣",
    "product_cost_frozenpear_custom3_name": "新婚燕尔",
    "product_cost_fume_40_name": "书呆菇",
    "product_cost_fumeshroom_custom2_name": "睡帽",
    "product_cost_fumeshroom_skin_gator_name": "沼泽菇",
    "product_cost_garlic_custom1_name": " crop 分流",
    "product_cost_garlic_custom2_name": "别咬我我 sterile",
    "product_cost_garlic_skin_fruitcake_name": "难吃 treat",
    "product_cost_gatlingpea_custom1_name": "豌豆……二……一……开火！",
    "product_cost_gatlingpea_custom2_name": "黑桃士兵",
    "product_cost_gatlingpea_custom3_name": "豌豆 emergency",
    "product_cost_gatlingpea_skin_neko_name": " rotten 士兵",
    "product_cost_gembundles_ddlc_bundle_name": "文学部",
    "product_cost_gembundles_lwa_bundle_name": "小 weeds 学院",
    "product_cost_ghostpepper_custom1_name": "领结 out 体验",
    "product_cost_ghostpepper_skin_bocchi_name": "热波奇椒",
    "product_cost_ghostpepper_skin_icecream_name": "为冰淇淋尖叫",
    "product_cost_ghostpepper_skin_jacob_name": " shackled 塞拉诺",
    "product_cost_ghostpepper_skin_snatcher_name": " shadow  puppet",
    "product_cost_gloomvine_custom1_name": " pollen 净化",
    "product_cost_goldbloom_321_name": "和平与 tranquil",
    "product_cost_goldbloom_custom1_name": "无 glare 方块",
    "product_cost_goldbloom_custom2_name": " golden 凝视",
    "product_cost_goldleaf_custom1_name": " lactose intolerant",
    "product_cost_goldleaf_custom2_name": " Goldie locks",
    "product_cost_goldleaf_custom3_name": " super  Mayan",
    "product_cost_grapeshot_custom1_name": " pain  chance 多云",
    "product_cost_grapeshot_custom2_name": " sapotes 漂浮",
    "product_cost_gravebuster_custom1_name": "亵渎 dead 之日",
    "product_cost_gravebuster_custom2_name": " tasseled 掘墓",
    "product_cost_gravebuster_custom3_name": " just  vine  dandy",
    "product_cost_gravebuster_skin_pvz1_name": " grave 起源",
    "product_cost_greatzucchini_custom1_name": " chillin 西葫芦",
    "product_cost_greatzucchini_custom2_name": "视觉是 illusion",
    "product_cost_grimrose_custom1_name": " east gone south",
    "product_cost_grimrose_custom2_name": " government spyris",
    "product_cost_guacodile_custom1_name": "核与蘸",
    "product_cost_guacodile_skin_feirune_name": "我是鳄鱼又怎样？",
    "product_cost_gumnut_custom1_name": " silly pecantics",
    "product_cost_headbutter_custom1_name": " worth  dying 黄油",
    "product_cost_headbutter_skin_erick_name": " generic 发型",
    "product_cost_heathseeker_custom1_name": " blooming 导弹",
    "product_cost_hf2023_afterschoolteatime_bundle_name": "放学后茶会",
    "product_cost_hf2023_beverages_bundle_name": "清爽饮品",
    "product_cost_hf2023_breakfast_bundle_name": "早餐礼包",
    "product_cost_hf2023_buffet_bundle_name": "自助畅吃",
    "product_cost_hf2023_chocolates_bundle_name": "赠挚爱的巧克力",
    "product_cost_hf2023_earlycaries_bundle_name": "早期 childhood 龋齿",
    "product_cost_hf2023_fulldaysmeal_bundle_name": "早午晚餐",
    "product_cost_hf2023_riceisasidedish_bundle_name": "米饭是配菜",
    "product_cost_hocus_custom1_name": "兔子 bungalow",
    "product_cost_hocus_lwadiana_name": " stern  sorcerer",
    "product_cost_hocus_mysterio_name": "昆汀 bloom",
    "product_cost_hollyknight_custom1_name": " holly  wrap！",
    "product_cost_homingthistle_custom1_name": " squeaky  surveillor",
    "product_cost_homingthistle_skin_navarch_name": "海滩 navarch",
    "product_cost_horsebean_custom1_name": " pea lots",
    "product_cost_horsebean_custom2_name": " peanwheel",
    "product_cost_horsebean_custom3_name": " licensed  plate",
    "product_cost_hotdate_custom1_name": " perfect match box",
    "product_cost_hotdate_skin_handsome_name": " handsome  hat",
    "product_cost_hotpotato_custom1_name": " high cal  hothead",
    "product_cost_hurrikale_custom1_name": " arctic foxy",
    "product_cost_hurrikale_skin_viking_name": " brasscandinavian",
    "product_cost_hypnoshroom_custom1_name": " hippienotic",
    "product_cost_iceberg_custom1_name": " endear muffs",
    "product_cost_iceberg_custom2_name": " romainetic  chess",
    "product_cost_iceberg_custom3_name": " iconic merchand ice",
    "product_cost_iceberg_custom4_name": " svelte n melt",
    "product_cost_iceberg_skin_iceshroom_name": " freezer  heritage",
    "product_cost_icebloom_322_name": "登山者",
    "product_cost_icebloom_custom1_name": " condensators",
    "product_cost_icebloom_skin_noelle_name": " snowy graves",
    "product_cost_iceburg_custom_valentines_name": " got my ice on you",
    "product_cost_iceweed_custom1_name": " skiweed",
    "product_cost_imitater_custom1_name": " stache potato",
    "product_cost_imitater_skin_pvz1_name": " starch contrast",
    "product_cost_imitater_skin_spamton_name": " BIG TOT",
    "product_cost_imppear_custom1_name": " imphair",
    "product_cost_imppear_skin_jaykrow_name": " imp pearto",
    "product_cost_inferno_custom1_name": " smoke cloak",
    "product_cost_inferno_skin_poss_name": " gong hawkeye",
    "product_cost_infinut_custom1_name": " tomorrow toaster",
    "product_cost_infinut_custom2_name": " who you gonna wall",
    "product_cost_infinut_custom3_name": " abra crackdabra",
    "product_cost_inkblot_custom1_name": " faellergic reaction",
    "product_cost_inkblot_custom2_name": " raggedy ann xious",
    "product_cost_inkblot_custom3_name": " sticker star",
}

P03: dict[str, str] = {}
P04: dict[str, str] = {}
P05: dict[str, str] = {}


def load_en(stem: str) -> dict[str, str]:
    return json.loads((CHUNK_DIR / f"{stem}.json").read_text(encoding="utf-8"))


def write_rest_module() -> None:
    tables = {
        "batch_033_p02": P02,
        "batch_033_p03": P03,
        "batch_033_p04": P04,
        "batch_033_p05": P05,
    }
    for stem, table in tables.items():
        src = load_en(stem)
        missing = set(src) - set(table)
        if missing:
            raise SystemExit(f"{stem} missing {len(missing)} translations (e.g. {next(iter(missing))})")
    out = CHUNK_DIR / "_batch033_rest.py"
    with out.open("w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\nT = ")
        json.dump(tables, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {out}")


if __name__ == "__main__":
    write_rest_module()
