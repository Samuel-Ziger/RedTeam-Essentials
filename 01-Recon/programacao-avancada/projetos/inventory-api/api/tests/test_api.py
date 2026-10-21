from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi.testclient import TestClient
from inventory_api.errors import dependency_unavailable, not_found
from inventory_api.main import create_app
from inventory_api.models import ProductPage, ProductView, StockMovementView

NOW = datetime(2026, 9, 29, 18, 0, tzinfo=timezone.utc)
PRODUCT_ID = UUID("00000000-0000-4000-8000-000000000001")
MOVEMENT_ID = UUID("00000000-0000-4000-8000-000000000010")


def product(version: int = 1) -> ProductView:
    return ProductView(
        id=PRODUCT_ID,
        sku="BOOK-001",
        name="Banco de Dados",
        priceCents=4500,
        stock=2,
        version=version,
        createdAt=NOW,
        updatedAt=NOW,
    )


class FakeService:
    def ready(self) -> None:
        return None

    def create_product(self, command: Any, key: str) -> tuple[ProductView, bool]:
        assert command.sku == "BOOK-001"
        assert key == "request-0001"
        return product(), False

    def get_product(self, product_id: UUID) -> ProductView:
        if product_id != PRODUCT_ID:
            raise not_found()
        return product()

    def list_products(self, **arguments: Any) -> ProductPage:
        assert arguments["limit"] == 20
        return ProductPage(items=[product()], nextCursor=None)

    def update_product(self, product_id: UUID, version: int, command: Any) -> ProductView:
        assert (product_id, version, command.name) == (PRODUCT_ID, 1, "Novo nome")
        changed = product(2)
        return changed.model_copy(update={"name": "Novo nome"})

    def adjust_stock(self, product_id: UUID, version: int, command: Any) -> tuple[StockMovementView, bool]:
        assert (product_id, version) == (PRODUCT_ID, 2)
        return (
            StockMovementView(
                id=MOVEMENT_ID,
                productId=PRODUCT_ID,
                delta=3,
                reason="entrada",
                resultingStock=5,
                resultingVersion=3,
                createdAt=NOW,
            ),
            False,
        )

    def list_events(self, product_id: UUID, limit: int) -> list[Any]:
        assert (product_id, limit) == (PRODUCT_ID, 20)
        return []


def test_create_get_update_and_adjust_contract() -> None:
    with TestClient(create_app(FakeService())) as client:
        created = client.post(
            "/api/v1/products",
            headers={"Idempotency-Key": "request-0001"},
            json={"sku": "book-001", "name": "Banco de Dados", "priceCents": 4500, "initialStock": 2},
        )
        assert created.status_code == 201
        assert created.headers["etag"] == '"1"'
        assert created.headers["location"].endswith(str(PRODUCT_ID))
        assert created.headers["x-request-id"]

        fetched = client.get(f"/api/v1/products/{PRODUCT_ID}")
        assert fetched.status_code == 200
        assert fetched.json()["priceCents"] == 4500

        changed = client.patch(
            f"/api/v1/products/{PRODUCT_ID}",
            headers={"If-Match": '"1"'},
            json={"name": "Novo nome"},
        )
        assert changed.status_code == 200
        assert changed.headers["etag"] == '"2"'

        movement = client.post(
            f"/api/v1/products/{PRODUCT_ID}/stock-movements",
            headers={"If-Match": '"2"'},
            json={"operationId": str(MOVEMENT_ID), "delta": 3, "reason": "entrada"},
        )
        assert movement.status_code == 201
        assert movement.headers["etag"] == '"3"'


def test_problem_details_for_validation_precondition_and_missing_resource() -> None:
    with TestClient(create_app(FakeService())) as client:
        invalid = client.post(
            "/api/v1/products",
            headers={"Idempotency-Key": "request-0001"},
            json={"sku": "x", "name": "", "priceCents": -1},
        )
        assert invalid.status_code == 422
        assert invalid.headers["content-type"].startswith("application/problem+json")
        assert invalid.json()["errors"]

        missing_header = client.patch(
            f"/api/v1/products/{PRODUCT_ID}",
            json={"name": "Novo nome"},
        )
        assert missing_header.status_code == 428
        assert missing_header.json()["type"].endswith("precondition-required")

        absent = client.get("/api/v1/products/00000000-0000-4000-8000-000000000099")
        assert absent.status_code == 404
        assert absent.json()["type"].endswith("product-not-found")


