from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "08-Cloud-RedTeam" / "labs" / "analyze_events.py"
SPEC = importlib.util.spec_from_file_location("cloud_event_analyzer", SCRIPT)
assert SPEC and SPEC.loader
analyzer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyzer)


@pytest.mark.parametrize(
    ("fixture", "provider"),
    [
        ("aws-cloudtrail.jsonl", "aws"),
        ("azure-activity.jsonl", "azure"),
        ("gcp-audit.jsonl", "gcp"),
    ],
)
def test_cloud_fixture_has_one_alert_and_one_benign_event(fixture: str, provider: str) -> None:
    path = ROOT / "08-Cloud-RedTeam" / "labs" / "fixtures" / fixture
    events = analyzer.load_events(path)
    alerts = analyzer.find_alerts(events)
    assert len(events) == 2
    assert len(alerts) == 1
    assert alerts[0]["provider"] == provider
    assert all(alerts[0][field] for field in ("time", "actor", "target", "reason"))


def test_loader_reports_invalid_json_line(tmp_path) -> None:
    fixture = tmp_path / "bad.jsonl"
    fixture.write_text('{}\n{"bad"\n', encoding="utf-8")
    with pytest.raises(ValueError, match="linha 2"):
        analyzer.load_events(fixture)


def test_failed_admin_change_does_not_alert() -> None:
    event = {
        "eventSource": "iam.amazonaws.com",
        "eventName": "AttachUserPolicy",
        "errorCode": "AccessDenied",
        "requestParameters": {
            "policyArn": "arn:aws:iam::aws:policy/AdministratorAccess",
            "userName": "student",
        },
    }
    assert analyzer.find_alerts([event]) == []
