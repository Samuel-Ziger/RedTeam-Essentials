"""Porta de leitura e adaptador de documento JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .domain import WorkItem
from .errors import ValidationError
from .ports import WorkItemRepository

MAX_DOCUMENT_BYTES = 32 * 1024 * 1024
MAX_ITEMS = 100_000


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"campo JSON duplicado: {key!r}")
        result[key] = value
    return result


def _reject_non_standard_number(value: str) -> None:
    raise ValidationError(f"numero JSON nao padrao: {value}")


class JsonWorkItemRepository(WorkItemRepository):
    """Lê um documento local e rejeita estruturas ambíguas."""

    _ROOT_FIELDS = frozenset({"items"})
    _ITEM_FIELDS = frozenset({"id", "title", "duration", "dependencies"})

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def list_items(self) -> tuple[WorkItem, ...]:
        try:
            with self._path.open("rb") as stream:
                raw = stream.read(MAX_DOCUMENT_BYTES + 1)
            if len(raw) > MAX_DOCUMENT_BYTES:
                raise ValidationError(f"documento excede o limite de {MAX_DOCUMENT_BYTES} bytes: {self._path}")
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ValidationError(f"documento nao e UTF-8 valido em {self._path}:{error.start}") from error
            document: Any = json.loads(
                text,
                object_pairs_hook=_strict_object,
                parse_constant=_reject_non_standard_number,
            )
        except json.JSONDecodeError as error:
            raise ValidationError(f"JSON invalido em {self._path}:{error.lineno}:{error.colno}") from error
        except ValueError as error:
            raise ValidationError(f"valor JSON fora dos limites em {self._path}") from error
        except RecursionError as error:
            raise ValidationError(f"JSON excede o limite seguro de aninhamento em {self._path}") from error

        if not isinstance(document, dict):
            raise ValidationError("a raiz do documento deve ser um objeto")
        unknown_root = set(document) - self._ROOT_FIELDS
        if unknown_root:
            raise ValidationError(f"campos desconhecidos na raiz: {', '.join(sorted(unknown_root))}")
        if set(document) != self._ROOT_FIELDS:
            raise ValidationError("a raiz deve conter exatamente o campo 'items'")
        if not isinstance(document["items"], list):
            raise ValidationError("'items' deve ser uma lista")
        if len(document["items"]) > MAX_ITEMS:
            raise ValidationError(f"'items' excede o limite de {MAX_ITEMS} elementos")

        return tuple(self._parse_item(value, index) for index, value in enumerate(document["items"]))

    def _parse_item(self, value: Any, index: int) -> WorkItem:
        if not isinstance(value, dict):
            raise ValidationError(f"items[{index}] deve ser um objeto")
        fields = set(value)
        missing = self._ITEM_FIELDS - fields
        unknown = fields - self._ITEM_FIELDS
        if missing:
            raise ValidationError(f"campos ausentes em items[{index}]: {', '.join(sorted(missing))}")
        if unknown:
            raise ValidationError(f"campos desconhecidos em items[{index}]: {', '.join(sorted(unknown))}")
        dependencies = value["dependencies"]
        if not isinstance(dependencies, list):
            raise ValidationError(f"dependencies em items[{index}] deve ser uma lista")
        return WorkItem(
            id=value["id"],
            title=value["title"],
            duration=value["duration"],
            dependencies=tuple(dependencies),
        )
