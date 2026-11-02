# 发布物说明

## 推荐：单体 all-in-one（最终用户）

| 文件 | 是否在 Git 中 | 说明 |
|------|----------------|------|
| `PvZ2_Reflourished_1.4.2_zh_allinone.apk` | **否**（约 1.3GB+） | 内嵌汉化 OBB + CDN 种子；系统直接安装；首次启动自动释放。本机产出：`F:\sen_work\PvZ2_Reflourished_1.4.2_zh_allinone.apk` |

用户步骤：卸载旧同包名 → 安装该 APK → 打开等释放完成即可。详见 `localization/汉化教程.md` §7.0。

构建：

```powershell
python localization\scripts\build_allinone_apk.py
```

## 分体包（开发 / adb 调试）

| 文件 | 是否在 Git 中 | 说明 |
|------|----------------|------|
| `PvZ2_Reflourished_1.4.2_zh.apk` | **否**（约 48MB） | 已打 CDN 补丁；需另推 OBB + CDN |
| `LawnStrings-en-us.rton` | 是 | 中文文案，安装后推到 CDN 目录 |
| `main.675.com.ea.game.pvz2_rfl.obb` | **否**（约 1.3GB） | 需按教程回封；完整图鉴请用 `main_schemeA_almanac.obb` |

推送路径见仓库根目录 `README.md` 与 `localization/汉化教程.md` 第 7 节。
