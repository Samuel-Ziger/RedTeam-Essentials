from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import pytest
from inventory_api.errors import Problem
from inventory_api.models import ProductCreate, ProductPatch, StockAdjustmentCreate
from inventory_api.outbox import OutboxWorker
from inventory_api.service import InventoryService, decode_cursor, encode_cursor

NOW = datetime(2026, 9, 29, 18, 0, tzinfo=timezone.utc)
PRODUCT_ID = UUID("00000000-0000-4000-8000-000000000001")
EVENT_ID = UUID("00000000-0000-4000-8000-000000000002")


def product_row(identifier: UUID = PRODUCT_ID, *, version: int = 1) -> dict[str, Any]:
    return {
        "id": identifier,
        "sku": "BOOK-001",
        "name": "Banco de Dados",
        "price_cents": 4500,
        "stock": 2,
        "version": version,
        "created_at": NOW,
        "updated_at": NOW,
    }


class FakeProducts:
    def __init__(self) -> None:
        self.created: dict[str, Any] | None = None

    def ping(self) -> None:
        return None

    def create_product(self, **arguments: Any) -> tuple[dict[str, Any], bool]:
        self.created = arguments
        return product_row(arguments["product_id"]), False

    def list_products(self, **arguments: Any) -> list[dict[str, Any]]:
        assert arguments["limit"] == 1
        return [product_row(), product_row(UUID("00000000-0000-4000-8000-000000000003"))]


class FakeAudit:
    def ping(self) -> None:
        return None


def id_factory() -> UUID:
    values = getattr(id_factory, "values", iter((PRODUCT_ID, EVENT_ID)))
    id_factory.values = values
    return next(values)


def test_create_product_normalizes_and_hashes_request() -> None:
    products = FakeProducts()
    id_factory.values = iter((PRODUCT_ID, EVENT_ID))
    service = InventoryService(products, FakeAudit(), clock=lambda: NOW, new_id=id_factory)

    product, replayed = service.create_product(
        ProductCreate(sku=" book-001 ", name=" Banco   de Dados ", priceCents=4500, initialStock=2),
        "request-0001",
    )

    assert not replayed
    assert product.id == PRODUCT_ID
    assert product.sku == "BOOK-001"
    assert products.created is not None
    assert len(products.created["request_hash"]) == 64
    assert products.created["values"]["name"] == "Banco de Dados"


def test_keyset_cursor_round_trip_and_rejection() -> None:
    cursor = encode_cursor(NOW, PRODUCT_ID)
    assert decode_cursor(cursor) == (NOW, PRODUCT_ID)

    with pytest.raises(Problem) as captured:
        decode_cursor("not-a-valid-cursor")
    assert captured.value.status == 400


@pytest.mark.parametrize(
    "cursor",
    [
        "",
        "not-a-valid-cursor",
        "eyJjcmVhdGVkQXQiOiIyMDI2LTAxLTAxVDAwOjAwOjAwIiwiaWQiOiJiYWQifQ",
    ],
)
def test_cursor_rejects_malformed_or_naive_payloads(cursor: str) -> None:
    with pytest.raises(Problem) as captured:
        decode_cursor(cursor)
    assert captured.value.status == 400


def test_list_builds_next_cursor_from_extra_row() -> None:
    service = InventoryService(FakeProducts(), FakeAudit())
    page = service.list_products(limit=1, after=None, query=None)

    assert len(page.items) == 1
    assert decode_cursor(page.next_cursor) == (NOW, PRODUCT_ID)


class OutboxSource:
    def __init__(self) -> None:
        self.marked: list[UUID] = []

    def pending_events(self) -> list[dict[str, Any]]:
        return [{"id": EVENT_ID, "aggregate_id": PRODUCT_ID}]

    def mark_published(self, event_id: UUID, published_at: datetime) -> None:
        assert published_at.tzinfo is not None
        self.marked.append(event_id)


class OutboxDestination:
    def __init__(self) -> None:
        self.published: list[UUID] = []

    def publish(self, event: dict[str, Any]) -> None:
        self.published.append(event["id"])


def test_outbox_marks_only_after_publish() -> None:
    source = OutboxSource()
    destination = OutboxDestination()
    worker = OutboxWorker(source, destination, 1)

    assert worker.run_once() == 1
    assert destination.published == [EVENT_ID]
    assert source.marked == [EVENT_ID]


def test_outbox_does_not_mark_an_event_when_publish_fails() -> None:
    class FailingDestination:
        def publish(self, event: dict[str, Any]) -> None:
            raise RuntimeError("temporary dependency failure")

    source = OutboxSource()
    worker = OutboxWorker(source, FailingDestination(), 1)

    with pytest.raises(RuntimeError, match="temporary"):
        worker.run_once()
    assert source.marked == []


class UseCaseProducts(FakeProducts):
    def get_product(self, product_id: UUID) -> dict[str, Any]:
        return product_row(product_id)

    def update_product(self, **arguments: Any) -> dict[str, Any]:
        assert arguments["expected_version"] == 1
        assert arguments["name"] == "Nome novo"
        return product_row(arguments["product_id"], version=2) | {"name": "Nome novo"}

    def adjust_stock(self, **arguments: Any) -> tuple[dict[str, Any], bool]:
        return (
            {
                "id": arguments["operation_id"],
                "product_id": arguments["product_id"],
                "delta": arguments["delta"],
                "reason": arguments["reason"],
                "resulting_stock": 5,
                "resulting_version": 2,
                "created_at": arguments["now"],
            },
            False,
        )


def test_update_and_stock_use_cases_pass_version_and_normalized_commands() -> None:
    products = UseCaseProducts()
    ids = iter((EVENT_ID, EVENT_ID))
    service = InventoryService(products, FakeAudit(), clock=lambda: NOW, new_id=lambda: next(ids))

    updated = service.update_product(
        PRODUCT_ID,
        1,
        ProductPatch(name="  Nome   novo  "),
    )
    movement, replayed = service.adjust_stock(
        PRODUCT_ID,
        1,
        StockAdjustmentCreate(operationId=EVENT_ID, delta=3, reason="  entrada  "),
    )

    assert updated.name == "Nome novo"
    assert movement.reason == "entrada"
    assert not replayed
