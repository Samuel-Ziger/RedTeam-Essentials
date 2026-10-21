#!/usr/bin/env python3
"""Hash and authenticate small local files without exposing key material."""

from __future__ import annotations

import argparse
import hashlib
import hmac
from pathlib import Path

MAX_BYTES = 16 * 1024 * 1024


def read_limited(path: Path) -> bytes:
    """Read a regular file while enforcing the course size limit."""
    if not path.is_file() or path.is_symlink():
        raise ValueError("input must be a regular, non-symlink file")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("input exceeds 16 MiB")
    return path.read_bytes()


def digest_file(path: Path) -> str:
    return hashlib.sha256(read_limited(path)).hexdigest()


def tag_file(key_path: Path, message_path: Path) -> str:
    key = read_limited(key_path)
    if len(key) < 32:
        raise ValueError("laboratory key must contain at least 32 bytes")
    return hmac.new(key, read_limited(message_path), hashlib.sha256).hexdigest()


def verify_file(key_path: Path, message_path: Path, expected: str) -> bool:
    try:
        expected_bytes = bytes.fromhex(expected)
    except ValueError:
        return False
    actual = bytes.fromhex(tag_file(key_path, message_path))
    return len(expected_bytes) == len(actual) and hmac.compare_digest(actual, expected_bytes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("digest", "mac", "verify"))
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--tag")
    args = parser.parse_args()
    try:
        if args.operation == "digest" and len(args.paths) == 1:
            print(digest_file(Path(args.paths[0])))
        elif args.operation == "mac" and len(args.paths) == 2:
            print(tag_file(Path(args.paths[0]), Path(args.paths[1])))
        elif args.operation == "verify" and len(args.paths) == 2 and args.tag:
            if not verify_file(Path(args.paths[0]), Path(args.paths[1]), args.tag):
                print("invalid")
                return 1
            print("valid")
        else:
            parser.error("invalid argument combination")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
