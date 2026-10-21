#!/usr/bin/env bash
set -Eeuo pipefail

COURSE_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
readonly COURSE_DIR

python3 "$COURSE_DIR/../../scripts/validate_windows_courses.py" --module 11
if command -v pwsh >/dev/null 2>&1 && \
    pwsh -NoLogo -NoProfile -Command \
        'if (Get-Command Invoke-Pester -ErrorAction SilentlyContinue) { exit 0 }; exit 1'; then
    RTE_TEST_PATH="$COURSE_DIR/exemplos/tests" \
        pwsh -NoLogo -NoProfile -Command 'Invoke-Pester -Path $env:RTE_TEST_PATH -CI'
else
    printf '[SKIP] PowerShell ou Pester indisponível; CI Windows executa os testes\n'
fi
printf '[OK] Windows empresarial II validado\n'
