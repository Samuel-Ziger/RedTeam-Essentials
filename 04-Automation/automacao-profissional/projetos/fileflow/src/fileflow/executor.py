from __future__ import annotations

import json
import os
import re
import shutil
import stat
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .domain import FileFlowError, Operation, Plan
from .planner import sha256


RUN_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def execute(plan: Plan, audit_path: Path | None = None, run_id: str | None = None) -> int:
    conflicts = [operation for operation in plan.operations if operation.action == "conflict"]
    if conflicts:
        raise FileFlowError(f"plano contem {len(conflicts)} conflito(s); nada foi copiado")

    run_id = run_id or f"run-{uuid.uuid4().hex}"
    if not RUN_ID.fullmatch(run_id):
        raise FileFlowError("run_id deve usar 1 a 64 caracteres ASCII seguros")
    for operation in plan.operations:
        _validate_source(operation)

    copied = 0
    for operation in plan.operations:
        if operation.action == "skip":
            target = Path(operation.target)
            if (
                not target.is_file()
                or target.is_symlink()
                or sha256(target) != operation.sha256
            ):
                raise FileFlowError(f"destino mudou depois do planejamento: {target}")
            _audit(audit_path, plan, operation, run_id, "skipped")
            continue
        source = Path(operation.source)
        target = Path(operation.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.is_file() and not target.is_symlink() and sha256(target) == operation.sha256:
                _audit(audit_path, str(target), "skipped", operation.sha256)
                continue
            raise FileFlowError(f"destino mudou depois do planejamento: {target}")
        temporary = target.parent / f".fileflow-{uuid.uuid4().hex}.tmp"
        try:
            shutil.copyfile(source, temporary)
            if sha256(temporary) != operation.sha256:
                raise FileFlowError(f"hash divergiu apos copia: {source}")
            try:
                os.link(temporary, target)
            except FileExistsError as error:
                raise FileFlowError(f"destino surgiu durante a execucao: {target}") from error
        finally:
            temporary.unlink(missing_ok=True)
        copied += 1
        _audit(audit_path, plan, operation, run_id, "copied")
    return copied


def _validate_source(operation: Operation) -> None:
    source = Path(operation.source)
    try:
        metadata = source.lstat()
    except OSError as error:
        raise FileFlowError(f"fonte indisponivel depois do planejamento: {source}") from error
    if source.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise FileFlowError(f"fonte deixou de ser arquivo regular: {source}")
    if metadata.st_size != operation.size or sha256(source) != operation.sha256:
        raise FileFlowError(f"fonte mudou depois do planejamento: {source}")


def _audit(
    path: Path | None,
    plan: Plan,
    operation: Operation,
    run_id: str,
    outcome: str,
) -> None:
    if path is None:
        return
    event = {
        "schemaVersion": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "file_processed",
        "runId": run_id,
        "planDigest": plan.digest,
        "operationId": operation.operation_id,
        "relativePath": operation.relative_path,
        "outcome": outcome,
        "sha256": operation.sha256,
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    except OSError as error:
        message = "auditoria falhou"
        if outcome == "copied":
            message += "; efeito confirmado, reconcilie antes de repetir"
        raise FileFlowError(message) from error
