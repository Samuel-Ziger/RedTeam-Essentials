import unittest

from dependency_planner.domain import WorkItem
from dependency_planner.service import PlanProject


class InMemoryRepository:
    def list_items(self) -> tuple[WorkItem, ...]:
        return (
            WorkItem("base", "Base", 2),
            WorkItem("api", "API", 3, ("base",)),
        )


class PlanProjectTests(unittest.TestCase):
    def test_case_use_depends_on_structural_port_not_json_adapter(self) -> None:
        plan = PlanProject(InMemoryRepository()).execute()

        self.assertEqual(plan.order, ("base", "api"))
        self.assertEqual(plan.minimum_duration, 5)


if __name__ == "__main__":
    unittest.main()
