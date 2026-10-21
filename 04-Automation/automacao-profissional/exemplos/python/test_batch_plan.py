import unittest

from batch_plan import plan


class PlanTests(unittest.TestCase):
    def test_deduplicates_and_sorts(self) -> None:
        self.assertEqual(plan("build,test,build,deploy"), ["build", "deploy", "test"])

    def test_rejects_empty_or_unsafe_id(self) -> None:
        for value in ("", "a,,b", "../x", "a b"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                plan(value)

    def test_rejects_more_than_64_items(self) -> None:
        with self.assertRaisesRegex(ValueError, "64"):
            plan(",".join(f"id{i}" for i in range(65)))

    def test_rejects_more_than_1023_bytes(self) -> None:
        with self.assertRaisesRegex(ValueError, "1023"):
            plan("a" * 1024)


if __name__ == "__main__":
    unittest.main()
