#!/usr/bin/env python3
"""Valida invariantes do layer MITRE ATT&CK Navigator sem dependências externas."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TECHNIQUE_ID = re.compile(r"^T\d{4}(?:\.\d{3})?$")
TACTICS = {
    "reconnaissance",
    "resource-development",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "defense-evasion",
    "credential-access",
    "discovery",
    "lateral-movement",
    "collection",
    "command-and-control",
    "exfiltration",
    "impact",
}


def validate_layer(layer: Any) -> list[str]:
    """Retorna erros estruturais e semânticos encontrados no layer."""
    errors: list[str] = []
    if not isinstance(layer, dict):
        return ["a raiz deve ser um objeto JSON"]

    for key in ("name", "versions", "domain", "techniques"):
        if key not in layer:
            errors.append(f"campo obrigatório ausente: {key}")
    if layer.get("domain") != "enterprise-attack":
        errors.append("domain deve ser enterprise-attack")

    versions = layer.get("versions")
    if not isinstance(versions, dict) or not all(versions.get(key) for key in ("attack", "navigator", "layer")):
        errors.append("versions deve informar attack, navigator e layer")

    techniques = layer.get("techniques")
    if not isinstance(techniques, list) or not techniques:
        errors.append("techniques deve ser uma lista não vazia")
        return errors

    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(techniques):
        prefix = f"techniques[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} deve ser um objeto")
            continue
        technique_id = item.get("techniqueID")
        tactic = item.get("tactic")
        if not isinstance(technique_id, str) or not TECHNIQUE_ID.fullmatch(technique_id):
            errors.append(f"{prefix}.techniqueID inválido: {technique_id!r}")
        if tactic not in TACTICS:
            errors.append(f"{prefix}.tactic inválida: {tactic!r}")
        pair = (str(technique_id), str(tactic))
        if pair in seen:
            errors.append(f"técnica/tática duplicada: {pair[0]} / {pair[1]}")
        seen.add(pair)
        score = item.get("score")
        if score is not None and (
            isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100
        ):
            errors.append(f"{prefix}.score deve estar entre 0 e 100")
        if not isinstance(item.get("enabled"), bool):
            errors.append(f"{prefix}.enabled deve ser booleano")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="MITRE-ATTACK-MAPPING.json")
    args = parser.parse_args()
    path = Path(args.path)
    try:
        layer = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERRO] Não foi possível ler {path}: {exc}", file=sys.stderr)
        return 1
    errors = validate_layer(layer)
    if errors:
        for error in errors:
            print(f"[ERRO] {error}", file=sys.stderr)
        return 1
    print(f"[OK] {path}: {len(layer['techniques'])} entradas válidas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
