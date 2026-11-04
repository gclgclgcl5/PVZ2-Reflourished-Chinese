# 史诗任务对白连贯性：分析账本

对照：`LawnStrings_en.json`（蓝本） / `LawnStrings_zh.json`。  
范围：**`NARRATIVE_EPIC_QUEST_*`**（约 **106** 场、**925** 行）。  
另有 **`NARRATIVE_EPIC_REALM_*`** —— 见 [`epic_realm_narrative_findings.md`](epic_realm_narrative_findings.md)（**领域仍未改稿**）。  
原则同主线：相邻句逻辑/包袱；术语跟 [`STYLE.md`](STYLE.md)。

原始转储：`F:\sen_work\epic_narrative_scan\all_epic_narr.txt`  
家族索引：`F:\sen_work\epic_narrative_scan\families.md`

---

## 体量与任务链（EPIC_QUEST）

| 家族 | 场次数（约） | 备注 |
|------|-------------|------|
| RIFT | 13 | 次元高速/裂缝长剧情 |
| METEORZ | 9 | 流星Z / 卡莫将军 |
| CLASSROOM | 8 | 香草宇宙教室+数值课 |
| ELECTRICCURRANT | 8 | 电流醋栗 |
| ALOE | 7 | 芦荟营救 |
| ENDANGERED | 7 | 濒危/被俘植物 |
| HERPLE_IMPPEAR | 7 | 小鬼梨 |
| EIGHTIES / PARODY / SHADOWLURKERS | 6 各 | 宝石/恶搞/暗影 |
| 其余（GEMJAM、GOLDBLOOM、POOLPARTY…） | ≤4 | 短链 |

