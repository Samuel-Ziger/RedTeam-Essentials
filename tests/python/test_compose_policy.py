from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("compose_policy", ROOT / "scripts" / "validate_compose_policy.py")
assert SPEC and SPEC.loader
policy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy)


def test_repository_compose_meets_local_security_policy() -> None:
    text = (ROOT / "docker-lab" / "docker-compose.yml").read_text(encoding="utf-8")
    assert policy.validate(text) == []
    assert len(policy.service_blocks(text)) == 8


def test_validator_rejects_public_port_and_missing_limits() -> None:
    text = """services:
  unsafe:
    image: example:latest
    ports:
      - "8080:80"
"""
    errors = policy.validate(text)
    assert any("localhost" in error for error in errors)
    assert any("healthcheck" in error for error in errors)
    assert any("mem_limit" in error for error in errors)


def test_mutable_image_inventory_distinguishes_digest() -> None:
    text = """services:
  pinned:
    image: example/app:1@sha256:abc
  moving:
    image: example/app:latest
"""
    assert policy.mutable_images(text) == ["image: example/app:latest"]
