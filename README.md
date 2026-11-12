# PvZ2 Reflourished 中文汉化

针对 **植物大战僵尸 2：返茂（Reflourished）1.4.2**（包名 `com.ea.game.pvz2_rfl`）的完整汉化工程。

- 联网后 UI / 图鉴 / 任务保持中文（APK CDN 防覆盖）
- 对话多风格汉字（LoadingFonts 方案 A）
- LawnStrings RTON 自研编解码（日常不依赖第三方 RTON GUI）

返茂作者已声明允许汉化；**请勿用于商业倒卖**。

## 项目说明

本项目通过解析并重打包 OBB 中的文本（Packages）与字体（LoadingFonts）模块实现本地化。代码与脚本仅针对中文语言包的构建与复现，不提供通用全量资源解包功能。所有原版美术、音频及玩法版权归原团队所有，如原作方要求停止维护将随时下架。

---

## 玩家

→ **[用户安装.md](./用户安装.md)**（推荐单体 all-in-one）

发布包在 **[Releases](https://github.com/gclgclgcl5/PVZ2-Reflourished-Chinese/releases)**；CDN 用 RTON 示例在 [`release_zh/`](./release_zh/)。

---

## 维护者（我们）

→ **[localization/维护者工作流.md](./localization/维护者工作流.md)**

改译文 → 复刻 OBB/APK → 打 `release_zh/…_allinone.apk` 的固定流程与踩坑。  
RTON 细节：[localization/rton_selfhost_plan.md](./localization/rton_selfhost_plan.md)。

```powershell
# 只改文案后：
python localization\scripts\build_zh_rton.py

# 整条出包见维护者工作流 §2
```

### 目录

```text
用户安装.md              玩家傻瓜安装
localization/            译文、脚本、维护者文档
  LawnStrings_zh.json    唯一现行中文
  维护者工作流.md
  scripts/
release_zh/              发布物落地（all-in-one 默认产出）
out_zh/                  本机复刻产出（不进 Git）
```

---

## 环境要点

- Python 3.10+（`pip install zstandard`）
- apktool、Android build-tools、JDK、adb（打 APK / 一体包时）
- 方案 A 字体：`fonts_cjk`（见维护者工作流）

## 许可

游戏与返茂版权归原作者；本仓库脚本与文档供学习交流。参考译文版权归各自贡献者。
