#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_network_courses.py" --module 17
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/route_policy.py" lookup "$course_dir/fixtures/routes.json" 10.20.30.40 >/dev/null
python3 "$course_dir/exemplos/route_policy.py" acl "$course_dir/fixtures/acl.json" 10.1.10.5 10.2.20.8 tcp 443 >/dev/null
echo "[OK] Redes IV validado"
