# 给翻译 AI 的说明（PvZ2 Reflourished LawnStrings）

风格细则见同目录 [`STYLE.md`](./STYLE.md)。

## 任务

将每个 `batch_XXX.json` 中的**英文 value**译为**简体中文**，并返回**相同结构**的 JSON：

```json
{
  "SOME_KEY": "中文译文"
}
```

- **Key 原样保留，禁止增删、改名；key 集合必须一致。**
- 只翻译字符串内容。

## 翻译规则（必须遵守）

1. **占位符原样保留**（含数量与顺序）：  
   `%s` `%d` `%1$s` `{0}` `{1}` `#` 以及成对的颜色/富文本标记等。  
2. **游戏指令原样保留**：`{SAY:…}` `{PLAYFUL:…}` `{NPC_ENTER:…}` 等对话/演出宏。  
3. **专有名词统一**：见 `STYLE.md` 与现行 `LawnStrings_zh.json` / `参考翻译`；机翻 glossary 已归档停用。  
4. **语气**：手游 UI 简洁自然；剧情可略口语，但不要过度网络烂梗。  
5. **空白与换行**：尽量保留原文 `\n` / `\r\n`。  
6. **不要翻译**：纯数字、技术 URL / `@@BADCACHE:` / `.RTON`、key 本身。

## 文件说明

| 文件 | 含义 |
|------|------|
| `manifest.json` | 总条目数、分批列表（**全量重导出**，覆盖旧混杂译文） |
| `batch_001.json` … | 待译英文原文 |
| `batch_XXX.zh.json` | 对应中文译文 |
| `remaining_keys.txt` | 全部待译 key 列表 |
| `STYLE.md` | 风格冻结 |

建议：**一次翻译 1 个 batch**，文件名用 `batch_001.zh.json`。

## 回导

```powershell
python localization\scripts\import_ai_translations.py localization\export_for_ai\batch_001.zh.json
```

或目录批量：

```powershell
python localization\scripts\import_ai_translations.py --dir localization\export_for_ai
```

## 辅助脚本

```powershell
python localization\scripts\export_all_for_ai.py
python localization\scripts\qa_translations.py
# 回导后请以 localization/LawnStrings_zh.json 为准继续维护
# translate_batches.py 等机翻脚本已停用（见 archive/machine_translation/）
```
