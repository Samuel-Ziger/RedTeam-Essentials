import unittest

from app_config import ResolvedProfile, resolve_profile


class ResolveProfileTests(unittest.TestCase):
    def test_uses_default(self) -> None:
        self.assertEqual(
            resolve_profile(None, {}),
            ResolvedProfile("development", "default"),
        )

    def test_environment_overrides_default(self) -> None:
        self.assertEqual(
            resolve_profile(None, {"APP_PROFILE": "testing"}),
            ResolvedProfile("testing", "environment"),
        )

    def test_cli_overrides_environment(self) -> None:
        self.assertEqual(
            resolve_profile("production", {"APP_PROFILE": "testing"}),
            ResolvedProfile("production", "cli"),
        )

    def test_rejects_invalid_direct_cli_value(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalido"):
            resolve_profile("other", {"APP_PROFILE": "testing"})

    def test_rejects_invalid_environment(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalido"):
            resolve_profile(None, {"APP_PROFILE": "unknown"})


if __name__ == "__main__":
    unittest.main()
