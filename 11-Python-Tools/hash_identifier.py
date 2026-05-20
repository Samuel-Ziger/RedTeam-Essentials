#!/usr/bin/env python3
"""
hash_identifier.py - Identifica o provavel tipo de um hash e sugere o modo
                     correspondente para hashcat/john.

Baseado em padroes (length, charset, prefixo) das hashes mais comuns em
pentests modernos. Util para olhar /etc/shadow, dumps NTDS, kerberoast
hashes, etc.

Uso:
    python hash_identifier.py '$2a$10$abc...'
    python hash_identifier.py -f hashes.txt

Autor:    Samuel Ziger - RedTeam Essentials
Versao:   2.0.0
Licenca:  MIT
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib" / "python"))
from rte_common import get_logger, log_success  # noqa: E402

LOG = get_logger("rte.hash")


@dataclass
class Sig:
    name: str
    hashcat_mode: int | None
    john_format: str | None
    pattern: re.Pattern[str]


SIGS: list[Sig] = [
    Sig("MD5",            0,     "raw-md5",      re.compile(r"^[a-f0-9]{32}$", re.I)),
    Sig("SHA-1",          100,   "raw-sha1",     re.compile(r"^[a-f0-9]{40}$", re.I)),
    Sig("SHA-256",        1400,  "raw-sha256",   re.compile(r"^[a-f0-9]{64}$", re.I)),
    Sig("SHA-512",        1700,  "raw-sha512",   re.compile(r"^[a-f0-9]{128}$", re.I)),
    Sig("NTLM",           1000,  "NT",           re.compile(r"^[a-f0-9]{32}$", re.I)),
    Sig("LM",             3000,  "LM",           re.compile(r"^[a-f0-9]{32}$", re.I)),
    Sig("MySQL >= 4.1",   300,   "mysql-sha1",   re.compile(r"^\*?[A-F0-9]{40}$", re.I)),
    Sig("bcrypt",         3200,  "bcrypt",       re.compile(r"^\$2[abxy]?\$\d{2}\$[./A-Za-z0-9]{53}$")),
    Sig("sha512crypt",    1800,  "sha512crypt",  re.compile(r"^\$6\$[^$]+\$[./A-Za-z0-9]{86}$")),
    Sig("sha256crypt",    7400,  "sha256crypt",  re.compile(r"^\$5\$[^$]+\$[./A-Za-z0-9]{43}$")),
    Sig("md5crypt",       500,   "md5crypt",     re.compile(r"^\$1\$[^$]+\$[./A-Za-z0-9]{22}$")),
    Sig("PHPass",         400,   "phpass",       re.compile(r"^\$P\$[./A-Za-z0-9]{31}$")),
    Sig("Argon2",         None,  "argon2",       re.compile(r"^\$argon2(id|i|d)\$.+$")),
    Sig("PBKDF2-HMAC-SHA256", 10900, "pbkdf2-hmac-sha256", re.compile(r"^pbkdf2_sha256\$\d+\$.+$")),
    Sig("Kerberos 5 TGS (Kerberoast)", 13100, "krb5tgs", re.compile(r"^\$krb5tgs\$23\$.+$")),
    Sig("Kerberos 5 ASREP (AS-REP Roast)", 18200, "krb5asrep", re.compile(r"^\$krb5asrep\$23\$.+$")),
    Sig("NetNTLMv2",      5600,  "netntlmv2",    re.compile(r"^[^:]+::[^:]+:[a-f0-9]+:[a-f0-9]+:[a-f0-9]+$", re.I)),
    Sig("NetNTLMv1",      5500,  "netntlm",      re.compile(r"^[^:]+::[^:]+:[a-f0-9]+:[a-f0-9]+:[a-f0-9]+$", re.I)),
    Sig("WPA-PMKID",      16800, "wpa-pmkid",    re.compile(r"^[a-f0-9]{32}\*[a-f0-9]{12}\*[a-f0-9]{12}\*[a-f0-9]+$", re.I)),
    Sig("JWT (HS*)",      None,  "jwt",          re.compile(r"^eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")),
]


def identify(hash_value: str) -> list[Sig]:
    h = hash_value.strip()
    return [s for s in SIGS if s.pattern.match(h)]


def fmt(sig: Sig) -> str:
    hc = f"-m {sig.hashcat_mode}" if sig.hashcat_mode is not None else "n/a"
    jo = sig.john_format or "n/a"
    return f"{sig.name:<35} hashcat={hc:<10} john={jo}"


def main() -> int:
    p = argparse.ArgumentParser(description="Identificador de hash")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("hash", nargs="?", help="hash inline")
    grp.add_argument("-f", "--file", help="arquivo com hashes (uma por linha)")
    args = p.parse_args()

    inputs: list[str]
    if args.file:
        inputs = [line.strip() for line in Path(args.file).read_text().splitlines() if line.strip()]
    else:
        inputs = [args.hash]

    for h in inputs:
        matches = identify(h)
        if not matches:
            LOG.warning("nenhum match para %s", h[:60])
            continue
        log_success(LOG, f"{h[:60]}{'…' if len(h) > 60 else ''}")
        for m in matches:
            print("  ", fmt(m))
    return 0


if __name__ == "__main__":
    sys.exit(main())
