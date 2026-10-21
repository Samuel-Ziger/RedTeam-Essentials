"""HTTP input and output schemas."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _camel(name: str) -> str:
    head, *tail = name.split("_")
    return head + "".join(part.capitalize() for part in tail)


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=_camel, populate_by_name=True, extra="forbid")


def _normalized(value: str) -> str:
    normalized = " ".join(value.split())
    if "\x00" in normalized:
        raise ValueError("text must not contain a NUL character")
    return normalized


class ProductCreate(ApiModel):
    sku: str = Field(min_length=3, max_length=32, pattern=r"^[A-Z0-9][A-Z0-9._-]+$")
    name: str = Field(min_length=1, max_length=120)
    price_cents: int = Field(strict=True, ge=0, le=1_000_000_000)
    initial_stock: int = Field(default=0, strict=True, ge=0, le=10_000_000)

    @field_validator("sku", mode="before")
    @classmethod
    def normalize_sku(cls, value: Any) -> Any:
        return value.strip().upper() if isinstance(value, str) else value

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: Any) -> Any:
        return _normalized(value) if isinstance(value, str) else value


class ProductPatch(ApiModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    price_cents: int | None = Field(default=None, strict=True, ge=0, le=1_000_000_000)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: Any) -> Any:
        return _normalized(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_change(self) -> ProductPatch:
        if self.name is None and self.price_cents is None:
            raise ValueError("at least one field must be supplied")
        return self


class StockAdjustmentCreate(ApiModel):
    operation_id: UUID
    delta: int = Field(strict=True, ge=-1_000_000, le=1_000_000)
    reason: str = Field(min_length=1, max_length=120)

    @field_validator("delta")
    @classmethod
    def delta_cannot_be_zero(cls, value: int) -> int:
        if value == 0:
            raise ValueError("delta cannot be zero")
        return value

    @field_validator("reason", mode="before")
    @classmethod
    def normalize_reason(cls, value: Any) -> Any:
        return _normalized(value) if isinstance(value, str) else value


class ProductView(ApiModel):
    id: UUID
    sku: str
    name: str
    price_cents: int
    stock: int
    version: int
    created_at: datetime
    updated_at: datetime


class ProductPage(ApiModel):
    items: list[ProductView]
    next_cursor: str | None


class StockMovementView(ApiModel):
    id: UUID
    product_id: UUID
    delta: int
    reason: str
    resulting_stock: int
    resulting_version: int
    created_at: datetime


class AuditEventView(ApiModel):
    event_id: str
    aggregate_id: str
    type: str
    occurred_at: datetime
    payload: dict[str, Any]


class HealthView(ApiModel):
    status: str


class ProblemView(ApiModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str
    request_id: str
    errors: list[dict[str, Any]] | None = None


ETAG_PATTERN = re.compile(r'^"([1-9][0-9]*)"$')


def parse_etag(value: str | None) -> int:
    if value is None:
        raise ValueError("If-Match header is required")
    match = ETAG_PATTERN.fullmatch(value)
    if match is None:
        raise ValueError('If-Match must contain a strong numeric ETag such as "3"')
    return int(match.group(1))
