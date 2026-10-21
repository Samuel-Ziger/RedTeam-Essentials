"""Caso de uso que orquestra porta e regras puras."""

from .domain import Plan
from .graph import build_plan
from .ports import WorkItemRepository


class PlanProject:
    def __init__(self, repository: WorkItemRepository) -> None:
        self._repository = repository

    def execute(self) -> Plan:
        return build_plan(self._repository.list_items())
