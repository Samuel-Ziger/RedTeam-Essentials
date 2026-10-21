"""Objetos imutaveis e contratos do dominio."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from .errors import ValidationError

MAX_ID_CHARS = 128
MAX_TITLE_CHARS = 512
MAX_DURATION = 1_000_000
MAX_DEPENDENCIES_PER_ITEM = 10_000
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


@dataclass(frozen=True, slots=True)
class WorkItem:
    """Tarefa com duracao positiva e pre-requisitos identificados por ID."""

    id: str
    title: str
    duration: int
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValidationError("id deve ser uma string nao vazia")
        if self.id != self.id.strip():
            raise ValidationError(f"id nao pode ter espacos externos: {self.id!r}")
        if len(self.id) > MAX_ID_CHARS:
            raise ValidationError(f"id excede o limite de {MAX_ID_CHARS} caracteres")
        if ID_PATTERN.fullmatch(self.id) is None:
            raise ValidationError(f"id deve usar somente ASCII alfanumerico, ponto, sublinhado ou hifen: {self.id!r}")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValidationError(f"titulo de {self.id!r} deve ser uma string nao vazia")
        if self.title != self.title.strip():
            raise ValidationError(f"titulo de {self.id!r} nao pode ter espacos externos")
        if len(self.title) > MAX_TITLE_CHARS:
            raise ValidationError(f"titulo de {self.id!r} excede o limite de {MAX_TITLE_CHARS} caracteres")
        if any(unicodedata.category(character) in {"Cc", "Cs"} for character in self.title):
            raise ValidationError(f"titulo de {self.id!r} contem caractere de controle invalido")
        if isinstance(self.duration, bool) or not isinstance(self.duration, int):
            raise ValidationError(f"duracao de {self.id!r} deve ser um inteiro")
        if self.duration <= 0:
            raise ValidationError(f"duracao de {self.id!r} deve ser positiva")
        if self.duration > MAX_DURATION:
            raise ValidationError(f"duracao de {self.id!r} excede o limite de {MAX_DURATION}")
        if not isinstance(self.dependencies, tuple):
            raise ValidationError(f"dependencias de {self.id!r} devem formar uma tupla")
        if len(self.dependencies) > MAX_DEPENDENCIES_PER_ITEM:
            raise ValidationError(f"{self.id!r} excede o limite de {MAX_DEPENDENCIES_PER_ITEM} dependencias")
        if any(
            not isinstance(value, str)
            or not value
            or value != value.strip()
            or len(value) > MAX_ID_CHARS
            or ID_PATTERN.fullmatch(value) is None
            for value in self.dependencies
        ):
            raise ValidationError(f"dependencia invalida em {self.id!r}")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise ValidationError(f"dependencia duplicada em {self.id!r}")
        if self.id in self.dependencies:
            raise ValidationError(f"{self.id!r} nao pode depender de si mesma")


@dataclass(frozen=True, slots=True)
class Plan:
    """Resultado completo e independente da forma de apresentacao."""

    order: tuple[str, ...]
    batches: tuple[tuple[str, ...], ...]
    critical_path: tuple[str, ...]
    minimum_duration: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "order": list(self.order),
            "batches": [list(batch) for batch in self.batches],
            "critical_path": list(self.critical_path),
            "minimum_duration": self.minimum_duration,
        }
