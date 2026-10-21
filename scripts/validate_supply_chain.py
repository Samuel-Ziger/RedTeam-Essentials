#!/usr/bin/env python3
"""Valida pinning local de Actions, imagens e dependencias Python."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ACTION = re.compile(r"^\s*-?\s*uses:\s*([^@\s]+)@([^\s#]+)", re.MULTILINE)
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PYTHON_PIN = re.compile(r"^[A-Za-z0-9_.-]+(?:\[[A-Za-z0-9_,.-]+\])?==[^=\s]+$")


def _ignored(path: Path) -> bool:
    return any(part in {".git", ".venv", "venv", "node_modules"} for part in path.parts)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for workflow in sorted((root / ".github/workflows").glob("*.yml")):
        content = workflow.read_text(encoding="utf-8")
        for action, revision in ACTION.findall(content):
            if action.startswith("./"):
                continue
            if not FULL_SHA.fullmatch(revision):
                errors.append(f"{workflow.relative_to(root)}: Action nao fixada por SHA: {action}@{revision}")

    for requirements in sorted(root.rglob("requirements*.txt")):
        if _ignored(requirements):
            continue
        for number, line in enumerate(requirements.read_text(encoding="utf-8").splitlines(), 1):
            value = line.strip()
            if not value or value.startswith("#"):
                continue
            if value.startswith("-r "):
                included = requirements.parent / value.removeprefix("-r ").strip()
                if not included.is_file():
                    errors.append(f"{requirements.relative_to(root)}:{number}: include ausente: {value}")
            elif not PYTHON_PIN.fullmatch(value):
                errors.append(f"{requirements.relative_to(root)}:{number}: dependencia nao fixada: {value}")

    compose_files = (
        set(root.rglob("compose.yaml")) | set(root.rglob("compose.yml")) | set(root.rglob("docker-compose.yml"))
    )
    for compose_path in sorted(compose_files):
        if _ignored(compose_path):
            continue
        for number, line in enumerate(compose_path.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip().startswith("image:") and "@sha256:" not in line:
                errors.append(f"{compose_path.relative_to(root)}:{number}: imagem sem digest")
    for dockerfile in sorted(root.rglob("Dockerfile*")):
        if _ignored(dockerfile) or not dockerfile.is_file():
            continue
        for number, line in enumerate(dockerfile.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip().startswith("FROM ") and "@sha256:" not in line:
                errors.append(f"{dockerfile.relative_to(root)}:{number}: imagem-base sem digest")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    for error in errors:
        print(f"[ERRO] {error}")
    if errors:
        return 1
    print("[OK] cadeia de fornecimento usa referencias imutaveis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
