"""Interface de linha de comando e composition root."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from .domain import Plan
from .errors import PlannerError
from .repository import JsonWorkItemRepository
from .service import PlanProject


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dependency-planner",
        description="Ordena tarefas, calcula lotes e caminho critico.",
    )
    parser.add_argument("project", help="caminho do documento JSON")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="formato de saida (padrao: text)",
    )
    return parser


def _format_text(plan: Plan) -> str:
    result = plan.as_dict()
    lines = [f"Ordem: {' -> '.join(result['order'])}", "Lotes paralelos:"]
    for index, batch in enumerate(result["batches"], start=1):
        lines.append(f"  {index}: {', '.join(batch)}")
    lines.extend(
        [
            f"Caminho critico: {' -> '.join(result['critical_path'])}",
            f"Duracao minima: {result['minimum_duration']}",
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        plan = PlanProject(JsonWorkItemRepository(args.project)).execute()
    except (PlannerError, OSError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(plan.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(_format_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
