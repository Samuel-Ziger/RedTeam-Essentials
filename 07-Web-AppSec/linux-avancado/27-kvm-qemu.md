# 27 — KVM, QEMU, libvirt e virtio offline

## Escopo

Todas as VMs deste capítulo são criadas **sem interface de rede**. Console
serial, ISO local e disco qcow2 bastam para os objetivos. Rede virtual pertence
ao módulo futuro de redes.

## Objetivos

- separar responsabilidades de KVM, QEMU e libvirt;
- entender VM fd, vCPU fd, `ioctl` e exit to user space;
- operar imagens, snapshots e virtio;
- modelar isolamento e resource control do processo QEMU.

## Camadas

KVM expõe `/dev/kvm` e uma API baseada em descritores e `ioctl`. User space abre
o system fd, verifica `KVM_GET_API_VERSION`, cria VM e vCPUs, mapeia memória e
entra em `KVM_RUN`. Certos eventos causam VM exit para QEMU tratar.

QEMU oferece modelo de máquina, firmware, dispositivos, armazenamento e loop de
execução. Com KVM, código guest suportado executa com aceleração; com TCG, QEMU
traduz instruções. libvirt fornece API, inventário, XML e ciclo de vida.

```bash
test -c /dev/kvm && stat /dev/kvm
qemu-system-x86_64 -accel help 2>/dev/null
virsh version 2>/dev/null || true
```

O exemplo [`kvm_probe.c`](exemplos/c/kvm_probe.c) somente consulta API e
capabilities; não cria uma VM.

## Memória e CPU

vCPU é uma thread no host e compete no scheduler. Overcommit pode ser correto
para cargas ociosas, mas degrada cauda sob contenção. Ballooning devolve páginas
cooperativamente; KSM deduplica conteúdo e introduz custo e considerações de
isolamento. Huge pages reduzem TLB pressure, mas complicam reserva e NUMA.

## Dispositivos e virtio

Emulação reproduz hardware conhecido, com mais traps. Virtio define dispositivo
paravirtualizado e filas compartilhadas para reduzir overhead. Este curso usa
virtio-blk/scsi, balloon, rng e console; dispositivos de rede são omitidos.

## Imagens

Raw é simples e previsível. qcow2 oferece alocação dinâmica, backing files,
snapshots e metadados. Uma cadeia longa de overlays aumenta dependências e pode
prejudicar performance. Nunca apague backing file enquanto descendentes dependem
dele.

```bash
qemu-img create -f qcow2 -b base.qcow2 -F qcow2 lab.qcow2
qemu-img info --backing-chain lab.qcow2
qemu-img check lab.qcow2
```

## Execução e fronteiras

Um vCPU é thread do QEMU que entra em `KVM_RUN`. Código guest executa até um
evento exigir saída: acesso a dispositivo emulado, halt, interrupção ou condição
tratada em user space. Muitos VM exits elevam custo; virtio reduz emulação por
queues e notificações compartilhadas, mas continua exigindo driver e protocolo
corretos.

Separe isolamento de hardware, kernel host, processo QEMU, dispositivos e gestão.
KVM não cria política de arquivo nem limita CPU sozinho. Execute QEMU com usuário
dedicado, paths explícitos, sandbox e cgroup; não conceda dispositivo físico ou
diretório do host sem requisito. Console serial substitui dependência de rede.

## Memória, storage e snapshots

Memória vista pelo guest, RSS do QEMU e páginas residentes no host não são iguais.
Balloon depende de cooperação do guest; overcommit pode provocar reclaim ou OOM
no host. Combine métricas de ambos os lados e evite prometer capacidade com base
apenas na RAM virtual configurada.

Snapshot interno, overlay externo e backup têm lifecycles diferentes. Uma cadeia
qcow2 referencia caminhos e formatos; movê-la ou apagar a base rompe descendentes.
Commit/rebase altera dependências e deve ocorrer sobre cópias testadas. Para o
laboratório, base permanece somente leitura e overlay é descartável.

## Falhas comuns

- chamar KVM de emulador completo;
- comparar TCG e KVM com cargas ou clocks diferentes;
- criar NIC por default sem perceber;
- apagar ou modificar backing file;
- confundir snapshot com backup;
- mapear bloco ou dispositivo real no guest de estudo.

## Prática B/C

1. Crie uma base somente leitura e overlay.
2. Inicie VM sem opção `-nic` ou use `-nic none`.
3. Acesse por console serial.
4. Compare TCG e KVM com carga de CPU local.
5. Limite o QEMU com cgroup/systemd.
6. Desligue, valide imagem e descarte o overlay.

## Exercícios

1. Desenhe descritores system, VM e vCPU e o ciclo `KVM_RUN`/VM exit.
2. Crie cadeia base e overlay, valide backing chain e prove que só o overlay
   mudou.
3. Compare guest RAM, QEMU RSS/PSS e cgroup sob workload controlado.
4. Audite a linha de comando e prove ausência de NIC e de bloco físico.

## Checklist de domínio

- [ ] Distingo KVM, QEMU, libvirt, firmware e virtio.
- [ ] Explico um VM exit e o retorno ao guest.
- [ ] Relaciono vCPU a thread e resource control do host.
- [ ] Preservo cadeia qcow2 e não confundo snapshot com backup.
- [ ] Opero a VM inteiramente offline por console serial.

Fontes: [KVM API](https://docs.kernel.org/virt/kvm/api.html) e
[QEMU system emulation](https://www.qemu.org/docs/master/system/index.html).
