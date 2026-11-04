# 史诗领域 TITLE 回炉记录（ICEAGE）

触发：`EPIC_REALM_ICEAGE_STEP_19_TITLE`（「非传统的游戏计划 / 痛苦的环境」）机翻抽查。

## 范围

- `EPIC_REALM_ICEAGE_STEP_1_TITLE` … `STEP_20_TITLE`（20）
- 同品牌：`EPIC_REALM_ICEAGE_TITLE`、`LEVEL_NAME`、`PLAYERS_EPIC_REALM_ICEAGE`、`UNLOCK_EPIC_REALM_ICEAGE_TITLE` / `_DESC`
- 只改 ZH：`localization/LawnStrings_zh.json` + `localization/current/LawnStrings_zh.json`
- EN / 宏未改；未 encode
- **不做**：`NARRATIVE_EPIC_REALM_*`（见 [`epic_realm_narrative_findings.md`](epic_realm_narrative_findings.md)）；其它领域无步进 TITLE

权威：`STYLE.md`、`almanac_name_lock.json`（火草、辣椒投手、低温空洞、极寒冰窟、僵王）。

## 质量冻结

对齐史诗任务 TITLE：习语中文重建、短标题任务口吻、专名锁表、同族品牌「低温空洞」一致。

## 落地

- 脚本：`F:\sen_work\_apply_epic_realm_iceage_titles_zh.py`
- 变更 **25** 键（20 STEP + 5 品牌/解锁）
- 样例：`STEP_19` → **换套路硬刚这要命地形！**
- PLAYERS「低温洞穴」→ **低温空洞**

## 验收

坏译针（游戏计划、非传统、痛苦的环境、投掷双手、重定向、游手好闲、落后一两分、以毒攻毒、低温洞穴、充值、英文残留）在本范围 **清零**；root / current **desync 0**；宏 EN↔ZH 一致。

## 仍可后续

- （UNLOCK / WORLD_PREVIEW / 商店钥匙品牌已于同轮抛光，见下）

## 补记：领域解锁/预览介绍

- 触发：`UNLOCK_EPIC_REALM_ICEAGE_DESC`「时光已让极寒冰窟元气大伤」机翻腔
- 已改：四域 `UNLOCK_*_DESC`、`WORLD_PREVIEW_DESCRIPTION_*`、商店 `product_epicrealm_*`、奖励屏钥匙文案；临时 `EPIC_REALM_*_DESCRIPTION`；品牌统一低温空洞 / 月虹市场 / 空中求援信号 / 《恶意仙境》/ 史诗领域
