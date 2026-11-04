# 图鉴 AI 汉化批次（宝开语）

## 必读

1. [`BAOKAI.md`](BAOKAI.md) — 宝开语风格与分层规则  
2. [`almanac_name_lock.json`](almanac_name_lock.json) — **冻结**的植物/僵尸短名（勿改）  
3. 上级 [`STYLE.md`](../STYLE.md)  
4. [`PILOT_REVIEW.md`](PILOT_REVIEW.md) — 试点验收清单

## 作业顺序

1. 读 [`PILOT_REVIEW.md`](PILOT_REVIEW.md)；在种子稿 `almanac_pilot.zh.json` 上按宝开语重写 `{FLAVOR}`  
2. 校验：`python localization\scripts\qa_almanac_baokai.py localization\export_for_ai\almanac\almanac_pilot.zh.json`  
3. 通过后再译 `almanac_001.json` … `almanac_003.json` 全量批次  

英文源批次不含短名 key；正文提到单位时必须使用锁表中文名。

## 回导

```powershell
python localization\scripts\qa_almanac_baokai.py localization\export_for_ai\almanac\almanac_001.zh.json
python localization\scripts\import_ai_translations.py localization\export_for_ai\almanac\almanac_001.zh.json
```

`almanac_current_zh_subset.json` 是现行中文对照，**不要**当授权参考成稿整段粘贴。

`almanac_stat_already_zh.json` 是无英文源、已有中文的截断 STAT 标签，不在 AI 英文批次里。
