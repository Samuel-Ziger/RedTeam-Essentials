# 06 - Cheatsheets

> Referencias rapidas e teoria de privesc / movimento lateral para lab e engagements autorizados.
> Use apos foothold ([13-Initial-Access](../13-Initial-Access/)) e antes / durante [14-Post-Exploitation](../14-Post-Exploitation/) e [03-AD-Notes](../03-AD-Notes/).

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
