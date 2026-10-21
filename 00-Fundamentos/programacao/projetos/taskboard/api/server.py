#!/usr/bin/env python3
"""TaskBoard: uma API HTTP/SQLite pequena, mas com fronteiras reais.

O projeto usa apenas a biblioteca padrão para deixar visíveis as decisões que
frameworks normalmente encapsulam: roteamento, contrato JSON, transações,
status HTTP, correlação de logs e encerramento gracioso.
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import signal
import sqlite3
import sys
import time
import uuid
from contextlib import closing
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import SplitResult, parse_qsl, urlsplit

MAX_BODY_BYTES = 16 * 1024
MAX_TITLE_LENGTH = 120
DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100
MAX_OFFSET = 1_000_000
MAX_SQLITE_ID = 9_223_372_036_854_775_807
REQUEST_TIMEOUT_SECONDS = 10

TASK_COLLECTION_PATH = "/api/tasks"
TASK_PATH = re.compile(r"^/api/tasks/([0-9]+)$")
REQUEST_ID = re.compile(r"^[A-Za-z0-9._-]{8,64}$")
UNSET = object()

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND {MAX_TITLE_LENGTH}),
    done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_done_id ON tasks(done, id DESC);
CREATE TABLE IF NOT EXISTS taskboard_meta (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    revision INTEGER NOT NULL CHECK (revision >= 0)
);
INSERT OR IGNORE INTO taskboard_meta (id, revision) VALUES (1, 0);
"""


