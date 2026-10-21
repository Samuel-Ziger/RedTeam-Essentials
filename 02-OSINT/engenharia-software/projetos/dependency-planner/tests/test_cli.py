import contextlib
import io
import json
import unittest
from pathlib import Path

from dependency_planner.cli import main

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_json_output_is_machine_readable(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main(
                [
                    str(PROJECT_ROOT / "fixtures" / "valid-project.json"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(payload["minimum_duration"], 14)
        self.assertEqual(payload["critical_path"][-1], "release")

    def test_cycle_returns_expected_exit_code_and_stderr(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main([str(PROJECT_ROOT / "fixtures" / "cyclic-project.json")])

        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("ciclo de dependencias", stderr.getvalue())

    def test_missing_file_returns_expected_exit_code(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = main([str(PROJECT_ROOT / "fixtures" / "missing.json")])

        self.assertEqual(code, 2)
        self.assertIn("erro:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
