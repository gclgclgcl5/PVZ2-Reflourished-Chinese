#!/usr/bin/env python3
"""Export Almanac (plant/zombie encyclopedia) strings for AI translation.

Reads LawnStrings_en.json, writes batches under export_for_ai/almanac/:
  almanac_001.json …   English source {KEY: en} (no short display names)
  almanac_name_lock.json  Frozen plant/zombie short names from LawnStrings_zh
  almanac_pilot.json      Small sample for style QA before full batches
  manifest.json
  keys.txt
  README.md

Also writes almanac_current_zh_subset.json (current zh for the same keys)
so you can compare; AI should translate from the English batches only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = ROOT / "LawnStrings_en.json"
ZH_PATH = ROOT / "LawnStrings_zh.json"
STAT_KEYS_PATH = ROOT / "almanac_stat_keys.json"
OUT_DIR = ROOT / "export_for_ai" / "almanac"

# Fewer, larger batches so AI import is easier (≈4 batches for full almanac)
TARGET_ENTRIES = 750
CHAR_BUDGET = 160000
PILOT_DESCRIPTION_LIMIT = 40
CJK_RE = re.compile(r"[\u4e00-\u9fff]")

# UI / quest / store noise that also ends with _DESCRIPTION
SKIP_PREFIXES = (
    "ACCOUNT_",
    "ADVICE_",
    "AWARD_",
    "AGE_",
    "APP_",
    "APPLY_",
    "FEATURE_",
    "MTX_",
    "PRODUCT_",
    "product_",
    "NARRATIVE_",
    "LTE_EVENTS_",
    "LTE_REPLAY_",
    "LTE_LEVEL_",
    "PERSISTENT_",
    "OFFLINE_",
    "JOUST_",
    "DAILY_",
    "COMMUNITY_",
    "COLLECT_",
    "DEFEAT_",
    "FINISH_",
    "PLAY_",
    "UNLOCK_",
    "WARNING_",
    "FAILED_",
    "CREDITS_",
    "LOADING",
    "QUEST_",
    "EPIC_QUEST_",
    "EPIC_REALM_",
    "RIFT_",
    "WORLDMAP_",
    "WORLD_PREVIEW_",
    "WORLD_NAME_",
    "PINATA_",
    "BOOST_",
    "POWERUP_",
    "MUTATOR_",
    "ACHIEVEMENT_",
    "achieve_",
    "STARCHALLENGE_",
    "OBJECTIVE_",
    "CHOOSER_",
    "DEFAULT_",
    "COLOR_",
    "NOTIFICATION_",
    "FACEBOOK_",
    "STORE_",
    "IAP_",
    "PURCHASE_",
    "SUBSCRIPTION_",
    "PROFILE_",
    "SETTINGS_",
    "HELP_",
    "ERROR_",
    "COMMON_",
    "GENERIC_",
    "HUD_",
    "MAP_",
    "TRAVELLOG_",
    "PENNY_",
    "DANGER_ROOM_",
    "PROGRESS_",
    "FIRST_CLEAR_",
    "GARDEN_",
    "ZEN_",
    "MAIL_",
    "INBOX_",
    "NEWS_",
    "CALENDAR_",
    "EVENT_CALENDAR_",
    "THYMED_",
    "LOD_",
    "VASEBREAKER_",
    "CANNON_",
    "SURVIVE_",
    "WIN_",
    "CLICK_",
    "CDN_",
    "SUGGEST_",
    "TUTORIAL_",
    "HOW_TO_",
    "HOWTO_",
    "POPUP_",
    "DIALOG_",
    "MODAL_",
    "TIP_",
    "TOOLTIP_GENERIC_",
    "LOCAL_NOTE_",
    "PUSH_",
    "RATE_",
    "UPDATE_",
    "LEGAL_",
    "PRIVACY_",
    "TERMS_",
    "CONNECT_",
    "NETWORK_",
    "DOWNLOAD_",
    "RETRY_",
    "PROGRESS_",
    "SOCIAL_",
    "LEADERBOARD_",
    "TOURNAMENT_",
    "REPLAY_",
    "SCHEDULED_",
    "REPEATABLE_",
)


def should_skip_value(value: str) -> bool:
    if not isinstance(value, str) or not value.strip():
        return True
    if value.startswith(("http://", "https://", "@@BADCACHE:")):
        return True
    if value.endswith((".RTON", ".json")):
        return True
    return False


def has_encyclopedia_siblings(key: str, en: dict[str, str]) -> bool:
    return (
        f"{key}_DESCRIPTION" in en
        or f"{key}_DESCRIPTION_HEADER" in en
        or f"{key}_TOOLTIP" in en
    )


def is_short_display_name(key: str, en: dict[str, str]) -> bool:
    """Plant/zombie short name keys — frozen, not AI-translated."""
    if key.startswith(SKIP_PREFIXES):
        return False
    if not has_encyclopedia_siblings(key, en):
        return False
    if key.endswith(("_DESCRIPTION", "_DESCRIPTION_HEADER", "_TOOLTIP")):
        return False
    if key.startswith(("ALMANAC_", "STAT_", "[STAT_")):
        return False
    if re.fullmatch(r"[A-Z][A-Z0-9]*", key):
        return True
    if key.startswith("ZOMBIE_") and key.count("_") <= 4:
        return True
    return False


def is_almanac_key(key: str, en: dict[str, str]) -> bool:
    if key.startswith("ALMANAC_"):
        return True
    if key.startswith("STAT_") or key.startswith("[STAT_"):
        return True
    if key.startswith(SKIP_PREFIXES):
        return False

    if key.endswith(("_DESCRIPTION", "_DESCRIPTION_HEADER", "_TOOLTIP")):
        if key.startswith("ZOMBIE_"):
            return True
        head = key.split("_")[0]
        if head in {
            "CDN",
            "SUGGEST",
            "TUTORIAL",
            "DIALOG",
            "POPUP",
            "UPDATE",
            "CONNECT",
            "NETWORK",
            "DOWNLOAD",
            "SOCIAL",
            "LEGAL",
            "PRIVACY",
            "TERMS",
            "RATE",
            "PUSH",
            "LOCAL",
            "MAIL",
            "INBOX",
            "NEWS",
            "ERROR",
            "HELP",
            "SETTINGS",
            "PROFILE",
            "STORE",
            "IAP",
        }:
            return False
        return True

    if is_short_display_name(key, en):
        return True

    return False


def build_name_lock(en: dict[str, str], zh: dict[str, str]) -> dict[str, str]:
    """Frozen short display names from current zh (fallback to en if missing)."""
    lock: dict[str, str] = {}
    for k in sorted(en.keys()):
        if not is_short_display_name(k, en):
            continue
        zv = zh.get(k)
        if isinstance(zv, str) and zv.strip():
            lock[k] = zv
        else:
            ev = en.get(k)
            if isinstance(ev, str) and ev.strip():
                lock[k] = ev
    return lock


def main() -> None:
    en: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))
    zh: dict[str, str] = {}
    if ZH_PATH.is_file():
        zh = json.loads(ZH_PATH.read_text(encoding="utf-8"))

    name_lock = build_name_lock(en, zh)

    selected: dict[str, str] = {}
    locked_out: list[str] = []
    for k, v in sorted(en.items()):
        if should_skip_value(v):
            continue
        if CJK_RE.search(v):
            continue
        if not is_almanac_key(k, en):
            continue
        # Short names stay in lock file only — never in AI EN batches
        if is_short_display_name(k, en):
            locked_out.append(k)
            continue
        selected[k] = v

    skipped_stat_zh: dict[str, str] = {}
    if STAT_KEYS_PATH.is_file():
        extra = json.loads(STAT_KEYS_PATH.read_text(encoding="utf-8"))
        for k, v in extra.items():
            if not isinstance(v, str):
                continue
            en_v = en.get(k)
            if (
                isinstance(en_v, str)
                and en_v.strip()
                and not CJK_RE.search(en_v)
                and k not in selected
                and not is_short_display_name(k, en)
            ):
                selected[k] = en_v
            elif k not in selected:
                skipped_stat_zh[k] = zh.get(k, v)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in OUT_DIR.glob("almanac_*.json"):
        if p.name.endswith(".zh.json"):
            continue
        p.unlink()
    for stale in ("almanac_pilot.json", "almanac_name_lock.json"):
        sp = OUT_DIR / stale
        if sp.is_file() and stale == "almanac_pilot.json":
            sp.unlink()

    batches: list[dict] = []
    cur: dict[str, str] = {}
    cur_chars = 0
    batch_idx = 1

    def flush() -> None:
        nonlocal cur, cur_chars, batch_idx
        if not cur:
            return
        name = f"almanac_{batch_idx:03d}.json"
        (OUT_DIR / name).write_text(
            json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        keys = list(cur.keys())
        batches.append(
            {
                "file": name,
                "entries": len(cur),
                "chars": cur_chars,
                "first_key": keys[0],
                "last_key": keys[-1],
            }
        )
        batch_idx += 1
        cur = {}
        cur_chars = 0

    for k, v in selected.items():
        if cur and (
            len(cur) >= TARGET_ENTRIES
            or (cur_chars + len(v) > CHAR_BUDGET and len(cur) >= 40)
        ):
            flush()
        cur[k] = v
        cur_chars += len(v)
    flush()

    # Pilot: first N *_DESCRIPTION keys (+ sibling HEADER/TOOLTIP when present)
    pilot: dict[str, str] = {}
    desc_count = 0
    for k, v in selected.items():
        if not k.endswith("_DESCRIPTION") or k.endswith("_DESCRIPTION_HEADER"):
            continue
        if desc_count >= PILOT_DESCRIPTION_LIMIT:
            break
        base = k[: -len("_DESCRIPTION")]
        for suffix in ("_DESCRIPTION", "_DESCRIPTION_HEADER", "_TOOLTIP"):
            sk = base + suffix
            if sk in selected and sk not in pilot:
                pilot[sk] = selected[sk]
        desc_count += 1
    (OUT_DIR / "almanac_pilot.json").write_text(
        json.dumps(pilot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (OUT_DIR / "almanac_name_lock.json").write_text(
        json.dumps(name_lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    zh_subset = {k: zh[k] for k in selected if k in zh}
    (OUT_DIR / "almanac_current_zh_subset.json").write_text(
        json.dumps(zh_subset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if skipped_stat_zh:
        (OUT_DIR / "almanac_stat_already_zh.json").write_text(
            json.dumps(skipped_stat_zh, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    (OUT_DIR / "keys.txt").write_text("\n".join(selected.keys()) + "\n", encoding="utf-8")

    manifest = {
        "purpose": "Almanac encyclopedia strings for AI Chinese translation (宝开语)",
        "source_en": str(EN_PATH.name),
        "total_keys": len(selected),
        "batch_count": len(batches),
        "name_lock_keys": len(name_lock),
        "name_lock_file": "almanac_name_lock.json",
        "short_names_excluded_from_batches": len(locked_out),
        "pilot_file": "almanac_pilot.json",
        "pilot_entries": len(pilot),
        "style_guide": "BAOKAI.md",
        "skipped_already_zh_stat_keys": len(skipped_stat_zh),
        "skipped_stat_file": "almanac_stat_already_zh.json" if skipped_stat_zh else None,
        "format": (
            'Each almanac_XXX.json is { "KEY": "English" }. '
            "Return the SAME keys with Simplified Chinese values as almanac_XXX.zh.json."
        ),
        "rules": [
            "Keep placeholders and tags: {KEYWORD} {STAT} {FLAVOR} {SAY:...} %s {COUNT} etc.",
            "Do not add/remove/rename keys.",
            "Translate from English batches only; ignore unauthorized third-party packs.",
            "Preserve \\r\\n line breaks when present.",
            "Short display names are LOCKED in almanac_name_lock.json — not in EN batches; do not invent new names.",
            "Follow BAOKAI.md: rewrite {FLAVOR} in 宝开语; HEADER light 宝开语; TOOLTIP functional.",
            "Batches contain English from LawnStrings_en only; already-Chinese STAT tokens are excluded.",
        ],
        "batches": batches,
    }
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    readme = """# 图鉴 AI 汉化批次（宝开语）

