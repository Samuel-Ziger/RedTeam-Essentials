#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int safe_token(const char *value) {
    size_t i;
    if (value == NULL || value[0] == '\0') return 0;
    if (strlen(value) > 512U) return 0;
    for (i = 0; value[i] != '\0'; i++) {
        const char c = value[i];
        if (!((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') ||
              (c >= '0' && c <= '9') || c == '_' || c == '-')) return 0;
    }
    return 1;
}

static void fail(const char *message) {
    fprintf(stderr, "%s\n", message);
    exit(2);
}

int main(int argc, char **argv) {
    long limit = -1;
    const char *after = NULL;
    const char *status = NULL;
    char *end = NULL;
    int seen_limit = 0;
    int seen_after = 0;
    int seen_status = 0;
    int i;

    for (i = 1; i < argc; i += 2) {
        if (i + 1 >= argc) fail("valor ausente");
        if (strcmp(argv[i], "--limit") == 0) {
            if (seen_limit) fail("argumento repetido");
            seen_limit = 1;
            errno = 0;
            limit = strtol(argv[i + 1], &end, 10);
            if (errno == ERANGE || *argv[i + 1] == '\0' || *end != '\0') fail("limit invalido");
        } else if (strcmp(argv[i], "--after") == 0) {
            if (seen_after) fail("argumento repetido");
            seen_after = 1;
            after = argv[i + 1];
        } else if (strcmp(argv[i], "--status") == 0) {
            if (seen_status) fail("argumento repetido");
            seen_status = 1;
            status = argv[i + 1];
        } else {
            fail("argumento desconhecido");
        }
    }
    if (limit < 1 || limit > 100) fail("limit invalido");
    if (after != NULL && !safe_token(after)) fail("after invalido");
    if (status != NULL && strcmp(status, "active") != 0 && strcmp(status, "archived") != 0) {
        fail("status invalido");
    }

    printf("GET /v1/items?limit=%ld", limit);
    if (after != NULL) printf("&after=%s", after);
    if (status != NULL) printf("&status=%s", status);
    putchar('\n');
    return 0;
}
