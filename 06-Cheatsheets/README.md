# 06 — Linux: do zero ao kernel

> Formação autocontida para usar, administrar, diagnosticar, proteger e
> compreender Linux. A pasta mantém o nome histórico para preservar links, mas
> este módulo é um curso progressivo, não uma coleção de comandos rápidos.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Iniciantes em Linux até estudantes que desejam compreender administração, memória e kernel. |
| Pré-requisitos | Módulos 00–05; executar comandos, ler código e interpretar status de saída. |
| Tempo estimado | 360–520 horas de leitura, 64 práticas, seis laboratórios e capstone. |
| Ambiente | VM Linux própria; disco, boot, módulos e kernel somente em clone descartável. |
| Evidência final | Duas VMs reproduzíveis, serviço local operável, diagnóstico e restauração comprovada. |
| Critério de conclusão | Laboratórios concluídos, testes locais aprovados e ao menos 75 pontos no capstone. |

## O que você será capaz de fazer

Ao concluir, você conseguirá:

- escolher uma distribuição por requisitos, suporte e modelo de atualização;
- verificar imagem, instalar, atualizar e recuperar uma VM;
- trabalhar com shell, arquivos, texto, permissões, contas e pacotes;
- explicar processos, sinais, descritores, memória virtual, cache, swap e OOM;
- administrar filesystem, LVM, RAID, LUKS, boot, systemd e journal;
- operar SSH e listeners locais sem antecipar o currículo de Redes;
- escrever automações Bash previsíveis, idempotentes e testadas;
- diagnosticar por evidências antes de reiniciar ou alterar;
- restaurar dados e serviço com RPO e RTO medidos;
- aplicar hardening proporcional com teste e rollback;
- explicar namespaces, cgroups, containers, syscalls, VFS e drivers;
- observar kernel e desempenho escolhendo ferramenta por pergunta e risco;
- reconstruir e defender um sistema Linux reproduzível.

## Qual distribuição usar

Para a primeira passagem, use Ubuntu 26.04 LTS em VM. A página oficial de ciclo
de releases confirma que ela é uma LTS lançada em abril de 2026. Debian 13,
codinome trixie, é a alternativa recomendada para a VM de servidor; a página
oficial de releases o identifica como stable. Em 11 de outubro de 2026, a
atualização publicada é Debian 13.7.

Depois, repita práticas escolhidas no Fedora atual para aprender RPM, DNF e
SELinux, e em Alpine para comparar musl, BusyBox e OpenRC. Arch, openSUSE, RHEL
e derivados entram como estudos comparativos. Kali é uma distribuição
especializada e não é a base recomendada para aprender administração geral.

Versões e suporte mudam. Confirme sempre no dia da instalação:

