#!/usr/bin/env python3
"""Audit a small declarative TLS policy without opening network connections."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

FIELDS = {
    "minimumVersion",
    "maximumVersion",
    "legacyAllowed",
    "requireClientCertificate",
    "certificateAutomation",
    "validationDisabled",
}
VERSIONS = {"TLSv1.2": 12, "TLSv1.3": 13}


def audit_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict) or set(policy) != FIELDS:
        raise ValueError("policy must contain exactly the documented fields")
    minimum = policy["minimumVersion"]
    maximum = policy["maximumVersion"]
    if minimum not in VERSIONS or maximum not in VERSIONS:
        raise ValueError("only TLSv1.2 and TLSv1.3 are accepted")
    for field in FIELDS - {"minimumVersion", "maximumVersion"}:
        if not isinstance(policy[field], bool):
            raise ValueError(f"{field} must be boolean")
    if VERSIONS[minimum] > VERSIONS[maximum]:
        raise ValueError("minimumVersion exceeds maximumVersion")
    findings: list[str] = []
    if minimum != "TLSv1.3":
        findings.append("TLSv1.2 compatibility requires an owned, time-bounded exception")
    if policy["legacyAllowed"]:
        findings.append("legacy protocol or cipher fallback is enabled")
    if policy["validationDisabled"]:
        findings.append("certificate validation must never be disabled")
    if not policy["certificateAutomation"]:
        findings.append("certificate renewal is not automated")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.policy.read_text(encoding="utf-8"))
        findings = audit_policy(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps({"findings": findings, "passed": not findings}, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
