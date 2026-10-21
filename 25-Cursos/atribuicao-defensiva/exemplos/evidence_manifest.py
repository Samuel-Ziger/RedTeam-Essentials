#!/usr/bin/env python3
"""Imprime manifesto SHA-256 de evidências locais sem modificar arquivos."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest(root: Path) -> dict[str, Any]:
    if not root.is_dir():
        raise ValueError("diretório de evidências não encontrado")
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"links simbólicos não são aceitos: {path.relative_to(root)}")
        if path.is_file():
            entries.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "size": path.stat().st_size,
                    "sha256": hash_file(path),
                }
            )
    if not entries:
        raise ValueError("nenhuma evidência regular encontrada")
    return {
        "algorithm": "sha256",
        "root_label": root.name,
        "files": entries,
        "note": "o hash prova integridade desde o cálculo, não autenticidade da origem",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_dir", type=Path)
    args = parser.parse_args()
    try:
        manifest = build_manifest(args.evidence_dir)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
