# Exemplos executáveis

Todos os exemplos são locais. O teste não usa privilégio, não altera cgroups,
não carrega eBPF ou módulo e não inicia VM.

Cada ferramenta emite uma linha `schema=rte-.../v1`. Esse campo permite que um
consumidor rejeite formato incompatível em vez de interpretar colunas por
posição. stdout contém dados; mensagens e falhas pertencem a stderr. Código de
saída diferente de zero invalida a coleta mesmo quando existe saída parcial.

## C de user space

| Arquivo | Demonstração |
|---------|--------------|
| [`elf_inspector.c`](c/elf_inspector.c) | leitura defensiva do ELF header |
| [`proc_snapshot.c`](c/proc_snapshot.c) | parser pequeno de `/proc/PID/status` |
| [`page_faults.c`](c/page_faults.c) | materialização de páginas e faults |
| [`kvm_probe.c`](c/kvm_probe.c) | consulta somente leitura da API KVM |
| [`seccomp_demo.c`](c/seccomp_demo.c) | filtro local que retorna `EPERM` |

Compile individualmente:

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  c/elf_inspector.c -o elf-inspector
./elf-inspector ./elf-inspector
```

Use diretório de build descartável e trate os programas como instrumentos
didáticos, não como coletores universais. `proc_snapshot` aceita apenas o
escopo implementado; `page_faults` possui limite de entrada; `kvm_probe`
consulta a API sem criar VM; `seccomp_demo` restringe somente o próprio
processo filho e não muda política global.

## Shell e systemd

- [`pressure_report.sh`](pressure_report.sh) produz snapshot sem identificadores;
- [`kernel_config_diff.sh`](kernel_config_diff.sh) compara opções resolvidas;
- [`reproducible_archive.sh`](reproducible_archive.sh) cria tar determinístico;
- [`rte-observer.service`](systemd/rte-observer.service) demonstra hardening e
  resource control;
- [`rte-observer`](systemd/rte-observer) é o processo local da unidade.

Os scripts recusam entradas ausentes ou inválidas antes de alterar saída. O
archive usa ordem, ownership e mtime normalizados; isso demonstra uma parte de
reprodutibilidade, não substitui pin de toolchain e dependências. A unit deve ser
validada com `systemd-analyze verify` antes de ser copiada para uma VM.

## Fontes privilegiadas não automáticas

- [`exec_counter.bpf.c`](bpf/exec_counter.bpf.c) exige clang, libbpf, BTF e loader;
- [`rte_seqfile.c`](kernel/rte_seqfile.c) exige headers correspondentes e VM.

Esses arquivos devem ser revisados, compilados e carregados manualmente somente
nos laboratórios C/D. O repositório nunca automatiza a carga.

Antes de carregar o módulo, compare headers, `uname -r` e vermagic e mantenha
console. Antes de anexar BPF, inspecione ELF/BTF, limite duração e prepare
rollback de falha parcial. Ambos precisam de inventário antes/depois para provar
cleanup. Nunca relaxe política do host para fazer o exemplo funcionar.

## Testes

```bash
bash tests/test_examples.sh
```

A suíte compila C com warnings como erro, verifica schemas e limites, compara
dois archives, valida a unit quando systemd está disponível e faz análise
estática das fontes privilegiadas. Ela deliberadamente não testa:

- instalação de kernel ou módulo;
- carga de programa BPF;
- mudanças em boot, cgroup ou Device Mapper;
- inicialização de QEMU;
- comportamento real-time;
- interfaces ou tráfego de rede.

Essas fronteiras são avaliadas nos laboratórios com snapshot, console, evidência
e cleanup. Um `[SKIP]` por ferramenta ausente deve ser registrado; não equivale
a cobertura executada.

## Como estender um exemplo

1. Preserve o schema ou incremente a versão quando quebrar o contrato.
2. Valide tamanho, formato e range antes de alocar ou abrir.
3. Trate short I/O, `EINTR` e cleanup em todo caminho de erro.
4. Não adicione hostname, endereço, serial, token ou dado pessoal à saída.
5. Crie teste que falha antes da mudança e passa depois.
6. Mantenha execução automática sem privilégio e sem rede.
