from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from datetime import date
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

EXAMPLES = Path(__file__).resolve().parents[1]
COURSE = EXAMPLES.parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inventory = load("crypto_inventory")
records = load("secure_record")


class CryptoEngineeringTests(unittest.TestCase):
    def test_inventory_prioritizes_weak_and_quantum_items(self) -> None:
        data = json.loads((COURSE / "fixtures/crypto-inventory.json").read_text(encoding="utf-8"))
        findings = inventory.audit_inventory(data, today=date(2026, 10, 1))
        priorities = {(item["asset"], item["priority"]) for item in findings}
        self.assertIn(("legacy-download-checksum", "critical"), priorities)
        self.assertIn(("long-term-archive", "high"), priorities)
        self.assertNotIn(("database-fields", "high"), priorities)

    def test_inventory_rejects_duplicates(self) -> None:
        data = json.loads((COURSE / "fixtures/crypto-inventory.json").read_text(encoding="utf-8"))
        data["assets"].append(dict(data["assets"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            inventory.validate_inventory(data)

    def test_ordered_record_round_trip(self) -> None:
        key = AESGCM.generate_key(bit_length=256)
        writer = records.RecordWriter(key, key_id="key-a", context="test")
        reader = records.RecordReader(key, key_id="key-a", context="test")
        messages = (b"one", b"two", b"three")
        sealed = [writer.seal(message) for message in messages]
        self.assertEqual(tuple(reader.open(item) for item in sealed), messages)

    def test_record_replay_is_rejected(self) -> None:
        key = AESGCM.generate_key(bit_length=256)
        writer = records.RecordWriter(key, key_id="key-a", context="test")
        reader = records.RecordReader(key, key_id="key-a", context="test")
        record = writer.seal(b"once")
        self.assertEqual(reader.open(record), b"once")
        with self.assertRaisesRegex(ValueError, "sequence"):
            reader.open(record)

    def test_out_of_order_record_is_rejected(self) -> None:
        key = AESGCM.generate_key(bit_length=256)
        writer = records.RecordWriter(key, key_id="key-a", context="test")
        reader = records.RecordReader(key, key_id="key-a", context="test")
        writer.seal(b"zero")
        second = writer.seal(b"one")
        with self.assertRaisesRegex(ValueError, "sequence"):
            reader.open(second)

    def test_tampered_record_is_rejected_without_state_advance(self) -> None:
        key = AESGCM.generate_key(bit_length=256)
        writer = records.RecordWriter(key, key_id="key-a", context="test")
        reader = records.RecordReader(key, key_id="key-a", context="test")
        original = writer.seal(b"message")
        changed = copy.deepcopy(original)
        changed["ciphertext"] = ("A" if changed["ciphertext"][0] != "A" else "B") + changed["ciphertext"][1:]
        with self.assertRaisesRegex(ValueError, "authentication"):
            reader.open(changed)
        self.assertEqual(reader.open(original), b"message")

    def test_unknown_record_field_is_rejected(self) -> None:
        key = AESGCM.generate_key(bit_length=256)
        writer = records.RecordWriter(key, key_id="key-a", context="test")
        reader = records.RecordReader(key, key_id="key-a", context="test")
        record = writer.seal(b"value")
        record["fallback"] = True
        with self.assertRaisesRegex(ValueError, "invalid record"):
            reader.open(record)


if __name__ == "__main__":
    unittest.main()
