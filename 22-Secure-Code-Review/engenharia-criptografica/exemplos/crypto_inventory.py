#!/usr/bin/env python3
"""Validate and prioritize a small offline cryptographic inventory."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT_FIELDS = {"schemaVersion", "assets"}
ASSET_FIELDS = {
    "asset",
    "owner",
    "use",
    "algorithm",
    "status",
    "dataYears",
    "externallyExposed",
    "migrationTarget",
    "deadline",
}
STATUSES = {"current", "deprecated", "experimental"}
WEAK = {"MD5", "SHA-1", "DES", "3DES", "RC4"}
QUANTUM_VULNERABLE = {"RSA", "RSA-OAEP", "RSA-PSS", "DH", "ECDH", "ECDSA", "Ed25519", "X25519"}


def _required_text(item: dict[str, Any], field: str) -> str:
    value = item[field]
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise ValueError(f"{field} must contain 1 to 128 characters")
    return value.strip()


def validate_inventory(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, dict) or set(data) != ROOT_FIELDS or data.get("schemaVersion") != 1:
        raise ValueError("inventory root or schemaVersion is invalid")
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("assets must be a non-empty list")
    names: set[str] = set()
    for item in assets:
        if not isinstance(item, dict) or set(item) != ASSET_FIELDS:
            raise ValueError("each asset must contain exactly the documented fields")
        name = _required_text(item, "asset")
        _required_text(item, "owner")
        _required_text(item, "use")
        _required_text(item, "algorithm")
        if name in names:
            raise ValueError(f"duplicate asset: {name}")
        names.add(name)
        if item["status"] not in STATUSES:
            raise ValueError(f"invalid status for {name}")
        if not isinstance(item["dataYears"], int) or not 0 <= item["dataYears"] <= 100:
            raise ValueError(f"invalid dataYears for {name}")
        if not isinstance(item["externallyExposed"], bool):
            raise ValueError(f"externallyExposed must be boolean for {name}")
        for field in ("migrationTarget", "deadline"):
            if not isinstance(item[field], str) or len(item[field]) > 256:
                raise ValueError(f"invalid {field} for {name}")
        if item["deadline"]:
            try:
                date.fromisoformat(item["deadline"])
            except ValueError as exc:
                raise ValueError(f"invalid deadline for {name}") from exc
    return assets


def audit_inventory(data: Any, *, today: date | None = None) -> list[dict[str, str]]:
    current = today or date.today()
    assets = validate_inventory(data)
    findings: list[dict[str, str]] = []
    for item in assets:
        algorithm = item["algorithm"]
        name = item["asset"]
        if algorithm in WEAK:
            findings.append({"asset": name, "priority": "critical", "reason": f"{algorithm} is deprecated"})
        if item["status"] == "deprecated" and algorithm not in WEAK:
            findings.append({"asset": name, "priority": "high", "reason": "asset is marked deprecated"})
        quantum_priority = item["dataYears"] >= 5 or item["externallyExposed"]
        if algorithm in QUANTUM_VULNERABLE and quantum_priority:
            findings.append(
                {
                    "asset": name,
                    "priority": "high",
                    "reason": "quantum-vulnerable public-key use needs a migration plan",
                }
            )
            if not item["migrationTarget"] or not item["deadline"]:
                findings.append(
                    {"asset": name, "priority": "high", "reason": "PQC migration target or deadline is missing"}
                )
        if item["status"] == "experimental":
            findings.append(
                {"asset": name, "priority": "medium", "reason": "experimental cryptography needs an isolation gate"}
            )
        if item["deadline"] and date.fromisoformat(item["deadline"]) < current:
            findings.append({"asset": name, "priority": "critical", "reason": "migration deadline has passed"})
    order = {"critical": 0, "high": 1, "medium": 2}
    return sorted(findings, key=lambda finding: (order[finding["priority"]], finding["asset"], finding["reason"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.inventory.read_text(encoding="utf-8"))
        findings = audit_inventory(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps({"findings": findings}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
