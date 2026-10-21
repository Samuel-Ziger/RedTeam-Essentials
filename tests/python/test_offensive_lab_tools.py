from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name: str):
    paths = {
        "roe_scope_guard": ROOT
        / "27-Operacoes-Seguranca-Avancadas"
        / "acervo"
        / "ferramentas"
        / "roe_scope_guard.py",
        "recon_correlator": ROOT
        / "40-Capstone-Purple-Team"
        / "acervo"
        / "tools"
        / "recon_correlator.py",
        "api_auth_matrix": ROOT
        / "40-Capstone-Purple-Team"
        / "acervo"
        / "tools"
        / "api_auth_matrix.py",
    }
    path = paths[name]
    spec = importlib.util.spec_from_file_location(f"test_{name}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope = load("roe_scope_guard")
recon = load("recon_correlator")
matrix = load("api_auth_matrix")


def test_scope_guard_supports_hosts_wildcards_and_networks() -> None:
    entries = ["localhost", "*.lab.local", "192.0.2.0/24"]
    assert scope.allowed("localhost", entries)
    assert scope.allowed("api.lab.local", entries)
    assert scope.allowed("192.0.2.10", entries)
    assert not scope.allowed("example.com", entries)
    assert not scope.allowed("198.51.100.10", entries)


def test_recon_correlates_and_prioritizes_observations() -> None:
    rows = [
        {"host": "app.lab", "ip": "192.0.2.1", "source": "dns", "technology": "nginx"},
        {"host": "APP.LAB.", "ip": "192.0.2.1", "source": "ct", "technology": "oauth"},
        {"host": "api.lab", "ip": "192.0.2.2", "source": "dns"},
    ]
    result = recon.correlate(rows)
    assert result[0]["host"] == "app.lab"
    assert result[0]["sources"] == ["ct", "dns"]
    assert result[0]["technologies"] == ["nginx", "oauth"]


def test_api_matrix_finds_bola_and_bfla_but_ignores_denied_request() -> None:
    rows = [
        {"principal": "a", "role": "user", "owner": "b", "resource": "/objects/2", "status": 200},
        {"principal": "a", "role": "user", "function": "admin", "resource": "/admin", "status": 204},
        {"principal": "a", "role": "user", "owner": "b", "resource": "/objects/3", "status": 403},
    ]
    findings = matrix.analyze(rows)
    assert [item["type"] for item in findings] == ["BOLA", "BFLA"]


def test_api_matrix_ignores_malformed_rows() -> None:
    rows = [None, {"status": "invalid"}, {"status": None}, {"status": 403}]
    assert matrix.analyze(rows) == []


def test_recon_ignores_malformed_rows() -> None:
    assert recon.correlate([None, {}, {"host": "app.lab", "source": "dns"}]) == [
        {
            "host": "app.lab",
            "ips": [],
            "asns": [],
            "sources": ["dns"],
            "technologies": [],
            "priority": 1,
        }
    ]
