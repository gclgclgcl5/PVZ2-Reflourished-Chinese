#!/usr/bin/env python3
"""Download open-source CJK fonts, subset to LawnStrings charset, rename for PvZ2.

Outputs TTFs under F:\\sen_work\\fonts_cjk\\ whose name tables match typefaces.json
Font fields (BrianneTod, Pico12, …) so NPC FontName resolution keeps working.

For Scheme A (patch_loadingfonts_append.py) the non-UI faces must fit in ~860KB
total after 0x1000 alignment. Prefer fewer CJK codepoints (see --compact) rather
than full LawnStrings cmap, or packing will exceed stock usize 0x4B7000.
"""
from __future__ import annotations

import json
import shutil
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.merge import Merger
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
LAWN = ROOT / "LawnStrings_zh.json"
SRC = ROOT / "fonts_src"
OUT = Path(r"F:\sen_work\fonts_cjk")

# (url, archive_member_or_None, local_name)
DOWNLOADS = [
    (
        "https://github.com/lxgw/LxgwWenKai/releases/download/v1.501/lxgw-wenkai-v1.501.zip",
        "lxgw-wenkai-v1.501/LXGWWenKai-Regular.ttf",
        "LXGWWenKai-Regular.ttf",
    ),
    (
        "https://github.com/TakWolf/fusion-pixel-font/releases/download/2026.10.25/fusion-pixel-font-12px-proportional-ttf-v2026.10.25.zip",
        "fusion-pixel-12px-proportional-zh_hans.ttf",
        "fusion-pixel-12px.ttf",
    ),
    (
        "https://github.com/lxgw/LxgwMarkerGothic/releases/download/v1.004/LxgwMarkerGothic-v1.004.zip",
        "LXGWMarkerGothic-Regular.ttf",
        "LXGWMarkerGothic-Regular.ttf",
    ),
    (
        "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/SC/NotoSansSC-Regular.otf",
        None,
        "NotoSansSC-Regular.otf",
    ),
    (
        "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/SC/NotoSansSC-Bold.otf",
        None,
        "NotoSansSC-Bold.otf",
    ),
    (
        "https://github.com/googlefonts/noto-cjk/raw/main/Serif/SubsetOTF/SC/NotoSerifSC-Regular.otf",
        None,
        "NotoSerifSC-Regular.otf",
    ),
]

# Target Font name (typefaces.json) -> source local file
FACE_MAP = [
    ("BrianneTod", "LXGWWenKai-Regular.ttf"),
    ("Pico12", "fusion-pixel-12px.ttf"),
    ("Ashley Script MT Std", "LXGWMarkerGothic-Regular.ttf"),
    ("Informal Roman", "NotoSerifSC-Regular.otf"),
    ("Rockwell Condensed", "NotoSansSC-Regular.otf"),
    ("Cro-Magnum Condensed", "NotoSansSC-Bold.otf"),
    ("Century751 SeBd BT", "NotoSansSC-Bold.otf"),
    ("Unmasked BB", "NotoSansSC-Bold.otf"),
    ("Newsflash BB", "NotoSansSC-Bold.otf"),
    ("ROG Fonts", "NotoSansSC-Bold.otf"),
    ("Blackadder ITC", "NotoSerifSC-Regular.otf"),
    ("MonsterFonts-HouseofTerror", "NotoSerifSC-Regular.otf"),
]

LATIN = "".join(chr(c) for c in range(0x20, 0x7F))
EXTRA = "…—–“”‘’¥€£©®™°×÷±≤≥∞·•※【】《》「」『』（）！"


def charset_from_lawn(compact_top_n: int | None = None) -> str:
    data = json.loads(LAWN.read_text(encoding="utf-8"))
    chars: set[str] = set(LATIN + EXTRA)
    if compact_top_n is None:
        for v in data.values():
            if isinstance(v, str):
                chars.update(v)
    else:
        from collections import Counter

        ctr: Counter[str] = Counter()
        for v in data.values():
            if isinstance(v, str):
                ctr.update(ch for ch in v if "\u4e00" <= ch <= "\u9fff")
        chars.update(ch for ch, _ in ctr.most_common(compact_top_n))
    chars.update("，。！？；：、")
    return "".join(sorted(chars))


