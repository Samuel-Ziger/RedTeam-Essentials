"""Expected domain/application failures translated to Problem Details."""

from __future__ import annotations


class Problem(Exception):
    def __init__(self, status: int, problem_type: str, title: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.problem_type = problem_type
        self.title = title
        self.detail = detail


def not_found(resource: str = "product") -> Problem:
    return Problem(
        404,
        f"https://inventory.example.test/problems/{resource}-not-found",
        "Resource not found",
        f"{resource} was not found",
    )


def duplicate_sku() -> Problem:
    return Problem(
        409,
        "https://inventory.example.test/problems/duplicate-sku",
        "Duplicate SKU",
        "The supplied SKU is already registered",
    )


def idempotency_conflict() -> Problem:
    return Problem(
        409,
        "https://inventory.example.test/problems/idempotency-conflict",
        "Idempotency key conflict",
        "This idempotency key was already used with a different request",
    )


def precondition_failed() -> Problem:
    return Problem(
        412,
        "https://inventory.example.test/problems/version-conflict",
        "Version conflict",
        "The resource changed; fetch it again and retry with the new ETag",
    )


def insufficient_stock() -> Problem:
    return Problem(
        409,
        "https://inventory.example.test/problems/insufficient-stock",
        "Insufficient stock",
        "The adjustment would make stock negative",
    )


def invalid_cursor() -> Problem:
    return Problem(
        400,
        "https://inventory.example.test/problems/invalid-cursor",
        "Invalid cursor",
        "The pagination cursor is invalid",
    )


def dependency_unavailable() -> Problem:
    return Problem(
        503,
        "https://inventory.example.test/problems/dependency-unavailable",
        "Dependency unavailable",
        "A required data store is temporarily unavailable",
    )
