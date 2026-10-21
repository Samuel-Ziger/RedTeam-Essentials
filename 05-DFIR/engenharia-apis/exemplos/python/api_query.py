#!/usr/bin/env python3
"""Build a deterministic API collection request without network access."""

from __future__ import annotations

import argparse
import re
import sys

TOKEN = re.compile(r"[A-Za-z0-9_-]+")


def build_query(limit: int, after: str | None = None, status: str | None = None) -> str:
    if not 1 <= limit <= 100:
        raise ValueError("limit deve estar entre 1 e 100")
    if after is not None and (len(after) > 512 or not TOKEN.fullmatch(after)):
        raise ValueError("after deve ser Base64URL sem padding com até 512 caracteres")
    if status not in {None, "active", "archived"}:
        raise ValueError("status deve ser active ou archived")
    parts = [f"limit={limit}"]
    if after is not None:
        parts.append(f"after={after}")
    if status is not None:
        parts.append(f"status={status}")
    return "GET /v1/items?" + "&".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--after")
    parser.add_argument("--status")
    for option in ("--limit", "--after", "--status"):
        if sys.argv[1:].count(option) > 1:
            parser.error(f"{option} não pode ser repetido")
    args = parser.parse_args()
    try:
        print(build_query(args.limit, args.after, args.status))
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
