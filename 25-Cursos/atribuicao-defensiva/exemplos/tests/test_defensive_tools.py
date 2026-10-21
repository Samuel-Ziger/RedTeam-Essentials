from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, COURSE / "exemplos" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


correlator = load_module("telemetry_correlator")
manifest_tool = load_module("evidence_manifest")


def fixture() -> dict:
    return json.loads((COURSE / "fixtures" / "eventos-sinteticos.json").read_text(encoding="utf-8"))


class DefensiveToolsTests(unittest.TestCase):
    def test_fixture_produces_high_confidence_technical_cluster(self) -> None:
        data = correlator.validate_case(fixture())
        clusters = correlator.correlate(data["events"])
        main = next(item for item in clusters if "evt-006" in item["event_ids"])
        self.assertEqual(main["confidence"], "high")
        self.assertTrue({"application", "cloud-audit", "identity"} <= set(main["sources"]))
        self.assertIn("autoria humana", main["note"])

    def test_same_ip_alone_does_not_merge_events(self) -> None:
        events = [fixture()["events"][9], fixture()["events"][10]]
        clusters = correlator.correlate(events)
        self.assertEqual(len(clusters), 2)

    def test_unauthorized_case_is_rejected(self) -> None:
        data = fixture()
        data["authorized"] = False
        with self.assertRaisesRegex(ValueError, "authorized"):
            correlator.validate_case(data)

    def test_naive_timestamp_is_rejected(self) -> None:
        data = fixture()
        data["events"][0]["timestamp"] = "2026-10-01T12:00:00"
        with self.assertRaisesRegex(ValueError, "fuso"):
            correlator.validate_case(data)

    def test_manifest_is_deterministic_and_complete(self) -> None:
        root = COURSE / "fixtures" / "evidencias-demo"
        first = manifest_tool.build_manifest(root)
        second = manifest_tool.build_manifest(root)
        self.assertEqual(first, second)
        self.assertEqual(len(first["files"]), 2)
        self.assertTrue(all(len(item["sha256"]) == 64 for item in first["files"]))

    def test_manifest_rejects_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "nenhuma evidência"):
                manifest_tool.build_manifest(Path(directory))
