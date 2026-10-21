# Folha de consulta Linux

Use depois de compreender os capítulos. Não é uma lista para executar inteira.

## Identidade e sistema

```bash
cat /etc/os-release
uname -a
hostnamectl
id
getent passwd USUARIO
uptime
```

## Ajuda

```bash
type -a COMANDO
COMANDO --help
man SECAO TOPICO
apropos TERMO
info coreutils
```

## Arquivos

```bash
pwd
stat -- CAMINHO
file -- CAMINHO
namei -l -- CAMINHO
find RAIZ -type f -print0
du -xhd1 CAMINHO | sort -h
df -hT
df -ih
```

## Permissões

```bash
stat -c '%A %a %U:%G %n' CAMINHO
getfacl -- CAMINHO
umask
findmnt -T CAMINHO
lsattr -- CAMINHO
getcap CAMINHO
```

## Processos e memória

```bash
ps -eo pid,ppid,user,state,%cpu,%mem,comm --forest
top -H
cat /proc/PID/status
ls -l /proc/PID/fd
grep -E '^(Rss|Pss|Private)' /proc/PID/smaps_rollup
free -h
vmstat 1 5
cat /proc/pressure/{cpu,memory,io}
```

## systemd e logs

```bash
systemctl status UNIDADE
systemctl cat UNIDADE
systemctl show UNIDADE
systemctl list-dependencies UNIDADE
journalctl -u UNIDADE -b
systemctl --failed
systemd-analyze critical-chain
```

## Armazenamento

```bash
lsblk -f
findmnt
blkid
cat /proc/mdstat
sudo pvs; sudo vgs; sudo lvs
swapon --show
```

## Interface local do host

```bash
ip -brief link
ip -brief address
ss -lntup
ss -xlp
getent hosts localhost
```

Rotas, vizinhança, DNS e métricas de enlace pertencem aos módulos 14 a 18.

## Boot e kernel

```bash
cat /proc/cmdline
uname -r
lsmod
modinfo MODULO
journalctl -k -b
journalctl --list-boots
cat /proc/sys/kernel/tainted
```

## Diagnóstico em ordem

```text
1. esperado vs observado e janela
2. primeira mensagem causal
3. mudanças recentes
4. estado da unidade/processo
5. CPU, memória, I/O e socket local no intervalo
6. permissão, MAC, montagem e limites
7. hipótese e teste mínimo
8. correção reversível
9. validação e prevenção
```

## Barreiras antes de mudar

```text
alvo exato · backup · snapshot · console · validação · rollback · teste
```
