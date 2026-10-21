#!/usr/bin/env python3
"""Gera um SBOM CycloneDX deterministico das dependencias declaradas."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def _component(name: str, version: str, component_type: str, purl: str) -> dict[str, Any]:
    return {"type": component_type, "name": name, "version": version, "purl": purl}


def collect_components(root: Path) -> list[dict[str, Any]]:
    components: dict[str, dict[str, Any]] = {}

    for requirements in sorted(root.rglob("requirements*.txt")):
        if any(part in {".git", ".venv", "venv", "node_modules"} for part in requirements.parts):
            continue
        for line in requirements.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if not value or value.startswith("#") or "==" not in value:
                continue
            name, version = value.split("==", 1)
            normalized_name = name.split("[", 1)[0]
            item = _component(normalized_name, version, "library", f"pkg:pypi/{normalized_name}@{version}")
            components[item["purl"]] = item

    compose_files = (
        set(root.rglob("compose.yaml")) | set(root.rglob("compose.yml")) | set(root.rglob("docker-compose.yml"))
    )
    for compose_path in sorted(compose_files):
        if any(part in {".git", ".venv", "venv", "node_modules"} for part in compose_path.parts):
            continue
        compose = compose_path.read_text(encoding="utf-8")
        for image in re.findall(r"^\s*image:\s*([^\s#]+)", compose, re.MULTILINE):
            if "@sha256:" in image:
                repository, digest = image.split("@", 1)
                version = digest
            else:
                repository, separator, version = image.rpartition(":")
                if not separator or "/" in version:
                    repository, version = image, "latest"
            item = _component(repository, version, "container", f"pkg:docker/{repository}@{version}")
            components[item["purl"]] = item

    for dockerfile in sorted(root.rglob("Dockerfile*")):
        if ".git" in dockerfile.parts or not dockerfile.is_file():
            continue
        content = dockerfile.read_text(encoding="utf-8")
        for image in re.findall(r"^FROM\s+([^\s]+)", content, re.MULTILINE):
            repository, separator, version = image.partition("@")
            if not separator:
                repository, separator, version = image.rpartition(":")
            if not separator:
                repository, version = image, "latest"
            item = _component(repository, version, "container", f"pkg:docker/{repository}@{version}")
            components[item["purl"]] = item

    for workflow in sorted((root / ".github/workflows").glob("*.yml")):
        content = workflow.read_text(encoding="utf-8")
        for action, version in re.findall(r"^\s*-?\s*uses:\s*([^@\s]+)@([^\s#]+)", content, re.MULTILINE):
            item = _component(action, version, "application", f"pkg:github/{action}@{version}")
            components[item["purl"]] = item
    return [components[key] for key in sorted(components)]


def build_sbom(root: Path) -> dict[str, Any]:
    components = collect_components(root)
    fingerprint = hashlib.sha256(json.dumps(components, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{fingerprint[:8]}-{fingerprint[8:12]}-{fingerprint[12:16]}-"
        f"{fingerprint[16:20]}-{fingerprint[20:32]}",
        "version": 1,
        "metadata": {"component": {"type": "application", "name": "redteam-essentials", "version": "2.1.0"}},
        "components": components,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build_sbom(args.root.resolve()), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"[OK] SBOM gerado em {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
