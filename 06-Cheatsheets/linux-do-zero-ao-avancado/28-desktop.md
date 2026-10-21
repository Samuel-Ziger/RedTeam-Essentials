# 28 — Desktop, sessão gráfica, áudio e energia

## Objetivos

- distinguir display manager, sessão, compositor, toolkit e portal;
- localizar configuração e logs no escopo do usuário correto;
- diagnosticar vídeo, áudio, entrada, energia e aplicação por camada;
- recuperar a sessão sem substituir toda a distribuição.

## Camadas de uma sessão

```text
kernel/DRM/KMS + driver GPU
       ↓
display manager → sessão do usuário
       ↓
compositor Wayland ou servidor Xorg
       ↓
desktop/window manager → toolkit → aplicação
       ↓
portais, input method, clipboard, notificações
```

GNOME, KDE Plasma, Xfce e outros combinam componentes e padrões diferentes.
Trocar desktop não troca kernel; trocar display server afeta captura, input e
compatibilidade gráfica.

## Wayland e X11

X11 permite que clientes interajam por um servidor com modelo histórico amplo;
isso facilita compatibilidade e também expõe superfícies como captura/input entre
clientes. Wayland define protocolo entre clientes e compositor, com isolamento
mais forte por padrão; portais mediam captura e compartilhamento. XWayland roda
aplicativos X em sessão Wayland.

```bash
printf 'tipo=%s display=%s wayland=%s\n' \
  "${XDG_SESSION_TYPE:-}" "${DISPLAY:-}" "${WAYLAND_DISPLAY:-}"
loginctl show-session "${XDG_SESSION_ID:-self}" 2>/dev/null | head
```

## XDG e configuração por usuário

```bash
printf '%s\n' \
  "config=${XDG_CONFIG_HOME:-$HOME/.config}" \
  "data=${XDG_DATA_HOME:-$HOME/.local/share}" \
  "cache=${XDG_CACHE_HOME:-$HOME/.cache}" \
  "runtime=${XDG_RUNTIME_DIR:-ausente}"
```

Configuração, dados, cache e runtime têm ciclos diferentes. Não coloque socket
persistente em cache ou segredos em diretório world-readable. `$XDG_RUNTIME_DIR`
deve pertencer ao usuário e existir apenas durante sua presença operacional.

## GPU

DRM/KMS no kernel administra dispositivos e modos; Mesa oferece drivers user
space para muitas GPUs; drivers proprietários podem usar integração própria.

```bash
lspci -nnk | grep -A3 -Ei 'vga|3d|display'
ls -l /dev/dri 2>/dev/null
glxinfo -B 2>/dev/null | sed -n '1,15p'
```

Renderização por software costuma indicar driver, permissão, sessão remota ou
VM, não necessariamente GPU defeituosa.

## Áudio

ALSA conecta kernel/hardware; PipeWire oferece grafo multimídia moderno e pode
substituir interfaces PulseAudio/JACK através de compatibilidade. WirePlumber é
um session/policy manager comum.

```bash
wpctl status 2>/dev/null
pactl info 2>/dev/null | head
aplay -l 2>/dev/null
```

Diagnostique dispositivo → perfil → rota → volume/mute → aplicação. Evite
executar servidores de áudio de usuário com `sudo`.

## Input, idioma e fontes

Layout do console, layout da sessão e input method são camadas. IBus/Fcitx
tratam composição; fontconfig descobre fontes:

```bash
localectl status 2>/dev/null
locale
fc-match sans 2>/dev/null
```

Mojibake costuma ser discordância de encoding; glifo ausente é problema de
fonte/fallback. Não são a mesma falha.

## Energia, suspensão e bateria

```bash
loginctl show-session self 2>/dev/null
systemctl status sleep.target suspend.target 2>/dev/null
cat /sys/class/power_supply/BAT*/capacity 2>/dev/null
powerprofilesctl get 2>/dev/null
```

Suspend-to-RAM mantém estado em RAM; hibernação grava estado em armazenamento e
exige swap/configuração compatível. Criptografia e Secure Boot influenciam o
modelo. Teste retomada antes de depender dela.

## Flatpak e portais

Aplicativos sandboxed pedem acesso a arquivos, câmera, microfone, captura e URLs
por portais. Conceder acesso amplo ao home elimina parte do isolamento. Revise
permissões e redefina exceções antigas.

## Troubleshooting gráfico

1. determine TTY ou sessão inteira afetada;
2. identifique tipo de sessão e compositor;
3. confira display manager e journal de usuário;
4. verifique driver, renderizador e `/dev/dri`;
5. teste novo usuário para separar configuração pessoal;
6. desative uma extensão por vez;
7. compare Wayland/Xorg somente como experimento;
8. preserve logs do boot com falha.

```bash
journalctl --user -b -p warning
journalctl -b -u display-manager
coredumpctl list --since today 2>/dev/null
```

## Exercícios

1. Mapeie sua sessão do login ao compositor e identifique se usa Wayland ou
   X11, sem alterar o padrão.
2. Execute uma aplicação com perfil de usuário temporário e compare o resultado
   ao perfil normal para separar estado da aplicação e do sistema.
3. Relacione um dispositivo de áudio à sessão, servidor de áudio e aplicação,
   preservando saídas antes de reiniciar qualquer componente.
4. Registre uma falha fictícia de suspensão ou monitor e escreva a sequência
   mínima de coleta que sobreviveria ao próximo boot.

## Checklist de domínio

Consigo localizar uma falha entre kernel/driver, display manager, compositor,
desktop, portal, áudio e configuração de usuário sem reinstalar a distro.
