#!/usr/bin/env python3
"""Audita uma descrição sanitizada de rede doméstica, totalmente offline."""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
from typing import Any

ALLOWED_KEYS = {"schema", "lan", "wifi", "management", "exposure", "recovery", "ipv6"}


def _finding(identifier: str, severity: str, message: str) -> dict[str, str]:
    return {"id": identifier, "severity": severity, "message": message}


def audit(document: dict[str, Any]) -> list[dict[str, str]]:
    if set(document) != ALLOWED_KEYS or document.get("schema") != "rte-home-network/v1":
        raise ValueError("schema ou campos de raiz inválidos")
    if not all(isinstance(document[key], dict) for key in ALLOWED_KEYS - {"schema"}):
        raise ValueError("cada seção deve ser um objeto")

    lan = document["lan"]
    try:
        network = ipaddress.ip_network(lan["prefix"], strict=True)
        start = ipaddress.ip_address(lan["dhcp_start"])
        end = ipaddress.ip_address(lan["dhcp_end"])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"LAN inválida: {exc}") from exc
    if network.version != 4 or start not in network or end not in network or int(start) > int(end):
        raise ValueError("pool DHCP fora da LAN ou invertido")

    findings: list[dict[str, str]] = []
    wifi = document["wifi"]
    security = wifi.get("security")
    if security not in {"WPA3-SAE", "WPA2-AES", "WPA2-WPA3-TRANSITION"}:
        findings.append(_finding("wifi.security", "high", "Use WPA3-SAE ou WPA2 com AES/CCMP."))
    if wifi.get("wps_enabled") is not False:
        findings.append(_finding("wifi.wps", "medium", "Desative WPS quando não for necessário."))
    if wifi.get("guest_isolation") is not True:
        findings.append(_finding("wifi.guest", "high", "Isole convidados da LAN e valide IPv4/IPv6."))

    management = document["management"]
    if management.get("wan_admin") is not False:
        findings.append(_finding("management.wan", "high", "Desative administração pela WAN."))
    if management.get("supported_firmware") is not True:
        findings.append(_finding("management.firmware", "high", "Use firmware suportado."))

    exposure = document["exposure"]
    if exposure.get("upnp_enabled") is not False:
        findings.append(_finding("exposure.upnp", "medium", "Desative ou inventarie mapeamentos UPnP."))
    forwards = exposure.get("port_forwards")
    if not isinstance(forwards, list) or len(forwards) > 50:
        raise ValueError("port_forwards deve ser lista limitada")
    if forwards:
        findings.append(_finding("exposure.forwards", "medium", "Revise dono, prazo e autenticação de cada exposição."))

    if document["ipv6"].get("firewall_inbound") is not True:
        findings.append(_finding("ipv6.firewall", "high", "Aplique política de entrada também ao IPv6."))
    recovery = document["recovery"]
    if recovery.get("encrypted_backup") is not True or recovery.get("restore_tested") is not True:
        findings.append(_finding("recovery.backup", "medium", "Proteja o backup e teste a restauração."))
    return sorted(findings, key=lambda item: (item["severity"], item["id"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.document.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("a raiz deve ser um objeto")
        print(json.dumps({"findings": audit(data)}, ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"erro: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
