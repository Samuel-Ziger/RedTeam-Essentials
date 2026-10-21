#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_edge_security_course.py"
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/edge_risk_engine.py" \
  "$course_dir/fixtures/requests-sinteticas.json" >/dev/null
python3 "$course_dir/exemplos/control_plane_audit.py" \
  "$course_dir/fixtures/politica-edge.json" >/dev/null
python3 "$course_dir/exemplos/token_bucket.py" \
  "$course_dir/fixtures/eventos-rate-limit.json" >/dev/null
echo "[OK] Especialização Purple Team validada"
