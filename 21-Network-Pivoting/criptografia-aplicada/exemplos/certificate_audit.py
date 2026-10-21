#!/usr/bin/env python3
"""Inspect one local PEM certificate without making a trust decision."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, ed448, rsa
from cryptography.hazmat.primitives.hashes import SHA256

MAX_CERTIFICATE_BYTES = 1024 * 1024


def _public_key_description(public_key: Any) -> dict[str, Any]:
    if isinstance(public_key, rsa.RSAPublicKey):
        return {"type": "RSA", "bits": public_key.key_size}
    if isinstance(public_key, ec.EllipticCurvePublicKey):
        return {"type": "EC", "curve": public_key.curve.name, "bits": public_key.key_size}
    if isinstance(public_key, ed25519.Ed25519PublicKey):
        return {"type": "Ed25519"}
    if isinstance(public_key, ed448.Ed448PublicKey):
        return {"type": "Ed448"}
    return {"type": type(public_key).__name__}


def _extension(certificate: x509.Certificate, extension_type: type[Any]) -> Any | None:
    try:
        return certificate.extensions.get_extension_for_class(extension_type).value
    except x509.ExtensionNotFound:
        return None


def audit_certificate(pem: bytes, *, now: datetime | None = None) -> dict[str, Any]:
    if not pem or len(pem) > MAX_CERTIFICATE_BYTES:
        raise ValueError("certificate must contain 1 byte to 1 MiB")
    try:
        certificate = x509.load_pem_x509_certificate(pem)
    except ValueError as exc:
        raise ValueError("invalid PEM certificate") from exc
    current = now or datetime.now(timezone.utc)
    san = _extension(certificate, x509.SubjectAlternativeName)
    constraints = _extension(certificate, x509.BasicConstraints)
    key_usage = _extension(certificate, x509.KeyUsage)
    extended_usage = _extension(certificate, x509.ExtendedKeyUsage)
    warnings: list[str] = []
    if current < certificate.not_valid_before_utc:
        warnings.append("certificate is not yet valid")
    if current >= certificate.not_valid_after_utc:
        warnings.append("certificate is expired")
    if constraints is None:
        warnings.append("Basic Constraints extension is absent")
    if constraints is not None and not constraints.ca and san is None:
        warnings.append("leaf certificate has no Subject Alternative Name")
    if constraints is not None and constraints.ca and key_usage is not None and not key_usage.key_cert_sign:
        warnings.append("CA certificate lacks keyCertSign")
    signature_hash = certificate.signature_hash_algorithm
    return {
        "subject": certificate.subject.rfc4514_string(),
        "issuer": certificate.issuer.rfc4514_string(),
        "serialHex": format(certificate.serial_number, "x"),
        "notBefore": certificate.not_valid_before_utc.isoformat(),
        "notAfter": certificate.not_valid_after_utc.isoformat(),
        "sha256Fingerprint": certificate.fingerprint(SHA256()).hex(),
        "publicKey": _public_key_description(certificate.public_key()),
        "signatureHash": signature_hash.name if signature_hash is not None else None,
        "isCA": constraints.ca if constraints is not None else None,
        "pathLength": constraints.path_length if constraints is not None else None,
        "dnsNames": san.get_values_for_type(x509.DNSName) if san is not None else [],
        "extendedKeyUsage": [item.dotted_string for item in extended_usage] if extended_usage else [],
        "warnings": warnings,
        "trustEvaluated": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        if not args.certificate.is_file() or args.certificate.is_symlink():
            raise ValueError("input must be a regular, non-symlink file")
        report = audit_certificate(args.certificate.read_bytes())
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
