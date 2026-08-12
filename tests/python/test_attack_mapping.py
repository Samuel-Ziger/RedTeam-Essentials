from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("attack_validator", ROOT / "scripts" / "validate_attack_mapping.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def valid_layer() -> dict:
    return {
        "name": "test",
        "versions": {"attack": "14", "navigator": "4.9", "layer": "4.5"},
        "domain": "enterprise-attack",
        "techniques": [{"techniqueID": "T1590.001", "tactic": "reconnaissance", "score": 50, "enabled": True}],
    }


def test_repository_layer_is_valid() -> None:
    import json

    layer = json.loads((ROOT / "MITRE-ATTACK-MAPPING.json").read_text(encoding="utf-8"))
    assert validator.validate_layer(layer) == []


def test_validator_reports_duplicate_and_bad_score() -> None:
    layer = valid_layer()
    layer["techniques"].append(dict(layer["techniques"][0], score=101))
    errors = validator.validate_layer(layer)
    assert any("duplicada" in error for error in errors)
    assert any("score" in error for error in errors)


def test_validator_requires_expected_metadata() -> None:
    assert validator.validate_layer({})
