#!/usr/bin/env python3
"""Classifica eventos HTTP sintéticos com um score explicável e offline."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED_EVENT_FIELDS = {
    "event_id",
    "timestamp",
    "client_type",
    "rate_per_minute",
    "distinct_paths_5m",
    "auth_failures_10m",
    "anomaly_score",
    "verified_bot",
    "challenge_passed",
}


def parse_timestamp(value: object) -> datetime:
    """Parse an aware ISO-8601 timestamp."""
    if not isinstance(value, str):
        raise ValueError("timestamp deve ser string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"timestamp inválido: {value}") from exc
    if parsed.tzinfo is None:
        raise ValueError("timestamp precisa de fuso")
    return parsed


def _non_negative_number(event: dict[str, Any], field: str) -> float:
    value = event[field]
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ValueError(f"{field} deve ser número não negativo")
    return float(value)


def validate_document(document: object) -> dict[str, Any]:
    """Validate the explicit authorization and event schema."""
    if not isinstance(document, dict):
        raise ValueError("documento deve ser objeto JSON")
    if document.get("authorized") is not True:
        raise ValueError("authorized deve ser true para fixtures de laboratório")
    events = document.get("events")
    if not isinstance(events, list) or not events:
        raise ValueError("events deve ser uma lista não vazia")
    seen: set[str] = set()
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"events[{index}] deve ser objeto")
        missing = REQUIRED_EVENT_FIELDS - event.keys()
        if missing:
            raise ValueError(f"events[{index}] sem campos: {sorted(missing)}")
        event_id = event["event_id"]
        if not isinstance(event_id, str) or not event_id or event_id in seen:
            raise ValueError("event_id deve ser string única")
        seen.add(event_id)
        parse_timestamp(event["timestamp"])
        if event["client_type"] not in {"browser", "api"}:
            raise ValueError("client_type deve ser browser ou api")
        for field in ("rate_per_minute", "distinct_paths_5m", "auth_failures_10m", "anomaly_score"):
            _non_negative_number(event, field)
        for field in ("verified_bot", "challenge_passed"):
            if not isinstance(event[field], bool):
                raise ValueError(f"{field} deve ser booleano")
        if "js_state" in event and not isinstance(event["js_state"], bool):
            raise ValueError("js_state deve ser booleano")
        if "api_authenticated" in event and not isinstance(event["api_authenticated"], bool):
            raise ValueError("api_authenticated deve ser booleano")
    return document


def score_event(event: dict[str, Any]) -> dict[str, Any]:
    """Return a transparent educational score for one validated event."""
    score = 0
    reasons: list[str] = []

    rate = float(event["rate_per_minute"])
    if rate > 120:
        score += 30
        reasons.append("very_high_rate:+30")
    elif rate > 60:
        score += 15
        reasons.append("high_rate:+15")

    failures = float(event["auth_failures_10m"])
    if failures >= 8:
        score += 30
        reasons.append("many_auth_failures:+30")
    elif failures >= 3:
        score += 15
        reasons.append("auth_failures:+15")

    paths = float(event["distinct_paths_5m"])
    if paths >= 25:
        score += 20
        reasons.append("broad_path_enumeration:+20")
    elif paths >= 10:
        score += 10
        reasons.append("path_enumeration:+10")

    anomaly = float(event["anomaly_score"])
    if anomaly >= 5:
        score += 30
        reasons.append("high_waf_anomaly:+30")
    elif anomaly >= 1:
        score += 10
        reasons.append("waf_anomaly:+10")

    if event["client_type"] == "browser" and not event.get("js_state", False):
        score += 10
        reasons.append("missing_browser_state:+10")
    if event["client_type"] == "api" and event.get("api_authenticated", False):
        score -= 20
        reasons.append("authenticated_api:-20")
    if event["verified_bot"]:
        score -= 25
        reasons.append("verified_bot:-25")
    if event["challenge_passed"]:
        score -= 20
        reasons.append("recent_challenge:-20")

    score = max(0, min(100, score))
    if score >= 70:
        action = "block"
    elif score >= 45:
        action = "rate_limit"
    elif score >= 25 and event["client_type"] == "browser":
        action = "challenge"
    elif score >= 25:
        action = "rate_limit"
    else:
        action = "observe"
    return {"event_id": event["event_id"], "score": score, "action": action, "reasons": reasons}


def analyze(document: object) -> dict[str, Any]:
    """Validate and analyze a complete fixture."""
    validated = validate_document(document)
    results = [score_event(event) for event in validated["events"]]
    actions: dict[str, int] = {}
    for item in results:
        action = str(item["action"])
        actions[action] = actions.get(action, 0) + 1
    return {
        "model": "educational-edge-risk-v1",
        "limitations": "score não prova autoria e exige validação local",
        "actions": actions,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.fixture.read_text(encoding="utf-8"))
        result = analyze(document)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
