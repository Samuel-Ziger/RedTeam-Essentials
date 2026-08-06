# Windows Privilege Escalation — Metodologia

> Checklist operacional pos-foothold em lab ou engagement autorizado.
> Complementa [windows_privesc_teoria.md](windows_privesc_teoria.md) e [windows_privesc_cheatsheet.md](windows_privesc_cheatsheet.md).

**Credito:** adaptado (MIT) do material HexSec / Leonardo Tamiano — reescrito em portugues, sem links de video.

---

## 1. Escanear servicos (antes do foothold)

- Mapear portas/servicos com `nmap` (escopo autorizado).
- Separar alvos web vs nao-web (AD, SMB, RDP, WinRM).

## 2. Foothold

### Servicos web

- [ ] Enumerar arquivos e diretorios
- [ ] Enumerar virtual hosts
- [ ] Checar CVEs conhecidos da stack
- [ ] Testar vulnerabilidades web manuais (ver modulo `07-Web-AppSec`)

### Servicos nao-web / AD

- [ ] Enumerar pontos de entrada (SMB, LDAP, Kerberos, RDP)
- [ ] Misconfigs comuns (null session, signing, AS-REP, etc.)
- [ ] CVEs e abuse paths — ver `03-AD-Notes`

## 3. Privilege Escalation (shell interativa)

### Usuarios, grupos e privilegios

- [ ] `whoami` / `whoami /groups` / `whoami /priv`
- [ ] Privilegios perigosos: `SeImpersonatePrivilege`, `SeBackupPrivilege`, `SeAssignPrimaryTokenPrivilege`

### Aplicacoes instaladas

- [ ] Listar software e versoes
- [ ] Cruzar com CVEs locais conhecidos

### Servicos

- [ ] Permissoes fracas no servico (`sc sdshow` / ACL)
- [ ] Unquoted service path
- [ ] DLL hijacking (ordem de busca + pasta gravavel)
- [ ] `binPath` / `ImagePath` alteravel

### Arquivos acessiveis

- [ ] Hives SAM + SYSTEM (se houver privilegio adequado)
- [ ] Historico PowerShell (`ConsoleHost_history.txt`)
- [ ] Arquivos de config / `.env` / backups
- [ ] Databases de gerenciadores de senha (`.kdbx`, etc.)

### Credenciais e politica

- [ ] Credenciais armazenadas (Credential Manager / cmdkey)
- [ ] AlwaysInstallElevated (HKLM + HKCU)
- [ ] Scheduled tasks com ACL fraca ou binario gravavel
- [ ] Chaves de registro criticas (Run, Winlogon, AppInit_DLLs)

### UAC / Admin

- [ ] Se membro de grupo privilegiado com integrity baixa → avaliar UAC
- [ ] Se ja Administrator → documentar acesso; dump de credenciais so em lab/autorizado
- [ ] Se precisar de Net-NTLM do usuario atual → cenarios de coercao/relay so em lab (Responder)

### Defesa ativa

- [ ] Se AV/EDR ativo: documentar bloqueios; nao priorizar bypass opaco em engajamento sem RoE
- [ ] Registrar tudo no [REPORT-TEMPLATE.md](../REPORT-TEMPLATE.md)

---

## Ordem sugerida (rapida)

```
whoami /priv  ->  servicos/ACL  ->  arquivos sensiveis  ->  tasks/registry
      |                 |                    |                    |
 SeImpersonate    unquoted/weak      history/SAM/creds     AlwaysInstallElevated
```

## Referencias internas

- Teoria: [windows_privesc_teoria.md](windows_privesc_teoria.md)
- Comandos: [windows_privesc_cheatsheet.md](windows_privesc_cheatsheet.md)
- Lateral: [windows_lateral_movement_teoria.md](windows_lateral_movement_teoria.md)
