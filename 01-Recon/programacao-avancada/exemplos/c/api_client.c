#define _POSIX_C_SOURCE 200112L

#include <errno.h>
#include <netdb.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <unistd.h>

enum { BUFFER_SIZE = 4096, MAX_RESPONSE_SIZE = 1024 * 1024 };

static int is_valid_endpoint(const char *host, const char *port) {
    size_t host_length = strlen(host);
    if (host_length == 0 || host_length > 253 ||
        (strcmp(host, "127.0.0.1") != 0 && strcmp(host, "localhost") != 0 &&
         strcmp(host, "::1") != 0)) {
        return 0;
    }
    for (size_t index = 0; index < host_length; index++) {
        unsigned char character = (unsigned char)host[index];
        if (character <= 0x20 || character == 0x7f) {
            return 0;
        }
    }

    char *end = NULL;
    errno = 0;
    long numeric_port = strtol(port, &end, 10);
    return errno == 0 && end != port && *end == '\0' &&
           numeric_port >= 1 && numeric_port <= 65535;
}

static int connect_to_localhost(const char *host, const char *port) {
    struct addrinfo hints = {0};
    struct addrinfo *addresses = NULL;
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    int status = getaddrinfo(host, port, &hints, &addresses);
    if (status != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(status));
        return -1;
    }

    int socket_fd = -1;
    for (const struct addrinfo *address = addresses; address != NULL;
         address = address->ai_next) {
        socket_fd = socket(address->ai_family, address->ai_socktype,
                           address->ai_protocol);
        if (socket_fd < 0) {
            continue;
        }
        struct timeval timeout = {.tv_sec = 3, .tv_usec = 0};
        if (setsockopt(socket_fd, SOL_SOCKET, SO_RCVTIMEO, &timeout,
                       sizeof timeout) != 0 ||
            setsockopt(socket_fd, SOL_SOCKET, SO_SNDTIMEO, &timeout,
                       sizeof timeout) != 0) {
            close(socket_fd);
            socket_fd = -1;
            continue;
        }
        if (connect(socket_fd, address->ai_addr, address->ai_addrlen) == 0) {
            break;
        }
        close(socket_fd);
        socket_fd = -1;
    }
    freeaddrinfo(addresses);
    return socket_fd;
}

static int send_all(int socket_fd, const char *data, size_t length) {
    size_t sent = 0;
    while (sent < length) {
        ssize_t result = send(socket_fd, data + sent, length - sent, 0);
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (result <= 0) {
            return -1;
        }
        sent += (size_t)result;
    }
    return 0;
}

static int read_response(int socket_fd) {
    char buffer[BUFFER_SIZE];
    char status_line[128] = {0};
    size_t total = 0;
    size_t status_length = 0;
    int status_complete = 0;

    for (;;) {
        ssize_t received = recv(socket_fd, buffer, sizeof buffer, 0);
        if (received < 0 && errno == EINTR) {
            continue;
        }
        if (received < 0) {
            perror("recv");
            return -1;
        }
        if (received == 0) {
            break;
        }
        total += (size_t)received;
        if (total > MAX_RESPONSE_SIZE) {
            fprintf(stderr, "resposta maior que o limite de 1 MB\n");
            return -1;
        }

        if (!status_complete) {
            for (ssize_t index = 0; index < received; index++) {
                char character = buffer[index];
                if (character == '\n') {
                    status_complete = 1;
                    break;
                }
                if (character != '\r' && status_length + 1 < sizeof status_line) {
                    status_line[status_length++] = character;
                }
            }
        }
        if (fwrite(buffer, 1, (size_t)received, stdout) != (size_t)received) {
            perror("fwrite");
            return -1;
        }
    }

    if (strncmp(status_line, "HTTP/1.1 200 ", 13) != 0 &&
        strncmp(status_line, "HTTP/1.0 200 ", 13) != 0) {
        fprintf(stderr, "status inesperado: %s\n", status_line);
        return -1;
    }
    if (!status_complete) {
        fprintf(stderr, "resposta terminou antes do fim da status line\n");
        return -1;
    }
    return 0;
}

int main(void) {
    const char *host = getenv("INVENTORY_HOST");
    const char *port = getenv("INVENTORY_PORT");
    host = host == NULL ? "127.0.0.1" : host;
    port = port == NULL ? "8101" : port;

    if (!is_valid_endpoint(host, port)) {
        fprintf(stderr, "host ou porta inválidos\n");
        return EXIT_FAILURE;
    }
    if (signal(SIGPIPE, SIG_IGN) == SIG_ERR) {
        perror("signal");
        return EXIT_FAILURE;
    }

    int socket_fd = connect_to_localhost(host, port);
    if (socket_fd < 0) {
        fprintf(stderr, "não foi possível conectar a %s:%s\n", host, port);
        return EXIT_FAILURE;
    }

    char request[512];
    const char *request_format = strchr(host, ':') == NULL
                                     ? "GET /health/live HTTP/1.1\r\n"
                                       "Host: %s:%s\r\n"
                                       "Accept: application/json\r\n"
                                       "User-Agent: rte-c-client/1\r\n"
                                       "Connection: close\r\n\r\n"
                                     : "GET /health/live HTTP/1.1\r\n"
                                       "Host: [%s]:%s\r\n"
                                       "Accept: application/json\r\n"
                                       "User-Agent: rte-c-client/1\r\n"
                                       "Connection: close\r\n\r\n";
    int length = snprintf(request, sizeof request, request_format, host, port);
    if (length < 0 || (size_t)length >= sizeof request) {
        fprintf(stderr, "request excedeu o buffer\n");
        close(socket_fd);
        return EXIT_FAILURE;
    }

    int result = send_all(socket_fd, request, (size_t)length);
    if (result == 0) {
        result = read_response(socket_fd);
    }
    close(socket_fd);
    return result == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
