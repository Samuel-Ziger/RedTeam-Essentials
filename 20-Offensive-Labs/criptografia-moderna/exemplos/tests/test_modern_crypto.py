from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

EXAMPLES = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


envelope = load("secure_envelope")
exchange = load("key_exchange")
signatures = load("signatures")


class ModernCryptoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = AESGCM.generate_key(bit_length=256)
        self.record = envelope.encrypt(
            self.key, b"synthetic", key_id="lab-key-a", context="tenant=lab;type=test"
        )

    def test_envelope_round_trip(self) -> None:
        self.assertEqual(envelope.decrypt(self.key, self.record), b"synthetic")

    def test_envelope_uses_fresh_nonce(self) -> None:
        other = envelope.encrypt(self.key, b"synthetic", key_id="lab-key-a", context="tenant=lab;type=test")
        self.assertNotEqual(self.record["nonce"], other["nonce"])

    def test_envelope_rejects_tampering(self) -> None:
        for field in ("kid", "ctx", "nonce", "ciphertext"):
            changed = copy.deepcopy(self.record)
            if field in {"kid", "ctx"}:
                changed[field] += "-changed"
            else:
                changed[field] = ("A" if changed[field][0] != "A" else "B") + changed[field][1:]
            with self.subTest(field=field), self.assertRaises(ValueError):
                envelope.decrypt(self.key, changed)

    def test_envelope_rejects_unknown_fields(self) -> None:
        changed = dict(self.record)
        changed["fallback"] = "ECB"
        with self.assertRaisesRegex(ValueError, "invalid envelope"):
            envelope.decrypt(self.key, changed)

    def test_x25519_agreement_and_context(self) -> None:
        alice = X25519PrivateKey.generate()
        bob = X25519PrivateKey.generate()
        first = exchange.derive_key(alice, exchange.public_bytes(bob), context=b"v1")
        second = exchange.derive_key(bob, exchange.public_bytes(alice), context=b"v1")
        different = exchange.derive_key(alice, exchange.public_bytes(bob), context=b"v2")
        self.assertEqual(first, second)
        self.assertNotEqual(first, different)

    def test_signature_rejects_changes(self) -> None:
        private = Ed25519PrivateKey.generate()
        message = b"artifact"
        signature = signatures.sign(private, message)
        public = private.public_key()
        self.assertTrue(signatures.verify(public, message, signature))
        self.assertFalse(signatures.verify(public, message + b"!", signature))
        self.assertFalse(signatures.verify(public, message, bytes(64)))


if __name__ == "__main__":
    unittest.main()
