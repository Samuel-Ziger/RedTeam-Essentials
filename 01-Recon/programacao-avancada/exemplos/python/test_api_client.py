from __future__ import annotations

import importlib.util
import sys
import threading
import unittest
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

CLIENT_PATH = Path(__file__).with_name("api_client.py")
SPEC = importlib.util.spec_from_file_location("module01_api_client", CLIENT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("não foi possível carregar api_client.py")
CLIENT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CLIENT
SPEC.loader.exec_module(CLIENT)

MOCK_PATH = Path(__file__).parents[1] / "mock_api.py"
MOCK_SPEC = importlib.util.spec_from_file_location("module01_mock_api", MOCK_PATH)
if MOCK_SPEC is None or MOCK_SPEC.loader is None:
    raise RuntimeError("não foi possível carregar mock_api.py")
MOCK = importlib.util.module_from_spec(MOCK_SPEC)
sys.modules[MOCK_SPEC.name] = MOCK
MOCK_SPEC.loader.exec_module(MOCK)


@contextmanager
def mock_api() -> Iterator[str]:
    server = MOCK.ThreadingHTTPServer(("127.0.0.1", 0), MOCK.ContractHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


class ApiClientTests(unittest.TestCase):
    def test_success_and_request_id(self) -> None:
        with mock_api() as base_url:
            response = CLIENT.get_json(base_url, "/health/live")

        self.assertEqual(response.status, 200)
        self.assertEqual(response.request_id, "mock-request-001")
        self.assertEqual(response.body, {"status": "ok"})

    def test_problem_details_preserves_status_and_body(self) -> None:
        with mock_api() as base_url:
            with self.assertRaises(CLIENT.ApiProblem) as captured:
                CLIENT.get_json(base_url, "/problem")

        self.assertEqual(captured.exception.status, 409)
        self.assertEqual(captured.exception.body["detail"], "conflito de teste")

    def test_invalid_json_and_non_object_are_rejected(self) -> None:
        with mock_api() as base_url:
            with self.assertRaisesRegex(RuntimeError, "JSON"):
                CLIENT.get_json(base_url, "/invalid-json")
            with self.assertRaisesRegex(RuntimeError, "objeto JSON"):
                CLIENT.get_json(base_url, "/array")

    def test_declared_oversized_response_is_rejected_before_reading(self) -> None:
        with mock_api() as base_url:
            with self.assertRaisesRegex(RuntimeError, "limite de 1 MB"):
                CLIENT.get_json(base_url, "/too-large")

    def test_redirect_is_not_followed_silently(self) -> None:
        with mock_api() as base_url:
            with self.assertRaises(CLIENT.ApiProblem) as captured:
                CLIENT.get_json(base_url, "/redirect")
        self.assertEqual(captured.exception.status, 302)

    def test_product_contract_rejects_boolean_stock(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "incompatível"):
            CLIENT._product_summary({"sku": "BOOK-001", "name": "Livro", "stock": True})


if __name__ == "__main__":
    unittest.main()
