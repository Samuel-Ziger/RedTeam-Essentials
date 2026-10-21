import unittest

from dependency_graph import CycleError, DependencyGraph


class DependencyGraphTests(unittest.TestCase):
    def test_orders_prerequisites_before_dependents(self) -> None:
        graph = DependencyGraph.from_dependencies(
            {"release": ["tests", "docs"], "tests": ["build"], "docs": [], "build": []}
        )
        order = graph.topological_order()

        self.assertLess(order.index("build"), order.index("tests"))
        self.assertLess(order.index("tests"), order.index("release"))
        self.assertLess(order.index("docs"), order.index("release"))
        self.assertEqual(order, graph.topological_order())

    def test_reports_cycle(self) -> None:
        graph = DependencyGraph.from_dependencies({"A": ["B"], "B": ["A"]})

        with self.assertRaisesRegex(CycleError, "A, B"):
            graph.topological_order()

    def test_rejects_empty_identifier(self) -> None:
        with self.assertRaises(ValueError):
            DependencyGraph().add_node("   ")

    def test_rejects_external_whitespace_without_partial_mutation(self) -> None:
        graph = DependencyGraph()

        with self.assertRaisesRegex(ValueError, "ASCII seguro"):
            graph.add_dependency("api", " modelo")

        self.assertEqual(graph.nodes, ())

    def test_rejects_unicode_to_keep_order_portable(self) -> None:
        with self.assertRaisesRegex(ValueError, "ASCII seguro"):
            DependencyGraph().add_node("tarefa-á")


if __name__ == "__main__":
    unittest.main()
