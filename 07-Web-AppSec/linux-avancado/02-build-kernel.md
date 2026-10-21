# 02 — Kconfig, kbuild, compilação e cross-build

## Objetivos

- entender como Kconfig decide recursos e dependências;
- produzir builds fora da árvore de fontes;
- reduzir uma configuração sem perder recuperação;
- separar compilação nativa, cruzada e instalação.

## Kconfig

Cada opção pode ser booleana (`y/n`) ou tristate (`y/m/n`). `depends on`
controla visibilidade; `select` força outro símbolo e deve ser usado com cuidado;
`imply` é mais fraco. O `.config` resolvido é entrada do build, mas headers e
Makefiles gerados materializam a decisão.

Configurações úteis:

```bash
make O=build defconfig
make O=build olddefconfig
make O=build menuconfig
make O=build savedefconfig
scripts/diffconfig old.config new.config
```

`localmodconfig` observa módulos carregados e pode remover o driver necessário
para um cenário que não estava ativo. Nunca o use sem manter um kernel conhecido
e uma entrada de boot recuperável.

## Build fora da árvore

```bash
make O="$PWD/build" olddefconfig
make O="$PWD/build" -j"$(nproc)"
make O="$PWD/build" modules
```

Vantagens: fonte limpa, múltiplas configs simultâneas e remoção simples do
resultado. Registre compilador, linker, binutils, commit e `.config`.

## Reprodutibilidade

Datas, hostname, usuário e caminhos podem aparecer no artefato. Para um
experimento, normalize o ambiente:

```bash
export KBUILD_BUILD_TIMESTAMP='1970-01-01 00:00:00 UTC'
export KBUILD_BUILD_USER='student'
export KBUILD_BUILD_HOST='lab'
export SOURCE_DATE_EPOCH=0
```

Isso não prova reprodutibilidade sozinho. Faça dois builds em diretórios
distintos, compare hashes e use `diffoscope` quando divergirem.

## Cross-build

Para uma toolchain AArch64 instalada:

```bash
make O=build-arm64 ARCH=arm64 defconfig
make O=build-arm64 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j"$(nproc)"
```

`ARCH` escolhe o alvo no kernel; `CROSS_COMPILE` é o prefixo da toolchain. Isso
não cria automaticamente um root filesystem compatível.

## Instalação segura

Não execute `make install` no host. Na VM C, copie kernel, módulos e config com
um sufixo exclusivo, gere initramfs conforme a distribuição e mantenha a entrada
anterior como padrão até validar console, raiz e shutdown.

## Como uma opção chega ao binário

Kconfig calcula símbolos a partir de tipo, dependências, defaults e escolhas do
usuário. O resultado gera macros, Makefiles condicionais e, em alguns casos,
código alternativo. Portanto, comparar somente dois arquivos `.config` mostra
a intenção resolvida, mas não demonstra que o objeto foi linkado, que o módulo
foi instalado ou que o caminho foi exercitado.

Para uma opção relevante, siga a cadeia completa:

```text
prompt/dependências → valor em .config → macro gerada → objeto no Makefile
→ símbolo ou módulo no build → artefato instalado → evidência em runtime
```

`olddefconfig` aceita defaults para símbolos novos; isso é conveniente, mas
pode mudar a superfície entre releases. Guarde o diff após toda atualização.
`savedefconfig` registra um conjunto mínimo relativo aos defaults daquela
versão, não uma configuração universal.

## Validação por estágios

Separe falha de configuração, compilação, link, instalação, initramfs e boot.
Uma build bem-sucedida ainda pode não localizar a raiz. Antes de reiniciar,
confirme arquitetura, formato, módulos, dependências, espaço em `/boot`, entrada
nova e console. Depois do boot, compare `uname -r`, cmdline, config exposta,
módulos e journal; não aceite apenas a tela de login.

Cross-build valida geração de artefato para outra arquitetura, mas execução
precisa de firmware, DT/ACPI, rootfs, loader e user space compatíveis. Emulação
QEMU reduz a distância, porém não valida timings nem periféricos da placa real.

## Falhas comuns

- usar `select` como se verificasse todas as dependências do símbolo forçado;
- executar builds diferentes no mesmo diretório de saída;
- instalar módulos com release string que colide com o kernel anterior;
- reduzir config antes de inventariar recuperação, storage e console;
- comparar hashes sem normalizar caminho, timestamp e toolchain.

## Prática B/C

1. Gere `defconfig` em diretório separado.
2. Ative `DEBUG_INFO_DWARF5`, BTF e os tracepoints suportados.
3. Compile duas vezes com ambiente normalizado.
4. Compare `vmlinux`, config e logs.
5. Na VM, crie entrada de boot paralela; nunca substitua a única funcional.

## Exercícios

1. Escolha três símbolos e desenhe dependências, valor final, objeto produzido e
   como provar a presença de cada recurso em runtime.
2. Faça dois builds limpos em caminhos distintos; se os hashes divergirem,
   classifique a primeira diferença com `diffoscope`.
3. Remova de uma cópia da config somente um recurso não essencial, preveja o
   efeito e valide sem instalar no host.
4. Escreva um checklist pré-boot e um critério objetivo de rollback.

## Checklist de domínio

- [ ] Explico `depends on`, `select`, `imply` e tristate.
- [ ] Produzo builds fora da árvore com toolchain e config registradas.
- [ ] Distingo reprodutibilidade de duas compilações apenas parecidas.
- [ ] Nunca substituo o único kernel recuperável.
- [ ] Explico quando o driver da raiz deve estar embutido ou no initramfs.

Fonte: [Kbuild](https://docs.kernel.org/kbuild/index.html).
