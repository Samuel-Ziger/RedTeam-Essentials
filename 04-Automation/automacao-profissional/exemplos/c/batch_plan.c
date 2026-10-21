#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 64
#define MAX_INPUT 1024

static int compare(const void *left, const void *right) {
    return strcmp(*(const char *const *)left, *(const char *const *)right);
}

static int valid(const char *value) {
    if (*value == '\0') return 0;
    for (; *value; value++) {
        char c = *value;
        if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
              (c >= '0' && c <= '9') || c == '_' || c == '-')) return 0;
    }
    return 1;
}

int main(int argc, char **argv) {
    const char *raw = NULL;
    const char *format = "text";
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--items") == 0 && i + 1 < argc) raw = argv[++i];
        else if (strcmp(argv[i], "--format") == 0 && i + 1 < argc) format = argv[++i];
        else { fputs("error: argumento invalido\n", stderr); return 2; }
    }
    if (raw == NULL || strlen(raw) >= MAX_INPUT || raw[0] == ',' ||
        raw[strlen(raw) - 1] == ',' || strstr(raw, ",,") != NULL) {
        fputs("error: items invalido\n", stderr); return 2;
    }
    char buffer[MAX_INPUT];
    (void)snprintf(buffer, sizeof(buffer), "%s", raw);
    char *items[MAX_ITEMS];
    size_t count = 0;
    for (char *token = strtok(buffer, ","); token; token = strtok(NULL, ",")) {
        if (!valid(token) || count == MAX_ITEMS) { fputs("error: ID invalido\n", stderr); return 2; }
        items[count++] = token;
    }
    if (count == 0) { fputs("error: lista vazia\n", stderr); return 2; }
    qsort(items, count, sizeof(*items), compare);
    size_t unique = 0;
    for (size_t i = 0; i < count; i++) if (i == 0 || strcmp(items[i], items[i - 1]) != 0) items[unique++] = items[i];
    if (strcmp(format, "json") == 0) {
        printf("{\"count\":%zu,\"items\":[", unique);
        for (size_t i = 0; i < unique; i++) printf("%s\"%s\"", i ? "," : "", items[i]);
        puts("]}");
    } else if (strcmp(format, "text") == 0) {
        printf("count=%zu items=", unique);
        for (size_t i = 0; i < unique; i++) printf("%s%s", i ? "," : "", items[i]);
        putchar('\n');
    } else { fputs("error: format invalido\n", stderr); return 2; }
    return 0;
}
