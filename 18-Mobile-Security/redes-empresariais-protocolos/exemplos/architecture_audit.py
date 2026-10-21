#!/usr/bin/env python3
"""Valida invariantes básicas de uma arquitetura de rede sintética."""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
from typing import Any


def audit(document: dict[str, Any]) -> dict[str, int]:
    if set(document) != {"schema", "sites", "services", "slos"} or document.get("schema") != "rte-architecture/v1":
        raise ValueError("schema ou raiz inválida")
    sites, services, slos = document["sites"], document["services"], document["slos"]
    if not isinstance(sites, list) or not 1 <= len(sites) <= 1000:
        raise ValueError("sites deve ser lista não vazia e limitada")
    if not isinstance(services, list) or not isinstance(slos, list) or len(services) > 10000 or len(slos) > 10000:
        raise ValueError("services/slos inválidos")
    site_ids: set[str] = set()
    networks: list[ipaddress._BaseNetwork] = []
    for index, site in enumerate(sites):
        if not isinstance(site, dict) or set(site) != {"id", "owner", "prefixes", "failure_domain"}:
            raise ValueError(f"site {index} inválido")
        if not all(isinstance(site[key], str) and site[key] for key in ("id", "owner", "failure_domain")):
            raise ValueError(f"site {index} sem id/owner/domínio")
        if site["id"] in site_ids:
            raise ValueError(f"site duplicado: {site['id']}")
        if not isinstance(site["prefixes"], list) or not site["prefixes"]:
            raise ValueError(f"site {site['id']} sem prefixo")
        for raw in site["prefixes"]:
            network = ipaddress.ip_network(raw, strict=True)
            if any(network.version == other.version and network.overlaps(other) for other in networks):
                raise ValueError(f"prefixo sobreposto: {network}")
            networks.append(network)
        site_ids.add(site["id"])

    service_ids: set[str] = set()
    for index, service in enumerate(services):
        if not isinstance(service, dict) or set(service) != {"id", "owner", "sites", "criticality"}:
            raise ValueError(f"serviço {index} inválido")
        if service["id"] in service_ids or not service["id"] or not service["owner"]:
            raise ValueError("serviço duplicado ou sem owner")
        if service["criticality"] not in {"low", "medium", "high", "critical"}:
            raise ValueError("criticidade inválida")
        if not isinstance(service["sites"], list) or not service["sites"] or any(site not in site_ids for site in service["sites"]):
            raise ValueError("serviço referencia site inexistente")
        service_ids.add(service["id"])

    slo_services: set[str] = set()
    for index, slo in enumerate(slos):
        if not isinstance(slo, dict) or set(slo) != {"service", "sli", "target", "window_days"}:
            raise ValueError(f"SLO {index} inválido")
        if slo["service"] not in service_ids or slo["service"] in slo_services:
            raise ValueError("SLO ausente/duplicado para serviço")
        if not isinstance(slo["target"], (int, float)) or isinstance(slo["target"], bool) or not 0 < slo["target"] <= 100:
            raise ValueError("target SLO inválido")
        if isinstance(slo["window_days"], bool) or not isinstance(slo["window_days"], int) or not 1 <= slo["window_days"] <= 365:
            raise ValueError("janela SLO inválida")
        slo_services.add(slo["service"])
    missing = service_ids - slo_services
    if missing:
        raise ValueError(f"serviços sem SLO: {sorted(missing)}")
    return {"sites": len(site_ids), "prefixes": len(networks), "services": len(service_ids), "slos": len(slo_services)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.document.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("raiz deve ser objeto")
        print(json.dumps(audit(data), ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"erro: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
