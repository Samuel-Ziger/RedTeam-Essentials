#!/usr/bin/env python3
"""Correlaciona observações de recon contidas em JSON, sem acessar a rede."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def correlate(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    assets: dict[str, dict[str, Any]] = {}
    for item in data:
        host = str(item.get("host", "")).lower().rstrip(".")
        if not host:
            continue
        asset = assets.setdefault(
            host, {"host": host, "ips": set(), "asns": set(), "sources": set(), "technologies": set()}
        )
        for key, output in (("ip", "ips"), ("asn", "asns"), ("source", "sources"), ("technology", "technologies")):
            value = item.get(key)
            if value:
                asset[output].add(str(value))
    result = []
    for asset in assets.values():
        normalized = {key: sorted(value) if isinstance(value, set) else value for key, value in asset.items()}
        normalized["priority"] = len(normalized["sources"]) + len(normalized["technologies"]) + len(normalized["ips"])
        result.append(normalized)
    return sorted(result, key=lambda item: (-item["priority"], item["host"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    data = json.loads(args.fixture.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("fixture deve ser uma lista JSON")
    print(json.dumps(correlate(data), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
