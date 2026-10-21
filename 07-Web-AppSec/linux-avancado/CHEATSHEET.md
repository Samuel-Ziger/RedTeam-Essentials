# Folha de consulta

Use esta página para lembrar caminhos de investigação, não como lista de
ajustes universais.

## Versão e configuração

```bash
uname -r
cat /proc/version
cat /proc/cmdline
zcat /proc/config.gz 2>/dev/null || grep '^CONFIG_' /boot/config-"$(uname -r)"
modinfo module_name
```

## Processos, CPU e memória

```bash
ps -eLo pid,tid,psr,cls,rtprio,pri,ni,stat,comm
cat /proc/PID/{status,sched,limits,cgroup}
taskset -pc PID
numactl --hardware
cat /proc/{meminfo,vmstat,pressure/memory}
grep -E 'Vm|Rss|Threads' /proc/PID/status
```

## Arquivos e I/O

```bash
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS
stat FILE
cat /proc/PID/mountinfo
lsblk -o NAME,MAJ:MIN,TYPE,SIZE,FSTYPE,MOUNTPOINTS
cat /sys/block/DEVICE/queue/scheduler
```

## systemd e cgroups

```bash
systemd-analyze critical-chain
systemctl show UNIT -p ControlGroup -p MemoryCurrent -p TasksCurrent
systemd-cgls
systemd-cgtop
cat /sys/fs/cgroup/cgroup.controllers
cat /proc/pressure/{cpu,memory,io}
```

## Observabilidade

```bash
perf stat -- command args
perf record -g -- command args
perf report
trace-cmd list 2>/dev/null || true
cat /sys/kernel/tracing/available_tracers 2>/dev/null
bpftool feature probe unprivileged 2>/dev/null || true
```

## ELF e depuração

```bash
file PROGRAM
readelf -hW PROGRAM
readelf -lW PROGRAM
objdump -d PROGRAM
ldd PROGRAM
strace -f -yy -o trace.log -- PROGRAM
gdb --args PROGRAM
coredumpctl info
```

Use `ldd`, `strace` e GDB somente em programa próprio ou confiável. Para
arquivo externo, comece por `file`, `readelf` e `objdump -p` sem executá-lo.

## Virtualização local

```bash
test -e /dev/kvm && stat /dev/kvm
qemu-img info disk.qcow2
virsh list --all
virsh dominfo VM
```

## Sequência de diagnóstico

1. Declare sintoma, impacto, início e SLO afetado.
2. Registre versão, configuração e carga.
3. Formule uma hipótese falsificável.
4. Escolha a métrica que a refutaria.
5. Mude uma variável por vez.
6. Compare distribuições, não apenas médias.
7. Reverta, repita e arquive evidência.
