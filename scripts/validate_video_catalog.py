#!/usr/bin/env python3
"""Validate the Portuguese video sections distributed across modules 00-24."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

MODULE_RE = re.compile(r"^(\d{2})-")
SECTION_RE = re.compile(
    r"^## Vídeos em português\s*$\n(?P<body>.*?)(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)
VIDEO_RE = re.compile(
    r"^\d+\. \[.+?\]\(https://www\.youtube\.com/watch\?v=([\w-]{11})\)"
    r" — \*\*[^*]+\*\*\.$",
    re.MULTILINE,
)


def validate_catalog(root: Path, minimum: int = 5) -> list[str]:
    """Return validation errors for video sections under *root*."""
    if not root.is_dir():
        return [f"diretório do projeto não encontrado: {root}"]

    modules = sorted(
        path
        for path in root.iterdir()
        if path.is_dir()
        and (match := MODULE_RE.match(path.name))
        and 0 <= int(match.group(1)) <= 24
    )
    expected = [f"{number:02d}" for number in range(25)]
    found = [MODULE_RE.match(module.name).group(1) for module in modules]
    errors: list[str] = []

    if found != expected:
        errors.append(f"seções esperadas {expected}; encontradas {found}")

    courses_readme = root / "25-Cursos" / "README.md"
    if not courses_readme.is_file():
        errors.append("25-Cursos: README.md não encontrado")
    elif "youtube.com/watch?v=" in courses_readme.read_text(encoding="utf-8"):
        errors.append("25-Cursos: vídeos avulsos devem ficar nos módulos temáticos")

    for module in modules:
        readme = module / "README.md"
        if not readme.is_file():
            errors.append(f"{module.name}: README.md não encontrado")
            continue
        content = readme.read_text(encoding="utf-8")
        sections = list(SECTION_RE.finditer(content))
        if len(sections) != 1:
            errors.append(
                f"{module.name}: esperada 1 seção de vídeos; encontradas {len(sections)}"
            )
            continue
        video_ids = VIDEO_RE.findall(sections[0].group("body"))
        if len(video_ids) < minimum:
            errors.append(
                f"{module.name}: {len(video_ids)} vídeo(s), mínimo {minimum}"
            )
        if len(video_ids) != len(set(video_ids)):
            errors.append(f"{module.name}: há vídeos duplicados")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path("."),
        help="raiz do repositório (padrão: diretório atual)",
    )
    parser.add_argument("--minimum", type=int, default=5)
    args = parser.parse_args()

    errors = validate_catalog(args.root, args.minimum)
    if errors:
        for error in errors:
            print(f"ERRO: {error}")
        return 1

    print("OK: módulos 00-24 possuem pelo menos 5 vídeos válidos em cada um")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
