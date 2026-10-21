#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
readonly ROOT
temporary=$(mktemp -d)
trap 'rm -rf -- "$temporary"' EXIT

pass_count=0

pass() {
    ((pass_count += 1))
    printf '[PASS] %s\n' "$1"
}

assert_contains() {
    local file=$1 expected=$2
    if ! grep -Fqx -- "$expected" "$file"; then
        printf '[FAIL] esperado em %s: %s\n' "$file" "$expected" >&2
        return 1
    fi
}

test_files() {
    bash "$ROOT/arquivos_seguro.sh" "$temporary" > "$temporary/files.out"
    assert_contains "$temporary/files.out" 'regular_files=3'
    assert_contains "$temporary/files.out" 'hardlink_same_inode=yes'
    assert_contains "$temporary/files.out" 'symlink_target=relatorio final.txt'
    assert_contains "$temporary/files.out" 'content_lines=3'
    pass 'arquivos, nomes e links'
}

test_diagnostic() {
    bash "$ROOT/diagnostico.sh" > "$temporary/diagnostic.out"
    assert_contains "$temporary/diagnostic.out" 'schema=linux-course-diagnostic/v1'
    grep -Eq '^kernel=.+$' "$temporary/diagnostic.out"
    grep -Eq '^page_size=[0-9]+$' "$temporary/diagnostic.out"
    grep -Eq '^mem_total_kib=[0-9]+$' "$temporary/diagnostic.out"
    if grep -Eq '^(hostname|serial|ip|mac)=' "$temporary/diagnostic.out"; then
        printf '[FAIL] diagnostico expôs identificador evitável\n' >&2
        return 1
    fi
    pass 'diagnostico somente leitura'
}

test_awk() {
    printf '%s\n' \
        '2026-09-30T10:00:00Z INFO api iniciou' \
        '2026-09-30T10:00:01Z ERROR banco falhou' \
        '2026-09-30T10:00:02Z INFO api pronto' |
        awk -f "$ROOT/analisar_logs.awk" > "$temporary/logs.out"
    assert_contains "$temporary/logs.out" 'total=3'
    assert_contains "$temporary/logs.out" 'level.INFO=2'
    assert_contains "$temporary/logs.out" 'level.ERROR=1'
    assert_contains "$temporary/logs.out" 'service.api=2'
    pass 'agregador awk'
}

test_backup() {
    mkdir -p -- "$temporary/source/sub" "$temporary/repository" "$temporary/restore"
    printf '%s\n' 'dado sintetico' > "$temporary/source/sub/data.txt"
    bash "$ROOT/backup_versionado.sh" \
        "$temporary/source" "$temporary/repository" test > "$temporary/backup.out"
    local archive checksum
    archive=$(sed -n 's/^archive=//p' "$temporary/backup.out")
    checksum=$(sed -n 's/^checksum=//p' "$temporary/backup.out")
    [[ -f $archive && -f $checksum ]]
    (cd -- "$(dirname -- "$checksum")" && sha256sum -c "$(basename -- "$checksum")") >/dev/null
    tar -C "$temporary/restore" -xzf "$archive"
    cmp -- "$temporary/source/sub/data.txt" "$temporary/restore/sub/data.txt"
    pass 'backup, checksum e restauracao'
}

test_diagnostic_comparator() {
    printf '%s\n' \
        'schema=linux-course-diagnostic/v1' \
        'timestamp_utc=2026-10-11T10:00:00Z' \
        'kernel=6.12.0' \
        'uid=1000' > "$temporary/before.txt"
    printf '%s\n' \
        'schema=linux-course-diagnostic/v1' \
        'timestamp_utc=2026-10-11T11:00:00Z' \
        'kernel=6.18.0' \
        'uid=1000' \
        'root_filesystem=ext4' > "$temporary/after.txt"

    python3 "$ROOT/comparar_diagnosticos.py" \
        "$temporary/before.txt" "$temporary/after.txt" > "$temporary/diff.out"
    assert_contains "$temporary/diff.out" 'differences=2'
    assert_contains "$temporary/diff.out" 'added=1'
    assert_contains "$temporary/diff.out" 'changed=1'
    assert_contains "$temporary/diff.out" '+ root_filesystem=ext4'
    assert_contains "$temporary/diff.out" '~ kernel: 6.12.0 -> 6.18.0'

    local status=0
    python3 "$ROOT/comparar_diagnosticos.py" --fail-on-change \
        "$temporary/before.txt" "$temporary/after.txt" >/dev/null || status=$?
    [[ $status -eq 1 ]]

    printf '%s\n' 'bad line' > "$temporary/invalid.txt"
    status=0
    python3 "$ROOT/comparar_diagnosticos.py" \
        "$temporary/invalid.txt" "$temporary/after.txt" >/dev/null 2>&1 || status=$?
    [[ $status -eq 2 ]]
    pass 'comparador de diagnosticos'
}

