# Referências

Os capítulos são autocontidos. Estas fontes servem para confirmar detalhes que
mudam entre versões e aprofundar o estudo.

## Fontes primárias

- [Documentação do kernel](https://docs.kernel.org/) e
  [tradução pt-BR](https://docs.kernel.org/translations/pt_BR/index.html).
- [Categorias de releases do kernel](https://kernel.org/category/releases.html)
  para distinguir mainline, stable e longterm no momento do estudo.
- [Código principal em kernel.org](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/).
- [Linux man-pages](https://www.kernel.org/doc/man-pages/).
- [Cross-reference do código no Bootlin Elixir](https://elixir.bootlin.com/linux/latest/source).
- [Scheduler EEVDF](https://docs.kernel.org/scheduler/sched-eevdf.html),
  [RCU](https://docs.kernel.org/RCU/whatisRCU.html) e
  [Memory Management](https://docs.kernel.org/mm/index.html).
- [Core API](https://docs.kernel.org/core-api/index.html) e
  [workqueues](https://docs.kernel.org/core-api/workqueue.html).
- [VFS](https://docs.kernel.org/filesystems/vfs.html) e
  [filesystems](https://docs.kernel.org/filesystems/index.html).
- [ftrace](https://docs.kernel.org/trace/ftrace.html),
  [kprobe events](https://docs.kernel.org/trace/kprobetrace.html) e
  [libbpf/CO-RE](https://docs.kernel.org/bpf/libbpf/libbpf_overview.html).
- [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) e
  [PSI](https://docs.kernel.org/accounting/psi.html).
- [KVM API](https://docs.kernel.org/virt/kvm/api.html),
  [QEMU](https://www.qemu.org/docs/master/system/index.html) e
  [libvirt](https://libvirt.org/docs.html).
- [LSM](https://docs.kernel.org/admin-guide/LSM/index.html),
  [seccomp](https://docs.kernel.org/userspace-api/seccomp_filter.html) e
  [assinatura de módulos](https://docs.kernel.org/admin-guide/module-signing.html).
- [fs-verity](https://docs.kernel.org/filesystems/fsverity.html) e
  [dm-verity](https://docs.kernel.org/admin-guide/device-mapper/verity.html).
- [systemd: resource control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)
  e [execução](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html).
- [Reproducible Builds](https://reproducible-builds.org/docs/) e a
  [especificação `SOURCE_DATE_EPOCH`](https://reproducible-builds.org/specs/source-date-epoch/).
- [Buildroot manual](https://buildroot.org/downloads/manual/manual.html) e
  [Device Tree specification](https://www.devicetree.org/specifications/).
- [Envio de patches](https://docs.kernel.org/process/submitting-patches.html) e
  [checklist de submissão](https://docs.kernel.org/process/submit-checklist.html).

## Comunidade, análise e discussão

- [KernelNewbies](https://kernelnewbies.org/) para trilhas de entrada e mudanças por release.
- [LKML](https://lore.kernel.org/lkml/) para discussões e revisão de patches.
- [LWN kernel index](https://lwn.net/Kernel/Index/) para contexto editorial.
- [Unix & Linux Stack Exchange](https://unix.stackexchange.com/) para perguntas reproduzíveis.
- [Fedora Docs](https://docs.fedoraproject.org/),
  [Debian Administrator's Handbook](https://www.debian.org/doc/manuals/debian-handbook/)
  e [ArchWiki](https://wiki.archlinux.org/) para variações por distribuição.

## Como avaliar uma referência

1. Registre versão, arquitetura e configuração a que o texto se aplica.
2. Prefira documentação e código do mesmo commit do experimento.
3. Trate blogs e fóruns como hipóteses, não como prova final.
4. Reproduza o caso numa VM antes de adotar qualquer ajuste.
5. Não copie valores de tuning sem modelo de carga e baseline equivalentes.
