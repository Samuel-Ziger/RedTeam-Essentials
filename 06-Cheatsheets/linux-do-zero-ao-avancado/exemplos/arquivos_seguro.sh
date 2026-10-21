#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    printf 'uso: %s DIRETORIO-PAI\n' "${0##*/}" >&2
}

main() {
    if (( $# != 1 )); then
        usage
        return 2
    fi

    local parent=$1
    if [[ ! -d $parent || ! -w $parent || $parent == / ]]; then
        printf 'erro: use um diretorio-pai gravavel e restrito\n' >&2
        return 1
    fi

    local lab
    lab=$(mktemp -d -- "$parent/arquivos-linux.XXXXXX")
    trap 'rm -rf -- "$lab"' RETURN

    mkdir -p -- "$lab/dados"
    printf '%s\n' alpha beta gamma > "$lab/dados/relatorio final.txt"
    printf '%s\n' delta > "$lab/dados/linha
extra.txt"
    ln -- "$lab/dados/relatorio final.txt" "$lab/dados/relatorio.hard"
    ln -s -- 'relatorio final.txt' "$lab/dados/relatorio.link"

    local regular_count=0
    while IFS= read -r -d '' path; do
        [[ -f $path ]] && ((regular_count += 1))
    done < <(find "$lab/dados" -maxdepth 1 -type f -print0)

    local inode_original inode_hard
    inode_original=$(stat -c '%i' -- "$lab/dados/relatorio final.txt")
    inode_hard=$(stat -c '%i' -- "$lab/dados/relatorio.hard")

    printf 'regular_files=%d\n' "$regular_count"
    printf 'hardlink_same_inode=%s\n' "$([[ $inode_original == "$inode_hard" ]] && printf yes || printf no)"
    printf 'symlink_target=%s\n' "$(readlink -- "$lab/dados/relatorio.link")"
    printf 'content_lines=%s\n' "$(wc -l < "$lab/dados/relatorio final.txt")"
}

main "$@"
