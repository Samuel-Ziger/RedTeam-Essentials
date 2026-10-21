"""PostgreSQL source-of-truth and MongoDB audit projection adapters."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from psycopg import errors as pg_errors
from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool
from pymongo import ASCENDING, DESCENDING, MongoClient

from .errors import duplicate_sku, idempotency_conflict, insufficient_stock, not_found, precondition_failed

Product = dict[str, Any]
Event = dict[str, Any]


def _like_pattern(value: str) -> str:
    """Build a literal contains pattern for PostgreSQL LIKE/ILIKE."""
    escaped = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def _same_stock_operation(
    previous: dict[str, Any],
    *,
    product_id: UUID,
    expected_version: int,
    delta: int,
    reason: str,
) -> bool:
    """Decide whether a repeated operation is the exact original request."""
    return (
        previous["product_id"] == product_id
        and previous["resulting_version"] - 1 == expected_version
        and previous["delta"] == delta
        and previous["reason"] == reason
    )


def _json_product(row: Product) -> Product:
    return {
        "id": str(row["id"]),
        "sku": row["sku"],
        "name": row["name"],
        "price_cents": row["price_cents"],
        "stock": row["stock"],
        "version": row["version"],
        "created_at": row["created_at"].isoformat(),
        "updated_at": row["updated_at"].isoformat(),
    }


class PostgresRepository:
    def __init__(self, pool: ConnectionPool[Any]) -> None:
        self.pool = pool

    def ping(self) -> None:
        with self.pool.connection() as connection:
            connection.execute("SELECT 1").fetchone()

    def create_product(
        self,
        *,
        product_id: UUID,
        event_id: UUID,
        values: dict[str, Any],
        idempotency_key: str,
        request_hash: str,
        now: datetime,
    ) -> tuple[Product, bool]:
        scope = "create-product"
        try:
            with self.pool.connection() as connection, connection.transaction():
                inserted = connection.execute(
                    """
                    INSERT INTO idempotency_record (scope, key, request_hash)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    RETURNING key
                    """,
                    (scope, idempotency_key, request_hash),
                ).fetchone()
                if inserted is None:
                    previous = connection.execute(
                        """
                        SELECT request_hash, response_body
                        FROM idempotency_record
                        WHERE scope = %s AND key = %s
                        FOR UPDATE
                        """,
                        (scope, idempotency_key),
                    ).fetchone()
                    if previous["request_hash"] != request_hash or previous["response_body"] is None:
                        raise idempotency_conflict()
                    return previous["response_body"], True

                row = connection.execute(
                    """
                    INSERT INTO product (
                        id, sku, name, price_cents, stock, version, created_at, updated_at
                    )
                    VALUES (%s, %s, %s, %s, %s, 1, %s, %s)
                    RETURNING *
                    """,
                    (
                        product_id,
                        values["sku"],
                        values["name"],
                        values["price_cents"],
                        values["initial_stock"],
                        now,
                        now,
                    ),
                ).fetchone()
                product = _json_product(row)
                self._add_outbox(
                    connection,
                    event_id=event_id,
                    aggregate_id=product_id,
                    event_type="product.created",
                    payload=product,
                    occurred_at=now,
                )
                connection.execute(
                    """
                    UPDATE idempotency_record
                    SET response_body = %s
                    WHERE scope = %s AND key = %s
                    """,
                    (Jsonb(product), scope, idempotency_key),
                )
                return product, False
        except pg_errors.UniqueViolation as exc:
            if exc.diag.constraint_name == "product_sku_unique":
                raise duplicate_sku() from exc
            raise

    def get_product(self, product_id: UUID) -> Product:
        with self.pool.connection() as connection:
            row = connection.execute("SELECT * FROM product WHERE id = %s", (product_id,)).fetchone()
        if row is None:
            raise not_found()
        return row

    def list_products(
        self,
        *,
        limit: int,
        after: tuple[datetime, UUID] | None,
        query: str | None,
    ) -> list[Product]:
        clauses: list[str] = []
        parameters: list[Any] = []
        if after is not None:
            clauses.append("(created_at, id) < (%s, %s)")
            parameters.extend(after)
        if query:
            clauses.append("(sku ILIKE %s ESCAPE '\\' OR name ILIKE %s ESCAPE '\\')")
            pattern = _like_pattern(query)
            parameters.extend((pattern, pattern))
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        parameters.append(limit + 1)
        sql = f"""
            SELECT * FROM product
            {where}
            ORDER BY created_at DESC, id DESC
            LIMIT %s
        """
        with self.pool.connection() as connection:
            return list(connection.execute(sql, parameters).fetchall())

    def update_product(
        self,
        *,
        product_id: UUID,
        expected_version: int,
        name: str | None,
        price_cents: int | None,
        event_id: UUID,
        now: datetime,
    ) -> Product:
        with self.pool.connection() as connection, connection.transaction():
            row = connection.execute(
                """
                UPDATE product
                SET name = coalesce(%s, name),
                    price_cents = coalesce(%s, price_cents),
                    version = version + 1,
                    updated_at = %s
                WHERE id = %s AND version = %s
                RETURNING *
                """,
                (name, price_cents, now, product_id, expected_version),
            ).fetchone()
            if row is None:
                self._raise_missing_or_stale(connection, product_id, expected_version)
            product = _json_product(row)
            self._add_outbox(
                connection,
                event_id=event_id,
                aggregate_id=product_id,
                event_type="product.updated",
                payload=product,
                occurred_at=now,
            )
            return product

    def adjust_stock(
        self,
        *,
        product_id: UUID,
        expected_version: int,
        operation_id: UUID,
        delta: int,
        reason: str,
        event_id: UUID,
        now: datetime,
    ) -> tuple[dict[str, Any], bool]:
        with self.pool.connection() as connection, connection.transaction():
            connection.execute(
                "SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))",
                (str(operation_id),),
            )
            previous = connection.execute(
                "SELECT * FROM stock_movement WHERE id = %s",
                (operation_id,),
            ).fetchone()
            if previous is not None:
                if not _same_stock_operation(
                    previous,
                    product_id=product_id,
                    expected_version=expected_version,
                    delta=delta,
                    reason=reason,
                ):
                    raise idempotency_conflict()
                return previous, True

            product = connection.execute(
                """
                UPDATE product
                SET stock = stock + %s,
                    version = version + 1,
                    updated_at = %s
                WHERE id = %s
                  AND version = %s
                  AND stock + %s >= 0
                RETURNING *
                """,
                (delta, now, product_id, expected_version, delta),
            ).fetchone()
            if product is None:
                current = connection.execute(
                    "SELECT version, stock FROM product WHERE id = %s",
                    (product_id,),
                ).fetchone()
                if current is None:
                    raise not_found()
                if current["version"] != expected_version:
                    raise precondition_failed()
                raise insufficient_stock()

            movement = connection.execute(
                """
                INSERT INTO stock_movement (
                    id, product_id, delta, reason, resulting_stock,
                    resulting_version, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    operation_id,
                    product_id,
                    delta,
                    reason,
                    product["stock"],
                    product["version"],
                    now,
                ),
            ).fetchone()
            self._add_outbox(
                connection,
                event_id=event_id,
                aggregate_id=product_id,
                event_type="stock.adjusted",
                payload={
                    "operationId": str(operation_id),
                    "delta": delta,
                    "reason": reason,
                    "newStock": product["stock"],
                    "productVersion": product["version"],
                },
                occurred_at=now,
            )
            return movement, False

    def pending_events(self, limit: int = 50) -> list[Event]:
        with self.pool.connection() as connection:
            return list(
                connection.execute(
                    """
                    SELECT id, aggregate_id, event_type, payload, occurred_at
                    FROM outbox_event
                    WHERE published_at IS NULL
                    ORDER BY occurred_at, id
                    LIMIT %s
                    """,
                    (limit,),
                ).fetchall()
            )

    def mark_published(self, event_id: UUID, published_at: datetime) -> None:
        with self.pool.connection() as connection, connection.transaction():
            connection.execute(
                """
                UPDATE outbox_event
                SET published_at = %s
                WHERE id = %s AND published_at IS NULL
                """,
                (published_at, event_id),
            )

    @staticmethod
    def _raise_missing_or_stale(connection: Any, product_id: UUID, expected_version: int) -> None:
        current = connection.execute("SELECT version FROM product WHERE id = %s", (product_id,)).fetchone()
        if current is None:
            raise not_found()
        if current["version"] != expected_version:
            raise precondition_failed()
        raise RuntimeError("update failed without a changed precondition")

    @staticmethod
    def _add_outbox(
        connection: Any,
        *,
        event_id: UUID,
        aggregate_id: UUID,
        event_type: str,
        payload: dict[str, Any],
        occurred_at: datetime,
    ) -> None:
        connection.execute(
            """
            INSERT INTO outbox_event (id, aggregate_id, event_type, payload, occurred_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (event_id, aggregate_id, event_type, Jsonb(payload), occurred_at),
        )


class MongoAuditRepository:
    def __init__(self, client: MongoClient[Any], database_name: str) -> None:
        self.client = client
        self.collection = client[database_name]["audit_events"]

    def ping(self) -> None:
        self.client.admin.command("ping")

    def ensure_indexes(self) -> None:
        self.collection.create_index([("eventId", ASCENDING)], unique=True)
        self.collection.create_index([("aggregateId", ASCENDING), ("occurredAt", DESCENDING), ("eventId", DESCENDING)])

    def publish(self, event: Event) -> None:
        document = {
            "eventId": str(event["id"]),
            "aggregateId": str(event["aggregate_id"]),
            "type": event["event_type"],
            "occurredAt": event["occurred_at"],
            "payload": event["payload"],
        }
        self.collection.update_one(
            {"eventId": document["eventId"]},
            {"$setOnInsert": document},
            upsert=True,
        )

    def list_events(self, aggregate_id: UUID, limit: int) -> list[Event]:
        cursor = (
            self.collection.find(
                {"aggregateId": str(aggregate_id)},
                {"_id": 0},
            )
            .sort([("occurredAt", DESCENDING), ("eventId", DESCENDING)])
            .limit(limit)
        )
        return list(cursor)
