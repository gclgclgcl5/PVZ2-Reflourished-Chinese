#!/usr/bin/env python3
"""Scheme A: replace dialogue fonts inside LoadingFonts with fixed stock usize.

Critical finding (1.4.2): growing the LoadingFonts payload usize crashes even
when metas are unchanged. EOF relocation of a pgsr with the *same* usize works.
Therefore replacements must be packed into the stock uncompressed size
(0x4B7000), padding with zeros if needed, then zstd-compressed and attached at
OBB EOF (catalog updated). Name-pool path bytes stay stock; only off/size u32s
change.
"""
from __future__ import annotations

import argparse
import struct
from pathlib import Path

import zstandard as zstd
from fontTools.ttLib import TTFont

from inspect_loadingfonts import (  # noqa: E402
    HDR_SIZE,
    INFO_AT,
    LF_CSIZE_AT,
    LF_FILE_OFF_AT,
    LF_TOTAL2_AT,
    LF_TOTAL_AT,
    LF_USIZE2_AT,
    LF_USIZE_AT,
    STOCK_FONTS,
    find_meta,
    read_pgsr,
)

# basename upper -> fonts_cjk filename from build_dialogue_cjk_fonts.py
FONT_FILES: dict[str, str] = {
    "ASHLEYSCRIPTMTSTD.TTF": "Ashley_Script_MT_Std.ttf",
    "BRIANNETOD.TTF": "BrianneTod.ttf",
    "CENTURY751.TTF": "Century751_SeBd_BT.ttf",
    "CROMAGNUMCONDENSED.TTF": "Cro-Magnum_Condensed.ttf",
    "HOUSE OF TERROR.TTF": "MonsterFonts-HouseofTerror.ttf",
    "INFROMAN.TTF": "Informal_Roman.ttf",
    "ITCBLKAD.TTF": "Blackadder_ITC.ttf",
    "NEWSFLASHBB.TTF": "Newsflash_BB.ttf",
    "PICO12__.TTF": "Pico12.ttf",
    "ROCKWELLCONDENSED.TTF": "Rockwell_Condensed.ttf",
    "ROGFONTS.TTF": "ROG_Fonts.ttf",
    "UNMASKEDBB.TTF": "Unmasked_BB.ttf",
}

# typefaces.json Font family names for stub renaming
FAMILY_NAMES: dict[str, str] = {
    "ASHLEYSCRIPTMTSTD.TTF": "Ashley Script MT Std",
    "BRIANNETOD.TTF": "BrianneTod",
    "CENTURY751.TTF": "Century751 SeBd BT",
    "CROMAGNUMCONDENSED.TTF": "Cro-Magnum Condensed",
    "HOUSE OF TERROR.TTF": "MonsterFonts-HouseofTerror",
    "INFROMAN.TTF": "Informal Roman",
    "ITCBLKAD.TTF": "Blackadder ITC",
    "NEWSFLASHBB.TTF": "Newsflash BB",
    "PICO12__.TTF": "Pico12",
    "ROCKWELLCONDENSED.TTF": "Rockwell Condensed",
    "ROGFONTS.TTF": "ROG Fonts",
    "UNMASKEDBB.TTF": "Unmasked BB",
}

STOCK_USIZE = 0x4B7000
UI_FACE = "FBUSV8C5EI.TTF"


def align(n: int, a: int = 0x1000) -> int:
    return (n + a - 1) & ~(a - 1)


def compress_payload(payload: bytes) -> bytes:
    """Match stock LoadingFonts zstd style when possible (often desc 0xA0)."""
    params = zstd.ZstdCompressionParameters.from_level(
        19, write_content_size=True, write_checksum=False
    )
    cctx = zstd.ZstdCompressor(compression_params=params)
    cobj = cctx.compressobj(size=len(payload))
    out = cobj.compress(payload) + cobj.flush()
    if out[:4] != b"\x28\xb5\x2f\xfd":
        raise SystemExit("zstd magic missing")
    fd = out[4]
    print(f"zstd csize={len(out)} desc=0x{fd:02x} single_segment={(fd >> 5) & 1}")
    return out


def set_family_name(font_path: Path, family: str) -> None:
    font = TTFont(font_path)
    name = font["name"]
    name.names = [r for r in name.names if r.nameID not in (1, 2, 3, 4, 6, 16, 17)]
    ps = family.replace(" ", "")[:31] if " " in family else family[:63]

    def add(name_id: int, string: str) -> None:
        name.setName(string, name_id, 3, 1, 0x409)

    add(1, family)
    add(2, "Regular")
    add(3, f"{family} Regular")
    add(4, family)
    add(6, ps)
    add(16, family)
    add(17, "Regular")
    font.save(font_path)
    font.close()


