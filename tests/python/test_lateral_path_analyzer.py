from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "24-Lateral-Movement" / "lateral_path_analyzer.py"
SPEC = importlib.util.spec_from_file_location("lateral_path_analyzer", SCRIPT)
assert SPEC and SPEC.loader
analyzer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyzer)


def graph() -> dict:
    path = ROOT / "24-Lateral-Movement" / "fixtures" / "lateral-graph.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_finds_multihop_lateral_path_with_preconditions() -> None:
    path = analyzer.find_path(graph(), "student", "fileserver")
    assert path is not None
    assert [step["protocol"] for step in path] == ["interactive-session", "winrm", "smb"]
    assert all(step["precondition"] for step in path)


def test_finds_helpdesk_rdp_path() -> None:
    path = analyzer.find_path(graph(), "helpdesk", "workstation")
    assert path is not None
    assert path[0]["protocol"] == "rdp"


def test_rejects_disabled_out_of_scope_and_unknown_paths() -> None:
    assert analyzer.find_path(graph(), "student", "dc01") is None
    assert analyzer.find_path(graph(), "outside", "fileserver") is None


def test_finds_linux_multihop_path_without_enabling_secret_access() -> None:
    path = analyzer.find_path(graph(), "linux-operator", "backup-linux")
    assert path is not None
    assert [step["protocol"] for step in path] == ["ssh-certificate", "ssh-restricted", "nfs-readonly"]
    assert analyzer.find_path(graph(), "app-linux", "prod-secrets") is None
