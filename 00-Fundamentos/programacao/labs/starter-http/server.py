#!/usr/bin/env python3
"""Primeiro servidor HTTP do Lab 04: pequeno, local e testável.

Este starter implementa somente ``GET /health`` e o erro de rota. O estudante
o amplia em fatias: domínio, repositório SQLite e, por fim, o CRUD de livros.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Sequence
from urllib.parse import SplitResult, urlsplit


class LocalThreadingHTTPServer(ThreadingHTTPServer):
    """Servidor cujas threads de request não impedem o encerramento do processo."""

    daemon_threads = True
    allow_reuse_address = True


class StarterHandler(BaseHTTPRequestHandler):
    """Traduz uma mensagem HTTP em uma pequena decisão de roteamento."""

    protocol_version = "HTTP/1.1"
    server_version = "RTEStarter/1.0"
    sys_version = ""

    def send_json(self, status: HTTPStatus, document: dict[str, Any]) -> None:
        """Serializa uma resposta uma vez e declara exatamente seu tamanho."""
        body = json.dumps(
            document,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def reject_unconsumed_body(self) -> bool:
        """Fecha a conexão se um GET tentar deixar bytes residuais no buffer."""
        lengths = self.headers.get_all("Content-Length", failobj=[])
        transfer_encoding = self.headers.get("Transfer-Encoding")
        valid_empty_length = (
            not lengths
            or (
                len(lengths) == 1
                and lengths[0].isascii()
                and lengths[0].isdecimal()
                and not lengths[0].strip("0")
            )
        )
        if not transfer_encoding and valid_empty_length:
            return False
        self.close_connection = True
        self.send_json(
            HTTPStatus.BAD_REQUEST,
            {"error": {"code": "body_not_allowed", "message": "GET não aceita corpo"}},
        )
        return True

    def request_target(self) -> SplitResult | None:
        """Interpreta o alvo sem deixar um ValueError derrubar o handler."""
        try:
            return urlsplit(self.path)
        except ValueError:
            self.close_connection = True
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    "error": {
                        "code": "invalid_request_target",
                        "message": "alvo da requisição inválido",
                    }
                },
            )
            return None

    def do_GET(self) -> None:  # noqa: N802 - nome definido pelo framework
        if self.reject_unconsumed_body():
            return
        target = self.request_target()
        if target is None:
            return
        if target.path == "/health" and not target.query:
            self.send_json(HTTPStatus.OK, {"status": "ok"})
            return

        self.send_json(
            HTTPStatus.NOT_FOUND,
            {
                "error": {
                    "code": "route_not_found",
                    "message": "rota não encontrada",
                }
            },
        )

    def log_message(self, format_: str, *args: object) -> None:
        """Mantém o log didático local sem tentar resolver DNS reverso."""
        del format_
        try:
            path = urlsplit(self.path).path
        except ValueError:
            path = "<invalid>"
        status = args[1] if len(args) > 1 else "-"
        print(f"http method={self.command} path={path!r} status={status}")


def require_loopback(host: str) -> str:
    """Aceita apenas endereço IP de loopback explícito."""
    try:
        address = ipaddress.ip_address(host)
    except ValueError as exc:
        raise ValueError("use um IP de loopback explícito, como 127.0.0.1") from exc
    if not address.is_loopback:
        raise ValueError("o starter deve escutar somente em loopback")
    return host


def make_server(host: str = "127.0.0.1", port: int = 0) -> LocalThreadingHTTPServer:
    """Cria o servidor; porta zero pede uma porta efêmera ao sistema."""
    require_loopback(host)
    if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65535:
        raise ValueError("porta deve ser um inteiro entre 0 e 65535")
    return LocalThreadingHTTPServer((host, port), StarterHandler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        server = make_server(args.host, args.port)
    except (OSError, ValueError) as exc:
        print(f"erro de inicialização: {exc}", file=sys.stderr)
        return 2

    with server:
        host, port = server.server_address[:2]
        print(f"starter ativo em http://{host}:{port}")
        try:
            server.serve_forever(poll_interval=0.1)
        except KeyboardInterrupt:
            print("encerrando starter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
