from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

from .domain import FileFlowError
from .executor import execute
from .planner import build_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Planeja e copia arquivos de forma idempotente.")
    parser.add_argument("--version", action="version", version="fileflow 1.1.0")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--extensions", default=".txt,.log")
    parser.add_argument("--max-files", type=int, default=10_000)
    parser.add_argument("--max-total-bytes", type=int, default=1_000_000_000)
    parser.add_argument("--run-id")
    parser.add_argument("--apply", action="store_true", help="aplica o plano; padrao e dry-run")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args(argv)
    try:
        plan = build_plan(
            args.source,
            args.target,
            args.extensions.split(","),
            max_files=args.max_files,
            max_total_bytes=args.max_total_bytes,
        )
        manifest = json.dumps(plan.as_dict(), ensure_ascii=False, indent=2)
        if args.manifest:
            _write_atomic(args.manifest, manifest + "\n")
        print(manifest)
        if args.apply:
            copied = execute(plan, args.audit, args.run_id)
            print(f"aplicado: {copied} arquivo(s)", file=sys.stderr)
        else:
            print("dry-run: nenhum arquivo foi alterado", file=sys.stderr)
        return 0
    except (FileFlowError, OSError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.{uuid.uuid4().hex}.tmp"
    try:
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
