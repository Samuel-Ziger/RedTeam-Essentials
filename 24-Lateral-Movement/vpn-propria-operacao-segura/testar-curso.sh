#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_privacy_courses.py" --module 24
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/wireguard_plan.py" "$course_dir/fixtures/vpn-plan.json" >/dev/null
python3 "$course_dir/exemplos/vpn_policy_audit.py" "$course_dir/fixtures/vpn-policy.json" >/dev/null
echo "[OK] VPN própria e operação segura validadas"
