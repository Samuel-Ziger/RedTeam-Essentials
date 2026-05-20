#!/usr/bin/env python3
"""
port_scanner.py - Scanner TCP assincrono educacional.

Usa asyncio.open_connection com timeout curto para descobrir portas abertas
em alvos autorizados. Suporta:
    * Faixa de portas (1-1024, 22,80,443, top100, top1000)
    * Banner grab basico (envia probe HTTP/empty e le ate 256 bytes)
    * Concurrency configuravel
    * Exportacao JSON

Nao substitui Nmap; e didatico e portavel (so stdlib).

Uso:
    python port_scanner.py -t 10.0.0.1 -p 1-1024 --banner
    python port_scanner.py -t scanme.nmap.org -p top1000 --concurrency 500

Autor:    Samuel Ziger - RedTeam Essentials
Versao:   2.0.0
Licenca:  MIT
"""
from __future__ import annotations

import argparse
import asyncio
import socket
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib" / "python"))
from rte_common import (  # noqa: E402
    RTEContext,
    confirm_authorization,
    export_json,
    get_logger,
    is_valid_domain,
    is_valid_ipv4,
    log_success,
)

LOG = get_logger("rte.portscan")

# Top portas mais comuns (extraido do nmap-services).
TOP_100 = [
    7,9,13,21,22,23,25,26,37,53,79,80,81,88,106,110,111,113,119,135,139,143,144,179,199,
    389,427,443,444,445,465,513,514,515,543,544,548,554,587,631,636,646,873,990,993,995,
    1025,1026,1027,1028,1029,1110,1433,1720,1723,1755,1900,2000,2001,2049,2121,2717,3000,
    3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,
    6000,6001,6646,7070,8000,8008,8009,8080,8081,8443,8888,9100,9999,10000,32768,49152,
    49153,49154,49155,49156,49157,
]
TOP_1000 = TOP_100 + list(range(1, 1001))  # superset suficiente para o didatico

PROBES = {
    80:  b"GET / HTTP/1.0\r\nHost: localhost\r\n\r\n",
    443: b"",
    21:  b"",
    22:  b"",
    25:  b"EHLO scanner.local\r\n",
}


def parse_ports(spec: str) -> list[int]:
    """Aceita 22 / 22,80 / 1-1024 / top100 / top1000."""
    spec = spec.strip().lower()
    if spec == "top100":
        return sorted(set(TOP_100))
    if spec == "top1000":
        return sorted(set(TOP_1000))
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return sorted(p for p in out if 1 <= p <= 65535)


async def scan_port(host: str, port: int, timeout: float, do_banner: bool) -> dict | None:
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
    except (OSError, asyncio.TimeoutError):
        return None

    banner = ""
    if do_banner:
        try:
            probe = PROBES.get(port, b"")
            if probe:
                writer.write(probe)
                await writer.drain()
            data = await asyncio.wait_for(reader.read(256), timeout=timeout)
            banner = data.decode("utf-8", errors="replace").strip()
        except Exception:  # noqa: BLE001
            banner = ""

    try:
        writer.close()
        await writer.wait_closed()
    except Exception:  # noqa: BLE001
        pass

    return {"port": port, "state": "open", "banner": banner[:240]}


async def run_scan(host: str, ports: Iterable[int], concurrency: int, timeout: float, banner: bool) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)
    open_ports: list[dict] = []

    async def task(p: int) -> None:
        async with sem:
            r = await scan_port(host, p, timeout, banner)
            if r:
                LOG.info("aberta %5d %s", r["port"], (r["banner"][:40] + "…") if r["banner"] else "")
                open_ports.append(r)

    await asyncio.gather(*(task(p) for p in ports))
    return sorted(open_ports, key=lambda r: r["port"])


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scanner TCP assincrono educacional")
    p.add_argument("-t", "--target", required=True, help="host ou IP")
    p.add_argument("-p", "--ports", default="top100", help="22 / 1-1024 / top100 / top1000")
    p.add_argument("--timeout", type=float, default=1.0, help="timeout por porta (segundos)")
    p.add_argument("--concurrency", type=int, default=500, help="paralelismo")
    p.add_argument("--banner", action="store_true", help="tentar banner grab")
    p.add_argument("-o", "--output", default="./output", help="diretorio de saida")
    p.add_argument("--no-confirm", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ctx = RTEContext(tool="Port Scanner", output_dir=Path(args.output))
    ctx.banner()

    if not (is_valid_domain(args.target) or is_valid_ipv4(args.target)):
        # Permite hosts como "scanme.nmap.org" via getaddrinfo, mas valida o input minimamente
        if not args.target.replace(".", "").replace("-", "").replace(":", "").isalnum():
            LOG.error("Alvo invalido: %s", args.target)
            return 1

    if not args.no_confirm:
        confirm_authorization(force=False)

    try:
        resolved = socket.gethostbyname(args.target)
        log_success(LOG, f"Resolvido {args.target} -> {resolved}")
    except socket.gaierror as exc:
        LOG.error("Falha de DNS: %s", exc)
        return 1

    ports = parse_ports(args.ports)
    LOG.info("Escaneando %d portas em %s ...", len(ports), args.target)

    results = asyncio.run(
        run_scan(args.target, ports, args.concurrency, args.timeout, args.banner)
    )

    output = {
        "metadata": {
            "tool": "port_scanner.py", "version": "2.0.0",
            "target": args.target, "resolved": resolved,
            "ports_scanned": len(ports), "concurrency": args.concurrency,
        },
        "open_ports": results,
        "summary": {"open_count": len(results)},
    }
    path = export_json(output, args.output, f"portscan_{args.target}")
    log_success(LOG, f"Salvo em {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
