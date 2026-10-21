#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_crypto_courses.py" --module 20
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/secure_envelope.py" >/dev/null
python3 "$course_dir/exemplos/key_exchange.py" >/dev/null
python3 "$course_dir/exemplos/signatures.py" >/dev/null
echo "[OK] Criptografia II validada"
