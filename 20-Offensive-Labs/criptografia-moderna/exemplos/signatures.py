#!/usr/bin/env python3
"""Ed25519 signatures with explicit domain separation."""

from __future__ import annotations

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

DOMAIN = b"rte-artifact-signature-v1\x00"
MAX_MESSAGE = 1024 * 1024


def _payload(message: bytes) -> bytes:
    if not isinstance(message, bytes) or len(message) > MAX_MESSAGE:
        raise ValueError("message must be bytes up to 1 MiB")
    return DOMAIN + len(message).to_bytes(8, "big") + message


def sign(private_key: Ed25519PrivateKey, message: bytes) -> bytes:
    return private_key.sign(_payload(message))


def verify(public_key: Ed25519PublicKey, message: bytes, signature: bytes) -> bool:
    if len(signature) != 64:
        return False
    try:
        public_key.verify(signature, _payload(message))
    except (InvalidSignature, ValueError):
        return False
    return True


def main() -> int:
    private_key = Ed25519PrivateKey.generate()
    message = b"synthetic artifact"
    signature = sign(private_key, message)
    print(f"valid: {verify(private_key.public_key(), message, signature)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
