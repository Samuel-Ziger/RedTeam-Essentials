#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <linux/kvm.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

int main(void)
{
    int fd = open("/dev/kvm", O_RDONLY | O_CLOEXEC);
    int version;
    int user_memory;

    printf("schema=rte-kvm-probe/v1\n");
    if (fd < 0) {
        printf("kvm_available=no\n");
        printf("reason=%s\n", strerror(errno));
        return 0;
    }
    version = ioctl(fd, KVM_GET_API_VERSION, 0);
    if (version < 0) {
        fprintf(stderr, "KVM_GET_API_VERSION: %s\n", strerror(errno));
        close(fd);
        return 1;
    }
    user_memory = ioctl(fd, KVM_CHECK_EXTENSION, KVM_CAP_USER_MEMORY);
    if (user_memory < 0) {
        fprintf(stderr, "KVM_CHECK_EXTENSION: %s\n", strerror(errno));
        close(fd);
        return 1;
    }
    printf("kvm_available=yes\n");
    printf("api_version=%d\n", version);
    printf("cap_user_memory=%d\n", user_memory);
    if (close(fd) != 0) {
        perror("close /dev/kvm");
        return 1;
    }
    return 0;
}
