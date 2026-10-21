"""Testes de unidade, integração HTTP e concorrência do TaskBoard."""

from __future__ import annotations

import concurrent.futures
import http.client
import json
import os
import socket
import sqlite3
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from contextlib import closing
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import server as server_module  # noqa: E402 - permite ajustar timeout no teste

from server import (  # noqa: E402 - importa o arquivo local do projeto
    MAX_BODY_BYTES,
    ApiError,
    create_task,
    delete_task,
    get_task,
    initialize,
    list_tasks,
    make_server,
    normalize_title,
    parse_list_query,
    query_tasks,
    update_task,
)


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temporary.name) / "nested" / "tasks.db"
        initialize(self.db_path)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_initialize_is_idempotent_and_configures_schema(self) -> None:
        initialize(self.db_path)
        with closing(sqlite3.connect(self.db_path)) as connection, connection:
            journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
            indexes = {
                row[1] for row in connection.execute("PRAGMA index_list(tasks)").fetchall()
            }
            revision = connection.execute(
                "SELECT revision FROM taskboard_meta WHERE id = 1"
            ).fetchone()[0]
        self.assertEqual(journal_mode, "wal")
        self.assertIn("idx_tasks_done_id", indexes)
        self.assertEqual(revision, 0)

    def test_crud_normalizes_and_updates_each_allowed_field(self) -> None:
        created = create_task(self.db_path, "  Estudar   HTTP ")
        self.assertEqual(created["title"], "Estudar HTTP")
        self.assertFalse(created["done"])
        self.assertRegex(created["createdAt"], r"^\d{4}-\d\d-\d\dT.*Z$")
        self.assertEqual(get_task(self.db_path, created["id"]), created)

        updated = update_task(
            self.db_path,
            created["id"],
            True,
            title_value="Entender transações",
        )
        self.assertIsNotNone(updated)
        self.assertEqual(updated["title"], "Entender transações")
        self.assertTrue(updated["done"])
        self.assertTrue(delete_task(self.db_path, created["id"]))
        self.assertEqual(list_tasks(self.db_path), [])

    def test_validation_does_not_partially_update(self) -> None:
        created = create_task(self.db_path, "Valor original")
        with self.assertRaises(ApiError) as context:
            update_task(
                self.db_path,
                created["id"],
                "sim",
                title_value="Não deve persistir",
            )
        self.assertEqual(context.exception.code, "invalid_done_type")
        self.assertEqual(get_task(self.db_path, created["id"]), created)

    def test_validation_and_missing_id(self) -> None:
        for value in (None, 3, "", " " * 3, "x" * 121, "abc\u200bdef"):
            with self.subTest(value=value), self.assertRaises(ApiError):
                normalize_title(value)
        with self.assertRaises(ApiError) as context:
            update_task(self.db_path, 1)
        self.assertEqual(context.exception.code, "empty_patch")
        self.assertIsNone(get_task(self.db_path, 999))
        self.assertIsNone(update_task(self.db_path, 999, True))
        self.assertFalse(delete_task(self.db_path, 999))

    def test_sql_metacharacters_remain_data(self) -> None:
        title = "'); DROP TABLE tasks; --"
        created = create_task(self.db_path, title)
        self.assertEqual(created["title"], title)
        self.assertEqual(len(list_tasks(self.db_path)), 1)

    def test_query_has_stable_order_filter_and_pagination(self) -> None:
        ids = [create_task(self.db_path, f"Tarefa {number}")["id"] for number in range(5)]
        update_task(self.db_path, ids[1], True)
        update_task(self.db_path, ids[3], True)

        first_page = query_tasks(self.db_path, limit=2, offset=0)
        second_page = query_tasks(self.db_path, limit=2, offset=2)
        completed = query_tasks(self.db_path, limit=10, done=True)

        self.assertEqual([task["id"] for task in first_page["tasks"]], ids[::-1][:2])
        self.assertEqual([task["id"] for task in second_page["tasks"]], ids[::-1][2:4])
        self.assertEqual(
            first_page["page"],
            {"limit": 2, "offset": 0, "total": 5, "hasMore": True, "revision": 7},
        )
        self.assertEqual({task["id"] for task in completed["tasks"]}, {ids[1], ids[3]})
        self.assertFalse(completed["page"]["hasMore"])

    def test_revision_detects_compensating_mutations_between_pages(self) -> None:
        create_task(self.db_path, "Tarefa estável")
        first_page = query_tasks(self.db_path, limit=1)
        revision = first_page["page"]["revision"]

        transient = create_task(self.db_path, "Inserção concorrente")
        self.assertTrue(delete_task(self.db_path, transient["id"]))
        self.assertEqual(query_tasks(self.db_path)["page"]["total"], 1)

        with self.assertRaises(ApiError) as context:
            query_tasks(self.db_path, limit=1, offset=1, expected_revision=revision)
        self.assertEqual(context.exception.status, 409)
        self.assertEqual(context.exception.code, "stale_page")

    def test_concurrent_writers_keep_every_committed_task(self) -> None:
        def create(number: int) -> int:
            return create_task(self.db_path, f"Concorrente {number}")["id"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            ids = list(executor.map(create, range(24)))

        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(list_tasks(self.db_path)), 24)

    def test_query_parser_is_strict(self) -> None:
        self.assertEqual(parse_list_query(""), (25, 0, None, None))
        self.assertEqual(
            parse_list_query("limit=10&offset=20&done=false&revision=7"),
            (10, 20, False, 7),
        )
        invalid = (
            "limit=0",
            "limit=101",
            "limit=-1",
            "offset=-1",
            "done=sim",
            "unknown=1",
            "limit=1&limit=2",
            "revision=-1",
            "broken",
        )
        for query in invalid:
            with self.subTest(query=query), self.assertRaises(ApiError):
                parse_list_query(query)


class HttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        db_path = Path(self.temporary.name) / "tasks.db"
        try:
            self.server = make_server("127.0.0.1", 0, db_path)
        except PermissionError as exc:
            self.temporary.cleanup()
            message = f"sockets locais indisponíveis neste ambiente: {exc}"
            if os.environ.get("RTE_REQUIRE_HTTP_TESTS") == "1":
                self.fail(message)
            self.skipTest(message)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.host = "127.0.0.1"
        self.port = self.server.server_port
        self.base_url = f"http://{self.host}:{self.port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temporary.cleanup()

    def request(
        self,
        method: str,
        path: str,
        payload: object | None = None,
        *,
        raw_body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, Any | None, dict[str, str]]:
        body = raw_body
        request_headers = dict(headers or {})
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        if body is not None and "Content-Type" not in request_headers:
            request_headers["Content-Type"] = "application/json"
        request_headers.setdefault("Accept", "application/json")
        request = urllib.request.Request(
            self.base_url + path,
            data=body,
            method=method,
            headers=request_headers,
        )
        try:
            response = urllib.request.urlopen(request, timeout=2)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            content = response.read()
            decoded = json.loads(content) if content else None
            return response.status, decoded, dict(response.headers.items())

    def raw_request(self, wire: bytes) -> tuple[int, Any | None, dict[str, str]]:
        with socket.create_connection((self.host, self.port), timeout=2) as connection:
            connection.sendall(wire)
            response = http.client.HTTPResponse(connection)
            response.begin()
            content = response.read()
            decoded = json.loads(content) if content else None
            return response.status, decoded, dict(response.headers.items())

    def assert_error(
        self,
        response: tuple[int, Any | None, dict[str, str]],
        expected_status: int,
        expected_code: str,
    ) -> dict[str, Any]:
        status, payload, headers = response
        self.assertEqual(status, expected_status)
        self.assertEqual(payload["error"]["code"], expected_code)
        self.assertTrue(payload["error"]["message"])
        self.assertEqual(payload["error"]["requestId"], headers["X-Request-ID"])
        return payload["error"]

    def create(self, title: str = "Aprender testes") -> dict[str, Any]:
        status, task, _headers = self.request("POST", "/api/tasks", {"title": title})
        self.assertEqual(status, 201)
        return task

    def test_health_readiness_and_head(self) -> None:
        status, health, headers = self.request("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(health, {"status": "ok", "service": "taskboard-api"})
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertRegex(headers["X-Request-ID"], r"^[0-9a-f]{32}$")

        status, ready, _headers = self.request("GET", "/ready")
        self.assertEqual(status, 200)
        self.assertEqual(ready["database"], "ready")

        status, body, headers = self.request("HEAD", "/api/tasks")
        self.assertEqual((status, body), (200, None))
        self.assertGreater(int(headers["Content-Length"]), 0)
        self.assertFalse(self.server.daemon_threads)
        self.assertTrue(self.server.block_on_close)

    def test_readiness_fails_when_database_or_schema_disappears(self) -> None:
        status, ready, _headers = self.request("GET", "/ready")
        self.assertEqual(status, 200)
        self.assertEqual(ready["database"], "ready")

        self.server.RequestHandlerClass.db_path.unlink()
        self.assert_error(
            self.request("GET", "/ready"),
            503,
            "database_unavailable",
        )

        initialize(self.server.RequestHandlerClass.db_path)
        with closing(sqlite3.connect(self.server.RequestHandlerClass.db_path)) as connection, connection:
            connection.execute("DROP TABLE taskboard_meta")
        self.assert_error(
            self.request("GET", "/ready"),
            503,
            "database_unavailable",
        )

    def test_http_lifecycle_and_headers(self) -> None:
        status, created, headers = self.request(
            "POST",
            "/api/tasks",
            {"title": "  Aprender   HTTP  "},
            headers={"X-Request-ID": "curso-request-001"},
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["title"], "Aprender HTTP")
        self.assertEqual(headers["Location"], f"/api/tasks/{created['id']}")
        self.assertEqual(headers["X-Request-ID"], "curso-request-001")

        task_id = created["id"]
        status, fetched, _headers = self.request("GET", f"/api/tasks/{task_id}")
        self.assertEqual((status, fetched), (200, created))

        status, updated, _headers = self.request(
            "PATCH",
            f"/api/tasks/{task_id}",
            {"title": "Praticar SQLite", "done": True},
        )
        self.assertEqual(status, 200)
        self.assertEqual(updated["title"], "Praticar SQLite")
        self.assertTrue(updated["done"])

        status, result, _headers = self.request("DELETE", f"/api/tasks/{task_id}")
        self.assertEqual((status, result), (204, None))
        self.assert_error(self.request("GET", f"/api/tasks/{task_id}"), 404, "task_not_found")

    def test_list_filter_and_pagination_contract(self) -> None:
        ids = [self.create(f"Tarefa {number}")["id"] for number in range(4)]
        self.request("PATCH", f"/api/tasks/{ids[1]}", {"done": True})
        self.request("PATCH", f"/api/tasks/{ids[3]}", {"done": True})

        status, page, _headers = self.request("GET", "/api/tasks?limit=2&offset=1")
        self.assertEqual(status, 200)
        self.assertEqual([task["id"] for task in page["tasks"]], ids[::-1][1:3])
        self.assertEqual(
            page["page"],
            {"limit": 2, "offset": 1, "total": 4, "hasMore": True, "revision": 6},
        )

        status, first_page, _headers = self.request("GET", "/api/tasks?limit=2")
        self.assertEqual(status, 200)
        revision = first_page["page"]["revision"]
        status, second_page, _headers = self.request(
            "GET", f"/api/tasks?limit=2&offset=2&revision={revision}"
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            [task["id"] for task in second_page["tasks"]],
            ids[::-1][2:4],
        )
        self.assertEqual(second_page["page"]["revision"], revision)

        status, page, _headers = self.request("GET", "/api/tasks?done=true&limit=100")
        self.assertEqual(status, 200)
        self.assertEqual({task["id"] for task in page["tasks"]}, {ids[1], ids[3]})

    def test_body_and_field_validation(self) -> None:
        cases = (
            ({}, 422, "missing_fields"),
            ({"title": "", "extra": 1}, 422, "unknown_fields"),
            ({"title": ""}, 422, "invalid_title_length"),
            ({"title": 42}, 422, "invalid_title_type"),
        )
        for payload, status, code in cases:
            with self.subTest(payload=payload):
                self.assert_error(self.request("POST", "/api/tasks", payload), status, code)

        task = self.create()
        task_path = f"/api/tasks/{task['id']}"
        patch_cases = (
            ({}, "empty_patch"),
            ({"done": "sim"}, "invalid_done_type"),
            ({"title": "x", "priority": "high"}, "unknown_fields"),
        )
        for payload, code in patch_cases:
            with self.subTest(payload=payload):
                self.assert_error(self.request("PATCH", task_path, payload), 422, code)

    def test_json_protocol_validation(self) -> None:
        cases = (
            (b"not-json", "application/json", 400, "invalid_json"),
            (b"[]", "application/json", 400, "invalid_json_shape"),
            (b'{"title":"a","title":"b"}', "application/json", 400, "duplicate_json_key"),
            (b'{"title":NaN}', "application/json", 400, "invalid_json"),
            (b'{"title":1e9999}', "application/json", 400, "invalid_json"),
            (b'{"\\ud800":1}', "application/json", 400, "invalid_json"),
            (
                b'{"title":' + b"[" * 1_100 + b"0" + b"]" * 1_100 + b"}",
                "application/json",
                400,
                "invalid_json",
            ),
            (b'{"title":"ok"}', "text/plain", 415, "unsupported_media_type"),
            (b"x" * (MAX_BODY_BYTES + 1), "application/json", 413, "payload_too_large"),
        )
        for body, content_type, status, code in cases:
            with self.subTest(code=code):
                self.assert_error(
                    self.request(
                        "POST",
                        "/api/tasks",
                        raw_body=body,
                        headers={"Content-Type": content_type},
                    ),
                    status,
                    code,
                )

    def test_empty_body_and_missing_content_length(self) -> None:
        self.assert_error(
            self.request(
                "POST",
                "/api/tasks",
                raw_body=b"",
                headers={"Content-Type": "application/json"},
            ),
            400,
            "empty_body",
        )

        connection = http.client.HTTPConnection(self.host, self.port, timeout=2)
        connection.putrequest("POST", "/api/tasks")
        connection.putheader("Content-Type", "application/json")
        connection.endheaders()
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
        self.assertEqual(response.status, 411)
        self.assertEqual(payload["error"]["code"], "content_length_required")

    def test_partial_body_timeout_closes_connection(self) -> None:
        original_timeout = server_module.REQUEST_TIMEOUT_SECONDS
        server_module.REQUEST_TIMEOUT_SECONDS = 0.1
        connection = http.client.HTTPConnection(self.host, self.port, timeout=2)
        try:
            connection.putrequest("POST", "/api/tasks")
            connection.putheader("Content-Type", "application/json")
            connection.putheader("Content-Length", "10")
            connection.endheaders(b"{}")
            response = connection.getresponse()
            payload = json.loads(response.read())
            self.assertEqual(response.status, 408)
            self.assertEqual(payload["error"]["code"], "request_timeout")
            self.assertEqual(response.headers["Connection"], "close")
        finally:
            server_module.REQUEST_TIMEOUT_SECONDS = original_timeout
            connection.close()

    def test_body_on_get_is_rejected_and_never_parsed_as_next_request(self) -> None:
        task = self.create("Não apagar por bytes residuais")
        smuggled = (
            f"DELETE /api/tasks/{task['id']} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        ).encode("ascii")

        connection = http.client.HTTPConnection(self.host, self.port, timeout=2)
        connection.request("GET", "/health", body=smuggled)
        response = connection.getresponse()
        payload = json.loads(response.read())
        self.assertEqual(response.status, 400)
        self.assertEqual(payload["error"]["code"], "body_not_allowed")
        self.assertEqual(response.headers["Connection"], "close")
        connection.close()

        status, preserved, _headers = self.request("GET", f"/api/tasks/{task['id']}")
        self.assertEqual(status, 200)
        self.assertEqual(preserved["title"], "Não apagar por bytes residuais")

    def test_body_on_unknown_route_is_not_parsed_as_a_second_request(self) -> None:
        nested_body = b'{"title":"nao deve existir"}'
        nested_request = (
            b"POST /api/tasks HTTP/1.1\r\n"
            + f"Host: {self.host}:{self.port}\r\n".encode("ascii")
            + b"Content-Type: application/json\r\n"
            + f"Content-Length: {len(nested_body)}\r\n\r\n".encode("ascii")
            + nested_body
        )
        wire = (
            b"PUT /rota-ausente HTTP/1.1\r\n"
            + f"Host: {self.host}:{self.port}\r\n".encode("ascii")
            + f"Content-Length: {len(nested_request)}\r\n\r\n".encode("ascii")
            + nested_request
        )

        response = self.raw_request(wire)
        self.assert_error(response, 404, "route_not_found")
        self.assertEqual(response[2]["Connection"], "close")
        status, page, _headers = self.request("GET", "/api/tasks")
        self.assertEqual(status, 200)
        self.assertEqual(page["page"]["total"], 0)

    def test_invalid_request_target_returns_json_and_closes_connection(self) -> None:
        wire = (
            b"GET http://[bad HTTP/1.1\r\n"
            + f"Host: {self.host}:{self.port}\r\n\r\n".encode("ascii")
        )
        response = self.raw_request(wire)
        self.assert_error(response, 400, "invalid_request_target")
        self.assertEqual(response[2]["Connection"], "close")

    def test_long_decimals_are_bounded_before_integer_conversion(self) -> None:
        many_digits = "9" * 5_000
        self.assert_error(
            self.request("GET", f"/api/tasks/{many_digits}"),
            404,
            "route_not_found",
        )
        self.assert_error(
            self.request("GET", f"/api/tasks?limit={many_digits}"),
            422,
            "invalid_query_parameter",
        )

        connection = http.client.HTTPConnection(self.host, self.port, timeout=2)
        connection.putrequest("POST", "/api/tasks")
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Content-Length", many_digits)
        connection.endheaders()
        response = connection.getresponse()
        payload = json.loads(response.read())
        self.assertEqual(response.status, 413)
        self.assertEqual(payload["error"]["code"], "payload_too_large")
        self.assertEqual(response.headers["Connection"], "close")
        connection.close()

    def test_routes_methods_options_and_query_validation(self) -> None:
        self.assert_error(self.request("GET", "/ausente"), 404, "route_not_found")
        self.assert_error(self.request("GET", "/api/tasks/0"), 404, "route_not_found")
        self.assert_error(
            self.request("OPTIONS", "/api/tasks/0"),
            404,
            "route_not_found",
        )
        self.assert_error(
            self.request("OPTIONS", "/api/tasks/9223372036854775808"),
            404,
            "route_not_found",
        )
        self.assert_error(
            self.request("GET", "/api/tasks?limit=101"),
            422,
            "invalid_query_parameter",
        )

        task = self.create("Testar query em escrita")
        self.assert_error(
            self.request("POST", "/api/tasks?debug=true", {"title": "x"}),
            400,
            "query_not_allowed",
        )
        self.assert_error(
            self.request("PATCH", f"/api/tasks/{task['id']}?debug=true", {"done": True}),
            400,
            "query_not_allowed",
        )
        self.assert_error(
            self.request("DELETE", f"/api/tasks/{task['id']}?debug=true"),
            400,
            "query_not_allowed",
        )
        self.assert_error(
            self.request("GET", f"/api/tasks/{task['id']}?debug=true"),
            400,
            "query_not_allowed",
        )
        self.assert_error(
            self.request("POST", f"/api/tasks/{task['id']}", {"title": "x"}),
            405,
            "method_not_allowed",
        )

        error = self.assert_error(
            self.request("PUT", "/api/tasks", {"title": "x"}),
            405,
            "method_not_allowed",
        )
        self.assertIn("POST", error["details"]["allowed"])

        error = self.assert_error(
            self.request("BREW", "/api/tasks"),
            405,
            "method_not_allowed",
        )
        self.assertIn("GET", error["details"]["allowed"])

        first_page = self.request("GET", "/api/tasks?limit=1")[1]
        revision = first_page["page"]["revision"]
        transient = self.create("Mudança concorrente")
        self.request("DELETE", f"/api/tasks/{transient['id']}")
        self.assert_error(
            self.request("GET", f"/api/tasks?limit=1&offset=1&revision={revision}"),
            409,
            "stale_page",
        )

        status, payload, headers = self.request("OPTIONS", "/api/tasks")
        self.assertEqual((status, payload), (204, None))
        self.assertEqual(headers["Allow"], "GET, HEAD, POST, OPTIONS")

    def test_invalid_client_request_id_is_replaced(self) -> None:
        _status, _payload, headers = self.request(
            "GET",
            "/health",
            headers={"X-Request-ID": "inválido com espaço"},
        )
        self.assertRegex(headers["X-Request-ID"], r"^[0-9a-f]{32}$")


if __name__ == "__main__":
    unittest.main()
