#!/usr/bin/env python3
"""Cliente somente-leitura da Inventory API usando a biblioteca padrão."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_RESPONSE_BYTES = 1_000_000


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(
        self, request: Any, file_pointer: Any, code: int, message: str, headers: Any, new_url: str
    ) -> None:
        return None


@dataclass(frozen=True)
class ApiResponse:
    status: int
    request_id: str | None
    body: dict[str, Any]


class ApiProblem(RuntimeError):
    """Erro HTTP com Problem Details ou resposta equivalente."""

    def __init__(self, status: int, body: dict[str, Any]) -> None:
        self.status = status
        self.body = body
        detail = body.get("detail", "resposta HTTP sem sucesso")
        super().__init__(f"HTTP {status}: {detail}")


def _decode_object(raw_body: bytes) -> dict[str, Any]:
    try:
        body = json.loads(raw_body)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("resposta não contém JSON UTF-8 válido") from error
    if not isinstance(body, dict):
        raise RuntimeError("o contrato esperava um objeto JSON")
    return body


def _read_limited(response: Any) -> bytes:
    declared = response.headers.get("Content-Length")
    if declared is not None:
        try:
            if int(declared) > MAX_RESPONSE_BYTES:
                raise RuntimeError("resposta maior que o limite de 1 MB")
        except ValueError as error:
            raise RuntimeError("Content-Length inválido na resposta") from error

    raw_body = response.read(MAX_RESPONSE_BYTES + 1)
    if len(raw_body) > MAX_RESPONSE_BYTES:
        raise RuntimeError("resposta maior que o limite de 1 MB")
    return raw_body


def get_json(base_url: str, path: str, *, timeout: float = 3.0) -> ApiResponse:
    request = Request(
        f"{base_url.rstrip('/')}{path}",
        headers={"Accept": "application/json", "User-Agent": "rte-python-client/1"},
        method="GET",
    )
    try:
        with build_opener(_NoRedirect).open(request, timeout=timeout) as response:  # noqa: S310 - URL local controlada
            body = _decode_object(_read_limited(response))
            return ApiResponse(
                status=response.status,
                request_id=response.headers.get("X-Request-ID"),
                body=body,
            )
    except HTTPError as error:
        try:
            problem = _decode_object(_read_limited(error))
        except RuntimeError:
            problem = {"detail": "resposta de erro não contém JSON válido"}
        raise ApiProblem(error.code, problem) from error


def _product_summary(value: Any) -> tuple[str, str, int]:
    if not isinstance(value, dict):
        raise RuntimeError("item de produto não é um objeto")
    sku = value.get("sku")
    name = value.get("name")
    stock = value.get("stock")
    if not isinstance(sku, str) or not isinstance(name, str) or type(stock) is not int:
        raise RuntimeError("item de produto incompatível com o contrato")
    return sku, name, stock


def main() -> int:
    base_url = os.environ.get("INVENTORY_URL", "http://127.0.0.1:8101")
    try:
        health = get_json(base_url, "/health/live")
        page = get_json(base_url, "/api/v1/products?limit=5")
    except (ApiProblem, URLError, TimeoutError, ValueError, RuntimeError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 1

    items = page.body.get("items")
    if health.body.get("status") != "ok" or not isinstance(items, list):
        print("erro: resposta incompatível com o contrato", file=sys.stderr)
        return 1

    print(f"health={health.body['status']} request_id={health.request_id}")
    print(f"produtos={len(items)} proximo_cursor={page.body.get('nextCursor')}")
    try:
        summaries = [_product_summary(item) for item in items]
    except RuntimeError as error:
        print(f"erro: {error}", file=sys.stderr)
        return 1
    for sku, name, stock in summaries:
        print(f"- {sku}: {name} (estoque={stock})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
