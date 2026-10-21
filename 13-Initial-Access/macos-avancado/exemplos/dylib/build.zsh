#!/bin/zsh
set -eu

if (( $# != 1 )); then
    print -u2 'uso: build.zsh DIRETORIO-DE-SAIDA-NOVO'
    exit 2
fi

output=${1:A}
if [[ -e $output ]]; then
    print -u2 'o diretório de saída já existe'
    exit 2
fi
mkdir -m 700 "$output"

script_dir=${0:A:h}
xcrun clang -std=c17 -Wall -Wextra -Wpedantic -Werror -fvisibility=hidden \
    -dynamiclib -install_name '@rpath/librte_math.dylib' \
    "$script_dir/rte_math.c" -o "$output/librte_math.dylib"
xcrun clang -std=c17 -Wall -Wextra -Wpedantic -Werror \
    "$script_dir/dylib_consumer.c" -o "$output/dylib_consumer"

"$output/dylib_consumer"
