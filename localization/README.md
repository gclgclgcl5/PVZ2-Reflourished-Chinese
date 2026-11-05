# PvZ2 Reflourished 1.4.2 汉化工程

作者已声明允许汉化。本目录存放**现行文案**、脚本与教程。

## 完整教程

请先阅读：**[汉化教程.md](./汉化教程.md)**  
提取 → 翻译 → Sen 回封 → 图鉴属性 `[STAT_…]` → OBB/APK → CDN 防覆盖 → 安装验证。

## 现行文案（唯一启用）

| 路径 | 说明 |
|------|------|
| **`LawnStrings_zh.json`** | **唯一现行中文** |
| `LawnStrings_en.json` / `.rton` | 英文原文 |
| `almanac_stat_keys.json` | 图鉴属性新增 `[STAT_…]` → 中文 |
| `almanac_name_lock.json` | 植物/僵尸短名锁表 |
| `objective_keys.json` | 关卡目标 `[OBJ_…]` 键 |
| `current/` | 与现行一致的 JSON / Sen / RTON 快照，便于核对 |
| `fonts_src/` | 对话 CJK 字体源（重建 LoadingFonts 用） |

短路径工作副本：`F:\sen_work\current\`（与 `current/` 同步用途相同）。

**不要**再用机翻底或旧 `LawnStrings_sen_zh.json` 整库覆盖现行文件。

## 结论摘要

| 资源 | 作用 | 汉化重点 |
| --- | --- | --- |
| APK | 壳 UI + **`libPVZ2.so` CDN 补丁** | 联网不丢中文 |
| OBB `Packages` | LawnStrings×6 + 图鉴属性字面量 | 离线底包（**zstd**） |
| CDN `LawnStrings-en-us.rton` | 运行时优先文案 | 须与 OBB **同一份**现行 RTON |

- 包名：`com.ea.game.pvz2_rfl`
- 成品示例：仓库根目录 `release_zh/`；本机大包多在 `F:\sen_work\`

## 目录

| 路径 | 说明 |
|------|------|
| `scripts/` | 提取、回封、图鉴/目标字面量、CDN/字体、单体打包等 |
| `汉化教程.md` | 完整操作文档 |

### 改译文的正确流程

1. 只改 **`LawnStrings_zh.json`**  
2. Sen：decode/encode（Sen 格式 `LocStringValues`）→ `LawnStrings_zh.rton`  
3. `repack_obb_packages`；若动了属性字面量再跑 `patch_packages_almanac_literals.py --stat-refs`（§5.1.1）；若关卡目标正文仍英文再跑 `patch_packages_objective_literals.py`（§5.1.2）  
4. 推 OBB + **同步 CDN** → `force-stop` 验收；或 `build_allinone_apk.py` 打单体包  
