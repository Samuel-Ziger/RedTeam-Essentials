#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

static int copy_all(int source, int destination, size_t *total) {
    unsigned char buffer[4096];
    *total = 0U;
    for (;;) {
        ssize_t count = read(source, buffer, sizeof(buffer));
        if (count == 0) {
            return 0;
        }
        if (count < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }

        ssize_t offset = 0;
        while (offset < count) {
            ssize_t written = write(destination, buffer + offset, (size_t)(count - offset));
            if (written < 0) {
                if (errno == EINTR) {
                    continue;
                }
                return -1;
            }
            offset += written;
        }
        *total += (size_t)count;
    }
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "uso: %s ORIGEM NOVO-DESTINO\n", argv[0]);
        return 2;
    }

    int source = open(argv[1], O_RDONLY | O_CLOEXEC);
    if (source == -1) {
        perror("open origem");
        return EXIT_FAILURE;
    }

    int destination = open(argv[2], O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0600);
    if (destination == -1) {
        perror("open destino");
        (void)close(source);
        return EXIT_FAILURE;
    }

    size_t total = 0U;
    int result = copy_all(source, destination, &total);
    int saved_errno = errno;
    if (close(source) == -1 && result == 0) {
        result = -1;
        saved_errno = errno;
    }
    if (close(destination) == -1 && result == 0) {
        result = -1;
        saved_errno = errno;
    }
    if (result == -1) {
        errno = saved_errno;
        perror("copiar");
        (void)unlink(argv[2]);
        return EXIT_FAILURE;
    }

    printf("bytes_copied=%zu\n", total);
    return EXIT_SUCCESS;
}
