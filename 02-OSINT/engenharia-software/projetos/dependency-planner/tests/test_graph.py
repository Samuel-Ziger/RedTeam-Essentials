import unittest

from dependency_planner.domain import WorkItem
from dependency_planner.errors import CycleError, ValidationError
from dependency_planner.graph import build_plan


def item(item_id: str, duration: int = 1, dependencies: tuple[str, ...] = ()) -> WorkItem:
    return WorkItem(item_id, f"Tarefa {item_id}", duration, dependencies)


class BuildPlanTests(unittest.TestCase):
    def test_builds_deterministic_order_batches_and_critical_path(self) -> None:
        plan = build_plan(
            [
                item("release", 1, ("tests", "docs")),
                item("docs", 2, ("model",)),
                item("tests", 3, ("api",)),
                item("api", 5, ("model",)),
                item("model", 3, ("discovery",)),
                item("discovery", 2),
            ]
        )

        self.assertEqual(
            plan.batches,
            (("discovery",), ("model",), ("api", "docs"), ("tests",), ("release",)),
        )
        self.assertEqual(
            plan.critical_path,
            ("discovery", "model", "api", "tests", "release"),
        )
        self.assertEqual(plan.minimum_duration, 14)
        positions = {value: index for index, value in enumerate(plan.order)}
        self.assertLess(positions["model"], positions["api"])
        self.assertLess(positions["tests"], positions["release"])

    def test_empty_project_is_valid(self) -> None:
        plan = build_plan([])

        self.assertEqual(plan.order, ())
        self.assertEqual(plan.minimum_duration, 0)

    def test_critical_path_tie_uses_smallest_identifier(self) -> None:
        plan = build_plan(
            [
                item("root", 1),
                item("alpha", 2, ("root",)),
                item("beta", 2, ("root",)),
                item("release", 1, ("beta", "alpha")),
            ]
        )

        self.assertEqual(plan.critical_path, ("root", "alpha", "release"))
        self.assertEqual(plan.minimum_duration, 4)

    def test_rejects_unknown_dependency(self) -> None:
        with self.assertRaisesRegex(ValidationError, "desconhecidas: missing"):
            build_plan([item("api", dependencies=("missing",))])

    def test_rejects_duplicate_identifier(self) -> None:
        with self.assertRaisesRegex(ValidationError, "id duplicado"):
            build_plan([item("A"), item("A")])

    def test_reports_closed_cycle_path(self) -> None:
        with self.assertRaises(CycleError) as context:
            build_plan(
                [
                    item("A", dependencies=("C",)),
                    item("B", dependencies=("A",)),
                    item("C", dependencies=("B",)),
                ]
            )

        path = context.exception.path
        self.assertEqual(path[0], path[-1])
        self.assertEqual(set(path[:-1]), {"A", "B", "C"})
        items_by_id = {
            "A": item("A", dependencies=("C",)),
            "B": item("B", dependencies=("A",)),
            "C": item("C", dependencies=("B",)),
        }
        for prerequisite, dependent in zip(path, path[1:]):
            self.assertIn(prerequisite, items_by_id[dependent].dependencies)

    def test_large_cycle_does_not_depend_on_python_recursion_limit(self) -> None:
        size = 2_000
        items = [
            item(
                f"N{index:04d}",
                dependencies=(f"N{(index - 1) % size:04d}",),
            )
            for index in range(size)
        ]

        with self.assertRaises(CycleError) as context:
            build_plan(items)

        self.assertEqual(context.exception.path[0], context.exception.path[-1])
        self.assertEqual(len(context.exception.path), size + 1)


if __name__ == "__main__":
    unittest.main()
