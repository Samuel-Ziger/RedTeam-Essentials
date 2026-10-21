#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_network_courses.py" --module 16
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/vlan_plan.py" "$course_dir/fixtures/vlan-plan.json" >/dev/null
echo "[OK] Redes III validado"
