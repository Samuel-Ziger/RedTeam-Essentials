"""Thread-safe in-memory repository used only by the local laboratory."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from threading import RLock
from uuid import uuid4

from .domain import Event, Item, Principal, Status, now_utc
from .errors import conflict, not_found, precondition


class InMemoryStore:
    def __init__(
        self,
        *,
        clock: Callable[[], datetime] = now_utc,
        item_id_factory: Callable[[], str] | None = None,
        event_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._lock = RLock()
        self._clock = clock
        self._item_id_factory = item_id_factory or (lambda: f"itm_{uuid4().hex}")
        self._event_id_factory = event_id_factory or (lambda: f"evt_{uuid4().hex}")
        self._items: dict[str, Item] = {}
        self._idempotency: dict[tuple[str, str, str], tuple[str, str]] = {}
        self._events: list[Event] = []
        self._sequence = 0

    def create(self, principal: Principal, title: str, key: str, fingerprint: str) -> tuple[Item, bool]:
        scope = (principal.tenant_id, principal.actor_id, key)
        with self._lock:
            recorded = self._idempotency.get(scope)
            if recorded is not None:
                previous_fingerprint, item_id = recorded
                if previous_fingerprint != fingerprint:
                    raise conflict("idempotency-conflict", "A chave já foi usada com outro comando.")
                return self._items[item_id], False

            self._sequence += 1
            current = self._clock()
            item = Item(
                item_id=self._item_id_factory(),
                tenant_id=principal.tenant_id,
                title=title,
                status="active",
                version=1,
                sequence=self._sequence,
                created_at=current,
                updated_at=current,
            )
            self._items[item.item_id] = item
            self._idempotency[scope] = (fingerprint, item.item_id)
            self._append_event("item.created", principal, item)
            return item, True

    def get(self, principal: Principal, item_id: str) -> Item:
        with self._lock:
            item = self._items.get(item_id)
            if item is None or item.tenant_id != principal.tenant_id:
                raise not_found()
            return item

    def list_items(self, principal: Principal, after_sequence: int, limit: int, status: Status | None) -> list[Item]:
        with self._lock:
            matches = [
                item
                for item in self._items.values()
                if item.tenant_id == principal.tenant_id
                and item.sequence > after_sequence
                and (status is None or item.status == status)
            ]
            return sorted(matches, key=lambda item: item.sequence)[:limit]

    def update(
        self,
        principal: Principal,
        item_id: str,
        expected_etag: str,
        *,
        title: str | None,
        status: Status | None,
    ) -> Item:
        with self._lock:
            current = self.get(principal, item_id)
            if current.etag != expected_etag:
                raise precondition("If-Match não corresponde à versão atual.")
            if current.status == "archived" and status == "active":
                raise conflict(
                    "invalid-transition",
                    "Um item arquivado não pode voltar ao estado active.",
                )
            updated = replace(
                current,
                title=title if title is not None else current.title,
                status=status if status is not None else current.status,
                version=current.version + 1,
                updated_at=self._clock(),
            )
            self._items[item_id] = updated
            self._append_event("item.updated", principal, updated)
            return updated

    def events(self, principal: Principal, *, limit: int = 50) -> list[Event]:
        with self._lock:
            return [event for event in self._events if event.tenant_id == principal.tenant_id][:limit]

    def _append_event(self, event_type: str, principal: Principal, item: Item) -> None:
        self._events.append(
            Event(
                event_id=self._event_id_factory(),
                event_type=event_type,
                tenant_id=principal.tenant_id,
                actor_id=principal.actor_id,
                item_id=item.item_id,
                occurred_at=self._clock(),
            )
        )
