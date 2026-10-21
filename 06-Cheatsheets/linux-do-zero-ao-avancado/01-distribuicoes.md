# 01 — Linux, GNU, Unix e distribuições

## Objetivos

- separar kernel, user space, distribuição, família e variante;
- escolher uma distribuição por requisitos verificáveis, não por popularidade;
- comparar ciclo de suporte, modelo de atualização, libc, init e política;
- confirmar release e suporte em fontes oficiais antes de instalar.

## Kernel não é distribuição

O kernel Linux administra CPU, memória, dispositivos, processos, rede e
sistemas de arquivos. Um sistema utilizável adiciona bibliotecas, shell,
utilitários, init, gerenciador de pacotes e aplicativos. Uma distribuição
seleciona, integra, testa, assina e entrega esses componentes com políticas de
atualização e suporte.

- **Unix:** família histórica e marca/especificação; Linux é Unix-like, não
  deriva do código Unix original.
- **GNU:** projeto que fornece Bash, glibc, Coreutils, GCC e muitas ferramentas
  comuns em sistemas Linux.
- **POSIX:** conjunto de interfaces e comportamentos padronizados para aumentar
  portabilidade entre sistemas semelhantes a Unix.
- **Distribuição:** produto/projeto que integra kernel e user space.

## As decisões que realmente diferenciam distros

| Decisão | Exemplos | Consequência |
|---------|----------|--------------|
| Pacotes | DEB, RPM, `pacman`, `apk` | Comandos, formato e repositórios |
| Atualização | fixa, LTS, rolling | Novidade versus previsibilidade |
| Init | systemd, OpenRC | Serviços, logs e boot |
| libc | glibc, musl | Compatibilidade binária e comportamento |
| Segurança | AppArmor, SELinux | Política e ferramentas operacionais |
| Governança | comunidade, empresa, híbrida | Suporte, prioridades e ciclo |
| Filosofia | pronta, mínima, imutável | Quanto o usuário monta e altera |

## Famílias principais

### Debian, Ubuntu e derivados

Usam pacotes DEB, `dpkg` no nível baixo e APT para resolver dependências e
repositórios. Debian stable prioriza mudança controlada. Ubuntu publica versões
intermediárias e LTS, acrescentando integrações e suporte comercial. Mint e
Pop!_OS focam experiência desktop.

**Use quando:** quer ampla documentação, servidor generalista, desktop
iniciante ou base comum em cloud.

### Fedora, RHEL e derivados

Usam RPM e DNF. Fedora integra tecnologias recentes com ciclo curto. RHEL
transforma uma base amadurecida em plataforma empresarial de ciclo longo.
CentOS Stream acompanha o desenvolvimento imediatamente anterior ao RHEL;
Rocky e AlmaLinux buscam compatibilidade no ecossistema empresarial.

**Use quando:** quer aprender SELinux, RPM, Podman ou ambientes corporativos
baseados em RHEL.

### Arch e derivados

Arch é rolling release, minimalista e configurado pelo usuário. Usa `pacman`.
A documentação é excelente, mas instruções da ArchWiki precisam ser adaptadas
antes de serem usadas em outra distro. O AUR distribui receitas de build da
comunidade, não pacotes oficialmente auditados.

**Use quando:** já sabe recuperar o sistema e aceita acompanhar mudanças.

### openSUSE

Leap oferece base de mudança mais controlada; Tumbleweed é rolling com
snapshots testados. Usa RPM, Zypper e YaST; Btrfs e snapshots são comuns.

**Use quando:** quer boa administração integrada, RPM e rollback com Btrfs.

### Alpine

Alpine usa musl, BusyBox, `apk` e OpenRC. É pequena, mas essa diferença pode
expor incompatibilidades com software que presume glibc, extensões GNU ou
systemd.

**Use quando:** a pequena superfície e o ambiente minimalista são requisitos,
não apenas porque a imagem de container parece menor.

### Gentoo, NixOS e sistemas imutáveis

Gentoo enfatiza compilação e escolhas finas. NixOS descreve o sistema de forma
declarativa e cria gerações reproduzíveis. Fedora Silverblue, openSUSE Aeon e
outros desktops imutáveis separam a imagem-base das aplicações. São valiosos,
mas mudam o modelo mental de administração tradicional.

### Kali e outras distros especializadas

Kali é uma plataforma para testes de segurança autorizados. Tails prioriza
sessões amnésicas e privacidade. Proxmox foca virtualização. Escolher uma
distro especializada significa aceitar seu objetivo e suas restrições; não a
torna automaticamente melhor para desktop, desenvolvimento ou servidor.

## Stable, LTS e rolling

- **Release fixa:** conjunto de versões estabilizado; correções podem ser
  retroportadas sem elevar a versão exibida pelo software.
- **LTS:** compromisso de manutenção prolongada, cujo escopo varia por projeto e
  repositório.
- **Rolling:** atualiza continuamente os componentes; reduz grandes upgrades,
  mas exige acompanhar avisos e integrar mudanças menores com frequência.

Versão antiga não significa necessariamente vulnerável: mantenedores podem
aplicar um patch sem adotar a versão nova inteira. Consulte o advisory da
distro, não apenas um comparador de números.

## Recomendação em 2026

Na revisão de 30 de setembro de 2026, Ubuntu 26.04 é uma LTS e Debian 13
`trixie` é stable. Para este curso:

1. Ubuntu 26.04 LTS Desktop para a primeira VM;
2. Debian 13 minimal para o projeto de servidor;
3. Fedora atual em uma VM secundária para RPM/DNF e SELinux;
4. container Alpine para comparar musl, BusyBox e OpenRC;
5. Arch apenas depois do capítulo de recuperação.

Essa lista não substitui conferir ciclo de vida, compatibilidade do hardware,
imagem oficial e checksum no dia da instalação.

## Como decidir

Responda, nesta ordem:

1. O hardware e a arquitetura são suportados?
2. Até quando os repositórios usados recebem correções?
3. O software exigido é suportado pelo fornecedor?
4. A equipe domina o gerenciador, init e controle de acesso?
5. Existe caminho testado de upgrade e rollback?
6. Requisitos pedem suporte comercial, certificação ou FIPS?
7. A imagem veio do site oficial e sua integridade foi verificada?

## Laboratório comparativo

Em duas VMs ou containers, colete:

```bash
cat /etc/os-release
uname -r
getconf GNU_LIBC_VERSION 2>/dev/null || ldd --version 2>&1 | head -n 1
ps -p 1 -o comm=
command -v apt dnf zypper pacman apk 2>/dev/null
readlink -f /bin/sh
```

Monte uma tabela: kernel, libc, init, shell `/bin/sh`, pacotes e política de
release. Um container mostrará a distro do user space, mas `uname -r` ainda
mostrará o kernel do host.

## Exercícios

1. Escolha uma distro para notebook antigo, servidor de banco e container
   pequeno. Justifique sem usar “é a melhor”.
2. Explique por que comandos GNU podem ter opções ausentes no BusyBox.
3. Compare suporte oficial com popularidade da comunidade.
4. Descubra se cada repositório habilitado em sua VM faz parte do suporte
   padrão ou comunitário.

## Checklist de domínio

Você concluiu quando consegue explicar por que duas distribuições com o mesmo
kernel podem se comportar de forma diferente e escolher uma delas com critérios
verificáveis.
