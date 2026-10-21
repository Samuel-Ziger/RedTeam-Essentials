#!/usr/bin/env bash
set -Eeuo pipefail

read_os_field() {
    local field=$1
    local value
    value=$(sed -n "s/^${field}=//p" /etc/os-release 2>/dev/null | head -n 1)
    value=${value%\"}
    value=${value#\"}
    printf '%s' "${value:-unknown}"
}

read_mem_total() {
    awk '$1 == "MemTotal:" { print $2; found=1; exit } END { if (!found) print "unknown" }' /proc/meminfo
}

read_init() {
    if [[ -r /proc/1/comm ]]; then
        tr -d '\n' < /proc/1/comm
    else
        printf unknown
    fi
}

read_root_fs() {
    if command -v findmnt >/dev/null 2>&1; then
        findmnt -n -o FSTYPE / 2>/dev/null || printf unknown
    else
        awk '$2 == "/" { print $3; found=1; exit } END { if (!found) print "unknown" }' /proc/mounts
    fi
}

main() {
    if (( $# != 0 )); then
        printf 'uso: %s\n' "${0##*/}" >&2
        return 2
    fi

    printf 'schema=linux-course-diagnostic/v1\n'
    printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'os_id=%s\n' "$(read_os_field ID)"
    printf 'os_version=%s\n' "$(read_os_field VERSION_ID)"
    printf 'kernel=%s\n' "$(uname -r)"
    printf 'architecture=%s\n' "$(uname -m)"
    printf 'cpu_count=%s\n' "$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf unknown)"
    printf 'page_size=%s\n' "$(getconf PAGESIZE 2>/dev/null || printf unknown)"
    printf 'mem_total_kib=%s\n' "$(read_mem_total)"
    printf 'init=%s\n' "$(read_init)"
    printf 'root_filesystem=%s\n' "$(read_root_fs)"
    printf 'uid=%s\n' "$(id -u)"
}

main "$@"
