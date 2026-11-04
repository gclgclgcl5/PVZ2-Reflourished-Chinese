# LTE 汉化优化 / 抽查范围（冻结）

## 规则

**只优化、只抽查「玩家当前仍能进」的限时活动**：以 `LawnStrings` 里存在的 `LTE_REPLAY_{FAMILY}_{YY}_DESC` 为白名单。

- 允许：`NARRATIVE_LTE_{20YY}_*_{FAMILY}_*`，且 `(FAMILY, 20YY)` 出现在某条 `LTE_REPLAY_*` 中  
- 允许：带年份的关卡名等，同白名单年份（如 `LTE_LEVEL_NAME_HEROES_2024`）  
- **Pass（不做优化 / 不进随机审阅池）**：无对应 `LTE_REPLAY` 的往届 LTE（例：`NARRATIVE_LTE_2023_11_HEROES_*`、`…_2023_11_FOODFIGHT_*`、`…_2023_04_ALTVERZ_*`，以及 2024 无重温条目的旧届等）

非 LTE（主线、史诗任务/领域、图鉴、UI、装扮等）**不受本规则排除**。

## 工具

- 随机审阅：[`../qa_random_review.html`](../qa_random_review.html) 载入 EN 后按 `LTE_REPLAY_*` 自动过滤  
- 脚本辅助：[`../scripts/lte_qa_scope.py`](../scripts/lte_qa_scope.py)（`is_lte_out_of_scope(key, en_map)`）

## 维护

新一届活动若已进游戏但尚未加 `LTE_REPLAY_*` 文案，抽查会暂时 Pass——补上 REPLAY 键后自动重新纳入。白名单以 **现行 EN 包**为准，勿手写死年份表。
