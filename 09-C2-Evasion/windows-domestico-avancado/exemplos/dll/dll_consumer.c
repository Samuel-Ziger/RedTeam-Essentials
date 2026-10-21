#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <stdio.h>
#include <string.h>
#include <wchar.h>

typedef int(__cdecl *rte_add_fn)(int, int);
typedef unsigned int(__cdecl *rte_api_version_fn)(void);

static int build_library_path(wchar_t *path, size_t capacity) {
    DWORD length = GetModuleFileNameW(NULL, path, (DWORD)capacity);
    wchar_t *separator;

    if (length == 0U || length >= capacity) {
        return 0;
    }
    separator = wcsrchr(path, L'\\');
    if (separator == NULL) {
        return 0;
    }
    separator[1] = L'\0';
    return wcscat_s(path, capacity, L"rte_math.dll") == 0;
}

int wmain(void) {
    wchar_t path[MAX_PATH];
    HMODULE library;
    FARPROC procedure;
    rte_add_fn add;
    rte_api_version_fn api_version;
    unsigned int version;

    if (!build_library_path(path, MAX_PATH)) {
        fwprintf(stderr, L"could_not_build_library_path\n");
        return 2;
    }

    library = LoadLibraryExW(
        path,
        NULL,
        LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_SYSTEM32
    );
    if (library == NULL) {
        fwprintf(stderr, L"load_failed=%lu\n", GetLastError());
        return 3;
    }

    procedure = GetProcAddress(library, "rte_add");
    if (procedure == NULL) {
        fprintf(stderr, "export_lookup_failed=%lu\n", GetLastError());
        FreeLibrary(library);
        return 4;
    }
    memcpy(&add, &procedure, sizeof(add));

    procedure = GetProcAddress(library, "rte_api_version");
    if (procedure == NULL) {
        fprintf(stderr, "export_lookup_failed=%lu\n", GetLastError());
        FreeLibrary(library);
        return 4;
    }
    memcpy(&api_version, &procedure, sizeof(api_version));

    version = api_version();
    printf("api_version=%u\n", version);
    if (version != 1U) {
        fprintf(stderr, "unsupported_api_version=%u\n", version);
        FreeLibrary(library);
        return 6;
    }
    printf("sum=%d\n", add(19, 23));

    if (!FreeLibrary(library)) {
        fprintf(stderr, "unload_failed=%lu\n", GetLastError());
        return 5;
    }
    return 0;
}
