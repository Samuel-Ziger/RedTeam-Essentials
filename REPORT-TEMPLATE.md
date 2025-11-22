# 📄 Template de Relatório Red Team

> **Modelo profissional para documentação de operações Red Team**

Este template segue padrões da indústria e pode ser adaptado para diferentes tipos de engagement (penetration test, red team, vulnerability assessment).

---

## 📋 Metadados do Relatório

```
Título: [Nome do Projeto/Engagement]
Cliente: [Nome da Organização]
Data do Engagement: [DD/MM/YYYY - DD/MM/YYYY]
Data do Relatório: [DD/MM/YYYY]
Versão: [1.0]
Classificação: [CONFIDENCIAL / RESTRITO]
Preparado por: [Nome do Red Team / Empresa]
```

---

## 📑 Índice

1. [Sumário Executivo](#sumário-executivo)
2. [Escopo e Metodologia](#escopo-e-metodologia)
3. [Resumo Técnico](#resumo-técnico)
4. [Achados Detalhados](#achados-detalhados)
5. [Caminho de Ataque (Attack Path)](#caminho-de-ataque)
6. [Recomendações](#recomendações)
7. [Conclusão](#conclusão)
8. [Apêndices](#apêndices)

---

## 1. Sumário Executivo

> **Destinado a:** C-Level, gerência, tomadores de decisão não-técnicos

### 1.1 Visão Geral

Este relatório documenta os resultados de um engagement de Red Team conduzido entre **[data início]** e **[data fim]** para **[nome da organização]**.

O objetivo foi avaliar a postura de segurança da organização simulando um adversário real, com foco em:
- [x] Obtenção de acesso inicial
- [x] Escalação de privilégios
- [x] Movimento lateral
- [x] Persistência
- [x] Exfiltração de dados (simulada)

### 1.2 Resultados Resumidos

**Nível de Risco Geral:** 🔴 CRÍTICO / 🟠 ALTO / 🟡 MÉDIO / 🟢 BAIXO

| Categoria | Crítico | Alto | Médio | Baixo | Total |
|-----------|---------|------|-------|-------|-------|
| Vulnerabilidades | X | X | X | X | XX |
| Configurações Inseguras | X | X | X | X | XX |
| Controles Ausentes | X | X | X | X | XX |

### 1.3 Principais Achados

**⚠️ Achados Críticos:**
1. **[Título do Achado]** - Permitiu acesso completo ao Domain Controller
2. **[Título do Achado]** - Credenciais hardcoded em aplicação web
3. **[Título do Achado]** - Ausência de segmentação de rede

**Impacto:**
- ⚠️ Acesso completo ao Active Directory em menos de 24 horas
- ⚠️ Exfiltração simulada de dados sensíveis (PII, financeiros)
- ⚠️ Persistência estabelecida sem detecção

### 1.4 Recomendações Prioritárias

**Ação Imediata (0-30 dias):**
1. Remediar credenciais hardcoded em aplicações
2. Implementar MFA em todos os acessos administrativos
3. Revisar e remediar privilégios excessivos no AD

**Curto Prazo (30-90 dias):**
1. Implementar segmentação de rede (VLANs, firewalls internos)
2. Deploy de EDR em todos os endpoints
3. Hardening de configurações de servidores

**Médio Prazo (90-180 dias):**
1. Implementar programa de monitoramento contínuo (SIEM)
2. Criar playbooks de resposta a incidentes
3. Treinamento de segurança para usuários

---

## 2. Escopo e Metodologia

### 2.1 Objetivos do Engagement

**Objetivos Definidos:**
- [ ] Obter acesso à rede interna
- [ ] Comprometer o Active Directory
- [ ] Acessar dados sensíveis (crown jewels)
- [ ] Estabelecer persistência
- [ ] Simular exfiltração de dados

**Cenário:**
- **Tipo:** Red Team / Penetration Test / Vulnerability Assessment
- **Perspectiva:** Externa / Interna / Híbrida
- **Conhecimento Prévio:** Black Box / Gray Box / White Box

### 2.2 Escopo Técnico

**Incluído no Escopo:**
- Faixas de IP: `10.10.0.0/16`, `192.168.1.0/24`
- Domínios: `exemplo.com`, `*.exemplo.com`
- Aplicações Web: `https://app.exemplo.com`
- Active Directory: `EXEMPLO.LOCAL`
- Funcionários: Social engineering permitido via email apenas

**Fora do Escopo:**
- Denial of Service (DoS/DDoS)
- Ataques físicos
- Social engineering presencial
- Sistemas de produção críticos: `[lista específica]`

### 2.3 Metodologia

Este engagement seguiu as seguintes frameworks e metodologias:

**Frameworks Utilizados:**
- ✅ **MITRE ATT&CK:** Mapeamento de táticas e técnicas
- ✅ **PTES (Penetration Testing Execution Standard)**
- ✅ **OWASP Testing Guide** (para aplicações web)
- ✅ **NIST Cybersecurity Framework**

**Fases Executadas:**

```
┌─────────────────────────────────────────────────────┐
│ 1. Reconhecimento (3 dias)                          │
│    - OSINT, DNS enum, subdomain discovery           │
├─────────────────────────────────────────────────────┤
│ 2. Enumeração e Scanning (2 dias)                   │
│    - Port scanning, service identification          │
├─────────────────────────────────────────────────────┤
│ 3. Exploração e Acesso Inicial (5 dias)             │
│    - Exploração de vulnerabilidades, phishing       │
├─────────────────────────────────────────────────────┤
│ 4. Pós-Exploração e Escalação (4 dias)              │
│    - Privilege escalation, credential dumping       │
├─────────────────────────────────────────────────────┤
│ 5. Movimento Lateral (3 dias)                       │
│    - Pass-the-hash, lateral movement, AD compromise │
├─────────────────────────────────────────────────────┤
│ 6. Persistência e Exfiltração (2 dias)              │
│    - Backdoors, data exfiltration (simulated)       │
├─────────────────────────────────────────────────────┤
│ 7. Documentação e Relatório (5 dias)                │
│    - Screenshot organization, report writing        │
└─────────────────────────────────────────────────────┘

Total: 24 dias úteis
```

### 2.4 Limitações e Restrições

**Restrições Aplicadas:**
- ⚠️ Testes realizados apenas em horário comercial
- ⚠️ Sistemas de produção críticos excluídos
- ⚠️ Limites de taxa de scanning: máximo 100 req/s
- ⚠️ Blue Team não foi notificado (true red team)

---

## 3. Resumo Técnico

> **Destinado a:** Equipe técnica, administradores de sistemas, blue team

### 3.1 Timeline do Ataque

```
Day 1-3: Reconhecimento
├─ Enumeração DNS revelou 47 subdomínios
├─ Identificados 3 servidores web vulneráveis
└─ OSINT revelou 15 emails de funcionários

Day 4-5: Acesso Inicial
├─ Phishing email enviado para 15 alvos
├─ 3 cliques obtidos, 1 credencial capturada
└─ Acesso inicial via VPN com credenciais válidas

Day 6-10: Escalação de Privilégios
├─ Enumeração de Active Directory
├─ Kerberoasting revelou 5 contas de serviço
├─ Crackeo de hash resultou em credencial válida
└─ Comprometimento de Domain Admin

Day 11-15: Movimento Lateral
├─ Pass-the-Hash para 12 workstations
├─ Access to file server contendo dados sensíveis
└─ Persistência via Golden Ticket

Day 16-20: Objetivos Alcançados
├─ Acesso a crown jewels (DB de clientes)
├─ Exfiltração simulada de 10 GB de dados
└─ Persistência mantida por 7 dias sem detecção
```

### 3.2 Estatísticas do Engagement

| Métrica | Valor |
|---------|-------|
| **Duração total** | 24 dias úteis |
| **Hosts descobertos** | 247 |
| **Portas abertas identificadas** | 1,342 |
| **Vulnerabilidades encontradas** | 73 |
| **Vulnerabilidades exploradas** | 12 |
| **Credenciais obtidas** | 45 pares user/pass |
| **Hosts comprometidos** | 23 |
| **Objetivos alcançados** | 5/5 (100%) |
| **Tempo até Domain Admin** | 8 dias |
| **Detecções pelo Blue Team** | 0 |

### 3.3 Vetor de Ataque Principal

**Cadeia de Ataque (Kill Chain):**

```
1. Reconnaissance
   ↓
2. Weaponization (Phishing email com payload)
   ↓
3. Delivery (Email enviado para 15 funcionários)
   ↓
4. Exploitation (1 usuário executou payload)
   ↓
5. Installation (Beacon Cobalt Strike instalado)
   ↓
6. Command & Control (C2 estabelecido)
   ↓
7. Actions on Objectives (Domain compromise + data exfil)
```

---

## 4. Achados Detalhados

### Formato de Achado Individual

**Para cada vulnerabilidade/achado, use este template:**

---

#### 🔴 ACHADO #001: [Título Descritivo]

**Severidade:** 🔴 CRÍTICA

**CVSS v3.1 Score:** 9.8 (Critical)  
**Vector String:** CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

**MITRE ATT&CK:**
- **Tática:** TA0006 - Credential Access
- **Técnica:** T1558.003 - Kerberoasting

**Categorias:**
- [x] Configuração Insegura
- [ ] Vulnerabilidade de Software
- [ ] Controle Ausente
- [ ] Erro de Lógica de Negócio

---

**Descrição:**

Durante a enumeração do Active Directory, identificamos que múltiplas contas de serviço possuem Service Principal Names (SPNs) configurados e são vulneráveis a ataques de Kerberoasting.

**Sistemas Afetados:**
- `EXEMPLO.LOCAL` (Domain Controller)
- Contas: `SVC-SQL`, `SVC-BACKUP`, `SVC-WEB`, `SVC-SHAREPOINT`, `SVC-EXCHANGE`

**Passo a Passo da Exploração:**

1. **Enumeração de SPNs:**
```powershell
# Comando executado
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
```

Resultado: 5 contas de serviço identificadas

2. **Solicitação de Tickets TGS:**
```bash
# Usando Rubeus
.\Rubeus.exe kerberoast /outfile:hashes.txt
```

3. **Crack de Hashes:**
```bash
hashcat -m 13100 hashes.txt rockyou.txt
```

**Tempo de crack:** 3 horas  
**Senha descoberta:** `SVC-SQL:Summer2023!`

4. **Verificação de Privilégios:**
```powershell
# A conta SVC-SQL possui privilégios de Domain Admin
net user SVC-SQL /domain
```

**Impacto:**

- ⚠️ **Confidencialidade:** ALTA - Acesso completo ao Domain Controller
- ⚠️ **Integridade:** ALTA - Capacidade de modificar qualquer objeto do AD
- ⚠️ **Disponibilidade:** ALTA - Potencial para DoS do domínio inteiro

**Impacto de Negócio:**
- Comprometimento total do Active Directory
- Acesso a todos os sistemas da rede
- Capacidade de criar contas administrativas persistentes
- Potencial exfiltração de dados de toda a organização

**Evidências:**

![Screenshot da enumeração de SPNs](images/kerberoast_enum.png)

![Hash capturado](images/kerberoast_hash.png)

![Acesso com credencial crackeada](images/kerberoast_access.png)

**Recomendações:**

**Imediato (0-7 dias):**
1. ✅ Alterar senhas de todas as contas de serviço para senhas complexas (25+ caracteres)
2. ✅ Implementar Group Managed Service Accounts (gMSA) quando possível
3. ✅ Auditar e remover privilégios excessivos de contas de serviço

**Curto Prazo (7-30 dias):**
1. ✅ Implementar monitoramento de eventos 4769 (TGS requests anômalos)
2. ✅ Configurar honeypot accounts com SPNs para detectar Kerberoasting
3. ✅ Implementar política de senha de 30+ caracteres para contas de serviço

**Médio Prazo (30-90 dias):**
1. ✅ Migrar para gMSA em toda a infraestrutura
2. ✅ Implementar PAM (Privileged Access Management) solution
3. ✅ Regular review de privilégios e SPNs

**Referências:**
- [MITRE ATT&CK T1558.003](https://attack.mitre.org/techniques/T1558/003/)
- [Microsoft: Kerberoasting without Mimikatz](https://docs.microsoft.com/security)
- [Detecting Kerberoasting Activity](https://adsecurity.org)

---

**[Repetir template acima para cada achado]**

---

## 5. Caminho de Ataque (Attack Path)

### 5.1 Diagrama de Ataque

```
┌──────────────┐
│   Internet   │
└──────┬───────┘
       │
       │ [Phishing Email]
       ↓
┌──────────────────┐
│  User Workstation│ (10.10.50.15)
│  user: jdoe      │
└──────┬───────────┘
       │
       │ [Credential Harvesting]
       ↓
┌──────────────────┐
│  VPN Gateway     │ (vpn.exemplo.com)
│                  │
└──────┬───────────┘
       │
       │ [VPN Access with valid creds]
       ↓
┌──────────────────┐
│  Internal Network│ (10.10.0.0/16)
│                  │
└──────┬───────────┘
       │
       │ [AD Enumeration + Kerberoasting]
       ↓
┌──────────────────┐
│ Domain Controller│ (10.10.10.5)
│  EXEMPLO-DC01    │
│  Domain Admin ✓  │
└──────┬───────────┘
       │
       │ [Golden Ticket + Lateral Movement]
       ↓
┌──────────────────────────────────────┐
│  Crown Jewels Accessed:              │
│  - File Server (Customer DB)         │
│  - SQL Server (Financial Data)       │
│  - SharePoint (Internal Docs)        │
└──────────────────────────────────────┘
```

### 5.2 Técnicas MITRE ATT&CK Utilizadas

| Tática | Técnica | ID | Descrição |
|--------|---------|----|-----------  |
| Reconnaissance | Gather Victim Identity Information | T1589 | OSINT de funcionários via LinkedIn |
| Initial Access | Phishing | T1566.001 | Email de phishing com link malicioso |
| Execution | User Execution | T1204.001 | Usuário executou payload |
| Persistence | Create Account | T1136.002 | Criação de conta de domínio |
| Privilege Escalation | Valid Accounts | T1078.002 | Uso de credenciais de Domain Admin |
| Defense Evasion | Obfuscated Files or Information | T1027 | Ofuscação de payload |
| Credential Access | Kerberoasting | T1558.003 | Ataque de Kerberoasting |
| Discovery | Account Discovery | T1087.002 | Enumeração de AD |
| Lateral Movement | Remote Services | T1021.001 | RDP para workstations |
| Collection | Data from Network Shared Drive | T1039 | Acesso a file servers |
| Exfiltration | Exfiltration Over C2 Channel | T1041 | Dados exfiltrados via C2 |

---

## 6. Recomendações

### 6.1 Recomendações por Prioridade

#### 🔴 CRÍTICO (0-30 dias)

**1. Implementar Multi-Factor Authentication (MFA)**
- **Onde:** VPN, Outlook Web Access, RDP, acesso administrativo
- **Custo Estimado:** Médio
- **Esforço:** Médio
- **Impacto:** Alto

**2. Remediar Kerberoasting**
- **Ação:** Alterar senhas de contas de serviço, implementar gMSA
- **Custo Estimado:** Baixo
- **Esforço:** Baixo
- **Impacto:** Crítico

**3. Remover Privilégios Excessivos**
- **Ação:** Revisar e remover membros desnecessários de Domain Admins
- **Custo Estimado:** Baixo
- **Esforço:** Médio
- **Impacto:** Alto

---

#### 🟠 ALTO (30-90 dias)

**4. Implementar EDR em Todos os Endpoints**
- **Produto:** CrowdStrike / SentinelOne / Microsoft Defender for Endpoint
- **Custo Estimado:** Alto
- **Esforço:** Alto
- **Impacto:** Crítico

**5. Segmentação de Rede**
- **Ação:** Implementar VLANs, firewalls internos, zero trust
- **Custo Estimado:** Alto
- **Esforço:** Alto
- **Impacto:** Alto

---

#### 🟡 MÉDIO (90-180 dias)

**6. Programa de Awareness de Segurança**
- **Ação:** Treinamento trimestral, simulações de phishing
- **Custo Estimado:** Médio
- **Esforço:** Médio
- **Impacto:** Médio

**7. SIEM e Monitoramento Contínuo**
- **Produto:** Splunk / ELK / Azure Sentinel
- **Custo Estimado:** Alto
- **Esforço:** Alto
- **Impacto:** Alto

---

### 6.2 Roadmap de Implementação

```
Mês 1-3: Remediações Críticas
├─ Implementar MFA
├─ Remediar Kerberoasting
├─ Revisar privilégios do AD
└─ Patch management de vulnerabilidades críticas

Mês 4-6: Fortalecimento de Defesas
├─ Deploy de EDR
├─ Início de segmentação de rede
├─ Implementar baselines de hardening
└─ Criar playbooks de resposta a incidentes

Mês 7-12: Maturidade de Segurança
├─ SIEM deployment completo
├─ Programa de threat hunting
├─ Purple team exercises
└─ Continuous improvement
```

---

## 7. Conclusão

### 7.1 Resumo dos Achados

Este engagement demonstrou que a organização possui **gaps significativos** em sua postura de segurança que podem ser explorados por um adversário com recursos moderados.

**Principais Conclusões:**
- ⚠️ Acesso inicial foi obtido em **2 dias** via phishing
- ⚠️ Comprometimento completo do AD em **8 dias**
- ⚠️ **Zero detecções** pelo Blue Team durante todo o engagement
- ⚠️ Persistência mantida por **7 dias** sem ser descoberta

**Pontos Positivos Identificados:**
- ✅ Patch management razoável (80% dos sistemas atualizados)
- ✅ Firewall perimetral configurado adequadamente
- ✅ Políticas de senha atendem requisitos mínimos

**Áreas de Melhoria Crítica:**
- ❌ Falta de MFA em acessos críticos
- ❌ Ausência de EDR/monitoramento de endpoints
- ❌ Privilégios excessivos no Active Directory
- ❌ Segmentação de rede insuficiente
- ❌ Falta de detecção e resposta a incidentes

### 7.2 Risco Residual

**Antes do Engagement:** 🔴 CRÍTICO  
**Após Implementação das Recomendações:** 🟡 MÉDIO

Com a implementação das recomendações críticas e de alta prioridade, estimamos uma redução de **70% no risco** de comprometimento bem-sucedido.

### 7.3 Próximos Passos Recomendados

1. **Reunião de debrief** com stakeholders técnicos e executivos
2. **Plano de ação** com prazos e responsáveis definidos
3. **Re-teste** em 6 meses para validar remediações
4. **Purple Team Exercise** para melhorar detecção
5. **Continuous Red Teaming** como parte do programa de segurança

---

## 8. Apêndices

### Apêndice A: Lista Completa de Hosts Comprometidos

| Hostname | IP Address | Tipo | Data Compromisso | Método |
|----------|------------|------|------------------|--------|
| EXEMPLO-DC01 | 10.10.10.5 | Domain Controller | 15/11/2025 | Kerberoasting |
| WEB-SERVER-01 | 10.10.20.10 | Web Server | 10/11/2025 | SQL Injection |
| FILE-SERVER-01 | 10.10.30.5 | File Server | 16/11/2025 | Pass-the-Hash |
| ... | ... | ... | ... | ... |

### Apêndice B: Credenciais Obtidas

**[REDACTED - Fornecido separadamente em arquivo criptografado]**

### Apêndice C: Comandos Executados

```bash
# Enumeração inicial
nmap -sC -sV -oA nmap_scan 10.10.0.0/16

# Kerberoasting
Get-ADUser -Filter {ServicePrincipalName -ne "$null"}
.\Rubeus.exe kerberoast

# Golden Ticket
.\mimikatz.exe "kerberos::golden /domain:exemplo.local /sid:S-1-5-21-... /rc4:NTLM_HASH /user:fakeadmin /id:500 /ptt"
```

### Apêndice D: Ferramentas Utilizadas

- Nmap 7.94
- Metasploit Framework 6.3
- Cobalt Strike 4.9
- BloodHound 4.3
- Rubeus
- Mimikatz
- Burp Suite Professional
- Custom scripts (fornecidos separadamente)

### Apêndice E: Glossário de Termos

- **AD:** Active Directory
- **C2:** Command and Control
- **EDR:** Endpoint Detection and Response
- **gMSA:** Group Managed Service Account
- **MFA:** Multi-Factor Authentication
- **SIEM:** Security Information and Event Management
- **SPN:** Service Principal Name
- **TGS:** Ticket Granting Service

---

## 📝 Controle de Versões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 0.1 | 20/11/2025 | Red Team Lead | Draft inicial |
| 0.2 | 22/11/2025 | Technical Writer | Revisão técnica |
| 1.0 | 25/11/2025 | Management | Versão final |

---

## 🔒 Classificação de Segurança

```
╔═══════════════════════════════════════════════════════╗
║                    CONFIDENCIAL                       ║
║                                                       ║
║  Este documento contém informações sensíveis sobre    ║
║  vulnerabilidades de segurança. Não distribuir sem    ║
║  autorização expressa.                                ║
║                                                       ║
║  Destruir após implementação das remediações.         ║
╚═══════════════════════════════════════════════════════╝
```

---

<div align="center">

**Preparado por: RedTeam Essentials**  
**Email: redteam@exemplo.com**  
**Data: 25 de Novembro de 2025**

---

*Este relatório é propriedade de [Nome da Organização] e contém informações confidenciais.*

</div>
