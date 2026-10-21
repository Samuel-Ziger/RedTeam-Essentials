import unittest

from dependency_planner.domain import MAX_DURATION, MAX_ID_CHARS, MAX_TITLE_CHARS, WorkItem
from dependency_planner.errors import ValidationError


class WorkItemTests(unittest.TestCase):
    def test_creates_valid_item(self) -> None:
        item = WorkItem("api", "Construir API", 3, ("model",))

        self.assertEqual(item.duration, 3)
        self.assertEqual(item.dependencies, ("model",))

    def test_rejects_boolean_duration(self) -> None:
        with self.assertRaisesRegex(ValidationError, "inteiro"):
            WorkItem("api", "Construir API", True)

    def test_rejects_self_dependency(self) -> None:
        with self.assertRaisesRegex(ValidationError, "si mesma"):
            WorkItem("api", "Construir API", 1, ("api",))

    def test_rejects_duplicate_dependency(self) -> None:
        with self.assertRaisesRegex(ValidationError, "duplicada"):
            WorkItem("api", "Construir API", 1, ("model", "model"))

    def test_rejects_values_above_explicit_limits(self) -> None:
        cases = (
            ("x" * (MAX_ID_CHARS + 1), "Titulo", 1, ()),
            ("id", "x" * (MAX_TITLE_CHARS + 1), 1, ()),
            ("id", "Titulo", MAX_DURATION + 1, ()),
        )

        for values in cases:
            with self.subTest(values=(len(values[0]), len(values[1]), values[2])):
                with self.assertRaisesRegex(ValidationError, "limite"):
                    WorkItem(*values)

    def test_rejects_ambiguous_external_whitespace(self) -> None:
        with self.assertRaisesRegex(ValidationError, "espacos externos"):
            WorkItem("api", " Titulo", 1)
        with self.assertRaisesRegex(ValidationError, "dependencia invalida"):
            WorkItem("api", "Titulo", 1, (" model",))

    def test_rejects_identifier_that_can_corrupt_text_output(self) -> None:
        for item_id in ("linha\nnova", "barra/caminho", "espaço-interno"):
            with self.subTest(item_id=item_id):
                with self.assertRaisesRegex(ValidationError, "ASCII"):
                    WorkItem(item_id, "Titulo", 1)

    def test_rejects_control_and_surrogate_in_title(self) -> None:
        for title in ("linha\nnova", "surrogate-\ud800"):
            with self.subTest(title=repr(title)):
                with self.assertRaisesRegex(ValidationError, "controle"):
                    WorkItem("id", title, 1)


if __name__ == "__main__":
    unittest.main()
