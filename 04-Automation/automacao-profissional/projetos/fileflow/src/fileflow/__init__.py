"""FileFlow: automacao local segura e auditavel."""

from .domain import Operation, Plan
from .executor import execute
from .planner import build_plan

__all__ = ["Operation", "Plan", "build_plan", "execute"]
