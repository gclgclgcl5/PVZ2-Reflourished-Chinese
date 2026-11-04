# -*- coding: utf-8 -*-
"""LTE QA scope: pass old events with no LTE_REPLAY_* entry."""
from __future__ import annotations

import re
from typing import Iterable, Mapping, Set, Tuple

REPLAY_RE = re.compile(r"^LTE_REPLAY_([A-Z0-9]+)_(\d{2})_DESC$")
NARR_LTE_RE = re.compile(r"^NARRATIVE_LTE_(\d{4})_\d{2}_([A-Z0-9]+)_")
LEVEL_YEAR_RE = re.compile(r"^LTE_LEVEL_NAME_([A-Z0-9]+)_(\d{4})$")
# other dated LTE UI crumbs, e.g. leftover year tags
LTE_YEAR_TAIL_RE = re.compile(r"^LTE_.*_(\d{4})$")


def replay_allowlist(en_map: Mapping[str, object]) -> Set[Tuple[str, int]]:
    allow: Set[Tuple[str, int]] = set()
    for k in en_map:
        m = REPLAY_RE.match(k)
        if not m:
            continue
        fam, yy = m.group(1), m.group(2)
        allow.add((fam, 2000 + int(yy)))
    return allow


def lte_family_year(key: str) -> Tuple[str, int] | None:
    m = NARR_LTE_RE.match(key)
    if m:
        return m.group(2), int(m.group(1))
    m = LEVEL_YEAR_RE.match(key)
    if m:
        return m.group(1), int(m.group(2))
    return None


def is_lte_out_of_scope(key: str, en_map: Mapping[str, object] | None = None, allow: Set[Tuple[str, int]] | None = None) -> bool:
    """True = pass / exclude from translation QA optimization."""
    fy = lte_family_year(key)
    if fy is None:
        return False
    if allow is None:
        if en_map is None:
            raise ValueError("en_map or allow required")
        allow = replay_allowlist(en_map)
    return fy not in allow


def filter_in_scope(keys: Iterable[str], en_map: Mapping[str, object]) -> list[str]:
    allow = replay_allowlist(en_map)
    return [k for k in keys if not is_lte_out_of_scope(k, allow=allow)]


if __name__ == "__main__":
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    en = json.loads((root / "LawnStrings_en.json").read_text(encoding="utf-8"))
    allow = sorted(replay_allowlist(en))
    print("allow", len(allow))
    for item in allow:
        print(" ", item)
    narr = [k for k in en if k.startswith("NARRATIVE_LTE_")]
    out = sum(1 for k in narr if is_lte_out_of_scope(k, allow=set(allow)))
    print(f"NARRATIVE_LTE total={len(narr)} out_of_scope={out} in_scope={len(narr)-out}")
