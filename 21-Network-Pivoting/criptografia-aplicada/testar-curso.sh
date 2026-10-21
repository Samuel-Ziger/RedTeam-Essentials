#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_crypto_courses.py" --module 21
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/tls_policy.py" "$course_dir/fixtures/tls-policy.json" >/dev/null
bash "$course_dir/exemplos/mini_pki.sh" >/dev/null
echo "[OK] Criptografia III validada"
