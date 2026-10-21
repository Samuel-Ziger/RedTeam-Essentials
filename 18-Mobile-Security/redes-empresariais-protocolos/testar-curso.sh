#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_network_courses.py" --module 18
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/architecture_audit.py" "$course_dir/fixtures/architecture.json" >/dev/null
python3 "$course_dir/exemplos/rnp1_demo.py" >/dev/null
echo "[OK] Redes V validado"
