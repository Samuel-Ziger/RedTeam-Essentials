import json
import tempfile
import unittest
from pathlib import Path

from fileflow.domain import FileFlowError
from fileflow.executor import execute
from fileflow.planner import build_plan


class FileFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.source = root / "source"
        self.target = root / "target"
        self.source.mkdir()
        (self.source / "a.txt").write_text("alpha", encoding="utf-8")
        (self.source / "ignored.bin").write_bytes(b"ignored")

    def test_plan_is_deterministic_and_filters_extensions(self) -> None:
        (self.source / "z.log").write_text("last", encoding="utf-8")
        plan = build_plan(self.source, self.target, [".txt", ".log"])

        self.assertEqual([Path(item.source).name for item in plan.operations], ["a.txt", "z.log"])
        self.assertEqual({item.action for item in plan.operations}, {"copy"})

    def test_dry_plan_does_not_create_target(self) -> None:
        build_plan(self.source, self.target, [".txt"])

        self.assertFalse(self.target.exists())

    def test_execute_copies_and_second_plan_skips(self) -> None:
        plan = build_plan(self.source, self.target, [".txt"])
        copied = execute(plan)
        second = build_plan(self.source, self.target, [".txt"])

        self.assertEqual(copied, 1)
        self.assertEqual((self.target / "a.txt").read_text(encoding="utf-8"), "alpha")
        self.assertEqual(second.operations[0].action, "skip")

    def test_conflict_aborts_before_copy(self) -> None:
        self.target.mkdir()
        (self.target / "a.txt").write_text("different", encoding="utf-8")
        (self.source / "b.txt").write_text("beta", encoding="utf-8")
        plan = build_plan(self.source, self.target, [".txt"])

        with self.assertRaisesRegex(FileFlowError, "nada foi copiado"):
            execute(plan)
        self.assertFalse((self.target / "b.txt").exists())

    def test_target_created_after_plan_is_never_overwritten(self) -> None:
        plan = build_plan(self.source, self.target, [".txt"])
        self.target.mkdir()
        (self.target / "a.txt").write_text("created concurrently", encoding="utf-8")

        with self.assertRaisesRegex(FileFlowError, "depois do planejamento"):
            execute(plan)
        self.assertEqual(
            (self.target / "a.txt").read_text(encoding="utf-8"),
            "created concurrently",
        )

    def test_rejects_nested_roots(self) -> None:
        with self.assertRaisesRegex(FileFlowError, "aninhados"):
            build_plan(self.source, self.source / "output", [".txt"])

    def test_rejects_symlink(self) -> None:
        try:
            (self.source / "link.txt").symlink_to(self.source / "a.txt")
        except OSError:
            self.skipTest("symlink indisponivel")

        with self.assertRaisesRegex(FileFlowError, "simbolico"):
            build_plan(self.source, self.target, [".txt"])

    def test_writes_jsonl_audit(self) -> None:
        audit = Path(self.temporary.name) / "audit.jsonl"
        plan = build_plan(self.source, self.target, [".txt"])
        execute(plan, audit, "run-test")
        event = json.loads(audit.read_text(encoding="utf-8"))

        self.assertEqual(event["outcome"], "copied")
        self.assertEqual(event["event"], "file_processed")
        self.assertEqual(event["runId"], "run-test")
        self.assertEqual(event["planDigest"], plan.digest)
        self.assertEqual(event["relativePath"], "a.txt")
        self.assertNotIn(str(self.source), audit.read_text(encoding="utf-8"))

    def test_manifest_is_deterministic_and_does_not_expose_roots(self) -> None:
        first = build_plan(self.source, self.target, [".txt"])
        second = build_plan(self.source, self.target, [".txt"])

        self.assertEqual(first.digest, second.digest)
        document = json.dumps(first.as_dict(), sort_keys=True)
        self.assertNotIn(str(self.source), document)
        self.assertNotIn(str(self.target), document)
        self.assertEqual(len(first.as_dict()["planDigest"]), 64)

    def test_rejects_file_and_byte_limits(self) -> None:
        (self.source / "b.txt").write_text("beta", encoding="utf-8")
        with self.assertRaisesRegex(FileFlowError, "1 arquivos"):
            build_plan(self.source, self.target, [".txt"], max_files=1)
        with self.assertRaisesRegex(FileFlowError, "4 bytes"):
            build_plan(self.source, self.target, [".txt"], max_total_bytes=4)

    def test_rejects_unsafe_extension(self) -> None:
        for extension in ("txt", ".", "../txt", ".txt/other", ".toolongextension99"):
            with self.subTest(extension=extension), self.assertRaises(FileFlowError):
                build_plan(self.source, self.target, [extension])

    def test_source_changed_after_plan_aborts_before_copy(self) -> None:
        (self.source / "b.txt").write_text("beta", encoding="utf-8")
        plan = build_plan(self.source, self.target, [".txt"])
        (self.source / "a.txt").write_text("changed", encoding="utf-8")

        with self.assertRaisesRegex(FileFlowError, "fonte mudou"):
            execute(plan)
        self.assertFalse(self.target.exists())

    def test_skip_source_changed_after_plan_is_not_silently_accepted(self) -> None:
        execute(build_plan(self.source, self.target, [".txt"]))
        skip_plan = build_plan(self.source, self.target, [".txt"])
        (self.source / "a.txt").write_text("changed", encoding="utf-8")

        with self.assertRaisesRegex(FileFlowError, "fonte mudou"):
            execute(skip_plan)

    def test_skip_target_changed_after_plan_is_not_silently_accepted(self) -> None:
        execute(build_plan(self.source, self.target, [".txt"]))
        skip_plan = build_plan(self.source, self.target, [".txt"])
        (self.target / "a.txt").write_text("changed", encoding="utf-8")

        with self.assertRaisesRegex(FileFlowError, "destino mudou"):
            execute(skip_plan)

    def test_rejects_unsafe_run_id_before_effect(self) -> None:
        plan = build_plan(self.source, self.target, [".txt"])

        with self.assertRaisesRegex(FileFlowError, "run_id"):
            execute(plan, run_id="../../unsafe")
        self.assertFalse(self.target.exists())

    def test_audit_failure_reports_confirmed_effect(self) -> None:
        audit_directory = Path(self.temporary.name) / "audit-as-directory"
        audit_directory.mkdir()

        with self.assertRaisesRegex(FileFlowError, "efeito confirmado"):
            execute(build_plan(self.source, self.target, [".txt"]), audit_directory)
        self.assertEqual((self.target / "a.txt").read_text(encoding="utf-8"), "alpha")


if __name__ == "__main__":
    unittest.main()
