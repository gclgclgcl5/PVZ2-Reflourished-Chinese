# 史诗任务 TITLE 全量回炉记录

范围：全部 `EPIC_QUEST_*_TITLE`（295）+ 同品牌 `LEVEL_NAME` / `PLAYERS_EPIC_QUEST_*`（合计展示面 336 键）。  
只改 ZH：`localization/LawnStrings_zh.json` + `localization/current/LawnStrings_zh.json`。EN / 宏未动；未 encode。

权威：`STYLE.md`、`almanac_name_lock.json`。对照导出：`F:\sen_work\epic_quest_titles_full\`。

## 批次落地

| 批次 | 族 | 脚本 |
|------|-----|------|
| A+B | RIFT / ALTVERZ / GEMJAM / ALOE / ELECTRICCURRANT / GOLDBLOOM / GIRA / PARODY / METEORZ | `_apply_epic_quest_titles_batch_ab.py` |
| C | EIGHTIES 复检 + TORCHWOOD / HERPLE / SHADOWLURKERS / TTTB / POOLPARTY / PICKLEDPEPPER | `_apply_epic_quest_titles_batch_c.py` |
| D | BEGHOULED + 短链 / 单关 / 高级种子包等余量 | `_apply_epic_quest_titles_batch_d.py` |
| E | 验收针 | `_verify_epic_quest_titles.py` |

## 质量冻结（已按此过目）

1. 语义对齐 EN；习语中文重建（drill / jams / lit / mosh pit / close and personal / literally / bring the heat 等）
2. 专名跟锁表：钢地刺、孢子菇、莲小蓬、忧郁藤蔓、夜影龙葵、复活萝卜、超能花菜、流星Z、强化瓷砖、宝石迷阵 等；禁英文残留
3. 短标题口语/任务口吻；勿公文「您」、勿丧尸/充值
4. 宏 `{LEVEL_NUMBER}` `{PLAYER}` 原样
5. 同族 TITLE / LEVEL_NAME / PLAYERS 品牌名一致

## 验收（批 E）

- keys **336**；TITLE-ish **295**
- root / current **desync 0**
- 坏译针（堵塞、演习、狂欢坑、字面上地、带来热量、莲花荚、地刺王、保存那些、近距离接触、Boosting Tiles、Begholed/Beghouled、Meteor Z、充值、任务小鬼僵尸、Weather Warz、宝尸迷阵、增强僵尸…）**清零**
- 英文单词残留（排除宏 / 流星Z）**清零**
- 宏集合 EN↔ZH **mismatch 0**

## 样板品牌（复检保留或回炉后）

- EIGHTIES：赠曲痛殴！
- METEORZ：他们来到了流星Z！
- ELECTRICCURRANT：电气布加洛！
- BEGHOULED：宝石迷阵闪电战！
- PICKLEDPEPPER：泡在麻烦里！
- HERPLE：不可能的小鬼任务！
- TORCHWOOD RFL：燃起来！
- POOLPARTY：后院水花大战！
- TTTB：它们已经尽力了！

## 明确未做

- `NARRATIVE_EPIC_QUEST_*` 对白（另账本）
- 史诗领域 / 非 `EPIC_QUEST_` 主线标题
- encode / 打包 / 装扮名
