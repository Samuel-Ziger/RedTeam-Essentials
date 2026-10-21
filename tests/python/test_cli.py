from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("rte_cli", ROOT / "rte.py")
assert SPEC and SPEC.loader
rte = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rte)


def test_catalog_is_available_to_cli() -> None:
    modules = rte.load_catalog()["modules"]
    assert len(modules) == 41
    assert modules[0]["id"] == "00"
    assert modules[-1]["id"] == "40"


def test_compose_command_scopes_profiles_and_destructive_flags() -> None:
    basic = rte.compose_command("up", "basic", build=True)
    assert "--profile" not in basic
    assert basic[-3:] == ["up", "-d", "--build"]

    api = rte.compose_command("up", "api")
    assert api[api.index("--profile") + 1] == "api"

    safe_down = rte.compose_command("down", "full")
    destructive_down = rte.compose_command("down", "full", volumes=True)
    assert "--volumes" not in safe_down
    assert destructive_down[-1] == "--volumes"


def test_cli_modules_json(capsys) -> None:
    assert rte.main(["modules", "--status", "active", "--json"]) == 0
    output = capsys.readouterr().out
    assert '"id": "09"' in output
    assert '"id": "25"' in output
    assert '"id": "26"' in output
    assert '"id": "40"' in output
