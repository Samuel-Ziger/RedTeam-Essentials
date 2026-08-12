#!/usr/bin/env python3
"""Valida políticas de segurança/reprodutibilidade do Compose sem PyYAML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SERVICE_RE = re.compile(r"^  ([a-z][a-z0-9-]*):$")
PORT_RE = re.compile(r'^\s+- ["\']([^"\']+)["\']$')


def service_blocks(text: str) -> dict[str, list[str]]:
    """Extrai blocos diretamente abaixo de ``services`` pela indentação."""
    blocks: dict[str, list[str]] = {}
    in_services = False
    current: str | None = None
    for line in text.splitlines():
        if line == "services:":
            in_services = True
            continue
        if in_services and line and not line.startswith(" "):
            break
        match = SERVICE_RE.match(line) if in_services else None
        if match:
            current = match.group(1)
            blocks[current] = []
        elif current:
            blocks[current].append(line)
    return blocks


def validate(text: str) -> list[str]:
    errors: list[str] = []
    blocks = service_blocks(text)
    if not blocks:
        return ["nenhum serviço encontrado"]
    for name, lines in blocks.items():
        body = "\n".join(lines)
        for field in ("healthcheck:", "mem_limit:", "cpus:"):
            if field not in body:
                errors.append(f"{name}: campo ausente: {field[:-1]}")
        in_ports = False
        for line in lines:
            stripped = line.strip()
            if stripped == "ports:":
                in_ports = True
                continue
            if in_ports and stripped and not stripped.startswith("-"):
                in_ports = False
            if in_ports:
                match = PORT_RE.match(line)
                if match and not match.group(1).startswith("127.0.0.1:"):
                    errors.append(f"{name}: porta não limitada a localhost: {match.group(1)}")
    expected_profiles = {
        "bwapp": {"extended", "full"},
        "webgoat": {"extended", "full"},
        "vulnerable-wordpress": {"extended", "full"},
        "nodegoat": {"api", "full"},
        "vampi": {"api", "full"},
    }
    for name, profiles in expected_profiles.items():
        body = "\n".join(blocks.get(name, []))
        for profile in profiles:
            if f'"{profile}"' not in body:
                errors.append(f"{name}: profile ausente: {profile}")
    return errors


def mutable_images(text: str) -> list[str]:
    """Lista imagens ainda não fixadas por digest para relatório de dívida."""
    return [line.strip() for line in text.splitlines() if line.strip().startswith("image:") and "@sha256:" not in line]


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "docker-lab/docker-compose.yml")
    text = path.read_text(encoding="utf-8")
    errors = validate(text)
    if errors:
        for error in errors:
            print(f"[ERRO] {error}", file=sys.stderr)
        return 1
    print(f"[OK] política Compose válida para {len(service_blocks(text))} serviços")
    mutable = mutable_images(text)
    if mutable:
        print(f"[AVISO] {len(mutable)} imagens aguardam digest verificado pelo registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
