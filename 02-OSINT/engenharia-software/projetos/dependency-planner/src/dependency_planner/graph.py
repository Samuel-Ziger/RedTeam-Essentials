"""Algoritmos puros sobre o grafo de tarefas."""

from __future__ import annotations

import heapq
from collections.abc import Iterable, Iterator, Mapping

from .domain import Plan, WorkItem
from .errors import CycleError, ValidationError


def _index_items(items: Iterable[WorkItem]) -> dict[str, WorkItem]:
    indexed: dict[str, WorkItem] = {}
    for item in items:
        if item.id in indexed:
            raise ValidationError(f"id duplicado: {item.id!r}")
        indexed[item.id] = item

    for item in indexed.values():
        unknown = sorted(set(item.dependencies) - indexed.keys())
        if unknown:
            raise ValidationError(f"{item.id!r} referencia dependencias desconhecidas: {', '.join(unknown)}")
    return indexed


def _dependents(items: Mapping[str, WorkItem]) -> dict[str, set[str]]:
    result = {item_id: set() for item_id in items}
    for item in items.values():
        for dependency in item.dependencies:
            result[dependency].add(item.id)
    return result


def _cycle_path(items: Mapping[str, WorkItem], dependents: Mapping[str, set[str]]) -> tuple[str, ...]:
    """Encontra um ciclo no sentido prerequisito -> dependente, sem recursao."""
    state: dict[str, int] = {item_id: 0 for item_id in items}
    path: list[str] = []
    positions: dict[str, int] = {}

    for start in sorted(items):
        if state[start] != 0:
            continue

        state[start] = 1
        positions[start] = len(path)
        path.append(start)
        stack: list[tuple[str, Iterator[str]]] = [(start, iter(sorted(dependents[start])))]

        while stack:
            current, dependencies = stack[-1]
            try:
                dependency = next(dependencies)
            except StopIteration:
                stack.pop()
                path.pop()
                positions.pop(current)
                state[current] = 2
                continue

            if state[dependency] == 0:
                state[dependency] = 1
                positions[dependency] = len(path)
                path.append(dependency)
                stack.append((dependency, iter(sorted(dependents[dependency]))))
            elif state[dependency] == 1:
                cycle_start = positions[dependency]
                return tuple(path[cycle_start:] + [dependency])
    return ()


def _topological_order(items: Mapping[str, WorkItem], dependents: Mapping[str, set[str]]) -> tuple[str, ...]:
    indegree = {item_id: len(item.dependencies) for item_id, item in items.items()}
    ready = [item_id for item_id, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    result: list[str] = []

    while ready:
        item_id = heapq.heappop(ready)
        result.append(item_id)
        for dependent in dependents[item_id]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, dependent)

    if len(result) != len(items):
        raise CycleError(_cycle_path(items, dependents))
    return tuple(result)


def _parallel_batches(items: Mapping[str, WorkItem], dependents: Mapping[str, set[str]]) -> tuple[tuple[str, ...], ...]:
    indegree = {item_id: len(item.dependencies) for item_id, item in items.items()}
    current = sorted(item_id for item_id, degree in indegree.items() if degree == 0)
    batches: list[tuple[str, ...]] = []
    produced = 0

    while current:
        batches.append(tuple(current))
        produced += len(current)
        following: list[str] = []
        for item_id in current:
            for dependent in dependents[item_id]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    following.append(dependent)
        current = sorted(following)

    if produced != len(items):
        raise CycleError(_cycle_path(items, dependents))
    return tuple(batches)


def _critical_path(items: Mapping[str, WorkItem], order: tuple[str, ...]) -> tuple[tuple[str, ...], int]:
    if not order:
        return (), 0
    finish: dict[str, int] = {}
    predecessor: dict[str, str | None] = {}

    for item_id in order:
        item = items[item_id]
        if item.dependencies:
            # Maior termino acumulado; no empate, menor ID. Evitar ``sorted``
            # aqui mantem a etapa de programacao dinamica linear em E.
            previous = min(item.dependencies, key=lambda value: (-finish[value], value))
            finish[item_id] = finish[previous] + item.duration
            predecessor[item_id] = previous
        else:
            finish[item_id] = item.duration
            predecessor[item_id] = None

    end = min(order, key=lambda value: (-finish[value], value))
    reverse_path: list[str] = []
    current: str | None = end
    while current is not None:
        reverse_path.append(current)
        current = predecessor[current]
    return tuple(reversed(reverse_path)), finish[end]


def build_plan(source: Iterable[WorkItem]) -> Plan:
    """Valida ``source`` e calcula todas as visoes do plano."""
    items = _index_items(source)
    dependents = _dependents(items)
    order = _topological_order(items, dependents)
    batches = _parallel_batches(items, dependents)
    critical_path, minimum_duration = _critical_path(items, order)
    return Plan(order, batches, critical_path, minimum_duration)
