# 「Excuse me / 告退套话」机翻分析

触发：`NARRATIVE_LTE_2023_11_HEROES_10_INTRO_13`  
EN: *Now if you will excuse me, I will go check on the special weapon!*  
旧 ZH: 现在麻烦你了，我去检查一下特殊武器！  
正译方向: **现在，请各位见谅，我要去查看一下那件特殊武器了！**（已按此写入 ZH）

## 病理

`if you will excuse me` = 礼貌告退（容我失陪 / 请见谅），**不是**「麻烦你了」（那是 I'm troubling you / sorry for the bother）。机翻把 excuse 的「借口/麻烦」义选错。

## 同句式在 NARRATIVE_* 中的分布

| 键 | EN | 现译判断 |
|----|-----|----------|
| `LTE_2023_11_HEROES_10_INTRO_13` | Now if you will excuse me… | **已修**（本条） |
| `LTE_2025_03_LUCKOTHEZOMBIE_8_INTRO_17` | Excuse me for a moment. | 「容我失陪片刻」— **合格** |
| `HOLIDAY_22_INTRO_11` | Excuse me, I was turned into an ad. | 「抱歉，…」— **合格**（致歉义） |
| `DARK_INTRO_ZOMBOSS_8` | Excuse me while I run some tests. | 「在此期间请勿打扰我」— 语义到了，略公文 |
| `LTE_2024_07_SUMMERNIGHTS_2_INTRO_1` | Pardon me for our sudden relocation… | 「请原谅我们突然的转移」— 可用，relocation→转移偏硬 |

**结论**：字面同款 `if you will excuse me` 在对白库里几乎是孤例；「麻烦你了」错译也是孤针。更大问题是 **同场 Heroes_10 整段仍偏机翻腔**，不是告退套话扩散。

## 同场 `LTE_2023_11_HEROES_10` 待看（非 excuse，但是同类直译）

| 键 | 问题摘要 |
|----|----------|
| INTRO_1 | 厌倦了和体臭的游戏选手交往 |
| INTRO_2 | 摧毁这个事件 |
| INTRO_3 | 太令人厌恶了，无法继续存在 |
| INTRO_9 | 见面会从今天开始并结束（begins AND ends） |
| INTRO_10 | 寻找复仇 |
| INTRO_16 | 阅读最后一期以了解最新情况 |
| INTRO_18 | 被取消 ← cancelation 活动取消义可留，口吻偏直 |
| INTRO_20 | 我想提醒你 Z-机甲…（可顺成读数/警报口吻） |

## 近亲套话（Allow me / 请允许我）

多处 `Allow me to…` →「请允许我…」：潘妮口吻可接受；注意错义：

- `LTE_2025_02_VALENBRAINZ_2_INTRO_5` *Allow me to recount* →「请允许我清点一下」— **recount=复述，不是清点**（P0 候选）

## 明确不做本轮

- 未批量改 Heroes_10 全场（仅修用户指定句）  
- 未改其它 LTE 家族全文  

## 范围更新（2026-11）

`NARRATIVE_LTE_2023_11_HEROES_*` 属**无 REPLAY 的往届 LTE**，已按 [`lte_qa_scope.md`](lte_qa_scope.md) 从优化翻译与随机抽查中 **Pass**；后续抽查/改优默认不再跟这条线。