def test_openapi_exposes_versioned_contract() -> None:
    with TestClient(create_app(FakeService())) as client:
        schema = client.get("/openapi.json").json()
    assert schema["info"]["version"] == "1.0.0"
    assert "/api/v1/products" in schema["paths"]
    assert "ProblemView" in schema["components"]["schemas"]


def test_request_id_is_preserved_or_replaced_and_present_on_errors() -> None:
    with TestClient(create_app(FakeService())) as client:
        supplied = client.get(
            "/does-not-exist",
            headers={"X-Request-ID": "student-request-001"},
        )
        generated = client.get(
            "/does-not-exist",
            headers={"X-Request-ID": "contains spaces"},
        )

    assert supplied.status_code == 404
    assert supplied.headers["x-request-id"] == "student-request-001"
    assert supplied.json()["requestId"] == "student-request-001"
    assert generated.status_code == 404
    assert len(generated.headers["x-request-id"]) == 32
    assert generated.json()["requestId"] == generated.headers["x-request-id"]


def test_invalid_etag_and_json_boolean_numbers_are_rejected() -> None:
    with TestClient(create_app(FakeService())) as client:
        invalid_etag = client.patch(
            f"/api/v1/products/{PRODUCT_ID}",
            headers={"If-Match": 'W/"1"'},
            json={"name": "Novo nome"},
        )
        boolean_price = client.post(
            "/api/v1/products",
            headers={"Idempotency-Key": "request-0001"},
            json={"sku": "BOOK-001", "name": "Livro", "priceCents": True},
        )
        unsafe_idempotency_key = client.post(
            "/api/v1/products",
            headers={"Idempotency-Key": "eight spaces "},
            json={"sku": "BOOK-001", "name": "Livro", "priceCents": 100},
        )

    assert invalid_etag.status_code == 400
    assert invalid_etag.json()["type"].endswith("invalid-etag")
    assert boolean_price.status_code == 422
    assert any(error["location"].endswith("priceCents") for error in boolean_price.json()["errors"])
    assert unsafe_idempotency_key.status_code == 422


class QueryRecordingService(FakeService):
    def __init__(self) -> None:
        self.query: str | None = "not-called"

    def list_products(self, **arguments: Any) -> ProductPage:
        self.query = arguments["query"]
        return ProductPage(items=[], nextCursor=None)


def test_query_whitespace_is_normalized_before_the_use_case() -> None:
    service = QueryRecordingService()
    with TestClient(create_app(service)) as client:
        response = client.get("/api/v1/products", params={"q": "  Banco   de dados  "})

    assert response.status_code == 200
    assert service.query == "Banco de dados"


class ReplayService(FakeService):
    def create_product(self, command: Any, key: str) -> tuple[ProductView, bool]:
        return product(), True

    def adjust_stock(
        self,
        product_id: UUID,
        version: int,
        command: Any,
    ) -> tuple[StockMovementView, bool]:
        movement, _ = super().adjust_stock(product_id, version, command)
        return movement, True


def test_idempotent_replays_are_explicit_in_the_http_contract() -> None:
    with TestClient(create_app(ReplayService())) as client:
        created = client.post(
            "/api/v1/products",
            headers={"Idempotency-Key": "request-0001"},
            json={"sku": "BOOK-001", "name": "Livro", "priceCents": 100},
        )
        movement = client.post(
            f"/api/v1/products/{PRODUCT_ID}/stock-movements",
            headers={"If-Match": '"2"'},
            json={"operationId": str(MOVEMENT_ID), "delta": 3, "reason": "entrada"},
        )

    assert created.headers["idempotency-replayed"] == "true"
    assert movement.headers["idempotency-replayed"] == "true"


class UnavailableService(FakeService):
    def ready(self) -> None:
        raise dependency_unavailable()


def test_readiness_failure_is_safe_and_retryable() -> None:
    with TestClient(create_app(UnavailableService())) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.headers["retry-after"] == "1"
    assert response.json()["detail"] == "A required data store is temporarily unavailable"


class BrokenService(FakeService):
    def get_product(self, product_id: UUID) -> ProductView:
        raise RuntimeError("database password must not leak")


def test_unexpected_error_uses_a_stable_envelope_without_leaking_details() -> None:
    with TestClient(create_app(BrokenService()), raise_server_exceptions=False) as client:
        response = client.get(
            f"/api/v1/products/{PRODUCT_ID}",
            headers={"X-Request-ID": "unexpected-error-001"},
        )

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.headers["x-request-id"] == "unexpected-error-001"
    assert response.json()["requestId"] == "unexpected-error-001"
    assert "password" not in response.text
