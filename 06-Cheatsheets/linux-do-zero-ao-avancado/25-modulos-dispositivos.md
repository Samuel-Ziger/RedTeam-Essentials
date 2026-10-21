# 25 — Módulos, drivers, dispositivos e udev

## Objetivos

- relacionar hardware, barramento, driver, módulo, sysfs e nó de dispositivo;
- explicar descoberta, aliases, parâmetros, dependências e autoload;
- distinguir módulo embutido, carregável, externo, assinado e incompatível;
- diagnosticar evento de dispositivo sem remover driver essencial.

## Descoberta de hardware

```bash
lscpu
lspci -nnk 2>/dev/null
lsusb -t 2>/dev/null
lsblk -o NAME,TYPE,TRAN,VENDOR,MODEL,SERIAL,SIZE
sudo dmidecode -t system 2>/dev/null
```

Serial e DMI podem identificar equipamento; saneie relatórios. Em VM, o sistema
vê dispositivos virtuais e drivers como `virtio`.

## Device model e sysfs

O kernel representa barramentos, dispositivos, drivers e classes em sysfs.

```bash
find /sys/class/net -maxdepth 1 -mindepth 1 -printf '%f -> %l\n'
readlink -f /sys/class/net/*/device 2>/dev/null
udevadm info --query=property --path=/sys/class/net/lo
```

`/dev` contém nós com major/minor que encaminham operações a drivers. devtmpfs
e udev normalmente criam nomes e links dinamicamente.

```bash
ls -l /dev/null /dev/zero /dev/random
stat -c '%t:%T %F %n' /dev/null
cat /proc/devices | head -n 30
```

## Módulos

```bash
lsmod
modinfo nome_do_modulo
find "/lib/modules/$(uname -r)" -type f | head
```

`modprobe` resolve dependências e aliases; `insmod` tenta inserir um arquivo
diretamente. Prefira `modprobe` na operação normal.

```bash
sudo modprobe modulo
sudo modprobe -r modulo
```

Remover driver em uso pode causar perda de dispositivo/dados. Faça somente em
VM, após verificar holders, mounts, rede e dependências. Não teste com driver do
disco raiz, rede de administração ou console.

## Parâmetros, blacklist e initramfs

```bash
modinfo -p modulo
find /sys/module/modulo/parameters -type f -maxdepth 1 -print 2>/dev/null
```

Parâmetros podem vir da linha do kernel, arquivos em `/etc/modprobe.d` ou
comando. Blacklist pode não afetar módulo embutido ou carregado pelo initramfs;
regenere initramfs quando a distro exigir e mantenha rollback.

## Assinatura e taint

Secure Boot/lockdown pode exigir módulo assinado por chave confiável. DKMS
reconstrói módulos externos a cada kernel, mas build bem-sucedido não prova
compatibilidade. Módulo proprietário, forçado ou falhas marcam o kernel como
tainted:

```bash
cat /proc/sys/kernel/tainted
modinfo -F signer modulo 2>/dev/null
dmesg --level=err,warn | tail
```

Registre o valor e decodifique conforme a documentação do kernel.

## udev

Udev recebe eventos, consulta propriedades e cria links/permissões ou aciona
ações curtas. Observe:

```bash
udevadm monitor --kernel --udev --property
udevadm info --attribute-walk --name=/dev/ttyUSB0 2>/dev/null
```

Uma regra pode combinar propriedades estáveis e atribuir `SYMLINK`, `OWNER`,
`GROUP`, `MODE` ou `TAG`. Evite nomes de kernel instáveis e `RUN+=` para trabalho
longo; acione uma unit systemd.

Exemplo conceitual para um dispositivo USB fictício:

```udev
SUBSYSTEM=="tty", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", \
  SYMLINK+="sensor-lab", GROUP="dialout", MODE="0660"
```

Valide sintaxe e evento em VM com dispositivo próprio:

```bash
sudo udevadm control --reload
sudo udevadm test /sys/caminho/do/dispositivo
```

Não use `MODE="0666"` por conveniência; conceda grupo específico.

## Firmware

Alguns drivers carregam blobs de `/lib/firmware`. Mensagens de firmware ausente
aparecem no kernel log. Instale o pacote oficial apropriado e confirme licença,
versão e hardware; não baixe blobs aleatórios.

## Módulo didático

`exemplos/kernel/hello_safe.c` registra init e exit, sem hooks ou acesso a
hardware. Compile somente contra headers correspondentes e carregue apenas em
VM descartável. O executor padrão compila se houver headers, mas nunca carrega.

## Exercícios

1. Escolha um dispositivo não crítico e siga o caminho do barramento à classe,
   driver, módulo e propriedades udev somente com leitura.
2. Compare major e minor de três nós e explique por que o nome em dev não é o
   driver em si.
3. Inspecione vermagic, licença, parâmetros e dependências de um módulo já
   presente sem carregá-lo ou removê-lo.
4. Capture um evento udev seguro, associe propriedades a links persistentes e
   proponha uma regra em texto sem instalá-la.

## Checklist de domínio

Consigo relacionar hardware → barramento → driver → módulo → sysfs → nó/link
udev, e tenho um plano de recuperação antes de alterar qualquer driver.
