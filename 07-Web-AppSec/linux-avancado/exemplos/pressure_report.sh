#!/usr/bin/env bash
set -Eeuo pipefail

printf 'schema=rte-pressure/v1\n'
printf 'kernel=%s\n' "$(uname -r)"

for resource in cpu memory io; do
    file="/proc/pressure/$resource"
    if [[ -r $file ]]; then
        while IFS= read -r line; do
            printf 'psi.%s.%s\n' "$resource" "$line"
        done < "$file"
    else
        printf 'psi.%s=unavailable\n' "$resource"
    fi
done

awk '
  /^(MemTotal|MemAvailable|SwapTotal|SwapFree):/ {
    key=$1
    sub(/:$/, "", key)
    printf "mem.%s_kib=%s\n", key, $2
  }
' /proc/meminfo
