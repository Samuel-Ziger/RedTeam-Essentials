# 14 — LVM, RAID e criptografia

## Objetivos

- desenhar a ordem exata das camadas antes de alterar armazenamento;
- explicar PV, VG, LV, thin pool, snapshot e perfis de RAID;
- separar redundância, disponibilidade, confidencialidade e backup;
- crescer e recuperar uma pilha de laboratório com alvo validado.

## Composição de camadas

Uma pilha comum pode ser:

```text
discos → RAID → LUKS → PV → VG → LV → filesystem → montagem
```

A ordem não é universal. Criptografar cada membro antes do RAID, criptografar o
array ou usar LVM antes/depois de LUKS muda boot, substituição, visibilidade e
operação. Desenhe a camada antes de executar qualquer ferramenta.

## LVM

- **PV:** dispositivo disponibilizado ao LVM;
- **VG:** pool formado por um ou mais PVs;
- **LV:** dispositivo lógico alocado no VG;
- **PE/LE:** unidades de alocação física/lógica.

```bash
sudo pvs
sudo vgs
sudo lvs -a -o +devices,segtype,data_percent,metadata_percent
```

LVM permite crescer e reorganizar volumes. Reduzir é mais perigoso e depende
do filesystem: XFS, por exemplo, não oferece redução tradicional. Cresça em
ordem: camada inferior, LV e filesystem. Para reduzir, filesystem compatível
vem antes do LV, offline quando exigido, sempre com backup.

### Thin provisioning e snapshots

Thin LVs alocam blocos sob demanda; oversubscription exige monitoramento de
dados e metadados. Ao esgotar o pool, múltiplos volumes falham. Snapshot LVM
tradicional usa copy-on-write e pode invalidar se o espaço reservado acabar.
Snapshot facilita consistência e rollback curto, mas não é backup independente.

## RAID

| Nível | Ideia | Tolera falha | Observação |
|-------|-------|--------------|------------|
| 0 | striping | nenhuma | desempenho/capacidade, sem redundância |
| 1 | espelho | membro(s), conforme conjunto | leitura e simplicidade |
| 5 | paridade simples | um membro | write penalty e rebuild arriscado em grandes arrays |
| 6 | paridade dupla | dois membros | mais segurança, maior custo |
| 10 | espelhos com striping | depende de quais membros | bom compromisso, exige mais discos |

RAID aumenta disponibilidade diante de certas falhas de dispositivo. Não
protege contra exclusão, corrupção propagada, ransomware, erro administrativo,
incêndio ou falha comum de controladora. Portanto, RAID não é backup.

```bash
cat /proc/mdstat
sudo mdadm --detail --scan 2>/dev/null
```

Monitore estado e teste substituição/rebuild no lab. Um array degradado que
ninguém observa é apenas uma falha adiada.

## LUKS/dm-crypt

LUKS guarda metadados e slots de chave; dm-crypt realiza a transformação de
blocos. Uma passphrase deriva uma chave que desbloqueia a chave de volume; ela
não criptografa diretamente cada bloco por si só.

```bash
lsblk -o NAME,TYPE,FSTYPE,MOUNTPOINTS
sudo cryptsetup status nome-do-mapeamento 2>/dev/null
sudo cryptsetup luksDump /dev/DISPOSITIVO_LOOP_DO_LAB  # somente imagem do lab
```

Proteções essenciais:

- backup seguro do header LUKS e teste de restauração;
- mais de um método autorizado de recuperação, sob controle separado;
- passphrase forte e proteção de chaves;
- descarte/hibernação avaliados no modelo de ameaça;
- initramfs e boot considerados na rota de desbloqueio;
- remoção de slot somente depois de confirmar outro slot funcional.

Criptografia em repouso não impede leitura por um processo autorizado depois do
desbloqueio e não oferece por si só integridade completa, backup ou controle de
acesso entre usuários logados.

## Laboratório seguro

Use [laboratórios de armazenamento](laboratorios/README.md) em uma VM
descartável. O alvo deve ser um arquivo criado naquele lab e associado a um
`/dev/loopN` confirmado por `losetup --list`. O roteiro deve abortar se o alvo
não for `loop`, estiver montado fora do diretório do lab ou contiver o root.

Nunca use `/dev/sda`, `/dev/nvme0n1`, glob ou variável vazia em um exemplo de
`pvcreate`, `mdadm --create`, `cryptsetup luksFormat` ou `mkfs`.

## Falhas e recuperação

Antes de uma mudança, capture:

```bash
lsblk -f
findmnt
sudo pvs --reportformat json 2>/dev/null
sudo vgs --reportformat json 2>/dev/null
sudo lvs --reportformat json 2>/dev/null
```

Conheça backups automáticos de metadados do LVM em `/etc/lvm/backup` e
`/etc/lvm/archive`, mas não os trate como cópia dos dados. Para RAID, documente
ordem, UUIDs e layout. Para LUKS, mantenha header e chaves fora do mesmo disco.

## Exercícios

1. Desenhe duas ordens LUKS/LVM e compare o que fica visível sem desbloqueio.
2. Calcule capacidade e tolerância aproximada de RAID 1, 5, 6 e 10.
3. Explique por que snapshot, RAID, replicação e backup são quatro coisas.
4. Em VM descartável, crie dois arquivos-imagem, monte uma pilha e destrua-a
   seguindo o roteiro de teardown.

## Checklist de domínio

Consigo desenhar uma pilha, prever domínio de falha, monitorar esgotamento e
recuperar metadados sem confundir disponibilidade, confidencialidade e backup.
