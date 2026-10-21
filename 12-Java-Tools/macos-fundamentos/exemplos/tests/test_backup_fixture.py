from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("backup_fixture", EXAMPLES / "Backup-RteFixture.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BackupFixtureTests(unittest.TestCase):
    def test_dry_run_does_not_create_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "backup"
            source.mkdir()
            (source / "fixture.txt").write_text("safe", encoding="utf-8")
            result = MODULE.backup(source, destination, dry_run=True)
            self.assertTrue(result["dryRun"])
            self.assertFalse(destination.exists())

    def test_backup_is_verifiable_and_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "backup"
            source.mkdir()
            (source / "nested").mkdir()
            (source / "nested/fixture.txt").write_text("safe\n", encoding="utf-8")
            MODULE.backup(source, destination)
            self.assertTrue(MODULE.verify(destination)["valid"])
            with self.assertRaises(FileExistsError):
                MODULE.backup(source, destination)

    def test_destination_inside_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            source.mkdir()
            with self.assertRaises(ValueError):
                MODULE.backup(source, source / "backup")


if __name__ == "__main__":
    unittest.main()
