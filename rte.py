#!/usr/bin/env python3
"""Interface unificada e segura para navegar, validar e operar o projeto."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "MODULE-CATALOG.json"
ANALYZERS = {
    "api": ROOT / "40-Capstone-Purple-Team/acervo/tools/api_auth_matrix.py",
    "cloud": ROOT / "32-Cloud-Security/cloud-red-team/labs/analyze_events.py",
    "edge-policy": ROOT / "26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/exemplos/control_plane_audit.py",
    "edge-risk": ROOT / "26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/exemplos/edge_risk_engine.py",
    "evidence": ROOT / "25-Cursos/atribuicao-defensiva/exemplos/evidence_manifest.py",
    "lateral": ROOT / "37-Pos-Exploracao-Movimento-Lateral/acervo/movimento-lateral/lateral_path_analyzer.py",
    "network": ROOT / "37-Pos-Exploracao-Movimento-Lateral/acervo/pivoting/path_analyzer.py",
    "privacy": ROOT / "23-Threat-Intel-Emulation/privacidade-anonimato-fundamentos/exemplos/privacy_model.py",
    "rate-limit": ROOT / "26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/exemplos/token_bucket.py",
    "recon": ROOT / "40-Capstone-Purple-Team/acervo/tools/recon_correlator.py",
    "telemetry": ROOT / "25-Cursos/atribuicao-defensiva/exemplos/telemetry_correlator.py",
    "vpn-plan": ROOT / "24-Lateral-Movement/vpn-propria-operacao-segura/exemplos/wireguard_plan.py",
    "vpn-policy": ROOT / "24-Lateral-Movement/vpn-propria-operacao-segura/exemplos/vpn_policy_audit.py",
}
VALIDATORS = (
    ROOT / "scripts/validate_module_catalog.py",
    ROOT / "scripts/validate_attack_mapping.py",
    ROOT / "scripts/validate_compose_policy.py",
    ROOT / "scripts/validate_video_catalog.py",
    ROOT / "scripts/validate_local_links.py",
    ROOT / "scripts/validate_supply_chain.py",
    ROOT / "scripts/validate_windows_courses.py",
    ROOT / "scripts/validate_macos_courses.py",
    ROOT / "scripts/validate_network_courses.py",
    ROOT / "scripts/validate_crypto_courses.py",
    ROOT / "scripts/validate_privacy_courses.py",
    ROOT / "scripts/validate_edge_security_course.py",
    ROOT / "scripts/validate_study_app.py",
)


def load_catalog(path: Path = CATALOG) -> dict[str, Any]:
    """Carrega a fonte canônica de módulos."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("modules"), list):
        raise ValueError("catalogo de modulos invalido")
    return data


def compose_command(action: str, profile: str, *, build: bool = False, volumes: bool = False) -> list[str]:
    """Monta um comando Compose limitado aos perfis conhecidos."""
    if profile not in {"basic", "api", "extended", "full"}:
        raise ValueError(f"perfil desconhecido: {profile}")
    command = [
        "docker",
        "compose",
        "-f",
        str(ROOT / "30-Web-API-AppSec/docker-lab/docker-compose.yml"),
    ]
    if profile != "basic":
        command.extend(["--profile", profile])
    if action == "up":
        command.extend(["up", "-d"])
        if build:
            command.append("--build")
    elif action == "down":
        command.append("down")
        if volumes:
            command.append("--volumes")
    elif action == "config":
        command.extend(["config", "--quiet"])
    elif action == "status":
        command.append("ps")
    else:
        raise ValueError(f"acao Compose desconhecida: {action}")
    return command


def run(command: Sequence[str]) -> int:
    """Executa apenas comandos previamente construídos pelo CLI."""
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def modules_command(args: argparse.Namespace) -> int:
    try:
        modules = load_catalog()["modules"]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 2
    if args.status:
        modules = [item for item in modules if item.get("status") == args.status]
    if args.json:
        print(json.dumps(modules, ensure_ascii=False, indent=2))
        return 0
    print("ID  STATUS       HORAS   MODULO")
    for module in modules:
        hours = module["estimatedHours"]
        if module["status"] == "catalog":
            estimate = "n/a"
        else:
            estimate = str(hours["min"]) if hours["min"] == hours["max"] else f"{hours['min']}-{hours['max']}"
        print(f"{module['id']}  {module['status']:<12} {estimate:>5}   {module['title']}")
    return 0


