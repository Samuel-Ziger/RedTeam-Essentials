import itertools
import unittest

from dependency_planner.domain import WorkItem
from dependency_planner.graph import build_plan


class SmallDagPropertyTests(unittest.TestCase):
    """Enumera todos os DAGs compatíveis com uma ordem de quatro vértices."""

    def test_every_generated_dag_preserves_edges_and_is_deterministic(self) -> None:
        node_ids = ("A", "B", "C", "D")
        possible_edges = tuple(itertools.combinations(node_ids, 2))

        for mask in range(1 << len(possible_edges)):
            dependencies = {node_id: [] for node_id in node_ids}
            selected_edges: list[tuple[str, str]] = []
            for bit, (prerequisite, dependent) in enumerate(possible_edges):
                if mask & (1 << bit):
                    dependencies[dependent].append(prerequisite)
                    selected_edges.append((prerequisite, dependent))

            items = [WorkItem(node_id, f"Tarefa {node_id}", 1, tuple(dependencies[node_id])) for node_id in node_ids]
            plan = build_plan(items)
            reversed_plan = build_plan(reversed(items))
            positions = {node_id: index for index, node_id in enumerate(plan.order)}

            with self.subTest(mask=mask):
                self.assertEqual(plan.order, reversed_plan.order)
                self.assertEqual(set(plan.order), set(node_ids))
                self.assertEqual(len(plan.order), len(set(plan.order)))
                self.assertTrue(all(positions[left] < positions[right] for left, right in selected_edges))
                self.assertEqual(plan.minimum_duration, len(plan.critical_path))


if __name__ == "__main__":
    unittest.main()
