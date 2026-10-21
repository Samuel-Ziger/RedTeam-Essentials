# 23 — Namespaces, cgroups e containers

## Objetivos

- diferenciar virtualização de hardware e isolamento de processos;
- mapear namespace, cgroup, capability, seccomp, MAC e montagem;
- explicar o que permanece compartilhado com o host;
- executar uma carga com identidade e limites mínimos sem tratá-la como sandbox absoluta.

## Container não é VM pequena

Uma VM virtualiza hardware e executa outro kernel. Um container organiza
processos do mesmo kernel com namespaces, cgroups, capabilities, seccomp,
controles MAC, filesystem em camadas e runtime. Uma vulnerabilidade no kernel
pode atravessar a fronteira; o modelo de ameaça é diferente.

## Namespaces

| Namespace | Isola uma visão de |
|-----------|--------------------|
| mount | montagens |
| PID | IDs/árvore de processos |
| network | interfaces, rotas, sockets, firewall |
| UTS | hostname/domainname |
| IPC | filas, semáforos, shared memory |
| user | IDs e capabilities mapeados |
| cgroup | raiz/visão de cgroups |
| time | alguns relógios/offsets |

```bash
lsns
readlink /proc/self/ns/*
unshare --user --map-root-user sh -c 'id; readlink /proc/self/ns/user'
```

Ser UID 0 no user namespace pode mapear para um UID comum fora dele. Nem toda
combinação está habilitada pela distro.

## cgroup v2

Namespaces mudam o que um processo vê; cgroups contabilizam, priorizam e
limitam recursos.

```bash
findmnt -t cgroup2
cat /proc/self/cgroup
systemd-cgls
systemd-cgtop
```

Controles incluem CPU, memória, I/O, PIDs e cpuset. Limite de CPU determina
tempo disponível, não velocidade do processador; limite de memória pode provocar
reclaim e OOM dentro do grupo.

Laboratório sem root, se systemd de usuário permitir:

```bash
systemd-run --user --scope -p MemoryMax=256M -p TasksMax=64 bash
```

Dentro da nova shell, examine `/proc/self/cgroup`; não tente esgotar o limite.

## Capabilities, seccomp e LSM

Capabilities dividem poderes do root; remova todas e acrescente somente as
necessárias. Seccomp filtra syscalls, reduzindo interface alcançável. SELinux e
AppArmor restringem objetos/operações. Nenhuma camada sozinha é sandbox completa.

```bash
grep -E '^Cap' /proc/self/status
grep -E '^(NoNewPrivs|Seccomp)' /proc/self/status
```

`--privileged`, montagem do socket do runtime, host PID/network e dispositivos
amplos removem grande parte do isolamento. Trate acesso ao daemon de container
como privilégio administrativo.

## Filesystem e imagens

Imagens possuem camadas imutáveis e metadados; o container adiciona camada de
escrita efêmera. Volumes/bind mounts persistem e podem expor o host. Um segredo
copiado em uma camada continua no histórico mesmo que removido em camada
posterior.

Boas práticas:

- origem oficial, digest e provenance/SBOM quando disponíveis;
- base mínima compatível, atualizada e reconstruída regularmente;
- build multi-stage sem toolchain no runtime;
- usuário não root e filesystem read-only quando possível;
- capabilities removidas, seccomp e MAC ativos;
- nenhum segredo na imagem ou argumentos;
- limites de memória/PIDs/CPU;
- healthcheck não substitui readiness real;
- logs e atualizações operáveis.

## Rootless

Podman/Docker rootless combinam user namespace e processos sem UID 0 no host,
reduzindo impacto de comprometimento do runtime. Restrições de portas,
filesystem, cgroups e rede variam. Rootless reduz privilégio; não torna imagem
não confiável segura.

## PID 1 no container

O primeiro processo precisa coletar filhos e encaminhar sinais. Aplicativo que
não faz isso pode acumular zombies ou ignorar shutdown. Use exec form no
entrypoint e, quando necessário, init mínimo:

```Dockerfile
ENTRYPOINT ["/usr/local/bin/aplicacao"]
```

Um script entrypoint deve terminar com `exec "$@"` depois da preparação.

## Diagnóstico

Relacione PID do container ao host, namespaces, cgroup, mounts e rede:

```bash
ps -eo pid,ppid,user,cgroup,comm
lsns -p PID
cat /proc/PID/cgroup
cat /proc/PID/mountinfo | head
```

## Exercícios

1. Compare os namespaces do shell e de um container ou escopo próprio, anotando
   os identificadores iguais e diferentes.
2. Defina limite pequeno e seguro de tarefas e memória e observe os arquivos do
   cgroup sem tentar esgotar o host.
3. Faça inventário de mounts, usuário, capabilities e seccomp de uma carga
   rootless; descreva a fronteira que cada controle não cobre.
4. Revise uma imagem fictícia que contém segredo em camada anterior e explique
   por que removê-lo apenas na camada seguinte não resolve a exposição.

## Checklist de domínio

Consigo explicar precisamente o que foi isolado, qual kernel é compartilhado,
quais recursos foram limitados e quais montagens/capabilities ainda atravessam
a fronteira.
