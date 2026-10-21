# 30 — LSM, seccomp, capabilities e sandbox

## Objetivos

- construir defesa em camadas após reduzir privilégio;
- entender hooks LSM e políticas por rótulo/caminho;
- criar allowlist de syscalls com seccomp;
- limitar capabilities, filesystem e recursos.

## Credenciais e capabilities

UID 0 tradicional agrega poderes demais. Capabilities dividem checks em bits,
mas algumas, como `CAP_SYS_ADMIN`, continuam amplas. Conjuntos permitted,
effective, inheritable, bounding e ambient interagem com `execve`, file
capabilities e `no_new_privs`.

```bash
grep '^Cap\|^NoNewPrivs' /proc/self/status
capsh --print 2>/dev/null | head -n 30
getcap -r ./build 2>/dev/null
```

Reduza bounding set antes de conceder capabilities. Capability não é papel de
negócio e não substitui autorização da aplicação.

## LSM

LSM fornece hooks onde módulos de segurança decidem acesso. SELinux usa labels e
tipos; AppArmor se orienta por perfis e caminhos; Landlock permite que processo
restrinja a si e descendentes em escopo de filesystem. Múltiplos LSMs podem ser
empilhados conforme kernel e config.

```bash
cat /sys/kernel/security/lsm 2>/dev/null
grep '^CONFIG_SECURITY' /boot/config-"$(uname -r)" 2>/dev/null | head
```

## seccomp

Seccomp filter avalia número de syscall, arquitetura e argumentos brutos por BPF
clássico. Ações incluem allow, errno, kill, log, trap e user notification. Filtro
não entende ponteiro apontado com segurança; paths devem ser controlados por LSM,
namespace/mount ou desenho do processo.

Instale `PR_SET_NO_NEW_PRIVS` antes de filtro sem privilégio. Allowlist deve ser
gerada pelo contrato da aplicação, testada em caminhos de erro, upgrade e shutdown.

## Sandbox em camadas

1. processo separado e protocolo mínimo;
2. UID dedicado/dinâmico;
3. nenhum privilégio e bounding set vazio;
4. filesystem somente leitura com diretórios explícitos;
5. LSM/Landlock para objetos;
6. seccomp para syscalls;
7. cgroup para dano por recurso;
8. logs e caminho de recuperação.

## Redução antes do filtro

Comece separando o parser ou worker arriscado em processo com protocolo mínimo.
Depois remova UID, grupos, capabilities, descritores e paths desnecessários.
Seccomp aplicado a um processo ainda privilegiado limita syscalls, mas não reduz
automaticamente autoridade já disponível por descritores abertos.

Capabilities são verificadas em operações específicas e namespaces relevantes.
`CAP_SYS_ADMIN` cobre domínios amplos; concedê-la para resolver uma negação
costuma invalidar a redução. Analise permitted, effective, bounding e ambient em
cada `execve`. `no_new_privs` impede ganhar privilégio por exec e é requisito
para filtro seccomp não privilegiado.

## Política observável

Gere allowlist exercitando startup, operação, erro, reload e shutdown, mas não
trate trace como especificação completa: cobertura não visitada ainda existe.
Relacione cada syscall a função necessária, use architecture check e defina ação
de default. Durante desenvolvimento, LOG ou ERRNO facilita diagnóstico; produção
pode exigir KILL conforme ameaça e recuperação.

Seccomp vê valores escalares do argumento no momento do filtro, não consegue
copiar path apontado com segurança nem acompanhar objeto depois. LSM ou Landlock
controla objetos do filesystem; mount namespace reduz visão; permissões e
descritores restringem autoridade. Cgroup limita exaustão, não acesso a dados.

## Falhas comuns

- aplicar filtro antes de conhecer lifecycle completo;
- omitir architecture check;
- conceder capability ampla para corrigir uma falha funcional;
- acreditar que seccomp filtra caminho;
- confundir namespace com autorização;
- bloquear o próprio recovery sem modo de diagnóstico.

## Prática A

Compile [`seccomp_demo.c`](exemplos/c/seccomp_demo.c). Ele instala um filtro que
nega uma syscall inofensiva escolhida para demonstração e confirma `EPERM`, sem
matar o shell nem alterar política global. Expanda apenas na VM.

## Exercícios

1. Inventarie autoridade do serviço por UID, grupos, capabilities, descritores e
   paths antes de criar filtro.
2. Capture syscalls nos cinco caminhos de lifecycle e marque lacunas de cobertura.
3. Proponha sandbox em camadas para processador local de arquivos, com modo de
   falha e recuperação.
4. Explique por que seccomp não autoriza somente `/data` e onde LSM, mount e
   directory fd entram.

## Checklist de domínio

- [ ] Reduzo arquitetura e privilégio antes de adicionar filtros.
- [ ] Entendo conjuntos de capabilities e `no_new_privs`.
- [ ] Projeto seccomp com arquitetura, default e lifecycle completo.
- [ ] Uso LSM ou Landlock para objetos, não ponteiros de seccomp.
- [ ] Testo negações, logs, upgrade e recovery.

Fontes: [LSM](https://docs.kernel.org/admin-guide/LSM/index.html) e
[seccomp filter](https://docs.kernel.org/userspace-api/seccomp_filter.html).
