# PvZ2 Reflourished 1.4.2 汉化工程

作者已声明允许汉化。本目录存放文案、脚本与教程。

## 完整教程

请先阅读：**[汉化教程.md](./汉化教程.md)**  
从提取 → 翻译 → Sen 回封 → OBB/APK → **CDN 防覆盖补丁** → 安装验证，可独立复现。

## 结论摘要

| 资源 | 作用 | 汉化重点 |
| --- | --- | --- |
| APK | 壳 UI + **`libPVZ2.so` CDN 补丁** | 联网不丢中文的关键 |
| OBB `Packages` | `LawnStrings*.rton` ×6 | 离线/资源底包（**zstd**） |
| CDN `LawnStrings-en-us.rton` | 运行时优先文案 | 需推送中文版，并由 SO 补丁保护 |

- 包名：`com.ea.game.pvz2_rfl`
- 文案约 **26637** 条（`LocStringValues`）
- 旧 zlib 工具无法安全回封本版 OBB

## 目录

| 路径 | 说明 |
|------|------|
| `LawnStrings_en.json` / `.rton` | 英文原文 |
| `LawnStrings_zh.json` | 中文译文（进行中） |
| `progress.json` | 翻译进度统计 |
| `scripts/extract_lawnstrings.py` | RTON → JSON |
| `scripts/apply_translation.py` | 术语表批量应用 |
| `scripts/patch_cdn_lawnstrings_skip.py` | 打 CDN 防覆盖补丁 |
| `scripts/repack_obb_packages.py` | 替换 Packages 内 LawnStrings 并 zstd |
| `汉化教程.md` | 完整操作文档 |
| `export_for_ai/` | **待译英文分批导出**（交给专门 AI） |
| `scripts/import_ai_translations.py` | 把 AI 译文 JSON 合并回 `LawnStrings_zh.json` |

成品示例见仓库根目录 `release_zh/`。

### 待译文本（给外部 AI）

已导出约 **19369** 条未译英文到 `export_for_ai/batch_001.json` … `batch_025.json`。  
说明见 `export_for_ai/README_给翻译AI.md`。译完后：

```powershell
python localization\scripts\import_ai_translations.py --dir localization\export_for_ai
```

（文件名需为 `*.zh.json` / `batch_XXX.zh.json` 等，详见该 README。）

## 当前进度

- [x] 提取 LawnStrings、术语表与高频 UI/单位名
- [x] Sen 编回 RTON、回封 OBB（zstd）
- [x] APK CDN 防覆盖补丁，联网保持中文
- [x] 全量整句汉化 `LawnStrings_zh.json`（见 `progress.json` / `qa_report.json`）
- [ ] encode RTON → 回封 OBB → 验证安装（另开阶段）

全量重译流程：`export_all_for_ai.py` → 分批 `.zh.json` → `import_ai_translations.py` → `qa_translations.py`。  
**不要**再对整库跑 `apply_translation.py` 短语替换，以免污染已整句译文。
