# 试点验收清单（宝开语）

文件：`almanac_pilot.json`（英）→ `almanac_pilot.zh.json`（中）

当前 `almanac_pilot.zh.json` 已用现行 `LawnStrings_zh.json` **种子填充**（114 键齐全），供对照；验收目标是按 [`BAOKAI.md`](BAOKAI.md) **重写 `{FLAVOR}` / 轻改 HEADER**，并保持锁表专名。

## 验收项

- [ ] 短名未改（对照 `almanac_name_lock.json`；批次内本无短名 key）
- [ ] `{KEYWORD}` / `{STAT}` / `{FLAVOR}` 宏与换行仍在
- [ ] `{FLAVOR}` 有拟人、冷幽默、反转，而非说明书腔
- [ ] HEADER 短、有人设；TOOLTIP 仍是功能短句
- [ ] 正文专名与锁表一致（如「强酸柠檬」而非 Acid Lemon）

## 命令

```powershell
python localization\scripts\qa_almanac_baokai.py localization\export_for_ai\almanac\almanac_pilot.zh.json
# 通过后再决定是否 import；全量译 almanac_001～003
```

试点通过后：按同样规则译 `almanac_001.json` … `almanac_003.json`。
