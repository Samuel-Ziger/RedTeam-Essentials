#!/usr/bin/env python3
"""Create and verify bounded, versioned scrypt password records."""

from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import secrets

DEFAULT_N = 2**14
R = 8
P = 1
SALT_BYTES = 16
KEY_BYTES = 32


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.b64decode(value + padding, altchars=b"-_", validate=True)


def create_record(password: str, *, salt: bytes | None = None, n: int = DEFAULT_N) -> str:
    if not password:
        raise ValueError("password must not be empty")
    if n < 2**14 or n > 2**20 or n & (n - 1):
        raise ValueError("scrypt N must be a power of two between 2^14 and 2^20")
    actual_salt = secrets.token_bytes(SALT_BYTES) if salt is None else salt
    if len(actual_salt) != SALT_BYTES:
        raise ValueError("salt must be 16 bytes")
    derived = hashlib.scrypt(
        password.encode("utf-8"), salt=actual_salt, n=n, r=R, p=P, dklen=KEY_BYTES
    )
    return "$".join(
        ("scrypt", "v=1", f"n={n}", f"r={R}", f"p={P}", _b64encode(actual_salt), _b64encode(derived))
    )


def verify_record(password: str, record: str) -> bool:
    try:
        algorithm, version, n_raw, r_raw, p_raw, salt_raw, derived_raw = record.split("$")
        n = int(n_raw.removeprefix("n="))
        r = int(r_raw.removeprefix("r="))
        p = int(p_raw.removeprefix("p="))
        if algorithm != "scrypt" or version != "v=1" or r != R or p != P:
            return False
        salt = _b64decode(salt_raw)
        expected = _b64decode(derived_raw)
        if len(salt) != SALT_BYTES or len(expected) != KEY_BYTES:
            return False
        if n < 2**14 or n > 2**20 or n & (n - 1):
            return False
        actual = hashlib.scrypt(
            password.encode("utf-8"), salt=salt, n=n, r=r, p=p, dklen=KEY_BYTES
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(actual, expected)


def main() -> int:
    password = getpass.getpass("Senha sintética: ")
    record = create_record(password)
    print(record)
    confirmation = getpass.getpass("Confirme: ")
    print("válida" if verify_record(confirmation, record) else "inválida")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
