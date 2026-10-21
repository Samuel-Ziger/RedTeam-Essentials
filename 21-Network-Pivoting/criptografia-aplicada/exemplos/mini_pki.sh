#!/usr/bin/env bash
set -euo pipefail

command -v openssl >/dev/null 2>&1 || {
  echo "openssl não encontrado" >&2
  exit 1
}

lab_dir="$(mktemp -d "${TMPDIR:-/tmp}/rte-pki.XXXXXX")"
cleanup() {
  find "$lab_dir" -type f -exec chmod u+w {} + 2>/dev/null || true
  rm -rf -- "$lab_dir"
}
trap cleanup EXIT INT TERM
umask 077

openssl req -x509 -newkey rsa:3072 -sha256 -nodes \
  -keyout "$lab_dir/root.key" -out "$lab_dir/root.pem" -days 2 \
  -subj "/CN=RTE Lab Root" \
  -addext "basicConstraints=critical,CA:TRUE,pathlen:0" \
  -addext "keyUsage=critical,keyCertSign,cRLSign" >/dev/null 2>&1

openssl req -new -newkey rsa:2048 -sha256 -nodes \
  -keyout "$lab_dir/server.key" -out "$lab_dir/server.csr" \
  -subj "/CN=api.example.test" >/dev/null 2>&1

printf '%s\n' \
  'basicConstraints=critical,CA:FALSE' \
  'keyUsage=critical,digitalSignature,keyEncipherment' \
  'extendedKeyUsage=serverAuth' \
  'subjectAltName=DNS:api.example.test,DNS:localhost,IP:127.0.0.1' \
  >"$lab_dir/server.ext"

openssl x509 -req -in "$lab_dir/server.csr" \
  -CA "$lab_dir/root.pem" -CAkey "$lab_dir/root.key" -CAcreateserial \
  -out "$lab_dir/server.pem" -days 1 -sha256 \
  -extfile "$lab_dir/server.ext" >/dev/null 2>&1

openssl verify -CAfile "$lab_dir/root.pem" "$lab_dir/server.pem" >/dev/null
openssl x509 -in "$lab_dir/server.pem" -noout -checkhost api.example.test >/dev/null
echo "[OK] mini-PKI e identidade verificadas; material descartado no encerramento"
