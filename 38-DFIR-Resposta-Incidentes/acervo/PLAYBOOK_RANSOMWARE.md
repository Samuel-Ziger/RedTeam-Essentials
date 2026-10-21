# 🚨 Playbook: Resposta a Ransomware

Este playbook fornece um guia passo-a-passo para responder a incidentes de ransomware.

---

## 📋 Informações do Playbook

| Campo | Detalhes |
|-------|----------|
| **Nome** | Ransomware Incident Response |
| **ID** | PLAYBOOK-DFIR-001 |
| **Versão** | 1.0 |
| **Última Atualização** | 2025-11-22 |
| **Autor** | RedTeam-Essentials |
| **Aprovado por** | CISO |
| **MITRE ATT&CK** | T1486 (Data Encrypted for Impact) |

---

## 🎯 Objetivos

- Conter rapidamente o ransomware para prevenir propagação
- Preservar evidências para investigação forense
- Restaurar operações críticas de negócio
- Identificar vetor de entrada e causa raiz
- Implementar melhorias para prevenir recorrência

---

## ⚠️ Triggers / Indicadores

Execute este playbook quando:

- [ ] Alertas de EDR/AV sobre ransomware
- [ ] Arquivos com extensões incomuns (.encrypted, .locked, .crypt)
- [ ] Notas de resgate (ransom notes) encontradas
- [ ] Impossibilidade de abrir arquivos (criptografados)
- [ ] Alertas de tentativa de criptografia em massa
- [ ] Usuários reportam telas de resgate

---

## 🚦 Severidade

**Nível:** 🔴 CRÍTICO

**Impacto Potencial:**
- Perda de dados críticos
- Parada de operações
- Danos à reputação
- Custos de recuperação elevados
- Possível vazamento de dados (double extortion)

---

## 👥 Equipe de Resposta

| Papel | Responsável | Contato |
|-------|-------------|---------|
| **Incident Commander** | CISO | +55 11 9XXXX-XXXX |
| **Lead Investigator** | Gerente de SOC | +55 11 9XXXX-XXXX |
| **Forensics Analyst** | Analista DFIR | +55 11 9XXXX-XXXX |
| **IT Operations** | Gerente de TI | +55 11 9XXXX-XXXX |
| **Communications** | Relações Públicas | +55 11 9XXXX-XXXX |
| **Legal** | Advogado Interno | +55 11 9XXXX-XXXX |

---

## 📞 Contatos Externos

| Entidade | Contato | Quando Acionar |
|----------|---------|----------------|
| **Polícia Federal (CCIBER)** | 194 ou denúncia online | Obrigatório para crimes cibernéticos |
| **CERT.br** | cert@cert.br | Notificação de incidente |
| **Segurador Cyber** | [Número da apólice] | Se houver seguro cyber |
| **Especialista Forense Externo** | [Contato] | Se recursos internos insuficientes |
| **Negociador de Ransomware** | [Contato] | Apenas se considerar pagamento |

---

## ⏱️ Timeline de Resposta

```
┌─────────────────────────────────────────────────────────────┐
│                    FASES DE RESPOSTA                        │
├─────────────────────────────────────────────────────────────┤
│ DETECÇÃO        │ 0-15 min  │ Identificar e confirmar      │
│ CONTENÇÃO       │ 15-60 min │ Isolar e parar propagação    │
│ ERRADICAÇÃO     │ 1-4 horas │ Remover ameaça               │
│ RECUPERAÇÃO     │ 4-24 horas│ Restaurar sistemas           │
│ PÓS-INCIDENTE   │ 24-72 horas│ Análise e melhorias         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 FASE 1: DETECÇÃO E ANÁLISE INICIAL (0-15 min)

### 1.1 Confirmar o Incidente

**Ações:**

```bash
# Verificar processos suspeitos
Get-Process | Where-Object {$_.ProcessName -like "*crypt*" -or $_.ProcessName -like "*ransom*"}

# Procurar por notas de resgate
Get-ChildItem -Path C:\ -Recurse -Include "*.txt","*.html" -ErrorAction SilentlyContinue | 
    Select-String -Pattern "ransom|bitcoin|decrypt|pay|crypto" -List

# Verificar extensões de arquivos criptografados
Get-ChildItem -Path C:\Users -Recurse | 
    Group-Object Extension | 
    Sort-Object Count -Descending | 
    Select-Object -First 20
