from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "21-Network-Pivoting" / "path_analyzer.py"
SPEC = importlib.util.spec_from_file_location("path_analyzer", SCRIPT)
assert SPEC and SPEC.loader
analyzer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyzer)


def topology() -> dict:
    path = ROOT / "21-Network-Pivoting" / "fixtures" / "topology.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_finds_port_specific_multihop_path() -> None:
    assert analyzer.find_path(topology(), "operator", "database", 5432) == ["operator", "web", "database"]


def test_rejects_blocked_port_and_unknown_node() -> None:
    assert analyzer.find_path(topology(), "operator", "management", 3389) is None
    assert analyzer.find_path(topology(), "outside", "database", 5432) is None
