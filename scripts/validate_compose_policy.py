#!/usr/bin/env python3
"""Valida políticas de segurança/reprodutibilidade do Compose sem PyYAML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SERVICE_RE = re.compile(r"^  ([a-z][a-z0-9-]*):$")
NESTED_KEY_RE = re.compile(r"^      ([a-z][a-z0-9-]*):")
PORT_RE = re.compile(r'^\s+- ["\']([^"\']+)["\']$')


def section_blocks(text: str, section: str) -> dict[str, list[str]]:
    """Extrai blocos diretamente abaixo de uma seção Compose pela indentação."""
    blocks: dict[str, list[str]] = {}
    in_section = False
    current: str | None = None
    for line in text.splitlines():
        if line == f"{section}:":
            in_section = True
            continue
        if in_section and line and not line.startswith(" "):
            break
        match = SERVICE_RE.match(line) if in_section else None
        if match:
            current = match.group(1)
            blocks[current] = []
        elif current:
            blocks[current].append(line)
    return blocks


def service_blocks(text: str) -> dict[str, list[str]]:
    """Extrai blocos diretamente abaixo de ``services`` pela indentação."""
    return section_blocks(text, "services")


def nested_mapping_keys(lines: list[str], field: str) -> set[str]:
    """Obtém chaves de um mapping de serviço com indentação Compose padrão."""
    keys: set[str] = set()
    in_mapping = False
    for line in lines:
        if line == f"    {field}:":
            in_mapping = True
            continue
        if in_mapping and line.startswith("    ") and not line.startswith("      "):
            break
        if in_mapping and (match := NESTED_KEY_RE.match(line)):
            keys.add(match.group(1))
    return keys


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
                elif in_ports and stripped.startswith("-") and not match:
                    errors.append(f"{name}: sintaxe de porta nao validavel: {stripped}")
        if name != "gateway" and "ports:" in body:
            errors.append(f"{name}: somente o gateway pode publicar portas")
        if 'restart: "no"' not in body:
            errors.append(f"{name}: restart deve ser explicitamente no")

    networks = section_blocks(text, "networks")
    lab_network = "\n".join(networks.get("rte-lab", []))
    if not lab_network or "internal: true" not in lab_network:
        errors.append("rte-lab: rede deve declarar internal: true")
    for name in ("rte-access", "rte-egress"):
        body = "\n".join(networks.get(name, []))
        if not body or "internal: false" not in body:
            errors.append(f"{name}: rede deve declarar internal: false")

    expected_networks = {
        "gateway": {"rte-access", "rte-lab"},
        "attacker": {"rte-egress", "rte-lab"},
    }
    for name, lines in blocks.items():
        expected = expected_networks.get(name, {"rte-lab"})
        actual = nested_mapping_keys(lines, "networks")
        if actual != expected:
            errors.append(
                f"{name}: redes devem ser {', '.join(sorted(expected))}; "
                f"encontradas: {', '.join(sorted(actual)) or 'nenhuma'}"
            )

    gateway = "\n".join(blocks.get("gateway", []))
    if "ports:" not in gateway:
        errors.append("gateway: nenhuma porta local publicada")
    expected_profiles = {
        "bwapp": {"extended", "full"},
        "webgoat": {"extended", "full"},
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


def mutable_base_images(text: str) -> list[str]:
    """Lista instrucoes FROM que nao usam digest."""
    return [line.strip() for line in text.splitlines() if line.strip().startswith("FROM ") and "@sha256:" not in line]


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "30-Web-API-AppSec/docker-lab/docker-compose.yml")
    text = path.read_text(encoding="utf-8")
    errors = validate(text)
    if errors:
        for error in errors:
            print(f"[ERRO] {error}", file=sys.stderr)
        return 1
    print(f"[OK] política Compose válida para {len(service_blocks(text))} serviços")
    mutable = mutable_images(text)
    if mutable:
        print(f"[ERRO] {len(mutable)} imagens sem digest imutavel", file=sys.stderr)
        return 1
    dockerfile = path.parent / "Dockerfile.kali-pentest"
    if dockerfile.is_file():
        mutable_bases = mutable_base_images(dockerfile.read_text(encoding="utf-8"))
        if mutable_bases:
            print(f"[ERRO] {len(mutable_bases)} imagens-base sem digest imutavel", file=sys.stderr)
            return 1
    print("[OK] todas as imagens Compose estao fixadas por digest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
