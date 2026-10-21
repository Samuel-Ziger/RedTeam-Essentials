#!/usr/bin/env bash
set -Eeuo pipefail

if (( $# != 2 )); then
    printf 'usage: %s OLD_CONFIG NEW_CONFIG\n' "$0" >&2
    exit 64
fi

old_config=$1
new_config=$2
for file in "$old_config" "$new_config"; do
    if [[ ! -r $file ]]; then
        printf 'config not readable: %s\n' "$file" >&2
        exit 66
    fi
done

temporary=$(mktemp -d)
trap 'rm -rf -- "$temporary"' EXIT

normalize() {
    awk '
      /^CONFIG_[A-Za-z0-9_]+=/ { print; next }
      /^# CONFIG_[A-Za-z0-9_]+ is not set$/ {
        print substr($0, 3, length($0) - 13) "=n"
      }
    ' "$1" | LC_ALL=C sort -u
}

normalize "$old_config" > "$temporary/old"
normalize "$new_config" > "$temporary/new"

printf 'schema=rte-kconfig-diff/v1\n'
awk -F= '
  NR == FNR { old[$1]=$2; next }
  {
    seen[$1]=1
    if (!($1 in old)) printf "added.%s=%s\n", $1, $2
    else if (old[$1] != $2) printf "changed.%s=%s->%s\n", $1, old[$1], $2
  }
  END {
    for (key in old) if (!(key in seen)) printf "removed.%s=%s\n", key, old[key]
  }
' "$temporary/old" "$temporary/new" | LC_ALL=C sort
