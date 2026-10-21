#!/usr/bin/env python3
"""Valida um plano de VLAN neutro e totalmente offline."""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
from typing import Any


def validate(document: dict[str, Any]) -> dict[str, int]:
    if set(document) != {"schema", "vlans", "ports"} or document.get("schema") != "rte-vlan-plan/v1":
        raise ValueError("schema ou campos de raiz inválidos")
    vlans = document["vlans"]
    ports = document["ports"]
    if not isinstance(vlans, list) or not 1 <= len(vlans) <= 4094:
        raise ValueError("vlans deve ser uma lista não vazia e limitada")
    if not isinstance(ports, list) or len(ports) > 10000:
        raise ValueError("ports deve ser uma lista limitada")

    ids: set[int] = set()
    names: set[str] = set()
    networks: list[ipaddress.IPv4Network] = []
    for index, item in enumerate(vlans):
        if not isinstance(item, dict) or set(item) != {"id", "name", "prefix", "purpose"}:
            raise ValueError(f"VLAN {index} possui estrutura inválida")
        vlan_id = item["id"]
        name = item["name"]
        if isinstance(vlan_id, bool) or not isinstance(vlan_id, int) or not 1 <= vlan_id <= 4094:
            raise ValueError(f"ID de VLAN inválido: {vlan_id!r}")
        if vlan_id in ids:
            raise ValueError(f"ID de VLAN duplicado: {vlan_id}")
        if not isinstance(name, str) or not name or name in names:
            raise ValueError(f"nome de VLAN inválido/duplicado: {name!r}")
        if not isinstance(item["purpose"], str) or not item["purpose"]:
            raise ValueError(f"VLAN {vlan_id} sem finalidade")
        network = ipaddress.ip_network(item["prefix"], strict=True)
        if network.version != 4:
            raise ValueError("este fixture exige prefixos IPv4")
        if any(network.overlaps(other) for other in networks):
            raise ValueError(f"prefixo sobreposto: {network}")
        ids.add(vlan_id)
        names.add(name)
        networks.append(network)

    port_names: set[str] = set()
    for index, port in enumerate(ports):
        if not isinstance(port, dict) or set(port) != {"name", "mode", "vlans", "native_vlan"}:
            raise ValueError(f"porta {index} possui estrutura inválida")
        name = port["name"]
        if not isinstance(name, str) or not name or name in port_names:
            raise ValueError(f"nome de porta inválido/duplicado: {name!r}")
        mode = port["mode"]
        assigned = port["vlans"]
        native = port["native_vlan"]
        if mode not in {"access", "trunk"} or not isinstance(assigned, list) or not assigned:
            raise ValueError(f"modo/VLANs inválidos na porta {name}")
        if any(isinstance(value, bool) or not isinstance(value, int) or value not in ids for value in assigned):
            raise ValueError(f"porta {name} referencia VLAN inexistente")
        if len(assigned) != len(set(assigned)):
            raise ValueError(f"porta {name} repete VLAN")
        if mode == "access" and (len(assigned) != 1 or native is not None):
            raise ValueError(f"porta access {name} deve ter uma VLAN e native null")
        if mode == "trunk" and (isinstance(native, bool) or not isinstance(native, int) or native not in assigned):
            raise ValueError(f"trunk {name} exige native_vlan permitida")
        port_names.add(name)
    return {"vlan_count": len(vlans), "port_count": len(ports), "trunk_count": sum(p["mode"] == "trunk" for p in ports)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.document.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("a raiz deve ser um objeto")
        print(json.dumps(validate(data), ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"erro: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
