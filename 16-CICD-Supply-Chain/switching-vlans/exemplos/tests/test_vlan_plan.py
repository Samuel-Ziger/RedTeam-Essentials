from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vlan_plan import validate

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures/vlan-plan.json"


class VlanPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_fixture(self) -> None:
        self.assertEqual(validate(self.document), {"vlan_count": 4, "port_count": 3, "trunk_count": 1})

    def test_rejects_duplicate_id(self) -> None:
        self.document["vlans"][1]["id"] = self.document["vlans"][0]["id"]
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_rejects_overlapping_prefix(self) -> None:
        self.document["vlans"][1]["prefix"] = "10.10.10.128/25"
        self.document["vlans"][0]["prefix"] = "10.10.10.0/24"
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_rejects_unknown_vlan_on_port(self) -> None:
        self.document["ports"][0]["vlans"] = [777]
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_rejects_access_with_native_vlan(self) -> None:
        document = copy.deepcopy(self.document)
        document["ports"][0]["native_vlan"] = 10
        with self.assertRaises(ValueError):
            validate(document)


if __name__ == "__main__":
    unittest.main()
