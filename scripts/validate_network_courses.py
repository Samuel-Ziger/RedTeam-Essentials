#!/usr/bin/env python3
"""Validate the five offline networking learning tracks (modules 14-18)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES = {
    "14": (ROOT / "14-Post-Exploitation/redes-fundamentos", 18, 5),
    "15": (ROOT / "15-Hybrid-Identity/redes-domesticas", 16, 5),
    "16": (ROOT / "16-CICD-Supply-Chain/switching-vlans", 17, 5),
    "17": (ROOT / "17-macOS-Security/roteamento-vpns", 19, 5),
    "18": (ROOT / "18-Mobile-Security/redes-empresariais-protocolos", 21, 6),
}
REQUIRED = {
    "README.md",
    "GLOSSARIO.md",
    "CHEATSHEET.md",
    "REFERENCIAS.md",
    "RESPOSTAS.md",
    "laboratorios/README.md",
    "exemplos/README.md",
    "testar-curso.sh",
}
LINK_RE = re.compile(r"\[[^]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)")
NUMBERED_RE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")
FORBIDDEN_CODE = re.compile(
    r"\b(?:nmap|masscan|zmap|ettercap|bettercap|aireplay-ng|airodump-ng|"
    r"scapy\.send|socket\.create_connection|requests\.(?:get|post)|"
    r"subprocess\.(?:run|Popen))\b",
    re.IGNORECASE,
)
GENERATED_SUFFIXES = {".pcap", ".pcapng", ".cap", ".log", ".pyc", ".bin"}


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

    present = {str(path.relative_to(course)) for path in course.rglob("*") if path.is_file()}
    for required in sorted(REQUIRED - present):
        errors.append(f"{module_id}: documento obrigatório ausente: {required}")
    if module_id == "18" and "PROTOCOLO-RNP1.md" not in present:
        errors.append("18: especificação PROTOCOLO-RNP1.md ausente")

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
        if path.suffix.lower() in GENERATED_SUFFIXES or path.name == ".DS_Store":
            errors.append(f"{module_id}: artefato gerado versionado: {path.relative_to(ROOT)}")
        if path.suffix.lower() == ".py":
            content = path.read_text(encoding="utf-8")
            if FORBIDDEN_CODE.search(content):
                errors.append(f"{module_id}: operação de rede ativa fora do escopo: {path.relative_to(ROOT)}")
            try:
                compile(content, str(path), "exec")
            except SyntaxError as exc:
                errors.append(f"{module_id}: Python inválido em {path.relative_to(ROOT)}: {exc}")
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{module_id}: JSON inválido em {path.relative_to(ROOT)}: {exc}")
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
    print(f"[PASS] network courses validated: {', '.join(selected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
