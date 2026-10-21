#!/usr/bin/env python3
"""Analisa modelos de privacidade sintéticos sem realizar operações de rede."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, NamedTuple

VPN_MODES = {"none", "commercial", "self_hosted", "corporate"}
DNS_MODES = {"system", "encrypted", "tunnel", "unknown"}
OBSERVER_MODELS = {"local", "service", "provider", "global"}
IDENTITY_MARKERS = {"account", "email", "phone", "payment", "sso"}


class Finding(NamedTuple):
    severity: str
    activity: str
    code: str
    message: str


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} deve ser texto não vazio")
    return value.strip()


def validate_scenario(data: Any) -> dict[str, Any]:
    """Validate and normalize the small educational input schema."""
    if not isinstance(data, dict):
        raise ValueError("o cenário deve ser um objeto JSON")
    _required_string(data.get("scenario"), "scenario")
    _required_string(data.get("objective"), "objective")
    if data.get("authorized") is not True:
        raise ValueError("authorized deve ser true para este laboratório")
    activities = data.get("activities")
    if not isinstance(activities, list) or not activities:
        raise ValueError("activities deve ser uma lista não vazia")
    names: set[str] = set()
    for index, item in enumerate(activities):
        if not isinstance(item, dict):
            raise ValueError(f"activities[{index}] deve ser objeto")
        name = _required_string(item.get("name"), f"activities[{index}].name")
        if name in names:
            raise ValueError(f"atividade duplicada: {name}")
        names.add(name)
        for field in ("https", "tor_browser", "endpoint_trusted"):
            if not isinstance(item.get(field), bool):
                raise ValueError(f"{name}.{field} deve ser booleano")
        if item.get("vpn") not in VPN_MODES:
            raise ValueError(f"{name}.vpn inválido")
        if item.get("dns") not in DNS_MODES:
            raise ValueError(f"{name}.dns inválido")
        if item.get("observer_model") not in OBSERVER_MODELS:
            raise ValueError(f"{name}.observer_model inválido")
        identifiers = item.get("identifiers")
        if not isinstance(identifiers, list) or any(not isinstance(value, str) for value in identifiers):
            raise ValueError(f"{name}.identifiers deve ser lista de textos")
    return data


def analyze_activity(activity: dict[str, Any]) -> list[Finding]:
    """Return deterministic educational findings for one activity."""
    name = activity["name"]
    findings: list[Finding] = []
    if not activity["https"]:
        findings.append(Finding("high", name, "NO_HTTPS", "conteúdo pode ficar exposto fora do túnel"))
    if not activity["endpoint_trusted"]:
        findings.append(Finding("critical", name, "ENDPOINT", "endpoint não confiável precede VPN, Tor e TLS"))
    identity = sorted(IDENTITY_MARKERS.intersection(activity["identifiers"]))
    if identity:
        findings.append(
            Finding("high", name, "EXPLICIT_IDENTITY", f"identidade explícita presente: {', '.join(identity)}")
        )
    if "browser_fingerprint" in activity["identifiers"]:
        findings.append(Finding("medium", name, "FINGERPRINT", "características do cliente podem ligar sessões"))
    if activity["vpn"] != "none":
        findings.append(Finding("info", name, "TRUST_SHIFT", "a VPN desloca confiança para o gateway"))
        if activity["dns"] not in {"tunnel", "encrypted"}:
            findings.append(Finding("high", name, "DNS_PATH", "o caminho DNS não acompanha a política do túnel"))
    if activity["tor_browser"] and activity["observer_model"] == "global":
        findings.append(
            Finding("high", name, "TRAFFIC_CORRELATION", "observador amplo pode correlacionar tempo e volume")
        )
    if not activity["tor_browser"] and activity["vpn"] == "none":
        findings.append(Finding("info", name, "DIRECT_PATH", "rede/ISP e destino ocupam as posições usuais"))
    findings.append(Finding("info", name, "RESIDUAL", "nenhuma arquitetura garante anonimato absoluto"))
    return findings


def analyze(data: Any) -> list[Finding]:
    scenario = validate_scenario(data)
    return [finding for activity in scenario["activities"] for finding in analyze_activity(activity)]


def render(findings: list[Finding]) -> str:
    order = {"critical": 0, "high": 1, "medium": 2, "info": 3}
    rows = sorted(findings, key=lambda item: (order[item.severity], item.activity, item.code))
    return "\n".join(
        f"[{item.severity.upper():8}] {item.activity:<24} {item.code:<19} {item.message}" for item in rows
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.scenario.read_text(encoding="utf-8"))
        findings = analyze(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(render(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
