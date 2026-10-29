#!/usr/bin/env python3
"""P2 merge: same-key entries where ref.original ≠ RFL English.

P2a — trivial diffs (case / punct / whitespace / orig substring of en)
P2b — keep RFL Chinese stats prefix, replace {FLAVOR} from reference
P2c — DESCRIPTION_HEADER where en is shorter than orig → use reference
Skip — rewritten narrative / other

Does not package RTON/OBB.
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
REPORT_PATH = ROOT / "ref_merge_p2_report.json"

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
MACRO_RE = re.compile(r"\{[A-Za-z_][^}]*\}")
KEYWORD_LINE = re.compile(r"^\{KEYWORD\}")
STAT_LINE = re.compile(r"^\{STAT\}")


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


def to_lf(s: str) -> str:
    return (
        s.replace("\r\n", "\n")
        .replace("/r\n", "\n")
        .replace("\\r\\n", "\n")
        .replace("\r", "\n")
    )


def trailing_ws(s: str) -> tuple[str, str]:
    i = len(s)
    while i > 0 and s[i - 1] in "\n\r \t":
        i -= 1
    return s[:i], s[i:]


def normalize_translation(text: str, en_val: str) -> str:
    t = text.replace("/r\n", "\r\n").replace("/r", "\r")
    t = t.replace("\\r\\n", "\r\n")
    # Prefer CRLF for multi-line game strings when en uses CRLF
    if "\r\n" in (en_val or "") or "\n" in to_lf(en_val or ""):
        t_lf = to_lf(t)
        if "\r\n" in (en_val or ""):
            t = t_lf.replace("\n", "\r\n")
        else:
            t = t_lf
    zb, _ = trailing_ws(t)
    _, et = trailing_ws(en_val if isinstance(en_val, str) else "")
    return zb + et


def is_technical(value: str) -> bool:
    if not isinstance(value, str):
        return True
    if value.startswith("http://") or value.startswith("https://"):
        return True
    if value.startswith("@@BADCACHE:"):
        return True
    if value.endswith(".RTON") or value.endswith(".json"):
        return True
    return False


def macro_kinds(s: str) -> set[str]:
    kinds: set[str] = set()
    for m in MACRO_RE.findall(s or ""):
        name = m[1:].split(":", 1)[0].split("}", 1)[0].strip().upper()
        if name in {"KEYWORD", "STAT", "FLAVOR"}:
            kinds.add(name)
    return kinds


def split_prefix_flavor(text: str) -> tuple[str, str, str]:
    """Return (prefix, flavor, kind) where kind is tag|prose|none|all.

    prefix excludes trailing blank lines; flavor includes {FLAVOR} when present.
    """
    if not isinstance(text, str) or not text:
        return "", "", "none"
    t = to_lf(text)
    idx = t.find("{FLAVOR}")
    if idx >= 0:
        pre = t[:idx].rstrip("\n")
        flav = t[idx:]
        return pre, flav, "tag"

    lines = t.split("\n")
    i = 0
    saw_kw = False
    while i < len(lines):
        line = lines[i]
        if KEYWORD_LINE.match(line) or STAT_LINE.match(line) or line.strip() == "":
            if KEYWORD_LINE.match(line) or STAT_LINE.match(line):
                saw_kw = True
            i += 1
            continue
        break
    if saw_kw and i < len(lines):
        pre = "\n".join(lines[:i]).rstrip("\n")
        flav = "\n".join(lines[i:])
        return pre, flav, "prose"
    return "", t, "all"


def extract_ref_flavor(ref_t: str, prefer_tag: bool) -> str:
    """Take flavor portion from reference; strip any KEYWORD/STAT block."""
    t = to_lf(ref_t).replace("/r\n", "\n").replace("/r", "")
    idx = t.find("{FLAVOR}")
    if idx >= 0:
        return t[idx:].strip()
    pre, flav, kind = split_prefix_flavor(t)
    if kind in {"tag", "prose"} and flav.strip():
        body = flav.strip()
        if not body.startswith("{FLAVOR}") and prefer_tag:
            return "{FLAVOR}" + body
        return body
    body = t.strip()
    # Strip leading keyword blocks if any remain
    pre2, flav2, kind2 = split_prefix_flavor(body)
    if kind2 in {"prose", "tag"} and flav2.strip():
        body = flav2.strip()
    if prefer_tag and not body.startswith("{FLAVOR}"):
        return "{FLAVOR}" + body
    return body


def classify(orig: str, en: str) -> str:
    e_n, o_n = norm_cmp(en), norm_cmp(orig)
    if not e_n or not o_n:
        return "other"
    if o_n + "!" == e_n or o_n == e_n + "!":
        return "punct_only"
    if o_n.lower() == e_n.lower():
        return "case_only"
    if re.sub(r"\s+", " ", o_n) == re.sub(r"\s+", " ", e_n):
        return "whitespace_only"
    if "{FLAVOR}" in o_n and "{FLAVOR}" in e_n and o_n in e_n:
        return "flavor_suffix_in_en"
    if "{FLAVOR}" in o_n and "{FLAVOR}" in e_n:
        return "both_flavor_diff"
    if "{KEYWORD}" in e_n and "{FLAVOR}" not in o_n and "{FLAVOR}" in e_n:
        return "en_added_stats_ref_flavor_only"
    if o_n and o_n in e_n:
        return "orig_substring_of_en"
    if e_n and e_n in o_n:
        return "en_substring_of_orig"
    # en has stats+flavor, ref orig is prose without flavor tag but matches flavor body
    if "{FLAVOR}" in e_n:
        _, en_flav, _ = split_prefix_flavor(en)
        flav_body = en_flav.replace("{FLAVOR}", "", 1).strip()
        if o_n and flav_body and (o_n in flav_body or flav_body in o_n or o_n[:40] in flav_body):
            return "en_added_stats_ref_flavor_only"
    return "other"


def is_trivial_substring(orig: str, en: str) -> bool:
    """orig is substring of en with only light extras (punct / trailing words)."""
    o_n, e_n = norm_cmp(orig), norm_cmp(en)
    if not o_n or o_n not in e_n:
        return False
    # Allow en = orig + punctuation / short suffix
    rest = e_n.replace(o_n, "", 1).strip()
    if rest == "" or rest in {".", "!", "?", "...", "…"}:
        return True
    if len(rest) <= 3 and not has_cjk(rest):
        return True
    # Also: only whitespace/nbsp differences already caught elsewhere
    return False


def splice_flavor(en: str, zh_cur: str, ref_t: str) -> str | None:
    en_pre, en_flav, en_kind = split_prefix_flavor(en)
    zh_pre, _zh_flav, zh_kind = split_prefix_flavor(zh_cur)

    prefer_tag = "{FLAVOR}" in en or en_kind == "tag"
    # Need a stats/prefix situation or at least flavor slot in en
    if en_kind == "all" and "{KEYWORD}" not in en and "{FLAVOR}" not in en:
        return None

    if zh_pre and "{KEYWORD}" in zh_pre:
        prefix = zh_pre
    elif en_pre and ("{KEYWORD}" in en_pre or en_kind in {"tag", "prose"}):
        # Fall back: keep English prefix only if zh has no stats — prefer zh if any KEYWORD
        prefix = zh_pre if "{KEYWORD}" in (zh_cur or "") else en_pre
        # If zh has keyword somewhere but split failed oddly, try again
        if "{KEYWORD}" in (zh_cur or "") and not (zh_pre and "{KEYWORD}" in zh_pre):
            # use zh everything before flavor
            zpre, _, zk = split_prefix_flavor(zh_cur)
            if zpre and "{KEYWORD}" in zpre:
                prefix = zpre
    else:
        prefix = zh_pre or en_pre

    ref_flav = extract_ref_flavor(ref_t, prefer_tag=prefer_tag)
    if not ref_flav.strip():
        return None

    if prefix.strip():
        merged = prefix.rstrip("\n") + "\n\n" + ref_flav.lstrip("\n")
    else:
        merged = ref_flav

    merged = normalize_translation(merged, en)

    # Validate macro kinds: keep KEYWORD/STAT from en if present
    en_kinds = macro_kinds(en)
    out_kinds = macro_kinds(merged)
    for need in ("KEYWORD", "STAT"):
        if need in en_kinds and need not in out_kinds:
            return None
    if "FLAVOR" in en_kinds and "FLAVOR" not in out_kinds and prefer_tag:
        # allow prose flavor without tag only if en also prose
        if en_kind == "tag":
            return None
    return merged


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ref_list = json.loads(REF_PATH.read_text(encoding="utf-8"))
    en: dict[str, str] = json.loads(EN_PATH.read_text(encoding="utf-8"))
    zh: dict[str, str] = json.loads(ZH_PATH.read_text(encoding="utf-8"))

    p2a: list[dict] = []
    p2b: list[dict] = []
    p2c: list[dict] = []
    skipped_other: list[dict] = []
    skipped_failed: list[dict] = []

    for x in ref_list:
        key = x["key"]
        if key not in en or key not in zh:
            continue
        o = x.get("original") or ""
        t = (x.get("translation") or "").strip()
        if not t or not has_cjk(t):
            continue
        if is_technical(en[key]) or is_technical(t):
            continue
        if norm_cmp(o) == norm_cmp(en[key]):
            continue  # P0 territory

        cat = classify(o, en[key])
        old = zh[key]

        # P2a
        if cat in {"case_only", "punct_only", "whitespace_only"} or (
            cat == "orig_substring_of_en" and is_trivial_substring(o, en[key])
        ):
            new_v = normalize_translation(t, en[key])
            if norm_cmp(old) != norm_cmp(new_v) or old != new_v:
                zh[key] = new_v
                p2a.append({"key": key, "cat": cat, "old": old[:120], "new": new_v[:120]})
            continue

        # P2c — longer HEADER from reference
        if cat == "en_substring_of_orig" and (
            "DESCRIPTION_HEADER" in key or key.endswith("_HEADER")
        ):
            new_v = normalize_translation(t, en[key])
            if norm_cmp(old) != norm_cmp(new_v):
                zh[key] = new_v
                p2c.append({"key": key, "old": old[:120], "new": new_v[:120]})
            continue

        # P2b — flavor splice for description-like / stats+flavor
        if cat in {
            "flavor_suffix_in_en",
            "both_flavor_diff",
            "en_added_stats_ref_flavor_only",
        } or (
            cat == "other"
            and ("_DESCRIPTION" in key)
            and ("{KEYWORD}" in en[key] or "{FLAVOR}" in en[key])
        ):
            # Only auto-splice when en has structure we understand
            if "{KEYWORD}" in en[key] or "{FLAVOR}" in en[key]:
                merged = splice_flavor(en[key], old, t)
                if merged is None:
                    skipped_failed.append(
                        {"key": key, "cat": cat, "reason": "splice_failed"}
                    )
                    continue
                if norm_cmp(old) != norm_cmp(merged):
                    zh[key] = merged
                    p2b.append(
                        {
                            "key": key,
                            "cat": cat,
                            "old": old[:140],
                            "new": merged[:140],
                        }
                    )
                continue

        # Also try P2b for orig_substring when it's a DESCRIPTION with stats
        if (
            cat == "orig_substring_of_en"
            and "_DESCRIPTION" in key
            and ("{KEYWORD}" in en[key] or "{FLAVOR}" in en[key])
        ):
            merged = splice_flavor(en[key], old, t)
            if merged is not None and norm_cmp(old) != norm_cmp(merged):
                zh[key] = merged
                p2b.append({"key": key, "cat": cat, "old": old[:140], "new": merged[:140]})
                continue
            if not is_trivial_substring(o, en[key]):
                skipped_other.append(
                    {
                        "key": key,
                        "cat": cat,
                        "en": en[key][:100],
                        "ref": t[:100],
                    }
                )
                continue

        skipped_other.append(
            {
                "key": key,
                "cat": cat,
                "en": (en[key][:100] if isinstance(en[key], str) else ""),
                "ref": t[:100],
            }
        )

    spot_keys = [
        "AKEE_DESCRIPTION",
        "ALOE_DESCRIPTION",
        "ZOMBIE_PROSPECTOR_DESCRIPTION",
        "BUTTON_CANCEL",
        "PINATA_PARTY_SPROUT_REWARD_TEXT",
    ]
    report = {
        "p2a_count": len(p2a),
        "p2b_count": len(p2b),
        "p2c_count": len(p2c),
        "skipped_other_count": len(skipped_other),
        "skipped_failed_count": len(skipped_failed),
        "p2a_samples": p2a[:20],
        "p2b_samples": p2b[:20],
        "p2c_samples": p2c[:20],
        "skipped_other_samples": skipped_other[:30],
        "skipped_failed_samples": skipped_failed[:20],
        "spotcheck": {k: zh.get(k, "")[:220] for k in spot_keys},
    }

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"P2a={len(p2a)} P2b={len(p2b)} P2c={len(p2c)} "
        f"skip_other={len(skipped_other)} skip_fail={len(skipped_failed)}"
    )
    for k in spot_keys:
        v = zh.get(k, "")
        print(f"  {k}: {v[:100]!r}...")

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
