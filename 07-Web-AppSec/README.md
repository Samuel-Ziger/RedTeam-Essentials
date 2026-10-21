# 07 — Linux avançado: engenharia de sistemas e kernel

> Especialização prática que começa onde o módulo 06 termina: ler o
> kernel, investigar subsistemas, medir comportamento e construir mudanças
> reproduzíveis. O nome histórico da pasta foi mantido para preservar links.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Quem concluiu a formação Linux do módulo 06 e quer atuar com sistemas, kernel, desempenho, virtualização ou plataforma. |
| Pré-requisitos | Módulos 00–06, C, Bash, Git, administração Linux e leitura técnica em inglês. |
| Tempo estimado | 420–620 horas de estudo, 72 práticas, nove laboratórios e projeto. |
| Ambiente | Duas VMs locais com snapshots; uma delas descartável para kernel, boot, armazenamento e KVM. |
| Evidência final | Dossiê técnico, pacote reproduzível, experimento de desempenho, patch didático e appliance Linux offline. |
| Critério de conclusão | Concluir exercícios, checklists, 72 práticas e nove gates; passar na validação e defender o projeto final com medições. |

## Limite deste módulo

**Redes não fazem parte do módulo 07.** Não há roteamento, namespaces de
rede, DNS, firewall, nftables, conntrack, sockets de rede, `tc`, XDP, Wi-Fi ou
administração remota. Esses assuntos terão um módulo próprio. Exemplos de
eBPF observam somente processos, escalonamento e arquivos; as VMs usam console
e imagens locais.

## Resultado da especialização

Ao concluir, você conseguirá:

- navegar no código-fonte do kernel e relacioná-lo a eventos observáveis;
- explicar ABI, ELF, loader, syscalls, tarefas, scheduler, SMP, RCU e MM;
- diagnosticar page faults, reclaim, NUMA, page cache, VFS e block layer;
- comparar ext4, XFS e Btrfs por invariantes, falhas e carga de trabalho;
- projetar boot verificável com initramfs, UKI, Secure Boot e TPM;
- controlar CPU, memória e I/O com systemd e cgroup v2;
- investigar gargalos com `perf`, ftrace, tracepoints, kprobes e eBPF local;
- depurar processos, kernel, oops, panic e dumps sem alterar evidência;
- operar KVM/QEMU, virtio, qcow2 e libvirt sem depender de rede;
- aplicar LSM, seccomp, capabilities, IMA, fs-verity e dm-verity;
- produzir pacotes e imagens reproduzíveis, atualizáveis e reversíveis;
- preparar, revisar, testar e justificar uma pequena contribuição ao kernel.

## Rota completa

### Etapa 1 — fonte, ABI e execução (75–105 h)

1. [Método, laboratório e evidência](linux-avancado/00-metodo-laboratorio.md).
2. [Árvore do kernel e leitura de código](linux-avancado/01-fonte-kernel.md).
3. [Kconfig, kbuild, compilação e cross-build](linux-avancado/02-build-kernel.md).
4. [ABI, syscalls, vDSO e ioctl](linux-avancado/03-abi-syscalls.md).
5. [ELF, linking e loader dinâmico](linux-avancado/04-elf-loader.md).
6. [Tarefas, `clone`, `exec`, sinais e espera](linux-avancado/05-processos-internals.md).
7. [Namespaces locais e credenciais](linux-avancado/06-namespaces-locais.md).

### Etapa 2 — CPU, concorrência e memória (80–115 h)

1. [Scheduler, EEVDF, RT e deadline](linux-avancado/07-scheduler.md).
2. [SMP, preempção, interrupções e timers](linux-avancado/08-smp-interrupcoes.md).
3. [Atomics, locks e modelo de memória](linux-avancado/09-concorrencia.md).
4. [RCU e estruturas lockless](linux-avancado/10-rcu.md).
5. [MM, page tables, allocators e reclaim](linux-avancado/11-mm-internals.md).
6. [NUMA, huge pages, PSI e DAMON](linux-avancado/12-numa-pressao.md).

### Etapa 3 — arquivos, blocos e dispositivos (80–115 h)

1. [VFS, inodes, dentries e page cache](linux-avancado/13-vfs-page-cache.md).
2. [ext4, XFS, Btrfs e consistência](linux-avancado/14-filesystems.md).
3. [Block layer, filas e writeback](linux-avancado/15-block-layer.md).
4. [Device Mapper, thin provisioning e verity](linux-avancado/16-device-mapper.md).
5. [I/O assíncrona, epoll e io_uring](linux-avancado/17-io-assincrona.md).
6. [Dispositivos, drivers, DMA e IOMMU](linux-avancado/18-drivers-iommu.md).

### Etapa 4 — inicialização, recursos e diagnóstico (90–130 h)

