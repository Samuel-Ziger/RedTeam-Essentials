#!/usr/bin/env python3
"""Parse bounded metadata from thin and universal Mach-O files."""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path
from typing import Any

THIN_MAGICS = {
    b"\xce\xfa\xed\xfe": ("little", False),
    b"\xcf\xfa\xed\xfe": ("little", True),
    b"\xfe\xed\xfa\xce": ("big", False),
    b"\xfe\xed\xfa\xcf": ("big", True),
}
FAT_MAGICS = {
    b"\xca\xfe\xba\xbe": ("big", False),
    b"\xca\xfe\xba\xbf": ("big", True),
    b"\xbe\xba\xfe\xca": ("little", False),
    b"\xbf\xba\xfe\xca": ("little", True),
}
CPU_NAMES = {
    7: "x86",
    0x01000007: "x86_64",
    12: "arm",
    0x0100000C: "arm64",
}
FILE_TYPES = {
    1: "object",
    2: "executable",
    6: "dylib",
    8: "bundle",
    10: "dSYM",
}
MAX_ARCHITECTURES = 64
MAX_LOAD_COMMANDS = 65_536
MAX_LOAD_COMMAND_BYTES = 128 * 1024 * 1024


def unpack_from(data: bytes, endian: str, fmt: str, offset: int) -> tuple[Any, ...]:
    prefix = "<" if endian == "little" else ">"
    size = struct.calcsize(prefix + fmt)
    if offset < 0 or offset + size > len(data):
        raise ValueError("structure extends beyond file")
    return struct.unpack_from(prefix + fmt, data, offset)


def cpu_name(value: int) -> str:
    return CPU_NAMES.get(value, f"unknown-0x{value:08x}")


def parse_thin(data: bytes, *, base_offset: int = 0, bounded_size: int | None = None) -> dict[str, Any]:
    if base_offset < 0 or base_offset + 4 > len(data):
        raise ValueError("missing Mach-O magic")
    magic = data[base_offset : base_offset + 4]
    if magic not in THIN_MAGICS:
        raise ValueError("unknown thin Mach-O magic")
    endian, is_64 = THIN_MAGICS[magic]
    header_size = 32 if is_64 else 28
    available = len(data) - base_offset if bounded_size is None else bounded_size
    if available < header_size or base_offset + available > len(data):
        raise ValueError("truncated Mach-O header or slice")
    fields = unpack_from(data, endian, "IIIIII", base_offset + 4)
    cpu_type, cpu_subtype, file_type, command_count, command_bytes, flags = fields
    if command_count > MAX_LOAD_COMMANDS:
        raise ValueError("too many load commands")
    if command_bytes > MAX_LOAD_COMMAND_BYTES:
        raise ValueError("load command area exceeds safety limit")
    if command_count * 8 > command_bytes:
        raise ValueError("load command count cannot fit in declared area")
    if header_size + command_bytes > available:
        raise ValueError("load commands extend beyond Mach-O slice")
    return {
        "kind": "thin64" if is_64 else "thin32",
        "endianness": endian,
        "cpuType": cpu_name(cpu_type),
        "cpuTypeRaw": cpu_type,
        "cpuSubtype": cpu_subtype,
        "fileType": FILE_TYPES.get(file_type, f"unknown-{file_type}"),
        "loadCommandCount": command_count,
        "loadCommandBytes": command_bytes,
        "flags": f"0x{flags:08x}",
    }


def parse(data: bytes) -> dict[str, Any]:
    if len(data) < 4:
        raise ValueError("file is too small")
    magic = data[:4]
    if magic in THIN_MAGICS:
        return {"schema": "rte.macos.macho-summary/v1", **parse_thin(data), "length": len(data)}
    if magic not in FAT_MAGICS:
        raise ValueError("file is not Mach-O")

    endian, is_64 = FAT_MAGICS[magic]
    architecture_count = unpack_from(data, endian, "I", 4)[0]
    if architecture_count > MAX_ARCHITECTURES:
        raise ValueError("too many universal architectures")
    record_format = "IIQQII" if is_64 else "IIIII"
    record_size = struct.calcsize(("<" if endian == "little" else ">") + record_format)
    table_end = 8 + architecture_count * record_size
    if table_end > len(data):
        raise ValueError("truncated universal architecture table")

    slices: list[dict[str, Any]] = []
    ranges: list[tuple[int, int]] = []
    for index in range(architecture_count):
        record = unpack_from(data, endian, record_format, 8 + index * record_size)
        cpu_type, cpu_subtype, offset, size, alignment = record[:5]
        if size < 4 or offset < table_end or offset + size > len(data):
            raise ValueError(f"invalid universal slice {index}")
        if alignment > 63 or offset % (1 << alignment) != 0:
            raise ValueError(f"invalid universal slice alignment {index}")
        ranges.append((offset, offset + size))
        thin = parse_thin(data, base_offset=offset, bounded_size=size)
        if thin["cpuTypeRaw"] != cpu_type:
            raise ValueError(f"universal slice CPU mismatch {index}")
        slices.append(
            {
                "index": index,
                "declaredCpuType": cpu_name(cpu_type),
                "declaredCpuSubtype": cpu_subtype,
                "offset": offset,
                "size": size,
                "alignmentPower": alignment,
                "header": thin,
            }
        )
    ordered = sorted(ranges)
    if any(current[1] > following[0] for current, following in zip(ordered, ordered[1:])):
        raise ValueError("universal slices overlap")
    return {
        "schema": "rte.macos.macho-summary/v1",
        "kind": "fat64" if is_64 else "fat32",
        "endianness": endian,
        "architectureCount": architecture_count,
        "length": len(data),
        "slices": slices,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        result = parse(args.path.read_bytes())
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
