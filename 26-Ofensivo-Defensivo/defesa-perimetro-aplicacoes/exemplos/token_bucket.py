#!/usr/bin/env python3
"""Simula rate limiting token-bucket com tempo fornecido pela fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def validate_document(document: object) -> dict[str, Any]:
    """Validate a deterministic simulation document."""
    if not isinstance(document, dict):
        raise ValueError("documento deve ser objeto JSON")
    if document.get("authorized") is not True:
        raise ValueError("authorized deve ser true")
    capacity = document.get("capacity")
    refill = document.get("refill_per_second")
    if isinstance(capacity, bool) or not isinstance(capacity, (int, float)) or capacity <= 0:
        raise ValueError("capacity deve ser positiva")
    if isinstance(refill, bool) or not isinstance(refill, (int, float)) or refill < 0:
        raise ValueError("refill_per_second deve ser não negativo")
    events = document.get("events")
    if not isinstance(events, list) or not events:
        raise ValueError("events deve ser lista não vazia")
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"events[{index}] deve ser objeto")
        if not isinstance(event.get("key"), str) or not event["key"]:
            raise ValueError("event.key deve ser string")
        for field in ("at", "cost"):
            value = event.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"event.{field} deve ser número não negativo")
        if event["cost"] == 0:
            raise ValueError("event.cost deve ser maior que zero")
    return document


def simulate(document: object) -> dict[str, Any]:
    """Run independent buckets keyed by the fixture's key field."""
    data = validate_document(document)
    capacity = float(data["capacity"])
    refill = float(data["refill_per_second"])
    state: dict[str, dict[str, float]] = {}
    decisions: list[dict[str, Any]] = []
    for index, event in enumerate(data["events"]):
        key = event["key"]
        now = float(event["at"])
        cost = float(event["cost"])
        bucket = state.setdefault(key, {"tokens": capacity, "last": now})
        if now < bucket["last"]:
            raise ValueError(f"tempo regressivo para a chave {key} no evento {index}")
        elapsed = now - bucket["last"]
        bucket["tokens"] = min(capacity, bucket["tokens"] + elapsed * refill)
        bucket["last"] = now
        allowed = bucket["tokens"] >= cost
        if allowed:
            bucket["tokens"] -= cost
        decisions.append(
            {
                "index": index,
                "key": key,
                "at": now,
                "cost": cost,
                "allowed": allowed,
                "tokens_remaining": round(bucket["tokens"], 6),
            }
        )
    allowed_count = sum(1 for item in decisions if item["allowed"])
    return {
        "algorithm": "token-bucket",
        "capacity": capacity,
        "refill_per_second": refill,
        "summary": {"allowed": allowed_count, "rejected": len(decisions) - allowed_count},
        "decisions": decisions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.fixture.read_text(encoding="utf-8"))
        result = simulate(document)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
