#!/usr/bin/env python3
"""A bounded, versioned AES-256-GCM envelope for local teaching."""

from __future__ import annotations

import base64
import json
import os
import re
from typing import Any

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VERSION = 1
ALGORITHM = "A256GCM"
MAX_PLAINTEXT = 1024 * 1024
IDENTIFIER = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
FIELDS = {"v", "alg", "kid", "ctx", "nonce", "ciphertext"}


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64decode(value: Any, *, maximum: int) -> bytes:
    if not isinstance(value, str) or len(value) > 2 * maximum + 8:
        raise ValueError("invalid envelope")
    try:
        padding = "=" * (-len(value) % 4)
        decoded = base64.b64decode(value + padding, altchars=b"-_", validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid envelope") from exc
    if len(decoded) > maximum:
        raise ValueError("invalid envelope")
    return decoded


def _validate_identifier(value: Any) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError("invalid envelope")
    return value


def associated_data(key_id: str, context: str) -> bytes:
    _validate_identifier(key_id)
    if not isinstance(context, str) or not 1 <= len(context.encode("utf-8")) <= 128:
        raise ValueError("invalid context")
    value = {"alg": ALGORITHM, "ctx": context, "kid": key_id, "v": VERSION}
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def encrypt(key: bytes, plaintext: bytes, *, key_id: str, context: str) -> dict[str, Any]:
    if not isinstance(key, bytes) or len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")
    if not isinstance(plaintext, bytes) or len(plaintext) > MAX_PLAINTEXT:
        raise ValueError("plaintext must be bytes up to 1 MiB")
    aad = associated_data(key_id, context)
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return {
        "v": VERSION,
        "alg": ALGORITHM,
        "kid": key_id,
        "ctx": context,
        "nonce": _b64encode(nonce),
        "ciphertext": _b64encode(ciphertext),
    }


def decrypt(key: bytes, envelope: dict[str, Any]) -> bytes:
    if not isinstance(key, bytes) or len(key) != 32:
        raise ValueError("authentication failed")
    if not isinstance(envelope, dict) or set(envelope) != FIELDS:
        raise ValueError("invalid envelope")
    if envelope.get("v") != VERSION or envelope.get("alg") != ALGORITHM:
        raise ValueError("unsupported envelope")
    key_id = _validate_identifier(envelope.get("kid"))
    context = envelope.get("ctx")
    aad = associated_data(key_id, context)
    nonce = _b64decode(envelope.get("nonce"), maximum=12)
    ciphertext = _b64decode(envelope.get("ciphertext"), maximum=MAX_PLAINTEXT + 16)
    if len(nonce) != 12 or len(ciphertext) < 16:
        raise ValueError("invalid envelope")
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, aad)
    except InvalidTag as exc:
        raise ValueError("authentication failed") from exc


def main() -> int:
    key = AESGCM.generate_key(bit_length=256)
    envelope = encrypt(key, b"local synthetic record", key_id="lab-2026-a", context="rte-demo")
    recovered = decrypt(key, envelope)
    print(json.dumps(envelope, ensure_ascii=False, sort_keys=True))
    print(f"round-trip: {recovered == b'local synthetic record'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
