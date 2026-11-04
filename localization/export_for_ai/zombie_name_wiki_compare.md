# 僵尸名称对照表（当前汉化 vs 百科译名）

来源：[植物大战僵尸百科 · 译名对照 / 植物大战僵尸2](https://plantsvszombies.wiki.gg/zh/wiki/PvZ_Wiki:%E8%AF%91%E5%90%8D%E5%AF%B9%E7%85%A7/%E6%A4%8D%E7%89%A9%E5%A4%A7%E6%88%98%E5%83%B5%E5%B0%B82)

## 怎么读

| 列 | 含义 |
| --- | --- |
| 百科建议名 | 社区选定「建议使用名」zh-CN（推荐对齐） |
| 中文版名 | 官方中文版游戏名（结构常不同，如「路障未来僵尸」） |
| 当前汉化 | `LawnStrings_zh.json` / `almanac_name_lock.json` |

**统计（按英文名去重后）**：百科可对照 198｜一致 110｜不一致 88｜返茂/百科未收录 353

## 不一致里的高频模式

- **其他译名分歧**（35）：小鬼大炮→小鬼僵尸炮；游乐园大炮→游乐园炮；侏罗纪暴徒僵尸→侏罗纪恶霸僵尸；侏罗纪石击僵尸→侏罗纪岩石拳手僵尸；迪斯科机 3000→迪斯科机3000型；8 位僵尸→8比特僵尸…
- **路障头→路障（百科无「头」）**（17）：蓬巴杜路障头僵尸→飞机头路障僵尸；比基尼路障头僵尸→比基尼路障僵尸；游乐园路障头僵尸→游乐园路障僵尸；路障头牛仔僵尸→路障牛仔僵尸；路障头农民僵尸→路障农民僵尸；侏罗纪路障头僵尸→侏罗纪路障僵尸…
- **铁桶头→铁桶（百科无「头」）**（16）：蓬巴杜铁桶头僵尸→飞机头铁桶僵尸；比基尼铁桶头僵尸→比基尼铁桶僵尸；游乐园铁桶头僵尸→游乐园铁桶僵尸；铁桶头牛仔僵尸→铁桶牛仔僵尸；铁桶头农民僵尸→铁桶农民僵尸；侏罗纪铁桶头僵尸→侏罗纪铁桶僵尸…
- **缺「僵尸」后缀**（11）：单个游乐园小鬼→游乐园分裂小鬼僵尸；游乐园小鬼双子→游乐园双子小鬼僵尸；侏罗纪小鬼→侏罗纪小鬼僵尸；朋克小鬼→小鬼朋克僵尸；机器蛛虫小鬼→机器虫小鬼僵尸；雪人小鬼→雪人小鬼僵尸…
- **××头 赘字**（4）：手摇风琴头僵尸→手摇风琴僵尸；矿车头僵尸→矿车僵尸；侏罗纪化石头僵尸→侏罗纪化石僵尸；琥珀头僵尸→琥珀僵尸
- **蓬巴杜 vs 飞机头**（1）：蓬巴杜僵尸→飞机头僵尸
- **弄臣 vs 小丑**（1）：弄臣僵尸→小丑僵尸
- **电玩城 vs 街机**（1）：电玩城僵尸→街机僵尸
- **擎天 vs 机甲巨人**（1）：擎天巨人僵尸→机甲巨人僵尸
- **仅空格/标点**（1）：Z 机甲→Z机甲

> 建议优先统一：**去掉多余「头」**、**Pompadour=飞机头**、**Gargantuar Prime=机甲巨人僵尸**、**Arcade=街机**；「渔夫」可保留因中文版同名。

## 一、与百科不一致（优先审）

| Key | 英文 | 当前汉化 | 百科建议名 | 中文版名 | 模式 |
| --- | --- | --- | --- | --- | --- |
| `ZOMBIE_BEACH` | Pompadour Zombie | 蓬巴杜僵尸 | 飞机头僵尸 | — | 蓬巴杜 vs 飞机头 |
| `ZOMBIE_BEACH_ARMOR1` | Pompadour Conehead | 蓬巴杜路障头僵尸 | 飞机头路障僵尸 | 路障飞机头僵尸 | 路障头→路障（百科无「头」） |
| `ZOMBIE_BEACH_ARMOR2` | Pompadour Buckethead | 蓬巴杜铁桶头僵尸 | 飞机头铁桶僵尸 | 铁桶飞机头僵尸 | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_BEACH_FEM_ARMOR1` | Bikini Conehead | 比基尼路障头僵尸 | 比基尼路障僵尸 | 路障比基尼僵尸 | 路障头→路障（百科无「头」） |
| `ZOMBIE_BEACH_FEM_ARMOR2` | Bikini Buckethead | 比基尼铁桶头僵尸 | 比基尼铁桶僵尸 | 铁桶比基尼僵尸 | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_CANNON` | Imp Cannon | 小鬼大炮 | 小鬼僵尸炮 | — | 其他译名分歧 |
| `ZOMBIE_CARNIE_ARMOR1` | Carnie Conehead | 游乐园路障头僵尸 | 游乐园路障僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_CARNIE_ARMOR2` | Carnie Buckethead | 游乐园铁桶头僵尸 | 游乐园铁桶僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_CARNIE_ARMOR4` | Grinderhead Zombie | 手摇风琴头僵尸 | 手摇风琴僵尸 | — | ××头 赘字 |
| `ZOMBIE_CARNIE_CANNON` | Carnie Cannon | 游乐园大炮 | 游乐园炮 | — | 其他译名分歧 |
| `ZOMBIE_CARNIE_IMP_SPLIT` | Carnie Imp Split | 单个游乐园小鬼 | 游乐园分裂小鬼僵尸 | — | 缺「僵尸」后缀 |
| `ZOMBIE_CARNIE_IMP_TWINS` | Carnie Imp Twins | 游乐园小鬼双子 | 游乐园双子小鬼僵尸 | — | 缺「僵尸」后缀 |
| `ZOMBIE_COWBOY_ARMOR1` | Conehead Cowboy | 路障头牛仔僵尸 | 路障牛仔僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_COWBOY_ARMOR2` | Buckethead Cowboy | 铁桶头牛仔僵尸 | 铁桶牛仔僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_COWBOY_ARMOR4` | Cart-Head Zombie | 矿车头僵尸 | 矿车僵尸 | — | ××头 赘字 |
| `ZOMBIE_DARK_ARMOR1` | Conehead Peasant | 路障头农民僵尸 | 路障农民僵尸 | 路障农夫僵尸 | 路障头→路障（百科无「头」） |
| `ZOMBIE_DARK_ARMOR2` | Buckethead Peasant | 铁桶头农民僵尸 | 铁桶农民僵尸 | 铁桶农夫僵尸 | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_DARK_JUGGLER` | Jester Zombie | 弄臣僵尸 | 小丑僵尸 | — | 弄臣 vs 小丑 |
| `ZOMBIE_DINO_ARMOR1` | Jurassic Conehead | 侏罗纪路障头僵尸 | 侏罗纪路障僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_DINO_ARMOR2` | Jurassic Buckethead | 侏罗纪铁桶头僵尸 | 侏罗纪铁桶僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_DINO_ARMOR3` | Jurassic Fossilhead | 侏罗纪化石头僵尸 | 侏罗纪化石僵尸 | 侏罗纪龙骨化石僵尸 | ××头 赘字 |
| `ZOMBIE_DINO_ARMOR4` | Amberhead Zombie | 琥珀头僵尸 | 琥珀僵尸 | — | ××头 赘字 |
| `ZOMBIE_DINO_BULLY` | Jurassic Bully | 侏罗纪暴徒僵尸 | 侏罗纪恶霸僵尸 | 侏罗纪野人僵尸 | 其他译名分歧 |
| `ZOMBIE_DINO_BULLY_VETERAN` | Jurassic Rockpuncher | 侏罗纪石击僵尸 | 侏罗纪岩石拳手僵尸 | — | 其他译名分歧 |
| `ZOMBIE_DINO_IMP` | Jurassic Imp | 侏罗纪小鬼 | 侏罗纪小鬼僵尸 | — | 缺「僵尸」后缀 |
| `ZOMBIE_DISCO_MECH` | Disco-tron 3000 | 迪斯科机 3000 | 迪斯科机3000型 | 迪斯科3000 | 其他译名分歧 |
| `ZOMBIE_EIGHTIES_8BIT` | 8-Bit Zombie | 8 位僵尸 | 8比特僵尸 | 8位僵尸 | 其他译名分歧 |
| `ZOMBIE_EIGHTIES_ARCADE` | Arcade Zombie | 电玩城僵尸 | 街机僵尸 | — | 电玩城 vs 街机 |
| `ZOMBIE_EIGHTIES_ARMOR1` | Neon Conehead | 霓虹路障头僵尸 | 霓虹路障僵尸 | 摇滚路障僵尸 | 路障头→路障（百科无「头」） |
| `ZOMBIE_EIGHTIES_ARMOR2` | Neon Buckethead | 霓虹铁桶头僵尸 | 霓虹铁桶僵尸 | 摇滚铁桶僵尸 | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_EIGHTIES_IMP` | Impunk | 朋克小鬼 | 小鬼朋克僵尸 | 摇滚小鬼僵尸 | 缺「僵尸」后缀 |
| `ZOMBIE_FUTURE_ARMOR1` | Future Conehead Zombie | 未来路障头僵尸 | 未来路障僵尸 | 路障未来僵尸 | 路障头→路障（百科无「头」） |
| `ZOMBIE_FUTURE_ARMOR2` | Future Buckethead Zombie | 未来铁桶头僵尸 | 未来铁桶僵尸 | 铁桶未来僵尸 | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_FUTURE_GARGANTUAR` | Gargantuar Prime | 擎天巨人僵尸 | 机甲巨人僵尸 | — | 擎天 vs 机甲巨人 |
| `ZOMBIE_FUTURE_IMP` | Bug Bot Imp | 机器蛛虫小鬼 | 机器虫小鬼僵尸 | — | 缺「僵尸」后缀 |
| `ZOMBIE_FUTURE_JETPACK_VETERAN` | Blastronaut Zombie | 航天员僵尸 | 爆炸宇航员僵尸 | — | 其他译名分歧 |
| `ZOMBIE_GENERAL_ZMECH_PHASE3` | Z-Mech | Z 机甲 | Z机甲 | — | 仅空格/标点 |
| `ZOMBIE_ICEAGE_ARMOR1` | Cave Conehead Zombie | 洞穴路障头僵尸 | 洞穴路障僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_ICEAGE_ARMOR2` | Cave Buckethead Zombie | 洞穴铁桶头僵尸 | 洞穴铁桶僵尸 | 洞穴石桶僵尸 | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_ICEAGE_ARMOR3` | Blockhead Zombie | 冰块头僵尸 | 冰块僵尸 | 冰砖僵尸 | 其他译名分歧 |
| `ZOMBIE_ICEAGE_GARGANTUAR` | Sloth Gargantuar | 树懒巨人僵尸 | 地懒巨人僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ICEAGE_IMP` | Yeti Imp | 雪人小鬼 | 雪人小鬼僵尸 | — | 缺「僵尸」后缀 |
| `ZOMBIE_IMPPEAR_IMP` | Imp Pear Imp | 小鬼梨小鬼 | 小鬼梨小鬼僵尸 | 梨小鬼僵尸 | 缺「僵尸」后缀 |
| `ZOMBIE_LOSTCITY_ARMOR1` | Conehead Adventurer Zombie | 路障头冒险家僵尸 | 路障冒险家僵尸 | 路障失落僵尸 | 路障头→路障（百科无「头」） |
| `ZOMBIE_LOSTCITY_ARMOR2` | Buckethead Adventurer Zombie | 铁桶头冒险家僵尸 | 铁桶冒险家僵尸 | 铁桶失落僵尸 | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_LOSTCITY_BUG` | Bug Zombie | 昆虫僵尸 | 虫子僵尸 | 失落昆虫僵尸 | 其他译名分歧 |
| `ZOMBIE_LOSTCITY_EXCAVATOR` | Excavator Zombie | 发掘者僵尸 | 发掘僵尸 | 失落发掘者僵尸 | 其他译名分歧 |
| `ZOMBIE_LOSTCITY_GARGANTUAR` | Porter Gargantuar | 脚夫巨人僵尸 | 搬运工巨人僵尸 | 失落巨人僵尸 | 其他译名分歧 |
| `ZOMBIE_LOSTCITY_IMPPORTER` | Imp Porter | 小鬼脚夫 | 小鬼搬运工僵尸 | 失落小鬼搬运工僵尸 | 缺「僵尸」后缀 |
| `ZOMBIE_LOST_ARMOR1` | Conehead Adventurer | 路障头冒险家僵尸 | 路障冒险家僵尸 | 路障失落僵尸 | 路障头→路障（百科无「头」） |
| `ZOMBIE_MODERN_SUPERFANIMP` | Super-Fan Imp | 超球迷小鬼 | 超级粉丝小鬼僵尸 | 粉丝小鬼僵尸 | 缺「僵尸」后缀 |
| `ZOMBIE_MUMMY_ARMOR1` | Conehead Mummy | 路障头木乃伊僵尸 | 路障木乃伊僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_MUMMY_ARMOR2` | Buckethead Mummy | 铁桶头木乃伊僵尸 | 铁桶木乃伊僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_MUMMY_ARMOR4` | Pyramid-Head Zombie | 金字塔头僵尸 | 金字塔僵尸 | — | 其他译名分歧 |
| `ZOMBIE_PIRATE_ARMOR1` | Conehead Pirate | 路障头海盗僵尸 | 路障海盗僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_PIRATE_ARMOR2` | Buckethead Pirate | 铁桶头海盗僵尸 | 铁桶海盗僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_PIRATE_ARMOR4` | Barrelhead Zombie | 酒桶头僵尸 | 酒桶僵尸 | — | 其他译名分歧 |
| `ZOMBIE_PROSPECTOR` | Prospector Zombie | 勘探者僵尸 | 淘金僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ROMAN_ARMOR1` | Roman Conehead | 罗马路障头僵尸 | 罗马路障僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_ROMAN_ARMOR2` | Roman Buckethead | 罗马铁桶头僵尸 | 罗马铁桶僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_ROMAN_ARMOR4` | Bust Head Zombie | 胸像头僵尸 | 半身像僵尸 | 石像僵尸 | 其他译名分歧 |
| `ZOMBIE_ROMAN_IMP` | Roman Imp | 罗马小鬼 | 罗马小鬼僵尸 | — | 缺「僵尸」后缀 |
| `ZOMBIE_TOMB_RAISER` | Tomb Raiser Zombie | 影立古墓僵尸 | 死神僵尸 | — | 其他译名分歧 |
| `ZOMBIE_TUTORIAL_ARMOR1` | Conehead Zombie | 路障头僵尸 | 路障僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_TUTORIAL_ARMOR2` | Buckethead Zombie | 铁桶头僵尸 | 铁桶僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_TUTORIAL_IMP` | Imp | 小鬼 | 小鬼僵尸 | — | 缺「僵尸」后缀 |
| `ZOMBIE_WEST_BULLRIDER` | Zombie Bull Rider | 僵尸牛骑士 | 僵尸牛骑手 | 骑牛小鬼僵尸 | 其他译名分歧 |
| `ZOMBIE_ZCORP` | ZCorp New Hire | 僵企新雇员僵尸 | Z公司新雇员僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ZCORP_ARMOR1` | ZCorp Conehead | 僵企路障头僵尸 | Z公司路障僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_ZCORP_ARMOR2` | ZCorp Buckethead | 僵企铁桶头僵尸 | Z公司铁桶僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_ZCORP_CONSULTANT` | ZCorp Consultant | 僵企顾问僵尸 | Z公司顾问僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ZCORP_FEM` | ZCorp Contractor | 僵企合同工僵尸 | Z公司合同工僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ZCORP_FEM_ARMOR1` | ZCorp Contractor Conehead | 僵企合同工路障头僵尸 | Z公司合同工路障僵尸 | — | 路障头→路障（百科无「头」） |
| `ZOMBIE_ZCORP_FEM_ARMOR2` | ZCorp Contractor Buckethead | 僵企合同工铁桶头僵尸 | Z公司合同工铁桶僵尸 | — | 铁桶头→铁桶（百科无「头」） |
| `ZOMBIE_ZCORP_FLAG` | ZCorp Flag Zombie | 僵企旗帜僵尸 | Z公司旗帜僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ZCORP_HELPDESK` | ZCorp HelpDesk | 僵企技术支持僵尸 | Z公司技术支持僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ZCORP_RACER_CHAIR` | ZCorp Chair Racer | 僵企转椅竞速僵尸 | Z公司转椅竞速僵尸 | — | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_BEACH` | Zombot Sharktronic Sub | 潜袭鲨机僵尸机器人 | 僵尸机器人鲨机潜艇 | 沙滩僵尸博士 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_CIRCUS` | Zombot Catastro-liope | 悲乐风琴僵尸机器人 | 僵尸机器人汽笛风琴灾厄 | — | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_COWBOY` | Zombot War Wagon | 兵戈牛车僵尸机器人 | 僵尸机器人战争牛车 | 西部僵尸博士 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_DARK` | Zombot Dark Dragon | 黑暗之龙僵尸机器人 | 僵尸机器人黑暗龙 | 黑暗机械龙 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_DINO` | Zombot Dinotronic Mechasaur | 恐惧机龙僵尸机器人 | 僵尸机器人恐电机龙 | 恐龙机械僵尸 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_EGYPT` | Zombot Sphinx-inator | 狮身终结者僵尸机器人 | 僵尸机器人狮身人面像终结者 | 埃及僵尸博士 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_EIGHTIES` | Zombot Multi-stage Masher | 狂舞碎灭者僵尸机器人 | 僵尸机器人多重舞台粉碎者 | 摇滚僵尸博士 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_FUTURE` | Zombot Tomorrow-tron | 明日破译者僵尸机器人 | 僵尸机器人明日机 | 未来僵尸博士 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_ICEAGE` | Zombot Tuskmaster 10,000 BC | 獠牙驯服者 10000 BC 僵尸机器人 | 僵尸机器人前10000年象牙主宰 | 獠牙征服者 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_LOSTCITY` | Zombot Aerostatic Gondola | 飞艇浮船僵尸机器人 | 僵尸机器人航空吊篮 | 飞艇僵尸博士 | 其他译名分歧 |
| `ZOMBIE_ZOMBOSSMECH_PIRATE` | Zombot Plank Walker | 甲板踏行者僵尸机器人 | 僵尸机器人跳板行走者 | 海盗僵尸博士 | 其他译名分歧 |

## 二、与百科一致

| Key | 英文 | 当前汉化 | 百科建议名 | 中文版名 |
| --- | --- | --- | --- | --- |
| `ZOMBIE_BARRELROLLER` | Barrel Roller Zombie | 滚桶僵尸 | 滚桶僵尸 | — |
| `ZOMBIE_BEACH_FEM` | Bikini Zombie | 比基尼僵尸 | 比基尼僵尸 | — |
| `ZOMBIE_BEACH_FISHERMAN` | Fisherman Zombie | 渔夫僵尸 | 钓鱼僵尸 | 渔夫僵尸 |
| `ZOMBIE_BEACH_FLAG` | Beach Flag Zombie | 海滩旗帜僵尸 | 海滩旗帜僵尸 | 沙滩旗子僵尸 |
| `ZOMBIE_BEACH_GARGANTUAR` | Deep Sea Gargantuar | 深海巨人僵尸 | 深海巨人僵尸 | — |
| `ZOMBIE_BEACH_IMP` | Imp Mermaid Zombie | 小鬼人鱼僵尸 | 小鬼人鱼僵尸 | 美人鱼小鬼僵尸 |
| `ZOMBIE_BEACH_OCTOPUS` | Octo Zombie | 章鱼僵尸 | 章鱼僵尸 | — |
| `ZOMBIE_BEACH_SNORKEL` | Snorkel Zombie | 潜水僵尸 | 潜水僵尸 | 浮潜僵尸 |
| `ZOMBIE_BEACH_SURFER` | Surfer Zombie | 冲浪僵尸 | 冲浪僵尸 | — |
| `ZOMBIE_BIRTHDAY_CAKETANK` | #caketank | #蛋糕坦克 | #蛋糕坦克 | — |
| `ZOMBIE_CARNIE` | Carnie Zombie | 游乐园僵尸 | 游乐园僵尸 | — |
| `ZOMBIE_CARNIE_FIREBREATHER` | Firebreather Zombie | 喷火僵尸 | 喷火僵尸 | — |
| `ZOMBIE_CARNIE_FLAG` | Carnie Flag Zombie | 游乐园旗帜僵尸 | 游乐园旗帜僵尸 | — |
| `ZOMBIE_CARNIE_GARGANTUAR` | Strongman Gargantuar | 大力士巨人僵尸 | 大力士巨人僵尸 | — |
| `ZOMBIE_CARNIE_MAGICIAN` | Magician Zombie | 魔术师僵尸 | 魔术师僵尸 | — |
| `ZOMBIE_CARNIE_STILTWALKER` | Stiltwalker Zombie | 高跷僵尸 | 高跷僵尸 | — |
| `ZOMBIE_CHICKEN` | Zombie Chicken | 僵尸鸡 | 僵尸鸡 | — |
| `ZOMBIE_CHICKEN_FARMER` | Chicken Wrangler Zombie | 牧鸡僵尸 | 牧鸡僵尸 | 鸡贼僵尸 |
| `ZOMBIE_COWBOY` | Cowboy Zombie | 牛仔僵尸 | 牛仔僵尸 | — |
| `ZOMBIE_COWBOY_FLAG` | Flag Cowboy Zombie | 旗帜牛仔僵尸 | 旗帜牛仔僵尸 | 旗子牛仔僵尸 |
| `ZOMBIE_COWBOY_FLAG_VETERAN` | Cowboy Rally Zombie | 牛仔集结僵尸 | 牛仔集结僵尸 | — |
| `ZOMBIE_COWBOY_GARGANTUAR` | Wild West Gargantuar | 狂野西部巨人僵尸 | 狂野西部巨人僵尸 | 西部巨人僵尸 |
| `ZOMBIE_DARK` | Peasant Zombie | 农民僵尸 | 农民僵尸 | 农夫僵尸 |
| `ZOMBIE_DARK_ARMOR3` | Knight Zombie | 骑士僵尸 | 骑士僵尸 | — |
| `ZOMBIE_DARK_FLAG` | Peasant Flag Zombie | 农民旗帜僵尸 | 农民旗帜僵尸 | 黑暗旗子僵尸 |
| `ZOMBIE_DARK_GARGANTUAR` | Dark Ages Gargantuar | 黑暗时代巨人僵尸 | 黑暗时代巨人僵尸 | 黑暗巨人僵尸 |
| `ZOMBIE_DARK_IMP` | Imp Monk Zombie | 小鬼僧侣僵尸 | 小鬼僧侣僵尸 | 僧侣小鬼僵尸 |
| `ZOMBIE_DARK_IMP_DRAGON` | Imp Dragon Zombie | 小鬼龙僵尸 | 小鬼龙僵尸 | 恶龙小鬼僵尸 |
| `ZOMBIE_DARK_KING` | Zombie King | 僵尸国王 | 僵尸国王 | 国王僵尸 |
| `ZOMBIE_DARK_WIZARD` | Wizard Zombie | 巫师僵尸 | 巫师僵尸 | 魔法师僵尸 |
| `ZOMBIE_DINO` | Jurassic Zombie | 侏罗纪僵尸 | 侏罗纪僵尸 | 侏罗纪普通僵尸 |
| `ZOMBIE_DINO_FLAG` | Jurassic Flag Zombie | 侏罗纪旗帜僵尸 | 侏罗纪旗帜僵尸 | 侏罗纪旗子僵尸 |
| `ZOMBIE_DINO_FLAG_VETERAN` | Jurassic Rally Zombie | 侏罗纪集结僵尸 | 侏罗纪集结僵尸 | — |
| `ZOMBIE_DINO_GARGANTUAR` | Jurassic Gargantuar | 侏罗纪巨人僵尸 | 侏罗纪巨人僵尸 | — |
| `ZOMBIE_DUCKYTUBE` | Ducky Tube Zombie | 鸭子救生圈僵尸 | 鸭子救生圈僵尸 | — |
| `ZOMBIE_EGYPT_GARGANTUAR` | Mummified Gargantuar | 木乃伊巨人僵尸 | 木乃伊巨人僵尸 | 埃及巨人僵尸 |
| `ZOMBIE_EGYPT_IMP` | Imp Mummy | 小鬼木乃伊僵尸 | 小鬼木乃伊僵尸 | 埃及小鬼僵尸 |
| `ZOMBIE_EIGHTIES` | Neon Zombie | 霓虹僵尸 | 霓虹僵尸 | 摇滚僵尸 |
| `ZOMBIE_EIGHTIES_BOOMBOX` | Boombox Zombie | 音响僵尸 | 音响僵尸 | 录音机僵尸 |
| `ZOMBIE_EIGHTIES_BREAKDANCER` | Breakdancer Zombie | 霹雳舞僵尸 | 霹雳舞僵尸 | — |
| `ZOMBIE_EIGHTIES_FLAG` | Neon Flag Zombie | 霓虹旗帜僵尸 | 霓虹旗帜僵尸 | 摇滚旗子僵尸 |
| `ZOMBIE_EIGHTIES_GARGANTUAR` | Hair Metal Gargantuar | 重金属巨人僵尸 | 重金属巨人僵尸 | — |
| `ZOMBIE_EIGHTIES_GLITTER` | Glitter Zombie | 闪光僵尸 | 闪光僵尸 | 闪动僵尸 |
| `ZOMBIE_EIGHTIES_MC` | MC Zom-B | 饶舌僵尸 | 饶舌僵尸 | 说唱僵尸 |
| `ZOMBIE_EIGHTIES_PUNK` | Punk Zombie | 朋克僵尸 | 朋克僵尸 | — |
| `ZOMBIE_EXPLORER` | Explorer Zombie | 探险家僵尸 | 探险家僵尸 | — |
| `ZOMBIE_EXPLORER_VETERAN` | Torchlight Zombie | 火光僵尸 | 火光僵尸 | — |
| `ZOMBIE_FOOTBALL_MECH` | Mecha-Football Zombie | 机甲橄榄球僵尸 | 机甲橄榄球僵尸 | — |
| `ZOMBIE_FUTURE` | Future Zombie | 未来僵尸 | 未来僵尸 | — |
| `ZOMBIE_FUTURE_ARMOR4` | Holo Head Zombie | 全息头僵尸 | 全息头僵尸 | — |
| `ZOMBIE_FUTURE_FLAG` | Future Flag Zombie | 未来旗帜僵尸 | 未来旗帜僵尸 | 旗帜未来僵尸 |
| `ZOMBIE_FUTURE_FLAG_VETERAN` | Robo-Rally Zombie | 机器集结僵尸 | 机器集结僵尸 | — |
| `ZOMBIE_FUTURE_JETPACK` | Jetpack Zombie | 喷射器僵尸 | 喷射器僵尸 | — |
| `ZOMBIE_FUTURE_JETPACK_DISCO` | Disco Jetpack Zombie | 迪斯科喷射器僵尸 | 迪斯科喷射器僵尸 | 喷射器舞者 |
| `ZOMBIE_FUTURE_PROTECTOR` | Shield Zombie | 屏障僵尸 | 屏障僵尸 | 电磁盾僵尸 |
| `ZOMBIE_GENERAL_CAESAR_PHASE3` | Roman Caesar Zombie | 罗马凯撒僵尸 | 罗马凯撒僵尸 | 凯撒僵尸 |
| `ZOMBIE_ICEAGE` | Cave Zombie | 洞穴僵尸 | 洞穴僵尸 | — |
| `ZOMBIE_ICEAGE_DODO` | Dodo Rider Zombie | 渡渡鸟骑手僵尸 | 渡渡鸟骑手僵尸 | 渡渡鸟骑士僵尸 |
| `ZOMBIE_ICEAGE_FLAG` | Cave Flag Zombie | 洞穴旗帜僵尸 | 洞穴旗帜僵尸 | 旗子洞穴僵尸 |
| `ZOMBIE_ICEAGE_HUNTER` | Hunter Zombie | 猎人僵尸 | 猎人僵尸 | — |
| `ZOMBIE_ICEAGE_TROGLOBITE` | Troglobite | 穴居僵尸 | 穴居僵尸 | — |
| `ZOMBIE_ICEAGE_WEASEL` | Ice Weasel | 冰鼬 | 冰鼬 | — |
| `ZOMBIE_ICEAGE_WEASELHOARDER` | Weasel Hoarder | 囤鼬僵尸 | 囤鼬僵尸 | 冰鼬僵尸 |
| `ZOMBIE_LOST` | Adventurer Zombie | 冒险家僵尸 | 冒险家僵尸 | 普通失落僵尸 |
| `ZOMBIE_LOSTCITY_CRYSTALSKULL` | Turquoise Skull Zombie | 绿松石头骨僵尸 | 绿松石头骨僵尸 | 失落考古学家 |
| `ZOMBIE_LOSTCITY_FLAG` | Flag Adventurer Zombie | 旗帜冒险家僵尸 | 旗帜冒险家僵尸 | 旗帜失落僵尸 |
| `ZOMBIE_LOSTCITY_IMP` | Lost City Imp Zombie | 失落之城小鬼僵尸 | 失落之城小鬼僵尸 | 失落小鬼僵尸 |
| `ZOMBIE_LOSTCITY_JANE` | Parasol Zombie | 阳伞僵尸 | 阳伞僵尸 | 失落洋伞僵尸 |
| `ZOMBIE_LOSTCITY_LOSTPILOT` | Lost Pilot Zombie | 失落飞行员僵尸 | 失落飞行员僵尸 | — |
| `ZOMBIE_LOSTCITY_RELICHUNTER` | Relic Hunter Zombie | 古物搜寻僵尸 | 古物搜寻僵尸 | 遗迹猎人僵尸 |
| `ZOMBIE_MECH_CONE` | Robo-Cone Zombie | 机器路障僵尸 | 机器路障僵尸 | 机甲路障僵尸 |
| `ZOMBIE_MODERN_ALLSTAR` | All-Star Zombie | 全明星僵尸 | 全明星僵尸 | — |
| `ZOMBIE_MODERN_BALLOON` | Balloon Zombie | 气球僵尸 | 气球僵尸 | — |
| `ZOMBIE_MODERN_NEWSPAPER` | Newspaper Zombie | 报纸僵尸 | 报纸僵尸 | — |
| `ZOMBIE_MUMMY` | Mummy Zombie | 木乃伊僵尸 | 木乃伊僵尸 | — |
| `ZOMBIE_MUMMY_FLAG` | Flag Mummy Zombie | 旗帜木乃伊僵尸 | 旗帜木乃伊僵尸 | 旗子木乃伊僵尸 |
| `ZOMBIE_MUMMY_FLAG_VETERAN` | Egypt Rally Zombie | 埃及集结僵尸 | 埃及集结僵尸 | — |
| `ZOMBIE_NEWSPAPER_VETERAN` | Sunday Edition Zombie | 周日版报纸僵尸 | 周日版报纸僵尸 | 周日版僵尸 |
| `ZOMBIE_PELICAN` | Pelican Zombie | 鹈鹕僵尸 | 鹈鹕僵尸 | — |
| `ZOMBIE_PHARAOH` | Pharaoh Zombie | 法老僵尸 | 法老僵尸 | — |
| `ZOMBIE_PIANO` | Pianist Zombie | 钢琴僵尸 | 钢琴僵尸 | — |
| `ZOMBIE_PIRATE` | Pirate Zombie | 海盗僵尸 | 海盗僵尸 | — |
| `ZOMBIE_PIRATE_CAPTAIN` | Pirate Captain Zombie | 海盗船长僵尸 | 海盗船长僵尸 | — |
| `ZOMBIE_PIRATE_CAPTAIN_PARROT` | Zombie Parrot | 僵尸鹦鹉 | 僵尸鹦鹉 | — |
| `ZOMBIE_PIRATE_FLAG` | Flag Pirate Zombie | 旗帜海盗僵尸 | 旗帜海盗僵尸 | 旗子海盗僵尸 |
| `ZOMBIE_PIRATE_FLAG_VETERAN` | Jolly Roger Zombie | 海盗旗僵尸 | 海盗旗僵尸 | — |
| `ZOMBIE_PIRATE_GARGANTUAR` | Gargantuar Pirate | 巨人海盗僵尸 | 巨人海盗僵尸 | 海盗巨人僵尸 |
| `ZOMBIE_PIRATE_IMP` | Imp Pirate Zombie | 小鬼海盗僵尸 | 小鬼海盗僵尸 | 海盗小鬼僵尸 |
| `ZOMBIE_RA` | Ra Zombie | 太阳神僵尸 | 太阳神僵尸 | — |
| `ZOMBIE_ROMAN` | Roman Zombie | 罗马僵尸 | 罗马僵尸 | — |
| `ZOMBIE_ROMAN_ARMOR3` | Centurion Zombie | 百夫长僵尸 | 百夫长僵尸 | — |
| `ZOMBIE_ROMAN_BALLISTA` | Zcorpion Zombie | 投石机僵尸 | 投石机僵尸 | 罗马攻城车 |
| `ZOMBIE_ROMAN_FLAG` | Roman Flag Zombie | 罗马旗帜僵尸 | 罗马旗帜僵尸 | — |
| `ZOMBIE_ROMAN_GARGANTUAR` | Gladiator Gargantuar | 角斗士巨人僵尸 | 角斗士巨人僵尸 | 罗马巨人僵尸 |
| `ZOMBIE_ROMAN_HEALER` | Healer Zombie | 治疗师僵尸 | 治疗师僵尸 | 治愈者僵尸 |
| `ZOMBIE_ROMAN_MEDUSA` | Zombie Medusa | 僵尸美杜莎 | 僵尸美杜莎 | 美杜莎僵尸 |
| `ZOMBIE_SEAGULL` | Seagull Zombie | 海鸥僵尸 | 海鸥僵尸 | — |
| `ZOMBIE_SWASHBUCKLER` | Swashbuckler Zombie | 剑客僵尸 | 剑客僵尸 | 飞索僵尸 |
| `ZOMBIE_TREASUREYETI` | Treasure Yeti | 宝藏雪人 | 宝藏雪人 | — |
| `ZOMBIE_TUTORIAL` | Basic Zombie | 普通僵尸 | 普通僵尸 | — |
| `ZOMBIE_TUTORIAL_ARMOR4` | Brickhead Zombie | 砖头僵尸 | 砖头僵尸 | — |
| `ZOMBIE_TUTORIAL_FLAG` | Flag Zombie | 旗帜僵尸 | 旗帜僵尸 | 旗子僵尸 |
| `ZOMBIE_TUTORIAL_FLAG_VETERAN` | Rally Zombie | 集结僵尸 | 集结僵尸 | — |
| `ZOMBIE_TUTORIAL_GARGANTUAR` | Gargantuar | 巨人僵尸 | 巨人僵尸 | — |
| `ZOMBIE_UNUSED_64` | Poncho Zombie | 斗篷僵尸 | 斗篷僵尸 | — |
| `ZOMBIE_VASE_GARGANTUAR` | Vase Gargantuar | 花瓶巨人僵尸 | 花瓶巨人僵尸 | 罐子巨人僵尸 |
| `ZOMBIE_WEST_BULL` | Zombie Bull | 僵尸牛 | 僵尸牛 | 机器牛 |
| `ZOMBIE_WEST_BULL_VETERAN` | Rodeo Legend Zombie | 牛仔传奇僵尸 | 牛仔传奇僵尸 | — |
| `ZOMBIE_ZCORP_GARGANTUAR` | Head Office Impgantuar | 总部巨鬼僵尸 | 总部巨鬼僵尸 | — |
| `ZOMBIE_ZCORP_IMP` | Gargimp Legal | 法务部小巨人僵尸 | 法务部小巨人僵尸 | — |

## 三、返茂 / 百科未收录（节选：疑似坏名）

完整未收录列表较长（节日变体、蒸汽时代、暗影等）。下列为明显机翻/音译/残留英文，建议优先改：

| Key | 英文 | 当前汉化 |
| --- | --- | --- |
| `ZOMBIE_BEACH_DUCKYTUBE_ARMOR1` | Pompadour Conehead Ducky Tube | Pompadour Conehead Ducky 管 |
| `ZOMBIE_BEACH_DUCKYTUBE_ARMOR2` | Pompadour Buckethead Ducky Tube | Pompadour Buckethead Ducky 管 |
| `ZOMBIE_BEACH_DUCKYTUBE_ARMOR4` | Pompadour Shellhead Ducky Tube | Pompadour Shellhead Ducky 管 |
| `ZOMBIE_BEACH_FEM_DUCKYTUBE_ARMOR1` | Bikini Conehead Ducky Tube | 比基尼锥头鸭管 |
| `ZOMBIE_BEACH_FEM_DUCKYTUBE_ARMOR2` | Bikini Buckethead Ducky Tube | 比基尼桶头鸭管 |
| `ZOMBIE_BEACH_FEM_DUCKYTUBE_ARMOR4` | Bikini Shellhead Ducky Tube | 比基尼贝壳鸭管 |
| `ZOMBIE_BIRTHDAY_IMP` | Present Imp | 现在小鬼僵尸 |
| `ZOMBIE_CARNIE_TOY_BALL` | Carnie Ball | 卡妮球 |
| `ZOMBIE_CARNIE_TOY_SNIFFER` | Carnie Snorter | 卡妮·斯诺特 |
| `ZOMBIE_CARNIE_TOY_TEDDY` | Carnie Teddy | 卡尼泰迪 |
| `ZOMBIE_CARNIE_TOY_TEETH` | Carnie Nibbler | 卡妮·尼布勒 |
| `ZOMBIE_CHILDREN_GARGANTUAR` | Teddy Beargantuar | 泰迪熊 |
| `ZOMBIE_DUCKYTUBE_ARMOR1` | Conehead Ducky Tube | 锥头鸭管 |
| `ZOMBIE_DUCKYTUBE_ARMOR2` | Buckethead Ducky Tube | 桶头鸭管 |
| `ZOMBIE_DUCKYTUBE_ARMOR4` | Brickhead Ducky Tube | 砖头鸭管 |
| `ZOMBIE_FEASTIVUS_CAKETANK` | #feastivuscaketank | #festivuscaketank |
| `ZOMBIE_FOODFIGHT_GARGANTUAR` | Food Fighter Prime | 美食斗士 Prime |
| `ZOMBIE_FUTURE_PROTECTOR_GENERATOR` | P0rta-Shield MK. II™ | P0rta-Shield MK。 II™ |
| `ZOMBIE_HERO_BASS_BASIC` | HERO Bassloid | HERO 贝斯洛德 |
| `ZOMBIE_RIFT_JANE` | Exca-sol Zombie | Exca-sol 僵尸 |
| `ZOMBIE_SERVANT_BESOM` | Besom Maid Zombie | Besom 女仆僵尸 |
| `ZOMBIE_SKYCITY_PELICAN` | Pelican-1 Aircraft | Pelican-1 飞机 |
| `ZOMBIE_SKYCITY_PROTECTOR` | ZACU Protector Zombie | ZACU 保护者僵尸 |
| `ZOMBIE_STPATRICK_GARGANTUAR` | Slamrock Gargantuar | Slamrock 巨人僵尸 |
| `ZOMBIE_STPATRICK_GLITTER` | Lepreglitter | Lepreglitter |
| `ZOMBIE_ZOMBOSSMECH_BEACH2` | Zombot Sharktronic Sub 2.0 | 僵博机器人 Sharktronic Sub 2.0 |
| `ZOMBIE_ZOMBOSSMECH_EGYPT2` | Zombot Sphinx-inator 2.0 | 僵博机器人 Sphinx-inator 2.0 |
| `ZOMBIE_ZOMBOSSMECH_FUTURE2` | Zombot Tomorrow-tron 2.0 | 僵博机器人明天-tron 2.0 |

## 四、返茂 / 百科未收录（完整）

| Key | 英文 | 当前汉化 |
| --- | --- | --- |
| `ZOMBIE_BEACH_ARMOR4` | Pompadour Shellhead Zombie | 蓬巴杜贝壳僵尸 |
| `ZOMBIE_BEACH_DUCKYTUBE` | Pompadour Ducky Tube Zombie | 蓬巴杜鸭子救生圈僵尸 |
| `ZOMBIE_BEACH_DUCKYTUBE_ARMOR1` | Pompadour Conehead Ducky Tube | Pompadour Conehead Ducky 管 |
| `ZOMBIE_BEACH_DUCKYTUBE_ARMOR2` | Pompadour Buckethead Ducky Tube | Pompadour Buckethead Ducky 管 |
| `ZOMBIE_BEACH_DUCKYTUBE_ARMOR4` | Pompadour Shellhead Ducky Tube | Pompadour Shellhead Ducky 管 |
| `ZOMBIE_BEACH_FEM_ARMOR4` | Bikini Shellhead Zombie | 比基尼贝壳僵尸 |
| `ZOMBIE_BEACH_FEM_DUCKYTUBE` | Bikini Ducky Tube Zombie | 比基尼鸭子救生圈僵尸 |
| `ZOMBIE_BEACH_FEM_DUCKYTUBE_ARMOR1` | Bikini Conehead Ducky Tube | 比基尼锥头鸭管 |
| `ZOMBIE_BEACH_FEM_DUCKYTUBE_ARMOR2` | Bikini Buckethead Ducky Tube | 比基尼桶头鸭管 |
| `ZOMBIE_BEACH_FEM_DUCKYTUBE_ARMOR4` | Bikini Shellhead Ducky Tube | 比基尼贝壳鸭管 |
| `ZOMBIE_BEACH_FLAG_VETERAN` | Beach Rally Zombie | 海滩拉力僵尸 |
| `ZOMBIE_BEACH_GREASER_IMP` | Greaser Imp | 润滑脂小鬼僵尸 |
| `ZOMBIE_BEACH_SHELL` | Shell Zombie | 贝壳僵尸 |
| `ZOMBIE_BEACH_SHELL_SHIELD` | Hardshell Zombie | 硬壳僵尸 |
| `ZOMBIE_BEACH_SNORKEL_VETERAN` | Scuba Zombie | 水肺僵尸 |
| `ZOMBIE_BIGHEAD` | Big Head Zombie | 大头僵尸 |
| `ZOMBIE_BIGHEAD_ALLSTAR` | Big Head All-Star | 大头全明星 |
| `ZOMBIE_BIGHEAD_ARMOR1` | Big Conehead | 大锥头 |
| `ZOMBIE_BIGHEAD_ARMOR2` | Big Buckethead | 大桶头 |
| `ZOMBIE_BIGHEAD_BALLOON` | Big Head Balloon | 大头气球 |
| `ZOMBIE_BIGHEAD_FLAG` | Big Head Flag Zombie | 大头旗帜僵尸 |
| `ZOMBIE_BIGHEAD_GARGANTUAR` | Big Head Gargantuar | 大头巨人僵尸 |
| `ZOMBIE_BIGHEAD_IMP` | Big Head Imp | 大头小鬼僵尸 |
| `ZOMBIE_BIGHEAD_LOSTPILOT` | Big Head Pilot | 大头飞行员 |
| `ZOMBIE_BIGHEAD_NEWSPAPER` | Big Head Newspaper | 大头报 |
| `ZOMBIE_BIGHEAD_SUPERFAN` | Big Head Super-Fan Imp | 大头超级粉丝小鬼 |
| `ZOMBIE_BIRTHDAY` | Birthdayz Zombie | 生日趴僵尸 |
| `ZOMBIE_BIRTHDAY_ARMOR1` | Birthdayz Conehead | 生日趴锥头 |
| `ZOMBIE_BIRTHDAY_ARMOR2` | Birthdayz Buckethead | 生日趴斗头 |
| `ZOMBIE_BIRTHDAY_FLAG` | Birthdayz Flag Zombie | 生日趴旗帜僵尸 |
| `ZOMBIE_BIRTHDAY_GARGANTUAR` | Birthdayz Gargantuar | 生日趴巨人僵尸 |
| `ZOMBIE_BIRTHDAY_IMP` | Present Imp | 现在小鬼僵尸 |
| `ZOMBIE_BIRTHDAY_JETPACK` | Birthdayz Jetpack | 生日趴喷气背包 |
| `ZOMBIE_BIRTHDAY_JUGGLER` | Birthdayz Jester | 生日趴小丑 |
| `ZOMBIE_BIRTHDAY_MECH_CONE` | Robo-Present Zombie | 机器人僵尸 |
| `ZOMBIE_BIRTHDAY_PHARAOH` | Birthdayz Pharaoh | 生日趴法老 |
| `ZOMBIE_BIRTHDAY_TROGLOBITE` | Birthdayz Troglobite | 生日趴穴居僵尸 |
| `ZOMBIE_CARNIE_COTTONCANDY_BLUE` | Blue Vendor Zombie | 蓝色商贩僵尸 |
| `ZOMBIE_CARNIE_COTTONCANDY_PINK` | Pink Vendor Zombie | 粉色商贩僵尸 |
| `ZOMBIE_CARNIE_DOVE` | Zombie Dove | 僵尸鸽子 |
| `ZOMBIE_CARNIE_IMP` | Cannonball Imp | 炮弹小鬼僵尸 |
| `ZOMBIE_CARNIE_MIRROR` | Funhouse Mirror Zombie | 游乐园镜子僵尸 |
| `ZOMBIE_CARNIE_MONKEY` | Mechanical Monkey Zombie | 机械猴僵尸 |
| `ZOMBIE_CARNIE_MUSICBOX` | Music Doll Zombie | 音乐娃娃僵尸 |
| `ZOMBIE_CARNIE_PRANKSTER` | Prankster Zombie | 恶作剧僵尸 |
| `ZOMBIE_CARNIE_TOY_BALL` | Carnie Ball | 卡妮球 |
| `ZOMBIE_CARNIE_TOY_GARGANTUAR` | Action Gargantuar | 行动巨人僵尸 |
| `ZOMBIE_CARNIE_TOY_SNIFFER` | Carnie Snorter | 卡妮·斯诺特 |
| `ZOMBIE_CARNIE_TOY_TEDDY` | Carnie Teddy | 卡尼泰迪 |
| `ZOMBIE_CARNIE_TOY_TEETH` | Carnie Nibbler | 卡妮·尼布勒 |
| `ZOMBIE_CARNIE_TRAPEZE_BLUE` | Trapeze Zombies | 空中飞人僵尸 |
| `ZOMBIE_CHILDRENSDAY_IMP` | Teddy Imp | 泰迪小鬼僵尸 |
| `ZOMBIE_CHILDREN_BALLOON` | Children Balloon | 儿童气球 |
| `ZOMBIE_CHILDREN_BASIC` | Kid Zombie | 小僵尸 |
| `ZOMBIE_CHILDREN_CAPTAIN` | Fishy Imp | 鱼腥味小鬼僵尸 |
| `ZOMBIE_CHILDREN_FLAG` | Kid Flag Zombie | 儿童旗帜僵尸 |
| `ZOMBIE_CHILDREN_FOOTBALL_MECH` | Toy Car Imp | 玩具车小鬼僵尸 |
| `ZOMBIE_CHILDREN_GARGANTUAR` | Teddy Beargantuar | 泰迪熊 |
| `ZOMBIE_CHILDREN_IMP` | Imp Child | 小鬼僵尸儿童 |
| `ZOMBIE_DARK_ARMOR4` | Towerhead Zombie | 塔楼僵尸 |
| `ZOMBIE_DARK_EXPLORER` | Dark Explorer Zombie | 深色探险家僵尸 |
| `ZOMBIE_DARK_FLAG_VETERAN` | Peasant Rally Zombie | 农民集会僵尸 |
| `ZOMBIE_DARK_ROBBER` | Bandit Zombie | 强盗僵尸 |
| `ZOMBIE_DARK_WIZARD_VETERAN` | Dark Summoner Zombie | 黑暗召唤者僵尸 |
| `ZOMBIE_DARK_WIZARD_VETERAN_VANILLA` | Arcane Shepherd Zombie | 奥术牧羊人僵尸 |
| `ZOMBIE_DESIRE_EMPEROR` | Royal Clan Zombie | 王族僵尸 |
| `ZOMBIE_DESIRE_SHIKAISEN` | Shikaisen Zombie | 尸海战僵尸 |
| `ZOMBIE_DINO_BULLY_BLUE` | Jurassic Imposter | 侏罗纪小鬼斯特 |
| `ZOMBIE_DINO_EGGSHELL` | Eggshell Imp | 蛋壳小鬼僵尸 |
| `ZOMBIE_DINO_EGGSTEALER` | Egg Stealer Imp | 偷蛋贼小鬼僵尸 |
| `ZOMBIE_DINO_PTERRY` | Rock Carrier Zombie | 运石僵尸 |
| `ZOMBIE_DUCKYTUBE_ARMOR1` | Conehead Ducky Tube | 锥头鸭管 |
| `ZOMBIE_DUCKYTUBE_ARMOR2` | Buckethead Ducky Tube | 桶头鸭管 |
| `ZOMBIE_DUCKYTUBE_ARMOR4` | Brickhead Ducky Tube | 砖头鸭管 |
| `ZOMBIE_EASTER_TROGLOBITE` | Springening Troglobite | 春天穴居僵尸 |
| `ZOMBIE_EIGHTIES_ARMOR4` | Speakerhead Zombie | 演讲者僵尸 |
| `ZOMBIE_EIGHTIES_BASS_BASIC` | Bassist Zombie | 贝斯手僵尸 |
| `ZOMBIE_EIGHTIES_FLAG_VETERAN` | Neon Rally Zombie | 霓虹拉力僵尸 |
| `ZOMBIE_EIGHTIES_PUNK_VETERAN` | Goth Punk Zombie | 哥特朋克僵尸 |
| `ZOMBIE_FAIRYTALE` | Poker Zombie | 扑克僵尸 |
| `ZOMBIE_FAIRYTALE_ARMOR1` | Poker Conehead | 扑克锥头 |
| `ZOMBIE_FAIRYTALE_ARMOR2` | Poker Buckethead | 扑克桶头 |
| `ZOMBIE_FAIRYTALE_ARMOR3_CAVALRY` | Diamond Knight Zombie | 钻石骑士僵尸 |
| `ZOMBIE_FAIRYTALE_CAVALRY` | Zombie Unicorn | 僵尸独角兽 |
| `ZOMBIE_FAIRYTALE_CHESIRE` | Cheshire Imp | 柴郡小鬼僵尸 |
| `ZOMBIE_FAIRYTALE_FLAG` | Poker Flag Zombie | 扑克旗帜僵尸 |
| `ZOMBIE_FAIRYTALE_FLAG_VETERAN` | Poker Rally Zombie | 扑克拉力赛僵尸 |
| `ZOMBIE_FAIRYTALE_GARGANTUAR` | Guardgantuar | 守卫刚图尔 |
| `ZOMBIE_FAIRYTALE_IMP` | Queen Imp | 女王小鬼僵尸 |
| `ZOMBIE_FAIRYTALE_IMP_ARMOR1` | Strawhead Impig | 稻草头小鬼僵尸ig |
| `ZOMBIE_FAIRYTALE_IMP_ARMOR2` | Buckethead Impig | 桶头小鬼僵尸ig |
| `ZOMBIE_FAIRYTALE_IMP_ARMOR4` | Brickhead Impig | 砖头小鬼僵尸ig |
| `ZOMBIE_FAIRYTALE_IMP_HEARTS` | Card Imp | 卡片小鬼僵尸 |
| `ZOMBIE_FAIRYTALE_IMP_MINIBOSS_PHASE1` | Card Queen Imp | 卡牌女王小鬼僵尸 |
| `ZOMBIE_FAIRYTALE_MIRRORQUEEN` | Mirror Queen Zombie | 镜子女王僵尸 |
| `ZOMBIE_FAIRYTALE_MIRRORQUEEN_VETERAN` | Mirror Queen Regnant Zombie | 镜子女王统治僵尸 |
| `ZOMBIE_FAIRYTALE_WITCH` | Frog Sorceress Zombie | 青蛙女巫僵尸 |
| `ZOMBIE_FAIRYTALE_WOLF` | Big Bad Wolf Zombie | 大灰狼僵尸 |
| `ZOMBIE_FEASTIVUS` | Feastivus Zombie | 盛宴节僵尸 |
| `ZOMBIE_FEASTIVUS_ARMOR1` | Feastivus Conehead | 盛宴节锥头 |
| `ZOMBIE_FEASTIVUS_ARMOR2` | Feastivus Buckethead | 盛宴节斗头 |
| `ZOMBIE_FEASTIVUS_CAKETANK` | #feastivuscaketank | #festivuscaketank |
| `ZOMBIE_FEASTIVUS_FISHERMAN` | Festive Fisherman | 节日渔夫 |
| `ZOMBIE_FEASTIVUS_FLAG` | Feastivus Flag Zombie | 盛宴节旗帜僵尸 |
| `ZOMBIE_FEASTIVUS_GARGANTUAR` | Ugly Sweater Gargantuar | 丑毛衣巨人僵尸 |
| `ZOMBIE_FEASTIVUS_HUNTER` | Snowball Thrower Zombie | 投雪球僵尸 |
| `ZOMBIE_FEASTIVUS_IMP` | Ugly Sweater Imp | 丑毛衣小鬼僵尸 |
| `ZOMBIE_FEASTIVUS_MULTPLICITY` | Zombie Multimplicity | 僵尸多重性 |
| `ZOMBIE_FEASTIVUS_PIANO` | Feastivus Pianist | 盛宴节钢琴家 |
| `ZOMBIE_FEASTIVUS_SWASHBUCKLER` | Regifting Zombie | 转赠僵尸 |
| `ZOMBIE_FOODFIGHT` | Food Fight Zombie | 食物大战僵尸 |
| `ZOMBIE_FOODFIGHT_ARMOR1` | Food Fight Conehead | 食物大战锥头 |
| `ZOMBIE_FOODFIGHT_ARMOR2` | Food Fight Buckethead | 食物大战桶头 |
| `ZOMBIE_FOODFIGHT_CHEFSTER` | Chefster | 切夫斯特 |
| `ZOMBIE_FOODFIGHT_FLAG` | Food Fight Flag Zombie | 食物大战旗帜僵尸 |
| `ZOMBIE_FOODFIGHT_GARGANTUAR` | Food Fighter Prime | 美食斗士 Prime |
| `ZOMBIE_FOODFIGHT_GOBBLER_KING` | Gobbler King Zombie | 贪吃王僵尸 |
| `ZOMBIE_FOODFIGHT_IMP` | Taco Imp | 玉米卷小鬼僵尸 |
| `ZOMBIE_FOODFIGHT_OVERSTUFF` | Overstuffed Zombie | 臃肿的僵尸 |
| `ZOMBIE_FOODFIGHT_PROTECTOR` | Food Blocker Zombie | 食物拦截僵尸 |
| `ZOMBIE_FOODFIGHT_TURKEY` | Zombie Turkey | 僵尸火鸡 |
| `ZOMBIE_FOODFIGHT_TURKEY_BOSS` | Giganturkey | 巨火鸡 |
| `ZOMBIE_FUTURE_PROTECTOR_GENERATOR` | P0rta-Shield MK. II™ | P0rta-Shield MK。 II™ |
| `ZOMBIE_FUTURE_PROTECTOR_VETERAN` | Deflector Zombie | 偏向器僵尸 |
| `ZOMBIE_GALAXY_DODO` | Huge-Gigantacus | 巨大巨塔克斯 |
| `ZOMBIE_GREATZUCCHINI_BASIC` | The Great Zucchini Zombie | 伟大的西葫芦僵尸 |
| `ZOMBIE_GREATZUCCHINI_GARGANTUAR` | Naked Gargantuar | 裸巨人僵尸 |
| `ZOMBIE_HALLOWEEN` | Spooky Scary Zombie | 幽灵恐怖僵尸 |
| `ZOMBIE_HALLOWEEN_ARMOR1` | Spooky Scary Conehead | 怪异可怕的锥头 |
| `ZOMBIE_HALLOWEEN_ARMOR2` | Spooky Scary Buckethead | 幽灵般的可怕桶头 |
| `ZOMBIE_HALLOWEEN_BREAKDANCER` | Haunting Breakdancer | 令人难以忘怀的霹雳舞者 |
| `ZOMBIE_HALLOWEEN_CROW` | Zombie Crow | 僵尸乌鸦 |
| `ZOMBIE_HALLOWEEN_FLAG` | Spooky Flag Zombie | 恐怖旗帜僵尸 |
| `ZOMBIE_HALLOWEEN_GARGANTUAR` | Frankentuar | 弗兰肯图尔 |
| `ZOMBIE_HALLOWEEN_GHOST` | Ghost | 幽灵 |
| `ZOMBIE_HALLOWEEN_IMP` | Bride of Frankentuar | 弗兰肯图尔的新娘 |
| `ZOMBIE_HALLOWEEN_OCTOPUS` | Halloween Octo Zombie | 万圣节章鱼僵尸 |
| `ZOMBIE_HALLOWEEN_RELICHUNTER` | Pumpkin Hunter | 南瓜头头猎人 |
| `ZOMBIE_HALLOWEEN_WITCH` | Zombie Witch | 僵尸女巫 |
| `ZOMBIE_HARVEST` | Harvest Zombie | 收割僵尸 |
| `ZOMBIE_HARVEST_ARMOR1` | Harvest Conehead | 收获锥头 |
| `ZOMBIE_HARVEST_ARMOR2` | Harvest Buckethead | 收获桶头 |
| `ZOMBIE_HARVEST_EGGSHELL` | Cage-Free Eggshell Imp | 散养蛋壳小鬼僵尸 |
| `ZOMBIE_HARVEST_EGGSTEALER` | Harvest Egg Stealer | 丰收蛋偷窃者 |
| `ZOMBIE_HARVEST_FLAG` | Harvest Flag Zombie | 收获旗帜僵尸 |
| `ZOMBIE_HARVEST_GARGANTUAR` | Harvest Gargantuar | 收获巨人僵尸 |
| `ZOMBIE_HARVEST_IMP` | Harvest Imp | 收获小鬼僵尸 |
| `ZOMBIE_HARVEST_OUTHOUSE` | Outhouse Zombie | 屋外僵尸 |
| `ZOMBIE_HARVEST_PITCHFORK` | Pitchfork Zombie | 干草叉僵尸 |
| `ZOMBIE_HARVEST_PTERRY` | Gourd Carrier Zombie | 葫芦娘僵尸 |
| `ZOMBIE_HERO_ARMOR1` | Wannabe Conehead | 想成为路障者 |
| `ZOMBIE_HERO_ARMOR2` | Wannabe Buckethead | 想成为水桶头 |
| `ZOMBIE_HERO_BASS_BASIC` | HERO Bassloid | HERO 贝斯洛德 |
| `ZOMBIE_HERO_CAPTAIN` | Captain Jones | 琼斯船长 |
| `ZOMBIE_HERO_CRYSTALSKULL` | Professor Brainstorm | 教授头脑风暴 |
| `ZOMBIE_HERO_ELECTRICBOOGALOO` | Wannabe Zombie | 想成为僵尸 |
| `ZOMBIE_HERO_FLAG` | Wannabe Flag Zombie | 想要成为旗帜僵尸 |
| `ZOMBIE_HERO_GLITTER` | Stellar Glitter | 星星闪光 |
| `ZOMBIE_HERO_IMPFINITY` | Impfinity Clone | 小鬼僵尸无限克隆 |
| `ZOMBIE_HERO_JETPACK_DISCO` | Electric Boogaloo | 电动布加洛 |
| `ZOMBIE_HERO_MC` | MC DOOM | MC 毁灭战士 |
| `ZOMBIE_HERO_NEPTUNA` | Neptuna Imp | 海王星小鬼僵尸 |
| `ZOMBIE_HERO_REPAIRIMP` | The Brainiac | 大脑 |
| `ZOMBIE_HERO_RUSTBOLT` | Rustbolt | 锈栓 |
| `ZOMBIE_HERO_SMASH` | The Smash | 粉碎 |
| `ZOMBIE_HERO_STILTWALKER` | Steelwalker | 钢行者 |
| `ZOMBIE_HERO_SUPERBRAINZ` | Super Brainz | 超级大脑 |
| `ZOMBIE_HERO_WEASEL` | Zom-Bat | 僵尸蝙蝠 |
| `ZOMBIE_HERO_WEASELHOARDER` | Immorticia | 仙草 |
| `ZOMBIE_HOLIDAY_DRINK` | Holiday Drinks | 节日饮品 |
| `ZOMBIE_HOLIDAY_GARGANTUAR` | Reindeer Gargantuar | 驯鹿巨人僵尸 |
| `ZOMBIE_HOLIDAY_IMP` | Elf Imp | 精灵小鬼僵尸 |
| `ZOMBIE_ICEAGE_ARMOR4` | Tuskhead Zombie | 象牙头僵尸 |
| `ZOMBIE_ICEAGE_CHARRED` | Charred Zombie | 烧焦的僵尸 |
| `ZOMBIE_ICEAGE_CHIEF` | Chief Icewind Zombie | 首席冰风僵尸 |
| `ZOMBIE_ICEAGE_CHIEF_MINIBOSS_PHASE1` | Elder Hailstorm | 冰雹长者 |
| `ZOMBIE_ICEAGE_CHIEF_VETERAN` | Chief Hailstorm Zombie | 首席冰雹僵尸 |
| `ZOMBIE_ICEAGE_DODO_VETERAN` | Robo Dodo | 机器渡渡鸟 |
| `ZOMBIE_ICEAGE_FLAG_VETERAN` | Cave Rally Zombie | 洞穴拉力赛僵尸 |
| `ZOMBIE_ICEAGE_HUNTER_VETERAN` | Shellshock Hunter Zombie | 炮弹冲击猎人僵尸 |
| `ZOMBIE_ICEAGE_WEASELHOARDER_VETERAN` | Weasel Queen | 黄鼠狼女王 |
| `ZOMBIE_ICEAGE_WEASEL_VETERAN` | Permafrost Weasel | 永久冻土黄鼠狼 |
| `ZOMBIE_IMPPEAR_OVERSEER` | The Overseer | 督军 |
| `ZOMBIE_IMPPEAR_PIANO` | Pianist Imp | 钢琴家小鬼僵尸 |
| `ZOMBIE_LEPRACHAUN_DODO` | Leprechaun Dodo Rider | 妖精渡渡鸟骑士 |
| `ZOMBIE_LEPRACHAUN_IMP` | Leprechaun Imp | 妖精小鬼僵尸 |
| `ZOMBIE_LION_DANCE` | Lion Dancer Zombie | 舞狮僵尸 |
| `ZOMBIE_LOSTCITY_ARMOR4` | Templehead Zombie | 庙头僵尸 |
| `ZOMBIE_LOSTCITY_CRYSTALSKULL_VETERAN` | Magenta Skull Zombie | 洋红色骷髅僵尸 |
| `ZOMBIE_LOSTCITY_EXPLORER` | Lost Explorer Zombie | 迷失探险家僵尸 |
| `ZOMBIE_LOSTCITY_FLAG_VETERAN` | Adventurer Rally Zombie | 冒险家拉力赛僵尸 |
| `ZOMBIE_LOST_ARMOR2` | Kettlehead Adventurer | 水壶头冒险家僵尸 |
| `ZOMBIE_LUNAR` | Lunar Zombie | 月球僵尸 |
| `ZOMBIE_LUNAR_ARMOR1` | Lunar Conehead | 月球锥头 |
| `ZOMBIE_LUNAR_ARMOR2` | Lunar Buckethead | 月球桶头 |
| `ZOMBIE_LUNAR_BANDIT` | Lunar Bandit Zombie | 月球强盗僵尸 |
| `ZOMBIE_LUNAR_FLAG` | Lunar Flag Zombie | 农历旗帜僵尸 |
| `ZOMBIE_LUNAR_GARGANTUAR` | Sheepish Gargantuar | 胆怯巨人僵尸 |
| `ZOMBIE_LUNAR_IMP` | Wooly Imp | 毛茸茸的小鬼僵尸 |
| `ZOMBIE_LUNAR_MONEYTREE` | Money Tree Zombie | 金钱树僵尸 |
| `ZOMBIE_LUNAR_NEWSPAPER` | Lunar Newspaper Zombie | 农历报纸僵尸 |
| `ZOMBIE_LUNAR_RELICHUNTER` | Lunar Raider Zombie | 月球袭击者僵尸 |
| `ZOMBIE_LUNAR_SUPERFANIMP` | Lunar Super-Fan Imp | 农历超级粉丝小鬼 |
| `ZOMBIE_MINIBOSS_IMPFINITY` | Impfinity | 小鬼僵尸有限 |
| `ZOMBIE_MODERN_BERSERKER` | Berserker Zombie | 狂战士僵尸 |
| `ZOMBIE_PIRATE_BARREL` | Pirate Barrel | 海盗滚桶 |
| `ZOMBIE_PLANTAGENET` | Plantagenet Zombie | 金雀花僵尸 |
| `ZOMBIE_PLANTAGENET_ARMOR1` | Plantagenet Conehead | 金雀花锥头 |
| `ZOMBIE_PLANTAGENET_ARMOR2` | Plantagenet Buckethead | 金雀花桶头 |
| `ZOMBIE_PLANTAGENET_FLAG` | Plantagenet Flag Zombie | 金雀花旗帜僵尸 |
| `ZOMBIE_PLANTAGENET_GARGANTUAR` | Chef Gargantuar | 厨师巨人僵尸 |
| `ZOMBIE_PLANTAGENET_IMP` | Server Imp | 服务器小鬼僵尸 |
| `ZOMBIE_PLANTAGENET_NOBLEWOMAN` | Noblewoman Zombie | 贵妇僵尸 |
| `ZOMBIE_PLANTAGENET_PRINCESS` | Royal Princess Zombie | 皇家公主僵尸 |
| `ZOMBIE_PLANTAGENET_WINE` | Wine Taster Zombie | 品酒师僵尸 |
| `ZOMBIE_RIFT` | Construction Zombie | 建筑僵尸 |
| `ZOMBIE_RIFT_ARMOR1` | Construction Conehead Zombie | 建筑路障僵尸 |
| `ZOMBIE_RIFT_ARMOR2` | Construction Buckethead Zombie | 建筑铁桶僵尸 |
| `ZOMBIE_RIFT_ARMOR4` | Hourglass-Head Zombie | 沙漏头僵尸 |
| `ZOMBIE_RIFT_BARRELROLLER` | Peculiar Barrel Roller | 特殊滚筒滚轮 |
| `ZOMBIE_RIFT_EXCAVATOR` | Para-vator Zombie | 伞兵僵尸 |
| `ZOMBIE_RIFT_FLAG` | Construction Flag Zombie | 建筑旗帜僵尸 |
| `ZOMBIE_RIFT_FLAG_VETERAN` | Construction Rally Zombie | 建筑拉力赛僵尸 |
| `ZOMBIE_RIFT_GARGANTUAR` | Babyface Gargantuar | 娃娃脸巨人僵尸 |
| `ZOMBIE_RIFT_GARGIMP` | Gargimp | 加金普 |
| `ZOMBIE_RIFT_IMP` | Construction Imp | 建筑小鬼僵尸 |
| `ZOMBIE_RIFT_JANE` | Exca-sol Zombie | Exca-sol 僵尸 |
| `ZOMBIE_RIFT_SNIFFER` | The Sniffer | 嗅探器 |
| `ZOMBIE_RIFT_WEASEL` | Tumble-Weasel | 翻滚黄鼠狼 |
| `ZOMBIE_ROMAN_SHIELD_PAIR` | Roman Shield Pair | 一对罗马盾牌僵尸 |
| `ZOMBIE_ROMAN_SHIELD_TRIAD` | Roman Shield Triad | 罗马盾牌僵尸三件套 |
| `ZOMBIE_SERVANT` | Maid Zombie | 女仆僵尸 |
| `ZOMBIE_SERVANT_ARMOR1` | Maid Conehead | 女仆锥头 |
| `ZOMBIE_SERVANT_ARMOR2` | Maid Buckethead | 女仆桶头 |
| `ZOMBIE_SERVANT_BELL` | Bell Maid Zombie | 贝尔女仆僵尸 |
| `ZOMBIE_SERVANT_BESOM` | Besom Maid Zombie | Besom 女仆僵尸 |
| `ZOMBIE_SERVANT_BLACK_IMP` | Imp Maid | 小鬼僵尸女仆 |
| `ZOMBIE_SERVANT_FLAG` | Maid Flag Zombie | 女仆旗帜僵尸 |
| `ZOMBIE_SERVANT_FLAG_BUFF` | Adept Maid Flag Zombie | 熟练女仆旗帜僵尸 |
| `ZOMBIE_SERVANT_FLAG_VETERAN` | Maid Rally Zombie | 女仆集结僵尸 |
| `ZOMBIE_SERVANT_FLY` | Flying Maid Zombie | 飞天女仆僵尸 |
| `ZOMBIE_SERVANT_FLY_BLACK` | Flying Black Maid Zombie | 飞行黑女仆僵尸 |
| `ZOMBIE_SERVANT_GARGANTUAR` | Maid Gargantuar | 女仆巨人僵尸 |
| `ZOMBIE_SERVANT_IMP` | Red Imp Maid | 红小鬼僵尸女仆 |
| `ZOMBIE_SERVANT_RED` | Red Maid Zombie | 红女仆僵尸 |
| `ZOMBIE_SERVANT_RED_ARMOR1` | Red Maid Conehead | 红女仆锥头 |
| `ZOMBIE_SERVANT_RED_ARMOR2` | Red Maid Buckethead | 红女仆桶头 |
| `ZOMBIE_SERVANT_RED_BELL` | Red Bell Maid Zombie | 红铃女仆僵尸 |
| `ZOMBIE_SERVANT_RED_BESOM` | Red Besom Maid Zombie | 红色扫把女仆僵尸 |
| `ZOMBIE_SERVANT_RED_FLAG` | Red Maid Flag Zombie | 红女仆旗帜僵尸 |
| `ZOMBIE_SERVANT_RED_FLAG_BUFF` | Adept Red Maid Flag Zombie | 熟练红女仆旗帜僵尸 |
| `ZOMBIE_SERVANT_RED_FLAG_VETERAN` | Red Maid Rally Zombie | 红女仆集结僵尸 |
| `ZOMBIE_SERVANT_RED_TEA` | Red Tea Server Zombie | 红茶服务器僵尸 |
| `ZOMBIE_SERVANT_TEA` | Tea Server Zombie | 茶席僵尸 |
| `ZOMBIE_SKYCITY` | Pilot Zombie | 飞行员僵尸 |
| `ZOMBIE_SKYCITY_ARBITER` | Arbiter-X | 仲裁者-X |
| `ZOMBIE_SKYCITY_ARMOR1` | Conehead Pilot Zombie | 锥头飞行员僵尸 |
| `ZOMBIE_SKYCITY_ARMOR2` | Buckethead Pilot Zombie | 桶头飞行员僵尸 |
| `ZOMBIE_SKYCITY_ARMOR3` | Pilot Helmet Zombie | 飞行员头盔僵尸 |
| `ZOMBIE_SKYCITY_ARMOR4` | Warhead Pilot Zombie | 弹头飞行员僵尸 |
| `ZOMBIE_SKYCITY_BATTLEPLANE` | Zombie Fighter | 僵尸战士 |
| `ZOMBIE_SKYCITY_CHICKEN` | Flying Zombie Chicken | 飞行僵尸鸡 |
| `ZOMBIE_SKYCITY_ELECTRIC` | Scientist Zombie | 科学家僵尸 |
| `ZOMBIE_SKYCITY_ELECTRIC_VETERAN` | Overcharged Scientist Zombie | 超负荷科学家僵尸 |
| `ZOMBIE_SKYCITY_FLAG` | Flag Pilot Zombie | 标记飞行员僵尸 |
| `ZOMBIE_SKYCITY_FLAG_VETERAN` | Rally Pilot Zombie | 拉力飞行员僵尸 |
| `ZOMBIE_SKYCITY_GARGANTUAR` | Colonel Gargantuar | 上校巨人僵尸 |
| `ZOMBIE_SKYCITY_GAS` | Gas Pod Imp | 燃气舱小鬼僵尸 |
| `ZOMBIE_SKYCITY_IMP` | Paratrooper Imp | 伞兵小鬼僵尸 |
| `ZOMBIE_SKYCITY_LAUNCHER_ZOMBIE` | Missile Imp | 导弹小鬼僵尸 |
| `ZOMBIE_SKYCITY_PELICAN` | Pelican-1 Aircraft | Pelican-1 飞机 |
| `ZOMBIE_SKYCITY_PROTECTOR` | ZACU Protector Zombie | ZACU 保护者僵尸 |
| `ZOMBIE_SKYCITY_ROCKET` | Commando Zombie | 突击队僵尸 |
| `ZOMBIE_SKYCITY_TWINSPLANE` | F-82 Twin Fighter Zombie | F-82 双战斗机僵尸 |
| `ZOMBIE_SPACE_DANCER` | Space Dancer | 太空舞者 |
| `ZOMBIE_SPORTZBALL` | Lawnbowl Zombie | 草坪碗僵尸 |
| `ZOMBIE_SPORTZBALL_ARMOR1` | Lawnbowl Conehead | 草坪碗圆锥头僵尸 |
| `ZOMBIE_SPORTZBALL_ARMOR2` | Lawnbowl Buckethead | 草坪碗斗头 |
| `ZOMBIE_SPORTZBALL_BALLOON` | Lawnbowl Balloon Zombie | 草坪碗气球僵尸 |
| `ZOMBIE_SPORTZBALL_FLAG` | Lawnbowl Flag Zombie | 草坪碗旗帜僵尸 |
| `ZOMBIE_SPORTZBALL_GARGANTUAR` | Lawnbowl Gargantuar | 草坪碗巨人僵尸 |
| `ZOMBIE_SPORTZBALL_IMP` | Lawnbowl Imp | 草坪碗小鬼僵尸 |
| `ZOMBIE_SPORTZBALL_WIZARD` | Lawnbowl Wizard | 草坪碗巫师 |
| `ZOMBIE_SPRING` | Springening Zombie | 春天的僵尸 |
| `ZOMBIE_SPRING_ARMOR1` | Springening Conehead | 弹簧锥头 |
| `ZOMBIE_SPRING_ARMOR2` | Springening Buckethead | 弹力桶头 |
| `ZOMBIE_SPRING_ARMOR4_RED` | Egghead Zombie | 蛋头僵尸 |
| `ZOMBIE_SPRING_FLAG` | Springening Flag Zombie | 春天旗帜僵尸 |
| `ZOMBIE_SPRING_GARGANTUAR` | Hippity-Hop Gargantuar | 嬉皮舞巨人僵尸 |
| `ZOMBIE_SPRING_IMP` | Chick Imp | 小鸡小鬼僵尸 |
| `ZOMBIE_SPRING_PROSPECTOR` | Flying Rabbit | 飞兔 |
| `ZOMBIE_SPRING_WIZARD` | Springening Wizard | 春天向导 |
| `ZOMBIE_STEAM` | Labor Zombie | 劳工僵尸 |
| `ZOMBIE_STEAM_ARMOR1` | Conehead Labor Zombie | 锥头劳工僵尸 |
| `ZOMBIE_STEAM_ARMOR2` | Buckethead Labor Zombie | 桶头劳工僵尸 |
| `ZOMBIE_STEAM_BARREL` | Barrel Zombie | 桶状僵尸 |
| `ZOMBIE_STEAM_CLOCKWORK` | Clockwork Zombie | 发条僵尸 |
| `ZOMBIE_STEAM_FLAG` | Flag Labor Zombie | 标记劳工僵尸 |
| `ZOMBIE_STEAM_FURNACE` | Furnace Zombie | 熔炉僵尸 |
| `ZOMBIE_STEAM_GARGANTUAR` | Foreman Gargantuar | 工头巨人僵尸 |
| `ZOMBIE_STEAM_GENTLEMAN` | Gentleman Zombie | 绅士僵尸 |
| `ZOMBIE_STEAM_IMP` | Industrial Imp | 工业小鬼僵尸 |
| `ZOMBIE_STEAM_INVENTOR` | Inventor Zombie | 发明家僵尸 |
| `ZOMBIE_STEAM_MECHANIC` | Mechanic Zombie | 机械僵尸 |
| `ZOMBIE_STEAM_MINER_COAL` | Coal Imp | 煤小鬼僵尸 |
| `ZOMBIE_STEAM_MINER_TRAIN` | Coal Train Zombie | 煤炭火车僵尸 |
| `ZOMBIE_STEAM_REPAIRIMP` | Repairimp | 修理小鬼 |
| `ZOMBIE_STPATRICK` | St. Paddy’s Zombie | 圣。帕迪的僵尸 |
| `ZOMBIE_STPATRICK_ARMOR1` | St. Paddy’s Conehead | 圣。帕迪的锥头 |
| `ZOMBIE_STPATRICK_ARMOR2` | St. Paddy’s Buckethead | 圣。帕迪的桶头 |
| `ZOMBIE_STPATRICK_FLAG` | St. Paddy’s Flag Zombie | 圣。帕迪的旗帜僵尸 |
| `ZOMBIE_STPATRICK_GARGANTUAR` | Slamrock Gargantuar | Slamrock 巨人僵尸 |
| `ZOMBIE_STPATRICK_GLITTER` | Lepreglitter | Lepreglitter |
| `ZOMBIE_STPATRICK_PUNK` | Leprepunk | 妖精朋克 |
| `ZOMBIE_STPATRICK_RA` | St. Paddy’s Ra Zombie | 圣。帕迪的太阳神僵尸 |
| `ZOMBIE_SUMMER_ARMOR1` | Summer Conehead | 夏季锥头 |
| `ZOMBIE_SUMMER_ARMOR2` | Summer Buckethead | 夏季桶头 |
| `ZOMBIE_SUMMER_BASIC` | Summer Zombie | 夏日僵尸 |
| `ZOMBIE_SUMMER_BOOMBOX` | Valenbrainz Boombox | 情尸节音箱 |
| `ZOMBIE_SUMMER_BUG` | Lightning Bug | 闪电虫 |
| `ZOMBIE_SUMMER_EXPLORER` | S'more Zombie | 更多僵尸 |
| `ZOMBIE_SUMMER_FLAG` | Summer Flag Zombie | 夏季旗帜僵尸 |
| `ZOMBIE_SUMMER_GARGANTUAR` | King of the Grill | 烧烤之王 |
| `ZOMBIE_SUMMER_IMP` | Hot Dog Imp | 热狗小鬼僵尸 |
| `ZOMBIE_SUMMER_SHELL_SHIELD` | Clamburger Zombie | 汉堡僵尸 |
| `ZOMBIE_VALENTINES` | Valenbrainz Zombie | 情尸僵尸 |
| `ZOMBIE_VALENTINES_ARMOR1` | Valenbrainz Conehead | 情尸节锥头 |
| `ZOMBIE_VALENTINES_ARMOR2` | Valenbrainz Buckethead | 情尸节桶头 |
| `ZOMBIE_VALENTINES_BALLOON` | Luv Zombie | 爱僵尸 |
| `ZOMBIE_VALENTINES_FLAG` | Valenbrainz Flag Zombie | 情尸节旗帜僵尸 |
| `ZOMBIE_VALENTINES_GARGANTUAR` | Lovestruck Gargantuar | 痴情巨人僵尸 |
| `ZOMBIE_VALENTINES_IMP` | Cupid Imp | 丘比特小鬼僵尸 |
| `ZOMBIE_VALENTINES_JANE` | Valenbrella Zombie | 情尸阳伞僵尸 |
| `ZOMBIE_VALENTINES_SUPERFANIMP` | Stupid Cupid-Fan Imp | 愚蠢的丘比特迷小鬼僵尸 |
| `ZOMBIE_WEALTH_GOD` | Wealth God Zombie | 财神僵尸 |
| `ZOMBIE_ZCORP_ARMOR4` | Computerhead New Hire | 电脑头新员工 |
| `ZOMBIE_ZCORP_FEM_ARMOR4` | Computerhead Contractor | 电脑头承包商 |
| `ZOMBIE_ZOMBOSSMECH_BEACH2` | Zombot Sharktronic Sub 2.0 | 僵博机器人 Sharktronic Sub 2.0 |
| `ZOMBIE_ZOMBOSSMECH_COWBOY2` | Zombot War Wagon 2.0 | 僵博机器人战车2.0 |
| `ZOMBIE_ZOMBOSSMECH_DARK2` | Zombot Dark Dragon 2.0 | 僵博机器人暗龙2.0 |
| `ZOMBIE_ZOMBOSSMECH_DINO2` | Zombot Dinotronic Mechasaur 2.0 | 僵博机器人恐龙电子机甲龙2.0 |
| `ZOMBIE_ZOMBOSSMECH_EGYPT2` | Zombot Sphinx-inator 2.0 | 僵博机器人 Sphinx-inator 2.0 |
| `ZOMBIE_ZOMBOSSMECH_EIGHTIES2` | Zombot Multi-stage Masher 2.0 | 僵博机器人多级捣碎器2.0 |
| `ZOMBIE_ZOMBOSSMECH_EIGHTIES_BATTLEZ` | Zombot Seasonal Sleigh-er | 僵博机器人季节性雪橇 |
| `ZOMBIE_ZOMBOSSMECH_FAIRYTALE` | Nanny's Nyctalopic Nightmare-tron | 保姆的夜魇梦魇 |
| `ZOMBIE_ZOMBOSSMECH_FUTURE2` | Zombot Tomorrow-tron 2.0 | 僵博机器人明天-tron 2.0 |
| `ZOMBIE_ZOMBOSSMECH_ICEAGE2` | Zombot Tuskmaster 10,000 BC 2.0 | 僵博机器人象牙大师 10,000 BC 2.0 |
| `ZOMBIE_ZOMBOSSMECH_LOSTCITY2` | Zombot Aerostatic Gondola 2.0 | 僵博机器人静压吊篮2.0 |
| `ZOMBIE_ZOMBOSSMECH_MARKET` | Greedy's Klepto-maton 20,000 | 贪婪的小偷 20,000 |
| `ZOMBIE_ZOMBOSSMECH_MODERN1` | Zombot Lawn-O-Tron | 僵博机器人草坪-O-特隆 |
| `ZOMBIE_ZOMBOSSMECH_PIRATE2` | Zombot Plank Walker 2.0 | 僵博机器人平板行走者2.0 |
| `ZOMBIE_ZOMBOSSMECH_SKYCITY` | Camotron Vulture Fighter | 卡莫特龙秃鹰战斗机 |
| `ZOMBIE_ZOMBOSSMECH_STEAM` | Zombot Loco-motive | 僵博机器人机车 |
