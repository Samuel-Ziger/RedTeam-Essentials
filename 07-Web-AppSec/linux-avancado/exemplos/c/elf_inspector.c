#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { IDENT_SIZE = 16, HEADER_SIZE = 64 };

static uint16_t read_u16(const unsigned char *p, int little)
{
    if (little != 0) {
        return (uint16_t)((uint16_t)p[0] | ((uint16_t)p[1] << 8));
    }
    return (uint16_t)(((uint16_t)p[0] << 8) | (uint16_t)p[1]);
}

static uint64_t read_uint(const unsigned char *p, size_t width, int little)
{
    uint64_t value = 0;
    size_t i;

    for (i = 0; i < width; ++i) {
        size_t index = little != 0 ? width - 1U - i : i;
        value = (value << 8) | (uint64_t)p[index];
    }
    return value;
}

static int inspect(const char *path)
{
    unsigned char header[HEADER_SIZE];
    FILE *file = fopen(path, "rb");
    size_t count;
    int elf_class;
    int little;
    size_t entry_offset;
    size_t entry_width;

    if (file == NULL) {
        fprintf(stderr, "open %s: %s\n", path, strerror(errno));
        return 1;
    }
    count = fread(header, 1, sizeof(header), file);
    if (ferror(file) != 0) {
        fprintf(stderr, "read %s: %s\n", path, strerror(errno));
        fclose(file);
        return 1;
    }
    if (fclose(file) != 0) {
        fprintf(stderr, "close %s: %s\n", path, strerror(errno));
        return 1;
    }
    if (count < IDENT_SIZE || header[0] != 0x7fU || header[1] != 'E' ||
        header[2] != 'L' || header[3] != 'F') {
        fprintf(stderr, "%s: not an ELF file\n", path);
        return 2;
    }
    elf_class = header[4];
    little = header[5] == 1U;
    if ((elf_class != 1 && elf_class != 2) ||
        (header[5] != 1U && header[5] != 2U)) {
        fprintf(stderr, "%s: unsupported ELF class or byte order\n", path);
        return 2;
    }
    entry_offset = elf_class == 1 ? 24U : 24U;
    entry_width = elf_class == 1 ? 4U : 8U;
    if (count < entry_offset + entry_width) {
        fprintf(stderr, "%s: truncated ELF header\n", path);
        return 2;
    }

    printf("schema=rte-elf/v1\n");
    printf("elf_class=%d\n", elf_class == 1 ? 32 : 64);
    printf("endianness=%s\n", little != 0 ? "little" : "big");
    printf("type=%" PRIu16 "\n", read_u16(&header[16], little));
    printf("machine=%" PRIu16 "\n", read_u16(&header[18], little));
    printf("entry=0x%" PRIx64 "\n",
           read_uint(&header[entry_offset], entry_width, little));
    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s ELF_FILE\n", argv[0]);
        return 64;
    }
    return inspect(argv[1]);
}
