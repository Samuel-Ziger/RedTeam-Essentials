#!/usr/bin/env python3
"""Servidor HTTP efêmero usado para executar os cinco clientes sem Docker."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class ContractHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:  # noqa: N802 - API definida por BaseHTTPRequestHandler
        if self.path == "/health/live":
            self._json(200, {"status": "ok"})
            return
        if self.path == "/api/v1/products?limit=5":
            self._json(
                200,
                {
                    "items": [
                        {
                            "id": "00000000-0000-4000-8000-000000000001",
                            "sku": "BOOK-001",
                            "name": "Banco de Dados",
                            "priceCents": 4500,
                            "stock": 2,
                            "version": 1,
                            "createdAt": "2026-09-29T18:00:00Z",
                            "updatedAt": "2026-09-29T18:00:00Z",
                        }
                    ],
                    "nextCursor": None,
                },
            )
            return
        if self.path == "/problem":
            self._json(
                409,
                {
                    "type": "https://inventory.example.test/problems/example",
                    "title": "Example conflict",
                    "status": 409,
                    "detail": "conflito de teste",
                },
                content_type="application/problem+json",
            )
            return
        if self.path == "/invalid-json":
            self._body(200, b"not-json", "application/json")
            return
        if self.path == "/array":
            self._json(200, [1, 2, 3])
            return
        if self.path == "/too-large":
            self._body(200, b"x" * 1_000_001, "application/json")
            return
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/health/live")
            self.send_header("Content-Length", "0")
            self.send_header("Connection", "close")
            self.end_headers()
            return
        self._json(404, {"detail": "not found"}, content_type="application/problem+json")

    def _json(
        self,
        status: int,
        value: Any,
        *,
        content_type: str = "application/json",
    ) -> None:
        self._body(
            status,
            json.dumps(value, separators=(",", ":")).encode(),
            content_type,
        )

    def _body(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", "mock-request-001")
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            self.wfile.write(body)
        except BrokenPipeError:
            pass

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0, help="porta; zero escolhe uma livre")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("--port deve estar entre 0 e 65535")

    server = ThreadingHTTPServer(("127.0.0.1", args.port), ContractHandler)
    print(server.server_port, flush=True)
    try:
        server.serve_forever(poll_interval=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
