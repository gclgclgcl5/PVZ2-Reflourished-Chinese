# PvZ2 Reflourished 1.4.2 汉化工程

作者已声明允许汉化。本目录存放**现行文案**、脚本与教程。

## 完整教程

请先阅读：**[汉化教程.md](./汉化教程.md)**  
提取 → 翻译 → Sen 回封 → 图鉴属性 `[STAT_…]` → OBB/APK → CDN 防覆盖 → 安装验证。

## 现行文案（唯一启用）

| 路径 | 说明 |
|------|------|
| **`LawnStrings_zh.json`** | **唯一现行中文**（参考译优化 + 图鉴 STAT 键 + 潘妮等） |
| `LawnStrings_en.json` / `.rton` | 英文原文 |
| `almanac_stat_keys.json` | 图鉴属性新增 `[STAT_…]` → 中文 |
| `current/` | 与现行一致的 JSON / Sen 格式 / RTON 快照，便于核对 |
| `参考翻译/` | 社区/人工参考，审校合并用 |

短路径工作副本：`F:\sen_work\current\`（与 `current/` 同步用途相同）。

**不要**再用机翻底或 `LawnStrings_sen_zh.json` 整库覆盖现行文件。机翻已归档：见 [`archive/machine_translation/`](./archive/machine_translation/README.md)。

## 结论摘要

| 资源 | 作用 | 汉化重点 |
| --- | --- | --- |
| APK | 壳 UI + **`libPVZ2.so` CDN 补丁** | 联网不丢中文 |
| OBB `Packages` | LawnStrings×6 + 图鉴属性字面量 | 离线底包（**zstd**） |
| CDN `LawnStrings-en-us.rton` | 运行时优先文案 | 须与 OBB **同一份**现行 RTON |

- 包名：`com.ea.game.pvz2_rfl`
- 现行键数见 `LawnStrings_zh.json` / `progress.json`（约 2.6 万+）

## 目录

| 路径 | 说明 |
|------|------|
| `scripts/` | **现行**工具：提取、合并参考译、回封、图鉴属性、CDN/字体补丁 |
| `export_for_ai/` | 分批审校用英文/译文（人工或外部 AI）；回导用 `import_ai_translations.py` |
| `archive/machine_translation/` | **已停用**机翻脚本与备份 |
| `archive/early_reports/` | 早期合并报告等 |
| `汉化教程.md` | 完整操作文档 |

成品示例见仓库根目录 `release_zh/`。

### 改译文的正确流程

1. 只改 **`LawnStrings_zh.json`**（或改 `export_for_ai/*.zh.json` 后 `import_ai_translations.py`）  
2. Sen：decode/encode（Sen 格式 `LocStringValues`）→ `LawnStrings_zh.rton`  
3. `repack_obb_packages`；若动了属性字面量再跑 `patch_packages_almanac_literals.py --stat-refs`（§5.1.1）  
4. 推 OBB + **同步 CDN** → `force-stop` 验收  

**已停用**（调用会直接退出）：`apply_translation.py`、`run_full_translate.py`、`translate_batches.py`。

## 当前进度

- [x] 提取 LawnStrings、参考译合并、QA  
- [x] Sen 编回 RTON、回封 OBB（zstd）+ 方案 A 对话字体  
- [x] APK CDN 防覆盖；CDN 推送现行中文  
- [x] 图鉴常见属性 `[STAT_…]`（可继续扩表）  
- [x] 「朋朋」→「潘妮」  
- [ ] 图鉴短标签/范围值补全、叙事英文残留清理（见验收结论）
