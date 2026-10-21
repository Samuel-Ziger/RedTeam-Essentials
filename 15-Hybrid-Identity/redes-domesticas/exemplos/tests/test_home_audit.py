from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from home_audit import audit

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures/home-network.json"


class HomeAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_fixture_has_expected_findings(self) -> None:
        identifiers = {item["id"] for item in audit(self.document)}
        self.assertIn("wifi.wps", identifiers)
        self.assertIn("exposure.upnp", identifiers)
        self.assertIn("recovery.backup", identifiers)

    def test_hardened_document_is_clean(self) -> None:
        doc = copy.deepcopy(self.document)
        doc["wifi"].update({"wps_enabled": False, "guest_isolation": True})
        doc["exposure"].update({"upnp_enabled": False, "port_forwards": []})
        doc["recovery"]["restore_tested"] = True
        self.assertEqual(audit(doc), [])

    def test_rejects_pool_outside_lan(self) -> None:
        self.document["lan"]["dhcp_start"] = "198.51.100.10"
        with self.assertRaises(ValueError):
            audit(self.document)

    def test_rejects_unknown_root_field(self) -> None:
        self.document["secret"] = "must-not-be-here"
        with self.assertRaises(ValueError):
            audit(self.document)


if __name__ == "__main__":
    unittest.main()
