# 11 — Processos, threads, jobs e sinais

## Objetivos

- explicar criação, substituição, espera e término de processos;
- interpretar árvore, estado, credenciais, descritores, limites e cgroup;
- usar sinais e job control sem confundir supervisão com segundo plano;
- distinguir processo, thread, zombie, órfão e serviço.

## Nascimento: fork, exec e wait

Conceitualmente, um processo cria outro com `fork()`/`clone()`; o filho pode
substituir sua imagem por outro programa com `execve()`. O pai usa `wait()` para
coletar status de término. Implementações modernas podem usar interfaces
otimizadas, mas esse modelo explica a árvore de processos.

```bash
printf 'shell pid=%s ppid=%s\n' "$$" "$PPID"
ps -eo user,pid,ppid,lstart,state,comm --forest | less
pstree -ap "$$" 2>/dev/null || true
```

## Identificadores e credenciais

Um processo tem PID, pai, grupo de processos, sessão, credenciais reais e
efetivas, descritores, ambiente, diretório atual, limites e namespaces.

```bash
cat "/proc/$$/status" | sed -n '1,30p'
readlink "/proc/$$/cwd"
tr '\0' '\n' < "/proc/$$/environ" | sed -n '1,10p'
ls -l "/proc/$$/fd"
```

O ambiente pode conter segredos mal posicionados. `/proc` aplica controles de
acesso, mas variáveis de ambiente não são um cofre.

## Estados

Estados observáveis comuns:

- `R`: executando ou pronto para CPU;
- `S`: sono interrompível, esperando evento;
- `D`: espera ininterruptível, frequentemente I/O;
- `T`: parado/rastreado;
- `Z`: zombie, terminou mas o pai não coletou status.

Zombie não consome a memória normal do processo, mas ocupa entrada na tabela.
Não se “mata” um zombie: corrige-se ou sinaliza-se o pai para coletá-lo. Um
órfão é reparentado a um subreaper ou init, conforme o contexto.

## Threads e tarefas

```bash
ps -L -p "$$" -o pid,tid,psr,state,comm
ls "/proc/$$/task"
```

No kernel, threads são tarefas que compartilham recursos escolhidos. Ferramentas
podem mostrar PID como ID do grupo e TID/LWP como thread individual.

## Job control da shell

```bash
sleep 120 &
job_pid=$!
jobs -l
kill -STOP "$job_pid"
jobs -l
kill -CONT "$job_pid"
wait "$job_pid"
```

`&`, `jobs`, `fg`, `bg` e `Ctrl-Z` pertencem ao controle interativo. Para
serviços duradouros, use systemd, que supervisiona, registra e aplica limites.
`nohup` e multiplexadores resolvem casos menores, mas não oferecem toda essa
gestão.

## Sinais

```bash
kill -l
trap 'printf "recebi TERM\n"; exit 0' TERM
```

Sinais são notificações assíncronas. `SIGTERM` solicita término tratável;
`SIGINT` costuma vir de Ctrl-C; `SIGHUP` pode indicar terminal fechado ou
reload por convenção da aplicação; `SIGKILL` não pode ser tratado e impede
cleanup do processo. Use KILL somente depois de entender por que TERM falhou.

```bash
kill -TERM PID
timeout --signal=TERM --kill-after=5s 30s comando
```

Confirme PID e processo antes. PIDs são reutilizados; em automação moderna,
systemd e pidfds podem oferecer identificação mais segura.

## Prioridade e agendamento

Nice influencia prioridade de tarefas normais; não garante uma porcentagem de
CPU.

```bash
ps -eo pid,ni,pri,psr,stat,comm --sort=-ni | head
nice -n 10 comando
renice 10 -p PID
chrt -p PID 2>/dev/null || true
```

Políticas de tempo real podem impedir trabalho essencial e exigem projeto,
limites e privilégio. Afinidade (`taskset`) restringe CPUs elegíveis, mas pode
piorar balanceamento e cache.

## Limites

```bash
ulimit -a
cat "/proc/$$/limits"
systemctl show --property=TasksMax,LimitNOFILE 2>/dev/null || true
```

`rlimit`, cgroups e limites de unidade resolvem problemas diferentes. Elevar
`nofile` sem dimensionar memória, portas, filas e aplicação desloca a falha.

## IPC e descritores

Pipes, FIFOs, sockets Unix, memória compartilhada, filas e sinais permitem
comunicação. Inspecione antes de concluir:

```bash
lsof -p "$$" 2>/dev/null | head
ss -xlp 2>/dev/null | head
ipcs 2>/dev/null || true
```

## Exercícios

1. Compile e execute `exemplos/c/processos.c`; desenhe fork, pipe e wait.
2. Crie processo que trate TERM e compare com KILL.
3. Abra um arquivo, remova seu nome e observe o descritor com `lsof` ou `/proc`.
4. Encontre um serviço e relacione PID, unidade, cgroup, descritores e logs.

## Checklist de domínio

Consigo explicar ciclo de vida, estados, sinais, threads, descritores, jobs,
prioridades e limites sem usar “processo travado” como diagnóstico final.
