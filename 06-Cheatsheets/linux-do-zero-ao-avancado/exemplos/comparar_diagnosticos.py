#!/usr/bin/env python3
"""Compara snapshots chave=valor produzidos pelo diagnóstico do curso."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


MAX_INPUT_BYTES = 1024 * 1024
KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
DEFAULT_IGNORED = frozenset({"timestamp_utc"})


class SnapshotError(ValueError):
    """Entrada não obedece ao formato didático."""


@dataclass(frozen=True)
class Difference:
    added: dict[str, str]
    removed: dict[str, str]
    changed: dict[str, tuple[str, str]]

    @property
    def count(self) -> int:
        return len(self.added) + len(self.removed) + len(self.changed)


def read_snapshot(path: Path) -> dict[str, str]:
    try:
        size = path.stat().st_size
    except OSError as error:
        raise SnapshotError(f"não foi possível acessar {path}: {error}") from error
    if size > MAX_INPUT_BYTES:
        raise SnapshotError(f"entrada excede {MAX_INPUT_BYTES} bytes: {path}")

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise SnapshotError(f"não foi possível ler {path}: {error}") from error

    values: dict[str, str] = {}
    for number, raw_line in enumerate(lines, start=1):
        if not raw_line or raw_line.startswith("#"):
            continue
        if "=" not in raw_line:
            raise SnapshotError(f"{path}:{number}: esperado chave=valor")
        key, value = raw_line.split("=", 1)
        if not KEY_PATTERN.fullmatch(key):
            raise SnapshotError(f"{path}:{number}: chave inválida: {key!r}")
        if key in values:
            raise SnapshotError(f"{path}:{number}: chave duplicada: {key}")
        values[key] = value
    if not values:
        raise SnapshotError(f"snapshot vazio: {path}")
    return values


def compare(
    before: dict[str, str],
    after: dict[str, str],
    ignored: set[str] | frozenset[str],
) -> Difference:
    before_keys = set(before) - set(ignored)
    after_keys = set(after) - set(ignored)
    return Difference(
        added={key: after[key] for key in sorted(after_keys - before_keys)},
        removed={key: before[key] for key in sorted(before_keys - after_keys)},
        changed={
            key: (before[key], after[key])
            for key in sorted(before_keys & after_keys)
            if before[key] != after[key]
        },
    )


def as_serializable(difference: Difference) -> dict[str, object]:
    return {
        "schema": "linux-course-diff/v1",
        "summary": {
            "differences": difference.count,
            "added": len(difference.added),
            "removed": len(difference.removed),
            "changed": len(difference.changed),
        },
        "added": difference.added,
        "removed": difference.removed,
        "changed": {
            key: {"before": old, "after": new}
            for key, (old, new) in difference.changed.items()
        },
    }


def render_text(difference: Difference) -> str:
    lines = [
        "schema=linux-course-diff/v1",
        f"differences={difference.count}",
        f"added={len(difference.added)}",
        f"removed={len(difference.removed)}",
        f"changed={len(difference.changed)}",
    ]
    for key, value in difference.added.items():
        lines.append(f"+ {key}={value}")
    for key, value in difference.removed.items():
        lines.append(f"- {key}={value}")
    for key, (old, new) in difference.changed.items():
        lines.append(f"~ {key}: {old} -> {new}")
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Compara dois snapshots chave=valor sem alterar o sistema."
    )
    result.add_argument("before", type=Path, help="snapshot anterior")
    result.add_argument("after", type=Path, help="snapshot posterior")
    result.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="CHAVE",
        help="ignora uma chave adicional; pode ser repetido",
    )
    result.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="formato determinístico de saída",
    )
    result.add_argument(
        "--fail-on-change",
        action="store_true",
        help="retorna status 1 quando houver diferença",
    )
    return result


def main(arguments: list[str] | None = None) -> int:
    options = parser().parse_args(arguments)
    invalid_ignored = [key for key in options.ignore if not KEY_PATTERN.fullmatch(key)]
    if invalid_ignored:
        print(f"erro: chave ignorada inválida: {invalid_ignored[0]!r}", file=sys.stderr)
        return 2

    try:
        before = read_snapshot(options.before)
        after = read_snapshot(options.after)
    except SnapshotError as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2

    ignored = set(DEFAULT_IGNORED)
    ignored.update(options.ignore)
    difference = compare(before, after, ignored)
    if options.format == "json":
        print(json.dumps(as_serializable(difference), ensure_ascii=False, sort_keys=True))
    else:
        print(render_text(difference))
    return 1 if options.fail_on_change and difference.count else 0


if __name__ == "__main__":
    raise SystemExit(main())
