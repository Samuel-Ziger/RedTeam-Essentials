#!/usr/bin/env python3
"""Correlaciona telemetria sintética por pivôs fortes, sem usar IP isolado."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

STRONG_KEYS = ("request_id", "session_id", "device")
REQUIRED_EVENT_FIELDS = ("event_id", "timestamp", "source", "kind", "action", "result")


def parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp deve ser texto ISO 8601")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("timestamp precisa de fuso ou Z")
    return parsed


def validate_case(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("caso deve ser objeto JSON")
    if data.get("authorized") is not True:
        raise ValueError("authorized deve ser true")
    if not isinstance(data.get("case_id"), str) or not data["case_id"].strip():
        raise ValueError("case_id ausente")
    events = data.get("events")
    if not isinstance(events, list) or not events:
        raise ValueError("events deve ser lista não vazia")
    ids: set[str] = set()
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"events[{index}] deve ser objeto")
        for field in REQUIRED_EVENT_FIELDS:
            if not isinstance(event.get(field), str) or not event[field].strip():
                raise ValueError(f"events[{index}].{field} ausente")
        if event["event_id"] in ids:
            raise ValueError(f"event_id duplicado: {event['event_id']}")
        ids.add(event["event_id"])
        parse_timestamp(event["timestamp"])
        for port_field in ("src_port", "dst_port"):
            if port_field in event:
                port = event[port_field]
                if not isinstance(port, int) or not 1 <= port <= 65535:
                    raise ValueError(f"{event['event_id']}.{port_field} inválida")
    return data


def correlate(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build connected components using request/session/device, never IP alone."""
    parent = list(range(len(events)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        root_left, root_right = find(left), find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    seen: dict[tuple[str, str], int] = {}
    for index, event in enumerate(events):
        for field in STRONG_KEYS:
            value = event.get(field)
            if not isinstance(value, str) or not value:
                continue
            key = (field, value)
            if key in seen:
                union(index, seen[key])
            else:
                seen[key] = index

    components: dict[int, list[dict[str, Any]]] = {}
    for index, event in enumerate(events):
        components.setdefault(find(index), []).append(event)

    clusters: list[dict[str, Any]] = []
    for members in components.values():
        members.sort(key=lambda item: parse_timestamp(item["timestamp"]))
        sources = sorted({item["source"] for item in members})
        links = {
            field: sorted({item[field] for item in members if isinstance(item.get(field), str) and item[field]})
            for field in STRONG_KEYS
        }
        if links["request_id"] and links["session_id"] and len(sources) >= 3:
            confidence = "high"
        elif (links["request_id"] or links["session_id"] or links["device"]) and len(sources) >= 2:
            confidence = "medium"
        else:
            confidence = "low"
        clusters.append(
            {
                "event_ids": [item["event_id"] for item in members],
                "start": members[0]["timestamp"],
                "end": members[-1]["timestamp"],
                "sources": sources,
                "links": links,
                "confidence": confidence,
                "note": "confiança técnica; não afirma autoria humana",
            }
        )
    clusters.sort(key=lambda item: parse_timestamp(item["start"]))
    return clusters


def render(case_id: str, clusters: list[dict[str, Any]]) -> str:
    lines = [f"CASE {case_id}", "Correlação por request/session/device; IP isolado é ignorado."]
    for index, cluster in enumerate(clusters, 1):
        links = ", ".join(
            f"{field}={values}" for field, values in cluster["links"].items() if values
        ) or "nenhum pivô forte compartilhado"
        lines.extend(
            [
                "",
                f"CLUSTER {index} confidence={cluster['confidence']}",
                f"events={','.join(cluster['event_ids'])}",
                f"sources={','.join(cluster['sources'])}",
                f"window={cluster['start']}..{cluster['end']}",
                f"links={links}",
                f"limite={cluster['note']}",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    args = parser.parse_args()
    try:
        data = validate_case(json.loads(args.case.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(render(data["case_id"], correlate(data["events"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
