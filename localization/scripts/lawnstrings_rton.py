#!/usr/bin/env python3
"""LawnStrings-only RTON decode/encode (no Sen dependency).

Reflourished 1.4.2 LawnStrings uses a single 0x90/0x91 UTF-8 byte-string
cache for keys and values (including CJK). Decode still accepts 0x92/0x93
for robustness; encode emits only 0x90/0x91. Root object fields: ``objects``
then ``version`` (uvarint). Slot limit: 2666496 bytes.
"""
from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from pathlib import Path
from typing import Iterable, Mapping, Sequence

LAWNSTRINGS_SLOT = 2666496
RTON_VERSION = 1
SEN_ALIAS = "LawnStringsData"
SEN_OBJCLASS = "LawnStringsData"


# ---------------------------------------------------------------------------
# varint
# ---------------------------------------------------------------------------


def read_varint(buf: bytes, i: int) -> tuple[int, int]:
    num = 0
    shift = 0
    while True:
        b = buf[i]
        i += 1
        num |= (b & 0x7F) << shift
        if b < 0x80:
            return num, i
        shift += 7


def write_varint(n: int) -> bytes:
    if n < 0:
        raise ValueError("varint must be non-negative")
    out = bytearray()
    while n >= 0x80:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


# ---------------------------------------------------------------------------
# decode
# ---------------------------------------------------------------------------


class RTONReader:
    def __init__(self, buf: bytes):
        self.buf = buf
        self.i = 0
        self.cached: list[str] = []
        self.cached_printable: list[str] = []

    def u8(self) -> int:
        b = self.buf[self.i]
        self.i += 1
        return b

    def varint(self) -> int:
        n, self.i = read_varint(self.buf, self.i)
        return n

    def latin(self) -> str:
        ln = self.varint()
        s = self.buf[self.i : self.i + ln].decode("utf-8", "replace")
        self.i += ln
        return s

    def utf8(self) -> str:
        _chars = self.varint()
        ln = self.varint()
        s = self.buf[self.i : self.i + ln].decode("utf-8", "replace")
        self.i += ln
        return s

    def read_string_code(self, code: int) -> str:
        if code == 0x90:
            s = self.latin()
            self.cached.append(s)
            return s
        if code == 0x91:
            return self.cached[self.varint()]
        if code == 0x92:
            s = self.utf8()
            self.cached_printable.append(s)
            return s
        if code == 0x93:
            return self.cached_printable[self.varint()]
        if code == 0x81:
            return self.latin()
        if code == 0x82:
            return self.utf8()
        raise ValueError(f"not a string opcode {code:02x} at {self.i - 1}")

    def skip_value(self, code: int) -> None:
        if code in (0x00, 0x01, 0x09, 0x0B, 0x11, 0x13, 0x21, 0x23, 0x27, 0x41, 0x43, 0x47):
            return
        if code in (0x08, 0x0A):
            self.i += 1
            return
        if code in (0x10, 0x12):
            self.i += 2
            return
        if code in (0x20, 0x22, 0x26):
            self.i += 4
            return
        if code in (0x24, 0x25, 0x28, 0x29, 0x44, 0x45, 0x48, 0x49):
            self.varint()
            return
        if code in (0x40, 0x42, 0x46):
            self.i += 8
            return
        if code in (0x81, 0x82, 0x90, 0x91, 0x92, 0x93):
            self.read_string_code(code)
            return
        if code == 0x84:
            return
        if code == 0x83:
            sub = self.u8()
            if sub == 0x00:
                return
            if sub == 0x02:
                self.utf8()
                self.varint()
                self.varint()
                self.i += 4
                return
            if sub == 0x03:
                self.utf8()
                self.utf8()
                return
            raise ValueError(f"unknown rtid {sub:02x}")
        if code == 0x85:
            while True:
                c = self.u8()
                if c == 0xFF:
                    return
                self.read_string_code(c)
                self.skip_value(self.u8())
            return
        if code == 0x86:
            marker = self.u8()
            if marker != 0xFD:
                raise ValueError(f"expected fd after 86, got {marker:02x}")
            self.varint()
            while True:
                c = self.u8()
                if c == 0xFE:
                    return
                self.skip_value(c)
            return
        raise ValueError(f"cannot skip opcode {code:02x} at {self.i - 1}")

    def read_array(self, *, expect_loc_strings: bool = False) -> list[str] | None:
        marker = self.u8()
        if marker != 0xFD:
            raise ValueError(f"expected fd after 86, got {marker:02x}")
        count = self.varint()
        string_items: list[str] = []
        pure_strings = True
        while True:
            code = self.u8()
            if code == 0xFE:
                break
            if code in (0x81, 0x82, 0x90, 0x91, 0x92, 0x93):
                string_items.append(self.read_string_code(code))
            elif code == 0x85:
                pure_strings = False
                nested = self.walk_object()
                if nested is not None:
                    return nested
            else:
                pure_strings = False
                self.skip_value(code)
        if expect_loc_strings:
            if pure_strings and len(string_items) == count:
                return string_items
            raise ValueError(
                f"LocStringValues expected {count} strings, "
                f"got pure={pure_strings} n={len(string_items)}"
            )
        return None

    def walk_object(self) -> list[str] | None:
        while True:
            code = self.u8()
            if code == 0xFF:
                return None
            key = self.read_string_code(code)
            vcode = self.u8()
            if key == "LocStringValues" and vcode == 0x86:
                return self.read_array(expect_loc_strings=True)
            if vcode == 0x85:
                found = self.walk_object()
                if found is not None:
                    return found
            elif vcode == 0x86:
                found = self.read_array(expect_loc_strings=False)
                if found is not None:
                    return found
            else:
                self.skip_value(vcode)


