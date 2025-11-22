# 📋 Template de Relatório Forense - DFIR

Este template segue padrões da indústria para documentação de incidentes de segurança.

---

## 📊 RESUMO EXECUTIVO

### Informações do Incidente

| Campo | Detalhes |
|-------|----------|
| **ID do Incidente** | INC-YYYY-NNNN |
| **Data da Detecção** | DD/MM/YYYY HH:MM |
| **Data do Incidente** | DD/MM/YYYY HH:MM (estimada) |
| **Investigador(es)** | Nome(s) |
| **Status** | Aberto / Em Investigação / Fechado |
| **Severidade** | Crítica / Alta / Média / Baixa |

### Breve Descrição

[Resumo de 2-3 parágrafos sobre o incidente detectado, impacto inicial e ações tomadas]

### Impacto

- **Sistemas Afetados:** [Lista de sistemas]
- **Dados Comprometidos:** [Sim/Não + Descrição]
- **Tempo de Inatividade:** [Horas/Minutos]
- **Impacto Financeiro:** [Se aplicável]
- **Impacto Regulatório:** [LGPD, GDPR, etc]

---

## 🔍 DETALHES TÉCNICOS

### Vetor de Ataque

**Método de Entrada:**
- [ ] Phishing
- [ ] Vulnerabilidade Explorada (CVE-XXXX-XXXX)
- [ ] Credenciais Comprometidas
- [ ] Malware
- [ ] Insider Threat
- [ ] Outro: _______________

**MITRE ATT&CK Mapping:**
- **Tática:** [Nome da Tática]
- **Técnica:** [TXXXX - Nome da Técnica]
- **Sub-técnica:** [TXXXX.XXX - Se aplicável]

### Timeline do Incidente

| Data/Hora | Evento | Fonte | Evidência |
|-----------|--------|-------|-----------|
| YYYY-MM-DD HH:MM | Primeira atividade suspeita | Event Log ID 4624 | `evidence_001.evtx` |
| YYYY-MM-DD HH:MM | Escalação de privilégios | Sysmon ID 10 | `evidence_002.xml` |
| YYYY-MM-DD HH:MM | Movimento lateral detectado | Network logs | `evidence_003.pcap` |
| YYYY-MM-DD HH:MM | Exfiltração de dados | Firewall logs | `evidence_004.log` |
| YYYY-MM-DD HH:MM | Incidente contido | Ação manual | `action_log.txt` |

### Sistemas Afetados

#### Sistema 1: [Nome/IP]

**Informações:**
- **Hostname:** WORKSTATION-01
- **IP Address:** 192.168.1.100
- **OS:** Windows 10 Pro 21H2
- **Função:** Estação de trabalho de RH
- **Usuário:** joao.silva

**Artefatos Coletados:**
- [ ] Dump de memória
- [ ] Imagem de disco
- [ ] Logs do sistema
- [ ] Logs de aplicação
- [ ] Tráfego de rede (PCAP)
- [ ] Registro do Windows

**Indicadores de Compromisso (IOCs):**
- Arquivo: `C:\Users\joao.silva\AppData\Local\Temp\malware.exe`
  - Hash MD5: `d41d8cd98f00b204e9800998ecf8427e`
  - Hash SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Conexão de rede: `malicious-c2.example.com:443`
- Chave de registro: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Updater`

---

## 🔬 ANÁLISE FORENSE

### Análise de Memória

**Ferramenta:** Volatility 3  
**Profile:** Win10x64_19041

```bash
# Processos suspeitos
vol.py -f memory.dmp windows.pslist

