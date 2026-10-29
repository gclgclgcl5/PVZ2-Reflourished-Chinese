# -*- coding: utf-8 -*-
"""Emit batch_033 chunk *.zh.json files."""
import importlib.util
import json
from pathlib import Path

CHUNK_DIR = Path(__file__).resolve().parent


def load_hand():
    spec = importlib.util.spec_from_file_location("hand", CHUNK_DIR / "_write_batch_033_zh.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.T


def load_json(name: str) -> dict:
    return json.loads((CHUNK_DIR / name).read_text(encoding="utf-8"))


def main():
    hand = load_hand()
    extra = load_json("batch_033_p02_p05_zh.json")

    stems = [f"batch_033_p{i:02d}" for i in range(6)]
    for stem in stems:
        src = load_json(f"{stem}.json")
        if stem in hand:
            tr = dict(hand[stem])
        else:
            tr = {}
        for k in src:
            if k in extra:
                tr[k] = extra[k]
            elif k not in tr:
                raise KeyError(f"Missing translation: {stem} / {k}")
        if set(tr) != set(src):
            raise SystemExit(f"{stem} key mismatch")
        out = CHUNK_DIR / f"{stem}.zh.json"
        with out.open("w", encoding="utf-8") as f:
            json.dump(tr, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"{stem}.zh.json: {len(tr)} keys")

    # verify
    for stem in stems:
        src = load_json(f"{stem}.json")
        zh = load_json(f"{stem}.zh.json")
        assert len(src) == len(zh) and set(src) == set(zh)


if __name__ == "__main__":
    main()