```

**Checklist:**

- [ ] Confirmar criptografia de arquivos
- [ ] Identificar nota de resgate
- [ ] Verificar número de sistemas afetados
- [ ] Identificar quando começou (timestamp)
- [ ] Capturar screenshots da nota de resgate

### 1.2 Notificar Partes Interessadas

**Imediato (0-5 min):**
- [ ] Notificar CISO/Gerência
- [ ] Acionar equipe de IR
- [ ] Iniciar bridge call de crise

**Primeiros 15 min:**
- [ ] Documentar em ticket de incidente
- [ ] Notificar Legal e Compliance
- [ ] Iniciar log de ações (incident log)

### 1.3 Análise Rápida

**Coletar Informações:**

```powershell
# Timestamp de modificação de arquivos
Get-ChildItem -Path C:\Users\JohnDoe\Documents -Recurse | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 10 FullName, LastWriteTime

# Processos em execução (snapshot)
Get-Process | Export-Csv -Path "C:\IR\processes_$(Get-Date -f yyyyMMdd_HHmmss).csv"

# Conexões de rede ativas
Get-NetTCPConnection | Where-Object State -eq "Established" | 
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess
```

**Perguntas a Responder:**
- Qual variante de ransomware? (ID Ransomware: https://id-ransomware.malwarehunterteam.com/)
- Quantos sistemas afetados?
- Quais dados criptografados?
- Existe backup disponível?
- Propagação ainda ativa?

---

## 🛡️ FASE 2: CONTENÇÃO (15-60 min)

### 2.1 Contenção Imediata

**CRÍTICO - Primeiros 5 minutos:**

```powershell
# 1. DESCONECTAR DA REDE (MANTER LIGADO!)
Disable-NetAdapter -Name "Ethernet" -Confirm:$false
Disable-NetAdapter -Name "Wi-Fi" -Confirm:$false

# 2. DOCUMENTAR antes de desligar
Get-Process > processes.txt
netstat -ano > network.txt
Get-Date > timestamp.txt

# 3. Se não for possível conter, DESLIGUE o sistema
Stop-Computer -Force
```

**⚠️ IMPORTANTE:**
- **NÃO desligue** antes de coletar memória volátil (se possível)
- **NÃO reconecte** à rede sem autorização
- **DOCUMENTE** tudo que fizer

### 2.2 Isolamento de Rede

**Ações de Rede:**

- [ ] Bloquear MAC address do sistema infectado no switch
- [ ] Desabilitar porta física no switch
- [ ] Bloquear IPs de C2 no firewall (se identificados)
- [ ] Isolar VLANs afetadas
- [ ] Desabilitar contas de usuário comprometidas

**Firewall Rules:**

```bash
# Exemplo de bloqueio de C2 (ajustar para seu firewall)
# Cisco ASA
access-list BLOCK_MALICIOUS_IPS extended deny ip any host 203.0.113.45
access-list BLOCK_MALICIOUS_IPS extended deny ip any host 198.51.100.23

# iptables (Linux)
iptables -A OUTPUT -d 203.0.113.45 -j DROP
iptables -A OUTPUT -d 198.51.100.23 -j DROP
```

### 2.3 Identificar Outros Sistemas Afetados

**Scan de Rede:**

```powershell
# Procurar por IOCs em outros sistemas (via WMI/PSRemoting)
$computers = Get-ADComputer -Filter * | Select-Object -ExpandProperty Name

foreach ($computer in $computers) {
    if (Test-Connection -ComputerName $computer -Count 1 -Quiet) {
        Invoke-Command -ComputerName $computer -ScriptBlock {
            Get-Process | Where-Object {$_.ProcessName -match "ransom|crypt"}
        }
    }
}
```

**Logs Centralizados (SIEM):**

```
# Query exemplo (Splunk)
index=windows EventCode=4688 
| search CommandLine="*encrypt*" OR CommandLine="*ransom*"
| stats count by ComputerName, User, CommandLine
```

### 2.4 Preservar Evidências

**Coleta de Memória (se sistema ainda ligado):**

```powershell
# Usar DumpIt, FTK Imager, ou Magnet RAM Capture
.\DumpIt.exe /output E:\evidence\memory_COMPUTERNAME_$(Get-Date -f yyyyMMdd_HHmmss).dmp
```

**Coleta de Logs:**

```powershell
# Event Logs
$outputDir = "E:\evidence\logs"
wevtutil epl Security "$outputDir\Security.evtx"
wevtutil epl System "$outputDir\System.evtx"
wevtutil epl Application "$outputDir\Application.evtx"

