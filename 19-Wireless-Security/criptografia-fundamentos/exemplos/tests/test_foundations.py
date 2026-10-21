from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


number_theory = load("number_theory")
hash_mac = load("hash_mac")
password_kdf = load("password_kdf")


class FoundationsTests(unittest.TestCase):
    def test_gcd_and_extended_identity(self) -> None:
        self.assertEqual(number_theory.gcd(252, 105), 21)
        divisor, x, y = number_theory.extended_gcd(252, 105)
        self.assertEqual(252 * x + 105 * y, divisor)

    def test_inverse(self) -> None:
        self.assertEqual(number_theory.modular_inverse(7, 26), 15)
        with self.assertRaises(ValueError):
            number_theory.modular_inverse(6, 26)

    def test_modular_power(self) -> None:
        self.assertEqual(number_theory.modular_power(7, 128, 13), pow(7, 128, 13))

    def test_digest_and_hmac_detect_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            key = root / "key"
            message = root / "message"
            key.write_bytes(b"k" * 32)
            message.write_bytes(b"before")
            digest = hash_mac.digest_file(message)
            tag = hash_mac.tag_file(key, message)
            self.assertTrue(hash_mac.verify_file(key, message, tag))
            message.write_bytes(b"after")
            self.assertNotEqual(hash_mac.digest_file(message), digest)
            self.assertFalse(hash_mac.verify_file(key, message, tag))

    def test_hmac_rejects_malformed_tag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            key = root / "key"
            message = root / "message"
            key.write_bytes(b"k" * 32)
            message.write_bytes(b"message")
            self.assertFalse(hash_mac.verify_file(key, message, "not-hex"))

    def test_scrypt_record(self) -> None:
        record = password_kdf.create_record("correct horse", salt=b"s" * 16)
        self.assertTrue(password_kdf.verify_record("correct horse", record))
        self.assertFalse(password_kdf.verify_record("wrong", record))

    def test_scrypt_records_use_individual_salts(self) -> None:
        first = password_kdf.create_record("same password")
        second = password_kdf.create_record("same password")
        self.assertNotEqual(first, second)

    def test_scrypt_rejects_unbounded_record(self) -> None:
        record = password_kdf.create_record("value", salt=b"s" * 16)
        self.assertFalse(password_kdf.verify_record("value", record.replace("n=16384", "n=8")))


if __name__ == "__main__":
    unittest.main()
