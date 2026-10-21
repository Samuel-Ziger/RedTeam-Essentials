#!/usr/bin/env python3
"""Audit structural metadata in an offline macOS configuration profile."""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import uuid
from pathlib import Path
from typing import Any

IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?$")
SENSITIVE_KEY_RE = re.compile(r"(?:password|secret|token|privatekey)", re.IGNORECASE)


def valid_uuid(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return str(uuid.UUID(value)).upper() == value.upper()
    except ValueError:
        return False


def audit(document: object) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    payloads: list[dict[str, str]] = []
    identifiers: set[str] = set()
    uuids: set[str] = set()

    if not isinstance(document, dict):
        return {"schema": "rte.macos.profile-audit/v1", "valid": False, "errors": ["root must be a dictionary"], "warnings": [], "payloads": []}
    if document.get("PayloadType") != "Configuration":
        errors.append("root PayloadType must be Configuration")
    content = document.get("PayloadContent")
    if not isinstance(content, list):
        errors.append("root PayloadContent must be an array")
        content = []

    all_payloads = [("root", document), *((f"payload[{index}]", item) for index, item in enumerate(content))]
    for location, payload in all_payloads:
        if not isinstance(payload, dict):
            errors.append(f"{location} must be a dictionary")
            continue
        identifier = payload.get("PayloadIdentifier")
        payload_uuid = payload.get("PayloadUUID")
        payload_type = payload.get("PayloadType")
        if not isinstance(identifier, str) or not IDENTIFIER_RE.fullmatch(identifier):
            errors.append(f"{location} has invalid PayloadIdentifier")
        elif identifier in identifiers:
            errors.append(f"duplicate PayloadIdentifier: {identifier}")
        else:
            identifiers.add(identifier)
        if not valid_uuid(payload_uuid):
            errors.append(f"{location} has invalid PayloadUUID")
        elif payload_uuid.upper() in uuids:
            errors.append(f"duplicate PayloadUUID: {payload_uuid}")
        else:
            uuids.add(payload_uuid.upper())
        if not isinstance(payload_type, str) or not payload_type:
            errors.append(f"{location} has invalid PayloadType")
        for key in payload:
            if SENSITIVE_KEY_RE.search(str(key)):
                warnings.append(f"{location} contains potentially sensitive key: {key}")
        payloads.append(
            {
                "location": location,
                "identifier": str(identifier or ""),
                "type": str(payload_type or ""),
                "uuid": str(payload_uuid or ""),
            }
        )
    return {
        "schema": "rte.macos.profile-audit/v1",
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "payloads": payloads,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        with args.path.open("rb") as stream:
            result = audit(plistlib.load(stream))
    except (OSError, plistlib.InvalidFileException) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
