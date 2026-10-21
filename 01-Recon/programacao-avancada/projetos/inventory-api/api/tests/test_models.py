from __future__ import annotations

from uuid import UUID

import pytest
from inventory_api.models import ProductCreate, ProductPatch, StockAdjustmentCreate, parse_etag
from pydantic import ValidationError


def test_create_normalizes_text_and_forbids_unknown_fields() -> None:
    command = ProductCreate(
        sku=" book-001 ",
        name="  Banco   de   Dados  ",
        priceCents=4500,
        initialStock=2,
    )

    assert command.sku == "BOOK-001"
    assert command.name == "Banco de Dados"
    assert command.model_dump() == {
        "sku": "BOOK-001",
        "name": "Banco de Dados",
        "price_cents": 4500,
        "initial_stock": 2,
    }

    with pytest.raises(ValidationError):
        ProductCreate(
            sku="BOOK-001",
            name="Livro",
            priceCents=100,
            admin=True,
        )


@pytest.mark.parametrize("value", [True, False, 1.5, "100"])
def test_money_rejects_non_integer_json_values(value: object) -> None:
    with pytest.raises(ValidationError):
        ProductCreate(sku="BOOK-001", name="Livro", priceCents=value)


def test_patch_requires_a_real_change() -> None:
    with pytest.raises(ValidationError, match="at least one field"):
        ProductPatch()
    with pytest.raises(ValidationError, match="at least one field"):
        ProductPatch(name=None, priceCents=None)

    with pytest.raises(ValidationError, match="NUL"):
        ProductPatch(name="nome\x00oculto")


def test_stock_command_rejects_zero_and_normalizes_reason() -> None:
    operation_id = UUID("00000000-0000-4000-8000-000000000010")
    command = StockAdjustmentCreate(
        operationId=operation_id,
        delta=3,
        reason="  entrada   conferida ",
    )
    assert command.reason == "entrada conferida"

    with pytest.raises(ValidationError, match="delta cannot be zero"):
        StockAdjustmentCreate(operationId=operation_id, delta=0, reason="teste")


@pytest.mark.parametrize(
    "value",
    [None, "1", 'W/"1"', '"0"', '"01"', '"1", "2"', "*"],
)
def test_only_one_strong_positive_numeric_etag_is_accepted(value: str | None) -> None:
    with pytest.raises(ValueError):
        parse_etag(value)


def test_valid_etag_is_decoded() -> None:
    assert parse_etag('"42"') == 42
