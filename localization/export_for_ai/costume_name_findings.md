# 植物装扮名称汉化质量：全量分析账本

对照：`LawnStrings_en.json`（蓝本） / `LawnStrings_zh.json`。  
术语：[`STYLE.md`](STYLE.md)、[`almanac/almanac_name_lock.json`](almanac/almanac_name_lock.json)。

扫描产物：`F:\sen_work\costume_name_scan\`  
（`coverage_checklist.txt`、`full_*.md`、`full_stats_flags.md`、`plant_drift_all_product.md`、`full_custom_holiday.md`）

---

## 1. 覆盖范围（已全量过目）

| 键族 | 条数 | 过目方式 | 说明 |
|------|------|----------|------|
| `product_cost_*_custom*_name` | **365** | 全量 EN/ZH 落盘 + 启发式 | 含 15 条节日/活动命名 custom（非 `custom数字`） |
| `product_cost_*_skin_*_name` | **164** | 全量落盘 + 拉丁/梗审 | **首轮遗漏，本轮补全** |
| `product_cost_*_costume_*_name` | **21** | 全量人工读 | 铁桶系列、FNF/百里香等 |
| `product_costume_*_name` | **22** | 全量 | 通用装扮件名 |
| `product_costume_*_s` | **53** | 全量 | 商店短名 |
| `product_costume_*` 且 EN=`Costume:…` | **124+** | 全量格式+专名针 | 统一「装扮：」 |
| `product_costume_*` 其它标题/说明面 | **55** | 全量落盘 | 含安全帽名、短 desc 型文案 |
| `product_costume_*_desc` | **22** | 全量 | 随名称问题点到 PinkTopper 等 |
| `product_bundle_*costume*` | **12** | 抽查 | 捆绑包短名，非装扮展示名核心 |

**展示名核心合计约 625 条**（custom+skin+cost_costume+pc_name+pc_s）。  
另有 Costume 标签与其它标题面合计约 200 条已扫。

---

## 2. 总判

1. **主体质量高**：custom/skin 绝大多数已是中文可读名；不是「大面积未译」问题。  
2. **硬伤少但确定**：`Black Belt→黑色领带`、`Pink Topper→粉色上衣`（且与同装 `_s`「粉色小帽」、desc「穿粉色衣服」连环矛盾）。  
3. **专名双轨是最大债**：装扮包/短名里「导弹槲寄生 / 遁地根 / 毒蝇伞 / 辣椒豆 / 葡萄霰弹」与锁名或同键另一面互殴（同植物有的面已用正确锁名）。  
4. **`skin_*` 新发现**：仅 3 条整段拉丁（`China` / `3l3ctro` / `Najimi…` 词序对调）；大量二次元/谐音梗有中文重建，整体可接受。个别弱译（「更墨西哥」「手杖态度」）。  
5. **新 P1**：`Count Jackula` 英文残留；Pinchess 丢 pin；Thyme/FNF/节日 custom 有可润空间。  
6. **注意**：`遁地根`/`导弹槲寄生` 也出现在 **ADVICE/叙事**（非仅装扮）；装扮改稿时若锁「逃脱树根/槲寄冰仙子」，需决定是否全局统一（超出本账本「只评装扮」时可另开）。

---

## 3. P0（错义 / 自相矛盾）

| 键 | EN | ZH | 问题 |
|----|-----|-----|------|
| `product_costume_BlackBelt_name` | Black Belt | 黑色领带 | 空手道黑带≠领带；`bonkchoy_blackbelt_*_s` 已是「菜问 黑带」 |
| `product_costume_PinkTopper_name` | Pink Topper | 粉色上衣 | topper=顶饰；`cherrybomb_pinktop_*_s`=「粉色小帽」 |
| `product_costume_PinkTopper_desc` | …pretty in pink | …穿粉色的**衣服** | 被错误「上衣」带着走 |
| `product_costume_cherrybomb_pinktop_nonconsume` | 同上 | 同上 | 与 `_s` 小帽矛盾 |

---

## 4. P1（专名漂移 / 残留英文 / 弱双关）

### 4.1 装扮面植物锁名漂移（product_costume 内已定位）

| 错误写法 | 锁名/偏好 | 装扮键例 |
|----------|-----------|----------|
| 导弹槲寄生 | 槲寄冰仙子 | `missiletoe_scarf_*_g20`、`*_t2_s`（同植物 `*_t2` 无后缀面已用槲寄冰仙子） |
| 遁地根 | 逃脱树根 | `escaperoot_helmet_*_g10`、`sheriff_*_s`（`*_t1` 无 `_s` 已用逃脱树根） |
| 毒蝇伞 | 金蟾菇 | `toadstool_afro_*_g10`、`purplehat_*_s`（`*_t1` 无 `_s` 已用金蟾菇） |
| 辣椒豆 | 巴豆 | `chilibean_diaper*`（desc 面已写巴豆） |
| 葡萄霰弹 | 葡萄爆弹 | `grapeshot_*_s`（同植物 `*_t1` 无 `_s` 已用葡萄爆弹） |

模式：**同一装扮 SKU 的「长名/无_s」往往正确，「_s / 廉价 Costume: 标签」用了旧译。**

### 4.2 错字与词选

| 键 | 问题 |
|----|------|
| `product_costume_zoybean_ski_nonconsume` / `_s` | 滑雪**撬**→橇 |
| `product_cost_acidlemon_custom5_name` | Sprinkles→**糖针**宜糖屑/彩针糖 |
| `product_cost_begonia_custom1_name` | **隐斗篷**哨兵语序别扭 |
| `product_costume_primalwall( nut)_overalls_*_s` | Bubba-**Earl**→布巴**伯爵**（人名误爵位；对比 `electricitea_skin_steam`「格雷伯爵」对 Earl Grey **正确**） |
| `product_costume_jackolantern_birthdayz_countjackula_nonconsume_g1` | 残留英文 **Count Jackula** |
| `product_cost_pepperpult_costume_pinchess_name` | Pinchess→只译「国际象棋」，丢 pin/别针双关 |
| `product_cost_peashooter_costume_peamix_name` | 保留 **MPea3**（MP3 梗，可留可注） |

### 4.3 节日 custom（15 条，此前漏扫）

整体可读。可润（非阻断）：

| 键 | EN | ZH | 备注 |
|----|-----|-----|------|
| `…_tallnut_custom_valentines_name` | Tough Love | 严厉的爱 | 偏字面，可「爱要硬气」等 |
| `…_peashooter_custom_feastivus_name` | 'Tis the Peason | 正当豆季 | 有重建，可再贴 season 歌谣感 |
| `…_pepperpult_custom_valentines_name` | Haben-Arrow… | 箭穿心哈巴涅罗 | 可用 |
| `…_wallnut_custom_halloween_name` | King Nutankhamun | 坚果坦卡蒙国王 | 图坦卡蒙谐音尚可 |
| `…_sunflower_custom_feastivus_name` | Zombie Down Your Chimney | 僵尸从烟囱下来 | 圣诞歌仿写，功能够 |

其余情人节/盛宴/Things 线（绿影、甜豌豆、阳光耀斑、胡桃夹子围巾等）**通过**。

### 4.4 `cost_*_costume_*`（21）

- 小喷菇世界铁桶系列：**全部已中文化**，质量稳。  
- `thymewarp_…_boyfriend`：Yesterday Night Funkin'→「昨夜放克」——FNF 梗可读。  
- `thymewarp_…_hourglass`：Thyme and Thyme Again→「一次又一次百里香」——time 双关偏弱，可「百里香了又香」。  
- `shadowshroom_…_mina`：Pinky→「粉粉」可用。

### 4.5 通用名其它

| 键 | 备注 |
|----|------|
| `Tiara_name` / 卷心菜 tiara `_s` | 「王冠」略大，可「头冠」 |
| `RangerHat_name` / 火爆辣椒 `_s` | Parks and Wreck→「公园与毁灭」可读、台梗弱 |
| `Diaper_name` / 巴豆尿布 `_s` | 语义对；产品向恶搞，改名需取舍 |
| `TopCollars` vs kernel `_s` | 「礼帽和翻领」vs「上衣领结」不完全对齐 |

---

## 5. P2（建议默认保留）

| 键 | EN≈ZH | 理由 |
|----|-------|------|
| `…_bombegranate_custom1_name` | D.E.A.F. | 对 L.E.A.F. 的缩写梗 |
| `…_melonpult_custom5_name` | M310N-PU17 | 伪编号梗 |
| `…_electriccurrant_skin_3l3ctro_name` | 3l3ctro | leetspeak 电梗 |
| `…_redstinger_skin_edgest_name` | China | 专名/梗名留英（若有中文设定再改） |
| `…_xshot_skin_insta_name` | Najimi…→词序对调仍拉丁 | 角色名可留；可选中文化 |
| `…_aloe_custom1` 等含 L.E.A.F. | — | STYLE 允许缩写梗 |
| `…_electricitea_skin_steam` | 格雷伯爵爵士 | Earl Grey **应**用伯爵 |

---

## 6. 按键族速评（全量后）

| 键族 | 结论 |
|------|------|
| custom×365 | 主干优秀；P0 无；P1 为词选/节日可润 |
| skin×164 | **补扫完成**；3 条整段拉丁（P2）；少量弱译（更墨西哥、手杖态度、通用发型） |
| cost_costume×21 | 铁桶全过；Pinchess/Thyme 可润 |
| pc_name×22 | **2 条 P0**（领带/上衣） |
| pc_s×53 | 专名漂移 + 滑雪撬；多数合格 |
| Costume: 标签 | 「装扮：」统一；混入旧植物译名（上表） |
| pc_other×55 | 标题面多正确锁名；Count Jackula 英文；粉帽 desc 误「衣服」 |
| pc_desc×22 | 随 BlackBelt/PinkTopper；Wax on 尚可 |
| bundle | 未发现新硬伤 |

---

## 7. 与叙事汉化关系

- 装扮展示名独立于 `NARRATIVE_*`。  
- **迷彩头巾**是图案名，勿改成「卡莫」。  
- 植物旧译（遁地根/导弹槲寄生/辣椒豆）全局别名已于 §10.4 收口。

---

## 8. 改稿顺序（1–3 已落地；其余仍可后续）

1. ~~P0：BlackBelt / PinkTopper~~ **已做**  
2. ~~装扮内专名对齐~~ **已做**  
3. ~~错字与高价值词选（含 Pinchess / Thyme / Tough Love / 头冠 / 领结）~~ **已做**  
4. ~~复扫 P1（Parks / 弱 skin）~~ **已做（第 2 轮 14 键）**  
5. 默认不动：D.E.A.F. / M310N / 3l3ctro / China / L.E.A.F. / Najimi；尿布语气另议

---

## 9. 改稿记录（装扮名）

- 脚本：`F:\sen_work\_apply_costume_names_zh.py`  
- 写入：`localization/LawnStrings_zh.json` + `localization/current/LawnStrings_zh.json`  
- 变更 **27** 键：P0（黑带 / 粉色小帽+desc）+ 五组装扮内植物锁名 + 滑雪橇 / 糖屑 / 斗篷隐哨 / 布巴·厄尔 / 伯爵杰库拉 / 别针象棋 / 百里香了又香 / 爱要硬气 / 头冠 / 礼帽与翻领  
- 验收：`product_costume_*` 内黑色领带、粉色上衣、滑雪撬、Count Jackula、导弹槲寄生、遁地根、毒蝇伞、辣椒豆、葡萄霰弹 **清零**  
- 未动：P2 留英、skin 弱译、ADVICE/叙事全局旧译、encode/打包  

## 10. 改稿后复扫（继续分析，未再改 ZH）

范围：改稿后再次全量扫 custom×365、skin×164、cost_costume×21、pc_name×22、pc_s×53。  
产物：`F:\sen_work\costume_name_scan\postfix_flags.md`（含误报）、语义深挖脚本结论如下。

### 10.1 回归验收

| 检查 | 结果 |
|------|------|
| P0 针（领带/上衣/滑雪撬/Count Jackula）在 `product_costume_*` | **0** |
| 五组旧植物译在 `product_costume_*` | **0** |
| 糖针 / 隐斗篷 / 布巴伯爵（本轮 touched） | **0** |
| 头冠 / 礼帽与翻领 | 已对齐 |
| 新 P0 | **无** |

### 10.2 剩余 P1 → **已改稿（第 2 轮）**

脚本：`F:\sen_work\_apply_costume_p1_zh.py`（再改 **14** 键，已同步 `current/`）。

| 键 | 新 ZH |
|----|-------|
| `RangerHat_name` / 火爆辣椒 `_s` | 园事与拆毁 |
| `chilibean_skin_superchilibean_name` | 更辣墨风 |
| `cactus_skin_festive_name` | 手杖无难 |
| `headbutter_skin_erick_name` | 杰瑞克发型 |
| `poisonpea_skin_mucky_name` | 脏脏泥点 |
| `puffshroom_skin_pvz1_name` | 海见老友 |
| `parsnip_skin_scout_name` | 掐上一千 |
| `cabbagepult_skin_pvz1_name` | 生菜怀旧浪漫 |
| `snowpea_skin_skipea_name` | 滑雪豆的幸福之钥 |
| `shinevine_skin_spaghetti_name` | 叉定胜局 |
| `sunshroom_skin_earmuffs_name` | 盛宴节 '09 |
| `squash_skin_scrooge_name` | 打击麦斯克鲁奇 |
| `peashooter_skin_peabob_name` | 方块射手豆豆鲍勃 |

**其它 skin 可读、仅登记**

- `Cripple Pear`→残梨、`Krill la Krill`→磷虾杀磷虾、`CAPitalist`→帽本家、`Working for Peanuts`→为花生打工、`北半球与暖赤道` 等：功能够，梗密度一般。  
- 长度启发式曾标「过短」的大量条目（太阳女神、不是猫、酸甜双拼等）**多数是合格短名**，不作 P1。

### 10.3 仍为 P2 / 默认不动

- D.E.A.F. / M310N-PU17 / 3l3ctro / China / Najimi 词序 / L.E.A.F. / MPea3  
- 尿布语气（产品恶搞）  
- 进退两糖、刺回过去、锣响鹰眼等「勉强可留」

### 10.4 全局植物锁名漂移（2026-11-04 已收口）

`product_*` 装扮面此前已清零。本轮把库内残留旧译统一到 `almanac_name_lock.json`：

| 旧译 | 锁名 | 键 |
|------|------|-----|
| 导弹槲寄生 | 槲寄冰仙子 | `ADVICE_NO_MISSILETOE_ON_RAILCART`、`NARRATIVE_LTE_2024_07_SUMMERNIGHTS_8_INTRO_16` |
| 遁地根 | 逃脱树根 | `ADVICE_NO_ESCAPEROOT_ON_RAILCART`、`ESCAPEROOT_DESCRIPTION` 机制行、`NARRATIVE_ESCAPEROOT_LOD_2` |
| 辣椒豆 | 巴豆 | `FINISH_COWBOY_4_DESC`、`NARRATIVE_SPONGEBOB_25_INTRO_11` |

验收：全库 `导弹槲寄生|遁地根|毒蝇伞|辣椒豆|葡萄霰弹|滑雪撬` **0** 命中。双写 root + `current/`。

### 10.5 仍可后续

- 尿布语气、其余「可读但梗一般」的 skin 精修  
- P2 留英梗（默认不动）  
- encode / 打包  

