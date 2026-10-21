#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    printf 'uso: %s FONTE REPOSITORIO ROTULO\n' "${0##*/}" >&2
}

main() {
    if (( $# != 3 )); then
        usage
        return 2
    fi

    local source=$1 repository=$2 label=$3
    [[ -d $source && -r $source ]] || {
        printf 'erro: fonte deve ser um diretorio legivel\n' >&2
        return 1
    }
    [[ $source != / && $repository != / && $repository != "$HOME" ]] || {
        printf 'erro: caminho amplo recusado\n' >&2
        return 1
    }
    [[ $label =~ ^[a-zA-Z0-9._-]+$ ]] || {
        printf 'erro: rotulo invalido\n' >&2
        return 1
    }

    install -d -m 0700 -- "$repository"
    local source_real repository_real
    source_real=$(realpath -- "$source")
    repository_real=$(realpath -- "$repository")
    if [[ $repository_real == "$source_real" || $repository_real == "$source_real"/* ]]; then
        printf 'erro: repositorio nao pode ficar dentro da fonte\n' >&2
        return 1
    fi

    local stamp archive temporary
    stamp=$(date -u +%Y%m%dT%H%M%SZ)
    archive="$repository_real/${label}-${stamp}-$$.tar.gz"
    temporary="$archive.partial"
    trap 'rm -f -- "$temporary"' RETURN

    tar -C "$source_real" -czf "$temporary" .
    tar -tzf "$temporary" >/dev/null
    mv -- "$temporary" "$archive"
    sha256sum -- "$archive" > "$archive.sha256"

    printf 'archive=%s\n' "$archive"
    printf 'checksum=%s\n' "$archive.sha256"
}

main "$@"
