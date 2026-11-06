#!/usr/bin/env python3
"""Sync flat LawnStrings_zh.json with sen order + STAT_/OBJ_ extras."""
from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from pathlib import Path

from lawnstrings_rton import (
    decode_rton_pairs,
    merge_extra_keys,
    pairs_to_sen_json,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FLAT = ROOT / "LawnStrings_zh.json"
DEFAULT_CURRENT = ROOT / "current"
DEFAULT_RTON = DEFAULT_CURRENT / "LawnStrings_zh.rton"
DEFAULT_SEN = DEFAULT_CURRENT / "LawnStrings_zh_sen.json"
DEFAULT_STAT = ROOT / "almanac_stat_keys.json"
DEFAULT_OBJ = ROOT / "objective_keys.json"


def _load_map(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"expected object in {path}")
    return {str(k): str(v) for k, v in data.items()}


def sync(
    *,
    flat_path: Path = DEFAULT_FLAT,
    current_dir: Path = DEFAULT_CURRENT,
    order_from_rton: Path | None = DEFAULT_RTON,
    order_from_sen: Path | None = DEFAULT_SEN,
    stat_path: Path = DEFAULT_STAT,
    obj_path: Path = DEFAULT_OBJ,
) -> list[tuple[str, str]]:
    flat = _load_map(flat_path)

    order_pairs: list[tuple[str, str]] = []
    if order_from_rton and order_from_rton.is_file():
        order_pairs = decode_rton_pairs(order_from_rton)
    elif order_from_sen and order_from_sen.is_file():
        sen = json.loads(order_from_sen.read_text(encoding="utf-8"))
        vals = sen["objects"][0]["objdata"]["LocStringValues"]
        order_pairs = [(vals[i], vals[i + 1]) for i in range(0, len(vals), 2)]
    else:
        order_pairs = list(flat.items())

    # Skeleton order from RTON/sen; overlay flat values.
    items: list[tuple[str, str]] = []
    seen: set[str] = set()
    for k, old_v in order_pairs:
        v = flat.get(k, old_v)
        items.append((k, v))
        seen.add(k)
    for k, v in flat.items():
        if k not in seen:
            items.append((k, v))
            seen.add(k)

    items = merge_extra_keys(items, _load_map(stat_path), _load_map(obj_path))

    # Dual-write flat (dedup last-wins) + current snapshots.
    dedup = OrderedDict(items)
    flat_text = json.dumps(dedup, ensure_ascii=False, indent="\t") + "\n"
    flat_path.write_text(flat_text, encoding="utf-8")

    current_dir.mkdir(parents=True, exist_ok=True)
    (current_dir / "LawnStrings_zh.json").write_text(flat_text, encoding="utf-8")

    sen = pairs_to_sen_json(items)
    if order_from_sen and order_from_sen.is_file():
        # Preserve unrelated template fields if any by reusing aliases/objclass only.
        pass
    (current_dir / "LawnStrings_zh_sen.json").write_text(
        json.dumps(sen, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"sync ok: ordered_pairs={len(items)} flat_keys={len(dedup)} "
        f"-> {flat_path.name} + {current_dir}"
    )
    return items


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--flat", type=Path, default=DEFAULT_FLAT)
    ap.add_argument("--current", type=Path, default=DEFAULT_CURRENT)
    ap.add_argument("--rton", type=Path, default=DEFAULT_RTON)
    ap.add_argument("--sen", type=Path, default=DEFAULT_SEN)
    ap.add_argument("--stat", type=Path, default=DEFAULT_STAT)
    ap.add_argument("--obj", type=Path, default=DEFAULT_OBJ)
    args = ap.parse_args()
    sync(
        flat_path=args.flat,
        current_dir=args.current,
        order_from_rton=args.rton,
        order_from_sen=args.sen,
        stat_path=args.stat,
        obj_path=args.obj,
    )


if __name__ == "__main__":
    main()
