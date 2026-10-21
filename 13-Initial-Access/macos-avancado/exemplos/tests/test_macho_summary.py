from __future__ import annotations

import importlib.util
import struct
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("macho_summary", EXAMPLES / "MachoSummary.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def thin64(cpu_type: int) -> bytes:
    return b"\xcf\xfa\xed\xfe" + struct.pack("<IIIIIII", cpu_type, 0, 2, 0, 0, 0, 0)


class MachoSummaryTests(unittest.TestCase):
    def test_parses_thin_arm64(self) -> None:
        result = MODULE.parse(thin64(0x0100000C))
        self.assertEqual(result["kind"], "thin64")
        self.assertEqual(result["cpuType"], "arm64")
        self.assertEqual(result["loadCommandCount"], 0)

    def test_parses_fat_binary_with_two_bounded_slices(self) -> None:
        first = thin64(0x0100000C)
        second = thin64(0x01000007)
        table_size = 8 + 2 * 20
        first_offset = table_size
        second_offset = first_offset + len(first)
        header = b"\xca\xfe\xba\xbe" + struct.pack(
            ">I" + "IIIII" * 2,
            2,
            0x0100000C,
            0,
            first_offset,
            len(first),
            0,
            0x01000007,
            0,
            second_offset,
            len(second),
            0,
        )
        result = MODULE.parse(header + first + second)
        self.assertEqual(result["kind"], "fat32")
        self.assertEqual(result["architectureCount"], 2)
        self.assertEqual(result["slices"][1]["header"]["cpuType"], "x86_64")

    def test_rejects_truncated_and_oversized_inputs(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.parse(b"\xcf\xfa\xed\xfe")
        malicious = b"\xcf\xfa\xed\xfe" + struct.pack(
            "<IIIIIII", 0x0100000C, 0, 2, 1, MODULE.MAX_LOAD_COMMAND_BYTES + 1, 0, 0
        )
        with self.assertRaises(ValueError):
            MODULE.parse(malicious)

    def test_rejects_cpu_mismatch_in_universal_slice(self) -> None:
        thin = thin64(0x0100000C)
        offset = 8 + 20
        header = b"\xca\xfe\xba\xbe" + struct.pack(
            ">IIIIII", 1, 0x01000007, 0, offset, len(thin), 0
        )
        with self.assertRaises(ValueError):
            MODULE.parse(header + thin)


if __name__ == "__main__":
    unittest.main()