- [ciclo de releases Ubuntu](https://ubuntu.com/about/release-cycle);
- [releases Debian](https://www.debian.org/releases/);
- [informações da Debian stable](https://www.debian.org/releases/stable/).

O capítulo [Distribuições e escolhas](linux-do-zero-ao-avancado/01-distribuicoes.md)
ensina como tomar a decisão sem depender destes exemplos.

## Rota completa

### Etapa 1 — entrar no sistema

1. [Como estudar e montar o laboratório](linux-do-zero-ao-avancado/00-como-estudar-laboratorio.md).
2. [Linux, GNU, Unix e distribuições](linux-do-zero-ao-avancado/01-distribuicoes.md).
3. [Instalação segura](linux-do-zero-ao-avancado/02-instalacao.md).
4. [Arquitetura Linux](linux-do-zero-ao-avancado/03-arquitetura-linux.md).
5. [Terminal e documentação](linux-do-zero-ao-avancado/04-terminal-ajuda.md).
6. [Sistema de arquivos](linux-do-zero-ao-avancado/05-sistema-arquivos.md).
7. [Manipulação de arquivos](linux-do-zero-ao-avancado/06-manipulacao-arquivos.md).
8. [Texto, fluxos e editores](linux-do-zero-ao-avancado/07-texto-fluxos-editores.md).
9. [Permissões](linux-do-zero-ao-avancado/08-permissoes.md).
10. [Lab 01 — shell, arquivos e permissões](linux-do-zero-ao-avancado/laboratorios/lab-01-shell-arquivos-permissoes.md).

### Etapa 2 — dominar o espaço de usuário

1. [Usuários, autenticação e sudo](linux-do-zero-ao-avancado/09-usuarios-autenticacao.md).
2. [Pacotes e software](linux-do-zero-ao-avancado/10-pacotes-software.md).
3. [Processos, threads e sinais](linux-do-zero-ao-avancado/11-processos-sinais.md).
4. [Memória virtual](linux-do-zero-ao-avancado/12-memoria.md).
5. [Lab 02 — identidades, processos e memória](linux-do-zero-ao-avancado/laboratorios/lab-02-identidades-processos-memoria.md).

### Etapa 3 — administrar a máquina

1. [Armazenamento](linux-do-zero-ao-avancado/13-armazenamento.md).
2. [LVM, RAID e criptografia](linux-do-zero-ao-avancado/14-lvm-raid-criptografia.md).
3. [Boot e initramfs](linux-do-zero-ao-avancado/15-boot.md).
4. [systemd, timers e journal](linux-do-zero-ao-avancado/16-systemd.md).
5. [Lab 03 — armazenamento, boot e systemd](linux-do-zero-ao-avancado/laboratorios/lab-03-armazenamento-boot-systemd.md).

### Etapa 4 — operar com segurança

1. [Interfaces de conectividade no host](linux-do-zero-ao-avancado/17-redes-linux.md).
2. [SSH e administração remota](linux-do-zero-ao-avancado/18-ssh-remoto.md).
3. [Bash e automação](linux-do-zero-ao-avancado/19-bash-automacao.md).
4. [Observabilidade e troubleshooting](linux-do-zero-ao-avancado/20-observabilidade.md).
5. [Backup e recuperação](linux-do-zero-ao-avancado/21-backup-recuperacao.md).
6. [Hardening](linux-do-zero-ao-avancado/22-hardening.md).
7. [Namespaces, cgroups e containers](linux-do-zero-ao-avancado/23-isolamento-containers.md).
8. [Guia de diagnóstico](linux-do-zero-ao-avancado/GUIA-DIAGNOSTICO.md).
9. [Lab 04 — operação, hardening e isolamento](linux-do-zero-ao-avancado/laboratorios/lab-04-operacao-hardening-isolamento.md).

O capítulo 17 trata somente da interface do sistema operacional com sockets e
gerenciadores do host. Endereçamento, DNS, protocolos, switching, VLAN,
roteamento, VPN, firewall e infraestrutura ficam nos módulos 14 a 18.

### Etapa 5 — compreender o kernel e operar profissionalmente

1. [Kernel e syscalls](linux-do-zero-ao-avancado/24-kernel.md).
2. [Módulos, drivers e dispositivos](linux-do-zero-ao-avancado/25-modulos-dispositivos.md).
3. [Build e debug de kernel](linux-do-zero-ao-avancado/26-kernel-build-debug.md).
4. [Desempenho e capacidade](linux-do-zero-ao-avancado/27-desempenho.md).
5. [Desktop, áudio e energia](linux-do-zero-ao-avancado/28-desktop.md).
6. [Operação de serviços](linux-do-zero-ao-avancado/29-servicos.md).
7. [Lab 05 — kernel, desempenho e serviços](linux-do-zero-ao-avancado/laboratorios/lab-05-kernel-desempenho-servicos.md).

### Etapa 6 — integrar

1. [Caderno com 64 práticas](linux-do-zero-ao-avancado/CADERNO-PRATICAS.md).
2. [Projeto e avaliação](linux-do-zero-ao-avancado/30-projeto-final.md).
3. [Host Observer — projeto de referência](linux-do-zero-ao-avancado/projetos/host-observer/README.md).
4. [Lab 06 — capstone Linux](linux-do-zero-ao-avancado/laboratorios/lab-06-capstone-linux.md).

## Segurança dos comandos

Nos exemplos, o prompt de usuário comum e o prompt administrativo não fazem
parte do comando. Privilégio não corrige um comando errado. Antes de alterar
boot, montagem, partição, conta, service manager ou kernel:

1. confirme a VM e o alvo exato;
2. crie snapshot e teste a restauração;
3. mantenha console fora do serviço alterado;
4. registre estado anterior, teste e rollback;
5. use arquivo-imagem, nunca dispositivo real, nos exercícios de disco;
6. interrompa se uma variável resolver para alvo amplo.

O executor automático nunca usa sudo, não instala units, não carrega módulos e
trabalha apenas em diretório temporário.

## Código real

Os [exemplos executáveis](linux-do-zero-ao-avancado/exemplos/README.md) incluem
Bash seguro, agregação AWK, comparação Python de baselines, backup versionado,
programas C sobre processos, memória e syscalls, unidades systemd e módulo
didático de kernel.

Execute a suíte:

~~~bash
bash 06-Cheatsheets/linux-do-zero-ao-avancado/testar-curso.sh
~~~

Ela compila com avisos como erro quando há compilador, testa contratos, valida
units quando a ferramenta existe e confere links Markdown locais.

## Recursos de apoio

- [folha de consulta](linux-do-zero-ao-avancado/CHEATSHEET.md);
- [glossário](linux-do-zero-ao-avancado/GLOSSARIO.md);
- [respostas comentadas](linux-do-zero-ao-avancado/RESPOSTAS.md);
- [referências oficiais e comunidades](linux-do-zero-ao-avancado/REFERENCIAS.md);
- [índice dos laboratórios](linux-do-zero-ao-avancado/laboratorios/README.md).

Os capítulos são suficientes para concluir a formação. Referências e vídeos
servem para confirmar comportamento da versão instalada e observar outras
explicações.

## Critério de conclusão

- [ ] Trabalho no terminal preservando argumentos e códigos de saída.
- [ ] Explico inode, descritor, processo, thread, syscall e memória virtual.
- [ ] Administro contas, pacotes, filesystems, systemd, SSH local e backups.
- [ ] Diagnostico por linha do tempo e hipótese antes de reiniciar.
- [ ] Aplico hardening com teste funcional e rollback.
- [ ] Relaciono syscall, VFS, page cache, driver e hardware.
- [ ] Concluí seis laboratórios e restaurei o capstone em servidor vazio.
- [ ] Sei encaminhar assuntos de rede aos módulos 14 a 18 sem fingir domínio.

## Continuação

O módulo 07 aprofunda internals e administração Linux. Redes começam no módulo
14. Escalação de privilégios e movimento lateral pertencem aos módulos
[36](../36-Escalacao-Privilegios/README.md) e
[37](../37-Pos-Exploracao-Movimento-Lateral/README.md), depois da base.
