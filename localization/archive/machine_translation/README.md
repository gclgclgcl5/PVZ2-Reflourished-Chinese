# 机翻归档（已停用）

本目录仅保留**历史机翻链路**与备份，**不得**再用于发布或覆盖现行译文。

## 现行唯一文案源

| 文件 | 说明 |
|------|------|
| `localization/LawnStrings_zh.json` | **唯一现行中文**（参考译合并 + 图鉴 STAT + 潘妮等） |
| `localization/current/` | 与现行一致的 JSON / Sen JSON / RTON / `almanac_stat_keys.json` 快照 |
| `localization/参考翻译/` | 人工/社区参考，用于审校与合并，不是机翻底 |

工作副本（短路径）：`F:\sen_work\current\`（与上表同步）。

## 这里有什么

| 路径 | 内容 |
|------|------|
| `data/LawnStrings_zh.json.bak_pre_refmerge` | 参考译合并前的机翻底 |
| `scripts/` | 术语表整库替换、分批机翻、glossary 重建等旧脚本 |
| `F:\sen_work\archive\machine_translation\` | 早期 `LawnStrings_sen_zh.json` 等 Sen/机翻产物 |

## 禁止事项

- 禁止用本目录或 `LawnStrings_sen_zh.json` **整库 encode** 覆盖 CDN / OBB  
- 禁止对现行库再跑 `apply_translation.py` / `run_full_translate.py`  
- 若需查旧词条，只读比对；改译文请直接编辑 `LawnStrings_zh.json` 后走教程 §4～§5.1.1  

## 若必须临时调用旧脚本

```powershell
cd F:\othergit\Reverse Engineer Anything\localization\archive\machine_translation\scripts
# 仅调试；输出不要写回 localization/LawnStrings_zh.json
```
