#!/usr/bin/env python3
"""Valida links locais Markdown sem rede ou dependencias externas."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote

INLINE_LINK = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^]]+\]:\s*(\S+)")
RUNTIME_PREFIXES = (
    ("study-app", "dist"),
    ("study-app", "public", "generated"),
)


def is_runtime_document(document: Path, root: Path) -> bool:
    relative = document.relative_to(root)
    if ".git" in relative.parts or "node_modules" in relative.parts:
        return True
    return any(relative.parts[: len(prefix)] == prefix for prefix in RUNTIME_PREFIXES)


def missing_links(root: Path) -> list[str]:
    missing: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if is_runtime_document(document, root):
            continue
        fenced = False
        for line_number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            targets = INLINE_LINK.findall(line)
            reference = REFERENCE_LINK.match(line)
            if reference:
                targets.append(reference.group(1))
            for raw_target in targets:
                target = raw_target.strip().split()[0].strip("<>")
                if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                relative = unquote(target.split("#", 1)[0])
                if relative and not (document.parent / relative).resolve().exists():
                    missing.append(f"{document.relative_to(root)}:{line_number}: {relative}")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    missing = missing_links(args.root.resolve())
    for error in missing:
        print(f"[ERRO] link local inexistente: {error}")
    if missing:
        return 1
    print("[OK] links locais Markdown validos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
