from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("module_catalog", ROOT / "scripts" / "validate_module_catalog.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def test_repository_module_catalog_is_complete() -> None:
    catalog = json.loads((ROOT / "MODULE-CATALOG.json").read_text(encoding="utf-8"))
    assert validator.validate(ROOT, catalog) == []
    assert len(catalog["modules"]) == 41


def test_catalog_rejects_unknown_prerequisite(tmp_path) -> None:
    module = tmp_path / "00-Test"
    module.mkdir()
    fields = "\n".join(f"| {field} | value |" for field in validator.CONTRACT_FIELDS)
    (module / "README.md").write_text(f"## Contrato do módulo\n{fields}\n", encoding="utf-8")
    catalog = {
        "schemaVersion": 1,
        "modules": [
            {
                "id": "00",
                "path": "00-Test",
                "title": "Test",
                "maturity": "introductory",
                "status": "active",
                "prerequisites": ["99"],
                "estimatedHours": {"min": 1, "max": 1},
            }
        ],
    }
    assert any("desconhecido" in error for error in validator.validate(tmp_path, catalog))


def test_catalog_rejects_prerequisite_cycle() -> None:
    data = json.loads((ROOT / "MODULE-CATALOG.json").read_text(encoding="utf-8"))
    data["modules"][0]["prerequisites"] = ["01"]
    errors = validator.validate(ROOT, data)
    assert any("ciclo de pre-requisitos" in error for error in errors)
