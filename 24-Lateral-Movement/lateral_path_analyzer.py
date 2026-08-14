#!/usr/bin/env python3
"""Encontra caminhos laterais permitidos em um grafo sintético, sem rede."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any


def find_path(data: dict[str, Any], source: str, target: str) -> list[dict[str, str]] | None:
    nodes = {str(node["id"]): node for node in data.get("nodes", []) if isinstance(node, dict) and node.get("id")}
    scoped = set(map(str, data.get("scope", [])))
    if source not in nodes or target not in nodes or source not in scoped or target not in scoped:
        return None

    graph: dict[str, list[dict[str, str]]] = {node: [] for node in nodes}
    for edge in data.get("edges", []):
        if not isinstance(edge, dict) or edge.get("enabled") is not True:
            continue
        origin, destination = str(edge.get("from", "")), str(edge.get("to", ""))
        if origin not in scoped or destination not in scoped:
            continue
        graph.get(origin, []).append(
            {
                "from": origin,
                "to": destination,
                "protocol": str(edge.get("protocol", "unknown")),
                "precondition": str(edge.get("precondition", "unspecified")),
            }
        )

    queue = deque([(source, [])])
    seen = {source}
    while queue:
        node, path = queue.popleft()
        if node == target:
            return path
        for edge in graph.get(node, []):
            if edge["to"] not in seen:
                seen.add(edge["to"])
                queue.append((edge["to"], [*path, edge]))
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()
    data = json.loads(args.graph.read_text(encoding="utf-8"))
    path = find_path(data, args.source, args.target)
    print(json.dumps({"allowed": path is not None, "steps": path}, ensure_ascii=False, indent=2))
    return 0 if path is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
