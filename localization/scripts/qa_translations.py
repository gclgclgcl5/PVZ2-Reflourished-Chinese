#!/usr/bin/env python3
"""QA LawnStrings_zh.json against LawnStrings_en.json."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = ROOT / "LawnStrings_en.json"
ZH_PATH = ROOT / "LawnStrings_zh.json"

PLACEHOLDER_RE = re.compile(
    r"%\d*\$?[sd]|%\d+\$[sd]|\{[0-9]+\}|(?<!\{)#(?!\})"
)
# Capture brace macros like {SAY:winnie} {KEYWORD} {STAT} …
MACRO_RE = re.compile(r"\{[A-Za-z_][^}]*\}")
LATIN_WORD_RE = re.compile(r"[A-Za-z]{3,}")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def is_technical(value: str) -> bool:
    if value.startswith("http://") or value.startswith("https://"):
        return True
    if value.startswith("@@BADCACHE:"):
        return True
    if value.endswith(".RTON") or value.endswith(".json"):
        return True
    return False


def is_intentional_english(key: str, value: str) -> bool:
    """Values that should remain English / symbolic after full localization."""
    if is_technical(value):
        return True
    if not value.strip():
        return True
    if value.strip() in {"$", ",", "3", "1", "2", "60+", "A.K.E.E.", "OK", "HP"}:
        return True
    if value.startswith("^") and value.endswith("^"):
        return True
    if value in {"{LEVEL}", "{tutorial}"} or value.startswith("??"):
        return True
    if "TEST" in key.upper() or key.startswith("PLAYERSEGMENT_TEST"):
        return True
    # Puzzle / cipher lines (reversed text, base64)
    if "SPONGEBOB_22_INTRO_5" in key or "SPONGEBOB_22_INTRO_7" in key:
        return True
    if "SPONGEBOB_22_INTRO_8" in key or "SPONGEBOB_22_INTRO_9" in key:
        return True
    # Skin codes / brand-like short names intentionally kept
    if key in {
        "product_cost_electriccurrant_skin_3l3ctro_name",
        "product_cost_redstinger_skin_edgest_name",
        "COLOR_FLAVOR",
        "COLOR_KEYWORD",
        "COLOR_STAT",
        "CURRENCY_SYMBOL",
        "NUMBER_FORMAT_SEPARATOR",
        "NUMBER_FORMAT_SEPARATOR_COUNT",
        "AGE_GATE_OLD",
    }:
        return True
    stripped = MACRO_RE.sub("", value).strip()
    if not stripped:
        return True
    if not re.search(r"[A-Za-z]{3,}", stripped):
        return True
    return False


def placeholder_bag(s: str) -> list[str]:
    return PLACEHOLDER_RE.findall(s)


def macro_bag(s: str) -> list[str]:
    return MACRO_RE.findall(s)


def strip_macros(s: str) -> str:
    return MACRO_RE.sub("", s)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", type=Path, default=ROOT / "qa_report.json")
    ap.add_argument("--mixed-limit", type=int, default=200)
    args = ap.parse_args()

    en: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))
    zh: dict[str, str] = json.loads(ZH_PATH.read_text(encoding="utf-8"))

    still_english: list[str] = []
    intentional_still: list[str] = []
    mixed: list[dict] = []
    ph_mismatch: list[dict] = []
    macro_mismatch: list[dict] = []
    crlf_flattened: list[str] = []
    missing_keys: list[str] = []

    for k, ev in en.items():
        if k not in zh:
            missing_keys.append(k)
            continue
        zv = zh[k]
        if is_technical(ev):
            continue
        if zv == ev:
            if is_intentional_english(k, ev):
                intentional_still.append(k)
            else:
                still_english.append(k)
            continue
        # Multiset compare: Chinese word order may move placeholders/macros.
        if Counter(placeholder_bag(ev)) != Counter(placeholder_bag(zv)):
            ph_mismatch.append({"key": k, "en": placeholder_bag(ev), "zh": placeholder_bag(zv)})
        if Counter(macro_bag(ev)) != Counter(macro_bag(zv)):
            macro_mismatch.append({"key": k, "en": macro_bag(ev), "zh": macro_bag(zv)})
        if "\r\n" in ev and "\r\n" not in zv and "\n" in zv:
            crlf_flattened.append(k)
        stripped = strip_macros(zv)
        if CJK_RE.search(stripped) and LATIN_WORD_RE.search(stripped):
            # Allow short kept tokens like OK, HP, PVZ if few; flag denser mixes.
            latin_words = LATIN_WORD_RE.findall(stripped)
            if len(latin_words) >= 2 or (len(latin_words) == 1 and len(latin_words[0]) >= 6):
                if len(mixed) < args.mixed_limit:
                    mixed.append({"key": k, "sample": zv[:160]})

    report = {
        "total_en": len(en),
        "still_english_actionable_count": len(still_english),
        "still_english_actionable_sample": still_english[:100],
        "intentional_still_english_count": len(intentional_still),
        "intentional_still_english_sample": intentional_still[:100],
        "missing_keys": missing_keys,
        "placeholder_mismatch_count": len(ph_mismatch),
        "placeholder_mismatch_sample": ph_mismatch[:50],
        "macro_mismatch_count": len(macro_mismatch),
        "macro_mismatch_sample": macro_mismatch[:50],
        "crlf_flattened_count": len(crlf_flattened),
        "crlf_flattened_sample": crlf_flattened[:50],
        "mixed_suspect_count_capped": len(mixed),
        "mixed_suspect_sample": mixed,
    }
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"QA written to {args.report}\n"
        f"  still_english_actionable: {report['still_english_actionable_count']}\n"
        f"  intentional_still_english: {report['intentional_still_english_count']}\n"
        f"  placeholder_mismatch: {report['placeholder_mismatch_count']}\n"
        f"  macro_mismatch: {report['macro_mismatch_count']}\n"
        f"  crlf_flattened: {report['crlf_flattened_count']}\n"
        f"  mixed_suspect (capped): {report['mixed_suspect_count_capped']}"
    )


if __name__ == "__main__":
    main()