# Sysmon (se instalado)
wevtutil epl "Microsoft-Windows-Sysmon/Operational" "$outputDir\Sysmon.evtx"
```

**Cópia da Nota de Resgate:**

```powershell
# Procurar e copiar notas de resgate
Get-ChildItem -Path C:\ -Recurse -Include "README.txt","HOW_TO_DECRYPT.html" -ErrorAction SilentlyContinue |
    Copy-Item -Destination "E:\evidence\ransom_notes\"
```

---

## 🧹 FASE 3: ERRADICAÇÃO (1-4 horas)

### 3.1 Identificar Variante

**Ferramentas de Identificação:**

- **ID Ransomware:** https://id-ransomware.malwarehunterteam.com/
  - Upload de arquivo criptografado + nota de resgate
  
- **No More Ransom:** https://www.nomoreransom.org/
  - Verificar se há decryptor disponível

**Análise de Amostra:**

```bash
# Análise de hash (VirusTotal)
# NÃO faça upload de dados sensíveis!
Get-FileHash -Path "C:\malware\sample.exe" -Algorithm SHA256

# Strings (procurar por IOCs)
strings64.exe C:\malware\sample.exe > sample_strings.txt
```

### 3.2 Remover Malware

**Scan Completo:**

```powershell
# Windows Defender Offline Scan
Start-Process -FilePath "C:\Program Files\Windows Defender\MpCmdRun.exe" -ArgumentList "-Scan -ScanType 3"

# Se EDR disponível, executar scan completo
```

**Verificar Persistência:**

```powershell
# Registry Run Keys
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

# Scheduled Tasks
Get-ScheduledTask | Where-Object {$_.TaskPath -notlike "\Microsoft\*"} | 
    Select-Object TaskName, TaskPath, State

# Services suspeitos
Get-Service | Where-Object {$_.DisplayName -notlike "Microsoft*" -and $_.Status -eq "Running"}
```

### 3.3 Reconstruir Sistemas Críticos

**Opção A: Reimagem (RECOMENDADO)**

```bash
# 1. Backup de dados do usuário (apenas não-criptografados)
# 2. Formatar completamente o disco
# 3. Instalar de imagem limpa (gold image)
# 4. Aplicar patches mais recentes
# 5. Instalar EDR/AV atualizado
# 6. Restaurar dados do usuário (com scan)
```

**Opção B: Limpeza Manual (não recomendado)**

```powershell
# Apenas se reimagem não for opção
# 1. Remover malware e persistência
# 2. Atualizar tudo (patches)
# 3. Trocar todas as credenciais
# 4. Scan completo com múltiplas ferramentas
# 5. Monitoramento intensivo
```

---

## 🔄 FASE 4: RECUPERAÇÃO (4-24 horas)

### 4.1 Avaliação de Backup

**Checklist de Backup:**

- [ ] Identificar backup mais recente não-afetado
- [ ] Verificar integridade do backup
- [ ] Confirmar que backup não está criptografado
- [ ] Verificar se backup não contém malware
- [ ] Documentar data/hora do backup

**Scan de Backup:**

```powershell
# Montar backup em sistema isolado
# Executar scan AV completo ANTES de restaurar

# Verificar por executáveis suspeitos
Get-ChildItem -Path "E:\backup" -Recurse -Include "*.exe","*.dll","*.ps1" | 
    ForEach-Object {
        $hash = Get-FileHash $_.FullName -Algorithm SHA256
        [PSCustomObject]@{
            File = $_.FullName
            Hash = $hash.Hash
            Size = $_.Length
            Modified = $_.LastWriteTime
        }
    } | Export-Csv "backup_executables.csv"
```

### 4.2 Restauração de Dados

**Processo de Restore:**

```powershell
# 1. Criar diretório temporário para restore
New-Item -Path "C:\Restore_Temp" -ItemType Directory

# 2. Restaurar dados críticos primeiro
robocopy "\\backup\share\critical_data" "C:\Restore_Temp" /E /Z /LOG:restore.log

# 3. Scan completo do restaurado
Start-Process -FilePath "C:\Program Files\Windows Defender\MpCmdRun.exe" `
    -ArgumentList "-Scan -ScanType 3 -File C:\Restore_Temp"

# 4. Se limpo, mover para localização final
```

