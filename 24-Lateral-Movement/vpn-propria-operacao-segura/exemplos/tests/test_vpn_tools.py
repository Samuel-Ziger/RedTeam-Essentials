from __future__ import annotations

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


planner = load_module("wireguard_plan")
auditor = load_module("vpn_policy_audit")


def load_json(name: str) -> dict:
    return json.loads((COURSE / "fixtures" / name).read_text(encoding="utf-8"))


class VpnToolsTests(unittest.TestCase):
    def test_plan_fixture_and_render_are_secret_free(self) -> None:
        plan = planner.validate_plan(load_json("vpn-plan.json"))
        output = planner.render(plan)
        self.assertIn("PrivateKey = <SERVER_PRIVATE_KEY>", output)
        self.assertIn("198.51.100.10:51820", output)
        self.assertIn("alice-laptop", output)

    def test_duplicate_address_is_rejected(self) -> None:
        plan = load_json("vpn-plan.json")
        plan["peers"][1]["address"] = plan["peers"][0]["address"]
        with self.assertRaisesRegex(ValueError, "duplicado"):
            planner.validate_plan(plan)

    def test_overlap_is_rejected(self) -> None:
        plan = load_json("vpn-plan.json")
        plan["reserved_networks"].append("10.66.0.0/25")
        with self.assertRaisesRegex(ValueError, "sobrepõe"):
            planner.validate_plan(plan)

    def test_real_looking_key_is_rejected_from_fixture(self) -> None:
        plan = load_json("vpn-plan.json")
        plan["server"]["public_key"] = "not-a-placeholder"
        with self.assertRaisesRegex(ValueError, "placeholder"):
            planner.validate_plan(plan)

    def test_good_policy_returns_baseline(self) -> None:
        findings = auditor.audit(load_json("vpn-policy.json"))
        self.assertEqual(
            findings,
            [{"severity": "info", "control": "baseline", "message": "controles declarados presentes"}],
        )

    def test_policy_finds_authorization_and_key_failures(self) -> None:
        policy = load_json("vpn-policy.json")
        policy["owned_or_authorized"] = False
        policy["private_keys_outside_repository"] = False
        findings = auditor.audit(policy)
        controls = {item["control"] for item in findings}
        self.assertTrue({"owned_or_authorized", "private_keys_outside_repository"} <= controls)
        self.assertTrue(all(item["severity"] == "critical" for item in findings))
