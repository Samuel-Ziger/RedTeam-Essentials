# 🔬 Forensics Artifacts - Artefatos Forenses Windows

> Guia de artefatos forenses importantes para investigação digital

---

## 📚 O que são Artefatos Forenses?

**Artifacts** são evidências digitais deixadas no sistema operacional que revelam atividades do usuário e do sistema.

---

## 🗂️ Registry (Registro do Windows)

### Localização
```
C:\Windows\System32\config\
├─ SAM (Security Account Manager)
├─ SECURITY
├─ SOFTWARE
└─ SYSTEM

C:\Users\<username>\
├─ NTUSER.DAT (configurações do usuário)
└─ AppData\Local\Microsoft\Windows\UsrClass.dat
```

### Chaves Importantes

#### Execução de Programas
```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist
→ Programas executados (em ROT-13)

SOFTWARE\Microsoft\Windows\CurrentVersion\Run
→ Programas que iniciam automaticamente

SYSTEM\CurrentControlSet\Services
→ Serviços instalados
```

#### USB Devices
```
SYSTEM\CurrentControlSet\Enum\USBSTOR
→ Dispositivos USB conectados

SYSTEM\MountedDevices
→ Volumes montados
```

---

## 📁 File System Artifacts

### Prefetch
```
Localização: C:\Windows\Prefetch\
Extensão: .pf

Informações:
├─ Programas executados
├─ Número de execuções
├─ Timestamp da última execução
└─ Arquivos acessados pelo programa

Análise:
PECmd.exe -f "C:\Windows\Prefetch\CALC.EXE-1234ABCD.pf"
```

### Jumplists
```
Localização:
C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\
C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations\

Informações:
└─ Arquivos recentemente abertos por aplicação

Análise:
JLECmd.exe -d "C:\Users\user\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations"
```

### Recycle Bin
```
Localização:
C:\$Recycle.Bin\<SID>\

Arquivos:
├─ $I... (metadata)
└─ $R... (arquivo deletado)

Análise:
RBCmd.exe -d "C:\$Recycle.Bin"
```

---

## 🌐 Browser Artifacts

### Chrome/Edge
```
C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\
├─ History (histórico navegação)
├─ Cache
├─ Cookies
└─ Login Data (senhas salvas)

Análise:
hindsight.exe --input "C:\Users\user\AppData\Local\Google\Chrome\User Data\Default" --format xlsx
```

### Firefox
```
C:\Users\<user>\AppData\Roaming\Mozilla\Firefox\Profiles\
├─ places.sqlite (histórico, bookmarks)
├─ cookies.sqlite
└─ formhistory.sqlite
```

---

## 📂 File Activity

### LNK Files (Atalhos)
```
Localização:
C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Recent\

Informações:
├─ Arquivo alvo
├─ Timestamps (criação, modificação, acesso)
├─ Volume serial number
└─ Informações de rede (se UNC path)

Análise:
LECmd.exe -d "C:\Users\user\AppData\Roaming\Microsoft\Windows\Recent"
```

### Shellbags
```
NTUSER.DAT\Software\Microsoft\Windows\Shell\BagMRU
→ Pastas acessadas via Explorer

Análise:
SBECmd.exe -d "C:\Users\user"
```

---

## ⏰ Timeline Analysis

### MACB Times
```
M - Modified (conteúdo modificado)
A - Accessed (acessado)
C - Changed (metadados mudaram)
B - Born (criado)

Análise com MFT:
MFTECmd.exe -f "C:\$MFT" --csv output_folder
```

---

## 🔐 Credentials

### SAM Database
```
C:\Windows\System32\config\SAM
→ Hashes NTLM de senhas locais

Extração (requer admin):
reg save HKLM\SAM sam.hive
reg save HKLM\SYSTEM system.hive

Análise:
secretsdump.py -sam sam.hive -system system.hive LOCAL
```

### LSASS Memory
```
Processo: lsass.exe
Conteúdo: Credenciais em memória

Dump (requer SYSTEM):
procdump.exe -ma lsass.exe lsass.dmp

Análise:
mimikatz # sekurlsa::minidump lsass.dmp
mimikatz # sekurlsa::logonpasswords
```

---

## 🖥️ Event Logs (resumo)

Ver arquivo: `windows_event_logs.md`

Localização:
```
C:\Windows\System32\winevt\Logs\*.evtx
```

---

## 🌐 Network Artifacts

### Prefetch (Network)
Mostra conexões de rede estabelecidas por executáveis

### Registry
```
SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces
→ Configurações de rede
```

---

## 📊 Ferramentas Essenciais

| Ferramenta | Uso |
|------------|-----|
| **Autopsy** | Suite forense completo |
| **FTK Imager** | Aquisição de imagens |
| **Eric Zimmerman Tools** | Análise de artifacts |
| **Volatility** | Análise de memória |
| **Wireshark** | Análise de pacotes |

---

## 💡 Workflow de Análise

```
1. Aquisição
   └─ Criar imagem forense (FTK Imager)

2. Triage
   └─ KAPE (Kroll Artifact Parser)

3. Timeline
   └─ Plaso/log2timeline

4. Análise
   └─ Eric Zimmerman Tools + Autopsy

5. Relatório
   └─ Documentar achados
```

---

<div align="center">

**🔬 Artefatos contam a história do sistema**

*Saber onde procurar é metade da investigação*

</div>
