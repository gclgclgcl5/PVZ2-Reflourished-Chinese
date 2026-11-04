#!/usr/bin/env python3
"""Build almanac_00N.zh.json from LawnStrings_zh + name lock.

- Prefer current Chinese when macros match EN.
- Apply almanac_name_lock English→Chinese replacements (longest first).
- Keep symbolic STAT values (1x3, ???) as-is.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "export_for_ai" / "almanac"
EN_PATH = ROOT / "LawnStrings_en.json"
ZH_PATH = ROOT / "LawnStrings_zh.json"
LOCK_PATH = OUT / "almanac_name_lock.json"
MACRO_RE = re.compile(r"\{[A-Za-z_][^}]*\}")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")

# Common EN leftovers in flavor not covered by short-name keys
EXTRA_REPLACEMENTS = [
    ("Crazy Dave", "疯狂戴夫"),
    ("Dr. Zomboss", "僵王博士"),
    ("Zomboss", "僵王博士"),
    ("Dave", "戴夫"),
    # Known wrong Chinese variants vs name lock
    ("酸液柠檬", "强酸柠檬"),
]


def macros(s: str) -> list[str]:
    return sorted(MACRO_RE.findall(s))


def apply_lock(text: str, pairs: list[tuple[str, str]]) -> str:
    out = text
    for en_name, zh_name in pairs:
        if not en_name or en_name == zh_name:
            continue
        if en_name not in out:
            continue
        # word-ish boundaries: don't eat longer Latin tokens
        parts: list[str] = []
        i = 0
        while True:
            pos = out.find(en_name, i)
            if pos < 0:
                parts.append(out[i:])
                break
            before = out[pos - 1] if pos > 0 else ""
            after_i = pos + len(en_name)
            after = out[after_i] if after_i < len(out) else ""
            # Only Latin letters count as name-token boundaries (CJK may abut names)
            left_ok = not before or not re.match(r"[A-Za-z]", before)
            right_ok = not after or not re.match(r"[A-Za-z]", after)
            parts.append(out[i:pos])
            if left_ok and right_ok:
                parts.append(zh_name)
            else:
                parts.append(en_name)
            i = after_i
        out = "".join(parts)
    return out


def main() -> None:
    en_full = json.loads(EN_PATH.read_text(encoding="utf-8"))
    zh_full = json.loads(ZH_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    pairs: list[tuple[str, str]] = []
    for k, zh_name in lock.items():
        en_name = en_full.get(k)
        if isinstance(en_name, str) and isinstance(zh_name, str) and en_name.strip():
            pairs.append((en_name, zh_name))
    # longest English names first
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    pairs.extend(EXTRA_REPLACEMENTS)

    for batch_name in ("almanac_001", "almanac_002", "almanac_003"):
        en_batch = json.loads((OUT / f"{batch_name}.json").read_text(encoding="utf-8"))
        out: dict[str, str] = {}
        used_zh = 0
        patched = 0
        for k, ev in en_batch.items():
            zv = zh_full.get(k)
            if isinstance(zv, str) and zv.strip() and macros(ev) == macros(zv):
                text = zv
                used_zh += 1
            elif isinstance(zv, str) and zv.strip() and CJK_RE.search(zv):
                # macro drift: still prefer Chinese body
                text = zv
                used_zh += 1
            else:
                # symbolic / missing — keep EN (1x3, ???)
                text = ev
            new = apply_lock(text, pairs)
            if new != text:
                patched += 1
            out[k] = new
        path = OUT / f"{batch_name}.zh.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{batch_name}: {len(out)} keys, from_zh={used_zh}, name_patched={patched} -> {path.name}")


if __name__ == "__main__":
    main()
