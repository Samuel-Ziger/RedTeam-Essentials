# 06 — Namespaces locais e credenciais

## Escopo

Este capítulo cobre somente PID, mount, UTS, IPC, user, cgroup e time. **Network
namespace foi deliberadamente excluído** e pertence ao futuro módulo de redes.

## Objetivos

- entender namespace como mudança de visão, não como VM;
- relacionar namespace, credenciais e capabilities;
- estudar propagação de mounts e PID 1;
- reconhecer limites de isolamento.

## Identidade e referências

Namespaces são objetos referenciados por tarefas e descritores. Entrar em um
namespace com `setns()` altera a associação da tarefa quando permitido. Entradas
em `/proc/PID/ns/` podem ser abertas ou bind-mounted para manter o objeto vivo.

```bash
readlink /proc/self/ns/{pid,mnt,user,uts,ipc,cgroup,time}
lsns -t pid,mnt,user,uts,ipc,cgroup,time
```

O mesmo processo pode ter PIDs diferentes vistos de namespaces aninhados. O
primeiro processo de um PID namespace tem deveres especiais de reaping e
tratamento de sinais.

## Mount namespace

O namespace isola a tabela de mounts, mas propagação `shared`, `slave`,
`private` ou `unbindable` decide se eventos atravessam fronteiras. `chroot`
troca a raiz de resolução e não é, sozinho, uma barreira de segurança.

```bash
findmnt -o TARGET,PROPAGATION
unshare --user --map-root-user --mount sh -c 'id; findmnt -n /'
```

O comando depende da política de user namespaces da distribuição. Falha pode
ser uma decisão de hardening, não defeito do exercício.

## User namespace e capabilities

UID 0 dentro de um user namespace não é root no namespace pai. Mapeamentos de
UID/GID controlam correspondência. Capabilities são avaliadas em relação ao user
namespace que governa o recurso; “root no container” não equivale a poder global.

Ainda assim, namespaces ampliam a superfície do kernel acessível a processos sem
privilégio. Política deve considerar threat model e atualizações.

## IPC, UTS, cgroup e time

- UTS isola hostname e domainname, não identidade criptográfica;
- IPC isola System V IPC e POSIX message queues;
- cgroup namespace muda a visão dos caminhos, não os limites;
- time namespace virtualiza offsets de alguns relógios, não o relógio de parede.

## Criação, entrada e persistência

`clone` ou `unshare` cria uma nova associação para a tarefa; `setns` entra em
objeto existente por descritor. A ordem importa, especialmente para user e mount
namespaces. Um bind mount de `/proc/PID/ns/TIPO` ou um descritor aberto mantém o
objeto referenciado mesmo após a última tarefa sair.

PID namespace tem visão hierárquica: o pai enxerga descendentes, mas o
descendente não enxerga PIDs do pai. O PID 1 interno precisa coletar órfãos e
possui tratamento especial de sinais. Matar esse init encerra as demais tarefas
do namespace; por isso um shell improvisado como PID 1 não substitui um
supervisor correto.

Mount namespace copia uma visão inicial, mas propagação pode transmitir eventos.
Antes de montar algo em prática, leia `findmnt -o TARGET,PROPAGATION` e torne a
árvore de laboratório privada no namespace. Confirme do lado de fora que nenhum
mount apareceu. `pivot_root` troca a raiz e permite desmontar a anterior;
`chroot` apenas muda a resolução de caminho da tarefa e não fornece isolamento
completo.

## Credenciais em camadas

User namespace mapeia IDs internos para intervalos externos. O UID 0 interno
possui capabilities calculadas no namespace que governa o recurso, não no host
inteiro. Setuid, file capabilities, LSM e políticas da distribuição continuam
participando da decisão. Analise sempre “capability em qual user namespace e
sobre qual objeto?”.

## Falhas comuns

- concluir isolamento só porque hostname ou PID mudou;
- esquecer propagação `shared` antes de montar;
- executar processo comum como PID 1 sem reaping;
- tratar root interno como root global;
- manter namespace vivo por descritor esquecido;
- habilitar user namespace sem considerar superfície e patching do kernel.

## Prática A/C

Em VM:

1. compare inodes de namespaces entre shell pai e `unshare`;
2. crie PID+mount+user namespace sem rede;
3. monte `proc` apenas dentro dele;
4. observe o comportamento do PID 1 local;
5. saia e confirme que mounts não vazaram.

## Exercícios

1. Compare inodes de cada namespace antes, durante e depois de `unshare` e
   explique quais mudaram.
2. Demonstre reaping correto e incorreto para PID 1 local com processos
   sintéticos.
3. Faça um mount em árvore privada, prove a ausência no namespace pai e execute
   cleanup na ordem inversa.
4. Desenhe mapeamento de UID interno/externo e determine onde uma capability
   seria avaliada.

## Checklist de domínio

- [ ] Distingo isolamento de visão, limitação de recurso e política de acesso.
- [ ] Explico `clone`, `unshare`, `setns` e persistência por descritor.
- [ ] Verifico propagação antes de alterar mounts.
- [ ] Entendo deveres especiais do PID 1 interno.
- [ ] Justifico por que namespace sozinho não é fronteira completa.
- [ ] Não uso network namespace neste módulo.

Fonte: [`namespaces(7)`](https://man7.org/linux/man-pages/man7/namespaces.7.html).