def pairs_from_strings(strings: Sequence[str]) -> list[tuple[str, str]]:
    if len(strings) % 2:
        raise ValueError(f"odd string count {len(strings)}")
    return [(strings[j], strings[j + 1]) for j in range(0, len(strings), 2)]


def ordered_dict_from_pairs(pairs: Sequence[tuple[str, str]]) -> OrderedDict[str, str]:
    """Last duplicate key wins (JSON-flat semantics)."""
    return OrderedDict(pairs)


def decode_rton_strings(data: bytes | Path) -> list[str]:
    buf = data.read_bytes() if isinstance(data, Path) else data
    if buf[0:4] != b"RTON":
        raise ValueError("not RTON")
    r = RTONReader(buf)
    r.i = 8
    strings = r.walk_object()
    if not strings:
        raise ValueError("LocStringValues not found")
    return strings


def decode_rton_pairs(data: bytes | Path) -> list[tuple[str, str]]:
    return pairs_from_strings(decode_rton_strings(data))


def decode_rton(data: bytes | Path) -> OrderedDict[str, str]:
    return ordered_dict_from_pairs(decode_rton_pairs(data))


# ---------------------------------------------------------------------------
# encode
# ---------------------------------------------------------------------------


class RTONWriter:
    def __init__(self) -> None:
        self.buf = bytearray()
        self.cache: list[str] = []
        self.cache_index: dict[str, int] = {}

    def raw(self, b: bytes | int) -> None:
        if isinstance(b, int):
            self.buf.append(b)
        else:
            self.buf.extend(b)

    def varint(self, n: int) -> None:
        self.raw(write_varint(n))

    def cached_string(self, s: str) -> None:
        idx = self.cache_index.get(s)
        if idx is not None:
            self.raw(0x91)
            self.varint(idx)
            return
        raw = s.encode("utf-8")
        self.raw(0x90)
        self.varint(len(raw))
        self.raw(raw)
        self.cache_index[s] = len(self.cache)
        self.cache.append(s)

    def uvarint_value(self, n: int) -> None:
        """Opcode 0x24 + unsigned RTON varint (used for objdata.version)."""
        self.raw(0x24)
        self.varint(n)


def encode_rton(
    pairs: Mapping[str, str] | Sequence[tuple[str, str]] | Sequence[str],
    *,
    version: int = RTON_VERSION,
) -> bytes:
    """Encode LawnStrings RTON matching Reflourished/Sen layout."""
    if isinstance(pairs, Mapping):
        items: list[tuple[str, str]] = list(pairs.items())
    elif pairs and isinstance(pairs[0], str):  # type: ignore[index]
        items = pairs_from_strings(pairs)  # type: ignore[arg-type]
    else:
        items = list(pairs)  # type: ignore[arg-type]

    flat: list[str] = []
    for k, v in items:
        flat.append(k)
        flat.append(v)

    w = RTONWriter()
    w.raw(b"RTON")
    w.raw(version.to_bytes(4, "little"))

    # root object
    w.cached_string("objects")
    w.raw(0x86)
    w.raw(0xFD)
    w.varint(1)

    # objects[0]
    w.raw(0x85)
    w.cached_string("aliases")
    w.raw(0x86)
    w.raw(0xFD)
    w.varint(1)
    w.cached_string(SEN_ALIAS)
    w.raw(0xFE)

    w.cached_string("objclass")
    w.cached_string(SEN_OBJCLASS)  # recall of alias via cache

    w.cached_string("objdata")
    w.raw(0x85)
    w.cached_string("LocStringValues")
    w.raw(0x86)
    w.raw(0xFD)
    w.varint(len(flat))
    for s in flat:
        w.cached_string(s)
    w.raw(0xFE)
    w.raw(0xFF)  # end objdata

    w.raw(0xFF)  # end objects[0]
    w.raw(0xFE)  # end objects array

    # Root-level sibling of "objects" (matches Sen / golden RTON).
    w.cached_string("version")
    w.uvarint_value(1)
    w.raw(0xFF)  # end root
    w.raw(b"DONE")
    return bytes(w.buf)


