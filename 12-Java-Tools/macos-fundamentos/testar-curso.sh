#!/usr/bin/env bash
set -Eeuo pipefail

COURSE_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
readonly COURSE_DIR

python3 "$COURSE_DIR/../../scripts/validate_macos_courses.py" --module 12
python3 -m unittest discover -s "$COURSE_DIR/exemplos/tests" -v
python3 "$COURSE_DIR/exemplos/Get-RteMacBaseline.py" \
    --fixture "$COURSE_DIR/exemplos/fixtures/mac-command-output.json" >/dev/null

if [[ $(uname -s) == Darwin ]]; then
    python3 "$COURSE_DIR/exemplos/Get-RteMacBaseline.py" >/dev/null
else
    printf '[SKIP] coleta real exige macOS; fixture validada localmente\n'
fi

printf '[OK] macOS I validado\n'
