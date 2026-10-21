#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

enum { LINE_SIZE = 512, PATH_SIZE = 64 };

static int valid_pid(const char *value)
{
    size_t i;

    if (value[0] == '\0') {
        return 0;
    }
    for (i = 0; value[i] != '\0'; ++i) {
        if (isdigit((unsigned char)value[i]) == 0) {
            return 0;
        }
    }
    return 1;
}

static void print_value(const char *key, char *value)
{
    size_t length = strlen(value);

    while (length > 0U && (value[length - 1U] == '\n' ||
                           value[length - 1U] == '\r')) {
        value[--length] = '\0';
    }
    while (*value == ' ' || *value == '\t') {
        ++value;
    }
    printf("%s=%s\n", key, value);
}

int main(int argc, char **argv)
{
    char pid_text[32];
    char path[PATH_SIZE];
    char line[LINE_SIZE];
    FILE *status;
    int found = 0;

    if (argc > 2) {
        fprintf(stderr, "usage: %s [PID]\n", argv[0]);
        return 64;
    }
    if (argc == 2) {
        if (valid_pid(argv[1]) == 0) {
            fprintf(stderr, "PID must contain only decimal digits\n");
            return 64;
        }
        if (snprintf(pid_text, sizeof(pid_text), "%s", argv[1]) >=
            (int)sizeof(pid_text)) {
            fprintf(stderr, "PID is too long\n");
            return 64;
        }
    } else {
        if (snprintf(pid_text, sizeof(pid_text), "%ld", (long)getpid()) >=
            (int)sizeof(pid_text)) {
            return 1;
        }
    }
    if (snprintf(path, sizeof(path), "/proc/%s/status", pid_text) >=
        (int)sizeof(path)) {
        return 1;
    }
    status = fopen(path, "r");
    if (status == NULL) {
        fprintf(stderr, "open %s: %s\n", path, strerror(errno));
        return 1;
    }

    printf("schema=rte-proc/v1\n");
    printf("pid=%s\n", pid_text);
    while (fgets(line, sizeof(line), status) != NULL) {
        char *separator = strchr(line, ':');
        if (separator == NULL) {
            continue;
        }
        *separator = '\0';
        if (strcmp(line, "Name") == 0 || strcmp(line, "State") == 0 ||
            strcmp(line, "Threads") == 0 || strcmp(line, "VmRSS") == 0) {
            print_value(line, separator + 1);
            ++found;
        }
    }
    if (ferror(status) != 0) {
        fprintf(stderr, "read %s: %s\n", path, strerror(errno));
        fclose(status);
        return 1;
    }
    if (fclose(status) != 0) {
        fprintf(stderr, "close %s: %s\n", path, strerror(errno));
        return 1;
    }
    return found >= 3 ? 0 : 1;
}
