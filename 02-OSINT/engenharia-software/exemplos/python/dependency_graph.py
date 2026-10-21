"""Grafo de dependências com ordenação determinística e detecção de ciclo."""

from __future__ import annotations

import heapq
import re
from collections.abc import Iterable


class CycleError(ValueError):
    """Indica que um grafo dirigido não pode ser ordenado."""


class DependencyGraph:
    """Mantém arestas no sentido pré-requisito -> tarefa dependente."""

    def __init__(self) -> None:
        self._dependents: dict[str, set[str]] = {}
        self._prerequisites: dict[str, set[str]] = {}

    @staticmethod
    def _validated_node(node: str) -> str:
        if not isinstance(node, str):
            raise TypeError("o identificador deve ser uma string")
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", node) is None:
            raise ValueError("o identificador deve usar apenas ASCII seguro")
        return node

    def add_node(self, node: str) -> None:
        node = self._validated_node(node)
        self._dependents.setdefault(node, set())
        self._prerequisites.setdefault(node, set())

    def add_dependency(self, task: str, prerequisite: str) -> None:
        """Registra que ``prerequisite`` deve vir antes de ``task``."""
        # Valide os dois argumentos antes de mutar o grafo: uma falha não pode
        # deixar apenas metade da operação aplicada.
        task_id = self._validated_node(task)
        prerequisite_id = self._validated_node(prerequisite)
        self.add_node(task_id)
        self.add_node(prerequisite_id)
        self._prerequisites[task_id].add(prerequisite_id)
        self._dependents[prerequisite_id].add(task_id)

    @property
    def nodes(self) -> tuple[str, ...]:
        return tuple(sorted(self._prerequisites))

    def topological_order(self) -> list[str]:
        indegree = {node: len(prerequisites) for node, prerequisites in self._prerequisites.items()}
        ready = [node for node, degree in indegree.items() if degree == 0]
        heapq.heapify(ready)
        result: list[str] = []

        while ready:
            node = heapq.heappop(ready)
            result.append(node)
            # O heap decide a ordem global de emissao; ordenar a adjacencia
            # seria trabalho redundante e elevaria o pior caso em grafos densos.
            for dependent in self._dependents[node]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    heapq.heappush(ready, dependent)

        if len(result) != len(indegree):
            blocked = sorted(node for node, degree in indegree.items() if degree)
            raise CycleError(f"ciclo detectado entre: {', '.join(blocked)}")
        return result

    @classmethod
    def from_dependencies(cls, dependencies: dict[str, Iterable[str]]) -> DependencyGraph:
        graph = cls()
        for task, prerequisites in dependencies.items():
            graph.add_node(task)
            for prerequisite in prerequisites:
                graph.add_dependency(task, prerequisite)
        return graph


if __name__ == "__main__":
    example = DependencyGraph.from_dependencies(
        {"modelo": [], "api": ["modelo"], "testes": ["api"], "docs": ["modelo"]}
    )
    print(" -> ".join(example.topological_order()))
