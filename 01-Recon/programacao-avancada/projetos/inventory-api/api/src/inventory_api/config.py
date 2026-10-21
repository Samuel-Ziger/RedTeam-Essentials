"""Validated process configuration."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass


def _integer(name: str, default: int, minimum: int, maximum: int) -> int:
    raw = os.environ.get(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _floating(name: str, default: float, minimum: float, maximum: float) -> float:
    raw = os.environ.get(name, str(default))
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _non_empty(name: str, default: str) -> str:
    value = os.environ.get(name, default).strip()
    if not value:
        raise ValueError(f"{name} must not be empty")
    return value


DATABASE_NAME = re.compile(r"^[A-Za-z0-9_.-]{1,63}$")


@dataclass(frozen=True, slots=True)
class Settings:
    postgres_dsn: str
    mongo_uri: str
    mongo_database: str
    pool_min: int
    pool_max: int
    outbox_interval_seconds: float

    @classmethod
    def from_environment(cls) -> Settings:
        pool_min = _integer("DB_POOL_MIN", 1, 1, 50)
        pool_max = _integer("DB_POOL_MAX", 5, pool_min, 100)
        mongo_database = _non_empty("MONGO_DATABASE", "inventory")
        if DATABASE_NAME.fullmatch(mongo_database) is None:
            raise ValueError("MONGO_DATABASE must contain only letters, digits, '.', '_' or '-'")
        return cls(
            postgres_dsn=_non_empty(
                "POSTGRES_DSN",
                "postgresql://inventory@127.0.0.1:5432/inventory",
            ),
            mongo_uri=_non_empty("MONGO_URI", "mongodb://127.0.0.1:27017"),
            mongo_database=mongo_database,
            pool_min=pool_min,
            pool_max=pool_max,
            outbox_interval_seconds=_floating("OUTBOX_INTERVAL_SECONDS", 0.5, 0.05, 60),
        )