1. [UEFI, initramfs, UKI, TPM e boot medido](linux-avancado/19-boot-confiavel.md).
2. [systemd avançado e ciclo de vida](linux-avancado/20-systemd-avancado.md).
3. [cgroup v2, PSI e OOM](linux-avancado/21-cgroups-recursos.md).
4. [perf, PMU, flame graphs e metodologia](linux-avancado/22-perf-metodologia.md).
5. [ftrace, tracepoints, kprobes e uprobes](linux-avancado/23-tracing.md).
6. [eBPF e CO-RE para observabilidade local](linux-avancado/24-ebpf-local.md).
7. [Depuração de user space](linux-avancado/25-debug-userspace.md).
8. [Oops, panic, kdump, crash e drgn](linux-avancado/26-debug-kernel.md).

### Etapa 5 — plataforma, segurança e engenharia (95–155 h)

1. [KVM, QEMU, libvirt e virtio offline](linux-avancado/27-kvm-qemu.md).
2. [Tempo real, latência e PREEMPT_RT](linux-avancado/28-tempo-real.md).
3. [Linux embarcado, Device Tree e Buildroot](linux-avancado/29-embarcado.md).
4. [LSM, seccomp, capabilities e sandbox](linux-avancado/30-seguranca-internals.md).
5. [Assinatura, IMA/EVM, fs-verity e dm-verity](linux-avancado/31-integridade.md).
6. [Pacotes, distribuições e builds reproduzíveis](linux-avancado/32-engenharia-distribuicao.md).
7. [Desenvolvimento e contribuição ao kernel](linux-avancado/33-contribuicao-kernel.md).
8. [Projeto final: appliance Linux offline](linux-avancado/34-projeto-final.md).

Use também o [glossário](linux-avancado/GLOSSARIO.md), a
[folha de consulta](linux-avancado/CHEATSHEET.md), as
[72 práticas cumulativas](linux-avancado/CADERNO-PRATICAS.md), o
[guia de experimentos e diagnóstico](linux-avancado/GUIA-EXPERIMENTOS-DIAGNOSTICO.md), o
[projeto de referência](linux-avancado/projetos/offline-appliance/README.md), as
[respostas orientativas](linux-avancado/RESPOSTAS.md) e as
[referências](linux-avancado/REFERENCIAS.md).

## Código e laboratórios

Os exemplos incluem analisadores de ELF e `/proc`, medição de page faults,
sonda segura de KVM, isolamento com seccomp, scripts de pressão e build
reproduzível, unidade systemd endurecida, programa eBPF não carregado
automaticamente e módulo didático para VM. Nenhum teste precisa de `sudo`.

```bash
bash 07-Web-AppSec/linux-avancado/testar-curso.sh
```

Os [nove laboratórios avaliativos](linux-avancado/laboratorios/README.md)
funcionam como gates progressivos e classificam o risco:

- **A:** somente leitura ou processo do próprio usuário;
- **B:** altera apenas arquivo/imagem descartável;
- **C:** exige snapshot de uma VM de estudo;
- **D:** exige VM sacrificável e console de recuperação.

## Critério de conclusão

- [ ] Relaciono uma medição de user space ao caminho correspondente no kernel.
- [ ] Sei separar estabilidade de ABI de detalhes internos que podem mudar.
- [ ] Explico scheduler, RCU, page tables, reclaim, VFS e block layer.
- [ ] Investigo desempenho com hipótese, baseline, controle e reversão.
- [ ] Leio traces sem confundir correlação com causalidade.
- [ ] Construo uma VM local sem rede, com limites e imagem verificável.
- [ ] Produzo um artefato reproduzível e documento sua cadeia de confiança.
- [ ] Entrego um patch didático pequeno, testado e revisável.
- [ ] Concluo as 72 práticas e os nove gates em ordem.
- [ ] Concluo e defendo o appliance final.

## Vídeos em português

Os vídeos complementam a leitura. O curso continua autocontido e os trechos que
fogem do escopo de redes devem ser ignorados nesta etapa.

1. [Hello World como você nunca viu: entendendo C](https://www.youtube.com/watch?v=Gp2m8ZuXoPg) — **Akitando**.
2. [Só precisamos de 640 kB de memória?](https://www.youtube.com/watch?v=cTVXKfYOYxo) — **Akitando**.
3. [Como funciona o boot de um Linux?](https://www.youtube.com/watch?v=5F6BbhgvFOE) — **Akitando**.
4. [Protegendo e recuperando dados: Git, backup e Btrfs](https://www.youtube.com/watch?v=yfEhz9poqW8) — **Akitando**.
5. [QEMU, KVM, libvirt e passthrough](https://www.youtube.com/watch?v=IDnabc3DjYY) — **Akitando**.

## Continuação avançada

Web, APIs e revisão segura de código continuam no
[módulo 30](../30-Web-API-AppSec/README.md), após a formação-base.
