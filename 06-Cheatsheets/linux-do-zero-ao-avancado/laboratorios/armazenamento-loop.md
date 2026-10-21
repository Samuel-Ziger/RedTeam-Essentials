# Laboratório C01 — armazenamento em arquivo loop

> Exclusivamente em clone descartável da VM. Os comandos de formatação apagam
> o alvo. Digite o caminho; não transforme este roteiro em script automático.

## Objetivo

Construir e explicar:

```text
arquivo de 2 GiB → loop device → LUKS → PV → VG → LV → ext4 → mount
```

Depois, criar dados sintéticos, desmontar, remontar, crescer e destruir somente
a pilha criada.

## Pré-condições

- snapshot chamado `antes-storage-c01`;
- console da VM aberto;
- nenhum dado real;
- pacotes `cryptsetup`, `lvm2` e ferramentas ext4 da distro;
- 3 GiB livres em `/var/tmp`;
- saída inicial de `lsblk -f`, `findmnt`, `pvs`, `vgs`, `lvs` salva.

## Criar o arquivo

```bash
lab_dir=$(mktemp -d /var/tmp/linux-storage-c01.XXXXXX)
chmod 0700 "$lab_dir"
truncate -s 2G "$lab_dir/disk.img"
ls -lh "$lab_dir/disk.img"
du -h "$lab_dir/disk.img"
```

Ele é esparso; tamanho aparente e blocos alocados diferem.

## Associar loop e validar

```bash
loop_device=$(sudo losetup --find --show "$lab_dir/disk.img")
printf 'ALVO=%s\n' "$loop_device"
sudo losetup --list --output NAME,BACK-FILE,SIZELIMIT,OFFSET | grep -F "$lab_dir/disk.img"
lsblk -o NAME,PATH,TYPE,SIZE,FSTYPE,MOUNTPOINTS "$loop_device"
```

Pare se:

- o alvo não começa por `/dev/loop`;
- o backing file não é exatamente `disk.img` deste lab;
- `findmnt --source "$loop_device"` encontra montagem inesperada;
- `lsblk` mostra filhos anteriores.

## Construir camadas

Somente depois das validações:

```bash
sudo cryptsetup luksFormat "$loop_device"
sudo cryptsetup open "$loop_device" curso_c01_crypt
sudo pvcreate /dev/mapper/curso_c01_crypt
sudo vgcreate curso_c01_vg /dev/mapper/curso_c01_crypt
sudo lvcreate -L 1G -n dados curso_c01_vg
sudo mkfs.ext4 -L CURSO_C01 /dev/curso_c01_vg/dados
sudo install -d -m 0750 /mnt/curso-c01
sudo mount /dev/curso_c01_vg/dados /mnt/curso-c01
```

Confirme cada camada com `lsblk -f`, `cryptsetup status`, `pvs`, `vgs`, `lvs` e
`findmnt`. Crie apenas texto sintético e hash.

## Crescer

Acrescente 256 MiB ao LV e depois ao ext4:

```bash
sudo lvextend -L +256M /dev/curso_c01_vg/dados
sudo resize2fs /dev/curso_c01_vg/dados
df -hT /mnt/curso-c01
```

Explique por que a ordem inversa seria incorreta. Não pratique redução neste
lab.

## Teardown na ordem inversa

```bash
sudo umount /mnt/curso-c01
sudo lvremove /dev/curso_c01_vg/dados
sudo vgremove curso_c01_vg
sudo pvremove /dev/mapper/curso_c01_crypt
sudo cryptsetup close curso_c01_crypt
sudo losetup --detach "$loop_device"
rmdir /mnt/curso-c01
rm -f -- "$lab_dir/disk.img"
rmdir -- "$lab_dir"
```

Antes de cada linha, confirme que o nome tem prefixo exclusivo `curso_c01` e o
loop ainda aponta ao arquivo. Compare o inventário final ao inicial.

## Critério

O diagrama e a saída devem mostrar a relação de cada camada. A conclusão explica
por que LUKS, LVM, filesystem e backup resolvem problemas diferentes.
