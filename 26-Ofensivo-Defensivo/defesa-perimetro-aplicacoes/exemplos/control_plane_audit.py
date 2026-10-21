#!/usr/bin/env python3
"""Audita uma política sintética de edge sem acessar infraestrutura."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read_path(document: dict[str, Any], dotted: str) -> object:
    current: object = document
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def validate_policy(document: object) -> dict[str, Any]:
    """Validate the top-level policy contract."""
    if not isinstance(document, dict):
        raise ValueError("política deve ser objeto JSON")
    if document.get("authorized") is not True:
        raise ValueError("authorized deve ser true")
    version = document.get("policy_version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("policy_version é obrigatória")
    return document


def audit(document: object) -> dict[str, Any]:
    """Evaluate explicit security invariants and return evidence."""
    policy = validate_policy(document)
    expected: tuple[tuple[str, object, str], ...] = (
        ("network.ingress_default", "deny", "entrada nega por padrão"),
        ("network.egress_default", "deny", "saída nega por padrão"),
        ("network.ipv6_covered", True, "IPv6 tem política explícita"),
        ("network.admin_public", False, "administração não é pública"),
        ("origin.direct_access", False, "origem direta está fechada"),
        ("origin.only_trusted_edge", True, "origem aceita somente a borda"),
        ("origin.tls_mode", "strict", "TLS até a origem é estrito"),
        ("origin.edge_authentication", True, "edge se autentica na origem"),
        ("waf.detection_first", True, "rollout começa em detecção"),
        ("waf.managed_rules", True, "regras gerenciadas estão ativas"),
        ("waf.change_review", True, "mudanças de regra têm revisão"),
        ("waf.exception_expiry", True, "exceções têm expiração"),
        ("challenge.server_validation", True, "desafio é validado no servidor"),
        ("challenge.single_use", True, "token de desafio é de uso único"),
        ("challenge.hostname_action_binding", True, "hostname e action são validados"),
        ("identity.admin_mfa", "phishing-resistant", "admin usa MFA resistente a phishing"),
        ("identity.recovery_protected", True, "recuperação tem proteção equivalente"),
        ("identity.break_glass_monitored", True, "break-glass é monitorado"),
        ("observability.request_id_all_layers", True, "request ID cruza as camadas"),
        ("observability.secret_redaction", True, "segredos são removidos dos logs"),
        ("observability.config_audit", True, "configuração gera auditoria"),
        ("operations.canary", True, "mudança usa canário"),
        ("operations.rollback_tested", True, "rollback foi testado"),
    )
    checks: list[dict[str, Any]] = []
    for path, expected_value, message in expected:
        actual = _read_path(policy, path)
        checks.append(
            {
                "control": path,
                "passed": actual == expected_value,
                "expected": expected_value,
                "actual": actual,
                "message": message,
            }
        )

    max_age = _read_path(policy, "challenge.max_token_age_seconds")
    age_passed = isinstance(max_age, int) and not isinstance(max_age, bool) and 0 < max_age <= 300
    checks.append(
        {
            "control": "challenge.max_token_age_seconds",
            "passed": age_passed,
            "expected": "1..300",
            "actual": max_age,
            "message": "token expira em no máximo cinco minutos",
        }
    )

    limits = _read_path(policy, "rate_limits")
    rate_passed = (
        isinstance(limits, list)
        and len(limits) >= 2
        and all(isinstance(item, dict) and item.get("route") and item.get("key") for item in limits)
    )
    checks.append(
        {
            "control": "rate_limits",
            "passed": rate_passed,
            "expected": "ao menos duas rotas com chave explícita",
            "actual": len(limits) if isinstance(limits, list) else None,
            "message": "limites protegem jornadas e isolam consumidores",
        }
    )

    failed = [item["control"] for item in checks if not item["passed"]]
    return {
        "policy_version": policy["policy_version"],
        "passed": not failed,
        "summary": {"checks": len(checks), "failed": len(failed)},
        "failed_controls": failed,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.policy.read_text(encoding="utf-8"))
        result = audit(document)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
