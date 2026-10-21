from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("baseline_compare", EXAMPLES / "Compare-RteMacBaseline.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BaselineCompareTests(unittest.TestCase):
    def test_classifies_all_four_states(self) -> None:
        desired = json.loads((EXAMPLES / "fixtures/desired-baseline.json").read_text(encoding="utf-8"))
        observed = json.loads((EXAMPLES / "fixtures/observed-baseline.json").read_text(encoding="utf-8"))
        result = MODULE.compare(desired, observed)
        counts = {status: sum(item["status"] == status for item in result) for status in (
            "compliant", "drift", "missing", "not-applicable"
        )}
        self.assertEqual(counts, {"compliant": 2, "drift": 1, "missing": 1, "not-applicable": 1})

    def test_rejects_unknown_schema(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.compare({}, {})


if __name__ == "__main__":
    unittest.main()