**Priorização de Restore:**

1. **Crítico (0-2 horas):**
   - Sistemas de produção
   - Bancos de dados principais
   - Aplicações core de negócio

2. **Alto (2-8 horas):**
   - Email e comunicações
   - Sistemas financeiros
   - CRM/ERP

3. **Médio (8-24 horas):**
   - Estações de trabalho
   - Dados departamentais
   - Aplicações secundárias

### 4.3 Validação de Sistemas

**Testes de Integridade:**

- [ ] Verificar funcionalidade de aplicações
- [ ] Confirmar acesso de usuários
- [ ] Validar integridade de dados
- [ ] Testar backups (restore test)
- [ ] Confirmar conectividade de rede
- [ ] Verificar logs de erro

**Monitoramento Intensivo (30 dias):**

```
Alertas Específicos:
- Qualquer execução de processo suspeito
- Tentativas de criptografia em massa
- Conexões para IPs de C2 conhecidos
- Modificação de registry keys de persistência
- Criação de scheduled tasks não-autorizadas
```

---

## 📊 FASE 5: PÓS-INCIDENTE (24-72 horas)

### 5.1 Análise de Causa Raiz

**Investigar Vetor de Entrada:**

Possíveis Vetores:
- [ ] Email de phishing
- [ ] RDP exposto/credenciais fracas
- [ ] Vulnerabilidade explorada (CVE-XXXX-XXXX)
- [ ] Drive-by download
- [ ] Insider threat
- [ ] Malvertising
- [ ] Supply chain (software comprometido)

**Análise Forense:**

```powershell
# Revisar logs de autenticação
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624,4625} |
    Where-Object {$_.TimeCreated -ge (Get-Date).AddDays(-7)} |
    Select-Object TimeCreated, Message |
    Out-GridView

# Revisar comandos PowerShell executados (se logging habilitado)
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; ID=4104}
```

### 5.2 Documentação Completa

**Relatório de Incidente:**

Use template: `FORENSIC_REPORT_TEMPLATE.md`

Incluir:
- Timeline detalhado
- IOCs identificados
- Sistemas afetados
- Vetor de entrada
- Ações tomadas
- Dados perdidos/recuperados
- Lições aprendidas

### 5.3 Melhorias Implementadas

**Correções Imediatas:**

- [ ] Patch de vulnerabilidades exploradas
- [ ] Bloqueio de IOCs (IPs, domínios, hashes)
- [ ] Atualização de regras de EDR/AV
- [ ] Hardening de sistemas expostos
- [ ] Troca de credenciais comprometidas

**Melhorias de Segurança:**

| Controle | Prazo | Responsável | Status |
|----------|-------|-------------|--------|
| Implementar MFA em RDP | 7 dias | TI | ⏳ |
| Email sandboxing | 30 dias | SecOps | 📋 |
| Segregação de backups (air gap) | 60 dias | TI | 📋 |
| EDR em todos endpoints | 30 dias | SecOps | ⏳ |
| Treinamento de phishing | 30 dias | RH | 📋 |

### 5.4 Lições Aprendidas

**Reunião de Post-Mortem:**

Agendar dentro de 72 horas após recuperação.

**Agenda:**
1. Cronologia do incidente (15 min)
2. O que funcionou bem? (15 min)
3. O que pode melhorar? (30 min)
4. Ação items (30 min)

**Perguntas a Responder:**
- Detecção foi rápida o suficiente?
- Contenção foi efetiva?
- Backup estava atualizado e funcional?
- Comunicação foi clara?
- Playbook ajudou ou precisa atualização?

---

## 📋 DECISÃO: PAGAR OU NÃO PAGAR?

### ⚠️ IMPORTANTE

**Posição Oficial:** **NÃO RECOMENDAMOS PAGAMENTO**

**Razões:**
- Não há garantia de recuperação
- Financia crime organizado
- Pode marcar organização como "pagadora"
- Pode violar sanções internacionais
- Dados podem vazar mesmo com pagamento (double extortion)

### Fatores a Considerar

**Pagar Pode Ser Considerado Se:**
- [ ] Backup não existe ou está corrompido
- [ ] Dados são críticos para vida/saúde (hospital)
- [ ] Perda financeira excede valor do resgate
- [ ] Após consulta com Legal e Executivo
- [ ] Negociador profissional envolvido

**Processo de Decisão:**

