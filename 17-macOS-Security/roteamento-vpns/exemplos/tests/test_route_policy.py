from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from route_policy import evaluate_acl, lookup

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


class RoutePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.routes = json.loads((FIXTURES / "routes.json").read_text(encoding="utf-8"))
        cls.acl = json.loads((FIXTURES / "acl.json").read_text(encoding="utf-8"))

    def test_longest_prefix_precedes_metric(self) -> None:
        result = lookup(self.routes, "10.20.30.40")
        self.assertIsNotNone(result)
        self.assertEqual(result["next_hop"], "192.0.2.3")

    def test_preference_then_metric_break_ties(self) -> None:
        result = lookup(self.routes, "10.20.9.9")
        self.assertIsNotNone(result)
        self.assertEqual(result["next_hop"], "192.0.2.2")

    def test_default_route(self) -> None:
        result = lookup(self.routes, "203.0.113.80")
        self.assertEqual(result["next_hop"], "192.0.2.1")

    def test_acl_first_match_and_default(self) -> None:
        allowed = evaluate_acl(self.acl, "10.1.10.5", "10.2.20.8", "tcp", 443)
        denied = evaluate_acl(self.acl, "10.1.10.5", "10.2.20.8", "tcp", 22)
        self.assertEqual(allowed, {"action": "allow", "rule_id": "users-to-app-https"})
        self.assertEqual(denied["action"], "deny")

    def test_invalid_port_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_acl(self.acl, "10.1.10.5", "10.2.20.8", "tcp", 70000)


if __name__ == "__main__":
    unittest.main()
