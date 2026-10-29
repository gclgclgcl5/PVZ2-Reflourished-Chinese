# PvZ2 Reflourished 汉化风格（冻结）

## 专名（权威）

- **第一权威**：`localization/参考翻译/utf8/LawnStrings-ParaTranz.json`（原版/社区 PvZ2 汉化，非返茂专表）。
- **现行成稿**：`localization/LawnStrings_zh.json`（唯一启用；改词请改这里）。
- 旧机翻术语表已归档：`localization/archive/machine_translation/scripts/glossary_*.py`（**勿再整库套用**）。
- 示例（以参考/现行为准）：上古埃及、狂野西部、炫光魔音游、冷却时间、阳光消耗、生命值、潘妮（勿写「朋朋」）等。

## 语气

- **UI / 按钮 / 提示**：短、直、无多余语气词。
- **剧情**：保留角色口吻。Crazy Dave（crazydave）略疯癫口语；Penny / Winnie 偏冷静书面。不要过度网络烂梗。

## 必须原样保留

- 占位符：`%s` `%d` `%1$s` `{0}` `{1}` `#` 等（数量与顺序不变）。
- 对话 / 演出宏：`{SAY:…}` `{PLAYFUL:…}` `{EXCITED:…}` `{TIRED:…}` `{NPC_ENTER:…}` 以及 `{KEYWORD}` `{STAT}` `{FLAVOR}` 等富文本标记。
- 换行：与英文对齐；参考里的 `/r\n` 导入时规范为 `\r\n`。
- 技术值：URL、`@@BADCACHE:`、`.RTON` / `.json` 文件名——不译。

## 合并优先级（文案）

1. **P0**：同 key 且参考 `original` ≡ 返茂英文 → 直接采用参考译文。  
2. **P1**：英文相同、key 不同（如 `achieve_*` ↔ `ACHIEVE_*`）→ 按英文映射写入返茂 key。  
3. **P2**（`merge_ref_p2.py`）：同 key 但英文已变 →  
   - 琐差异（大小写 / 标点 / 空白）：可覆盖；  
   - 图鉴 `*_DESCRIPTION`：**保留返茂中文数值前缀**（`{KEYWORD}`/`{STAT}`），仅替换参考 `{FLAVOR}`；  
   - HEADER 英文缩短而参考更完整：可采用参考全文；  
   - 剧情等英文重写过大：**不自动合并**。  
4. 参考没有的返茂独有句：保留现译，专名以新 glossary 为准。

## 禁止

- 中英夹杂整句（如「向日葵 are very important…」）。
- 翻译或删改宏标签本身。
- 用已废弃的旧官中 glossary 回灌，把参考译名改回去。
- 用短语表对已整句参考译文再次全文替换污染。