## 必读

1. [`BAOKAI.md`](BAOKAI.md) — 宝开语风格与分层规则  
2. [`almanac_name_lock.json`](almanac_name_lock.json) — **冻结**的植物/僵尸短名（勿改）  
3. 上级 [`STYLE.md`](../STYLE.md)
4. [`PILOT_REVIEW.md`](PILOT_REVIEW.md) — 试点验收清单

## 作业顺序

1. 读 `PILOT_REVIEW.md`；在种子稿 `almanac_pilot.zh.json` 上按宝开语重写 `{FLAVOR}`  
2. 校验：`python localization\\scripts\\qa_almanac_baokai.py localization\\export_for_ai\\almanac\\almanac_pilot.zh.json`  
3. 通过后再译 `almanac_001.json` … 全量批次  

英文源批次不含短名 key；正文提到单位时必须使用锁表中文名。

## 回导

```powershell
python localization\\scripts\\qa_almanac_baokai.py localization\\export_for_ai\\almanac\\almanac_001.zh.json
python localization\\scripts\\import_ai_translations.py localization\\export_for_ai\\almanac\\almanac_001.zh.json
```

`almanac_current_zh_subset.json` 是现行中文对照，**不要**当授权参考成稿整段粘贴。

`almanac_stat_already_zh.json` 是无英文源、已有中文的截断 STAT 标签，不在 AI 英文批次里。
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    print(
        f"exported {len(selected)} almanac keys -> {len(batches)} batches in {OUT_DIR}\n"
        f"  name_lock: {len(name_lock)} short names\n"
        f"  pilot: {len(pilot)} keys ({desc_count} entities)\n"
        f"  excluded short names from batches: {len(locked_out)}"
    )


if __name__ == "__main__":
    main()
