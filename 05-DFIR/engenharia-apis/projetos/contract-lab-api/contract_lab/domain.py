"""Framework-independent domain objects and value normalization."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal

from .errors import bad_request

Status = Literal["active", "archived"]
Role = Literal["reader", "writer"]


@dataclass(frozen=True, slots=True)
class Principal:
    actor_id: str
    tenant_id: str
    role: Role


@dataclass(frozen=True, slots=True)
class Item:
    item_id: str
    tenant_id: str
    title: str
    status: Status
    version: int
    sequence: int
    created_at: datetime
    updated_at: datetime

    @property
    def etag(self) -> str:
        return f'"{self.item_id}-v{self.version}"'


@dataclass(frozen=True, slots=True)
class Event:
    event_id: str
    event_type: str
    tenant_id: str
    actor_id: str
    item_id: str
    occurred_at: datetime


def now_utc() -> datetime:
    return datetime.now(UTC)


def normalize_title(value: str) -> str:
    title = " ".join(value.split())
    if not 3 <= len(title) <= 80:
        raise bad_request("invalid-title", "title deve possuir entre 3 e 80 caracteres.")
    return title
