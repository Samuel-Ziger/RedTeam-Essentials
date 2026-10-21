# 03 — ABI, syscalls, vDSO e ioctl

## Objetivos

- distinguir API fonte, ABI binária e UAPI do kernel;
- seguir uma syscall da libc ao kernel;
- entender retorno, `errno`, restart e cópia user/kernel;
- avaliar quando `ioctl` é apropriado.

## Camadas do contrato

Um programa geralmente chama um wrapper da libc. O wrapper organiza registradores
conforme a calling convention, executa a instrução de transição e converte
retorno negativo em `errno`. Número, registradores e instrução variam por ABI e
arquitetura.

Headers em `include/uapi/` e `arch/*/include/uapi/` são destinados a user space.
Estruturas internas fora dessa fronteira podem mudar. Compatibilidade de
processos 32-bit em kernel 64-bit pode exigir conversão de layout e ponteiros.

## Entrada e saída

O kernel não deve desreferenciar ponteiro de user space como ponteiro comum.
Rotinas como `copy_from_user()` e `copy_to_user()` tratam falhas e limites. O
retorno parcial faz parte da semântica de várias syscalls; um `read()` curto não
é necessariamente erro.

```c
ssize_t n;
do {
    n = read(fd, buffer, capacity);
} while (n < 0 && errno == EINTR);
```

Repetir cegamente operações com efeito colateral pode duplicá-las. Leia o
contrato específico.

## vDSO

Algumas operações, como obtenção de tempo em certas arquiteturas, podem ser
atendidas por código que o kernel mapeia no processo. A vDSO preserva a interface
sem pagar toda transição. Verifique o caminho real em vez de assumir:

```bash
grep -E '\[vdso\]|\[vvar\]' /proc/self/maps
strace -e clock_gettime date >/dev/null
```

Ausência no `strace` pode indicar vDSO, mas confirme com símbolos e medição.

## ioctl

`ioctl(fd, request, argument)` multiplexa comandos associados a um descritor.
Uma UAPI robusta reserva tamanhos, usa tipos de largura explícita, valida flags,
alinha estruturas e planeja extensão. Ponteiros, padding implícito e tipos como
`long` dificultam compatibilidade entre ABIs.

## Ferramentas

```bash
ausyscall --dump 2>/dev/null | head
strace -f -yy -e trace=%process,%file -- ./programa
readelf -Ws /lib*/libc.so.6 2>/dev/null | grep ' getpid@' | head
```

`strace` altera timing. Ele responde quais syscalls foram observadas, não prova
sozinho o caminho interno nem representa custo sem overhead.

## Contratos de compatibilidade

ABI inclui mais que número de syscall: calling convention, tamanho e alinhamento
de tipos, layout de estruturas, flags, códigos de erro e efeitos observáveis.
Uma UAPI publicada precisa continuar funcionando com binários já compilados.
Isso explica por que estruturas extensíveis carregam tamanho, campos reservados e
flags que devem ser zero quando desconhecidas.

Ao projetar uma interface, defina:

- unidade e largura de todo inteiro;
- alinhamento e endianness quando os bytes cruzam fronteiras;
- comportamento para flags desconhecidas;
- tamanho mínimo aceito e campos adicionados no fim;
- ownership de buffers e duração da validade;
- possibilidade de retorno parcial, interrupção e retry;
- compatibilidade de processos 32-bit.

`errno` descreve uma classe de falha no ponto da chamada; não substitui o
contexto da aplicação. Preserve o retorno original antes de executar outra
função que possa alterar `errno`. Para escrita parcial, avance o ponteiro e o
tamanho restante; repetir a operação inteira pode duplicar bytes.

## Como provar o caminho

Compare quatro camadas: chamada na fonte, símbolo da libc, instrução na
desmontagem e evento visto pelo tracer. `getpid()` pode ser cacheado por runtimes
antigos ou seguir caminho diferente; relógios podem usar vDSO. Um resultado
ausente no `strace` é pista, não prova suficiente. Inspecione
`AT_SYSINFO_EHDR`, símbolos da vDSO e binário real.

Para `ioctl`, decodifique direction, type, number e size quando a interface usa
macros `_IO*`. Valide também no kernel: tamanho codificado não garante que o
driver trate o argumento corretamente.

## Falhas comuns

- confundir API C com ABI do kernel;
- usar `long` ou ponteiro cru em estrutura persistente;
- repetir syscall com efeito colateral após `EINTR` sem consultar o contrato;
- tratar short I/O como EOF ou erro universal;
- medir custo de syscall sem separar vDSO e overhead do tracer.

## Prática A

Compile um programa que usa `openat`, `read`, `write` e `close`. Compare fonte,
desmontagem e trace. Localize os wrappers e as definições `SYSCALL_DEFINE` na
fonte correspondente. Registre divergências arquiteturais.

## Exercícios

1. Implemente funções `read_all` e `write_all` que tratem `EINTR`, retorno
   parcial e EOF sem loop infinito.
2. Compare a calling convention de uma syscall em x86-64 e AArch64 usando
   documentação da mesma versão.
3. Proponha uma estrutura de UAPI v1 extensível e teste rejeição de tamanho e
   flags desconhecidas.
4. Demonstre uma função atendida pela vDSO e documente as evidências usadas.

## Checklist de domínio

- [ ] Distingo API, ABI, UAPI, wrapper da libc e implementação interna.
- [ ] Trato retorno parcial e `EINTR` conforme o contrato específico.
- [ ] Proponho layouts compatíveis entre versões e ABIs.
- [ ] Não interpreto ausência no `strace` como prova isolada.
- [ ] Explico por que inserir campo no meio de um `ioctl` quebra binários.

Fonte: [Linux syscall user dispatch e UAPI](https://docs.kernel.org/userspace-api/index.html).
