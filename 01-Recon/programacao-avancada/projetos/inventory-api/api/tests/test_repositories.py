from __future__ import annotations

from uuid import UUID

from inventory_api.repositories import _like_pattern, _same_stock_operation


def test_contains_search_escapes_sql_wildcards_without_changing_literals() -> None:
    assert _like_pattern("book") == "%book%"
    assert _like_pattern("100%_safe\\value") == "%100\\%\\_safe\\\\value%"


def test_stock_replay_must_match_body_resource_and_original_precondition() -> None:
    product_id = UUID("00000000-0000-4000-8000-000000000001")
    previous = {
        "product_id": product_id,
        "resulting_version": 4,
        "delta": 2,
        "reason": "entrada",
    }

    assert _same_stock_operation(
        previous,
        product_id=product_id,
        expected_version=3,
        delta=2,
        reason="entrada",
    )
    assert not _same_stock_operation(
        previous,
        product_id=product_id,
        expected_version=4,
        delta=2,
        reason="entrada",
    )