def validate_command(args: argparse.Namespace) -> int:
    commands: list[list[str]] = [[sys.executable, str(path)] for path in VALIDATORS]
    commands.extend(([sys.executable, str(ROOT / "scripts/scan_secrets.py")],))
    if args.all:
        commands.extend(
            (
                [sys.executable, "-m", "pytest"],
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    str(ROOT / "study-app/scripts/tests"),
                    "-p",
                    "test_*.py",
                    "-v",
                ],
                ["npm", "--prefix", str(ROOT / "study-app"), "test"],
                ["bash", str(ROOT / "tests/bash/test_rte_common.sh")],
                ["bash", str(ROOT / "00-Fundamentos/programacao/testar-curso.sh")],
                ["bash", str(ROOT / "01-Recon/programacao-avancada/testar-curso.sh")],
                ["bash", str(ROOT / "02-OSINT/engenharia-software/testar-curso.sh")],
                ["bash", str(ROOT / "03-AD-Notes/desenvolvimento-aplicacoes/testar-curso.sh")],
                ["bash", str(ROOT / "04-Automation/automacao-profissional/testar-curso.sh")],
                ["bash", str(ROOT / "05-DFIR/engenharia-apis/testar-curso.sh")],
                ["bash", str(ROOT / "06-Cheatsheets/linux-do-zero-ao-avancado/testar-curso.sh")],
                ["bash", str(ROOT / "07-Web-AppSec/linux-avancado/testar-curso.sh")],
                ["bash", str(ROOT / "08-Cloud-RedTeam/windows-domestico-fundamentos/testar-curso.sh")],
                ["bash", str(ROOT / "09-C2-Evasion/windows-domestico-avancado/testar-curso.sh")],
                ["bash", str(ROOT / "10-Container-Sec/windows-empresarial-fundamentos/testar-curso.sh")],
                ["bash", str(ROOT / "11-Python-Tools/windows-empresarial-avancado/testar-curso.sh")],
                ["bash", str(ROOT / "12-Java-Tools/macos-fundamentos/testar-curso.sh")],
                ["bash", str(ROOT / "13-Initial-Access/macos-avancado/testar-curso.sh")],
                ["bash", str(ROOT / "14-Post-Exploitation/redes-fundamentos/testar-curso.sh")],
                ["bash", str(ROOT / "15-Hybrid-Identity/redes-domesticas/testar-curso.sh")],
                ["bash", str(ROOT / "16-CICD-Supply-Chain/switching-vlans/testar-curso.sh")],
                ["bash", str(ROOT / "17-macOS-Security/roteamento-vpns/testar-curso.sh")],
                ["bash", str(ROOT / "18-Mobile-Security/redes-empresariais-protocolos/testar-curso.sh")],
                ["bash", str(ROOT / "19-Wireless-Security/criptografia-fundamentos/testar-curso.sh")],
                ["bash", str(ROOT / "20-Offensive-Labs/criptografia-moderna/testar-curso.sh")],
                ["bash", str(ROOT / "21-Network-Pivoting/criptografia-aplicada/testar-curso.sh")],
                ["bash", str(ROOT / "22-Secure-Code-Review/engenharia-criptografica/testar-curso.sh")],
                ["bash", str(ROOT / "23-Threat-Intel-Emulation/privacidade-anonimato-fundamentos/testar-curso.sh")],
                ["bash", str(ROOT / "24-Lateral-Movement/vpn-propria-operacao-segura/testar-curso.sh")],
                ["bash", str(ROOT / "25-Cursos/atribuicao-defensiva/testar-curso.sh")],
                ["bash", str(ROOT / "26-Ofensivo-Defensivo/defesa-perimetro-aplicacoes/testar-curso.sh")],
            )
        )
    failures = 0
    for command in commands:
        print(f"\n==> {' '.join(command)}", flush=True)
        failures += run(command) != 0
    if failures:
        print(f"\n[FALHA] {failures} etapa(s) falharam.", file=sys.stderr)
        return 1
    print("\n[OK] validacoes concluidas.")
    return 0


def scope_command(args: argparse.Namespace) -> int:
    return run(
        [
            sys.executable,
            str(ROOT / "27-Operacoes-Seguranca-Avancadas/acervo/ferramentas/roe_scope_guard.py"),
            "--scope",
            str(args.scope),
            "--target",
            args.target,
        ]
    )


def analyze_command(args: argparse.Namespace) -> int:
    return run([sys.executable, str(ANALYZERS[args.analyzer]), *args.arguments])


def lab_command(args: argparse.Namespace) -> int:
    if args.action == "doctor":
        command = ["bash", str(ROOT / "30-Web-API-AppSec/docker-lab/lab-doctor.sh")]
        if args.config_only:
            command.append("--config-only")
        return run(command)
    return run(compose_command(args.action, args.profile, build=args.build, volumes=args.volumes))


def report_command(args: argparse.Namespace) -> int:
    command = ["bash", str(ROOT / "report/generate-pdf.sh")]
    if args.input:
        command.append(str(args.input))
    return run(command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    modules = subparsers.add_parser("modules", help="lista a trilha canonica de modulos")
    modules.add_argument("--status", choices=("active", "theory-only", "catalog"))
    modules.add_argument("--json", action="store_true")
    modules.set_defaults(handler=modules_command)

    validate = subparsers.add_parser("validate", help="executa validacoes offline")
    validate.add_argument("--all", action="store_true", help="inclui suites Python e Bash")
    validate.set_defaults(handler=validate_command)

    scope = subparsers.add_parser("scope", help="verifica um alvo contra uma allowlist RoE")
    scope.add_argument("--scope", required=True, type=Path)
    scope.add_argument("--target", required=True)
    scope.set_defaults(handler=scope_command)

    analyze = subparsers.add_parser("analyze", help="executa um analisador totalmente offline")
    analyze.add_argument("analyzer", choices=sorted(ANALYZERS))
    analyze.add_argument("arguments", nargs=argparse.REMAINDER, help="argumentos do analisador")
    analyze.set_defaults(handler=analyze_command)

    lab = subparsers.add_parser("lab", help="opera somente o Compose local do projeto")
    lab.add_argument("action", choices=("config", "doctor", "down", "status", "up"))
    lab.add_argument("--profile", choices=("basic", "api", "extended", "full"), default="basic")
    lab.add_argument("--build", action="store_true", help="reconstroi a estacao atacante ao subir")
    lab.add_argument("--volumes", action="store_true", help="remove volumes no teardown")
    lab.add_argument("--config-only", action="store_true", help="doctor sem acessar o daemon")
    lab.set_defaults(handler=lab_command)

    report = subparsers.add_parser("report", help="gera PDF e arquivo 7z")
    report.add_argument("input", nargs="?", type=Path)
    report.set_defaults(handler=report_command)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