PID: 4567 | malware.exe | PPID: 1234 (explorer.exe)
Criado: 2025-11-20 14:23:45 UTC
Injeção detectada: svchost.exe (PID 2345)
```

**Achados:**
- Processo `malware.exe` executando de diretório temporário
- Injeção de código em processo legítimo `svchost.exe`
- Conexões de rede para IP malicioso: 203.0.113.45:443

### Análise de Logs

#### Windows Event Logs

**Security.evtx:**
```
Event ID 4624: Logon bem-sucedido
Timestamp: 2025-11-20 14:20:12
Logon Type: 10 (RemoteInteractive/RDP)
Account: DOMAIN\administrator
Source IP: 10.0.0.50
```

**Sysmon:**
```
Event ID 1: Process Creation
Timestamp: 2025-11-20 14:23:45
Process: malware.exe
CommandLine: "C:\Users\joao.silva\AppData\Local\Temp\malware.exe" -stealth
Parent: explorer.exe
Hashes: MD5=d41d8cd98f00b204e9800998ecf8427e
```

#### Network Logs

**Tráfego Suspeito:**
```
Source: 192.168.1.100:49876
Destination: 203.0.113.45:443
Protocol: HTTPS
Bytes Sent: 15 MB
Timestamp: 2025-11-20 14:25:00 - 14:45:00
```

### Análise de Arquivos

**Malware Identificado:**

| Arquivo | Hash SHA256 | Tipo | VirusTotal | Comportamento |
|---------|-------------|------|-----------|---------------|
| malware.exe | e3b0c4429... | PE32 | 45/70 | RAT, Keylogger, Exfiltração |

**Artefatos de Persistência:**
- Registry Run Key: `HKCU\...\Run\Updater`
- Scheduled Task: `\Microsoft\Windows\UpdateOrchestrator\Malware`
- Service: `WindowsUpdateService` (falso)

---

## 📁 EVIDÊNCIAS COLETADAS

### Chain of Custody

| ID | Tipo | Descrição | Data Coleta | Coletado Por | Hash |
|----|------|-----------|-------------|--------------|------|
| E001 | Memory Dump | RAM do WORKSTATION-01 | 2025-11-20 15:00 | João Silva | sha256:abc123... |
| E002 | Disk Image | SSD 500GB | 2025-11-20 16:00 | João Silva | sha256:def456... |
| E003 | Event Logs | Security, System, Sysmon | 2025-11-20 15:15 | João Silva | sha256:ghi789... |
| E004 | Network PCAP | Tráfego 14:00-15:00 | 2025-11-20 15:30 | Maria Costa | sha256:jkl012... |

### Armazenamento de Evidências

- **Localização Física:** Sala de Evidências, Armário 3, Gaveta B
- **Localização Digital:** `\\forensics-server\cases\INC-2025-0042\`
- **Backup:** `\\backup-server\forensics\INC-2025-0042\` (criptografado)
- **Acesso Restrito:** Apenas equipe de IR e legal

---

## 🛡️ CONTENÇÃO E ERRADICAÇÃO

### Ações de Contenção

| Data/Hora | Ação | Executor | Resultado |
|-----------|------|----------|-----------|
| 2025-11-20 15:00 | Isolamento de rede do WORKSTATION-01 | SOC | Sucesso |
| 2025-11-20 15:10 | Desabilitar conta comprometida | Admin | Sucesso |
| 2025-11-20 15:20 | Bloquear IOCs no firewall | SecOps | Sucesso |
| 2025-11-20 15:30 | Bloquear domínios maliciosos no DNS | NetOps | Sucesso |

### Ações de Erradicação

- [ ] Reimagem completa do sistema afetado
- [ ] Remoção de malware de sistemas adicionais
- [ ] Limpeza de persistência em todos os sistemas
- [ ] Reset de credenciais comprometidas
- [ ] Patch de vulnerabilidades exploradas

---

## 🔄 RECUPERAÇÃO

### Plano de Recuperação

1. **Validação de Limpeza**
   - Scan completo com EDR atualizado
   - Verificação de IOCs em toda rede
   - Análise de logs pós-erradicação

2. **Restauração de Serviços**
   - Reimagem do sistema com build limpo
   - Restauração de dados de backup (validado)
   - Testes de funcionalidade

3. **Monitoramento Intensivo**
   - Período: 30 dias
   - Alertas específicos para IOCs relacionados
   - Revisão diária de logs

---

## 📊 ANÁLISE DE CAUSA RAIZ

### Causa Primária

[Descrição detalhada de como o incidente ocorreu]

**Exemplo:**
Usuário clicou em link malicioso em email de phishing, baixando malware que explorou vulnerabilidade conhecida (CVE-2021-XXXXX) para elevar privilégios.

### Fatores Contribuintes

1. **Controles Faltantes:**
   - Falta de EDR no endpoint
   - Email gateway sem sandboxing
   - Patching desatualizado

2. **Falhas de Processo:**
   - Treinamento de awareness insuficiente
   - Política de patching não seguida
   - Segregação de rede inadequada

3. **Falhas Técnicas:**
   - Vulnerabilidade crítica não corrigida há 90 dias
   - Logs não centralizados
   - Detecção de comportamento anômalo ausente

---

## ✅ RECOMENDAÇÕES

### Curto Prazo (0-30 dias)

| Prioridade | Recomendação | Responsável | Prazo | Status |
|------------|--------------|-------------|-------|--------|
| 🔴 Crítica | Implementar EDR em todos endpoints | TI | 15 dias | ⏳ Em Progresso |
| 🔴 Crítica | Patch de CVE-2021-XXXXX em toda frota | TI | 7 dias | ⏳ Em Progresso |
| 🟠 Alta | Centralizar logs em SIEM | SecOps | 30 dias | 📋 Planejado |
| 🟠 Alta | Treinamento de phishing para todos | RH/Sec | 30 dias | 📋 Planejado |

### Médio Prazo (30-90 dias)

| Prioridade | Recomendação | Responsável | Prazo | Status |
|------------|--------------|-------------|-------|--------|
| 🟡 Média | Implementar sandboxing de email | TI | 60 dias | 📋 Planejado |
| 🟡 Média | Segregação de rede (VLANs) | NetOps | 90 dias | 📋 Planejado |
| 🟡 Média | Programa de Vulnerability Management | SecOps | 90 dias | 📋 Planejado |

### Longo Prazo (90+ dias)

- Implementar Zero Trust Architecture
- SOC 24x7 ou serviço gerenciado
- Red Team exercises trimestrais
- Playbooks automatizados de IR

---

## 📋 LIÇÕES APRENDIDAS

### O que funcionou bem?

- Detecção rápida via alerta manual
- Contenção imediata impediu propagação
- Coleta de evidências bem executada
- Comunicação efetiva entre equipes

### O que pode melhorar?

- Tempo de resposta inicial (30min é muito)
- Falta de automação em contenção
- Documentação durante o incidente
- Testes de restore de backup

### Mudanças de Processo

1. **Detecção:**
   - Implementar alertas automatizados para IOCs
   - Baseline de comportamento de rede

2. **Resposta:**
   - Playbook de isolamento automatizado
   - Checklist de coleta de evidências

3. **Recuperação:**
   - Testes mensais de restore
   - Gold images atualizadas

---

## 📎 ANEXOS

### A. IOCs Completos

**Hashes de Arquivos:**
```
MD5:    d41d8cd98f00b204e9800998ecf8427e
SHA1:   da39a3ee5e6b4b0d3255bfef95601890afd80709
SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

