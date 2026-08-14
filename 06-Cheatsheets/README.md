# 06 - Cheatsheets

> Referencias rapidas e teoria de privesc / movimento lateral para lab e engagements autorizados.
> Use apos foothold ([13-Initial-Access](../13-Initial-Access/)) e antes / durante [14-Post-Exploitation](../14-Post-Exploitation/) e [03-AD-Notes](../03-AD-Notes/).

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários de Linux e Windows. |
| Pré-requisitos | Módulo 00; VM vulnerável própria e snapshots. |
| Tempo estimado | 12 horas de leitura e prática. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Árvore de decisão com evidência, detecção, correção e cleanup. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

## Conteudo

| Documento | Tema |
|-----------|------|
| [powershell_cheatsheet.md](powershell_cheatsheet.md) | PowerShell essencial para pentest, enum e automacao. |
| [linux_privesc_teoria.md](linux_privesc_teoria.md) | Privilege escalation Linux: SUID, sudo, capabilities, cron, kernel. |
| [linux_privesc_modern.md](linux_privesc_modern.md) | Privesc Linux moderno: containers, Polkit, systemd, CVEs recentes. |
| [windows_lateral_movement_teoria.md](windows_lateral_movement_teoria.md) | Movimento lateral Windows: WinRM, PsExec, WMI, RDP, relays. |
| [windows_privesc_teoria.md](windows_privesc_teoria.md) | Privilege escalation Windows: tokens, servicos, UAC, AlwaysInstallElevated. |
| [windows_privesc_metodologia.md](windows_privesc_metodologia.md) | Checklist pos-foothold (adaptado HexSec, PT). |
| [windows_privesc_cheatsheet.md](windows_privesc_cheatsheet.md) | Comandos densos de enum Windows privesc (adaptado HexSec, PT). |
| [linux_path_hijacking.md](linux_path_hijacking.md) | PATH hijacking + lab minimo SUID (adaptado HexSec, PT). |

## Fluxo recomendado

```
Foothold  -->  PrivEsc host (Windows/Linux)  -->  Lateral movement  -->  AD / Cloud
                     |                                  |
              windows_privesc / linux_*          windows_lateral_movement
```

1. **Cheatsheet PS** - [powershell_cheatsheet.md](powershell_cheatsheet.md) para enum rapida no Windows.
2. **PrivEsc Windows** - metodologia → teoria → [windows_privesc_cheatsheet.md](windows_privesc_cheatsheet.md).
3. **PrivEsc Linux** - [linux_privesc_teoria.md](linux_privesc_teoria.md) + [linux_path_hijacking.md](linux_path_hijacking.md) + modern.
4. **Lateral** - [windows_lateral_movement_teoria.md](windows_lateral_movement_teoria.md); depois paths AD no modulo 03.
5. **DFIR** - revisar [05-DFIR](../05-DFIR/) para saber quais artefatos voce deixa.

## MITRE ATT&CK (parcial)

- T1059.001 - PowerShell
- T1068 - Exploitation for Privilege Escalation
- T1548 - Abuse Elevation Control Mechanism
- T1134 - Access Token Manipulation
- T1021 - Remote Services (lateral)
- T1047 - Windows Management Instrumentation
- T1053 - Scheduled Task/Job
- T1543.003 - Windows Service

## Etica e escopo

- Apenas em hosts de lab ou no escopo escrito do pentest/red team.
- PrivEsc e lateral movement geram Event Logs / EDR alerts — alinhar com o cliente.
- Nao deixar persistencia nao documentada; cleanup ao final.
- Em containers/cloud, preferir labs isolados (`kind`/`minikube`, contas proprias) — ver modulos 08 e 10.

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Escalação de privilégios Linux - Explorando binários SUID](https://www.youtube.com/watch?v=DIsBdvFaiX0) — **Solyd Offensive Security**.
2. [Curso GRATUITO de pentest:  ESCALAÇÃO DE PRIVILÉGIOS!](https://www.youtube.com/watch?v=2XKiy2P3BGQ) — **Kraken Academy**.
3. [Resolvendo Pentest - Escalando privilégios!](https://www.youtube.com/watch?v=_-_x9fzw8Pg) — **TRW SYSTEM Tecnologia e Segurança da Informação**.
4. [Privilege Escalation em Linux: Como pentesters escalam privilégios na prática](https://www.youtube.com/watch?v=Sz8Sfqk9lQA) — **Hacking Club**.
5. [Aproveitando de permissões para escalar privilégios no Linux](https://www.youtube.com/watch?v=qZcgf2S_4wc) — **Ricardo Longatto**.
