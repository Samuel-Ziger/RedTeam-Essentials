from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("project_metrics", ROOT / "scripts" / "project_metrics.py")
assert SPEC and SPEC.loader
metrics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(metrics)


def test_all_modules_have_contracts() -> None:
    result = metrics.collect(ROOT)
    assert result["modules"] == 26
    assert result["modules_with_contract"] == result["modules"]
    assert result["test_files"] >= 10
    assert result["fixture_files"] >= 5
