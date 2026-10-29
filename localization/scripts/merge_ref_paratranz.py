#!/usr/bin/env python3
"""Merge ParaTranz 参考翻译 into LawnStrings_zh.json (P0 + P1 only).

P0: same key, original == en, reference has CJK -> overwrite zh
P1: English text match, different key (e.g. achieve_* <-> ACHIEVE_*) -> write RFL key

Does not do P2 flavor merge or packaging.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF_PATH = ROOT / "参考翻译" / "utf8" / "LawnStrings-ParaTranz.json"
EN_PATH = ROOT / "LawnStrings_en.json"
ZH_PATH = ROOT / "LawnStrings_zh.json"
REPORT_PATH = ROOT / "ref_merge_report.json"

CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def has_cjk(s: str) -> bool:
    return bool(CJK_RE.search(s or ""))


def norm_cmp(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return (
        s.replace("\r\n", "\n")
        .replace("/r\n", "\n")
        .replace("\\r\\n", "\n")
        .replace("\r", "\n")
        .strip()
    )


def trailing_ws(s: str) -> tuple[str, str]:
    i = len(s)
    while i > 0 and s[i - 1] in "\n\r \t":
        i -= 1
    return s[:i], s[i:]


def normalize_translation(ref_t: str, en_val: str) -> str:
    """Fix /r\\n and align trailing whitespace to English."""
    t = ref_t.replace("/r\n", "\r\n").replace("/r", "\r")
    # If still literal backslash-r sequences from JSON oddities
    t = t.replace("\\r\\n", "\r\n")
    zb, _ = trailing_ws(t)
    _, et = trailing_ws(en_val if isinstance(en_val, str) else "")
    return zb + et


def is_technical(value: str) -> bool:
    if value.startswith("http://") or value.startswith("https://"):
        return True
    if value.startswith("@@BADCACHE:"):
        return True
    if value.endswith(".RTON") or value.endswith(".json"):
        return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ref_list = json.loads(REF_PATH.read_text(encoding="utf-8"))
    en: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))
    zh: dict[str, str] = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    ref = {x["key"]: x for x in ref_list}

    # en text -> list of RFL keys
    en_to_keys: dict[str, list[str]] = {}
    for k, v in en.items():
        if isinstance(v, str) and v.strip() and not is_technical(v):
            en_to_keys.setdefault(norm_cmp(v), []).append(k)

    p0_changed: list[dict] = []
    p0_same = 0
    skipped_en_mismatch: list[dict] = []
    skipped_empty = 0
    skipped_tech = 0

    for key, x in ref.items():
        if key not in zh or key not in en:
            continue
        o = x.get("original") or ""
        t = (x.get("translation") or "").strip()
        if not t:
            skipped_empty += 1
            continue
        if not has_cjk(t):
            continue
        if is_technical(en[key]) or is_technical(t):
            skipped_tech += 1
            continue
        if norm_cmp(o) != norm_cmp(en[key]):
            if len(skipped_en_mismatch) < 50:
                skipped_en_mismatch.append(
                    {
                        "key": key,
                        "ref_original": o[:120],
                        "en": en[key][:120] if isinstance(en[key], str) else en[key],
                    }
                )
            else:
                skipped_en_mismatch.append({"key": key})  # count via len; trim later
            continue
        new_v = normalize_translation(t, en[key])
        old = zh[key]
        if norm_cmp(old) == norm_cmp(new_v) and old == new_v:
            p0_same += 1
            continue
        if norm_cmp(old) == norm_cmp(new_v):
            # only whitespace/newline style diff
            zh[key] = new_v
            p0_changed.append({"key": key, "kind": "whitespace", "old": old, "new": new_v})
        else:
            zh[key] = new_v
            p0_changed.append(
                {
                    "key": key,
                    "kind": "overwrite",
                    "old": old[:160],
                    "new": new_v[:160],
                }
            )

    # Trim mismatch list samples
    mismatch_count = sum(1 for x in ref.values()
                         if x["key"] in en and x["key"] in zh
                         and (x.get("translation") or "").strip()
                         and has_cjk(x.get("translation") or "")
                         and norm_cmp(x.get("original") or "") != norm_cmp(en[x["key"]]))
    skipped_en_mismatch = [s for s in skipped_en_mismatch if "ref_original" in s][:30]

    # P1: alias by English text
    p1_changed: list[dict] = []
    # Build ref translations keyed by normalized original (prefer stage, then longer)
    ref_by_orig: dict[str, tuple[str, str]] = {}  # orig_norm -> (ref_key, translation)
    for x in ref_list:
        o = x.get("original") or ""
        t = (x.get("translation") or "").strip()
        if not o.strip() or not t or not has_cjk(t):
            continue
        on = norm_cmp(o)
        prev = ref_by_orig.get(on)
        if prev is None or (x.get("stage") or 0) >= 1:
            ref_by_orig[on] = (x["key"], t)

    p0_keys = {c["key"] for c in p0_changed}
    for on, (ref_key, t) in ref_by_orig.items():
        rfl_keys = en_to_keys.get(on)
        if not rfl_keys:
            continue
        for rk in rfl_keys:
            if rk == ref_key:
                continue  # would be P0 if aligned
            if rk in p0_keys:
                continue
            # If same key already handled as P0 with matching original, skip
            if rk in ref and norm_cmp(ref[rk].get("original") or "") == on:
                continue
            new_v = normalize_translation(t, en[rk])
            old = zh.get(rk, "")
            if norm_cmp(old) == norm_cmp(new_v):
                continue
            zh[rk] = new_v
            p1_changed.append(
                {
                    "rfl_key": rk,
                    "ref_key": ref_key,
                    "old": old[:160],
                    "new": new_v[:160],
                }
            )

    report = {
        "p0_overwrite": sum(1 for c in p0_changed if c["kind"] == "overwrite"),
        "p0_whitespace": sum(1 for c in p0_changed if c["kind"] == "whitespace"),
        "p0_unchanged_same": p0_same,
        "p0_samples": [c for c in p0_changed if c["kind"] == "overwrite"][:25],
        "p1_mapped": len(p1_changed),
        "p1_samples": p1_changed[:25],
        "skipped_en_mismatch_count": mismatch_count,
        "skipped_en_mismatch_samples": skipped_en_mismatch,
        "skipped_empty": skipped_empty,
        "skipped_tech": skipped_tech,
        "spotcheck": {
            k: zh.get(k)
            for k in (
                "STAT_RECHARGE",
                "STAT_SUNCOST",
                "STAT_TOUGHNESS",
                "STAT_SUNPROD",
                "SUNFLOWER",
                "SNOWPEA",
                "EGYPT",
                "COWBOY",
                "AKEE",
            )
        },
    }

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"P0 overwrite={report['p0_overwrite']} ws={report['p0_whitespace']} "
        f"same={p0_same} | P1={len(p1_changed)} | en_mismatch≈{mismatch_count}"
    )
    print("spotcheck", json.dumps(report["spotcheck"], ensure_ascii=False, indent=2))

    if args.dry_run:
        print("dry-run: zh not written")
        return

    ZH_PATH.write_text(
        json.dumps(zh, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {ZH_PATH}")
    print(f"wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