def encode_rton_to_file(
    pairs: Mapping[str, str] | Sequence[tuple[str, str]],
    out: Path,
    *,
    slot_limit: int = LAWNSTRINGS_SLOT,
) -> bytes:
    data = encode_rton(pairs)
    if len(data) > slot_limit:
        raise SystemExit(
            f"RTON too large: {len(data)} > slot {slot_limit}"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return data


# ---------------------------------------------------------------------------
# Sen JSON / merge helpers
# ---------------------------------------------------------------------------


def sen_json_to_pairs(sen: Mapping) -> list[tuple[str, str]]:
    vals = sen["objects"][0]["objdata"]["LocStringValues"]
    return pairs_from_strings(vals)


def pairs_to_sen_json(
    pairs: Sequence[tuple[str, str]] | Mapping[str, str],
    *,
    template: Mapping | None = None,
) -> dict:
    if isinstance(pairs, Mapping):
        items = list(pairs.items())
    else:
        items = list(pairs)
    flat: list[str] = []
    for k, v in items:
        flat.append(k)
        flat.append(v)

    if template is not None:
        sen = json.loads(json.dumps(template))  # deep copy via JSON
    else:
        sen = {
            "objects": [
                {
                    "aliases": [SEN_ALIAS],
                    "objclass": SEN_OBJCLASS,
                    "objdata": {"LocStringValues": []},
                }
            ]
        }
    sen["objects"][0]["objdata"]["LocStringValues"] = flat
    return sen


def merge_extra_keys(
    pairs: Sequence[tuple[str, str]] | Mapping[str, str],
    *extras: Mapping[str, str],
) -> list[tuple[str, str]]:
    """Update existing keys in order; append new keys from extras."""
    if isinstance(pairs, Mapping):
        items = list(pairs.items())
    else:
        items = list(pairs)
    index = {k: i for i, (k, _) in enumerate(items)}
    for extra in extras:
        for k, v in extra.items():
            if k in index:
                i = index[k]
                items[i] = (k, v)
            else:
                index[k] = len(items)
                items.append((k, v))
    return items


def load_json_pairs(path: Path) -> list[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "objects" in data:
        return sen_json_to_pairs(data)
    if isinstance(data, dict):
        return list(data.items())
    raise ValueError(f"unsupported JSON shape: {path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Iterable[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_dec = sub.add_parser("decode", help="RTON -> flat JSON")
    p_dec.add_argument("rton", type=Path)
    p_dec.add_argument("-o", "--output", type=Path, required=True)
    p_dec.add_argument(
        "--sen",
        action="store_true",
        help="write Sen-shaped JSON instead of flat dict",
    )

    p_enc = sub.add_parser("encode", help="flat or Sen JSON -> RTON")
    p_enc.add_argument("json_in", type=Path)
    p_enc.add_argument("-o", "--output", type=Path, required=True)
    p_enc.add_argument(
        "--slot-limit",
        type=int,
        default=LAWNSTRINGS_SLOT,
        help=f"fail if larger (default {LAWNSTRINGS_SLOT})",
    )

    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.cmd == "decode":
        pairs = decode_rton_pairs(args.rton)
        if args.sen:
            payload = pairs_to_sen_json(pairs)
        else:
            payload = OrderedDict(pairs)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {len(pairs)} pairs -> {args.output}")
        return

    if args.cmd == "encode":
        pairs = load_json_pairs(args.json_in)
        data = encode_rton_to_file(pairs, args.output, slot_limit=args.slot_limit)
        print(
            f"wrote {args.output} ({len(data)} bytes, "
            f"pairs={len(pairs)}, headroom={args.slot_limit - len(data)})"
        )
        return


if __name__ == "__main__":
    main()
