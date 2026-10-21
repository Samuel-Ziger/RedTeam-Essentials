// SPDX-License-Identifier: GPL-2.0
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, __u64);
} exec_count SEC(".maps");

SEC("tp/sched/sched_process_exec")
int count_local_exec(void *context)
{
    __u32 key = 0;
    __u64 *value;

    (void)context;
    value = bpf_map_lookup_elem(&exec_count, &key);
    if (value != NULL) {
        __sync_fetch_and_add(value, 1);
    }
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
