#!/usr/bin/env bash
set -Eeuo pipefail

COURSE_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
readonly COURSE_DIR

python3 "$COURSE_DIR/../../scripts/validate_macos_courses.py" --module 13
python3 -m unittest discover -s "$COURSE_DIR/exemplos/tests" -v
python3 "$COURSE_DIR/exemplos/ProfileAudit.py" \
    "$COURSE_DIR/exemplos/fixtures/training.mobileconfig" >/dev/null
python3 "$COURSE_DIR/exemplos/Compare-RteMacBaseline.py" \
    "$COURSE_DIR/exemplos/fixtures/desired-baseline.json" \
    "$COURSE_DIR/exemplos/fixtures/observed-baseline.json" >/dev/null

if [[ $(uname -s) == Darwin ]]; then
    output=$(mktemp -d)
    trap 'rm -rf -- "$output"' EXIT
    "$COURSE_DIR/exemplos/dylib/build.zsh" "$output/build" >/dev/null
    codesign --sign - --force "$output/build/librte_math.dylib"
    codesign --sign - --force "$output/build/dylib_consumer"
    codesign --verify --strict "$output/build/librte_math.dylib"
    codesign --verify --strict "$output/build/dylib_consumer"
    "$output/build/dylib_consumer" >"$output/native-output.txt"
    grep -Fx 'api_version=1' "$output/native-output.txt" >/dev/null
    grep -Fx 'sum=42' "$output/native-output.txt" >/dev/null
else
    printf '[SKIP] build Mach-O/dylib e codesign exigem macOS; CI executa no Mac\n'
fi

printf '[OK] macOS II validado\n'
