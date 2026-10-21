# 02 — Instalação segura e primeira inicialização

## Objetivos

- autenticar a origem da imagem e verificar sua integridade;
- distinguir firmware, tabela de partição, partição e sistema de arquivos;
- instalar uma VM com acesso recuperável e estado inicial documentado;
- validar atualização, boot, relógio, montagem e serviços após instalar.

## Antes de baixar

Escolha somente o site oficial. Determine a arquitetura com base na CPU:
`amd64`/`x86_64` para PCs de 64 bits comuns, `arm64`/`aarch64` para ARM de 64
bits. Nomes variam entre projetos.

Baixe a ISO e o arquivo de checksums assinado. Um hash detecta corrupção apenas
se a lista usada como referência for autêntica. O fluxo correto é:

1. obter imagem, checksums e assinatura por canal oficial;
2. importar e conferir a chave pelo procedimento da distribuição;
3. verificar a assinatura do arquivo de checksums;
4. calcular o hash da ISO e compará-lo.

Exemplo genérico; use os nomes publicados pela distro:

```bash
sha256sum distro.iso
sha256sum --check SHA256SUMS 2>/dev/null | grep 'distro.iso: OK'
```

O segundo comando confirma consistência com a lista; ele não autentica a lista.

## VM antes de dual boot

Use VM durante o curso. Dual boot acrescenta riscos de redimensionamento,
bootloader, BitLocker/FileVault e firmware. Se futuramente usar máquina física:

- tenha backup verificado fora do disco;
- salve chaves de recuperação;
- desative inicialização rápida do outro sistema quando aplicável;
- saiba iniciar por mídia de recuperação;
- nunca redimensione uma partição sem confirmar o mapa e o backup.

## Firmware, UEFI e tabela de partição

Em hardware moderno, prefira UEFI com GPT. A ESP é uma pequena partição FAT
que armazena carregadores EFI; não é a mesma coisa que `/boot`. Secure Boot
valida componentes do caminho de inicialização quando a distro e os módulos
usados possuem assinaturas compatíveis.

Para a VM de estudos, um esquema simples basta:

| Montagem | Tamanho | Observação |
|----------|---------|------------|
| ESP | 512 MiB | FAT32, somente em UEFI |
| `/` | restante | ext4 ou padrão da distro |
| swap | arquivo | flexível para a VM |

Partições separadas para `/home`, `/var` e `/tmp` podem impor limites e
facilitar algumas operações, mas também criam risco de dimensionamento ruim.
Adote-as por requisito, não por ritual.

## Escolhas do instalador

- hostname sem dados pessoais, por exemplo `linux-lab`;
- usuário administrativo distinto de `root`;
- senha longa e exclusiva;
- fuso horário e layout corretos;
- criptografia de disco em notebook ou mídia transportável;
- somente os componentes necessários;
- atualizações de segurança habilitadas de acordo com a política do ambiente;
- SSH desabilitado até o capítulo 18, se não houver necessidade.

Criptografia protege dados em repouso quando a máquina está desligada. Não
protege uma sessão já desbloqueada nem substitui backup.

## Primeira inicialização

Colete estado antes de alterar:

```bash
cat /etc/os-release
uname -r
uname -m
hostnamectl 2>/dev/null || hostname
timedatectl 2>/dev/null || date
lsblk -f
findmnt
ip -brief address 2>/dev/null || true
systemctl --failed 2>/dev/null || true
```

Atualize usando apenas o gerenciador da família:

```bash
# Debian/Ubuntu
sudo apt update
sudo apt full-upgrade

# Fedora
sudo dnf upgrade --refresh

# Arch: upgrade completo; nunca sincronize e atualize apenas um pacote-base
sudo pacman -Syu

# Alpine
sudo apk update
sudo apk upgrade
```

Leia a transação antes de confirmar. Não misture repositórios de releases ou
famílias diferentes.

## Estado reproduzível

Guarde em seu diário:

- URL e data da imagem;
- hash verificado;
- firmware UEFI ou BIOS legado;
- CPU, RAM, disco e tipo de rede da VM;
- seleção de pacotes;
- mapa de partições;
- saída do diagnóstico inicial;
- nome e momento dos snapshots.

## Exercícios

1. Crie um arquivo de evidência na VM.
2. Tire um snapshot.
3. Modifique e remova o arquivo.
4. Restaure o snapshot.
5. Confirme o conteúdo e registre quanto demorou.

Depois, repita a coleta inicial e produza uma tabela com esperado, observado e
ação para qualquer divergência. Explique ainda por que checksum sem assinatura
autêntica não prova a procedência da imagem.

Um snapshot não é backup quando reside no mesmo armazenamento da VM. Aqui ele
serve para praticar reversão rápida.

## Checklist de domínio

- [ ] Verifiquei origem e integridade da ISO.
- [ ] Sei diferenciar UEFI, GPT, ESP, `/boot` e filesystem raiz.
- [ ] A VM está atualizada e `systemctl --failed` foi investigado.
- [ ] Testei restauração de snapshot.
- [ ] Registrei todas as escolhas sem armazenar segredos.
