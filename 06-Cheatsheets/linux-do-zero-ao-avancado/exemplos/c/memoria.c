#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <unistd.h>

static int parse_mebibytes(const char *text, size_t *result) {
    char *end = NULL;
    errno = 0;
    unsigned long value = strtoul(text, &end, 10);
    if (errno != 0 || end == text || *end != '\0' || value == 0UL || value > 64UL) {
        return -1;
    }
    *result = (size_t)value;
    return 0;
}

static long minor_faults(void) {
    struct rusage usage;
    if (getrusage(RUSAGE_SELF, &usage) == -1) {
        return -1L;
    }
    return usage.ru_minflt;
}

int main(int argc, char **argv) {
    size_t mebibytes = 8U;
    if (argc > 2 || (argc == 2 && parse_mebibytes(argv[1], &mebibytes) == -1)) {
        fprintf(stderr, "uso: %s [MIB_ENTRE_1_E_64]\n", argv[0]);
        return 2;
    }

    long page_size_value = sysconf(_SC_PAGESIZE);
    if (page_size_value <= 0L) {
        fputs("nao foi possivel obter o tamanho de pagina\n", stderr);
        return EXIT_FAILURE;
    }
    size_t page_size = (size_t)page_size_value;
    if (mebibytes > SIZE_MAX / (1024U * 1024U)) {
        fputs("tamanho excede o limite\n", stderr);
        return EXIT_FAILURE;
    }
    size_t bytes = mebibytes * 1024U * 1024U;

    long before = minor_faults();
    unsigned char *memory = calloc(bytes, 1U);
    if (memory == NULL) {
        perror("calloc");
        return EXIT_FAILURE;
    }
    long after_reserve = minor_faults();

    for (size_t offset = 0U; offset < bytes; offset += page_size) {
        memory[offset] = (unsigned char)(offset / page_size);
    }
    memory[bytes - 1U] = 1U;
    long after_touch = minor_faults();

    printf("pid=%ld\n", (long)getpid());
    printf("page_size=%zu\n", page_size);
    printf("allocated_bytes=%zu\n", bytes);
    printf("minor_faults_before=%ld\n", before);
    printf("minor_faults_after_reserve=%ld\n", after_reserve);
    printf("minor_faults_after_touch=%ld\n", after_touch);
    printf("last_byte=%u\n", (unsigned int)memory[bytes - 1U]);

    free(memory);
    return EXIT_SUCCESS;
}
