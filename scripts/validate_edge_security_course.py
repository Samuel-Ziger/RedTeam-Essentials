#!/usr/bin/env python3
"""Valida a especialização Purple Team do módulo 26."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes"
EXPECTED_CHAPTERS = 22
EXPECTED_LABS = 7
REQUIRED = {
    "README.md",
    "GLOSSARIO.md",
    "CHEATSHEET.md",
    "REFERENCIAS.md",
    "RESPOSTAS.md",
    "laboratorios/README.md",
    "exemplos/README.md",
    "exemplos/edge_risk_engine.py",
    "exemplos/control_plane_audit.py",
    "exemplos/token_bucket.py",
    "exemplos/tests/test_edge_tools.py",
    "fixtures/requests-sinteticas.json",
    "fixtures/politica-edge.json",
    "fixtures/eventos-rate-limit.json",
    "testar-curso.sh",
}
LINK_RE = re.compile(r"\[[^]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)")
NUMBERED_RE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")
ACTIVE_NETWORK = re.compile(
    r"\b(?:requests\.(?:get|post|put|delete)|httpx\.|urllib\.request|"
    r"socket\.(?:socket|create_connection)|subprocess\.(?:run|Popen))\b",
    re.IGNORECASE,
)
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
DANGEROUS_AUTOMATION = re.compile(
    r"\b(?:captcha\s+bypass|cloudflare\s+bypass|waf\s+bypass|rotate\s+proxies|"
    r"evade\s+rate\s+limit|disable\s+(?:firewall|waf))\b",
    re.IGNORECASE,
)
GENERATED_SUFFIXES = {".pyc", ".key", ".p12", ".pfx", ".pcap", ".pcapng", ".log"}


def local_link_errors() -> list[str]:
    errors: list[str] = []
    for document in sorted(COURSE.rglob("*.md")):
        content = document.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(content):
            target = (document.parent / raw).resolve()
            if not target.exists():
                errors.append(f"{document.relative_to(ROOT)} -> {raw}")
    return errors


def validate() -> list[str]:
    """Return every structural or safe-scope violation."""
    errors: list[str] = []
    if not COURSE.is_dir():
        return [f"curso ausente: {COURSE.relative_to(ROOT)}"]
    present = {str(path.relative_to(COURSE)) for path in COURSE.rglob("*") if path.is_file()}
    for required in sorted(REQUIRED - present):
        errors.append(f"documento obrigatório ausente: {required}")

    chapters = sorted(path for path in COURSE.glob("*.md") if NUMBERED_RE.match(path.name))
    expected_names = [f"{number:02d}" for number in range(EXPECTED_CHAPTERS)]
    found_names = [path.name[:2] for path in chapters]
    if found_names != expected_names:
        errors.append(f"capítulos esperados={expected_names}; encontrados={found_names}")

    labs = sorted(path for path in (COURSE / "laboratorios").glob("*.md") if NUMBERED_RE.match(path.name))
    if len(labs) != EXPECTED_LABS:
        errors.append(f"esperados {EXPECTED_LABS} labs; encontrados {len(labs)}")
    errors.extend(local_link_errors())

    for path in COURSE.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in GENERATED_SUFFIXES or path.name == ".DS_Store":
            errors.append(f"artefato sensível/gerado versionado: {relative}")
        content = path.read_text(encoding="utf-8", errors="replace")
        if PRIVATE_KEY.search(content):
            errors.append(f"chave privada versionada: {relative}")
        if DANGEROUS_AUTOMATION.search(content):
            errors.append(f"instrução de evasão fora do escopo: {relative}")
        if path.suffix == ".py":
            if ACTIVE_NETWORK.search(content):
                errors.append(f"operação de rede ativa fora do escopo: {relative}")
            try:
                compile(content, str(path), "exec")
            except SyntaxError as exc:
                errors.append(f"Python inválido em {relative}: {exc}")
        if path.suffix == ".json":
            try:
                json.loads(content)
            except json.JSONDecodeError as exc:
                errors.append(f"JSON inválido em {relative}: {exc}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print("[PASS] curso Purple Team do módulo 26 validado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
