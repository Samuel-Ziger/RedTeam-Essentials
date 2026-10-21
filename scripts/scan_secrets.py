#!/usr/bin/env python3
"""Scanner offline de credenciais de alta confianca para o repositorio."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

TEXT_SUFFIXES = {
    ".env",
    ".java",
    ".json",
    ".md",
    ".ps1",
    ".psm1",
    ".py",
    ".sh",
    ".toml",
    ".yaml",
    ".yml",
}
IGNORED_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".venv", "__pycache__", "build"}
ALLOW_MARKER = "secret-scan: allow"
PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "aws-access-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b"),
    "gitlab-token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "slack-token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
}


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    kind: str


def scan(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name != ".env":
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for line_number, line in enumerate(lines, 1):
            if ALLOW_MARKER in line.lower():
                continue
            for kind, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(path.relative_to(root), line_number, kind))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    for finding in findings:
        print(f"[SEGREDO] {finding.path}:{finding.line}: {finding.kind}")
    if findings:
        print(f"[FALHA] {len(findings)} possivel(is) segredo(s).", file=sys.stderr)
        return 1
    print("[OK] nenhum segredo de alta confianca encontrado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
