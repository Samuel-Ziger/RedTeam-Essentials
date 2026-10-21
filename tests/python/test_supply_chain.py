from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"test_{name}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


secrets = load_script("scan_secrets")
sbom = load_script("generate_sbom")
links = load_script("validate_local_links")
supply_chain = load_script("validate_supply_chain")


def test_secret_scanner_finds_token_without_disclosing_value(tmp_path: Path) -> None:
    token = "ghp_" + "A" * 36
    (tmp_path / "config.py").write_text(f'TOKEN = "{token}"\n', encoding="utf-8")
    findings = secrets.scan(tmp_path)
    assert [(item.path.name, item.line, item.kind) for item in findings] == [("config.py", 1, "github-token")]
    assert token not in repr(findings)


def test_secret_scanner_allows_explicit_test_fixture(tmp_path: Path) -> None:
    token = "AKIA" + "A" * 16
    (tmp_path / "fixture.env").write_text(f"TOKEN={token} # secret-scan: allow\n", encoding="utf-8")
    assert secrets.scan(tmp_path) == []


def test_sbom_is_deterministic_and_contains_declared_dependencies() -> None:
    first = sbom.build_sbom(ROOT)
    second = sbom.build_sbom(ROOT)
    assert first == second
    purls = {item["purl"] for item in first["components"]}
    assert "pkg:pypi/ldap3@2.9.1" in purls
    assert any(item.startswith("pkg:docker/") for item in purls)
    assert any("kalilinux/kali-rolling@sha256:" in item for item in purls)
    assert any("python:3.14-slim@sha256:51dafde8" in item for item in purls)
    assert "pkg:pypi/fastapi@0.142.1" in purls
    assert any("postgres:18.6-alpine3.23@sha256:" in item for item in purls)
    assert any("mongo:8.3.11-noble@sha256:" in item for item in purls)


def test_local_link_validator_ignores_code_fences_and_reports_missing(tmp_path: Path) -> None:
    (tmp_path / "exists.md").write_text("ok\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "[ok](exists.md)\n```markdown\n[example](missing-in-example.md)\n```\n[bad](missing.md)\n",
        encoding="utf-8",
    )
    assert links.missing_links(tmp_path) == ["README.md:5: missing.md"]


def test_repository_supply_chain_references_are_immutable() -> None:
    assert supply_chain.validate(ROOT) == []
