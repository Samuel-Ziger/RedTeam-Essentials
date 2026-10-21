"""Application use cases independent from HTTP and database drivers."""

from __future__ import annotations

import base64
import hashlib
import json
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from .errors import invalid_cursor
from .models import (
    AuditEventView,
    ProductCreate,
    ProductPage,
    ProductPatch,
    ProductView,
    StockAdjustmentCreate,
    StockMovementView,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _request_hash(command: ProductCreate) -> str:
    canonical = json.dumps(command.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def encode_cursor(created_at: datetime, product_id: UUID) -> str:
    payload = json.dumps(
        {"createdAt": created_at.isoformat(), "id": str(product_id)},
        separators=(",", ":"),
    ).encode()
    return base64.urlsafe_b64encode(payload).decode().rstrip("=")


def decode_cursor(cursor: str) -> tuple[datetime, UUID]:
    try:
        padding = "=" * (-len(cursor) % 4)
        value = json.loads(base64.b64decode(cursor + padding, altchars=b"-_", validate=True))
        created_at = datetime.fromisoformat(value["createdAt"])
        product_id = UUID(value["id"])
        if created_at.tzinfo is None:
            raise ValueError("cursor datetime must include timezone")
        return created_at, product_id
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise invalid_cursor() from exc


class InventoryService:
    def __init__(
        self,
        products: Any,
        audit: Any,
        *,
        clock: Callable[[], datetime] = _utc_now,
        new_id: Callable[[], UUID] = uuid4,
    ) -> None:
        self.products = products
        self.audit = audit
        self.clock = clock
        self.new_id = new_id

    def ready(self) -> None:
        self.products.ping()
        self.audit.ping()

    def create_product(self, command: ProductCreate, idempotency_key: str) -> tuple[ProductView, bool]:
        row, replayed = self.products.create_product(
            product_id=self.new_id(),
            event_id=self.new_id(),
            values=command.model_dump(),
            idempotency_key=idempotency_key,
            request_hash=_request_hash(command),
            now=self.clock(),
        )
        return ProductView.model_validate(row), replayed

    def get_product(self, product_id: UUID) -> ProductView:
        return ProductView.model_validate(self.products.get_product(product_id))

    def list_products(self, *, limit: int, after: str | None, query: str | None) -> ProductPage:
        decoded = decode_cursor(after) if after else None
        rows = self.products.list_products(limit=limit, after=decoded, query=query)
        has_next = len(rows) > limit
        page_rows = rows[:limit]
        items = [ProductView.model_validate(row) for row in page_rows]
        next_cursor = None
        if has_next and items:
            last = items[-1]
            next_cursor = encode_cursor(last.created_at, last.id)
        return ProductPage(items=items, next_cursor=next_cursor)

    def update_product(
        self,
        product_id: UUID,
        expected_version: int,
        command: ProductPatch,
    ) -> ProductView:
        row = self.products.update_product(
            product_id=product_id,
            expected_version=expected_version,
            name=command.name,
            price_cents=command.price_cents,
            event_id=self.new_id(),
            now=self.clock(),
        )
        return ProductView.model_validate(row)

    def adjust_stock(
        self,
        product_id: UUID,
        expected_version: int,
        command: StockAdjustmentCreate,
    ) -> tuple[StockMovementView, bool]:
        row, replayed = self.products.adjust_stock(
            product_id=product_id,
            expected_version=expected_version,
            operation_id=command.operation_id,
            delta=command.delta,
            reason=command.reason,
            event_id=self.new_id(),
            now=self.clock(),
        )
        return StockMovementView.model_validate(row), replayed

    def list_events(self, product_id: UUID, limit: int) -> list[AuditEventView]:
        self.products.get_product(product_id)
        return [AuditEventView.model_validate(event) for event in self.audit.list_events(product_id, limit)]
