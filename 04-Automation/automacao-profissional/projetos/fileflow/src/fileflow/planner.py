from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from pathlib import Path

from .domain import FileFlowError, Operation, Plan


EXTENSION = re.compile(r"^\.[A-Za-z0-9][A-Za-z0-9_-]{0,15}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_extensions(values: Iterable[str]) -> frozenset[str]:
    result = frozenset(value.lower() for value in values)
    if not result or any(not EXTENSION.fullmatch(value) for value in result):
        raise FileFlowError("extensoes devem usar . + 1 a 16 caracteres seguros")
    return result


def build_plan(
    source: Path,
    target: Path,
    extensions: Iterable[str],
    *,
    max_files: int = 10_000,
    max_total_bytes: int = 1_000_000_000,
) -> Plan:
    if not 1 <= max_files <= 1_000_000:
        raise FileFlowError("max_files deve estar entre 1 e 1000000")
    if not 1 <= max_total_bytes <= 1_000_000_000_000:
        raise FileFlowError("max_total_bytes deve estar entre 1 e 1000000000000")
    source = source.resolve()
    target = target.resolve()
    allowed = normalize_extensions(extensions)
    if not source.is_dir():
        raise FileFlowError(f"origem nao e diretorio: {source}")
    if source == target or source in target.parents or target in source.parents:
        raise FileFlowError("origem e destino nao podem ser iguais ou aninhados")

    operations: list[Operation] = []
    total_bytes = 0
    for candidate in sorted(source.rglob("*")):
        if candidate.is_symlink():
            raise FileFlowError(f"link simbolico nao permitido: {candidate}")
        if not candidate.is_file() or candidate.suffix.lower() not in allowed:
            continue
        relative = candidate.relative_to(source)
        destination = target / relative
        digest = sha256(candidate)
        size = candidate.stat().st_size
        total_bytes += size
        if len(operations) + 1 > max_files:
            raise FileFlowError(f"origem excede limite de {max_files} arquivos")
        if total_bytes > max_total_bytes:
            raise FileFlowError(f"origem excede limite de {max_total_bytes} bytes")
        if not destination.exists():
            action = "copy"
        elif not destination.is_file() or destination.is_symlink():
            action = "conflict"
        else:
            action = "skip" if sha256(destination) == digest else "conflict"
        relative_path = relative.as_posix()
        operation_id = hashlib.sha256(f"{relative_path}\0{digest}".encode()).hexdigest()[:24]
        operations.append(
            Operation(
                operation_id,
                relative_path,
                str(candidate),
                str(destination),
                size,
                digest,
                action,
            )
        )
    return Plan(str(source), str(target), tuple(operations))
