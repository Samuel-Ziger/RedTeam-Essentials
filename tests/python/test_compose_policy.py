from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("compose_policy", ROOT / "scripts" / "validate_compose_policy.py")
assert SPEC and SPEC.loader
policy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy)


def test_repository_compose_meets_local_security_policy() -> None:
    text = (ROOT / "30-Web-API-AppSec" / "docker-lab" / "docker-compose.yml").read_text(encoding="utf-8")
    assert policy.validate(text) == []
    assert len(policy.service_blocks(text)) == 7
    assert policy.mutable_images(text) == []


def test_validator_rejects_public_port_and_missing_limits() -> None:
    text = """services:
  unsafe:
    image: example:latest
    ports:
      - "8080:80"
"""
    errors = policy.validate(text)
    assert any("localhost" in error for error in errors)
    assert any("somente o gateway" in error for error in errors)
    assert any("healthcheck" in error for error in errors)
    assert any("mem_limit" in error for error in errors)
    assert any("restart" in error for error in errors)
    assert any("internal" in error for error in errors)


def test_validator_rejects_unquoted_or_long_port_syntax() -> None:
    text = """networks:
  rte-lab:
    internal: true
services:
  unsafe:
    image: example:latest
    ports:
      - 127.0.0.1:8080:80
    healthcheck: {test: [\"CMD\", \"true\"]}
    mem_limit: 128m
    cpus: 0.25
    restart: \"no\"
"""
    assert any("nao validavel" in error for error in policy.validate(text))


def test_validator_requires_exact_network_topology() -> None:
    text = (ROOT / "30-Web-API-AppSec" / "docker-lab" / "docker-compose.yml").read_text(encoding="utf-8")
    unsafe = text.replace("      rte-lab:\n        ipv4_address: 172.28.0.10", "      rte-access: {}", 1)
    errors = policy.validate(unsafe)
    assert any(error.startswith("dvwa: redes devem ser rte-lab") for error in errors)


def test_validator_binds_internal_flag_to_correct_network() -> None:
    text = (ROOT / "30-Web-API-AppSec" / "docker-lab" / "docker-compose.yml").read_text(encoding="utf-8")
    unsafe = text.replace(
        "  rte-lab:\n    driver: bridge\n    internal: true", "  rte-lab:\n    driver: bridge\n    internal: false"
    )
    assert "rte-lab: rede deve declarar internal: true" in policy.validate(unsafe)


def test_mutable_image_inventory_distinguishes_digest() -> None:
    text = """services:
  pinned:
    image: example/app:1@sha256:abc
  moving:
    image: example/app:latest
"""
    assert policy.mutable_images(text) == ["image: example/app:latest"]
    assert policy.mutable_base_images("FROM python:3.12\nFROM alpine@sha256:abc\n") == ["FROM python:3.12"]
