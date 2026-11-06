# LawnStrings RTON 自研说明

**状态：已落地。** 日常编解码使用本仓库脚本，不依赖第三方 RTON GUI。

## 入口

| 脚本 | 作用 |
|------|------|
| [`scripts/lawnstrings_rton.py`](./scripts/lawnstrings_rton.py) | LawnStrings 专用 RTON decode / encode |
| [`scripts/sync_lawnstrings.py`](./scripts/sync_lawnstrings.py) | 按 RTON 键序合并扁平文案 + `STAT_` / `OBJ_` |
| [`scripts/build_zh_rton.py`](./scripts/build_zh_rton.py) | 一键 sync → encode → 可选 Packages repack / release 复制 |
| [`scripts/tests/test_lawnstrings_rton.py`](./scripts/tests/test_lawnstrings_rton.py) | Roundtrip / 槽位 / 抽样测试 |

```powershell
cd localization\scripts
python build_zh_rton.py
python -m unittest localization.scripts.tests.test_lawnstrings_rton -v
```

## 格式要点（1.4.2）

- 头：`RTON` + version `01 00 00 00`；尾：`DONE`
- 根对象字段：`objects`（LawnStringsData）+ `version`（`0x24` uvarint）
- `LocStringValues`：交替 key/value；字符串用 **`0x90` / `0x91`** 单池（UTF-8 字节，含中文）
- 槽位上限：`LAWNSTRINGS_SLOT = 2666496`（见 `repack_obb_packages.py`）

权威文案：[`LawnStrings_zh.json`](./LawnStrings_zh.json)。  
完整装包流程见 [汉化教程.md](./汉化教程.md)。

## 规格参考（可选阅读）

实现时对照过公开 RTON 说明与开源编解码（算法自写，未整段拷贝 GPL 源码），例如：

- [h3x4n1um/RETON](https://github.com/h3x4n1um/RETON)（opcode 速查）
- [nineteendo/pyvz2](https://github.com/nineteendo/pyvz2)、[LambdaEd1th/serde_rton](https://github.com/LambdaEd1th/serde_rton)

OBB Packages / LoadingFonts 仍用本仓库既有 **zstd 原地槽补丁**，与 RTON 脚本无关。
