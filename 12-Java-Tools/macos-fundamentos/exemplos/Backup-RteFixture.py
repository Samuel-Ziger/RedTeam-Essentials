#!/usr/bin/env python3
"""Back up a synthetic directory and verify its SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

MANIFEST_NAME = "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entries(root: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if relative == MANIFEST_NAME or path.is_dir():
            continue
        if path.is_symlink():
            result.append({"path": relative, "type": "symlink", "target": str(path.readlink())})
        elif path.is_file():
            result.append(
                {"path": relative, "type": "file", "size": path.stat().st_size, "sha256": sha256(path)}
            )
    return result


def backup(source: Path, destination: Path, *, dry_run: bool = False) -> dict[str, Any]:
    source = source.resolve(strict=True)
    destination = destination.resolve(strict=False)
    if not source.is_dir():
        raise ValueError("source must be a directory")
    if destination == source or source in destination.parents:
        raise ValueError("destination cannot be the source or be inside it")
    if destination.exists():
        raise FileExistsError("destination already exists")

    plan = {
        "schema": "rte.macos.fixture-backup-plan/v1",
        "source": str(source),
        "destination": str(destination),
        "entryCount": len(entries(source)),
        "dryRun": dry_run,
    }
    if dry_run:
        return plan

    shutil.copytree(source, destination, symlinks=True, copy_function=shutil.copy2)
    manifest = {"schema": "rte.macos.fixture-manifest/v1", "entries": entries(destination)}
    (destination / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {**plan, "manifest": str(destination / MANIFEST_NAME), "dryRun": False}


def verify(destination: Path) -> dict[str, Any]:
    destination = destination.resolve(strict=True)
    manifest_path = destination / MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != "rte.macos.fixture-manifest/v1" or not isinstance(manifest.get("entries"), list):
        raise ValueError("unknown or invalid manifest")
    expected = manifest["entries"]
    actual = entries(destination)
    return {
        "schema": "rte.macos.fixture-verification/v1",
        "valid": actual == expected,
        "expectedCount": len(expected),
        "actualCount": len(actual),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path)
    parser.add_argument("destination", nargs="?", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    try:
        if args.verify:
            if args.source or args.destination or args.dry_run:
                parser.error("--verify cannot be combined with backup arguments")
            result = verify(args.verify)
            print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
            return 0 if result["valid"] else 1
        if args.source is None or args.destination is None:
            parser.error("source and destination are required for backup")
        result = backup(args.source, args.destination, dry_run=args.dry_run)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
