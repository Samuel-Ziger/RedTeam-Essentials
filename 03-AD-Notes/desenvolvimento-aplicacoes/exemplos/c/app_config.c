#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool valid_profile(const char *value) {
    return strcmp(value, "development") == 0 || strcmp(value, "testing") == 0 ||
           strcmp(value, "production") == 0;
}

static void help(void) {
    puts("Usage: app_config [--profile development|testing|production] [--format text|json]");
}

static int fail(const char *message, const char *value) {
    if (value == NULL) {
        fprintf(stderr, "error: %s\n", message);
    } else {
        fprintf(stderr, "error: %s: %s\n", message, value);
    }
    return 2;
}

int main(int argc, char **argv) {
    const char *profile = NULL;
    const char *source = NULL;
    const char *format = "text";

    for (int index = 1; index < argc; ++index) {
        if (strcmp(argv[index], "--help") == 0) {
            help();
            return 0;
        }
        if (strcmp(argv[index], "--profile") == 0) {
            if (++index == argc) {
                return fail("--profile exige um valor", NULL);
            }
            profile = argv[index];
            source = "cli";
        } else if (strcmp(argv[index], "--format") == 0) {
            if (++index == argc) {
                return fail("--format exige um valor", NULL);
            }
            format = argv[index];
        } else {
            return fail("opcao desconhecida", argv[index]);
        }
    }

    if (profile == NULL) {
        profile = getenv("APP_PROFILE");
        source = profile == NULL ? "default" : "environment";
        if (profile == NULL) {
            profile = "development";
        }
    }
    if (!valid_profile(profile)) {
        return fail("profile invalido", profile);
    }
    if (strcmp(format, "text") != 0 && strcmp(format, "json") != 0) {
        return fail("format invalido", format);
    }

    if (strcmp(format, "json") == 0) {
        printf("{\"profile\":\"%s\",\"source\":\"%s\"}\n", profile, source);
    } else {
        printf("profile=%s source=%s\n", profile, source);
    }
    return 0;
}
