from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
COURSE = HERE.parents[2]
SPEC = importlib.util.spec_from_file_location("privacy_model", COURSE / "exemplos" / "privacy_model.py")
assert SPEC and SPEC.loader
privacy_model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(privacy_model)


def fixture() -> dict:
    return json.loads((COURSE / "fixtures" / "cenario-pesquisa.json").read_text(encoding="utf-8"))


class PrivacyModelTests(unittest.TestCase):
    def test_fixture_is_valid_and_has_expected_findings(self) -> None:
        findings = privacy_model.analyze(fixture())
        codes = {finding.code for finding in findings}
        self.assertTrue({"TRUST_SHIFT", "EXPLICIT_IDENTITY", "TRAFFIC_CORRELATION", "RESIDUAL"} <= codes)

    def test_account_is_not_hidden_by_transport(self) -> None:
        activity = fixture()["activities"][1]
        activity["vpn"] = "commercial"
        codes = {finding.code for finding in privacy_model.analyze_activity(activity)}
        self.assertIn("EXPLICIT_IDENTITY", codes)
        self.assertIn("TRUST_SHIFT", codes)

    def test_untrusted_endpoint_is_critical(self) -> None:
        activity = fixture()["activities"][0]
        activity["endpoint_trusted"] = False
        finding = next(item for item in privacy_model.analyze_activity(activity) if item.code == "ENDPOINT")
        self.assertEqual(finding.severity, "critical")

    def test_refuses_unauthorized_scenario(self) -> None:
        data = fixture()
        data["authorized"] = False
        with self.assertRaisesRegex(ValueError, "authorized"):
            privacy_model.validate_scenario(data)

    def test_rejects_duplicate_activity(self) -> None:
        data = fixture()
        data["activities"].append(dict(data["activities"][0]))
        with self.assertRaisesRegex(ValueError, "duplicada"):
            privacy_model.validate_scenario(data)

    def test_render_prioritizes_higher_severity(self) -> None:
        findings = privacy_model.analyze(fixture())
        lines = privacy_model.render(findings).splitlines()
        self.assertTrue(lines[0].startswith("[HIGH"))
