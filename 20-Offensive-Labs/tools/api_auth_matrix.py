#!/usr/bin/env python3
"""Analisa resultados HTTP offline em busca de candidatos BOLA/BFLA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def analyze(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    findings = []
    for row in rows:
        status = int(row.get("status", 0))
        if not 200 <= status < 300:
            continue
        principal = str(row.get("principal", "anonymous"))
        owner = str(row.get("owner", ""))
        function = str(row.get("function", "user"))
        role = str(row.get("role", "anonymous"))
        if owner and principal != owner:
            findings.append({"type": "BOLA", "principal": principal, "resource": str(row.get("resource", ""))})
        if function == "admin" and role != "admin":
            findings.append({"type": "BFLA", "principal": principal, "resource": str(row.get("resource", ""))})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    rows = json.loads(args.fixture.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise SystemExit("fixture deve ser uma lista JSON")
    print(json.dumps({"findings": analyze(rows)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
