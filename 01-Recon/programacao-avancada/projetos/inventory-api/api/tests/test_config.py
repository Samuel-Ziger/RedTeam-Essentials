from __future__ import annotations

import pytest
from inventory_api.config import Settings

ENVIRONMENT_KEYS = (
    "POSTGRES_DSN",
    "MONGO_URI",
    "MONGO_DATABASE",
    "DB_POOL_MIN",
    "DB_POOL_MAX",
    "OUTBOX_INTERVAL_SECONDS",
)


def clear_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ENVIRONMENT_KEYS:
        monkeypatch.delenv(key, raising=False)


def test_defaults_are_bounded_and_local(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_settings(monkeypatch)

    settings = Settings.from_environment()

    assert settings.postgres_dsn.startswith("postgresql://")
    assert settings.mongo_uri.startswith("mongodb://")
    assert (settings.pool_min, settings.pool_max) == (1, 5)
    assert settings.outbox_interval_seconds == 0.5


@pytest.mark.parametrize(
    ("name", "value", "message"),
    [
        ("DB_POOL_MIN", "zero", "must be an integer"),
        ("DB_POOL_MIN", "0", "must be between"),
        ("OUTBOX_INTERVAL_SECONDS", "nan", "must be between"),
        ("POSTGRES_DSN", "   ", "must not be empty"),
        ("MONGO_DATABASE", "bad database/name", "must contain only"),
    ],
)
def test_invalid_configuration_fails_fast(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    value: str,
    message: str,
) -> None:
    clear_settings(monkeypatch)
    monkeypatch.setenv(name, value)

    with pytest.raises(ValueError, match=message):
        Settings.from_environment()


def test_pool_max_cannot_be_smaller_than_pool_min(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_settings(monkeypatch)
    monkeypatch.setenv("DB_POOL_MIN", "4")
    monkeypatch.setenv("DB_POOL_MAX", "3")

    with pytest.raises(ValueError, match="DB_POOL_MAX must be between 4 and 100"):
        Settings.from_environment()
