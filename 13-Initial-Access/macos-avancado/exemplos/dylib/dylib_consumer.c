#include <dlfcn.h>
#include <stdio.h>
#include <string.h>

typedef int (*rte_add_fn)(int, int);
typedef unsigned int (*rte_api_version_fn)(void);

static int load_symbol(void *library, const char *name, void *target, size_t target_size) {
    void *symbol;
    const char *error;

    (void)dlerror();
    symbol = dlsym(library, name);
    error = dlerror();
    if (error != NULL || symbol == NULL || target_size != sizeof(symbol)) {
        fprintf(stderr, "symbol_lookup_failed=%s\n", error == NULL ? name : error);
        return 0;
    }
    memcpy(target, &symbol, target_size);
    return 1;
}

int main(void) {
    void *library = dlopen("@loader_path/librte_math.dylib", RTLD_NOW | RTLD_LOCAL);
    rte_add_fn add;
    rte_api_version_fn api_version;

    if (library == NULL) {
        fprintf(stderr, "load_failed=%s\n", dlerror());
        return 2;
    }
    if (!load_symbol(library, "rte_add", &add, sizeof(add)) ||
        !load_symbol(library, "rte_api_version", &api_version, sizeof(api_version))) {
        (void)dlclose(library);
        return 3;
    }

    printf("api_version=%u\n", api_version());
    printf("sum=%d\n", add(19, 23));
    if (dlclose(library) != 0) {
        fprintf(stderr, "unload_failed=%s\n", dlerror());
        return 4;
    }
    return 0;
}
