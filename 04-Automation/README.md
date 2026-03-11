## ⚙️ Módulo 04 – Automation

Este módulo reúne **scripts de automação** para preparar e organizar seus ambientes de estudo (Windows e Linux) e estruturar melhor os artefatos gerados durante labs, CTFs e pentests.

Todos os scripts seguem a filosofia do repositório:
- **Uso somente em ambientes de laboratório / teste**
- **Automação segura e comentada**
- **Foco em organização e produtividade**

---

## 🪟 `windows_setup_clean.ps1`

**Objetivo**: automatizar a configuração inicial de um **Windows para labs/pentest**, instalando ferramentas essenciais, ajustando o PowerShell e criando uma estrutura de pastas de trabalho.

### O que ele faz
- Configura o **PowerShell**:
  - Define `ExecutionPolicy` para `RemoteSigned` no usuário atual
  - Habilita execução de scripts em chave de registro (quando possível)
- Instala o **Chocolatey** (se ainda não existir)
- Instala, via Chocolatey, ferramentas recomendadas para laboratório:
  - `git`, `vscode`, `python3`, `wget`, `curl`, `7zip`, `notepadplusplus`, `sysinternals`, `wireshark`
- (Opcional) Cria a estrutura de pastas:
  - `C:\Users\<usuario>\Pentest\Tools`, `Scripts`, `Wordlists`, `Exploits`, `Notes`, `Labs`, `Reports`, `Logs`
- Ajusta configurações úteis do sistema:
  - Exibir extensões de arquivo
  - Exibir arquivos ocultos
- Oferece opção de limpeza (arquivos temporários e lixeira)

### Parâmetros
- `-SkipToolsInstall`  
  **Pula** a instalação das ferramentas via Chocolatey.

- `-CreateFolders`  
  Cria a estrutura de pastas de pentest em `C:\Users\<usuario>\Pentest`.

### Pré-requisitos
- Windows 10/11
- PowerShell (recomendado 5.1+)
- **Conexão com a internet** (para Chocolatey e pacotes)
- Idealmente rodar em um **terminal elevado (Administrador)** para evitar falhas em configurações de sistema.

### Exemplos de uso
```powershell
# Execução padrão (configura PowerShell, instala ferramentas, pergunta sobre limpeza)
.\windows_setup_clean.ps1

# Apenas configurações e estrutura de pastas, sem instalar ferramentas
.\windows_setup_clean.ps1 -SkipToolsInstall -CreateFolders
```

### Quando usar
- Ao criar uma **VM Windows nova** para estudos
- Antes de iniciar um **curso / trilha de pentest** para padronizar ambiente
- Para padronizar o ambiente entre múltiplas VMs de laboratório

---

## 🐧 `linux_postinstall.sh`

**Objetivo**: automatizar a pós-instalação em **Kali/Ubuntu (ou outras distros Debian-based)**, instalando ferramentas essenciais, criando estrutura de pastas e adicionando aliases úteis.

### O que ele faz
- Verifica se está executando como `root` (ou `sudo`)
- Atualiza o sistema:
  - `apt update && apt upgrade -y`
  - `apt dist-upgrade -y`
- Instala ferramentas essenciais de desenvolvimento:
  - `git`, `vim`, `curl`, `wget`, `build-essential`, `python3-pip`
- Instala ferramentas de rede:
  - `nmap`, `netcat-traditional`, `tcpdump`, `wireshark`
- Se detectar **Kali Linux**, instala ainda:
  - `metasploit-framework`, `burpsuite`, `zaproxy`, `sqlmap`
- Cria a estrutura de pastas em `~/Pentest`:
  - `Tools`, `Scripts`, `Wordlists`, `Exploits`, `Notes`, `Labs`, `Reports`, `Logs`
- Adiciona aliases úteis no `~/.bashrc`:
  - `ll`, `update`, `ports`, `myip`, `serve`
- Faz limpeza com `apt autoremove` e `apt autoclean`

### Pré-requisitos
- Distribuição **Debian-based** (Kali, Ubuntu, Parrot, etc.)
- Gerenciador de pacotes `apt`
- Script executado como **root**:
  - `sudo ./linux_postinstall.sh`

### Exemplos de uso
```bash
chmod +x linux_postinstall.sh
sudo ./linux_postinstall.sh

# Depois de terminar, recarregar o bashrc
source ~/.bashrc
```

### Quando usar
- Após instalar uma **VM Linux nova** para laboratório
- Para criar um ambiente Kali/Ubuntu já com:
  - Ferramentas básicas de rede
  - Ferramentas de pentest
  - Estrutura de diretórios padrão para estudos

---

## 🗂️ `organize_logs.ps1`

**Objetivo**: organizar rapidamente **logs, prints e arquivos de evidência** de um pentest/CTF em uma estrutura de pastas consistente dentro do diretório `Pentest\Labs`.

### O que ele faz
- Cria a estrutura:
  - `C:\Users\<usuario>\Pentest\Labs\<TargetName>\Screenshots`
  - `... \Scans`
  - `... \Exploits`
  - `... \Loot`
  - `... \Notes`
- Move arquivos do diretório de origem (`SourcePath`) para pastas específicas com base na extensão:
  - Imagens (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`) → `Screenshots`
  - Scans (`.xml`, `.nmap`, `.gnmap`) → `Scans`
  - Scripts/binaries (`.py`, `.sh`, `.ps1`, `.c`, `.cpp`, `.exe`) → `Exploits`
  - Documentos (`.txt`, `.md`, `.doc`, `.docx`, `.pdf`) → `Notes`
  - Qualquer outra coisa → `Loot`

### Parâmetros
- `-SourcePath` (obrigatório)  
  Pasta onde estão os arquivos desorganizados (por exemplo, downloads do navegador ou dump de uma pasta de trabalho).

- `-TargetName` (obrigatório)  
  Nome do alvo/lab/projeto. Será usado para nomear a pasta em `Pentest\Labs\<TargetName>`.

### Exemplos de uso
```powershell
# Organizar arquivos baixados de um lab do HackTheBox
.\organize_logs.ps1 -SourcePath "C:\Users\<usuario>\Downloads" -TargetName "HTB_Forest"

# Organizar evidências de um CTF
.\organize_logs.ps1 -SourcePath "C:\Temp\CTF-Files" -TargetName "CTF_2026_Final"
```

### Quando usar
- Depois de um **lab do TryHackMe / HackTheBox** para guardar tudo organizado
- Ao finalizar um **engajamento de laboratório** e querer separar:
  - Scans
  - Exploits utilizados
  - Evidências (prints, loot, relatórios)

---

## ✅ Boas práticas ao usar o módulo 04

- **Sempre** use estes scripts em:
  - Máquinas/VMs **suas** ou com autorização explícita
  - Ambientes de **laboratório isolados**
- Leia o código antes de executar para entender o que está sendo feito.
- Customize as listas de ferramentas/pastas conforme sua necessidade.
- Combine o módulo 04 com:
  - `LAB-SETUP.md` para montar o lab completo
  - `05-DFIR` e `06-Cheatsheets` para aprimorar análise e documentação

