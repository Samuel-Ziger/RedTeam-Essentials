#!/usr/bin/env python3
"""A bounded, ordered AES-GCM record stream for protocol review exercises."""

from __future__ import annotations

import base64
import json
import os
import re
import secrets
from typing import Any

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VERSION = 1
ALGORITHM = "A256GCM"
MAX_PLAINTEXT = 64 * 1024
FIELDS = {"v", "alg", "kid", "stream", "seq", "ctx", "nonce", "ciphertext"}
IDENTIFIER = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


def _validate_identity(value: Any) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError("invalid record")
    return value


def _validate_context(value: Any) -> str:
    if not isinstance(value, str) or not 1 <= len(value.encode("utf-8")) <= 128:
        raise ValueError("invalid record")
    return value


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64decode(value: Any, maximum: int) -> bytes:
    if not isinstance(value, str) or len(value) > 2 * maximum + 8:
        raise ValueError("invalid record")
    try:
        padding = "=" * (-len(value) % 4)
        result = base64.b64decode(value + padding, altchars=b"-_", validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid record") from exc
    if len(result) > maximum:
        raise ValueError("invalid record")
    return result


def _aad(key_id: str, stream: str, sequence: int, context: str) -> bytes:
    value = {
        "alg": ALGORITHM,
        "ctx": context,
        "kid": key_id,
        "seq": sequence,
        "stream": stream,
        "v": VERSION,
    }
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


class RecordWriter:
    def __init__(self, key: bytes, *, key_id: str, context: str) -> None:
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError("record key must contain 32 bytes")
        self._cipher = AESGCM(key)
        self.key_id = _validate_identity(key_id)
        self.context = _validate_context(context)
        self.stream = secrets.token_hex(16)
        self._prefix = os.urandom(4)
        self._sequence = 0

    def seal(self, plaintext: bytes) -> dict[str, Any]:
        if not isinstance(plaintext, bytes) or len(plaintext) > MAX_PLAINTEXT:
            raise ValueError("plaintext must be bytes up to 64 KiB")
        if self._sequence >= 2**64:
            raise ValueError("record sequence exhausted")
        sequence = self._sequence
        nonce = self._prefix + sequence.to_bytes(8, "big")
        aad = _aad(self.key_id, self.stream, sequence, self.context)
        ciphertext = self._cipher.encrypt(nonce, plaintext, aad)
        self._sequence += 1
        return {
            "v": VERSION,
            "alg": ALGORITHM,
            "kid": self.key_id,
            "stream": self.stream,
            "seq": sequence,
            "ctx": self.context,
            "nonce": _b64encode(nonce),
            "ciphertext": _b64encode(ciphertext),
        }


class RecordReader:
    def __init__(self, key: bytes, *, key_id: str, context: str) -> None:
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError("record key must contain 32 bytes")
        self._cipher = AESGCM(key)
        self.key_id = _validate_identity(key_id)
        self.context = _validate_context(context)
        self._stream: str | None = None
        self._prefix: bytes | None = None
        self._next_sequence = 0

    def open(self, record: Any) -> bytes:
        if not isinstance(record, dict) or set(record) != FIELDS:
            raise ValueError("invalid record")
        if record.get("v") != VERSION or record.get("alg") != ALGORITHM:
            raise ValueError("unsupported record")
        key_id = _validate_identity(record.get("kid"))
        stream = _validate_identity(record.get("stream"))
        context = _validate_context(record.get("ctx"))
        sequence = record.get("seq")
        if key_id != self.key_id or context != self.context:
            raise ValueError("record context mismatch")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence != self._next_sequence:
            raise ValueError("record sequence mismatch")
        if self._stream is not None and stream != self._stream:
            raise ValueError("record stream mismatch")
        nonce = _b64decode(record.get("nonce"), 12)
        ciphertext = _b64decode(record.get("ciphertext"), MAX_PLAINTEXT + 16)
        if len(nonce) != 12 or len(ciphertext) < 16 or int.from_bytes(nonce[4:], "big") != sequence:
            raise ValueError("invalid record")
        if self._prefix is not None and nonce[:4] != self._prefix:
            raise ValueError("record nonce prefix mismatch")
        aad = _aad(key_id, stream, sequence, context)
        try:
            plaintext = self._cipher.decrypt(nonce, ciphertext, aad)
        except InvalidTag as exc:
            raise ValueError("authentication failed") from exc
        self._stream = stream
        self._prefix = nonce[:4]
        self._next_sequence += 1
        return plaintext


def main() -> int:
    key = AESGCM.generate_key(bit_length=256)
    writer = RecordWriter(key, key_id="lab-key-a", context="rte-record-demo")
    reader = RecordReader(key, key_id="lab-key-a", context="rte-record-demo")
    records = [writer.seal(value) for value in (b"one", b"two", b"three")]
    print([reader.open(record).decode("ascii") for record in records])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
