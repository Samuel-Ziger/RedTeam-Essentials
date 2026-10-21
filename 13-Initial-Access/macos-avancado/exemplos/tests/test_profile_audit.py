from __future__ import annotations

import copy
import importlib.util
import plistlib
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("profile_audit", EXAMPLES / "ProfileAudit.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ProfileAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with (EXAMPLES / "fixtures/training.mobileconfig").open("rb") as stream:
            cls.document = plistlib.load(stream)

    def test_accepts_inert_training_profile(self) -> None:
        result = MODULE.audit(self.document)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["payloads"]), 2)

    def test_rejects_duplicate_uuid_and_missing_identifier(self) -> None:
        document = copy.deepcopy(self.document)
        document["PayloadContent"][0]["PayloadUUID"] = document["PayloadUUID"]
        del document["PayloadContent"][0]["PayloadIdentifier"]
        result = MODULE.audit(document)
        self.assertFalse(result["valid"])
        self.assertTrue(any("duplicate PayloadUUID" in error for error in result["errors"]))
        self.assertTrue(any("PayloadIdentifier" in error for error in result["errors"]))

    def test_warns_about_sensitive_key_names(self) -> None:
        document = copy.deepcopy(self.document)
        document["PayloadContent"][0]["ExamplePassword"] = "fixture-only"
        result = MODULE.audit(document)
        self.assertTrue(result["valid"])
        self.assertTrue(any("sensitive key" in warning for warning in result["warnings"]))


if __name__ == "__main__":
    unittest.main()
