#!/usr/bin/env python3
"""Gate offline: aceita um alvo somente quando ele pertence à allowlist RoE."""

from __future__ import annotations

import argparse
import fnmatch
import ipaddress
from pathlib import Path


def load_scope(path: Path) -> list[str]:
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            entries.append(value.lower().rstrip("."))
    if not entries:
        raise ValueError("allowlist vazia")
    return entries


def allowed(target: str, entries: list[str]) -> bool:
    candidate = target.lower().rstrip(".")
    try:
        address = ipaddress.ip_address(candidate)
    except ValueError:
        address = None
    for entry in entries:
        try:
            network = ipaddress.ip_network(entry, strict=False)
        except ValueError:
            network = None
        if address is not None and network is not None and address in network:
            return True
        if network is None and fnmatch.fnmatchcase(candidate, entry):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", required=True, type=Path)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()
    try:
        entries = load_scope(args.scope)
    except (OSError, ValueError) as exc:
        print(f"DENY: {exc}")
        return 2
    if allowed(args.target, entries):
        print(f"ALLOW: {args.target}")
        return 0
    print(f"DENY: {args.target} está fora do escopo")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
