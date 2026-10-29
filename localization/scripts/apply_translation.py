"""Apply glossary + phrase rules to LawnStrings_zh.json and report progress."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from glossary_pvz2 import apply_phrases, build_exact_map  # noqa: E402

EN_PATH = ROOT / "LawnStrings_en.json"
ZH_PATH = ROOT / "LawnStrings_zh.json"
PROGRESS_PATH = ROOT / "progress.json"


def looks_chinese(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def should_keep_english(key: str, value: str) -> bool:
    if value.startswith("http://") or value.startswith("https://"):
        return True
    if value.startswith("@@BADCACHE:"):
        return True
    if value.startswith("{SAY:"):
        # Narrative dialogue — phrase-replace inside later
        return False
    if key.startswith("NARRATIVE_") and value.isupper() and "_" in value:
        # Likely another key reference
        return True
    if value.endswith(".RTON") or value.endswith(".json"):
        return True
    return False


def translate_value(key: str, value: str, exact: dict[str, str]) -> str:
    if should_keep_english(key, value):
        return value
    if value in exact:
        return exact[value]
    # Key-based overrides for common buttons stored as keys themselves
    key_ui = {
        "#OF#": "# / #",
        "ACCOUNT_DELETION": "删除账号",
        "ACCOUNT_DELETION_BUTTON_CANCEL": "取消",
        "ACCOUNT_DELETION_BUTTON_DELETE": "删除",
        "ACCOUNT_DELETION_BUTTON_OK": "确定",
        "ACCOUNT_DELETION_FAILURE_TITLE": "错误",
        "ACCOUNT_DELETION_SUCCESS_TITLE": "账号已删除",
        "ACCOUNT_DELETION_YES_NO_TITLE_A": "删除我的账号",
        "ACCOUNT_DELETION_YES_NO_TITLE_B": "此操作无法撤销！",
    }
    if key in key_ui:
        return key_ui[key]

    phrased = apply_phrases(value)
    if phrased != value:
        return phrased
    return value


def categorize(key: str) -> str:
    ku = key.upper()
    if "ZOMBIE" in ku:
        return "zombie"
    if any(x in ku for x in ("PLANT_", "_PLANT", "SEED_", "ALMANAC_PLANT")):
        return "plant"
    if any(
        x in ku
        for x in (
            "BUTTON",
            "MENU",
            "DIALOG",
            "SETTINGS",
            "OPTIONS",
            "TITLE",
            "LOADING",
            "ERROR",
            "TAP_",
            "TOUCH_",
            "CONTINUE",
            "PAUSE",
            "STORE",
            "SHOP",
            "ALMANAC",
            "QUEST",
            "DAILY",
        )
    ):
        return "ui"
    if ku.startswith("NARRATIVE_") or "{SAY:" in key:
        return "narrative"
    return "other"


def main() -> None:
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    exact = build_exact_map()
    zh: dict[str, str] = {}
    stats = {"ui": 0, "plant": 0, "zombie": 0, "narrative": 0, "other": 0}
    changed = 0
    for k, v in en.items():
        t = translate_value(k, v, exact)
        zh[k] = t
        if t != v:
            changed += 1
            stats[categorize(k)] += 1

    ZH_PATH.write_text(json.dumps(zh, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = {
        "total_keys": len(en),
        "changed_from_english": changed,
        "remaining_english": len(en) - changed,
        "changed_by_category": stats,
        "pct_changed": round(100.0 * changed / len(en), 2),
    }
    PROGRESS_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
