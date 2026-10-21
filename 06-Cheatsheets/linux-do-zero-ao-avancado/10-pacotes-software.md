# 10 — Pacotes, repositórios e software

## Objetivos

- consultar propriedade, origem, dependências e versão de um pacote;
- explicar a cadeia de confiança de metadados, chaves e repositórios;
- planejar atualização e rollback sem misturar fontes incompatíveis;
- distinguir pacote do sistema, formato autocontido e dependência de projeto.

## O que um gerenciador resolve

Um pacote registra arquivos, versão, dependências, scripts e metadados. O
gerenciador de alto nível escolhe um conjunto compatível em repositórios,
verifica assinaturas e executa uma transação. Instalar um arquivo manualmente
fora desse modelo transfere para você atualização, inventário e remoção.

## Mapa entre famílias

| Tarefa | Debian/Ubuntu | Fedora/RHEL | Arch | openSUSE | Alpine |
|--------|---------------|-------------|------|----------|--------|
| atualizar índice | `apt update` | integrado | integrado | `zypper refresh` | `apk update` |
| atualizar sistema | `apt full-upgrade` | `dnf upgrade` | `pacman -Syu` | `zypper update` | `apk upgrade` |
| instalar | `apt install P` | `dnf install P` | `pacman -S P` | `zypper install P` | `apk add P` |
| remover | `apt remove P` | `dnf remove P` | `pacman -R P` | `zypper remove P` | `apk del P` |
| procurar | `apt search T` | `dnf search T` | `pacman -Ss T` | `zypper search T` | `apk search T` |

Esses comandos não possuem semântica perfeitamente equivalente. Leia a
transação e a documentação da família.

## Consultar sem alterar

```bash
# Debian/Ubuntu
apt-cache policy bash
dpkg-query -S /bin/bash
dpkg-query -L bash | head

# Fedora/RHEL
dnf info bash
rpm -qf /bin/bash
rpm -ql bash | head
```

Perguntas operacionais essenciais: qual pacote possui este arquivo, qual
repositório fornece a versão, quais dependências serão alteradas e qual advisory
corrige uma falha.

## Confiança no repositório

Assinatura confirma que metadados/pacotes vieram de uma chave aceita e não
foram modificados; não garante ausência de bugs. Adicione somente repositórios
necessários, com chave escopada e instruções atuais. Evite padrões antigos que
confiam globalmente em qualquer pacote assinado por uma chave de terceiro.

Antes de habilitar um repositório, registre:

1. proprietário e URL oficial;
2. distribuições e arquiteturas suportadas;
3. fingerprint obtida por canal independente;
4. escopo da chave;
5. política de atualização e remoção;
6. como retornar aos pacotes oficiais.

## Atualizações seguras

- leia notas de release e mudanças incompatíveis;
- tenha backup e rollback testados;
- atualize primeiro um ambiente de teste;
- não interrompa transação;
- trate arquivos de configuração divergentes conscientemente;
- reinicie serviços/processos que ainda usam bibliotecas antigas;
- reinicie no novo kernel quando necessário e valide o boot anterior como fallback.

```bash
checkrestart 2>/dev/null || true
needs-restarting -r 2>/dev/null || true
```

Ferramentas variam por distro e podem exigir pacote adicional.

## Flatpak, Snap, AppImage e linguagem

- Flatpak foca aplicativos desktop e permissões/sandbox;
- Snap empacota aplicações com serviço e modelo próprios;
- AppImage é um artefato executável autocontido, sem atualização universal;
- `pip`, npm, Maven e NuGet gerenciam dependências de projetos, não devem
  substituir indiscriminadamente o gerenciador do sistema.

Isolamento não é absoluto. Revise origem, permissões, atualização e integração.

## Compilar da fonte

Faça em conta comum e use diretório de staging:

```bash
tar -xf projeto.tar.gz
cd projeto
./configure --prefix=/usr/local
make -j"$(getconf _NPROCESSORS_ONLN)"
make check
make DESTDIR="$PWD/stage" install
find stage -type f -print
```

O fluxo varia (CMake, Meson, Cargo etc.). Leia `README`/`INSTALL`, verifique
assinatura/tag, fixe a versão, teste e crie pacote nativo quando a instalação
precisar ser administrável. Nunca execute `curl ... | sudo sh` sem baixar,
inspecionar, autenticar e entender o script.

## Bibliotecas dinâmicas

```bash
file /bin/ls
ldd /bin/ls
ldconfig -p 2>/dev/null | head
readelf -d /bin/ls 2>/dev/null | grep NEEDED
```

`ldd` pode executar mecanismos do loader em certos cenários; não o use em
binário não confiável. Prefira inspeção estática com `readelf`/`objdump` nesse
caso.

## Exercícios

1. Encontre o pacote dono de cinco arquivos e liste sua origem.
2. Simule uma instalação e explique cada dependência proposta.
3. Compare uma aplicação nativa, Flatpak e AppImage em atualização e permissões.
4. Compile um programa pequeno para `stage` sem instalar no sistema.

## Checklist de domínio

Consigo instalar, auditar, atualizar e remover software mantendo origem,
integridade, dependências e reversão visíveis.
