#!/usr/bin/env python3
"""
subdomain_enum.py - Enumeracao passiva de subdominios.

Fontes consultadas (somente APIs publicas/gratuitas):
    * crt.sh (Certificate Transparency)
    * HackerTarget (limite gratuito)
    * AlienVault OTX

Verifica cada subdominio resolvendo via DNS (asyncio + resolver do sistema).
Exporta JSON com metadata, lista bruta e lista "live" (que resolveu).

Uso:
    python subdomain_enum.py -d exemplo.com --resolve -o ./output
    python subdomain_enum.py -d exemplo.com --sources crtsh,hackertarget

Autor:    Samuel Ziger - RedTeam Essentials
Versao:   2.0.0
Licenca:  MIT
"""
from __future__ import annotations

import argparse
import asyncio
import json
import socket
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Permite rodar standalone OU como modulo
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib" / "python"))
from rte_common import (  # noqa: E402
    RTEContext,
    confirm_authorization,
    export_json,
    get_logger,
    is_valid_domain,
    log_success,
)

LOG = get_logger("rte.subdomain")
USER_AGENT = "RTE-SubdomainEnum/2.0"

SOURCES = {"crtsh", "hackertarget", "otx"}


def _http_get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_crtsh(domain: str) -> set[str]:
    LOG.info("crt.sh ...")
    try:
        raw = _http_get(f"https://crt.sh/?q={urllib.parse.quote('%.' + domain)}&output=json")
        data = json.loads(raw)
        names: set[str] = set()
        for row in data:
            for value in str(row.get("name_value", "")).splitlines():
                v = value.strip().lower().lstrip("*.")
                if v.endswith(f".{domain}") or v == domain:
                    names.add(v)
        return names
    except Exception as exc:  # noqa: BLE001
        LOG.warning("crt.sh falhou: %s", exc)
        return set()


def fetch_hackertarget(domain: str) -> set[str]:
    LOG.info("HackerTarget ...")
    try:
        raw = _http_get(f"https://api.hackertarget.com/hostsearch/?q={urllib.parse.quote(domain)}")
        if "API count exceeded" in raw or "error" in raw.lower():
            LOG.warning("HackerTarget: limite atingido")
            return set()
        names = set()
        for line in raw.splitlines():
            host = line.split(",", 1)[0].strip().lower()
            if host.endswith(f".{domain}") or host == domain:
                names.add(host)
        return names
    except Exception as exc:  # noqa: BLE001
        LOG.warning("HackerTarget falhou: %s", exc)
        return set()


def fetch_otx(domain: str) -> set[str]:
    LOG.info("AlienVault OTX ...")
    try:
        raw = _http_get(f"https://otx.alienvault.com/api/v1/indicators/domain/{urllib.parse.quote(domain)}/passive_dns")
        data = json.loads(raw)
        names = set()
        for row in data.get("passive_dns", []):
            host = str(row.get("hostname", "")).strip().lower()
            if host.endswith(f".{domain}") or host == domain:
                names.add(host)
        return names
    except Exception as exc:  # noqa: BLE001
        LOG.warning("OTX falhou: %s", exc)
        return set()


SOURCE_FN = {"crtsh": fetch_crtsh, "hackertarget": fetch_hackertarget, "otx": fetch_otx}


async def resolve_host(host: str, sem: asyncio.Semaphore, executor: ThreadPoolExecutor) -> tuple[str, list[str]] | None:
    """Resolve via getaddrinfo em thread; retorna (host, ips) ou None."""
    async with sem:
        loop = asyncio.get_running_loop()
        try:
            infos = await loop.run_in_executor(executor, socket.getaddrinfo, host, None)
            ips = sorted({i[4][0] for i in infos})
            return host, ips
        except (socket.gaierror, socket.herror, OSError):
            return None


async def resolve_all(hosts: list[str], concurrency: int = 100) -> dict[str, list[str]]:
    LOG.info("Resolvendo %d hosts (concurrency=%d)...", len(hosts), concurrency)
    sem = asyncio.Semaphore(concurrency)
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        results = await asyncio.gather(*(resolve_host(h, sem, ex) for h in hosts))
    live = {h: ips for r in results if r for (h, ips) in [r]}
    log_success(LOG, f"Hosts vivos: {len(live)}/{len(hosts)}")
    return live


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Enumeracao passiva de subdominios")
    p.add_argument("-d", "--domain", required=True, help="dominio alvo (ex: exemplo.com)")
    p.add_argument("-o", "--output", default="./output", help="diretorio de saida")
    p.add_argument(
        "--sources",
        default="crtsh,hackertarget,otx",
        help="fontes separadas por virgula (crtsh,hackertarget,otx)",
    )
    p.add_argument("--resolve", action="store_true", help="resolve cada subdominio (live)")
    p.add_argument("--concurrency", type=int, default=100, help="paralelismo do DNS resolve")
    p.add_argument("--no-confirm", action="store_true", help="pula confirmacao etica")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ctx = RTEContext(tool="Subdomain Enum", output_dir=Path(args.output))
    ctx.banner()

    if not is_valid_domain(args.domain):
        LOG.error("Dominio invalido: %s", args.domain)
        return 1
    if not args.no_confirm:
        confirm_authorization(force=False)

    chosen = {s.strip() for s in args.sources.split(",")} & SOURCES
    if not chosen:
        LOG.error("Nenhuma fonte valida selecionada.")
        return 1

    aggregated: set[str] = set()
    per_source: dict[str, list[str]] = {}
    for src in sorted(chosen):
        names = SOURCE_FN[src](args.domain)
        per_source[src] = sorted(names)
        aggregated |= names
        log_success(LOG, f"{src}: {len(names)} resultados")

    live: dict[str, list[str]] = {}
    if args.resolve and aggregated:
        live = asyncio.run(resolve_all(sorted(aggregated), concurrency=args.concurrency))

    output = {
        "metadata": {
            "tool": "subdomain_enum.py",
            "version": "2.0.0",
            "target": args.domain,
            "sources": sorted(chosen),
        },
        "subdomains": sorted(aggregated),
        "per_source": per_source,
        "live": live,
        "summary": {
            "total_unique": len(aggregated),
            "live_count": len(live),
        },
    }
    path = export_json(output, args.output, f"subdomains_{args.domain}")
    log_success(LOG, f"Salvo em {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
