# 🧠 Memory Analysis - Análise de Memória (Teoria)

> Fundamentos de análise forense de memória RAM

---

## 📚 O que é Memory Forensics?

**Memory Forensics** é a análise da memória RAM para extrair evidências de:
- Processos em execução
- Conexões de rede ativas
- Credenciais
- Malware residente apenas em memória
- Comandos executados

### Por que é importante?
```
Memória volátil contém:
├─ Dados não salvos em disco
├─ Malware fileless
├─ Credenciais em texto claro
├─ Chaves de criptografia
└─ Estado atual do sistema
```

---

## 🔧 Aquisição de Memória

### Ferramentas de Dump

#### Windows
```powershell
# DumpIt (Comae)
DumpIt.exe

# FTK Imager
File → Capture Memory

# Magnet RAM Capture
RAM Capture.exe

# WinPMEM
winpmem_mini_x64.exe memdump.raw
```

#### Linux
```bash
# LiME (Linux Memory Extractor)
insmod lime.ko "path=/tmp/ram.lime format=raw"

# AVML (Azure)
./avml memory.dmp
```

---

## 🛠️ Volatility Framework

**Volatility** é a ferramenta padrão para análise de memória.

### Instalação
```bash
# Volatility 2
pip install volatility

# Volatility 3
pip3 install volatility3
```

### Identificar Perfil (Vol 2)
```bash
volatility -f memory.dmp imageinfo
volatility -f memory.dmp kdbgscan
```

---

## 🔍 Plugins Essenciais (Volatility 2)

### Informações do Sistema
```bash
# Informações gerais
volatility -f memory.dmp --profile=Win10x64 imageinfo

# Processos em execução
volatility -f memory.dmp --profile=Win10x64 pslist
volatility -f memory.dmp --profile=Win10x64 pstree

# Processos ocultos
volatility -f memory.dmp --profile=Win10x64 psxview
```

### Network
```bash
# Conexões de rede (Windows 7-)
volatility -f memory.dmp --profile=Win7x64 connections
volatility -f memory.dmp --profile=Win7x64 connscan

# Network info (Windows 10+)
volatility -f memory.dmp --profile=Win10x64 netscan
```

### DLLs e Handles
```bash
# DLLs carregadas por processo
volatility -f memory.dmp --profile=Win10x64 dlllist -p 1234

# Handles abertos
volatility -f memory.dmp --profile=Win10x64 handles -p 1234
```

### Registry
```bash
# Hives do registro
volatility -f memory.dmp --profile=Win10x64 hivelist

# Dump de chave específica
volatility -f memory.dmp --profile=Win10x64 printkey -K "Software\Microsoft\Windows\CurrentVersion\Run"
```

### Credentials
```bash
# Hashes (requer mimikatz plugin)
volatility -f memory.dmp --profile=Win10x64 hashdump

# LSA secrets
volatility -f memory.dmp --profile=Win10x64 lsadump
```

### Comandos Executados
```bash
# Command history
volatility -f memory.dmp --profile=Win10x64 cmdscan
volatility -f memory.dmp --profile=Win10x64 consoles
```

---

## 🎯 Hunting Malware

### Processos Suspeitos
```bash
# Processos ocultos
volatility -f memory.dmp --profile=Win10x64 psxview

# Injeção de código
volatility -f memory.dmp --profile=Win10x64 malfind

# Hooks
volatility -f memory.dmp --profile=Win10x64 ssdt
```

### Análise de Processo Específico
```bash
# Dump de processo
volatility -f memory.dmp --profile=Win10x64 procdump -p 1234 -D output/

# Memória do processo
volatility -f memory.dmp --profile=Win10x64 memdump -p 1234 -D output/
```

---

## 🔐 Extração de Credenciais

### Mimikatz (em dump)
```powershell
# Carregar dump
mimikatz # sekurlsa::minidump lsass.dmp

# Extrair credenciais
mimikatz # sekurlsa::logonpasswords
```

### Volatility
```bash
# Plugin mimikatz para Volatility
volatility -f memory.dmp --profile=Win10x64 mimikatz
```

---

## 📊 Timeline de Análise

```
Workflow típico:
1. Identificar perfil do sistema
2. Listar processos (pslist, pstree)
3. Verificar processos ocultos (psxview)
4. Analisar conexões de rede (netscan)
5. Buscar injeções (malfind)
6. Extrair artefatos específicos
7. Correlacionar achados
8. Documentar evidências
```

---

## 💡 Red Flags em Memória

```
Indicadores de comprometimento:
├─ Processos sem parent process
├─ Processos ocultos (não em pslist mas em psscan)
├─ Injeção de código em processos legítimos
├─ Conexões para IPs desconhecidos
├─ DLLs não assinadas em processos do sistema
├─ Processos do sistema rodando de diretórios errados
└─ Hooks em SSDT/IRP
```

---

## 🎓 Recursos de Aprendizado

### Labs
- MemLabs (GitHub) - Desafios de memory forensics
- Blue Team Labs Online
- CyberDefenders

### Ferramentas
- **Volatility** - Análise de memória
- **Rekall** - Framework forense
- **MemProcFS** - File system virtual em memória

---

<div align="center">

**🧠 A memória não mente**

*Análise de RAM revela o estado verdadeiro do sistema*

</div>