def make_stub(template: bytes, family: str, dest: Path) -> bytes:
    dest.write_bytes(template)
    # subset to tiny ASCII if large
    if dest.stat().st_size > 40000:
        from fontTools.subset import Options, Subsetter

        font = TTFont(dest)
        opts = Options()
        opts.notdef_outline = True
        opts.drop_tables += ["DSIG"]
        sub = Subsetter(options=opts)
        sub.populate(text=" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        sub.subset(font)
        font.save(dest)
        font.close()
    set_family_name(dest, family)
    return dest.read_bytes()


def resolve_replace_list(only: list[str] | None, all_dialogue: bool) -> list[str]:
    if all_dialogue:
        return list(FONT_FILES.keys())
    if not only:
        raise SystemExit("pass --only NAME or --all-dialogue")
    out: list[str] = []
    for raw in only:
        key = raw.strip().upper()
        if not key.endswith(".TTF"):
            matches = [k for k in FONT_FILES if k.replace(".TTF", "") == key or k.startswith(key)]
            if key == "PICO12" or key == "PICO":
                key = "PICO12__.TTF"
            elif len(matches) == 1:
                key = matches[0]
            else:
                key = key + ".TTF"
        if key == UI_FACE:
            raise SystemExit("refusing to replace UI face FBUSV8C5EI.TTF")
        if key not in FONT_FILES:
            raise SystemExit(f"unknown {raw!r}; choose from {sorted(FONT_FILES)}")
        out.append(key)
    return out


def _read_font(path: Path) -> bytes:
    if not path.exists():
        raise SystemExit(f"missing {path}")
    blob = path.read_bytes()
    if len(blob) < 1000:
        raise SystemExit(f"font too small: {path}")
    return blob


def pack_fixed_usize(
    stock_payload: bytes,
    fonts_dir: Path,
    replace: list[str],
    stub_others: bool,
    full_coverage: bool,
) -> tuple[bytes, dict[str, tuple[int, int]]]:
    """Pack fonts into exactly STOCK_USIZE.

    full_coverage:
      - Replace UI with fonts_cjk/fbUsv8C5eI_full.ttf (full LawnStrings cmap)
      - Pack styled faces from --only / defaults (Brianne/Pico/Ashley)
      - Alias every other dialogue face to the UI blob (shared off/size)
    """
    extracted: dict[str, bytes] = {
        name: bytes(stock_payload[off : off + size]) for name, (off, size) in STOCK_FONTS.items()
    }

    if full_coverage:
        ui_path = fonts_dir / "fbUsv8C5eI_full.ttf"
        ui_blob = _read_font(ui_path)
        extracted[UI_FACE] = ui_blob
        print(f"  replace {UI_FACE} <- {ui_path.name} ({len(ui_blob)} bytes)")

        styled_default = [
            "BRIANNETOD.TTF",
            "PICO12__.TTF",
            "ASHLEYSCRIPTMTSTD.TTF",
        ]
        styled = replace if replace else styled_default
        for name in styled:
            if name not in FONT_FILES:
                raise SystemExit(f"not a dialogue face: {name}")
            blob = _read_font(fonts_dir / FONT_FILES[name])
            extracted[name] = blob
            print(f"  replace {name} <- {FONT_FILES[name]} ({len(blob)} bytes)")

        # name -> which extracted key owns the bytes (for sharing)
        owner: dict[str, str] = {UI_FACE: UI_FACE}
        for name in STOCK_FONTS:
            if name == UI_FACE:
                continue
            if name in styled:
                owner[name] = name
            else:
                owner[name] = UI_FACE
                print(f"  alias  {name} -> {UI_FACE}")

        new_payload = bytearray()
        key_meta: dict[str, tuple[int, int]] = {}
        new_meta: dict[str, tuple[int, int]] = {}
        for name in STOCK_FONTS:
            key = owner[name]
            if key not in key_meta:
                blob = extracted[key]
                off = align(len(new_payload), 0x1000)
                if off > len(new_payload):
                    new_payload.extend(b"\x00" * (off - len(new_payload)))
                new_payload.extend(blob)
                key_meta[key] = (off, len(blob))
                print(f"  pack-unique {key:28s} off={off:#08x} size={len(blob):#x}")
            new_meta[name] = key_meta[key]
            print(f"  meta {name:28s} -> {new_meta[name][0]:#08x}/{new_meta[name][1]:#x}")
    else:
        stub_template = extracted.get("ROGFONTS.TTF") or next(iter(extracted.values()))
        stub_dir = fonts_dir / "_stubs"
        stub_dir.mkdir(parents=True, exist_ok=True)

        for name in replace:
            src = fonts_dir / FONT_FILES[name]
            blob = _read_font(src)
            extracted[name] = blob
            print(f"  replace {name} <- {src.name} ({len(blob)} bytes)")

        if stub_others:
            for name in FONT_FILES:
                if name in replace:
                    continue
                dest = stub_dir / (name.replace(" ", "_") + ".stub.ttf")
                extracted[name] = make_stub(stub_template, FAMILY_NAMES[name], dest)
                print(f"  stub    {name} ({len(extracted[name])} bytes)")

        new_payload = bytearray()
        new_meta = {}
        for name in STOCK_FONTS:
            blob = extracted[name]
            off = align(len(new_payload), 0x1000)
            if off > len(new_payload):
                new_payload.extend(b"\x00" * (off - len(new_payload)))
            new_payload.extend(blob)
            new_meta[name] = (off, len(blob))
            print(f"  pack {name:28s} off={off:#08x} size={len(blob):#x}")

    if len(new_payload) > STOCK_USIZE:
        raise SystemExit(
            f"packed payload {len(new_payload)} exceeds fixed usize {STOCK_USIZE}; "
            "use --full-coverage or smaller subsets / --stub-others"
        )
    new_payload.extend(b"\x00" * (STOCK_USIZE - len(new_payload)))
    print(f"packed usize={len(new_payload):#x} (fixed)")
    return bytes(new_payload), new_meta


def build_pgsr(
    stock_hdr: bytes,
    stock_payload: bytes,
    fonts_dir: Path,
    replace: list[str],
    stub_others: bool,
    full_coverage: bool = False,
) -> tuple[bytes, int, int]:
    hdr = bytearray(stock_hdr)
    payload, new_meta = pack_fixed_usize(
        stock_payload, fonts_dir, replace, stub_others, full_coverage
    )
    stock_info = bytes(hdr[INFO_AT:])
    patched_fields: set[int] = set()
    for name, (old_off, old_size) in STOCK_FONTS.items():
        field_at = find_meta(bytes(hdr), old_off, old_size)
        if field_at is None:
            # already patched mid-loop — search using previous new_meta? use stock snapshot
            fake = bytearray(HDR_SIZE)
            fake[INFO_AT:] = stock_info
            field_at = find_meta(bytes(fake), old_off, old_size)
            if field_at is None:
                raise SystemExit(f"meta not found for {name}")
        no, ns = new_meta[name]
        struct.pack_into("<II", hdr, field_at, no, ns)
        patched_fields.add(field_at - INFO_AT)
        patched_fields.add(field_at + 4 - INFO_AT)

    # verify only off/size changed
    new_info = bytes(hdr[INFO_AT:])
    for i in range(0, len(new_info), 4):
        if new_info[i : i + 4] != stock_info[i : i + 4] and i not in patched_fields:
            raise SystemExit(f"unexpected info diff at info+{i:#x}")

    zblob = compress_payload(payload)
    csize = len(zblob)
    struct.pack_into("<I", hdr, 0x1C, csize)
    struct.pack_into("<I", hdr, 0x20, STOCK_USIZE)
    struct.pack_into("<I", hdr, 0x28, csize + HDR_SIZE)
    pgsr = bytes(hdr) + zblob
    pgsr += b"\x00" * ((-len(pgsr)) % 0x1000)
    return pgsr, csize, STOCK_USIZE


def write_obb_with_pgsr(base_obb: bytes, pgsr: bytes, csize: int, usize: int) -> bytes:
    data = bytearray(base_obb)
    new_off = align(len(data), 0x1000)
    if new_off > len(data):
        data.extend(b"\x00" * (new_off - len(data)))
    data.extend(pgsr)
    total = HDR_SIZE + csize
    struct.pack_into("<I", data, LF_FILE_OFF_AT, new_off)
    struct.pack_into("<I", data, LF_TOTAL_AT, total)
    struct.pack_into("<I", data, LF_CSIZE_AT, csize)
    struct.pack_into("<I", data, LF_USIZE_AT, usize)
    struct.pack_into("<I", data, LF_USIZE2_AT, usize)
    struct.pack_into("<I", data, LF_TOTAL2_AT, total)
    print(f"catalog -> file_off={new_off:#x} csize={csize:#x} usize={usize:#x}")
    return bytes(data)


REQUIRED_FULL_COVERAGE = (
    "fbUsv8C5eI_full.ttf",
    "BrianneTod.ttf",
    "Pico12.ttf",
    "Ashley_Script_MT_Std.ttf",
)


def require_full_coverage_fonts(fonts_dir: Path) -> None:
    missing = [n for n in REQUIRED_FULL_COVERAGE if not (fonts_dir / n).is_file()]
    if missing:
        raise SystemExit(
            f"fonts_cjk 缺少方案 A 字体: {', '.join(missing)}\n"
            f"目录: {fonts_dir}\n"
            "请先运行: python localization/scripts/build_dialogue_cjk_fonts.py --skip-download\n"
            "（或去掉 --skip-download 以下载 fonts_src）"
        )


def apply_full_coverage_obb(
    stock_obb: Path | bytes,
    base_obb: Path | bytes,
    fonts_dir: Path,
    out_obb: Path,
    *,
    stock_file_off: int = 0xB17B000,
) -> Path:
    """Attach full-coverage LoadingFonts (Scheme A) onto base_obb; write out_obb."""
    require_full_coverage_fonts(fonts_dir)
    stock = stock_obb.read_bytes() if isinstance(stock_obb, Path) else stock_obb
    base = base_obb.read_bytes() if isinstance(base_obb, Path) else base_obb
    replace = ["BRIANNETOD.TTF", "PICO12__.TTF", "ASHLEYSCRIPTMTSTD.TTF"]
    hdr, _z, payload = read_pgsr(stock, stock_file_off)
    if len(payload) != STOCK_USIZE:
        print(f"warn stock payload {len(payload):#x} != {STOCK_USIZE:#x}")
    print("mode=full-coverage replace=", ", ".join(replace))
    pgsr, csize, usize = build_pgsr(
        hdr, payload, fonts_dir, replace, stub_others=False, full_coverage=True
    )
    out = write_obb_with_pgsr(base, pgsr, csize, usize)
    out_obb.parent.mkdir(parents=True, exist_ok=True)
    out_obb.write_bytes(out)
    print(f"wrote {out_obb} ({len(out)} bytes)")
    return out_obb


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stock-obb", type=Path, required=True)
    ap.add_argument("--base-obb", type=Path, default=None)
    ap.add_argument("--fonts-dir", type=Path, default=Path(r"F:\sen_work\fonts_cjk"))
    ap.add_argument("--only", action="append", default=None)
    ap.add_argument("--all-dialogue", action="store_true")
    ap.add_argument(
        "--stub-others",
        action="store_true",
        help="replace non-selected dialogue faces with tiny stubs to free space",
    )
    ap.add_argument(
        "--full-coverage",
        action="store_true",
        help="full LawnStrings cmap: pack Brianne/Pico pixel/Ashley, alias other dialogue faces to UI",
    )
    ap.add_argument("--stock-file-off", type=lambda x: int(x, 0), default=0xB17B000)
    ap.add_argument("--out-obb", type=Path, required=True)
    ap.add_argument("--out-pgsr", type=Path, default=None)
    args = ap.parse_args()

    if args.full_coverage:
        replace = args.only or [
            "BRIANNETOD.TTF",
            "PICO12__.TTF",
            "ASHLEYSCRIPTMTSTD.TTF",
        ]
        # normalize --only values
        if args.only:
            replace = resolve_replace_list(args.only, False)
        stub_others = False
        print("mode=full-coverage replace=", ", ".join(replace))
    else:
        replace = resolve_replace_list(args.only, args.all_dialogue)
        stub_others = args.stub_others or (len(replace) <= 3 and not args.all_dialogue)
        print("replace:", ", ".join(replace), "| stub_others=", stub_others)

    stock = args.stock_obb.read_bytes()
    hdr, _z, payload = read_pgsr(stock, args.stock_file_off)
    if len(payload) != STOCK_USIZE:
        print(f"warn stock payload {len(payload):#x} != {STOCK_USIZE:#x}")

    pgsr, csize, usize = build_pgsr(
        hdr, payload, args.fonts_dir, replace, stub_others, args.full_coverage
    )
    if args.out_pgsr:
        args.out_pgsr.write_bytes(pgsr)
        print(f"wrote {args.out_pgsr}")

    base = args.base_obb.read_bytes() if args.base_obb else stock
    out = write_obb_with_pgsr(base, pgsr, csize, usize)
    args.out_obb.write_bytes(out)
    print(f"wrote {args.out_obb} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
