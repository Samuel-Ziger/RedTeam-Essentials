#!/usr/bin/env python3
"""Encontra caminhos autorizados em uma topologia JSON sem acessar a rede."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any


def find_path(data: dict[str, Any], source: str, target: str, port: int) -> list[str] | None:
    nodes = set(map(str, data.get("nodes", [])))
    if source not in nodes or target not in nodes:
        return None
    graph: dict[str, list[str]] = {node: [] for node in nodes}
    for edge in data.get("edges", []):
        if port in edge.get("ports", []):
            graph.get(str(edge.get("from")), []).append(str(edge.get("to")))
    queue = deque([(source, [source])])
    seen = {source}
    while queue:
        node, path = queue.popleft()
        if node == target:
            return path
        for neighbor in graph.get(node, []):
            if neighbor in nodes and neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, [*path, neighbor]))
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topology", type=Path)
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("port", type=int)
    args = parser.parse_args()
    data = json.loads(args.topology.read_text(encoding="utf-8"))
    path = find_path(data, args.source, args.target, args.port)
    print(json.dumps({"allowed": path is not None, "path": path, "port": args.port}, ensure_ascii=False))
    return 0 if path else 1


if __name__ == "__main__":
    raise SystemExit(main())
