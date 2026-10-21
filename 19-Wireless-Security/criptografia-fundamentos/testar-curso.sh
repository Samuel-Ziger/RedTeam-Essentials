#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_crypto_courses.py" --module 19
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/number_theory.py" gcd 252 105 >/dev/null
python3 "$course_dir/exemplos/hash_mac.py" digest "$course_dir/fixtures/message.txt" >/dev/null
echo "[OK] Criptografia I validada"
