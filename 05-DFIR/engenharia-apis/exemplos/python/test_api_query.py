import unittest

from api_query import build_query


class QueryTests(unittest.TestCase):
    def test_builds_canonical_query(self) -> None:
        self.assertEqual(
            build_query(20, "abc_123", "active"),
            "GET /v1/items?limit=20&after=abc_123&status=active",
        )

    def test_rejects_invalid_values(self) -> None:
        for values in (
            (0, None, None),
            (1, "bad=token", None),
            (1, "a" * 513, None),
            (1, None, "all"),
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                build_query(*values)


if __name__ == "__main__":
    unittest.main()
