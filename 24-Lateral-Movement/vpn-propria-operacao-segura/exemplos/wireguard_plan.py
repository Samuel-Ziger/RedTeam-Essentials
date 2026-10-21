#!/usr/bin/env python3
"""Valida um plano WireGuard e imprime configurações com placeholders."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
from pathlib import Path
from typing import Any

INTERFACE_RE = re.compile(r"^[a-zA-Z0-9_.-]{1,15}$")
PLACEHOLDER_RE = re.compile(r"^<[A-Z0-9_]+>$")


def _string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} deve ser texto não vazio")
    return value.strip()


def validate_plan(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("plano deve ser objeto JSON")
    server = data.get("server")
    peers = data.get("peers")
    reserved = data.get("reserved_networks", [])
    if not isinstance(server, dict):
        raise ValueError("server deve ser objeto")
    if not isinstance(peers, list) or not peers:
        raise ValueError("peers deve ser lista não vazia")
    if not isinstance(reserved, list) or any(not isinstance(item, str) for item in reserved):
        raise ValueError("reserved_networks deve ser lista de prefixos")

    interface = _string(server.get("interface"), "server.interface")
    if not INTERFACE_RE.fullmatch(interface):
        raise ValueError("server.interface inválida")
    tunnel = ipaddress.ip_interface(_string(server.get("tunnel_ipv4"), "server.tunnel_ipv4"))
    if tunnel.version != 4:
        raise ValueError("server.tunnel_ipv4 deve ser IPv4")
    endpoint = _string(server.get("endpoint"), "server.endpoint")
    if ":" not in endpoint or any(char.isspace() for char in endpoint):
        raise ValueError("server.endpoint deve incluir host:porta")
    port = server.get("listen_port")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("server.listen_port inválida")
    _string(server.get("egress_interface"), "server.egress_interface")
    ipaddress.ip_address(_string(server.get("dns"), "server.dns"))
    server_public = _string(server.get("public_key"), "server.public_key")
    if not PLACEHOLDER_RE.fullmatch(server_public):
        raise ValueError("use placeholder explícito para server.public_key")

    reserved_networks = [ipaddress.ip_network(item, strict=False) for item in reserved]
    if any(tunnel.network.overlaps(network) for network in reserved_networks if network.version == 4):
        raise ValueError("prefixo do túnel sobrepõe reserved_networks")

    names: set[str] = set()
    addresses: set[ipaddress.IPv4Address] = {tunnel.ip}
    for index, peer in enumerate(peers):
        if not isinstance(peer, dict):
            raise ValueError(f"peers[{index}] deve ser objeto")
        name = _string(peer.get("name"), f"peers[{index}].name")
        if name in names:
            raise ValueError(f"peer duplicado: {name}")
        names.add(name)
        address = ipaddress.ip_interface(_string(peer.get("address"), f"{name}.address"))
        if address.version != 4 or address.network.prefixlen != 32:
            raise ValueError(f"{name}.address deve ser IPv4 /32")
        if address.ip not in tunnel.network:
            raise ValueError(f"{name}.address fora do prefixo do túnel")
        if address.ip in addresses:
            raise ValueError(f"endereço duplicado: {address.ip}")
        addresses.add(address.ip)
        public_key = _string(peer.get("public_key"), f"{name}.public_key")
        if not PLACEHOLDER_RE.fullmatch(public_key):
            raise ValueError(f"use placeholder explícito para {name}.public_key")
        routes = peer.get("client_allowed_ips")
        if not isinstance(routes, list) or not routes:
            raise ValueError(f"{name}.client_allowed_ips deve ser lista não vazia")
        for route in routes:
            if not isinstance(route, str):
                raise ValueError(f"rota inválida em {name}")
            ipaddress.ip_network(route, strict=False)
        keepalive = peer.get("keepalive", 0)
        if not isinstance(keepalive, int) or not 0 <= keepalive <= 65535:
            raise ValueError(f"{name}.keepalive inválido")
    return data


def render_server(plan: dict[str, Any]) -> str:
    server = plan["server"]
    lines = [
        "# TEMPLATE: substitua segredos apenas no servidor",
        "[Interface]",
        f"Address = {server['tunnel_ipv4']}",
        f"ListenPort = {server['listen_port']}",
        "PrivateKey = <SERVER_PRIVATE_KEY>",
    ]
    for peer in plan["peers"]:
        lines.extend(
            [
                "",
                "[Peer]",
                f"# {peer['name']}",
                f"PublicKey = {peer['public_key']}",
                f"AllowedIPs = {peer['address']}",
            ]
        )
    return "\n".join(lines)


def render_client(plan: dict[str, Any], peer: dict[str, Any]) -> str:
    server = plan["server"]
    lines = [
        f"# TEMPLATE: {peer['name']}; a chave privada fica neste dispositivo",
        "[Interface]",
        f"Address = {peer['address']}",
        f"PrivateKey = <{peer['name'].upper().replace('-', '_')}_PRIVATE_KEY>",
        f"DNS = {server['dns']}",
        "",
        "[Peer]",
        f"PublicKey = {server['public_key']}",
        f"Endpoint = {server['endpoint']}",
        f"AllowedIPs = {', '.join(peer['client_allowed_ips'])}",
    ]
    if peer.get("keepalive", 0):
        lines.append(f"PersistentKeepalive = {peer['keepalive']}")
    return "\n".join(lines)


def render(plan: dict[str, Any]) -> str:
    sections = ["===== SERVER wg0.conf =====", render_server(plan)]
    for peer in plan["peers"]:
        sections.extend([f"\n===== CLIENT {peer['name']} =====", render_client(plan, peer)])
    return "\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        plan = validate_plan(json.loads(args.plan.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(render(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
