#!/usr/bin/env bash
set -Eeuo pipefail

if (( $# < 2 || $# > 3 )); then
    printf 'usage: %s SOURCE_DIR OUTPUT.tar [SOURCE_DATE_EPOCH]\n' "$0" >&2
    exit 64
fi

source_dir=$1
output=$2
epoch=${3:-${SOURCE_DATE_EPOCH:-0}}

if [[ ! -d $source_dir ]]; then
    printf 'source directory not found: %s\n' "$source_dir" >&2
    exit 66
fi
if [[ ! $epoch =~ ^[0-9]+$ ]]; then
    printf 'SOURCE_DATE_EPOCH must be a non-negative integer\n' >&2
    exit 64
fi

source_dir=$(cd -- "$source_dir" && pwd)
output_parent=$(dirname -- "$output")
mkdir -p -- "$output_parent"
output_parent=$(cd -- "$output_parent" && pwd)
output="$output_parent/$(basename -- "$output")"

tar --sort=name \
    --format=posix \
    --pax-option=delete=atime,delete=ctime \
    --mtime="@$epoch" \
    --owner=0 --group=0 --numeric-owner \
    -cf "$output" -C "$source_dir" .

printf 'archive=%s\n' "$output"
printf 'sha256=%s\n' "$(sha256sum "$output" | awk '{print $1}')"