compile_c() {
    local source=$1 output=$2
    cc -std=c17 -Wall -Wextra -Wpedantic -Werror "$source" -o "$output"
}

test_c() {
    if ! command -v cc >/dev/null 2>&1; then
        printf '[SKIP] compilador C ausente\n'
        return
    fi

    compile_c "$ROOT/c/processos.c" "$temporary/processos"
    "$temporary/processos" > "$temporary/processos.out"
    assert_contains "$temporary/processos.out" 'child_message=ola-do-filho'
    assert_contains "$temporary/processos.out" 'child_exit=7'

    compile_c "$ROOT/c/memoria.c" "$temporary/memoria"
    "$temporary/memoria" 2 > "$temporary/memoria.out"
    assert_contains "$temporary/memoria.out" 'allocated_bytes=2097152'
    assert_contains "$temporary/memoria.out" 'last_byte=1'

    compile_c "$ROOT/c/syscalls.c" "$temporary/syscalls"
    printf '%s\n' 'copiar por syscalls' > "$temporary/input.txt"
    "$temporary/syscalls" "$temporary/input.txt" "$temporary/output.txt" > "$temporary/syscalls.out"
    cmp -- "$temporary/input.txt" "$temporary/output.txt"
    assert_contains "$temporary/syscalls.out" 'bytes_copied=20'
    pass 'processos, memoria e syscalls em C'
}

test_systemd_units() {
    if command -v systemd-analyze >/dev/null 2>&1; then
        local staged_dir="$temporary/systemd"
        local staged_script="$staged_dir/curso-observador"
        mkdir -p -- "$staged_dir"
        cp -- "$ROOT/systemd/curso-observador" "$staged_script"
        chmod 0755 -- "$staged_script"
        sed "s|^ExecStart=.*|ExecStart=$staged_script|" \
            "$ROOT/systemd/curso-observador.service" > "$staged_dir/curso-observador.service"
        cp -- "$ROOT/systemd/curso-observador.timer" "$staged_dir/curso-observador.timer"
        if ! systemd-analyze verify \
            "$staged_dir/curso-observador.service" \
            "$staged_dir/curso-observador.timer" 2> "$temporary/systemd.err"; then
            if grep -Evq \
                '^(Failed to turn off SO_PASSRIGHTS|Failed to enable SO_PASSCRED)' \
                "$temporary/systemd.err"; then
                cat "$temporary/systemd.err" >&2
                return 1
            fi
            printf '[SKIP] sockets de credenciais do systemd restritos pelo sandbox\n'
        fi
        pass 'unidades systemd'
    else
        printf '[SKIP] systemd-analyze ausente\n'
    fi
}

test_shell_syntax() {
    local script
    for script in "$ROOT"/*.sh "$ROOT/systemd/curso-observador"; do
        bash -n "$script"
    done
    if command -v shellcheck >/dev/null 2>&1; then
        shellcheck "$ROOT"/*.sh "$ROOT/systemd/curso-observador"
    else
        printf '[SKIP] ShellCheck ausente\n'
    fi
    pass 'sintaxe dos scripts'
}

test_files
test_diagnostic
test_awk
test_backup
test_diagnostic_comparator
test_c
test_systemd_units
test_shell_syntax

printf '\n[OK] %d grupos de testes aprovados\n' "$pass_count"
