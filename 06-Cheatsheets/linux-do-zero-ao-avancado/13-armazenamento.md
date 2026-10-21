# 13 — Discos, partições e sistemas de arquivos

## Objetivos

- mapear aplicação, VFS, filesystem, camada de bloco e dispositivo;
- inventariar discos e montagens por identificadores persistentes;
- escolher filesystem por requisitos de carga, suporte e recuperação;
- investigar capacidade, inodes, integridade e arquivos removidos ainda abertos.

## Da aplicação ao meio

```text
aplicação → syscall → VFS → filesystem → page cache/writeback
          → camada de bloco → driver/controlador → dispositivo
```

Dispositivo de bloco oferece blocos endereçáveis. Partição divide o espaço;
filesystem organiza nomes e metadados; ponto de montagem conecta o filesystem
à árvore. Nenhum desses termos é sinônimo de “disco”.

## Inventário somente leitura

```bash
lsblk -e7 -o NAME,PATH,TYPE,SIZE,FSTYPE,FSVER,LABEL,UUID,MOUNTPOINTS
findmnt --real
blkid 2>/dev/null
cat /proc/partitions
```

Nomes `/dev/sda`, `/dev/vda` e `/dev/nvme0n1` dependem de driver e ordem de
detecção. Para configuração persistente, prefira UUID, LABEL ou caminhos
estáveis de `/dev/disk/by-*`, conforme o caso.

## Setor, alinhamento e tabelas

Dispositivos expõem tamanhos lógico e físico. Partições desalinhadas podem
amplificar I/O. GPT é a escolha moderna e carrega identificadores e cópia de
metadados; MBR possui limitações históricas.

```bash
lsblk -o NAME,LOG-SEC,PHY-SEC,MIN-IO,OPT-IO,ALIGNMENT
sudo fdisk -l          # apenas lista
sudo parted -l        # apenas lista
```

Não execute comandos de criação em um dispositivo real neste curso. O lab usa
arquivo-imagem e dispositivo loop validado.

## Escolher filesystem

| Filesystem | Força comum | Atenção |
|------------|-------------|----------|
| ext4 | generalista, maduro, ampla recuperação | menos recursos integrados que Btrfs |
| XFS | escala, paralelismo e arquivos grandes | não reduz filesystem; ferramentas próprias |
| Btrfs | checksums, subvolumes, snapshots, compressão | exige entender perfis, scrub e espaço |
| FAT/exFAT | intercâmbio e ESP | sem permissões Unix nativas equivalentes |
| tmpfs | dados voláteis apoiados por memória/swap | consome recursos de memória |

ZFS é um ecossistema avançado fora da árvore principal do kernel, com
modelo integrado de pool, volume, filesystem, checksums e snapshots. Use
pacotes e orientação da distribuição.

Escolha por carga, tamanho, suporte, recuperação, crescimento, checksums,
snapshots e competência da equipe — não por benchmark isolado.

## Montagem

```bash
findmnt -T /var
findmnt -no SOURCE,FSTYPE,OPTIONS /
mountpoint /boot 2>/dev/null || true
```

Opções frequentes:

- `ro`/`rw`: somente leitura/leitura-escrita;
- `nodev`: não interpretar nós de dispositivo;
- `nosuid`: ignorar setuid/setgid de executáveis;
- `noexec`: impedir exec direto, mas não é fronteira completa contra código;
- `noatime`/`relatime`: política de timestamp de acesso;
- `discard`: TRIM contínuo, cuja escolha deve considerar dispositivo e distro.

## `/etc/fstab`

Cada linha descreve origem, ponto, tipo, opções, dump e ordem de fsck:

```text
UUID=EXEMPLO  /srv/dados  ext4  defaults,nodev,nosuid  0  2
```

Antes de reiniciar após editar uma VM:

```bash
sudo findmnt --verify --verbose
sudo mount --all --fake --verbose
systemctl daemon-reload
```

A simulação não prova disponibilidade futura do dispositivo. Mantenha console
de recuperação. Em systemd, entradas geram units e opções `x-systemd.*` podem
expressar automount, timeout e dependências.

## Uso e arquivos apagados ainda abertos

```bash
df -hT /
du -xhd1 /var 2>/dev/null | sort -h
lsof +L1 2>/dev/null | head
```

`df` mede o filesystem; `du` soma entradas alcançáveis. Diferença pode vir de
arquivo removido ainda aberto, blocos reservados, snapshots, metadados ou
montagem escondendo conteúdo.

## Integridade, SMART e TRIM

- filesystem journal reduz inconsistência após queda, mas não é backup;
- `fsck` deve seguir as regras do filesystem, geralmente desmontado;
- `smartctl`/`nvme` expõem saúde e erros, sem prever toda falha;
- `fstrim` informa blocos livres a SSD/armazenamento compatível;
- Btrfs/ZFS scrub verificam checksums, mas correção depende de redundância.

```bash
systemctl status fstrim.timer 2>/dev/null || true
sudo smartctl -a /dev/DISPOSITIVO_DO_LAB   # placeholder: não copie literalmente
```

## Quotas

Quotas limitam uso por usuário, grupo ou projeto conforme filesystem e
configuração. Limites soft admitem período de graça; hard bloqueiam novo uso.
Elas controlam consumo, não garantem desempenho nem disponibilidade.

## Exercícios

1. Desenhe todas as camadas que sustentam `/home` na sua VM.
2. Explique divergência entre `df` e `du` e reproduza com arquivo aberto.
3. Compare ext4, XFS e Btrfs para banco transacional, servidor de arquivos e
   notebook; identifique informação que falta antes da decisão.
4. Valide uma entrada `fstab` baseada em UUID em VM descartável.

## Checklist de domínio

Consigo inventariar armazenamento sem confundir dispositivo, partição,
volume, filesystem e montagem, e nunca formato algo identificado só pelo nome.
