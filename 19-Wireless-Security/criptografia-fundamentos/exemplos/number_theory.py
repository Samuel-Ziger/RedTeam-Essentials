#!/usr/bin/env python3
"""Small, transparent number-theory helpers for teaching."""

from __future__ import annotations

import argparse


def gcd(a: int, b: int) -> int:
    """Return the non-negative greatest common divisor."""
    while b:
        a, b = b, a % b
    return abs(a)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) such that a*x + b*y == g == gcd(a, b)."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    if old_r < 0:
        return -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def modular_inverse(value: int, modulus: int) -> int:
    """Return the inverse of value modulo modulus."""
    if modulus <= 1:
        raise ValueError("modulus must be greater than one")
    divisor, coefficient, _ = extended_gcd(value, modulus)
    if divisor != 1:
        raise ValueError("inverse does not exist")
    return coefficient % modulus


def modular_power(base: int, exponent: int, modulus: int) -> int:
    """Compute modular exponentiation with validated teaching inputs."""
    if exponent < 0:
        raise ValueError("exponent must be non-negative")
    if modulus <= 1:
        raise ValueError("modulus must be greater than one")
    return pow(base, exponent, modulus)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("gcd", "inverse", "pow"))
    parser.add_argument("values", nargs="+", type=int)
    args = parser.parse_args()
    expected = 3 if args.operation == "pow" else 2
    if len(args.values) != expected:
        parser.error(f"{args.operation} expects {expected} integers")
    try:
        if args.operation == "gcd":
            result = gcd(*args.values)
        elif args.operation == "inverse":
            result = modular_inverse(*args.values)
        else:
            result = modular_power(*args.values)
    except ValueError as exc:
        parser.error(str(exc))
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
