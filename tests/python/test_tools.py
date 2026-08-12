from __future__ import annotations

import base64
import hashlib
import hmac
import json

import pytest
from conftest import load_tool

hash_identifier = load_tool("hash_identifier")
jwt_analyzer = load_tool("jwt_analyzer")
port_scanner = load_tool("port_scanner")
subdomain_enum = load_tool("subdomain_enum")


def b64url(value: dict) -> str:
    raw = json.dumps(value, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def test_port_parser_supports_lists_ranges_and_deduplication() -> None:
    assert port_scanner.parse_ports("443,80,80,100-102") == [80, 100, 101, 102, 443]
    assert len(port_scanner.parse_ports("top100")) == 100


@pytest.mark.parametrize("spec", ["abc", "1-x", "22-20"])
def test_port_parser_rejects_invalid_or_empty_specs(spec: str) -> None:
    with pytest.raises(ValueError):
        port_scanner.parse_ports(spec)


def test_jwt_decode_and_static_findings() -> None:
    token = f"{b64url({'alg': 'none', 'kid': '../key'})}.{b64url({'sub': 'lab'})}."
    header, payload, signature = jwt_analyzer.decode_jwt(token)
    codes = {finding["code"] for finding in jwt_analyzer.analyze(header, payload, signature)}
    assert {"JWT-001", "JWT-002", "JWT-006", "JWT-010"} <= codes


def test_jwt_secret_check_uses_offline_wordlist(tmp_path) -> None:
    header = b64url({"alg": "HS256"})
    payload = b64url({"sub": "student"})
    signing_input = f"{header}.{payload}".encode()
    digest = hmac.new(b"lab-secret", signing_input, hashlib.sha256).digest()
    signature = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    token = f"{header}.{payload}.{signature}"
    wordlist = tmp_path / "secrets.txt"
    wordlist.write_text("wrong\nlab-secret\n", encoding="utf-8")
    assert jwt_analyzer.try_secrets(token, "HS256", wordlist) == "lab-secret"


def test_hash_identifier_reports_ambiguous_raw_hashes() -> None:
    names = {item.name for item in hash_identifier.identify("d41d8cd98f00b204e9800998ecf8427e")}
    assert {"MD5", "NTLM", "LM"} <= names


def test_subdomain_parsers_with_offline_fixtures(monkeypatch) -> None:
    crt_fixture = json.dumps([{"name_value": "*.api.example.com\nexample.com"}, {"name_value": "outside.test"}])
    monkeypatch.setattr(subdomain_enum, "_http_get", lambda _url: crt_fixture)
    assert subdomain_enum.fetch_crtsh("example.com") == {"api.example.com", "example.com"}
