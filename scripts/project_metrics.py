#!/usr/bin/env python3
"""Gera métricas reproduzíveis de conteúdo e qualidade do repositório."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = re.compile(r"^\d{2}-")


def collect(root: Path = ROOT) -> dict[str, int]:
    modules = sorted(path for path in root.iterdir() if path.is_dir() and MODULE.match(path.name))
    markdown = [path for path in root.rglob("*.md") if ".git" not in path.parts]
    contracts = sum("## Contrato do módulo" in (module / "README.md").read_text(encoding="utf-8") for module in modules)
    tests = [path for path in (root / "tests").rglob("*") if path.is_file() and "__pycache__" not in path.parts]
    fixtures = [path for path in root.rglob("*") if path.is_file() and "fixtures" in path.parts]
    return {
        "modules": len(modules),
        "modules_with_contract": contracts,
        "markdown_documents": len(markdown),
        "test_files": len(tests),
        "fixture_files": len(fixtures),
    }


def main() -> None:
    print(json.dumps(collect(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
