# 05 — Tarefas, `clone`, `exec`, sinais e espera

## Objetivos

- entender por que processos e threads são tarefas no kernel;
- acompanhar criação, execução, parada, saída e reaping;
- relacionar PID, TID, TGID, credenciais e namespaces;
- diagnosticar zombies, estados de sono e sinais.

## `task_struct` como ponto de encontro

Cada tarefa possui estado de escalonamento, credenciais, relações familiares,
referências a memória, arquivos, sinais e namespaces. Threads do mesmo processo
compartilham recursos conforme flags usadas na criação e costumam ter o mesmo
TGID, mas TIDs distintos.

```bash
ps -eLo pid,ppid,tid,tgid,stat,wchan:24,comm
ls /proc/self/task
cat /proc/self/status
```

## Criação

`fork()` cria um novo processo com copy-on-write. `vfork()` tem restrições fortes
porque pai e filho compartilham o espaço temporariamente. `clone()` e `clone3()`
expõem quais recursos são compartilhados e também fundamentam threads e
namespaces.

`execve()` não cria um PID novo: substitui imagem, mappings e atributos definidos
pelo contrato. Descritores sem `FD_CLOEXEC` sobrevivem, uma fonte clássica de
vazamento entre programas.

## Estados e espera

- `R`: executando ou pronto;
- `S`: sono interruptível;
- `D`: sono normalmente não interruptível;
- `T`: parado ou sob tracing;
- `Z`: terminou, mas o pai ainda não coletou status.

Um zombie quase não consome memória de programa, mas ocupa uma entrada de PID e
indica que o pai não chamou `wait*()`. Matar o zombie não funciona: ele já saiu.

## Sinais

Sinais padrão podem coalescer; sinais real-time possuem fila e ordem definida.
Handlers executam assincronamente: apenas funções async-signal-safe podem ser
chamadas com segurança. `signalfd` permite integrar sinais a um event loop local.

## `/proc` e corrida

PIDs são reutilizados. Ler `/proc/PID` em várias etapas pode misturar instâncias
se o processo sair. `pidfd_open()` e operações pidfd reduzem essa corrida ao
representar a identidade com um descritor.

## Compartilhamento e transições

Pense em uma tarefa como referências para conjuntos de recursos: `mm`, tabela
de arquivos, handlers de sinal, filesystem context, credenciais e namespaces.
Flags de `clone` decidem o que é compartilhado. Threads não são uma categoria
mágica separada; são tarefas que compartilham recursos suficientes para compor
um grupo.

No `fork`, page tables são copiadas e páginas normalmente permanecem
compartilhadas até escrita provocar copy-on-write. No `execve`, o PID continua,
mas imagem, stack e mappings mudam; algumas propriedades são preservadas e
outras resetadas. Audite descritores, handlers, signal mask, credenciais e
`no_new_privs` conforme o contrato, em vez de resumir a operação como “trocar
o programa”.

## Espera e shutdown correto

O pai deve coletar todos os filhos, inclusive quando vários terminam antes de um
único sinal `SIGCHLD`. Um handler normalmente apenas registra condição ou
escreve em descritor seguro; o loop principal chama `waitpid(-1, ..., WNOHANG)`
até não haver mais status. Em programas multithread, escolha explicitamente
qual thread recebe sinais bloqueando-os antes de criar as demais.

Shutdown confiável define fases: parar novas entradas, notificar workers,
esperar até deadline, escalar somente se necessário e coletar status. Enviar
`SIGKILL` imediatamente elimina a oportunidade de liberar estado em user
space, embora o kernel feche descritores.

## Diagnóstico por estados

`wchan`, stack, syscalls e contadores ajudam a explicar sono; a letra do
`ps` sozinha não fornece causa. Estado D pode terminar quando o recurso
progride e não significa automaticamente disco defeituoso. Um zombie aponta
problema no pai ou subreaper, não consumo ativo do filho.

## Falhas comuns

- confundir PID, TID e TGID;
- usar PID antigo sem validar identidade;
- fazer logging não seguro dentro de signal handler;
- esquecer `O_CLOEXEC` em um caminho de erro;
- coletar apenas um filho por `SIGCHLD`.

## Prática A

1. Crie um programa com três threads e identifique PID/TID.
2. Observe `/proc/PID/task/TID/status`.
3. Gere um filho que termina antes de `waitpid` e confirme o estado `Z`.
4. Corrija o programa e explique o papel de `SIGCHLD`.
5. Marque descritores com `O_CLOEXEC` e confirme depois de `execve`.

## Exercícios

1. Construa uma tabela de recursos compartilhados para duas combinações de flags
   de `clone`.
2. Escreva um supervisor que cria três filhos, trata `SIGCHLD` por `signalfd`
   e coleta todos sem busy wait.
3. Demonstre vazamento de descritor através de `execve`, corrija com criação
   atômica `CLOEXEC` e adicione teste.
4. Compare identificação por PID e pidfd em um cenário com término rápido.

## Checklist de domínio

- [ ] Relaciono tarefa, thread group, PID, TID e TGID.
- [ ] Explico o que `fork`, `clone` e `execve` preservam ou substituem.
- [ ] Coleto todos os filhos e reconheço zombie corretamente.
- [ ] Projeto handlers somente com operações async-signal-safe.
- [ ] Explico como pidfd reduz a corrida de reutilização de PID.

Fonte: [`clone(2)`](https://man7.org/linux/man-pages/man2/clone.2.html).
