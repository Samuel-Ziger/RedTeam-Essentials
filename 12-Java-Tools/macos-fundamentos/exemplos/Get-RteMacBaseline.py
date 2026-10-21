#!/usr/bin/env python3
"""Collect a small, privacy-preserving local macOS baseline."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
from pathlib import Path
from typing import Any

COMMANDS: dict[str, tuple[str, ...]] = {
    "productVersion": ("/usr/bin/sw_vers", "-productVersion"),
    "buildVersion": ("/usr/bin/sw_vers", "-buildVersion"),
    "architecture": ("/usr/bin/uname", "-m"),
    "hardwareModel": ("/usr/sbin/sysctl", "-n", "hw.model"),
    "fileVault": ("/usr/bin/fdesetup", "status"),
    "sip": ("/usr/bin/csrutil", "status"),
    "gatekeeper": ("/usr/sbin/spctl", "--status"),
}


def command_key(command: tuple[str, ...]) -> str:
    """Return the stable fixture key for a command."""
    return " ".join(Path(command[0]).name if index == 0 else value for index, value in enumerate(command))


def read_fixture(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or any(not isinstance(key, str) or not isinstance(value, str) for key, value in data.items()):
        raise ValueError("fixture must be an object of string command outputs")
    return data


def collect(fixture: dict[str, str] | None = None) -> dict[str, Any]:
    if fixture is None and platform.system() != "Darwin":
        raise RuntimeError("real collection requires macOS; use --fixture elsewhere")

    values: dict[str, str | None] = {}
    errors: list[str] = []
    for field, command in COMMANDS.items():
        if fixture is not None:
            key = command_key(command)
            if key not in fixture:
                values[field] = None
                errors.append(f"missing fixture command: {key}")
                continue
            values[field] = fixture[key].strip()
            continue

        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = (completed.stdout or completed.stderr).strip()
        if completed.returncode != 0:
            values[field] = None
            errors.append(f"{command_key(command)} exited {completed.returncode}")
        else:
            values[field] = output

    return {
        "schema": "rte.macos.local-baseline/v1",
        "operatingSystem": {
            "productVersion": values["productVersion"],
            "buildVersion": values["buildVersion"],
        },
        "hardware": {
            "architecture": values["architecture"],
            "model": values["hardwareModel"],
        },
        "protections": {
            "fileVault": values["fileVault"],
            "sip": values["sip"],
            "gatekeeper": values["gatekeeper"],
        },
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    fixture = read_fixture(args.fixture) if args.fixture else None
    try:
        result = collect(fixture)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
