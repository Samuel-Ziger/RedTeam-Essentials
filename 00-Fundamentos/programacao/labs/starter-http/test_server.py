from __future__ import annotations

import http.client
import json
import socket
import threading
import unittest
import urllib.error
import urllib.request

from server import make_server


class StarterServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = make_server("127.0.0.1", 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address[:2]
        self.base_url = f"http://{host}:{port}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.assertFalse(self.thread.is_alive(), "thread HTTP não encerrou")

    def test_health_explica_status_headers_e_json(self) -> None:
        with self.opener.open(f"{self.base_url}/health", timeout=2) as response:
            body = response.read()
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "application/json")
            self.assertEqual(int(response.headers["Content-Length"]), len(body))
            self.assertEqual(json.loads(body), {"status": "ok"})

    def test_rota_desconhecida_possui_erro_estavel(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as context:
            self.opener.open(f"{self.base_url}/desconhecida", timeout=2)
        with context.exception as error:
            self.assertEqual(error.code, 404)
            self.assertEqual(json.loads(error.read())["error"]["code"], "route_not_found")

    def test_servidor_recusa_bind_fora_do_loopback(self) -> None:
        with self.assertRaisesRegex(ValueError, "loopback"):
            make_server("0.0.0.0", 0)

    def test_get_com_corpo_fecha_sem_interpretar_segunda_requisicao(self) -> None:
        host, port = self.server.server_address[:2]
        nested = b"GET /health HTTP/1.1\r\nHost: local\r\n\r\n"
        wire = (
            b"GET /health HTTP/1.1\r\n"
            + f"Host: {host}:{port}\r\n".encode("ascii")
            + f"Content-Length: {len(nested)}\r\n\r\n".encode("ascii")
            + nested
        )
        with socket.create_connection((host, port), timeout=2) as connection:
            connection.sendall(wire)
            response = http.client.HTTPResponse(connection)
            response.begin()
            payload = json.loads(response.read())
        self.assertEqual(response.status, 400)
        self.assertEqual(response.headers["Connection"], "close")
        self.assertEqual(payload["error"]["code"], "body_not_allowed")

    def test_alvo_invalido_retorna_json_sem_traceback(self) -> None:
        host, port = self.server.server_address[:2]
        wire = (
            b"GET http://[bad HTTP/1.1\r\n"
            + f"Host: {host}:{port}\r\n\r\n".encode("ascii")
        )
        with socket.create_connection((host, port), timeout=2) as connection:
            connection.sendall(wire)
            response = http.client.HTTPResponse(connection)
            response.begin()
            payload = json.loads(response.read())
        self.assertEqual(response.status, 400)
        self.assertEqual(response.headers["Connection"], "close")
        self.assertEqual(payload["error"]["code"], "invalid_request_target")


if __name__ == "__main__":
    unittest.main()
