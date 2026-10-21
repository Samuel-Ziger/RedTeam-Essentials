from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("mac_baseline", EXAMPLES / "Get-RteMacBaseline.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MacBaselineTests(unittest.TestCase):
    def test_fixture_produces_sanitized_baseline(self) -> None:
        fixture = json.loads((EXAMPLES / "fixtures/mac-command-output.json").read_text(encoding="utf-8"))
        result = MODULE.collect(fixture)
        self.assertEqual(result["operatingSystem"]["productVersion"], "26.0")
        self.assertEqual(result["hardware"]["architecture"], "arm64")
        self.assertEqual(result["errors"], [])
        serialized = json.dumps(result).lower()
        self.assertNotIn("serial", serialized)
        self.assertNotIn("uuid", serialized)
        self.assertNotIn("network", serialized)

    def test_missing_command_is_reported(self) -> None:
        result = MODULE.collect({})
        self.assertIsNone(result["protections"]["sip"])
        self.assertGreater(len(result["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
