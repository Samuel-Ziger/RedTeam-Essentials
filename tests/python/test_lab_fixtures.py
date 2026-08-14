from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_dfir_auth_fixture_is_ordered_and_synthetic() -> None:
    path = ROOT / "05-DFIR" / "labs" / "fixtures" / "auth-events.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) >= 5
    timestamps = [datetime.fromisoformat(row["timestamp_utc"].replace("Z", "+00:00")) for row in rows]
    assert timestamps == sorted(timestamps)
    assert {row["event_id"] for row in rows} >= {"4624", "4625", "4672"}
    assert all(row["user"].startswith("LAB\\") for row in rows)


def test_kubernetes_fixture_contains_positive_and_negative_examples() -> None:
    path = ROOT / "10-Container-Sec" / "labs" / "fixtures" / "k8s-audit.jsonl"
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    assert len(events) == 2
    assert any(event["verb"] == "get" for event in events)
    privileged = [
        event
        for event in events
        if any(
            container.get("securityContext", {}).get("privileged") is True
            for container in event.get("requestObject", {}).get("spec", {}).get("containers", [])
        )
    ]
    assert len(privileged) == 1
    assert privileged[0]["verb"] == "create"
