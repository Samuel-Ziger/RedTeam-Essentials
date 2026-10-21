#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <unistd.h>

static int parse_mib(const char *text, size_t *bytes)
{
    char *end = NULL;
    unsigned long value;

    errno = 0;
    value = strtoul(text, &end, 10);
    if (errno != 0 || end == text || *end != '\0' || value == 0UL ||
        value > 512UL || value > SIZE_MAX / (1024UL * 1024UL)) {
        return -1;
    }
    *bytes = (size_t)value * 1024U * 1024U;
    return 0;
}

int main(int argc, char **argv)
{
    struct rusage before;
    struct rusage after;
    unsigned char *memory;
    size_t bytes = 16U * 1024U * 1024U;
    size_t page_size;
    size_t offset;
    unsigned long checksum = 0UL;
    long system_page_size;

    if (argc > 2 || (argc == 2 && parse_mib(argv[1], &bytes) != 0)) {
        fprintf(stderr, "usage: %s [MIB:1..512]\n", argv[0]);
        return 64;
    }
    system_page_size = sysconf(_SC_PAGESIZE);
    if (system_page_size <= 0) {
        fprintf(stderr, "sysconf(_SC_PAGESIZE) failed\n");
        return 1;
    }
    page_size = (size_t)system_page_size;
    memory = calloc(bytes, 1U);
    if (memory == NULL) {
        fprintf(stderr, "allocate %zu bytes: %s\n", bytes, strerror(errno));
        return 1;
    }
    if (getrusage(RUSAGE_SELF, &before) != 0) {
        perror("getrusage before");
        free(memory);
        return 1;
    }
    for (offset = 0; offset < bytes; offset += page_size) {
        memory[offset] = (unsigned char)(offset / page_size % 251U);
        checksum += memory[offset];
    }
    if (getrusage(RUSAGE_SELF, &after) != 0) {
        perror("getrusage after");
        free(memory);
        return 1;
    }
    printf("schema=rte-page-faults/v1\n");
    printf("allocated_bytes=%zu\n", bytes);
    printf("page_size=%zu\n", page_size);
    printf("minor_fault_delta=%ld\n", after.ru_minflt - before.ru_minflt);
    printf("major_fault_delta=%ld\n", after.ru_majflt - before.ru_majflt);
    printf("checksum=%lu\n", checksum);
    free(memory);
    return 0;
}
