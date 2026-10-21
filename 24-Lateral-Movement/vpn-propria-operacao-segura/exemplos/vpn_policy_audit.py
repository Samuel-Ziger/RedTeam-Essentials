#!/usr/bin/env python3
"""Audita uma política sintética de VPN sem acessar o sistema ou a rede."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOOLEAN_CONTROLS = {
    "owned_or_authorized": "a infraestrutura precisa ser própria ou autorizada",
    "out_of_band_console_tested": "teste o console fora de banda antes do firewall",
    "backup_restore_tested": "backup sem restauração testada não é recuperação",
    "individual_peer_keys": "use uma chave por dispositivo",
    "private_keys_outside_repository": "mantenha chaves privadas fora do repositório",
    "minimum_firewall": "aplique política mínima de entrada e encaminhamento",
    "central_admin_logs": "preserve eventos administrativos centralmente",
    "patch_process": "defina atualização, teste e rollback",
    "revocation_runbook": "defina revogação de peers",
}


def validate_policy(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("política deve ser objeto JSON")
    for field in BOOLEAN_CONTROLS:
        if not isinstance(data.get(field), bool):
            raise ValueError(f"{field} deve ser booleano")
    for field in ("data_retention_days", "peer_review_days"):
        value = data.get(field)
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"{field} deve ser inteiro positivo")
    if data.get("dns_policy") not in {"tunnel", "split", "local", "documented_fallback"}:
        raise ValueError("dns_policy inválida")
    if data.get("ipv6_policy") not in {"full_support", "explicit_block", "split"}:
        raise ValueError("ipv6_policy inválida")
    if data.get("failure_policy") not in {"fail_closed", "documented_fallback"}:
        raise ValueError("failure_policy inválida")
    return data


def audit(data: Any) -> list[dict[str, str]]:
    policy = validate_policy(data)
    findings: list[dict[str, str]] = []
    for field, message in BOOLEAN_CONTROLS.items():
        if not policy[field]:
            severity = "critical" if field in {"owned_or_authorized", "private_keys_outside_repository"} else "high"
            findings.append({"severity": severity, "control": field, "message": message})
    if policy["data_retention_days"] > 90:
        findings.append(
            {
                "severity": "medium",
                "control": "data_retention_days",
                "message": "justifique retenção operacional superior a 90 dias",
            }
        )
    if policy["peer_review_days"] > 180:
        findings.append(
            {
                "severity": "medium",
                "control": "peer_review_days",
                "message": "revise peers ao menos semestralmente",
            }
        )
    if not findings:
        findings.append({"severity": "info", "control": "baseline", "message": "controles declarados presentes"})
    return findings


def render(findings: list[dict[str, str]]) -> str:
    return "\n".join(
        f"[{item['severity'].upper():8}] {item['control']:<34} {item['message']}" for item in findings
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    try:
        findings = audit(json.loads(args.policy.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(render(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
