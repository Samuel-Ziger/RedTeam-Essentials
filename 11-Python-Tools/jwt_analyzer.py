#!/usr/bin/env python3
"""
jwt_analyzer.py - Analisador estatico de JSON Web Tokens.

Decodifica header e payload (sem verificar assinatura), aponta red flags
comuns em pentest web (alg=none, alg=HS256 com chaves fracas em wordlist,
exp/iat ausentes ou implausiveis, kid/x5u injectaveis, etc.) e gera um
relatorio JSON.

Uso:
    python jwt_analyzer.py -t <jwt>
    python jwt_analyzer.py -f token.txt --bruteforce-secrets common-passwords.txt

Sem dependencias externas.

Autor:    Samuel Ziger - RedTeam Essentials
Versao:   2.0.0
Licenca:  MIT
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib" / "python"))
from rte_common import (  # noqa: E402
    RTEContext,
    export_json,
    get_logger,
    log_success,
)

LOG = get_logger("rte.jwt")

_HMAC_ALGS = {
    "HS256": hashlib.sha256,
    "HS384": hashlib.sha384,
    "HS512": hashlib.sha512,
}


def _b64url_decode(seg: str) -> bytes:
    seg += "=" * (-len(seg) % 4)
    return base64.urlsafe_b64decode(seg.encode("ascii"))


def decode_jwt(token: str) -> tuple[dict, dict, str]:
    parts = token.strip().split(".")
    if len(parts) != 3:
        raise ValueError("JWT deve ter 3 partes (header.payload.signature)")
    header = json.loads(_b64url_decode(parts[0]))
    payload = json.loads(_b64url_decode(parts[1]))
    return header, payload, parts[2]


def analyze(header: dict, payload: dict, signature: str) -> list[dict]:
    findings: list[dict] = []

    def add(sev: str, code: str, msg: str) -> None:
        findings.append({"severity": sev, "code": code, "message": msg})

    alg = str(header.get("alg", "")).upper()
    if alg in ("NONE", ""):
        add("CRITICAL", "JWT-001", "alg=none: assinatura nao verificada (CVE-classic).")
    if "kid" in header:
        kid = str(header["kid"])
        if any(c in kid for c in "../\\;'\""):
            add("HIGH", "JWT-002", f"kid suspeito (path/SQLi): {kid!r}")
    for jws in ("jku", "x5u"):
        if jws in header:
            add("HIGH", "JWT-003", f"{jws} presente ({header[jws]!r}): potencial SSRF/cache poisoning.")
    if alg.startswith("HS"):
        add("INFO", "JWT-004", f"HMAC ({alg}). Verifique secret forte e nao reutilizado.")
    if alg.startswith("RS") or alg.startswith("ES"):
        add("INFO", "JWT-005", f"Assinatura assimetrica ({alg}). Cheque confusao alg HS<->RS.")

    now = int(time.time())
    if "exp" not in payload:
        add("MEDIUM", "JWT-006", "Sem campo exp: token nunca expira.")
    else:
        try:
            exp = int(payload["exp"])
            if exp - now > 60 * 60 * 24 * 30:
                add("LOW", "JWT-007", f"exp muito longe ({exp - now}s).")
            if exp < now:
                add("INFO", "JWT-008", "Token ja expirado.")
        except (TypeError, ValueError):
            add("MEDIUM", "JWT-009", "exp nao e numerico.")

    if "iat" not in payload:
        add("LOW", "JWT-010", "Sem iat (issued-at).")
    for claim in ("iss", "aud", "sub"):
        if claim not in payload:
            add("INFO", "JWT-011", f"Sem claim {claim}.")

    for key, value in payload.items():
        if isinstance(value, str) and len(value) > 256:
            add("LOW", "JWT-012", f"Claim {key!r} muito longa ({len(value)} chars).")

    if not signature and alg not in ("NONE", ""):
        add("HIGH", "JWT-013", f"Assinatura vazia com alg={alg}.")
    return findings


def try_secrets(token: str, alg: str, secrets_file: Path) -> str | None:
    """Tenta quebrar HS256/384/512 com wordlist."""
    fn = _HMAC_ALGS.get(alg)
    if not fn:
        return None
    head_b64, payload_b64, sig_b64 = token.split(".")
    signing_input = f"{head_b64}.{payload_b64}".encode("ascii")
    expected = _b64url_decode(sig_b64)
    LOG.info("Bruteforce %s com %s ...", alg, secrets_file)
    with secrets_file.open("rb") as fh:
        for raw in fh:
            secret = raw.strip()
            if not secret:
                continue
            got = hmac.new(secret, signing_input, fn).digest()
            if hmac.compare_digest(got, expected):
                return secret.decode("utf-8", errors="replace")
    return None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="JWT analyzer educacional")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("-t", "--token", help="JWT no proprio comando")
    grp.add_argument("-f", "--file", help="arquivo contendo o JWT")
    p.add_argument("--bruteforce-secrets", help="wordlist para tentar HS*")
    p.add_argument("-o", "--output", default="./output", help="diretorio de saida")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ctx = RTEContext(tool="JWT Analyzer", output_dir=Path(args.output))
    ctx.banner()

    if args.file:
        token = Path(args.file).read_text().strip()
    else:
        token = args.token.strip()

    try:
        header, payload, sig = decode_jwt(token)
    except Exception as exc:  # noqa: BLE001
        LOG.error("JWT invalido: %s", exc)
        return 1

    log_success(LOG, f"Algoritmo: {header.get('alg', '?')}")
    findings = analyze(header, payload, sig)

    cracked: str | None = None
    alg = str(header.get("alg", "")).upper()
    if args.bruteforce_secrets and alg in _HMAC_ALGS:
        cracked = try_secrets(token, alg, Path(args.bruteforce_secrets))
        if cracked is not None:
            findings.append(
                {
                    "severity": "CRITICAL",
                    "code": "JWT-CRACK",
                    "message": f"Secret encontrado por bruteforce: {cracked!r}",
                }
            )

    output = {
        "metadata": {"tool": "jwt_analyzer.py", "version": "2.0.0"},
        "header": header,
        "payload": payload,
        "signature_present": bool(sig),
        "findings": findings,
        "cracked_secret": cracked,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    export_json(output, args.output, "jwt_analysis")
    return 0


if __name__ == "__main__":
    sys.exit(main())
