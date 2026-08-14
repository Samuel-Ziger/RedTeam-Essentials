"""Helpers para importar scripts que ainda nao sao pacotes Python."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lib" / "python"))


def load_tool(name: str):
    """Carrega uma ferramenta de ``11-Python-Tools`` sem executar sua CLI."""
    path = ROOT / "11-Python-Tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"rte_test_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Nao foi possivel importar {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
