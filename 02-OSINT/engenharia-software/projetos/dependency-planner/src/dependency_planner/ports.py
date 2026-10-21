"""Contratos de fronteira consumidos pelos casos de uso."""

from __future__ import annotations

from typing import Protocol

from .domain import WorkItem


class WorkItemRepository(Protocol):
    """Porta de leitura independente do mecanismo de persistencia."""

    def list_items(self) -> tuple[WorkItem, ...]:
        """Retorna uma fotografia imutavel das tarefas."""
        ...
