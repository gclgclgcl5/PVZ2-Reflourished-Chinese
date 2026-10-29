# PvZ2 Reflourished 中文汉化

针对 **植物大战僵尸 2：返茂（Reflourished）1.4.2**（包名 `com.ea.game.pvz2_rfl`）的完整汉化工程。

- 联网后 UI / 图鉴 / 任务文案保持中文（APK 内 CDN 防覆盖补丁）
- 对话气泡可显示汉字（Packages 内字体兼容映射）
- 译文、脚本与逐步教程均在本仓库

返茂作者已声明允许汉化；**请勿用于商业倒卖**。

## 玩家：快速安装

需要三件套（与游戏版本一致）：

| 文件 | 说明 | 本仓库 |
|------|------|--------|
| `PvZ2_Reflourished_1.4.2_zh.apk` | 含 CDN 补丁的签名包 | **GitHub Releases**（约 48MB，未纳入 Git） |
| `LawnStrings-en-us.rton` | 中文文案（推到 CDN 目录） | [`release_zh/`](./release_zh/) |
| `main.675.com.ea.game.pvz2_rfl.obb` | 已替换中文 + 对话字体 | **约 1.3GB，未纳入 Git**（见下） |

### APK / OBB 如何获取

Git 仓库只保留可复现的源码与 CDN 用 RTON；大二进制请：

1. 打开本仓库 **[Releases](https://github.com/gclgclgcl5/PVZ2-Reflourished-Chinese/releases)** 下载 APK / OBB（若已发布）  
2. 或 **按教程本地生成**：[`localization/汉化教程.md`](./localization/汉化教程.md) 第 5–7 节  

安装摘要：

```powershell
adb install -r PvZ2_Reflourished_1.4.2_zh.apk
adb push main.675.com.ea.game.pvz2_rfl.obb /sdcard/Android/obb/com.ea.game.pvz2_rfl/main.675.com.ea.game.pvz2_rfl.obb
adb push release_zh\LawnStrings-en-us.rton /sdcard/Android/data/com.ea.game.pvz2_rfl/files/No_Backup/CDN.1.4.2/LawnStrings-en-us.rton
adb shell am start -n com.ea.game.pvz2_rfl/com.popcap.PvZ2.PvZ2GameActivity
```

成功标准：标题为「开始」、对话为汉字、联网不回英文。细节与排错见教程。

## 汉化者：从零复现

请直接阅读：

**[localization/汉化教程.md](./localization/汉化教程.md)**

覆盖：提取 LawnStrings、翻译/合并参考译、Sen 编 RTON、回封 Packages（zstd）、对话横杠修复、CDN SO 补丁、闪退踩坑等。

### 目录结构

```text
localization/          译文、脚本、教程
  LawnStrings_zh.json  中文文案
  scripts/             提取 / 回封 / CDN 补丁 / 对话字体
  汉化教程.md
release_zh/            发布物示例（APK + CDN RTON；OBB 需自备）
```

第三方工具 **Sen** 请自行从官网获取，勿依赖本仓库内本地 `tools/` 副本。

## 环境要点

- Python 3.10+（`pip install zstandard`）
- Sen（RTON / RSB）
- apktool、Android build-tools、JDK、adb
- 工作路径尽量短、无空格（如 `F:\sen_work`）

## 许可与声明

- 游戏与返茂模组版权归原作者所有  
- 本仓库脚本与教程以学习交流为目的提供  
- 参考译文（如 ParaTranz）版权归各自贡献者  

问题与改进欢迎开 Issue / PR。
