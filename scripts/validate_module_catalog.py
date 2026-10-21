#!/usr/bin/env python3
"""Valida a fonte única de metadados dos módulos numerados."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

CONTRACT_FIELDS = (
    "Público",
    "Pré-requisitos",
    "Tempo estimado",
    "Ambiente",
    "Evidência final",
    "Critério de conclusão",
)
MATURITY = {"introductory", "developing", "established", "catalog"}
STATUS = {"active", "theory-only", "catalog"}


def validate(root: Path, catalog: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(catalog, dict) or catalog.get("schemaVersion") != 1:
        return ["schemaVersion deve ser 1"]
    modules = catalog.get("modules")
    if not isinstance(modules, list):
        return ["modules deve ser uma lista"]

    actual = sorted(path.name for path in root.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name))
    declared: list[str] = []
    ids: set[str] = set()
    for index, module in enumerate(modules):
        prefix = f"modules[{index}]"
        if not isinstance(module, dict):
            errors.append(f"{prefix}: entrada deve ser objeto")
            continue
        module_id = module.get("id")
        path_name = module.get("path")
        if not isinstance(module_id, str) or not re.fullmatch(r"\d{2}", module_id):
            errors.append(f"{prefix}: id invalido")
            continue
        if module_id in ids:
            errors.append(f"{prefix}: id duplicado: {module_id}")
        ids.add(module_id)
        if not isinstance(path_name, str) or not path_name.startswith(f"{module_id}-"):
            errors.append(f"{prefix}: path nao corresponde ao id")
            continue
        declared.append(path_name)
        if not isinstance(module.get("title"), str) or not module["title"].strip():
            errors.append(f"{path_name}: title ausente")
        if module.get("maturity") not in MATURITY:
            errors.append(f"{path_name}: maturity invalida")
        if module.get("status") not in STATUS:
            errors.append(f"{path_name}: status invalido")
        prerequisites = module.get("prerequisites")
        if not isinstance(prerequisites, list) or any(not isinstance(item, str) for item in prerequisites):
            errors.append(f"{path_name}: prerequisites deve ser lista de ids")
        hours = module.get("estimatedHours")
        if not isinstance(hours, dict) or any(not isinstance(hours.get(key), int) for key in ("min", "max")):
            errors.append(f"{path_name}: estimatedHours invalido")
        elif hours["min"] < 0 or hours["max"] < hours["min"]:
            errors.append(f"{path_name}: intervalo de horas invalido")

        readme = root / path_name / "README.md"
        if not readme.is_file():
            errors.append(f"{path_name}: README.md ausente")
            continue
        content = readme.read_text(encoding="utf-8")
        if "## Contrato do módulo" not in content:
            errors.append(f"{path_name}: contrato ausente")
        for field in CONTRACT_FIELDS:
            if not re.search(rf"^\|\s*{re.escape(field)}\s*\|", content, re.MULTILINE):
                errors.append(f"{path_name}: campo do contrato ausente: {field}")

    if declared != actual:
        errors.append(f"catalogo diverge dos diretorios: declarados={declared}; atuais={actual}")
    expected_ids = {name[:2] for name in actual}
    if ids != expected_ids:
        errors.append(f"ids divergem dos diretorios: declarados={sorted(ids)}; atuais={sorted(expected_ids)}")
    dependency_graph: dict[str, list[str]] = {}
    for module in modules:
        if isinstance(module, dict):
            module_id = module.get("id")
            prerequisites = module.get("prerequisites", [])
            if not isinstance(prerequisites, list):
                prerequisites = []
            if isinstance(module_id, str):
                dependency_graph[module_id] = [item for item in prerequisites if isinstance(item, str)]
            for prerequisite in prerequisites:
                if prerequisite not in ids:
                    errors.append(f"{module.get('path')}: pre-requisito desconhecido: {prerequisite}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module_id: str) -> None:
        if module_id in visiting:
            errors.append(f"ciclo de pre-requisitos detectado em {module_id}")
            return
        if module_id in visited:
            return
        visiting.add(module_id)
        for prerequisite in dependency_graph.get(module_id, []):
            if prerequisite in dependency_graph:
                visit(prerequisite)
        visiting.remove(module_id)
        visited.add(module_id)

    for module_id in dependency_graph:
        visit(module_id)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    path = args.root / "MODULE-CATALOG.json"
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERRO] catalogo ilegivel: {exc}")
        return 1
    errors = validate(args.root, catalog)
    for error in errors:
        print(f"[ERRO] {error}")
    if errors:
        return 1
    print(f"[OK] catalogo valido para {len(catalog['modules'])} modulos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
