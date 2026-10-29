"""Extract LocStringValues key/value pairs from LawnStrings RTON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


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
        raise ValueError(f"not a string opcode {code:02x} at {self.i-1}")

    def skip_value(self, code: int) -> None:
        # Minimal skipper for values before LocStringValues.
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
        raise ValueError(f"cannot skip opcode {code:02x} at {self.i-1}")

    def read_array(self, *, expect_loc_strings: bool = False) -> list[str] | None:
        """Parse 0x86 array body (caller already consumed 0x86)."""
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
                f"LocStringValues expected {count} strings, got pure={pure_strings} n={len(string_items)}"
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


def pairs_from_strings(strings: list[str]) -> dict[str, str]:
    if len(strings) % 2:
        raise ValueError(f"odd string count {len(strings)}")
    return {strings[j]: strings[j + 1] for j in range(0, len(strings), 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rton", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()
    r = RTONReader(args.rton.read_bytes())
    if r.buf[0:4] != b"RTON":
        raise ValueError("not RTON")
    r.i = 8
    strings = r.walk_object()
    if not strings:
        raise ValueError("LocStringValues not found")
    pairs = pairs_from_strings(strings)
    args.output.write_text(json.dumps(pairs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(pairs)} keys from {len(strings)} strings -> {args.output}")


if __name__ == "__main__":
    main()
