# -*- coding: utf-8 -*-
import importlib.util
import json
from pathlib import Path

CHUNK_DIR = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    hand = load_module("hand", CHUNK_DIR / "_write_batch_033_zh.py")
    rest = load_module("rest", CHUNK_DIR / "_batch033_rest.py")
    T = {**hand.T, **rest.T}

    for stem, tr in T.items():
        src_path = CHUNK_DIR / f"{stem}.json"
        src = json.loads(src_path.read_text(encoding="utf-8"))
        if set(tr.keys()) != set(src.keys()):
            missing = set(src) - set(tr)
            extra = set(tr) - set(src)
            raise SystemExit(f"{stem}: missing {len(missing)} extra {len(extra)}")
        out_path = CHUNK_DIR / f"{stem}.zh.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(tr, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Wrote {out_path.name} ({len(tr)} keys)")


if __name__ == "__main__":
    main()
