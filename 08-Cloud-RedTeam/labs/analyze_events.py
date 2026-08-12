#!/usr/bin/env python3
"""Detecta concessões administrativas em fixtures AWS, Azure e GCP."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def load_events(path: Path) -> list[dict[str, Any]]:
    """Carrega JSON Lines e informa a linha inválida ao operador."""
    events: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"linha {number}: JSON inválido: {exc.msg}") from exc
        if not isinstance(event, dict):
            raise ValueError(f"linha {number}: evento deve ser um objeto")
        events.append(event)
    return events


def _aws_alert(event: dict[str, Any]) -> dict[str, str] | None:
    if event.get("eventSource") != "iam.amazonaws.com" or event.get("eventName") != "AttachUserPolicy":
        return None
    request = event.get("requestParameters", {})
    policy = str(request.get("policyArn", ""))
    if not policy.endswith("/AdministratorAccess") or event.get("errorCode"):
        return None
    return {
        "provider": "aws",
        "time": str(event.get("eventTime", "")),
        "actor": str(event.get("userIdentity", {}).get("arn", "unknown")),
        "target": str(request.get("userName", "unknown")),
        "reason": "AdministratorAccess anexado a usuário IAM",
    }


def _azure_alert(event: dict[str, Any]) -> dict[str, str] | None:
    operation = str(event.get("operationName", {}).get("value", ""))
    properties = event.get("properties", {})
    if operation != "Microsoft.Authorization/roleAssignments/write":
        return None
    if str(event.get("status", {}).get("value", "")).lower() != "succeeded":
        return None
    if properties.get("roleDefinitionName") != "Owner":
        return None
    return {
        "provider": "azure",
        "time": str(event.get("eventTimestamp", "")),
        "actor": str(event.get("caller", "unknown")),
        "target": str(properties.get("principalId", "unknown")),
        "reason": "role Owner atribuída no Azure RBAC",
    }


def _gcp_alert(event: dict[str, Any]) -> dict[str, str] | None:
    proto = event.get("protoPayload", {})
    if proto.get("methodName") != "SetIamPolicy" or proto.get("status", {}).get("code", 0) != 0:
        return None
    bindings = proto.get("serviceData", {}).get("policyDelta", {}).get("bindingDeltas", [])
    owners = [item for item in bindings if item.get("action") == "ADD" and item.get("role") == "roles/owner"]
    if not owners:
        return None
    return {
        "provider": "gcp",
        "time": str(event.get("timestamp", "")),
        "actor": str(proto.get("authenticationInfo", {}).get("principalEmail", "unknown")),
        "target": str(owners[0].get("member", "unknown")),
        "reason": "binding roles/owner adicionado à IAM policy",
    }


def find_alerts(events: Iterable[dict[str, Any]]) -> list[dict[str, str]]:
    """Normaliza alertas dos três formatos, preservando eventos benignos."""
    alerts: list[dict[str, str]] = []
    for event in events:
        for detector in (_aws_alert, _azure_alert, _gcp_alert):
            alert = detector(event)
            if alert:
                alerts.append(alert)
                break
    return alerts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    try:
        events = load_events(args.fixture)
    except (OSError, ValueError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 2
    alerts = find_alerts(events)
    print(json.dumps({"events": len(events), "alerts": alerts}, ensure_ascii=False, indent=2))
    return 1 if not alerts else 0


if __name__ == "__main__":
    raise SystemExit(main())
