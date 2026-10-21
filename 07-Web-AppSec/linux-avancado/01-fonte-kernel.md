# 01 — Árvore do kernel e leitura de código

## Objetivos

- navegar na árvore sem tentar lê-la linearmente;
- encontrar definição, implementação, chamadores e mantenedores;
- correlacionar fonte, configuração e binário em execução;
- distinguir mainline, stable, longterm e árvores de subsistema.

## A árvore

Diretórios centrais:

| Caminho | Papel |
|---------|-------|
| `arch/` | código dependente de arquitetura e entrada de syscalls |
| `block/` | camada genérica de I/O em bloco |
| `drivers/` | drivers por classe e barramento |
| `fs/` | VFS e implementações de filesystems |
| `include/` | headers internos, UAPI e gerados |
| `init/` | inicialização do kernel |
| `kernel/` | scheduler, sinais, locking, tracing e infraestrutura |
| `mm/` | memória virtual, allocators e reclaim |
| `security/` | LSM e políticas de integridade |
| `tools/` | perf, BPF, testes e utilitários |

O arquivo `MAINTAINERS` conecta caminho, mantenedor, lista, status e árvore. A
documentação em `Documentation/` deve ser lida no mesmo checkout do código.

## Estratégia de leitura

Comece por um comportamento observável, não por `start_kernel()`. Exemplo:

```bash
git grep -n 'SYSCALL_DEFINE.*getpid'
git grep -n 'struct task_struct' -- include kernel
git log -L :do_sys_openat2:fs/open.c
scripts/get_maintainer.pl -f fs/open.c
```

Fluxo recomendado:

1. encontre o ponto de entrada;
2. anote estruturas e invariantes;
3. abra apenas um nível de chamados por vez;
4. localize configurações `CONFIG_*` e caminhos condicionais;
5. leia o histórico do trecho e a discussão do patch;
6. valide no sistema com tracepoint ou teste pequeno.

## Fonte versus sistema ativo

O nome da release não prova que a distribuição usa a fonte vanilla. Fornecedores
aplicam backports. Guarde `uname -r`, identificador do pacote, config e, quando
disponível, commit ou SRPM/source package.

```bash
uname -r
modinfo -F vermagic module_name 2>/dev/null || true
grep -E 'CONFIG_(SMP|PREEMPT|BPF)=' /boot/config-"$(uname -r)" 2>/dev/null
```

## Símbolos e artefatos

`vmlinux` costuma conter símbolos e informação de depuração; `bzImage` ou
`Image` é o artefato de boot; `System.map` lista símbolos; módulos são objetos
ELF relocáveis. KASLR e restrições de `/proc/kallsyms` alteram o que user space
consegue observar.

## Navegação orientada por invariantes

Ao ler uma função, não transcreva cada linha. Registre entradas, estado protegido,
efeitos observáveis, erros e quem possui cada referência. Para um ponteiro,
pergunte onde nasce, qual lock ou protocolo protege seu lifetime e onde a última
referência é liberada. Para um campo, procure leitores e escritores; o nome da
estrutura sozinho raramente revela a regra de concorrência.

Macros escondem parte importante do fluxo. Expanda mentalmente uma
`SYSCALL_DEFINE`, confirme a declaração na UAPI e use o preprocessor somente
quando necessário. Chamadas indiretas por tabelas de operações exigem descobrir
qual implementação foi selecionada em runtime. Configuração, arquitetura e
static keys podem remover um caminho inteiro do binário.

O histórico responde perguntas que a fotografia atual não responde:

```bash
git blame -L START,END -- path/to/file.c
git show --stat --oneline COMMIT
git log --follow -- path/to/file.c
```

`blame` encontra o commit que tocou a linha, não a pessoa culpada. Leia a
mensagem, patches anteriores e discussão vinculada. Em árvores stable, um commit
pode ser backportado com outro identificador ou adaptado ao contexto antigo.

## Da fonte à observação

Uma hipótese de código precisa de ponte: símbolo, tracepoint, contador, teste de
autoverificação ou comportamento de UAPI. Antes de instrumentar função interna,
procure tracepoint estável e teste existente em `tools/testing/selftests`.
Compare config compilada com a ativa; encontrar código sob um `#ifdef` não
prova que ele exista no kernel executado.

## Falhas comuns

- ler a branch `master` enquanto a VM executa kernel downstream antigo;
- assumir que nome de símbolo implica o mesmo contrato entre versões;
- ignorar retorno de erro e caminhos de cleanup;
- seguir apenas o happy path, sem concorrência nem lifetime;
- usar offsets copiados de outra build.

## Prática A

No checkout correspondente à sua versão:

1. localize a implementação de `getpid`;
2. identifique o tipo retornado e a UAPI relacionada;
3. encontre o mantenedor do arquivo;
4. escolha um commit recente no mesmo trecho e resuma problema e trade-off;
5. desenhe o caminho da syscall até o retorno.

## Exercícios

1. Para uma função pequena, produza uma tabela com callers, callees, locks,
   configurações e códigos de erro.
2. Compare o mesmo trecho em mainline e na fonte da distribuição; marque
   backports e mudanças semânticas.
3. Localize o selftest mais próximo do subsistema e explique qual invariante ele
   verifica e qual permanece sem cobertura.
4. Escolha uma chamada indireta, identifique a tabela de operações e prove qual
   implementação a sua VM selecionou.

## Checklist de domínio

- [ ] Distingo mainline, stable, longterm, árvore de subsistema e downstream.
- [ ] Relaciono fonte, commit, config e artefato em execução.
- [ ] Encontro mantenedores e histórico sem atribuir culpa pelo `blame`.
- [ ] Analiso ownership, concorrência, erros e cleanup.
- [ ] Sei explicar por que offsets de `task_struct` de outra build são frágeis.

Fonte: [guia de desenvolvimento](https://docs.kernel.org/process/development-process.html).