**Domínios/IPs Maliciosos:**
```
malicious-c2.example.com
203.0.113.45
198.51.100.23
```

**Registry Keys:**
```
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Updater
HKLM\System\CurrentControlSet\Services\WindowsUpdateService
```

### B. Comandos Utilizados

**Coleta de Memória:**
```powershell
.\DumpIt.exe /output E:\evidence\memory.dmp
```

**Coleta de Logs:**
```powershell
wevtutil epl Security E:\evidence\Security.evtx
wevtutil epl System E:\evidence\System.evtx
```

**Análise de Memória:**
```bash
vol.py -f memory.dmp windows.pslist
vol.py -f memory.dmp windows.netscan
vol.py -f memory.dmp windows.malfind
```

### C. Screenshots

[Anexar screenshots relevantes]

### D. Referências

- NIST SP 800-61 Rev. 2: Computer Security Incident Handling Guide
- SANS Incident Handler's Handbook
- MITRE ATT&CK Framework: https://attack.mitre.org/

---

## ✍️ ASSINATURAS

**Preparado por:**
Nome: _______________________  
Cargo: Analista de DFIR  
Data: ___/___/______  
Assinatura: _______________________

**Revisado por:**
Nome: _______________________  
Cargo: Gerente de Segurança  
Data: ___/___/______  
Assinatura: _______________________

**Aprovado por:**
Nome: _______________________  
Cargo: CISO  
Data: ___/___/______  
Assinatura: _______________________

---

## 📋 CONTROLE DE VERSÃO

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | DD/MM/YYYY | Nome | Versão inicial |
| 1.1 | DD/MM/YYYY | Nome | Adicionado seção X |

---

<div align="center">

**CONFIDENCIAL - DISTRIBUIÇÃO RESTRITA**

Este documento contém informações sensíveis de segurança.  
Distribuição apenas para pessoal autorizado.

**Classificação:** CONFIDENCIAL  
**Validade:** [Data de Expiração]

---

*Template mantido por RedTeam-Essentials*  
*Baseado em padrões NIST, SANS e ISO 27035*

</div>