```
1. Avaliar impacto total sem pagamento
2. Consultar Legal sobre legalidade
3. Consultar Seguradora
4. Aprovar em nível C-Level
5. Documentar decisão e justificativa
6. Se pagar: usar negociador profissional
```

### Alternativas ao Pagamento

- Restaurar de backup
- Verificar se decryptor disponível (No More Ransom)
- Aceitar perda de dados
- Reconstruir dados de fontes alternativas

---

## 🔧 FERRAMENTAS NECESSÁRIAS

### Software de IR

| Ferramenta | Uso | Download |
|------------|-----|----------|
| **FTK Imager** | Coleta de memória/disco | AccessData |
| **Volatility** | Análise de memória | https://www.volatilityfoundation.org/ |
| **KAPE** | Coleta de artefatos | Eric Zimmerman |
| **Autoruns** | Verificar persistência | Sysinternals |
| **Process Explorer** | Análise de processos | Sysinternals |
| **TCPView** | Conexões de rede | Sysinternals |
| **Wireshark** | Análise de tráfego | https://www.wireshark.org/ |

### Decryptors Conhecidos

- **No More Ransom Project:** https://www.nomoreransom.org/
- **Emsisoft:** https://www.emsisoft.com/ransomware-decryption-tools/
- **Kaspersky:** https://noransom.kaspersky.com/
- **Avast:** https://www.avast.com/ransomware-decryption-tools

---

## 📞 COMUNICAÇÃO

### Templates de Comunicação

**Email para Usuários (Interno):**

```
Assunto: [URGENTE] Incidente de Segurança - Ação Necessária

Prezados Colaboradores,

Identificamos um incidente de segurança que afetou alguns sistemas da empresa.

AÇÕES IMEDIATAS:
1. NÃO abra emails suspeitos
2. NÃO clique em links desconhecidos
3. REPORTE qualquer comportamento estranho no seu computador
4. MANTENHA seu computador ligado e conectado à rede

Nossa equipe de TI está trabalhando na resolução. Atualizações serão enviadas a cada 2 horas.

Dúvidas: Entre em contato com helpdesk@empresa.com

Obrigado pela cooperação.

Equipe de Segurança da Informação
```

**Comunicado à Imprensa (se necessário):**

```
Coordenar com Relações Públicas e Legal antes de qualquer comunicação externa.

Pontos-chave:
- Reconhecer o incidente sem detalhes técnicos
- Enfatizar medidas tomadas
- Confirmar que autoridades foram notificadas
- Informar se dados de clientes foram afetados (se aplicável)
- Disponibilizar canal para clientes afetados
```

---

## ✅ CHECKLIST COMPLETO

### Detecção
- [ ] Incidente confirmado
- [ ] Variante identificada
- [ ] Escopo inicial determinado
- [ ] Partes interessadas notificadas
- [ ] Equipe de IR acionada

### Contenção
- [ ] Sistemas afetados isolados
- [ ] Propagação interrompida
- [ ] IOCs bloqueados no firewall
- [ ] Contas comprometidas desabilitadas
- [ ] Evidências preservadas

### Erradicação
- [ ] Malware removido
- [ ] Persistência eliminada
- [ ] Sistemas reconstruídos ou limpos
- [ ] Patches aplicados
- [ ] Credenciais trocadas

### Recuperação
- [ ] Backup validado
- [ ] Dados restaurados
- [ ] Sistemas em produção
- [ ] Funcionalidade confirmada
- [ ] Monitoramento intensivo ativado

### Pós-Incidente
- [ ] Relatório completo gerado
- [ ] IOCs compartilhados (CERT.br, etc)
- [ ] Melhorias implementadas
- [ ] Reunião de lições aprendidas
- [ ] Playbook atualizado

---

## 📚 REFERÊNCIAS

- NIST SP 800-61 Rev. 2: Computer Security Incident Handling Guide
- SANS Ransomware Response Checklist
- CISA Ransomware Guide: https://www.cisa.gov/stopransomware
- No More Ransom: https://www.nomoreransom.org/
- MITRE ATT&CK T1486: https://attack.mitre.org/techniques/T1486/

---

<div align="center">

**Este playbook deve ser testado regularmente via table-top exercises**

**Última Atualização:** 2025-11-22  
**Próxima Revisão:** 2026-05-22

---

*Playbook mantido por RedTeam-Essentials*  
*Baseado em melhores práticas da indústria*

</div>
