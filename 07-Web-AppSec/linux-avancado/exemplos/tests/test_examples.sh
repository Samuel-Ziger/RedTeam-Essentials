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

assert_line() {
    local file=$1 expected=$2
    if ! grep -Fqx -- "$expected" "$file"; then
        printf '[FAIL] expected in %s: %s\n' "$file" "$expected" >&2
        return 1
    fi
}

compile_c() {
    local source=$1 output=$2
    cc -std=c17 -Wall -Wextra -Wpedantic -Werror "$source" -o "$output"
}

test_c_portable() {
    if ! command -v cc >/dev/null 2>&1; then
        printf '[SKIP] C compiler unavailable\n'
        return
    fi

    compile_c "$ROOT/c/elf_inspector.c" "$temporary/elf-inspector"
    "$temporary/elf-inspector" "$temporary/elf-inspector" > "$temporary/elf.out"
    assert_line "$temporary/elf.out" 'schema=rte-elf/v1'
    grep -Eq '^elf_class=(32|64)$' "$temporary/elf.out"
    grep -Eq '^entry=0x[0-9a-f]+$' "$temporary/elf.out"

    compile_c "$ROOT/c/proc_snapshot.c" "$temporary/proc-snapshot"
    "$temporary/proc-snapshot" > "$temporary/proc.out"
    assert_line "$temporary/proc.out" 'schema=rte-proc/v1'
    grep -Eq '^pid=[0-9]+$' "$temporary/proc.out"
    grep -Eq '^Threads=[0-9]+$' "$temporary/proc.out"

    compile_c "$ROOT/c/page_faults.c" "$temporary/page-faults"
    "$temporary/page-faults" 2 > "$temporary/faults.out"
    assert_line "$temporary/faults.out" 'schema=rte-page-faults/v1'
    assert_line "$temporary/faults.out" 'allocated_bytes=2097152'
    grep -Eq '^minor_fault_delta=[0-9]+$' "$temporary/faults.out"
    pass 'portable C examples'
}

test_linux_c() {
    if ! command -v cc >/dev/null 2>&1; then
        return
    fi

    if [[ -r /usr/include/linux/kvm.h ]]; then
        compile_c "$ROOT/c/kvm_probe.c" "$temporary/kvm-probe"
        "$temporary/kvm-probe" > "$temporary/kvm.out"
        assert_line "$temporary/kvm.out" 'schema=rte-kvm-probe/v1'
        grep -Eq '^kvm_available=(yes|no)$' "$temporary/kvm.out"
    else
        printf '[SKIP] Linux KVM headers unavailable\n'
    fi

    if [[ -r /usr/include/linux/seccomp.h && -r /usr/include/linux/filter.h ]]; then
        compile_c "$ROOT/c/seccomp_demo.c" "$temporary/seccomp-demo"
        "$temporary/seccomp-demo" > "$temporary/seccomp.out"
        assert_line "$temporary/seccomp.out" 'schema=rte-seccomp/v1'
        assert_line "$temporary/seccomp.out" 'getppid_result=-1'
        assert_line "$temporary/seccomp.out" 'getppid_errno=1'
    else
        printf '[SKIP] Linux seccomp headers unavailable\n'
    fi
    pass 'Linux API C examples'
}

test_pressure() {
    bash "$ROOT/pressure_report.sh" > "$temporary/pressure.out"
    assert_line "$temporary/pressure.out" 'schema=rte-pressure/v1'
    grep -Eq '^kernel=.+$' "$temporary/pressure.out"
    grep -Eq '^mem.MemTotal_kib=[0-9]+$' "$temporary/pressure.out"
    if grep -Eq '^(hostname|ip|mac|serial)=' "$temporary/pressure.out"; then
        printf '[FAIL] pressure report exposed avoidable identifier\n' >&2
        return 1
    fi
    pass 'read-only pressure report'
}

