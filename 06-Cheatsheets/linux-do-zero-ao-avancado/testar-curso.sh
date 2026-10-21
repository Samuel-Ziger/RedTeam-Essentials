#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
readonly ROOT

printf '==> exemplos seguros do curso Linux\n'
bash "$ROOT/exemplos/tests/test_examples.sh"

printf '\n==> links Markdown locais do curso\n'
python3 - "$ROOT" <<'PY'
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
pattern = re.compile(r"\[[^]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)")
errors = []
for document in sorted(root.rglob("*.md")):
    text = document.read_text(encoding="utf-8")
    for raw in pattern.findall(text):
        target = (document.parent / raw).resolve()
        if not target.exists():
            errors.append(f"{document.relative_to(root)} -> {raw}")
if errors:
    print("links locais ausentes:", file=sys.stderr)
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("[PASS] links Markdown locais")
PY

printf '\n[OK] curso Linux validado sem privilegios\n'
