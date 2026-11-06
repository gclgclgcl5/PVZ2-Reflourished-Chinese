# 发布物目录

本目录是**成品落地**（大 APK/OBB 默认不进 Git，见仓库 `.gitignore`）。

## 给玩家

安装说明：**[用户安装.md](../用户安装.md)**（推荐单体 all-in-one）。

| 文件 | 是否进 Git | 说明 |
|------|------------|------|
| `PvZ2_Reflourished_1.4.2_zh_allinone.apk` | 否（约 1.3GB+） | 内嵌 OBB + CDN；系统直接安装 |
| `LawnStrings-en-us.rton` | 可 | 分体 / CDN 种子 |
| `PvZ2_Reflourished_1.4.2_zh.apk` | 否 | 分体用小 APK |
| `main.675….obb` | 否 | 分体 / 打一体包的输入 |

## 给我们

构建步骤：**[localization/维护者工作流.md](../localization/维护者工作流.md)** §2-D。

```powershell
python localization\scripts\build_allinone_apk.py
# 默认产出本目录 PvZ2_Reflourished_1.4.2_zh_allinone.apk
```
