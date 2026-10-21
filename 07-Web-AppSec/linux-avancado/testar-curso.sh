#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
readonly ROOT

printf '==> safe advanced Linux examples\n'
bash "$ROOT/exemplos/tests/test_examples.sh"

printf '\n==> local Markdown links\n'
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
    print("missing local links:", file=sys.stderr)
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("[PASS] local Markdown links")
PY

printf '\n==> network-scope guard\n'
python3 - "$ROOT" <<'PY'
import sys
from pathlib import Path

root = Path(sys.argv[1])
forbidden_files = {
    "nftables", "conntrack", "routing", "roteamento", "network-namespace",
    "networking", "tcpdump", "wireshark", "xdp-program",
}
errors = []
for path in root.rglob("*"):
    if path.is_file() and any(term in path.name.lower() for term in forbidden_files):
        errors.append(str(path.relative_to(root)))
if errors:
    print("network-specific files found:", *errors, sep="\n", file=sys.stderr)
    raise SystemExit(1)
print("[PASS] no network-specific course files")
PY

printf '\n[OK] advanced Linux course validated without privileges\n'
