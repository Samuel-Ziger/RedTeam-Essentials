#!/usr/bin/env python3
"""Simula seleção de rota e ACL first-match usando documentos offline."""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
from typing import Any


def load_document(path: Path, expected_schema: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != expected_schema:
        raise ValueError("schema inválido")
    return data


def lookup(document: dict[str, Any], destination: str) -> dict[str, Any] | None:
    if set(document) != {"schema", "routes"}:
        raise ValueError("campos inválidos no documento de rotas")
    address = ipaddress.ip_address(destination)
    routes = document["routes"]
    if not isinstance(routes, list) or len(routes) > 10000:
        raise ValueError("routes deve ser lista limitada")
    candidates: list[tuple[int, int, int, int, dict[str, Any]]] = []
    for index, route in enumerate(routes):
        if not isinstance(route, dict) or set(route) != {"prefix", "next_hop", "preference", "metric", "source"}:
            raise ValueError(f"rota {index} inválida")
        network = ipaddress.ip_network(route["prefix"], strict=True)
        preference = route["preference"]
        metric = route["metric"]
        if network.version != address.version:
            continue
        if isinstance(preference, bool) or isinstance(metric, bool) or not isinstance(preference, int) or not isinstance(metric, int) or min(preference, metric) < 0:
            raise ValueError(f"preferência/métrica inválida na rota {index}")
        next_hop = route["next_hop"]
        if next_hop != "null" and ipaddress.ip_address(next_hop).version != address.version:
            raise ValueError(f"next hop incompatível na rota {index}")
        if address in network:
            candidates.append((-network.prefixlen, preference, metric, index, route))
    if not candidates:
        return None
    selected = min(candidates)[4]
    return {**selected, "destination": str(address)}


def evaluate_acl(document: dict[str, Any], source: str, destination: str, protocol: str, port: int) -> dict[str, Any]:
    if set(document) != {"schema", "rules", "default_action"} or document["default_action"] not in {"allow", "deny"}:
        raise ValueError("documento ACL inválido")
    src = ipaddress.ip_address(source)
    dst = ipaddress.ip_address(destination)
    if src.version != dst.version or protocol not in {"tcp", "udp", "icmp", "any"} or isinstance(port, bool) or not 0 <= port <= 65535:
        raise ValueError("fluxo inválido")
    rules = document["rules"]
    if not isinstance(rules, list) or len(rules) > 10000:
        raise ValueError("rules deve ser lista limitada")
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict) or set(rule) != {"id", "action", "source", "destination", "protocol", "ports"}:
            raise ValueError(f"regra {index} inválida")
        ports = rule["ports"]
        if rule["action"] not in {"allow", "deny"} or rule["protocol"] not in {"tcp", "udp", "icmp", "any"}:
            raise ValueError(f"ação/protocolo inválido na regra {index}")
        if not isinstance(ports, list) or any(isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 65535 for value in ports):
            raise ValueError(f"portas inválidas na regra {index}")
        src_net = ipaddress.ip_network(rule["source"], strict=True)
        dst_net = ipaddress.ip_network(rule["destination"], strict=True)
        if src.version != src_net.version or dst.version != dst_net.version:
            continue
        protocol_match = rule["protocol"] in {"any", protocol}
        port_match = not ports or port in ports
        if src in src_net and dst in dst_net and protocol_match and port_match:
            return {"action": rule["action"], "rule_id": rule["id"]}
    return {"action": document["default_action"], "rule_id": "implicit-default"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    route_parser = subparsers.add_parser("lookup")
    route_parser.add_argument("document", type=Path)
    route_parser.add_argument("destination")
    acl_parser = subparsers.add_parser("acl")
    acl_parser.add_argument("document", type=Path)
    acl_parser.add_argument("source")
    acl_parser.add_argument("destination")
    acl_parser.add_argument("protocol")
    acl_parser.add_argument("port", type=int)
    args = parser.parse_args()
    try:
        if args.command == "lookup":
            result = lookup(load_document(args.document, "rte-routes/v1"), args.destination)
        else:
            result = evaluate_acl(load_document(args.document, "rte-acl/v1"), args.source, args.destination, args.protocol, args.port)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"erro: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