test_config_diff() {
    printf '%s\n' 'CONFIG_ALPHA=y' '# CONFIG_BETA is not set' > "$temporary/old.config"
    printf '%s\n' 'CONFIG_ALPHA=m' 'CONFIG_BETA=y' 'CONFIG_GAMMA=y' > "$temporary/new.config"
    bash "$ROOT/kernel_config_diff.sh" \
        "$temporary/old.config" "$temporary/new.config" > "$temporary/config.out"
    assert_line "$temporary/config.out" 'schema=rte-kconfig-diff/v1'
    assert_line "$temporary/config.out" 'changed.CONFIG_ALPHA=y->m'
    assert_line "$temporary/config.out" 'changed.CONFIG_BETA=n->y'
    assert_line "$temporary/config.out" 'added.CONFIG_GAMMA=y'
    pass 'kernel config diff'
}

test_reproducible_archive() {
    mkdir -p -- "$temporary/source/sub"
    printf '%s\n' alpha > "$temporary/source/a.txt"
    printf '%s\n' beta > "$temporary/source/sub/b.txt"
    touch -d '2020-01-01 00:00:00 UTC' "$temporary/source/a.txt"
    bash "$ROOT/reproducible_archive.sh" \
        "$temporary/source" "$temporary/one.tar" 1700000000 > "$temporary/one.out"
    touch -d '2025-01-01 00:00:00 UTC' "$temporary/source/a.txt"
    bash "$ROOT/reproducible_archive.sh" \
        "$temporary/source" "$temporary/two.tar" 1700000000 > "$temporary/two.out"
    cmp -- "$temporary/one.tar" "$temporary/two.tar"
    tar -tf "$temporary/one.tar" > "$temporary/tar.list"
    grep -Fqx './sub/b.txt' "$temporary/tar.list"
    pass 'reproducible archive'
}

test_systemd() {
    if ! command -v systemd-analyze >/dev/null 2>&1; then
        printf '[SKIP] systemd-analyze unavailable\n'
        return
    fi
    local staged="$temporary/systemd"
    mkdir -p -- "$staged"
    cp -- "$ROOT/systemd/rte-observer" "$staged/rte-observer"
    chmod 0755 "$staged/rte-observer"
    sed "s|^ExecStart=.*|ExecStart=$staged/rte-observer|" \
        "$ROOT/systemd/rte-observer.service" > "$staged/rte-observer.service"
    if ! systemd-analyze verify \
        "$staged/rte-observer.service" 2> "$temporary/systemd.err"; then
        if grep -Evq \
            '^(Failed to turn off SO_PASSRIGHTS|Failed to enable SO_PASSCRED)' \
            "$temporary/systemd.err"; then
            cat "$temporary/systemd.err" >&2
            return 1
        fi
        printf '[SKIP] systemd credential sockets restricted by sandbox\n'
    fi
    pass 'hardened systemd unit'
}

test_static_privileged_sources() {
    grep -Fq 'SEC("tp/sched/sched_process_exec")' "$ROOT/bpf/exec_counter.bpf.c"
    grep -Fq 'remove_proc_entry(RTE_ENTRY, NULL)' "$ROOT/kernel/rte_seqfile.c"
    if grep -R -Eq 'SEC\("(xdp|tc)|BPF_PROG_TYPE_(SOCKET|XDP|SCHED)' "$ROOT/bpf"; then
        printf '[FAIL] network BPF program found in network-free module\n' >&2
        return 1
    fi
    pass 'privileged sources remain local and non-automatic'
}

test_shell() {
    local script
    for script in "$ROOT"/*.sh "$ROOT/systemd/rte-observer"; do
        bash -n "$script"
    done
    if command -v shellcheck >/dev/null 2>&1; then
        shellcheck "$ROOT"/*.sh "$ROOT/systemd/rte-observer"
    else
        printf '[SKIP] ShellCheck unavailable\n'
    fi
    pass 'shell syntax and static analysis'
}

test_c_portable
test_linux_c
test_pressure
test_config_diff
test_reproducible_archive
test_systemd
test_static_privileged_sources
test_shell

printf '\n[OK] %d advanced Linux example groups passed\n' "$pass_count"
