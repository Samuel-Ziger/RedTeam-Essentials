# 03 — Arquitetura do sistema Linux

## Objetivos

- localizar a fronteira entre aplicação, biblioteca, syscall, kernel e hardware;
- relacionar processo, descritor, inode, VFS e filesystem;
- explicar o caminho do firmware até o PID 1;
- diferenciar ISA, ABI, API, formato ELF e compatibilidade de bibliotecas.

## As camadas

```text
aplicativos e serviços
shell, bibliotecas e ferramentas de user space
---------------- interface de chamadas de sistema ----------------
kernel: scheduler | memória | VFS | rede | IPC | segurança | drivers
hardware: CPU | RAM | controladores | discos | interfaces
```

O processador possui modos de privilégio. O kernel executa com autoridade para
controlar hardware e isolamento; aplicações executam em user space. Uma
aplicação solicita serviços por chamadas de sistema, frequentemente através
de uma biblioteca como glibc ou musl.

## Kernel monolítico modular

Linux é normalmente descrito como kernel monolítico modular: subsistemas
centrais compartilham o espaço privilegiado, enquanto funcionalidades como
drivers podem ser carregadas como módulos. Isso não significa que tudo está em
um único arquivo ou sempre carregado.

```bash
uname -r
cat /proc/version
lsmod | head
modinfo loop 2>/dev/null | head
```

`uname -r` mostra a release do kernel em execução, não a release da distro.

## Processos e recursos

Um programa é código armazenado. Um processo é uma instância em execução
com espaço de endereços, descritores, credenciais, sinais e estado de
agendamento. Threads de um processo compartilham recursos, inclusive o espaço
de endereços, mas possuem pilha e estado de CPU próprios.

```bash
ps -eo pid,ppid,user,state,comm --forest | head -n 25
printf 'PID da shell: %s\n' "$$"
ls -l "/proc/$$/fd"
```

Descritores 0, 1 e 2 normalmente representam entrada padrão, saída padrão e
erro padrão. “Tudo é arquivo” é uma heurística: muitas interfaces usam
descritores, mas sockets, pipes e dispositivos têm semânticas próprias.

## VFS e sistemas de arquivos

O Virtual Filesystem Switch oferece uma interface comum (`open`, `read`,
`write`, `stat`) sobre ext4, XFS, Btrfs, tmpfs, NFS e outros. Um inode guarda
metadados e referências aos dados; o nome pertence a uma entrada de diretório
que aponta para o inode.

```bash
stat /etc/hosts
findmnt -T /etc/hosts
df -T / /tmp
```

`/proc`, `/sys` e partes de `/run` são interfaces virtuais ou temporárias, não
arquivos comuns persistidos no disco como `/etc/hosts`.

## Espaços virtuais de informação

- `/proc`: processos e parâmetros/estado expostos pelo kernel.
- `/sys`: objetos de dispositivos, drivers, barramentos e subsistemas.
- `/dev`: nós de dispositivo, geralmente administrados dinamicamente por udev.
- `/run`: estado volátil desde o boot atual.

```bash
cat /proc/cpuinfo | sed -n '1,12p'
cat /proc/meminfo | sed -n '1,12p'
find /sys/class -maxdepth 1 -mindepth 1 -type d | head
mount | grep -E ' on /(proc|sys|dev|run) '
```

Leia essas interfaces; não escreva nelas sem entender a documentação do
parâmetro e ter uma reversão testada.

## Do boot ao PID 1

1. firmware inicializa hardware e escolhe uma entrada de boot;
2. bootloader carrega kernel e initramfs;
3. kernel configura CPU, memória e drivers iniciais;
4. initramfs localiza e monta a raiz real;
5. kernel inicia o primeiro processo de user space;
6. o init, frequentemente systemd, ativa serviços e sessões.

```bash
ps -p 1 -o pid,comm,args
cat /proc/1/cgroup
systemd-analyze 2>/dev/null || true
```

## Identidade e autorização

O kernel toma decisões usando IDs numéricos, capabilities, namespaces e
políticas de segurança. Nomes de usuário tornam IDs legíveis.

```bash
id
getent passwd "$(id -un)"
grep -E '^(Uid|Gid|Groups|Cap)' "/proc/$$/status"
```

O UID 0 tem tratamento especial tradicional, mas root dentro de um user
namespace pode não equivaler a root no host.

## ABI, API e arquitetura

- **ISA:** instruções da CPU, como x86-64 ou AArch64.
- **ABI:** convenção binária: registradores, chamadas, formato e linking.
- **API:** interface de código-fonte oferecida a programas.
- **ELF:** formato comum de executáveis, objetos e bibliotecas em Linux.

```bash
uname -m
file /bin/sh
readelf -h /bin/sh 2>/dev/null | sed -n '1,20p'
ldd /bin/sh 2>/dev/null || true
```

Scripts são interpretados; binários precisam ser compatíveis com arquitetura,
ABI, loader e bibliotecas exigidas.

## Exercícios

1. Desenhe o caminho de `cat /etc/hosts` da shell ao disco/page cache.
2. Descubra quais filesystems sustentam `/`, `/proc`, `/sys`, `/dev` e `/run`.
3. Compare PID, PPID, descritores e mapas de memória de duas shells.
4. Explique por que um container pode ter Ubuntu no user space e kernel Fedora
   no host.

## Checklist de domínio

Sem consultar o texto, explique user/kernel space, syscall, processo, thread,
VFS, inode, PID 1, ABI e o papel de `/proc`, `/sys`, `/dev` e `/run`.
