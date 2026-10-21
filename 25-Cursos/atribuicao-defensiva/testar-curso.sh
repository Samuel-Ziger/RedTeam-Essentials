#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd -- "$course_dir/../.." && pwd)"

python3 "$project_root/scripts/validate_privacy_courses.py" --module 25
python3 -m unittest discover -s "$course_dir/exemplos/tests" -v
python3 "$course_dir/exemplos/telemetry_correlator.py" \
  "$course_dir/fixtures/eventos-sinteticos.json" >/dev/null
python3 "$course_dir/exemplos/evidence_manifest.py" \
  "$course_dir/fixtures/evidencias-demo" >/dev/null
echo "[OK] Rastreabilidade e atribuição defensiva validadas"
