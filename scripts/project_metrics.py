#!/usr/bin/env python3
"""Gera métricas reproduzíveis de conteúdo e qualidade do repositório."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = re.compile(r"^\d{2}-")
CONTRACT_FIELDS = (
    "Público",
    "Pré-requisitos",
    "Tempo estimado",
    "Ambiente",
    "Evidência final",
    "Critério de conclusão",
)
EXCLUDED_PARTS = {".git", ".pytest_cache", ".ruff_cache", "__pycache__", "node_modules"}
EXCLUDED_PREFIXES = (
    ("study-app", "dist"),
    ("study-app", "public", "generated"),
)


def is_source_file(path: Path, root: Path) -> bool:
    """Ignora caches e artefatos reproduzíveis ao calcular o inventário."""
    relative = path.relative_to(root)
    if EXCLUDED_PARTS.intersection(relative.parts):
        return False
    return not any(relative.parts[: len(prefix)] == prefix for prefix in EXCLUDED_PREFIXES)


def is_test_file(path: Path) -> bool:
    name = path.name
    return (
        (name.startswith("test_") and path.suffix in {".py", ".sh"})
        or name.endswith(".test.js")
        or name.endswith(".Tests.ps1")
        or (name.startswith("Test") and path.suffix == ".java")
    )


def collect(root: Path = ROOT) -> dict[str, int]:
    modules = sorted(path for path in root.iterdir() if path.is_dir() and MODULE.match(path.name))
    files = [path for path in root.rglob("*") if path.is_file() and is_source_file(path, root)]
    markdown = [path for path in files if path.suffix.lower() == ".md"]
    readmes = [(module / "README.md").read_text(encoding="utf-8") for module in modules]
    contracts = sum("## Contrato do módulo" in content for content in readmes)
    complete_contracts = sum(
        "## Contrato do módulo" in content and all(field in content for field in CONTRACT_FIELDS) for content in readmes
    )
    tests = [path for path in files if is_test_file(path)]
    fixtures = [path for path in files if "fixtures" in path.relative_to(root).parts]
    workflows = [
        path
        for path in (root / ".github/workflows").glob("*")
        if path.is_file() and path.suffix in {".yml", ".yaml"}
    ]
    return {
        "ci_workflows": len(workflows),
        "modules": len(modules),
        "modules_with_contract": contracts,
        "modules_with_complete_contract": complete_contracts,
        "markdown_documents": len(markdown),
        "test_files": len(tests),
        "fixture_files": len(fixtures),
    }


def main() -> None:
    print(json.dumps(collect(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
