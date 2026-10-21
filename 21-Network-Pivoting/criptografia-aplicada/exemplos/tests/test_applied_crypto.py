from __future__ import annotations

import importlib.util
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

EXAMPLES = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


certificate_audit = load("certificate_audit")
tls_policy = load("tls_policy")


def make_leaf(start: datetime, end: datetime) -> bytes:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "api.example.test")])
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(start)
        .not_valid_after(end)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(x509.SubjectAlternativeName([x509.DNSName("api.example.test")]), critical=False)
        .sign(key, hashes.SHA256())
    )
    return certificate.public_bytes(serialization.Encoding.PEM)


class AppliedCryptoTests(unittest.TestCase):
    def test_certificate_inventory(self) -> None:
        now = datetime.now(timezone.utc)
        report = certificate_audit.audit_certificate(
            make_leaf(now - timedelta(minutes=1), now + timedelta(days=1)), now=now
        )
        self.assertEqual(report["dnsNames"], ["api.example.test"])
        self.assertFalse(report["isCA"])
        self.assertFalse(report["trustEvaluated"])
        self.assertEqual(report["warnings"], [])

    def test_expired_certificate_warning(self) -> None:
        now = datetime.now(timezone.utc)
        report = certificate_audit.audit_certificate(
            make_leaf(now - timedelta(days=2), now - timedelta(days=1)), now=now
        )
        self.assertIn("certificate is expired", report["warnings"])

    def test_policy_passes_strict_profile(self) -> None:
        policy = {
            "minimumVersion": "TLSv1.3",
            "maximumVersion": "TLSv1.3",
            "legacyAllowed": False,
            "requireClientCertificate": True,
            "certificateAutomation": True,
            "validationDisabled": False,
        }
        self.assertEqual(tls_policy.audit_policy(policy), [])

    def test_policy_detects_validation_bypass(self) -> None:
        policy = {
            "minimumVersion": "TLSv1.2",
            "maximumVersion": "TLSv1.3",
            "legacyAllowed": True,
            "requireClientCertificate": False,
            "certificateAutomation": False,
            "validationDisabled": True,
        }
        self.assertEqual(len(tls_policy.audit_policy(policy)), 4)

    def test_policy_rejects_unknown_field(self) -> None:
        with self.assertRaises(ValueError):
            tls_policy.audit_policy({"minimumVersion": "TLSv1.3"})


if __name__ == "__main__":
    unittest.main()
