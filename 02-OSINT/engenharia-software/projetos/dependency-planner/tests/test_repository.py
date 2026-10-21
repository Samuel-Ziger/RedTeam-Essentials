import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from dependency_planner.errors import ValidationError
from dependency_planner.repository import JsonWorkItemRepository


class JsonWorkItemRepositoryTests(unittest.TestCase):
    def _write(self, document: object) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "project.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def test_reads_strict_document(self) -> None:
        path = self._write(
            {
                "items": [
                    {
                        "id": "A",
                        "title": "Tarefa A",
                        "duration": 2,
                        "dependencies": [],
                    }
                ]
            }
        )

        items = JsonWorkItemRepository(path).list_items()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, "A")

    def test_rejects_unknown_field(self) -> None:
        path = self._write(
            {
                "items": [
                    {
                        "id": "A",
                        "title": "Tarefa A",
                        "duration": 2,
                        "dependencies": [],
                        "ignored": True,
                    }
                ]
            }
        )

        with self.assertRaisesRegex(ValidationError, "desconhecidos"):
            JsonWorkItemRepository(path).list_items()

    def test_rejects_non_list_dependencies(self) -> None:
        path = self._write(
            {
                "items": [
                    {
                        "id": "A",
                        "title": "Tarefa A",
                        "duration": 2,
                        "dependencies": "B",
                    }
                ]
            }
        )

        with self.assertRaisesRegex(ValidationError, "deve ser uma lista"):
            JsonWorkItemRepository(path).list_items()

    def test_rejects_non_utf8_document(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "project.json"
        path.write_bytes(b'{"items": []}\xff')

        with self.assertRaisesRegex(ValidationError, "UTF-8"):
            JsonWorkItemRepository(path).list_items()

    def test_rejects_document_before_unbounded_read(self) -> None:
        path = self._write({"items": []})

        with mock.patch("dependency_planner.repository.MAX_DOCUMENT_BYTES", 4):
            with self.assertRaisesRegex(ValidationError, "bytes"):
                JsonWorkItemRepository(path).list_items()

    def test_rejects_item_count_above_policy(self) -> None:
        path = self._write({"items": [self._item("A"), self._item("B")]})

        with mock.patch("dependency_planner.repository.MAX_ITEMS", 1):
            with self.assertRaisesRegex(ValidationError, "elementos"):
                JsonWorkItemRepository(path).list_items()

    def test_rejects_duplicate_json_key_and_non_standard_number(self) -> None:
        duplicate = self._write_raw('{"items":[{"id":"A","id":"B","title":"T","duration":1,"dependencies":[]}]}')
        not_a_number = self._write_raw('{"items":[{"id":"A","title":"T","duration":NaN,"dependencies":[]}]}')

        with self.assertRaisesRegex(ValidationError, "duplicado"):
            JsonWorkItemRepository(duplicate).list_items()
        with self.assertRaisesRegex(ValidationError, "nao padrao"):
            JsonWorkItemRepository(not_a_number).list_items()

    def test_rejects_excessive_json_nesting_as_validation_error(self) -> None:
        path = self._write_raw("[" * 100_000 + "0" + "]" * 100_000)

        with self.assertRaisesRegex(ValidationError, "aninhamento"):
            JsonWorkItemRepository(path).list_items()

    def test_rejects_huge_integer_as_validation_error(self) -> None:
        path = self._write_raw('{"items":[{"id":"A","title":"T","duration":' + "1" * 5_000 + ',"dependencies":[]}]}')

        with self.assertRaisesRegex(ValidationError, "fora dos limites"):
            JsonWorkItemRepository(path).list_items()

    @staticmethod
    def _item(item_id: str) -> dict[str, object]:
        return {
            "id": item_id,
            "title": f"Tarefa {item_id}",
            "duration": 1,
            "dependencies": [],
        }

    def _write_raw(self, content: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "project.json"
        path.write_text(content, encoding="utf-8")
        return path


if __name__ == "__main__":
    unittest.main()
