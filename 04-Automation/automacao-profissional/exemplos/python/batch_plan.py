from __future__ import annotations

import argparse
import json
import re
from collections.abc import Sequence

ID = re.compile(r"^[A-Za-z0-9_-]+$")
MAX_ITEMS = 64
MAX_INPUT_BYTES = 1023


def plan(raw: str) -> list[str]:
    if len(raw.encode("utf-8")) > MAX_INPUT_BYTES:
        raise ValueError("items excede 1023 bytes")
    values = raw.split(",")
    if len(values) > MAX_ITEMS:
        raise ValueError("items excede 64 IDs")
    if not values or any(not ID.fullmatch(value) for value in values):
        raise ValueError("items deve conter IDs separados por virgula")
    return sorted(set(values))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        items = plan(args.items)
    except ValueError as error:
        parser.error(str(error))
    if args.format == "json":
        print(json.dumps({"count": len(items), "items": items}, separators=(",", ":")))
    else:
        print(f"count={len(items)} items={','.join(items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
