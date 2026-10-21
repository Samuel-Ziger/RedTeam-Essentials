#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static int write_all(int descriptor, const char *buffer, size_t length) {
    while (length > 0U) {
        ssize_t written = write(descriptor, buffer, length);
        if (written < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        buffer += (size_t)written;
        length -= (size_t)written;
    }
    return 0;
}

int main(void) {
    int channel[2];
    if (pipe(channel) == -1) {
        perror("pipe");
        return EXIT_FAILURE;
    }

    pid_t child = fork();
    if (child == -1) {
        perror("fork");
        (void)close(channel[0]);
        (void)close(channel[1]);
        return EXIT_FAILURE;
    }

    if (child == 0) {
        const char message[] = "ola-do-filho";
        (void)close(channel[0]);
        if (write_all(channel[1], message, sizeof(message) - 1U) == -1) {
            (void)close(channel[1]);
            _exit(70);
        }
        (void)close(channel[1]);
        _exit(7);
    }

    (void)close(channel[1]);
    char buffer[64];
    size_t used = 0U;
    for (;;) {
        ssize_t count = read(channel[0], buffer + used, sizeof(buffer) - 1U - used);
        if (count == 0) {
            break;
        }
        if (count < 0) {
            if (errno == EINTR) {
                continue;
            }
            perror("read");
            (void)close(channel[0]);
            return EXIT_FAILURE;
        }
        used += (size_t)count;
        if (used == sizeof(buffer) - 1U) {
            break;
        }
    }
    (void)close(channel[0]);
    buffer[used] = '\0';

    int status = 0;
    if (waitpid(child, &status, 0) == -1) {
        perror("waitpid");
        return EXIT_FAILURE;
    }

    printf("parent_pid=%ld child_pid=%ld\n", (long)getpid(), (long)child);
    printf("child_message=%s\n", buffer);
    if (WIFEXITED(status)) {
        printf("child_exit=%d\n", WEXITSTATUS(status));
        return EXIT_SUCCESS;
    }
    fputs("child_exit=abnormal\n", stderr);
    return EXIT_FAILURE;
}