class ApiError(Exception):
    """Falha esperada, segura para apresentar ao cliente HTTP."""

    def __init__(
        self,
        status: HTTPStatus,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.details = details


class DuplicateJsonKey(ValueError):
    """Indica objeto JSON ambíguo com a mesma chave mais de uma vez."""


class TaskServer(ThreadingHTTPServer):
    """Servidor que deixa de aceitar conexões e aguarda workers no encerramento."""

    daemon_threads = False
    block_on_close = True
    allow_reuse_address = True
    request_queue_size = 64


def connect(db_path: Path) -> sqlite3.Connection:
    """Abre uma conexão curta e configura garantias para esta conexão."""
    connection = sqlite3.connect(db_path, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 5000")
    connection.execute("PRAGMA synchronous = NORMAL")
    return connection


def initialize(db_path: Path) -> None:
    """Cria diretório, schema e índice de forma idempotente."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(connect(db_path)) as connection:
        # WAL permite que leitores não bloqueiem um escritor. O modo fica
        # persistido no arquivo; as demais PRAGMAs são configuradas por conexão.
        connection.execute("PRAGMA journal_mode = WAL")
        with connection:
            connection.executescript(SCHEMA)


def normalize_title(value: Any) -> str:
    """Normaliza espaços e valida o valor de domínio ``title``."""
    if not isinstance(value, str):
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "invalid_title_type",
            "title deve ser texto",
        )
    title = " ".join(value.split())
    if not 1 <= len(title) <= MAX_TITLE_LENGTH:
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "invalid_title_length",
            f"title deve ter entre 1 e {MAX_TITLE_LENGTH} caracteres após normalização",
            details={"field": "title", "minLength": 1, "maxLength": MAX_TITLE_LENGTH},
        )
    if not title.isprintable():
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "invalid_title_characters",
            "title contém caracteres de controle não permitidos",
            details={"field": "title"},
        )
    return title


def validate_done(value: Any) -> bool:
    """Aceita booleano JSON real; 0, 1 e strings não são booleanos."""
    if not isinstance(value, bool):
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "invalid_done_type",
            "done deve ser booleano",
            details={"field": "done"},
        )
    return value


def serialize(row: sqlite3.Row) -> dict[str, Any]:
    """Converte uma linha SQLite no contrato público da API."""
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "createdAt": row["created_at"],
    }


def list_tasks(db_path: Path) -> list[dict[str, Any]]:
    """Lista todas as tarefas; função simples usada nos testes de repositório."""
    with closing(connect(db_path)) as connection:
        rows = connection.execute(
            "SELECT id, title, done, created_at FROM tasks ORDER BY id DESC"
        ).fetchall()
    return [serialize(row) for row in rows]


def query_tasks(
    db_path: Path,
    *,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = 0,
    done: bool | None = None,
    expected_revision: int | None = None,
) -> dict[str, Any]:
    """Lista uma página de um snapshot lógico e consistente.

    O ``revision`` muda em toda mutação. Páginas seguintes podem enviar a
    revisão recebida na primeira página; assim, uma alteração concorrente não
    produz silenciosamente lacunas ou duplicatas típicas de paginação por
    ``OFFSET``.
    """
    where = " WHERE done = ?" if done is not None else ""
    filter_values: tuple[int, ...] = (int(done),) if done is not None else ()

    with closing(connect(db_path)) as connection, connection:
        # Um BEGIN explícito mantém count e itens no mesmo snapshot em WAL.
        connection.execute("BEGIN")
        revision = connection.execute(
            "SELECT revision FROM taskboard_meta WHERE id = 1"
        ).fetchone()[0]
        if expected_revision is not None and revision != expected_revision:
            raise ApiError(
                HTTPStatus.CONFLICT,
                "stale_page",
                "a coleção mudou; reinicie a paginação pela primeira página",
                details={"currentRevision": revision},
            )
        total = connection.execute(
            f"SELECT COUNT(*) FROM tasks{where}",  # fragmento fixo, não vem do cliente
            filter_values,
        ).fetchone()[0]
        rows = connection.execute(
            f"""
            SELECT id, title, done, created_at
              FROM tasks{where}
             ORDER BY id DESC
             LIMIT ? OFFSET ?
            """,
            (*filter_values, limit, offset),
        ).fetchall()

    tasks = [serialize(row) for row in rows]
    return {
        "tasks": tasks,
        "page": {
            "limit": limit,
            "offset": offset,
            "total": total,
            "hasMore": offset + len(tasks) < total,
            "revision": revision,
        },
    }


def get_task(db_path: Path, task_id: int) -> dict[str, Any] | None:
    with closing(connect(db_path)) as connection:
        row = connection.execute(
            "SELECT id, title, done, created_at FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
    return serialize(row) if row is not None else None


def create_task(db_path: Path, title_value: Any) -> dict[str, Any]:
    title = normalize_title(title_value)
    created_at = (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )
    with closing(connect(db_path)) as connection, connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, created_at) VALUES (?, ?)",
            (title, created_at),
        )
        connection.execute(
            "UPDATE taskboard_meta SET revision = revision + 1 WHERE id = 1"
        )
        row = connection.execute(
            "SELECT id, title, done, created_at FROM tasks WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    if row is None:  # pragma: no cover - proteção contra violação interna
        raise RuntimeError("tarefa recém-criada não encontrada")
    return serialize(row)


def update_task(
    db_path: Path,
    task_id: int,
    done_value: Any = UNSET,
    *,
    title_value: Any = UNSET,
) -> dict[str, Any] | None:
    """Atualiza apenas campos fornecidos, em uma única transação.

    ``done_value`` permanece como terceiro argumento para preservar o exercício
    anterior; o handler também pode enviar somente ``title_value``.
    """
    assignments: list[str] = []
    values: list[Any] = []
    if title_value is not UNSET:
        assignments.append("title = ?")
        values.append(normalize_title(title_value))
    if done_value is not UNSET:
        assignments.append("done = ?")
        values.append(int(validate_done(done_value)))
    if not assignments:
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "empty_patch",
            "PATCH exige ao menos um dos campos: title ou done",
        )

    with closing(connect(db_path)) as connection, connection:
        cursor = connection.execute(
            f"UPDATE tasks SET {', '.join(assignments)} WHERE id = ?",
            (*values, task_id),
        )
        if cursor.rowcount == 0:
            return None
        connection.execute(
            "UPDATE taskboard_meta SET revision = revision + 1 WHERE id = 1"
        )
        row = connection.execute(
            "SELECT id, title, done, created_at FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
    if row is None:  # pragma: no cover - protegido pelo lock/rowcount acima
        raise RuntimeError("tarefa atualizada não encontrada")
    return serialize(row)


def delete_task(db_path: Path, task_id: int) -> bool:
    with closing(connect(db_path)) as connection, connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount > 0:
            connection.execute(
                "UPDATE taskboard_meta SET revision = revision + 1 WHERE id = 1"
            )
    return cursor.rowcount > 0


def _bounded_decimal(value: str, maximum: int) -> int | None:
    """Converte decimal limitado sem entregar milhares de dígitos a ``int``."""
    if not value.isascii() or not value.isdecimal():
        return None
    normalized = value.lstrip("0") or "0"
    maximum_text = str(maximum)
    if len(normalized) > len(maximum_text):
        return None
    if len(normalized) == len(maximum_text) and normalized > maximum_text:
        return None
    return int(normalized)


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKey(key)
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"constante JSON não permitida: {value}")


def _parse_finite_json_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"número JSON fora da faixa finita: {value}")
    return number


def _validate_fields(
    payload: dict[str, Any],
    *,
    allowed: set[str],
    required: set[str] = frozenset(),
) -> None:
    unknown = sorted(payload.keys() - allowed)
    missing = sorted(required - payload.keys())
    if unknown:
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "unknown_fields",
            "o JSON possui campos não reconhecidos",
            details={"fields": unknown},
        )
    if missing:
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "missing_fields",
            "o JSON não possui todos os campos obrigatórios",
            details={"fields": missing},
        )


def _parse_nonnegative_integer(name: str, value: str, maximum: int) -> int:
    if not value.isascii() or not value.isdecimal():
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "invalid_query_parameter",
            f"{name} deve ser um inteiro decimal não negativo",
            details={"field": name},
        )
    parsed = _bounded_decimal(value, maximum)
    if parsed is None:
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "invalid_query_parameter",
            f"{name} deve ser menor ou igual a {maximum}",
            details={"field": name, "maximum": maximum},
        )
    return parsed


def parse_list_query(query: str) -> tuple[int, int, bool | None, int | None]:
    """Valida paginação e filtro sem aceitar parâmetros silenciosamente."""
    try:
        pairs = parse_qsl(query, keep_blank_values=True, strict_parsing=True)
    except ValueError as exc:
        raise ApiError(
            HTTPStatus.BAD_REQUEST,
            "invalid_query_string",
            "query string inválida",
        ) from exc

    values: dict[str, str] = {}
    for name, value in pairs:
        if name not in {"limit", "offset", "done", "revision"}:
            raise ApiError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "unknown_query_parameter",
                f"parâmetro de consulta desconhecido: {name}",
                details={"field": name},
            )
        if name in values:
            raise ApiError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "duplicate_query_parameter",
                f"parâmetro de consulta repetido: {name}",
                details={"field": name},
            )
        values[name] = value

    limit = _parse_nonnegative_integer(
        "limit", values.get("limit", str(DEFAULT_PAGE_SIZE)), MAX_PAGE_SIZE
    )
    if limit < 1:
        raise ApiError(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "invalid_query_parameter",
            "limit deve estar entre 1 e 100",
            details={"field": "limit", "minimum": 1, "maximum": MAX_PAGE_SIZE},
        )
    offset = _parse_nonnegative_integer(
        "offset", values.get("offset", "0"), MAX_OFFSET
    )

    done: bool | None = None
    if "done" in values:
        if values["done"] not in {"true", "false"}:
            raise ApiError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "invalid_query_parameter",
                "done deve ser true ou false",
                details={"field": "done"},
            )
        done = values["done"] == "true"
    revision = (
        _parse_nonnegative_integer("revision", values["revision"], MAX_SQLITE_ID)
        if "revision" in values
        else None
    )
    return limit, offset, done, revision


def _validate_unicode_scalars(value: Any) -> None:
    """Rejeita surrogates isolados que JSON aceita, mas UTF-8 não representa."""
    if isinstance(value, str):
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError("texto JSON contém surrogate Unicode isolado") from exc
        return
    if isinstance(value, list):
        for item in value:
            _validate_unicode_scalars(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _validate_unicode_scalars(key)
            _validate_unicode_scalars(item)


class TaskHandler(BaseHTTPRequestHandler):
    """Traduz HTTP para operações de domínio e persistência."""

    db_path = Path("tasks.db")
    server_version = "TaskBoard/2.0"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(REQUEST_TIMEOUT_SECONDS)

    def version_string(self) -> str:
        return self.server_version

    def _prepare_context(self) -> None:
        candidate = self.headers.get("X-Request-ID", "")
        self.request_id = candidate if REQUEST_ID.fullmatch(candidate) else uuid.uuid4().hex
        self.response_status = HTTPStatus.INTERNAL_SERVER_ERROR
        self.started_at = time.perf_counter()
        try:
            self.parsed_target: SplitResult | None = urlsplit(self.path)
        except ValueError:
            self.parsed_target = None

    def _request_target(self) -> SplitResult:
        if self.parsed_target is None:
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "invalid_request_target",
                "alvo da requisição inválido",
            )
        return self.parsed_target

    def _send_json(
        self,
        status: HTTPStatus,
        payload: object,
        *,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        # ASCII escapado também protege a fronteira caso um valor interno
        # contenha, por engano, um surrogate Unicode isolado.
        body = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
        self.response_status = status
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Request-ID", self.request_id)
        if self.close_connection:
            self.send_header("Connection", "close")
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_empty(
        self,
        status: HTTPStatus,
        *,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.response_status = status
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Request-ID", self.request_id)
        if self.close_connection:
            self.send_header("Connection", "close")
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()

    def _send_error(self, error: ApiError) -> None:
        payload: dict[str, Any] = {
            "error": {
                "code": error.code,
                "message": str(error),
                "requestId": self.request_id,
            }
        }
        if error.details:
            payload["error"]["details"] = error.details
        self._send_json(error.status, payload)

    def _reject_body_for_bodyless_method(self) -> None:
        """Rejeita framing de corpo que esta operação não vai consumir.

        Em uma conexão HTTP/1.1 persistente, deixar bytes declarados por
        Content-Length no buffer faria o parser tratá-los como o próximo
        request. Fechamos a conexão nos casos ambíguos ou com corpo antes de
        executar qualquer leitura/escrita de domínio.
        """
        if self.headers.get("Transfer-Encoding"):
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "body_not_allowed",
                f"{self.command} não aceita corpo nesta API",
            )

        lengths = self.headers.get_all("Content-Length", failobj=[])
        if not lengths:
            return
        if len(lengths) != 1:
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "ambiguous_content_length",
                "envie no máximo um Content-Length",
            )
        value = lengths[0]
        if not value.isascii() or not value.isdecimal():
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "invalid_content_length",
                "Content-Length deve conter somente dígitos decimais",
            )
        if value.strip("0"):
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "body_not_allowed",
                f"{self.command} não aceita corpo nesta API",
            )

    def _close_if_body_will_not_be_consumed(self) -> None:
        """Impede reuso quando uma resposta deixa um possível corpo sem ler."""
        lengths = self.headers.get_all("Content-Length", failobj=[])
        if self.headers.get("Transfer-Encoding") or (lengths and lengths != ["0"]):
            self.close_connection = True

    def _read_json_object(self) -> dict[str, Any]:
        if self.headers.get("Transfer-Encoding"):
            self.close_connection = True
            raise ApiError(
                HTTPStatus.NOT_IMPLEMENTED,
                "unsupported_transfer_encoding",
                "Transfer-Encoding não é aceito; envie Content-Length",
            )

        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self.close_connection = True
            raise ApiError(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "unsupported_media_type",
                "use Content-Type application/json",
            )

        lengths = self.headers.get_all("Content-Length", failobj=[])
        if not lengths:
            self.close_connection = True
            raise ApiError(
                HTTPStatus.LENGTH_REQUIRED,
                "content_length_required",
                "Content-Length é obrigatório",
            )
        if len(lengths) != 1:
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "ambiguous_content_length",
                "envie exatamente um Content-Length",
            )
        if not lengths[0].isascii() or not lengths[0].isdecimal():
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "invalid_content_length",
                "Content-Length deve conter somente dígitos decimais",
            )
        length = _bounded_decimal(lengths[0], MAX_BODY_BYTES)
        if length is None:
            self.close_connection = True
            raise ApiError(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                "payload_too_large",
                f"o corpo excede o limite de {MAX_BODY_BYTES} bytes",
                details={"maxBytes": MAX_BODY_BYTES},
            )
        if length < 1:
            raise ApiError(HTTPStatus.BAD_REQUEST, "empty_body", "o corpo JSON está vazio")

        try:
            raw_body = self.rfile.read(length)
        except TimeoutError as exc:
            self.close_connection = True
            raise ApiError(
                HTTPStatus.REQUEST_TIMEOUT,
                "request_timeout",
                "tempo esgotado durante a leitura do corpo",
            ) from exc
        if len(raw_body) != length:
            self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "incomplete_body",
                "o corpo terminou antes do tamanho declarado",
            )

        try:
            value = json.loads(
                raw_body.decode("utf-8"),
                object_pairs_hook=_unique_json_object,
                parse_constant=_reject_json_constant,
                parse_float=_parse_finite_json_float,
            )
            _validate_unicode_scalars(value)
        except DuplicateJsonKey as exc:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "duplicate_json_key",
                f"chave JSON repetida: {exc}",
            ) from exc
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_json", "JSON inválido") from exc
        if not isinstance(value, dict):
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "invalid_json_shape",
                "o JSON deve ser um objeto",
            )
        return value

    def _task_id(self, path: str) -> int | None:
        match = TASK_PATH.fullmatch(path)
        if match is None:
            return None
        task_id = _bounded_decimal(match.group(1), MAX_SQLITE_ID)
        return task_id if task_id is not None and task_id >= 1 else None

    def _reject_query_on_write(self, query: str) -> None:
        if query:
            if self.command in {"POST", "PATCH", "PUT"}:
                self.close_connection = True
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "query_not_allowed",
                "esta operação não aceita parâmetros de consulta",
            )

    def _route_not_found(self) -> None:
        raise ApiError(HTTPStatus.NOT_FOUND, "route_not_found", "rota não encontrada")

    def _task_not_found(self) -> None:
        raise ApiError(HTTPStatus.NOT_FOUND, "task_not_found", "tarefa não encontrada")

    def _dispatch(self, operation: Callable[[], None]) -> None:
        self._prepare_context()
        try:
            operation()
        except ApiError as exc:
            self._send_error(exc)
        except sqlite3.Error:
            self.close_connection = True
            logging.exception("database_error request_id=%s", self.request_id)
            self._send_error(
                ApiError(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "erro interno")
            )
        except (BrokenPipeError, ConnectionResetError):
            logging.warning("client_disconnected request_id=%s", self.request_id)
        except Exception:
            self.close_connection = True
            logging.exception("unhandled_error request_id=%s", self.request_id)
            self._send_error(
                ApiError(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "erro interno")
            )
        finally:
            elapsed_ms = (time.perf_counter() - self.started_at) * 1000
            logging.info(
                "http_request request_id=%s client=%s method=%s path=%s status=%d duration_ms=%.2f",
                self.request_id,
                self.client_address[0],
                self.command,
                self.parsed_target.path if self.parsed_target is not None else "<invalid>",
                int(self.response_status),
                elapsed_ms,
            )

    def do_GET(self) -> None:  # noqa: N802 - nome definido pelo framework
        self._dispatch(self._get)

    def do_HEAD(self) -> None:  # noqa: N802
        self._dispatch(self._get)

    def _get(self) -> None:
        self._reject_body_for_bodyless_method()
        parsed = self._request_target()
        if parsed.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "service": "taskboard-api"})
            return
        if parsed.path == "/ready":
            try:
                if not self.db_path.is_file():
                    raise sqlite3.OperationalError("arquivo do banco ausente")
                with closing(connect(self.db_path)) as connection:
                    table = connection.execute(
                        "SELECT 1 FROM sqlite_master "
                        "WHERE type = 'table' AND name = 'tasks'"
                    ).fetchone()
                    if table is None:
                        raise sqlite3.OperationalError("schema tasks ausente")
                    connection.execute(
                        "SELECT id, title, done, created_at FROM tasks LIMIT 1"
                    ).fetchone()
                    metadata = connection.execute(
                        "SELECT revision FROM taskboard_meta WHERE id = 1"
                    ).fetchone()
                    if metadata is None:
                        raise sqlite3.OperationalError("metadados de revisão ausentes")
            except sqlite3.Error as exc:
                raise ApiError(
                    HTTPStatus.SERVICE_UNAVAILABLE,
                    "database_unavailable",
                    "banco de dados indisponível",
                ) from exc
            self._send_json(
                HTTPStatus.OK,
                {"status": "ok", "service": "taskboard-api", "database": "ready"},
            )
            return
        if parsed.path == TASK_COLLECTION_PATH:
            limit, offset, done, revision = parse_list_query(parsed.query)
            self._send_json(
                HTTPStatus.OK,
                query_tasks(
                    self.db_path,
                    limit=limit,
                    offset=offset,
                    done=done,
                    expected_revision=revision,
                ),
            )
            return

        task_id = self._task_id(parsed.path)
        if task_id is None:
            self._route_not_found()
        if parsed.query:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "query_not_allowed",
                "este recurso não aceita parâmetros de consulta",
            )
        task = get_task(self.db_path, task_id)
        if task is None:
            self._task_not_found()
        self._send_json(HTTPStatus.OK, task)

    def do_POST(self) -> None:  # noqa: N802
        self._dispatch(self._post)

    def _post(self) -> None:
        parsed = self._request_target()
        if parsed.path != TASK_COLLECTION_PATH:
            self.close_connection = True
            if self._allowed_methods(parsed.path) is not None:
                self._method_not_allowed()
                return
            self._route_not_found()
        self._reject_query_on_write(parsed.query)
        payload = self._read_json_object()
        _validate_fields(payload, allowed={"title"}, required={"title"})
        task = create_task(self.db_path, payload["title"])
        self._send_json(
            HTTPStatus.CREATED,
            task,
            extra_headers={"Location": f"/api/tasks/{task['id']}"},
        )

    def do_PATCH(self) -> None:  # noqa: N802
        self._dispatch(self._patch)

    def _patch(self) -> None:
        parsed = self._request_target()
        task_id = self._task_id(parsed.path)
        if task_id is None:
            self.close_connection = True
            if self._allowed_methods(parsed.path) is not None:
                self._method_not_allowed()
                return
            self._route_not_found()
        self._reject_query_on_write(parsed.query)
        payload = self._read_json_object()
        _validate_fields(payload, allowed={"title", "done"})
        task = update_task(
            self.db_path,
            task_id,
            payload.get("done", UNSET),
            title_value=payload.get("title", UNSET),
        )
        if task is None:
            self._task_not_found()
        self._send_json(HTTPStatus.OK, task)

    def do_DELETE(self) -> None:  # noqa: N802
        self._dispatch(self._delete)

    def _delete(self) -> None:
        self._reject_body_for_bodyless_method()
        parsed = self._request_target()
        task_id = self._task_id(parsed.path)
        if task_id is None:
            if self._allowed_methods(parsed.path) is not None:
                self._method_not_allowed()
                return
            self._route_not_found()
        self._reject_query_on_write(parsed.query)
        if not delete_task(self.db_path, task_id):
            self._task_not_found()
        self._send_empty(HTTPStatus.NO_CONTENT)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._dispatch(self._options)

    def _options(self) -> None:
        self._reject_body_for_bodyless_method()
        parsed = self._request_target()
        self._reject_query_on_write(parsed.query)
        allowed = self._allowed_methods(parsed.path)
        if allowed is None:
            self._route_not_found()
        self._send_empty(HTTPStatus.NO_CONTENT, extra_headers={"Allow": ", ".join(allowed)})

    def _method_not_allowed(self) -> None:
        # Um método inesperado pode carregar um corpo que não consumiremos.
        # Fechar esta conexão evita interpretar esses bytes como outro request.
        self._close_if_body_will_not_be_consumed()
        allowed = self._allowed_methods(self._request_target().path)
        if allowed is None:
            self._route_not_found()
        error = ApiError(
            HTTPStatus.METHOD_NOT_ALLOWED,
            "method_not_allowed",
            f"método {self.command} não permitido para esta rota",
            details={"allowed": allowed},
        )
        # RFC 9110 exige Allow em 405; o envelope também mantém a informação.
        payload = {
            "error": {
                "code": error.code,
                "message": str(error),
                "requestId": self.request_id,
                "details": error.details,
            }
        }
        self._send_json(
            error.status,
            payload,
            extra_headers={"Allow": ", ".join(allowed)},
        )

    @staticmethod
    def _allowed_methods(path: str) -> list[str] | None:
        if path in {"/health", "/ready"}:
            return ["GET", "HEAD", "OPTIONS"]
        if path == TASK_COLLECTION_PATH:
            return ["GET", "HEAD", "POST", "OPTIONS"]
        match = TASK_PATH.fullmatch(path)
        task_id = _bounded_decimal(match.group(1), MAX_SQLITE_ID) if match else None
        if task_id is not None and task_id >= 1:
            return ["GET", "HEAD", "PATCH", "DELETE", "OPTIONS"]
        return None

    def do_PUT(self) -> None:  # noqa: N802
        self._dispatch(self._method_not_allowed)

    def do_TRACE(self) -> None:  # noqa: N802
        self._dispatch(self._method_not_allowed)

    def do_CONNECT(self) -> None:  # noqa: N802
        self._dispatch(self._method_not_allowed)

    def _dispatch_unknown_method(self) -> None:
        self._dispatch(self._method_not_allowed)

    def __getattr__(self, name: str) -> Any:
        """Mantém o envelope JSON também para métodos HTTP desconhecidos."""
        if name.startswith("do_"):
            return self._dispatch_unknown_method
        raise AttributeError(name)

    def log_message(self, template: str, *args: object) -> None:
        # O log estruturado é emitido uma vez em _dispatch.
        logging.debug("http_server message=%s", template % args)


def make_server(host: str, port: int, db_path: Path) -> TaskServer:
    initialize(db_path)

    class ConfiguredTaskHandler(TaskHandler):
        pass

    ConfiguredTaskHandler.db_path = db_path
    return TaskServer((host, port), ConfiguredTaskHandler)


def main() -> int:
    host = os.environ.get("APP_HOST", "127.0.0.1")
    try:
        port = int(os.environ.get("APP_PORT", "8000"))
    except ValueError:
        print("APP_PORT deve ser inteiro", file=sys.stderr)
        return 2
    if not 1 <= port <= 65535:
        print("APP_PORT deve estar entre 1 e 65535", file=sys.stderr)
        return 2

    db_path = Path(os.environ.get("APP_DB_PATH", "data/tasks.db"))
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    server = make_server(host, port, db_path)

    previous_sigterm = signal.getsignal(signal.SIGTERM)

    def request_shutdown(signum: int, _frame: object) -> None:
        raise KeyboardInterrupt(f"signal {signum}")

    signal.signal(signal.SIGTERM, request_shutdown)
    logging.info("server_started host=%s port=%d db=%s", host, port, db_path)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        logging.info("server_stopping")
    finally:
        signal.signal(signal.SIGTERM, previous_sigterm)
        server.server_close()
        logging.info("server_stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
