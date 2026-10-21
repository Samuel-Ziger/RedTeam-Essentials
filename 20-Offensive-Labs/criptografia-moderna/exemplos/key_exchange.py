#!/usr/bin/env python3
"""Authenticated-protocol building block: X25519 followed by HKDF."""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

DOMAIN = b"rte-x25519-session-v1\x00"


def public_bytes(private_key: X25519PrivateKey) -> bytes:
    return private_key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def derive_key(private_key: X25519PrivateKey, peer_public: bytes, *, context: bytes) -> bytes:
    if not 1 <= len(context) <= 256:
        raise ValueError("context must contain 1 to 256 bytes")
    if len(peer_public) != 32:
        raise ValueError("X25519 public key must contain 32 bytes")
    peer = X25519PublicKey.from_public_bytes(peer_public)
    shared_secret = private_key.exchange(peer)
    if shared_secret == bytes(32):
        raise ValueError("invalid shared secret")
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=DOMAIN + context).derive(shared_secret)


def main() -> int:
    alice = X25519PrivateKey.generate()
    bob = X25519PrivateKey.generate()
    context = b"protocol=rte-demo;version=1;roles=alice,bob"
    alice_key = derive_key(alice, public_bytes(bob), context=context)
    bob_key = derive_key(bob, public_bytes(alice), context=context)
    print(f"same session key: {alice_key == bob_key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
