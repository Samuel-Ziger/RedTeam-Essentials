from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


class FileFlowError(Exception):
    """Falha esperada de entrada, planejamento ou execucao."""


@dataclass(frozen=True, slots=True)
class Operation:
    operation_id: str
    relative_path: str
    source: str
    target: str
    size: int
    sha256: str
    action: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "operationId": self.operation_id,
            "relativePath": self.relative_path,
            "size": self.size,
            "sha256": self.sha256,
            "action": self.action,
        }


@dataclass(frozen=True, slots=True)
class Plan:
    source_root: str
    target_root: str
    operations: tuple[Operation, ...]

    def canonical_dict(self) -> dict[str, Any]:
        counts = {name: 0 for name in ("copy", "skip", "conflict")}
        for operation in self.operations:
            counts[operation.action] += 1
        return {
            "schemaVersion": 1,
            "counts": counts,
            "operations": [operation.as_dict() for operation in self.operations],
        }

    @property
    def digest(self) -> str:
        encoded = json.dumps(
            self.canonical_dict(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        result = self.canonical_dict()
        result["planDigest"] = self.digest
        return result