def download_all() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    for url, member, local_name in DOWNLOADS:
        dest = SRC / local_name
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"cached {dest.name}")
            continue
        print(f"download {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "pvz2-loc/1.0"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            blob = resp.read()
        if member:
            with zipfile.ZipFile(BytesIO(blob)) as zf:
                # member path may vary; find by basename
                names = zf.namelist()
                hit = member if member in names else next(
                    (n for n in names if n.endswith(Path(member).name) or n.endswith(local_name.replace("fusion-pixel-12px.ttf", "fusion-pixel-12px-proportional-zh_hans.ttf"))),
                    None,
                )
                if hit is None:
                    # fusion pixel zip layout
                    hit = next(
                        (
                            n
                            for n in names
                            if n.lower().endswith(".ttf")
                            and ("zh_hans" in n.lower() or "zh-hans" in n.lower() or "sc" in n.lower())
                        ),
                        None,
                    )
                if hit is None:
                    hit = next(n for n in names if n.lower().endswith((".ttf", ".otf")))
                print(f"  extract {hit}")
                dest.write_bytes(zf.read(hit))
        else:
            dest.write_bytes(blob)
        print(f"  wrote {dest} ({dest.stat().st_size})")


def subset_font(src: Path, text: str, dest: Path) -> None:
    font = TTFont(src)
    opts = Options()
    opts.layout_closure = True
    opts.glyph_names = True
    opts.notdef_outline = True
    opts.retain_gids = False
    opts.drop_tables += ["DSIG"]
    sub = Subsetter(options=opts)
    sub.populate(text=text)
    sub.subset(font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    font.save(dest)
    font.close()


def set_family_name(font_path: Path, family: str) -> None:
    font = TTFont(font_path)
    # Clear and set Windows/Mac name records commonly read by engines
    name = font["name"]
    # Remove existing 1/2/3/4/6/16/17
    name.names = [
        r
        for r in name.names
        if r.nameID not in (1, 2, 3, 4, 6, 16, 17)
    ]
    ps = family.replace(" ", "")[:31] if " " in family else family[:63]

    def add(name_id: int, string: str) -> None:
        # platform 3 (Windows), enc 1 (Unicode BMP), lang 0x409
        name.setName(string, name_id, 3, 1, 0x409)
        # platform 1 Mac Roman fallback
        try:
            name.setName(string, name_id, 1, 0, 0)
        except Exception:
            pass

    add(1, family)
    add(2, "Regular")
    add(3, f"{family} Regular")
    add(4, family)
    add(6, ps)
    add(16, family)
    add(17, "Regular")
    font.save(font_path)
    font.close()


def otf_to_ttf(src: Path, dest: Path) -> None:
    """Save as glyf-based TTF when possible; otherwise copy."""
    font = TTFont(src, recalcBBoxes=False, recalcTimestamp=False)
    if "CFF " in font or "CFF2" in font:
        # fontTools cannot always convert CFF→glyf; keep OTF path for subset only
        font.save(dest)
    else:
        font.save(dest)
    font.close()


def merge_fallback(primary: Path, fallback: Path, text: str, dest: Path) -> None:
    """Subset primary; if many CJK missing, replace with sans subset instead."""
    tmp = dest.parent / "_tmp"
    tmp.mkdir(exist_ok=True)
    p1 = tmp / "p1.ttf"
    subset_font(primary, text, p1)
    f1 = TTFont(p1)
    cmap = f1.getBestCmap() or {}
    missing = [c for c in text if ord(c) > 0x7F and ord(c) not in cmap]
    f1.close()
    if len(missing) <= 32:
        if missing:
            print(f"  warn {len(missing)} missing glyphs kept (pixel font)")
        shutil.copyfile(p1, dest)
        return
    print(f"  {len(missing)} missing; using sans fallback for {dest.name}")
    subset_font(fallback, text, dest)


def build_ui_full(text: str) -> None:
    """Subset stock UI face to full LawnStrings charset (for --full-coverage)."""
    src = OUT / "_ui_stock.ttf"
    if not src.exists():
        # fall back to uncompressed stock extract or previous full
        for cand in (OUT / "_ui_raw.ttf", OUT / "fbUsv8C5eI.ttf"):
            if cand.exists() and cand.stat().st_size > 1_000_000:
                src = cand
                break
    if not src.exists():
        raise SystemExit("missing fonts_cjk/_ui_stock.ttf for UI full subset")
    dest = OUT / "fbUsv8C5eI_full.ttf"
    print(f"build UI full from {src.name}")
    subset_font(src, text, dest)
    # Keep game-facing family; stock UI uses an opaque PostScript-ish id.
    set_family_name(dest, "fbUsv8C5eI")
    print(f"  -> {dest} ({dest.stat().st_size})")


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--compact",
        type=int,
        nargs="?",
        const=400,
        default=None,
        help="only top-N CJK by frequency (+ ASCII/punct); recommended ~300-500 for Scheme A",
    )
    ap.add_argument(
        "--skip-download",
        action="store_true",
        help="use existing localization/fonts_src caches",
    )
    args = ap.parse_args()
    if not args.skip_download:
        download_all()
    text = charset_from_lawn(args.compact)
    print(f"charset size {len(text)} compact={args.compact}")
    OUT.mkdir(parents=True, exist_ok=True)
    fallback = SRC / "NotoSansSC-Regular.otf"
    for face_name, src_name in FACE_MAP:
        src = SRC / src_name
        if not src.exists():
            raise SystemExit(f"missing source {src}")
        # safe filename
        out_name = (
            face_name.replace(" ", "_").replace("/", "_") + ".ttf"
        )
        dest = OUT / out_name
        print(f"build {face_name} from {src.name}")
        if src_name.startswith("fusion-pixel"):
            merge_fallback(src, fallback, text, dest)
        else:
            subset_font(src, text, dest)
        set_family_name(dest, face_name)
        print(f"  -> {dest} ({dest.stat().st_size})")
    build_ui_full(text)
    print("done")


if __name__ == "__main__":
    main()
