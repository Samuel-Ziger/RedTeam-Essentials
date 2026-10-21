from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from architecture_audit import audit

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures/architecture.json"


class ArchitectureAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_architecture(self) -> None:
        self.assertEqual(audit(self.document), {"sites": 3, "prefixes": 6, "services": 2, "slos": 2})

    def test_rejects_prefix_overlap(self) -> None:
        self.document["sites"][1]["prefixes"][0] = "10.10.1.0/24"
        with self.assertRaises(ValueError):
            audit(self.document)

    def test_rejects_missing_slo(self) -> None:
        self.document["slos"].pop()
        with self.assertRaises(ValueError):
            audit(self.document)

    def test_rejects_unknown_site(self) -> None:
        self.document["services"][0]["sites"] = ["unknown"]
        with self.assertRaises(ValueError):
            audit(self.document)


if __name__ == "__main__":
    unittest.main()
