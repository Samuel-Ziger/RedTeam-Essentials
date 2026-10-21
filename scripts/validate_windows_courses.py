#!/usr/bin/env python3
"""Validate the four offline Windows learning tracks."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES = {
    "08": (ROOT / "08-Cloud-RedTeam/windows-domestico-fundamentos", 18, 6),
    "09": (ROOT / "09-C2-Evasion/windows-domestico-avancado", 20, 6),
    "10": (ROOT / "10-Container-Sec/windows-empresarial-fundamentos", 19, 6),
    "11": (ROOT / "11-Python-Tools/windows-empresarial-avancado", 22, 7),
}
REQUIRED = {
    "README.md",
    "GLOSSARIO.md",
    "CHEATSHEET.md",
    "REFERENCIAS.md",
    "RESPOSTAS.md",
    "laboratorios/README.md",
    "exemplos/README.md",
}
LINK_RE = re.compile(r"\[[^]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)")
NUMBERED_RE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")
FORBIDDEN_ACTIVE = re.compile(
    r"\b(?:New-NetIPAddress|Set-DnsClientServerAddress|New-NetFirewallRule|"
    r"Enable-PSRemoting|New-SmbShare|Install-ADDSForest|Invoke-Expression|IEX|"
    r"DownloadString|DisableRealtimeMonitoring)\b",
    re.IGNORECASE,
)
FORBIDDEN_NATIVE = re.compile(
    r"\b(?:OpenProcess|WriteProcessMemory|CreateRemoteThread|VirtualAllocEx)\b"
)
GENERATED_SUFFIXES = {".dll", ".exe", ".obj", ".pdb", ".lib", ".exp", ".etl", ".dmp"}
BOURNE_CONTINUATION = re.compile(r"\\\s*$", re.MULTILINE)


def local_link_errors(course: Path) -> list[str]:
    errors: list[str] = []
    for document in sorted(course.rglob("*.md")):
        content = document.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(content):
            target = (document.parent / raw).resolve()
            if not target.exists():
                errors.append(f"{document.relative_to(ROOT)} -> {raw}")
    return errors


def validate_course(module_id: str) -> list[str]:
    course, expected_chapters, expected_labs = COURSES[module_id]
    errors: list[str] = []
    if not course.is_dir():
        return [f"{module_id}: curso ausente: {course.relative_to(ROOT)}"]

    present = {str(path.relative_to(course)) for path in course.rglob("*.md")}
    for required in sorted(REQUIRED - present):
        errors.append(f"{module_id}: documento obrigatório ausente: {required}")

    chapters = sorted(path for path in course.glob("*.md") if NUMBERED_RE.match(path.name))
    expected_names = [f"{number:02d}" for number in range(expected_chapters)]
    found_names = [path.name[:2] for path in chapters]
    if found_names != expected_names:
        errors.append(f"{module_id}: capítulos esperados={expected_names}; encontrados={found_names}")

    labs = sorted(path for path in (course / "laboratorios").glob("*.md") if NUMBERED_RE.match(path.name))
    if len(labs) != expected_labs:
        errors.append(f"{module_id}: esperados {expected_labs} labs; encontrados {len(labs)}")

    errors.extend(local_link_errors(course))

    for path in course.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in GENERATED_SUFFIXES:
            errors.append(f"{module_id}: artefato gerado versionado: {path.relative_to(ROOT)}")
        if path.suffix.lower() in {".ps1", ".psm1", ".c", ".h"}:
            text = path.read_text(encoding="utf-8")
            if FORBIDDEN_ACTIVE.search(text):
                errors.append(f"{module_id}: operação fora do escopo: {path.relative_to(ROOT)}")
            if path.suffix.lower() in {".c", ".h"} and FORBIDDEN_NATIVE.search(text):
                errors.append(f"{module_id}: API nativa ofensiva fora do escopo: {path.relative_to(ROOT)}")
            if path.suffix.lower() == ".ps1" and "tests" not in path.parts:
                if "Set-StrictMode" not in text or "$ErrorActionPreference" not in text:
                    errors.append(f"{module_id}: PowerShell sem modo estrito: {path.relative_to(ROOT)}")
            if path.suffix.lower() == ".ps1" and BOURNE_CONTINUATION.search(text):
                errors.append(
                    f"{module_id}: continuacao de linha Bash em PowerShell: {path.relative_to(ROOT)}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", choices=sorted(COURSES))
    args = parser.parse_args()
    selected = [args.module] if args.module else sorted(COURSES)
    errors: list[str] = []
    for module_id in selected:
        errors.extend(validate_course(module_id))
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print(f"[PASS] Windows courses validated: {', '.join(selected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
