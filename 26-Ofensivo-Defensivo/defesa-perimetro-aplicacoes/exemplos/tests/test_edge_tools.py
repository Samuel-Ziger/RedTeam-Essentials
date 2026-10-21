from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, COURSE / "exemplos" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


risk = load_module("edge_risk_engine")
policy = load_module("control_plane_audit")
bucket = load_module("token_bucket")


def fixture(name: str) -> dict:
    return json.loads((COURSE / "fixtures" / name).read_text(encoding="utf-8"))


class EdgeRiskTests(unittest.TestCase):
    def test_normal_browser_is_observed(self) -> None:
        result = risk.analyze(fixture("requests-sinteticas.json"))
        item = next(entry for entry in result["results"] if entry["event_id"] == "req-001")
        self.assertEqual(item["action"], "observe")
        self.assertEqual(item["score"], 0)

    def test_compound_login_abuse_is_blocked_with_reasons(self) -> None:
        result = risk.analyze(fixture("requests-sinteticas.json"))
        item = next(entry for entry in result["results"] if entry["event_id"] == "req-003")
        self.assertEqual(item["action"], "block")
        self.assertGreaterEqual(len(item["reasons"]), 3)

    def test_authenticated_api_never_receives_browser_challenge(self) -> None:
        result = risk.analyze(fixture("requests-sinteticas.json"))
        item = next(entry for entry in result["results"] if entry["event_id"] == "req-005")
        self.assertNotEqual(item["action"], "challenge")
        self.assertIn("authenticated_api:-20", item["reasons"])

    def test_verified_bot_does_not_override_high_waf_anomaly(self) -> None:
        event = copy.deepcopy(fixture("requests-sinteticas.json")["events"][2])
        event["verified_bot"] = True
        scored = risk.score_event(event)
        self.assertGreaterEqual(scored["score"], 45)

    def test_unauthorized_fixture_is_rejected(self) -> None:
        document = fixture("requests-sinteticas.json")
        document["authorized"] = False
        with self.assertRaisesRegex(ValueError, "authorized"):
            risk.analyze(document)

    def test_naive_timestamp_is_rejected(self) -> None:
        document = fixture("requests-sinteticas.json")
        document["events"][0]["timestamp"] = "2026-10-01T12:00:00"
        with self.assertRaisesRegex(ValueError, "fuso"):
            risk.analyze(document)


class ControlPlaneAuditTests(unittest.TestCase):
    def test_reference_policy_passes(self) -> None:
        result = policy.audit(fixture("politica-edge.json"))
        self.assertTrue(result["passed"])
        self.assertEqual(result["summary"]["failed"], 0)

    def test_direct_origin_access_fails(self) -> None:
        document = fixture("politica-edge.json")
        document["origin"]["direct_access"] = True
        result = policy.audit(document)
        self.assertFalse(result["passed"])
        self.assertIn("origin.direct_access", result["failed_controls"])

    def test_turnstile_age_above_five_minutes_fails(self) -> None:
        document = fixture("politica-edge.json")
        document["challenge"]["max_token_age_seconds"] = 301
        result = policy.audit(document)
        self.assertIn("challenge.max_token_age_seconds", result["failed_controls"])


class TokenBucketTests(unittest.TestCase):
    def test_reference_fixture_is_deterministic(self) -> None:
        document = fixture("eventos-rate-limit.json")
        first = bucket.simulate(document)
        second = bucket.simulate(document)
        self.assertEqual(first, second)
        self.assertEqual(first["summary"], {"allowed": 4, "rejected": 2})

    def test_keys_have_isolated_capacity(self) -> None:
        result = bucket.simulate(fixture("eventos-rate-limit.json"))
        tenant_b = [item for item in result["decisions"] if item["key"] == "tenant-b"]
        self.assertTrue(tenant_b[0]["allowed"])
        self.assertFalse(tenant_b[1]["allowed"])

    def test_regressive_time_is_rejected_per_key(self) -> None:
        document = fixture("eventos-rate-limit.json")
        document["events"] = [
            {"key": "tenant-a", "at": 2, "cost": 1},
            {"key": "tenant-a", "at": 1, "cost": 1},
        ]
        with self.assertRaisesRegex(ValueError, "regressivo"):
            bucket.simulate(document)


if __name__ == "__main__":
    unittest.main()
