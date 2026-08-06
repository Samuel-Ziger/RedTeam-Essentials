# 04 - Automation

> Scripts de setup e organizacao para labs Windows/Linux. Uso somente em ambientes autorizados.

## Conteudo

| Script | Plataforma | Tema |
|--------|------------|------|
| [windows_setup_clean.ps1](windows_setup_clean.ps1) | Windows | Provisiona VM de lab (Chocolatey, pastas, tweaks). |
| [linux_postinstall.sh](linux_postinstall.sh) | Debian/Kali | Pos-install: tools, pastas, aliases, SecLists. |
| [organize_logs.ps1](organize_logs.ps1) | Cross (PS) | Organiza evidencias em `~/Pentest/Labs/<alvo>`. |
| [ad_recon.sh](ad_recon.sh) | Linux | Wrapper nmap + NetExec (`nxc`) + Impacket. |

Todos usam a lib comum em `lib/` (logging, dry-run, validacao).

---

## windows_setup_clean.ps1 (v2)

**Parametros:**
- `-DryRun` — simula sem instalar
- `-SkipTools` — pula pacotes Chocolatey
- `-SkipFolders` — nao cria `~/Pentest`
- `-OnlyChoco` — so Chocolatey
- `-ExtraPackages` — lista adicional (ex.: `ghidra`)

```powershell
./windows_setup_clean.ps1 -DryRun
./windows_setup_clean.ps1 -SkipTools
./windows_setup_clean.ps1 -ExtraPackages ghidra,radare2
```

---

## linux_postinstall.sh (v2)

```bash
chmod +x linux_postinstall.sh
sudo ./linux_postinstall.sh
sudo RTE_DRYRUN=1 ./linux_postinstall.sh   # se suportado via rte_common
source ~/.bashrc
```

Detecta Kali/Parrot/Ubuntu/Debian. Em Kali tenta `netexec` (sucessor do CrackMapExec).

---

## organize_logs.ps1 (v2)

**Parametros:** `-SourcePath`, `-TargetName`, `-BasePath`, `-CopyMode`, `-DryRun`.

```powershell
./organize_logs.ps1 -SourcePath "$HOME/Downloads" -TargetName "HTB_Forest"
./organize_logs.ps1 -SourcePath ./raw -TargetName "Lab_DVWA" -CopyMode -DryRun
```

Gera `INDEX.md` com hashes SHA-256 dos arquivos movidos/copiados.

---

## ad_recon.sh

```bash
./ad_recon.sh -t 192.168.56.0/24 -u user -p 'Pass' --domain lab.local
# Preferir NetExec: nxc smb <alvo> -u user -p pass
```

Proximo passo tipico: coletar com SharpHound / bloodhound-python e importar no **BloodHound CE**.

---

## Etica

Apenas em VMs/labs seus ou com autorizacao escrita. Nao rode setup em maquinas de producao.
