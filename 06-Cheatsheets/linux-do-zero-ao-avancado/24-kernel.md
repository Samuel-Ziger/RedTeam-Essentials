# 24 — Kernel, syscalls e subsistemas

## Objetivos

- acompanhar uma operação da biblioteca até syscall, subsistema e driver;
- explicar scheduler, memória, VFS, bloco, dispositivos e segurança como partes;
- distinguir interfaces estáveis de user space e APIs internas do kernel;
- observar comportamento com a ferramenta de menor privilégio e overhead útil.

## Responsabilidade do kernel

O kernel multiplexa hardware entre cargas e impõe fronteiras. Seus subsistemas
principais incluem:

- scheduler e ciclo de vida de tarefas;
- gerenciamento de memória;
- VFS e filesystems;
- block layer e I/O;
- pilha de rede;
- IPC;
- drivers e device model;
- namespaces e cgroups;
- criptografia;
- Linux Security Modules;
- tracing, auditoria e performance counters.

## System calls

Uma syscall faz transição controlada para uma operação do kernel. Funções de
biblioteca podem envolver zero, uma ou várias syscalls. `printf()` normalmente
bufferiza em user space e mais tarde chama `write()`.

```bash
strace -e trace=openat,read,write,close cat /etc/hostname
```

Argumentos entram conforme a ABI da arquitetura; retorno negativo é convertido
pela libc em `-1` e `errno` quando aplicável. A lista/número de syscalls varia
por arquitetura, embora APIs de alto nível sejam mais portáveis.

O exemplo `exemplos/c/syscalls.c` usa `open`, `read`, `write` e `close` com
tratamento de leitura parcial e `EINTR`.

## Scheduler

O scheduler escolhe tarefas executáveis por CPU considerando classe, prioridade,
afinidade, fairness e topologia. Cargas normais usam uma classe de tempo
compartilhado; classes de tempo real e deadline exigem análise rigorosa.

```bash
chrt -p "$$"
taskset -pc "$$"
cat /proc/schedstat | head
```

Preempção, tick e configuração do kernel alteram latência. Mais context
switches não são automaticamente ruins; interprete com workload e fila.

## Memória no kernel

O subsistema MM gerencia page tables, fault, anonymous memory, page cache,
reclaim, swap, NUMA e alocadores. O buddy allocator fornece páginas; SLUB/SLAB
mantêm caches de objetos. Memória do kernel também é contabilizada em cgroups
modernos.

```bash
grep -E '^(Slab|SReclaimable|SUnreclaim|PageTables|KernelStack)' /proc/meminfo
sudo slabtop -o 2>/dev/null | head
```

## VFS

VFS usa objetos conceituais como superblock, inode, dentry e file para oferecer
interface uniforme. O page cache associa páginas a arquivos; dirty pages são
escritas posteriormente conforme política e fsync.

`write()` concluído não garante persistência em mídia. `fsync()` pede
durabilidade conforme garantias do filesystem/dispositivo, mas aplicações
também precisam ordenar arquivo, rename e diretório corretamente.

## I/O e block layer

Requisições passam por filas e drivers. Schedulers de I/O (`none`, `mq-deadline`,
`bfq` etc.) dependem de dispositivo e carga.

```bash
for scheduler in /sys/block/*/queue/scheduler; do
    printf '%s: ' "$scheduler"
    cat "$scheduler"
done
```

Não escolha por nome: SSD NVMe, HDD e storage virtual possuem filas e latência
diferentes.

## Subsistemas não aprofundados aqui

O kernel também implementa a pilha de conectividade, netfilter e interfaces
usadas por sockets. Este capítulo apenas reconhece essa responsabilidade.
Filas, protocolos, roteamento e processamento de pacotes pertencem aos módulos
14 a 18, onde poderão ser ligados corretamente a enlace e infraestrutura.

## Interrupções, exceções e trabalho adiado

Interrupção sinaliza evento externo; exceção ocorre por instrução/estado da CPU,
como page fault; syscall é entrada intencional. O kernel divide trabalho entre
contextos imediato e adiado (softirq, tasklet legado, workqueue, threads).

```bash
cat /proc/interrupts | head
ps -e -o pid,psr,comm | grep '^ *[0-9].*\[' | head
```

## Concorrência interna

Spinlocks, mutexes, atomics, per-CPU data, seqlocks e RCU atendem padrões
diferentes. Código em contexto atômico não pode dormir. RCU permite leituras
baratas com atualização e período de graça; não significa ausência de
sincronização.

## Linux Security Modules

LSM oferece hooks para SELinux, AppArmor, Smack, Landlock e outros. Módulos
podem coexistir conforme configuração e stacking suportado.

```bash
cat /sys/kernel/security/lsm 2>/dev/null
cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null
```

Seccomp filtra syscalls; capabilities quebram privilégios; lockdown restringe
interfaces quando a integridade do kernel exige. São mecanismos distintos.

## Configuração e ABI

```bash
zcat /proc/config.gz 2>/dev/null | head ||
    grep '^CONFIG_' "/boot/config-$(uname -r)" | head
```

Opções `CONFIG_*` podem ser built-in (`y`), módulo (`m`) ou ausentes. O kernel
busca estabilidade da ABI de user space; interfaces internas de módulos não
possuem a mesma promessa. Módulo externo precisa ser reconstruído/validado para
o kernel da distro.

## Interfaces administrativas

- syscalls e netlink: interfaces programáticas;
- `/proc` e `/sys`: pseudo-filesystems;
- `sysctl`: visão de parte de `/proc/sys`;
- ioctl: comandos associados a descritores/dispositivos;
- tracefs/debugfs: observação e debug, não API estável geral.

Não escreva em `debugfs`, sysfs ou sysctl experimental por tentativa. Consulte
a documentação da release em execução.

## Exercícios

1. Trace o exemplo de syscalls e associe cada chamada a uma linha do código,
   incluindo retorno, erro possível e descritor afetado.
2. Desenhe o caminho de uma leitura que acerta o page cache e outra que exige
   I/O, indicando onde a aplicação recupera controle.
3. Compare configuração embutida, módulo e opção ausente em três itens do
   kernel em execução.
4. Escolha entre log, strace, perf e tracepoint para quatro perguntas e
   justifique privilégio, detalhe, overhead e risco de dados sensíveis.

## Checklist de domínio

Consigo acompanhar uma leitura de arquivo, alocação e envio de pacote pelos
subsistemas, diferenciando biblioteca, syscall, VFS, driver e hardware.
