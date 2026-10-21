# Laboratório C02 — boot e recuperação

> Use clone descartável, snapshot e console do hypervisor. Não use acesso SSH
> como único caminho de recuperação.

## Parte 1 — mapear

Colete:

```bash
test -d /sys/firmware/efi && echo UEFI || echo legado
findmnt / /boot /boot/efi 2>/dev/null
cat /proc/cmdline
ls -lh /boot
ps -p 1 -o pid,comm,args
systemd-analyze critical-chain
journalctl --list-boots
```

Desenhe firmware, ESP, bootloader, kernel, initramfs, raiz e PID 1.

## Parte 2 — falha não essencial no fstab

Crie um arquivo-imagem pequeno e um mount de laboratório seguindo as barreiras
do C01. Adicione a entrada por UUID com `nofail,x-systemd.device-timeout=5s` e
valide. Depois, troque **somente o UUID dessa entrada de lab** por um UUID
inexistente.

Objetivo: observar timeout controlado sem impedir boot, localizar a unit gerada,
ler journal, corrigir e validar. Isso ensina dependência sem tornar a VM
inicializável.

## Parte 3 — entrada temporária

No menu de boot, edite temporariamente a linha do kernel para entrar em
`systemd.unit=rescue.target`. Não persista. Registre:

- quais filesystems estavam montados;
- quais serviços existiam;
- qual rede estava ativa;
- como voltar ao target padrão.

## Parte 4 — mídia de resgate

Inicie pela ISO da distro, identifique a raiz da VM sem montar automaticamente
outros discos, monte sob `/mnt/resgate`, depois monte ESP/boot conforme layout.
Pratique entrar em `chroot` seguindo o guia da distro e sair/desmontar em ordem.

Não reinstale bootloader se ele não está quebrado. O objetivo é aprender o
ambiente, não executar toda ferramenta de reparo.

## Critério

Entregue uma árvore de decisão: firmware não encontra entrada; bootloader não
encontra kernel; kernel não encontra root; initramfs não desbloqueia; systemd
entra em emergency; serviço final falha. Para cada etapa, indique evidência e
recuperação.
