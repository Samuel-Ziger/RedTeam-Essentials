# Referências e comunidades

O curso é autocontido. Estas fontes servem para confirmar comportamento da
versão instalada, acompanhar mudanças e aprofundar. Priorize o manual local e a
documentação da sua distribuição antes de aplicar uma resposta de fórum.

## Estado das versões na revisão

Revisado em 11 de outubro de 2026. As páginas oficiais confirmavam Ubuntu 26.04
como LTS e Debian 13 trixie como stable, com a atualização 13.7 publicada em
setembro de 2026. Não transforme esses números em regra permanente: confirme a
release suportada e suas notas no dia de instalar.

O projeto do kernel distingue mainline, stable e longterm. A distribuição pode
manter seu próprio kernel e retroportar correções; por isso, número de versão
isolado não demonstra suporte nem vulnerabilidade.

- [Ciclo e suporte do Ubuntu](https://ubuntu.com/about/release-cycle).
- [Releases do Debian](https://www.debian.org/releases/).
- [Debian stable e point releases](https://www.debian.org/releases/stable/).
- [Categorias de release do kernel](https://www.kernel.org/category/releases.html).

## Kernel e interfaces

- [Documentação oficial do kernel Linux](https://docs.kernel.org/).
- [Guia do usuário e administrador do kernel](https://docs.kernel.org/admin-guide/).
- [Memory Management](https://docs.kernel.org/admin-guide/mm/).
- [Conceitos de memória](https://docs.kernel.org/admin-guide/mm/concepts.html).
- [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html).
- [Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html).
- [Projeto Linux man-pages](https://www.kernel.org/doc/man-pages/).
- [Interface `/proc`](https://man7.org/linux/man-pages/man5/proc.5.html).
- [Processo de desenvolvimento do kernel](https://docs.kernel.org/process/).
- [KernelNewbies](https://kernelnewbies.org/) — comunidade e material introdutório.

## Shell, comandos e padrões

- [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/).
- [GNU Coreutils](https://www.gnu.org/software/coreutils/manual/coreutils.html).
- [GNU grep](https://www.gnu.org/software/grep/manual/grep.html).
- [GNU sed](https://www.gnu.org/software/sed/manual/sed.html).
- [GNU awk](https://www.gnu.org/software/gawk/manual/).
- [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/).
- [Filesystem Hierarchy Standard 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html).
- [ShellCheck Wiki](https://www.shellcheck.net/wiki/).

## Inicialização e serviços

- [systemd: portal oficial](https://systemd.io/).
- [Manual pages do systemd](https://www.freedesktop.org/software/systemd/man/latest/).
- [Boot Loader Specification](https://uapi-group.org/specifications/specs/boot_loader_specification/).
- [Documentação GNU GRUB](https://www.gnu.org/software/grub/manual/grub/).
- [Udev](https://www.freedesktop.org/software/systemd/man/latest/udev.html).

## Distribuições

- [Releases Debian](https://www.debian.org/releases/).
- [Manual do administrador Debian](https://www.debian.org/doc/manuals/debian-handbook/).
- [Documentação Ubuntu Server](https://documentation.ubuntu.com/server/).
- [Ciclo de releases Ubuntu](https://ubuntu.com/about/release-cycle).
- [Documentação Fedora](https://docs.fedoraproject.org/).
- [Documentação RHEL](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/).
- [ArchWiki](https://wiki.archlinux.org/) — adapte instruções à sua distro.
- [Documentação openSUSE](https://doc.opensuse.org/).
- [Documentação Alpine](https://docs.alpinelinux.org/).
- [Sobre o Alpine](https://www.alpinelinux.org/about/).

## Armazenamento, rede e segurança

- [Documentação LVM](https://docs.kernel.org/admin-guide/device-mapper/).
- [Cryptsetup e LUKS](https://gitlab.com/cryptsetup/cryptsetup/-/wikis/home).
- [Documentação Btrfs](https://btrfs.readthedocs.io/).
- [Documentação XFS](https://docs.kernel.org/filesystems/xfs.html).
- [Manual iproute2](https://www.kernel.org/pub/linux/utils/net/iproute2/).
- [OpenSSH](https://www.openssh.com/manual.html).
- [nftables Wiki](https://wiki.nftables.org/).
- [SELinux User and Administrator Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_selinux/).
- [Documentação AppArmor](https://documentation.ubuntu.com/server/how-to/security/apparmor/).
- [Linux Audit](https://github.com/linux-audit/audit-documentation).

## Desempenho e observabilidade

- [Perf Wiki](https://perf.wiki.kernel.org/).
- [Kernel tracing](https://docs.kernel.org/trace/).
- [Pressure Stall Information](https://docs.kernel.org/accounting/psi.html).
- [BPF documentation](https://docs.kernel.org/bpf/).
- [Brendan Gregg: Linux Performance](https://www.brendangregg.com/linuxperf.html).

## Cursos e vídeos complementares

- [Introduction to Linux (LFS101), Linux Foundation](https://training.linuxfoundation.org/training/introduction-to-linux/).
- [Como instalar Linux em VM, Linux Foundation](https://training.linuxfoundation.org/resources/webinars/how-to-install-linux/).
- [Terminal no Linux, Curso em Vídeo](https://www.youtube.com/watch?v=mgs92GtkQCE).
- [Instalação avançada de programas, Curso em Vídeo](https://www.youtube.com/watch?v=HlbrYQqyXpg).
- [Dominando o terminal, Diolinux](https://www.youtube.com/watch?v=pPg1Pqh6GJE).
- [Gerenciamento de processos, Vagner Fonseca](https://www.youtube.com/watch?v=10gE9jXoP5Q).
- [Como funciona o systemd, Vagner Fonseca](https://www.youtube.com/watch?v=TGfXfuC3680).

## Fóruns e comunidades

- [Unix & Linux Stack Exchange](https://unix.stackexchange.com/).
- [Ask Ubuntu](https://askubuntu.com/).
- [Fedora Discussion](https://discussion.fedoraproject.org/).
- [Fóruns Debian](https://forums.debian.net/).
- [Arch Linux Forums](https://bbs.archlinux.org/).
- [KernelNewbies](https://kernelnewbies.org/).

Ao pedir ajuda, publique um exemplo mínimo, release, comando, saída saneada e o
que já foi testado. Nunca publique chave privada, token, endereço de cliente,
serial, dump irrestrito de ambiente ou core dump sem revisão.

## Como avaliar um tutorial

Antes de executar:

1. confira data, distro e release;
2. encontre a mesma opção no manual local;
3. identifique se o autor alterou arquivo gerado ou fonte de verdade;
4. verifique se existe backup, teste e rollback;
5. desconfie de `curl | sh`, `chmod 777`, desativar MAC/firewall e comandos
   destrutivos sem alvo validado;
6. reproduza primeiro em snapshot;
7. registre a diferença entre seu sistema e o tutorial.

Fóruns contêm diagnósticos valiosos, mas respostas antigas podem ser corretas
para outra release e erradas hoje. A resposta final deve apontar para evidência
do seu host e documentação correspondente.