术语粗扫（丧尸/大卫/青灰/废渣/植物性食物/**充值**）：**EPIC_QUEST 与 EPIC_REALM 均 0 命中**（冷却已多写「冷却时间」，符合 STYLE）。

---

## 总判（先读这）

史诗任务对白整体比海滩/海盗主线**干净**：大量教学/数值句可读；叶绿素用法正确。  
问题集中在：**(1) 字面机器译把习语砸碎；(2) 个别双关铺垫没收；(3) 专名与主线/图鉴不一致。**  
P0 数量少于主线首轮。**史诗任务改稿已落地**（见文末「改稿记录」）；领域仍未动。

---

## P0（相邻句断 / 语义反了 / 习语砸碎）

### METEORZ（流星Z）— `…_METEORZ_8_INTRO`
| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `_16` | *Bingo.*（说对了） | 「宾果游戏」——接不上「炸月」揭晓 |
| `_23` | *ugly MUG*＝丑脸 | 「丑陋的杯子」 |
| `_24` | 僵王脸每晚从天上瞪你们 | 「带着那张无知的脸盯着你们睡觉」主客颠倒 |
| `_29` | carve face **into** the moon | 「把他的脸雕刻成月亮」变成把脸雕成月亮本体 |

同场还有：Camo 称谓「卡莫 / 迷彩」混用（`_11` vs `_15`）→ 标 P1。

### ENDANGERED（濒危营救）
| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `…_02_INTRO_12` | *on my watch*＝在我眼皮底下 | 「在我的手表上玩弄」 |
| `…_08_INTRO_2` | *show him what's what* | 「展示什么是什么」 |
| `…_08_INTRO_5`→`_6`→outro `_4` | *GRIM situation* 铺垫 Grimrose，后文 *now I get it* | 只译「严峻的情况」，戴夫后知后觉包袱悬空 |

另：`…_08_OUTRO_3` Grimrose→「墓碑玫瑰」，图鉴锁名多为「**暗樱草**」（STAT 里仍见墓碑玫瑰残留）——专名 P1。  
`…_02_INTRO_9` Homing Thistle→「归巢蓟」，主线/图鉴多用「**导向蓟**」。

### ALOE（芦荟）
| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `…_09_INTRO_2` | *This is a first*＝戴夫难得思考 | 「这只是一个开始…请继续这段旅程」——打掉讽刺，后文「点亮」玩笑变悬浮 |
| `…_10_INTRO_3` | 永久获得芦荟 | 句末赘「无胡！」无来源 |

`…_09_INTRO_4` *bright idea*→「点赞」丢光亮双关（P1，可与 `_3` 照明开关一起收）。

### ELECTRICCURRANT（电流醋栗）
| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `…_6_INTRO_2` | *thank you for inquiring*＝谢你关心电量 | 「感谢你为我寻找醋栗」——话题被改写成找植物 |

同链：`电流醋栗` / `电流红醋栗` 混用（`_2` vs `_4`）→ P1。  
`…_2_INTRO_4` *positive development* 电学双关弱化（P1，可选）。

### GOLDBLOOM（黄金蓓蕾）
| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `…_1_INTRO_1` | *leather*（皮革） | 「羽毛」——嗅觉铺垫错味 |

### EIGHTIES 宝石线
| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `…_EIGHTIES_10_OUTRO_3` | *Me and User Dave* | 残留英文 **「Me」** |
| `…_EIGHTIES_10_INTRO_4` | *avenue is stacked* | 「大道堆叠」难懂（P1 偏 P0） |

### RIFT（裂缝高速）
| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `…_RIFT_1_INTRO_7` | *Last time I'm asking*＝最后一次问路 | 「上次向旅行日志问路」——时态/语气反了 |

---

## P1（能读但笑点/专名弱）

| 位置 | 问题 |
|------|------|
| CLASSROOM `…_STEP_05_INTRO_1` | Jurassic Marsh →「恐龙危机」；主线世界名应为「侏罗纪沼泽」 |
| CLASSROOM 数值课 | 整体好；`recharge` 已作「冷却时间」✓；Citron「充能柚子」需与锁表核对 |
| BEGHOULED Power-Ups | 「金手指道具」+ 移换指/铁铲指——与主线「火焰指」等是否统一，待 STYLE 确认 |
| ELECTRICCURRANT `Watt` / `coulomb-ination` | 中文另造「瓦特」「库仑」尚可；*positive* 电双关仍弱 |
| ENDANGERED GRIM / 暗樱草 | 见上；outro「保存」辣椒投手宜「救出/救下」 |
| HERPLE `…_04_5` | *ain't so bad after all*→「毕竟没那么坏」略生硬 |
| HERPLE `…_01_5` | *And I thought stale milk was bad* 比较句变陈述 |
| GOLDBLOOM `…_2_INTRO_3` | *MUST GO FASTER* 被收成「冷却再快一点」，赛博梗/语速梗变机制吐槽 |
| RIFT `…_2_INTRO_3` | *close and personal*→「亲密和私人」 |
| RIFT `…_1_INTRO_6` | Wild West→「西部荒野」vs「狂野西部」 |
| ALOE Travel Log | 「旅行木标」vs 他处「旅行日志」 |
| METEORZ Camo | 「卡莫」/「迷彩」不统一 |
| PARODY / SHADOWLURKERS / GEMJAM | **复扫已补 P0**（见下节）；POOLPARTY 复扫无新硬伤 |
| ELECTRICCURRANT `…_10_OUTRO_1` | 「电醋栗」vs 他处「电流醋栗/电流红醋栗」—专名再统一 |
| BEGHOULED Power-Ups | 「金手指道具」仍待与主线火焰指等 STYLE 对齐 |

---

## 按链可读性速评（未改）

| 链 | 观感 |
|----|------|
| CLASSROOM | 长但连贯；修世界名即可 |
| ALOE | 短链好读；`_09` 思考梗、`无胡` 必修 |
| ELECTRICCURRANT | 机制清楚；询问句 + 专名统一 |
| ENDANGERED | 剧情在；手表/what's what/GRIM 三处伤叙事 |
| METEORZ | 高潮场 `_8` 中译伤最重 |
| RIFT | 气氛好；「上次问路」等 MT 点缀 |
| HERPLE / GOLDBLOOM | 中等；皮革→羽毛是硬伤 |
| **PARODY** | 电影恶搞链；**temple/ACTION/Hasta/bombing** 等漏网（复扫） |
| **SHADOWLURKERS** | 忧郁藤营救可读；**Jeepers→吉普车** 开场即炸 |
| **GEMJAM** | 短；`Heard the horde's hoard` 整句跑偏 |
| POOLPARTY / BEGHOULED | 复扫未见同级 P0 |

---

## 复扫补遗（启发式 + 先前未深挖链全量过目）

范围：2543 条 `EPIC_QUEST_*` + `EPIC_REALM_*`；对照已知 P0 池去重；并深挖先前标注「未挂 P0」的 PARODY / SHADOW / GEMJAM / POOLPARTY。

### 新发现 P0（任务侧，先前账本未列）

| 键 | EN 意图 | ZH 问题 |
|----|---------|---------|
| `…_PARODY_01_INTRO_10` | *My head is my temple*＝圣殿/禁地 | 「太阳穴」——解剖义选错，后文嘲头梗断 |
| `…_PARODY_05_INTRO_7` | *a great one*＝好片 | 「伟大的比赛」——电影变竞赛 |
| `…_PARODY_06_INTRO_7` | *ACTION!*＝开拍 | 「行动！」 |
| `…_PARODY_09_INTRO_6` | *Hasta la vista!*（终结者梗） | 「祝你好运！」 |
| `…_PARODY_10_INTRO_1` | *bombing with test audiences*＝票房扑街 | 「被测试观众轰炸」——字面爆炸 |
| `…_SHADOWLURKERS_01_INTRO_1` | *Jeepers!*＝感叹 | 「吉普车」 |
| `…_GEMJAM_1_INTRO_2` | *Heard the horde's hoard, huh?* 听/群/窖双关 | 「无脑，潦倒，却在悄悄藏宝？」——语义全跑 |

### 新发现 / 加重 P1（任务侧）

| 位置 | 问题 |
|------|------|
| PARODY `…_05_INTRO_2` | *overtake the field*→「反超领域」 |
| PARODY `…_10_OUTRO_2` | *bargain bin*→「进便宜货」生硬 |
| PARODY `…_06_INTRO_1` | *terrible associates*→「会成为糟糕的同事」时态/语气偏 |
| SHADOW `…_01_INTRO_5` | *can't play tricks with tacos*→「不会用玉米卷耍花招」许可义变能力义 |
| SHADOW `…_08_INTRO_6` | *We've got this*→「我们有这个」 |
| SHADOW `…_08_OUTRO_5` | *Indeed it has*→「确实有」 |
| SHADOW `…_02_INTRO_5` | *captured*→「占领」宜「俘虏/抓走」 |
| SHADOW 专名 | Gloom-shroom「忧郁蘑菇/幽暗蘑菇」混用 |
| GEMJAM `…_1_INTRO_1` | *audio-detected…stash* 句略绕，可顺手润 |

### 复扫结论（任务）

- **首轮已挂 P0 全部仍在**（METEORZ mug/Bingo、ENDANGERED watch、ALOE 无胡、EIGHTIES Me、RIFT 上次问路等）——无「已修好却账本未删」的误报。  
- **真正遗漏集中在首轮声明「未深挖」的 PARODY / SHADOW / GEMJAM**；POOLPARTY 复扫干净。  
- STYLE 粗扫（丧尸/大卫/青灰/废渣/充值/Plant Food 英文残留）：EPIC 仍 **0**。  
- 改稿建议顺序更新：**原 P0 池 → PARODY 电影梗五连 → SHADOW Jeepers → GEMJAM horde/hoard → 再扫 P1**。

原始复扫产物：`F:\sen_work\epic_rescan\`（`rescan_report.md` / `pass2_new.md` / `family_*.txt`）。

---

## 与主线账本的关系

- 主线 R1/R2 已清的「青灰/废渣/Hang on」类：**史诗任务侧未复现同款残留**。  
- 新问题类型偏 **习语字面译**（watch / mug / Bingo / what's what / Jeepers / temple）与 **专名漂移**（导向蓟/暗樱草/侏罗纪沼泽）。  
- **LTE 节日线**另有同款习语残留（手表/杯子/Dang），见主线账本「复扫」节——**不在 EPIC 前缀内**。  
- 建议改稿顺序（将来）：**METEORZ_8 → ENDANGERED → ALOE → PARODY → SHADOW → GEMJAM → ELECTRICCURRANT_6 → GOLDBLOOM_1 → RIFT_1 → EIGHTIES_10**，再扫剩余 P1。

---

## 改稿记录（EPIC_QUEST）

- 脚本：`F:\sen_work\_apply_epic_quest_zh.py`  
- 写入：`localization/LawnStrings_zh.json` + `localization/current/LawnStrings_zh.json`  
- 变更约 **58** 键：账本 P0 全量 + 复扫 PARODY/SHADOW/GEMJAM + 同场/专名 P1（卡莫统一、导向蓟/暗樱草/侏罗纪沼泽/旅行日志/狂野西部、电流醋栗、忧郁蘑菇/忧郁藤蔓、HERPLE 两句润色）  
- 验收：原硬伤针（宾果游戏/丑陋的杯子/手表/什么是什么/无胡/太阳穴/吉普车/Me 等）在 `EPIC_QUEST` **清零**；卡莫「迷彩」残留 **0**；GRIM→暗樱草包袱链已接上  
- EN 未改；未 encode / 未打包  

### 仍可后续润（非阻断）

- BEGHOULED「金手指道具」vs 主线强化指称谓  
- CLASSROOM 其它数值课细读、Citron「充能柚子」锁表核对  
- 全 925 行文学精校  
- SHADOW / GEMJAM 复扫项若仍有残留可再扫  

### 改稿补记（PARODY 机翻口袋 · 2026-11）

- 触发：`PARODY_01_INTRO_4`「创意出口会引起我的警报」词表对译  
- 脚本：`F:\sen_work\_apply_epic_quest_parody_narr_zh.py`  
- **整族** `NARRATIVE_EPIC_QUEST_PARODY_*`（5 场 / 52 行）回炉；`creative outlet` 成对锁定；片场黑话（still / parts / introduction scene / remake）重建  
- 顺手按用户改法修 LTE：`NARRATIVE_LTE_2023_11_HEROES_10_INTRO_13`（if you will excuse me ←「现在麻烦你了」）  
- 同类「告退套话」机翻分析见下节交叉：LTE Heroes_10 同场仍有一批直译腔待另账

史诗领域：[`epic_realm_narrative_findings.md`](epic_realm_narrative_findings.md)（**P0/同场 P1 已改稿**）；领域 TITLE：[`epic_realm_title_findings.md`](epic_realm_title_findings.md)。
