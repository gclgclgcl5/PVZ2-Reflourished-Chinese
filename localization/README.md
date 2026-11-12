# localization — 文案与脚本

作者已声明允许汉化。本目录存放**现行文案**、脚本与**维护者**文档。

项目定位见仓库根目录 [README.md](../README.md#项目说明)。

## 先读哪篇

| 读者 | 文档 |
|------|------|
| 玩家 | [用户安装.md](../用户安装.md) |
| **我们** | **[维护者工作流.md](./维护者工作流.md)** |
| RTON 实现 | [rton_selfhost_plan.md](./rton_selfhost_plan.md) |

旧「汉化教程 / 复刻最短路径」已拆并，仅留跳转页。

## 现行文案（唯一启用）

| 路径 | 说明 |
|------|------|
| **`LawnStrings_zh.json`** | **唯一现行中文** |
| `LawnStrings_en.json` / `.rton` | 英文原文 |
| `almanac_stat_keys.json` | 图鉴 `[STAT_…]` |
| `almanac_name_lock.json` | 植物/僵尸短名锁表 |
| `objective_keys.json` | 关卡 `[OBJ_…]` |
| `fonts_src/` → `fonts_cjk/` | 方案 A 多字体（可本地生成，大文件不进 Git） |
| `current/` | 现行 JSON / RTON 快照 |

**不要**用旧机翻底整库覆盖现行文件。

## 产物落点

| 路径 | 说明 |
|------|------|
| `../release_zh/` | 发布物；`build_allinone_apk.py` 默认输出 |
| `../out_zh/` | `reproduce_zh*` 默认输出 |

## 改译文最短动作

1. 只改 **`LawnStrings_zh.json`**
2. `python localization/scripts/build_zh_rton.py`
3. 按 [维护者工作流.md](./维护者工作流.md) 决定：只推 CDN，还是重打 OBB / 一体包
