# 15 — UEFI, bootloader e initramfs

## Objetivos

- narrar o boot do firmware até o PID 1 e o serviço final;
- localizar configuração, artefatos e logs de cada etapa;
- diferenciar parâmetro temporário, configuração persistente e imagem initramfs;
- recuperar uma falha controlada usando console e entrada anterior.

## Sequência completa

```text
energia/reset
  → firmware (UEFI/BIOS) e hardware
  → entrada de boot / bootloader
  → kernel + linha de comando + initramfs
  → descoberta da raiz real
  → switch_root
  → PID 1
  → unidades, serviços e login
```

Diagnosticar boot exige localizar a etapa em que a progressão parou.

## UEFI e ESP

UEFI lê executáveis na EFI System Partition (ESP). Entradas persistem em NVRAM.

```bash
test -d /sys/firmware/efi && echo UEFI || echo BIOS-ou-container
findmnt /boot /boot/efi 2>/dev/null
sudo efibootmgr -v 2>/dev/null
```

Secure Boot cria uma cadeia de verificação. Módulos externos podem precisar
ser assinados; desativar Secure Boot apenas para contornar um erro remove um
controle sem corrigir a cadeia.

## Bootloaders

GRUB é comum e suporta múltiplos filesystems/OS. systemd-boot é mais simples e
se integra ao modelo Boot Loader Specification em UEFI. A distro gera
configuração a partir de arquivos-fonte: não edite cegamente um arquivo gerado,
pois a próxima atualização pode sobrescrevê-lo.

```bash
bootctl status 2>/dev/null || true
grep -E '^[^#]' /etc/default/grub 2>/dev/null
ls -l /boot
```

Mantenha ao menos um kernel anterior funcional e saiba selecioná-lo.

## Linha de comando do kernel

```bash
cat /proc/cmdline
```

Parâmetros informam raiz, console, modo de recuperação, LSM e ajustes. Uma
alteração temporária no menu é melhor para teste; persista apenas depois de
validar. Parâmetros podem reduzir segurança ou impedir boot.

## Initramfs

Initramfs é um pequeno user space em memória que carrega drivers e ferramentas
necessários para localizar/desbloquear/montar a raiz real. Pode conter suporte
a LVM, RAID, LUKS, rede e storage especial.

```bash
lsinitramfs "/boot/initrd.img-$(uname -r)" 2>/dev/null | head
lsinitrd 2>/dev/null | head
```

Depois de mudar armazenamento, driver ou configuração exigida antes da raiz,
regenere initramfs com a ferramenta da distro e confira o arquivo gerado.

## systemd no boot

```bash
systemd-analyze
systemd-analyze critical-chain
systemd-analyze blame | head -n 20
systemctl --failed
journalctl -b -p warning
journalctl -b -1 2>/dev/null | tail
```

`blame` mede tempo de ativação percebido, não prova que uma unidade atrasou o
caminho crítico. Use `critical-chain` e dependências.

## Alvos e modos de recuperação

Targets agrupam estados: `multi-user.target`, `graphical.target`,
`rescue.target` e `emergency.target`. Rescue oferece mais serviços; emergency
é ambiente mínimo. Use console da VM e documentação da distro.

Recuperação típica:

1. registrar a mensagem exata e última etapa;
2. tentar kernel anterior/entrada conhecida;
3. editar temporariamente a linha de boot para diagnóstico;
4. iniciar mídia de resgate se a raiz não monta;
5. identificar, desbloquear e montar a raiz e a ESP;
6. corrigir `fstab`, pacote, initramfs ou bootloader;
7. validar configuração antes de reiniciar;
8. preservar logs e documentar a causa.

`chroot` troca a raiz percebida para processos, mas não cria VM/container e
pode exigir montar `/dev`, `/proc`, `/sys` e `/run` corretamente.

## Kernel panic e emergency shell

Panic é falha irrecuperável do kernel; “failed to mount” em user space não é
automaticamente panic. Capture console serial, `pstore` ou kdump quando
configurados. Em initramfs shell, examine `/proc/cmdline`, dispositivos,
módulos e mensagens antes de tentar comandos aleatórios.

## Exercícios

1. Desenhe a rota exata da sua VM, incluindo arquivos e partições.
2. Compare duas inicializações com `journalctl --list-boots`.
3. Em clone descartável, provoque uma entrada `fstab` inválida não essencial,
   recupere pelo console e registre o procedimento.
4. Verifique se o driver do filesystem raiz existe no kernel ou initramfs.

## Checklist de domínio

Consigo separar firmware, bootloader, kernel, initramfs e PID 1, localizar uma
falha pela etapa e recuperar a VM sem reinstalar como primeira resposta.
