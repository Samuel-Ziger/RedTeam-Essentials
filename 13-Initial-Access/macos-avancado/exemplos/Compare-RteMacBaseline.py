#!/usr/bin/env python3
"""Compare offline desired and observed macOS settings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def compare(desired: object, observed: object) -> list[dict[str, Any]]:
    if not isinstance(desired, dict) or desired.get("schema") != "rte.macos.desired-baseline/v1":
        raise ValueError("unknown desired baseline schema")
    if not isinstance(observed, dict) or observed.get("schema") != "rte.macos.observed-baseline/v1":
        raise ValueError("unknown observed baseline schema")
    settings = desired.get("settings")
    values = observed.get("settings")
    facts = observed.get("facts", {})
    if not isinstance(settings, list) or not isinstance(values, dict) or not isinstance(facts, dict):
        raise ValueError("invalid baseline structure")

    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for setting in settings:
        if not isinstance(setting, dict) or not isinstance(setting.get("id"), str):
            raise ValueError("each desired setting needs an id")
        setting_id = setting["id"]
        if setting_id in seen:
            raise ValueError(f"duplicate desired setting: {setting_id}")
        seen.add(setting_id)
        requires_arch = setting.get("requiresArchitecture")
        if requires_arch is not None and facts.get("architecture") != requires_arch:
            status, actual = "not-applicable", None
        elif setting_id not in values:
            status, actual = "missing", None
        else:
            actual = values[setting_id]
            status = "compliant" if actual == setting.get("value") else "drift"
        result.append(
            {
                "id": setting_id,
                "status": status,
                "desired": setting.get("value"),
                "actual": actual,
                "severity": setting.get("severity", "unspecified"),
            }
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("desired", type=Path)
    parser.add_argument("observed", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        desired = json.loads(args.desired.read_text(encoding="utf-8"))
        observed = json.loads(args.observed.read_text(encoding="utf-8"))
        result = compare(desired, observed)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
