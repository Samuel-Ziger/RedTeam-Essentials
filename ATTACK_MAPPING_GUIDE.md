# 🎯 Guia de Uso - Mapeamento MITRE ATT&CK

Este guia explica como usar o mapeamento MITRE ATT&CK do RedTeam-Essentials.

---

## 📋 O Que é o Mapeamento ATT&CK?

O arquivo `MITRE-ATTACK-MAPPING.json` contém um **layer** do ATT&CK Navigator que mapeia todas as técnicas cobertas por este repositório.

**Benefícios:**
- 🎯 Visualizar graficamente suas áreas de conhecimento
- 📊 Identificar gaps de aprendizado
- 🔍 Correlacionar com APTs reais
- 📝 Documentar testes com IDs oficiais
- 🎓 Estudar de forma estruturada

---

## 🌐 Como Visualizar no ATT&CK Navigator

### Passo 1: Acessar o Navigator

Abra em seu navegador:
```
https://mitre-attack.github.io/attack-navigator/
```

### Passo 2: Carregar o Layer

1. Clique em **"Open Existing Layer"** (parte superior)
2. Clique em **"Upload from local"**
3. Selecione o arquivo: `MITRE-ATTACK-MAPPING.json`
4. Aguarde o carregamento

### Passo 3: Explorar a Visualização

Você verá um heatmap com cores:

| Cor | Score | Significado |
|-----|-------|-------------|
| 🟢 Verde Escuro | 100 | Maior profundidade editorial declarada |
| 🟢 Verde Médio | 75 | Profundidade intermediária |
| 🟡 Verde Claro | 50 | Introdução, teoria ou exemplos |
| 🟡 Amarelo | 25 | Planejado - futuro desenvolvimento |
| ⚪ Branco | 0 | Não coberto |

---

## 📊 Técnicas Cobertas (52 entradas validadas)

O layer da **v2.1** cobre principalmente os módulos 01–14. Os módulos mais
novos ainda precisam de revisão técnica antes de ampliar o layer; quantidade de
técnicas não representa profundidade ou eficácia de detecção.

| Area | Modulos | Exemplos |
|------|---------|----------|
| Initial Access | 35, 30 | T1566, T1190, T1133 |
| Windows Privesc | 36 | T1548, T1134, T1068 |
| Web AppSec labs | 30 | T1190 (SQLi/SSRF/XSS) |
| Cloud / Containers | 32, 33 | T1580, T1611, T1610 |
| Post-Ex / Exfil | 37 | T1041, T1005, T1090 |
| C2 / Stealth (teoria) | 35 | T1071, T1685, T1027 |

### Reconnaissance (TA0043) - 6 técnicas

| ID | Técnica | Score | Módulo | Recursos |
|----|---------|-------|--------|----------|
| **T1590** | Gather Victim Network Information | 100% | 29-Reconhecimento-OSINT | dns_enum.ps1, passive_recon_cheatsheet.md |
| **T1592** | Gather Victim Host Information | 100% | 29-Reconhecimento-OSINT | Reconhecimento passivo |
| **T1596** | Search Open Technical Databases | 100% | 29-Reconhecimento-OSINT | DNS enumeration |
| **T1593** | Search Open Websites/Domains | 100% | 29-Reconhecimento-OSINT | osint_automation.ps1 |
| **T1594** | Search Victim-Owned Websites | 100% | 29-Reconhecimento-OSINT | Pesquisa em sites |
| **T1598** | Phishing for Information | 75% | 29 + 35 | phishing-teoria.md |

### Discovery (TA0007) - 4 técnicas

| ID | Técnica | Score | Módulo | Recursos |
|----|---------|-------|--------|----------|
| **T1087** | Account Discovery | 100% | 31-Active-Directory-Identidade | ad_enum_commands.md |
| **T1069** | Permission Groups Discovery | 100% | 31-Active-Directory-Identidade | Enumeração de grupos |
| **T1482** | Domain Trust Discovery | 100% | 31-Active-Directory-Identidade | Trusts de domínio |
| **T1083** | File and Directory Discovery | 75% | 28-Engenharia-Ferramentas-Seguranca | organize_logs.ps1 |

### Credential Access (TA0006) - 3 técnicas

| ID | Técnica | Score | Módulo | Recursos |
|----|---------|-------|--------|----------|
| **T1558.003** | Kerberoasting | 100% | 31-Active-Directory-Identidade | kerberoasting_teoria.md |
| **T1558.004** | AS-REP Roasting | 75% | 31-Active-Directory-Identidade | Teoria parcial |
| **T1003** | OS Credential Dumping | 75% | 38-DFIR-Resposta-Incidentes | Perspectiva forense |

### Lateral Movement (TA0008) - 4 técnicas

| ID | Técnica | Score | Módulo | Recursos |
|----|---------|-------|--------|----------|
| **T1021.001** | Remote Desktop Protocol | 100% | 37-Pos-Exploracao-Movimento-Lateral | windows_lateral_movement_teoria.md |
| **T1021.002** | SMB/Windows Admin Shares | 100% | 37-Pos-Exploracao-Movimento-Lateral | SMB exploitation |
| **T1021.006** | Windows Remote Management | 100% | 37-Pos-Exploracao-Movimento-Lateral | WinRM usage |
| **T1550** | Use Alternate Authentication Material | 100% | 37-Pos-Exploracao-Movimento-Lateral | Pass-the-Hash, PtT |

### Privilege Escalation (TA0004)

| ID | Técnica | Score | Módulo | Recursos |
|----|---------|-------|--------|----------|
| **T1068** | Exploitation for Privilege Escalation | 100% | 36-Escalacao-Privilegios | linux + windows_privesc |
| **T1548** | Abuse Elevation Control Mechanism | 100% | 36-Escalacao-Privilegios | SUDO/UAC |
| **T1134** | Access Token Manipulation | 75% | 36-Escalacao-Privilegios | windows_privesc_teoria.md |
| **T1611** | Escape to Host | 75% | 33-Containers-Supply-Chain | docker-escape-techniques.md |
| **T1078** | Valid Accounts | 50% | 37-Pos-Exploracao-Movimento-Lateral | Uso de credenciais |

### Execution (TA0002) - 2 técnicas

| ID | Técnica | Score | Módulo | Recursos |
|----|---------|-------|--------|----------|
| **T1059.001** | PowerShell | 100% | 36-Escalacao-Privilegios | powershell_cheatsheet.md |
| **T1059.004** | Unix Shell | 100% | 36-Escalacao-Privilegios | Bash scripting |

### Collection (TA0009) - 1 técnica

| ID | Técnica | Score | Módulo | Recursos |
|----|---------|-------|--------|----------|
| **T1119** | Automated Collection | 50% | 28-Engenharia-Ferramentas-Seguranca | organize_logs.ps1 |

### Stealth e Defense Impairment - teoria (35-Acesso-Inicial-C2)

| ID | Técnica | Score | Status |
|----|---------|-------|--------|
| **T1070** | Indicator Removal (Stealth) | 50% | Teoria DFIR |
| **T1685** | Disable or Modify Tools (Defense Impairment) | 75% | 35-Acesso-Inicial-C2 |
| **T1027** | Obfuscated Files or Information (Stealth) | 50% | 35 (teoria) |
| **T1055** | Process Injection (Stealth) | 50% | 35 (teoria) |

### Initial Access / Exfiltration (novos na v2.1)

| ID | Técnica | Score | Módulo |
|----|---------|-------|--------|
| **T1566** | Phishing | 75% | 35-Acesso-Inicial-C2 |
| **T1190** | Exploit Public-Facing Application | 100% | 30-Web-API-AppSec |
| **T1133** | External Remote Services | 75% | 35-Acesso-Inicial-C2 |
| **T1041** | Exfiltration Over C2 Channel | 75% | acervo legado em 37-Pos-Exploracao-Movimento-Lateral |
| **T1090** | Proxy | 75% | 37 (tunnels) |

---

## 🎓 Como Usar para Aprendizado

### 1. Identificar Técnicas de Interesse

**Exemplo:** Você quer aprender sobre Active Directory

1. No Navigator, filtre por tática: **"Credential Access"**
2. Procure técnicas verdes (maior profundidade editorial declarada)
3. Identifique: **T1558.003 - Kerberoasting**
4. Veja no layer: Módulo 31-Active-Directory-Identidade

### 2. Estudar a Técnica

**No Repositório:**
```bash
cd 31-Active-Directory-Identidade/active-directory-identidade-hibrida
cat kerberoasting_teoria.md
```

**Na Matriz ATT&CK:**
```
https://attack.mitre.org/techniques/T1558/003/
```

**Estudar:**
- Como a técnica funciona
- Procedimentos de APTs reais
- Métodos de detecção (blue team)
- Mitigações recomendadas

### 3. Praticar em Lab

Use as instruções de `LAB-SETUP.md`:
```bash
# Montar AD vulnerável
# Executar Kerberoasting
# Analisar logs de detecção
```

### 4. Documentar seu Progresso

No seu caderno de estudos:
```markdown
## T1558.003 - Kerberoasting

**Data:** 2025-11-22
**Status:** ✅ Estudado e praticado

**O que aprendi:**
- Como funciona o Kerberos
- Como extrair TGS tickets
- Como quebrar hashes offline
- Como detectar (Event ID 4769)

**Lab realizado:**
- GOAD - Kerberoasting no DC01
- Capturei 5 SPNs
- Quebrei hash de svc_sql

**Próximos passos:**
- [ ] Estudar AS-REP Roasting (T1558.004)
- [ ] Estudar Golden Ticket (T1558.001)
```

---

## 🔍 Como Identificar Gaps

### Ver Técnicas Não Cobertas

1. No Navigator, procure áreas **brancas** (sem cor)
2. Essas são técnicas não cobertas pelo repositório
3. Anote para estudar em outras fontes

**Exemplo de Gap:**
- **T1059.003** - Windows Command Shell
- **T1053** - Scheduled Task/Job
- **T1047** - Windows Management Instrumentation

### Priorizar Estudos

Use o Roadmap para decidir:
- **TIER 1-2:** Foque em técnicas com score 75-100%
- **TIER 3:** Estude técnicas planejadas (score 25-50%)
- **TIER 4:** Contribua implementando técnicas não cobertas

---

## 📝 Usar em Relatórios

### Template de Achado

Ao escrever relatórios de pentesting, use IDs do ATT&CK:

```markdown
## Achado 1: Kerberoasting Bem-Sucedido

**Severidade:** Alta  
**CVSS:** 7.5  
**MITRE ATT&CK:** T1558.003 - Kerberoasting

**Descrição:**
Durante a fase de post-exploitation, foi possível extrair tickets 
Kerberos (TGS) de contas de serviço e quebrar o hash offline.

**Impacto:**
Comprometimento de credenciais de contas de serviço privilegiadas.

**Evidências:**
- Account: svc_sql@DOMAIN.LOCAL
- Hash: $krb5tgs$23$*svc_sql...
- Quebrado em: 2 horas (hashcat)
- Senha: Winter2023!

**Recomendações:**
1. Implementar senhas longas (25+ caracteres) para SPNs
2. Habilitar monitoramento de Event ID 4769
3. Usar Managed Service Accounts (MSA)
4. Implementar Credential Guard

**Referências:**
- https://attack.mitre.org/techniques/T1558/003/
- https://github.com/Samuel-Ziger/RedTeam-Essentials/blob/main/31-Active-Directory-Identidade/active-directory-identidade-hibrida/kerberoasting_teoria.md
```

---

## 🏆 Gamificação do Aprendizado

### Criar sua "Badge Collection"

Marque técnicas conforme você aprende:

```markdown
# Minhas Badges ATT&CK

## Reconnaissance ⭐⭐⭐⭐⭐⭐ (6/6)
- ✅ T1590 - Gather Victim Network Information
- ✅ T1592 - Gather Victim Host Information
- ✅ T1596 - Search Open Technical Databases
- ✅ T1593 - Search Open Websites/Domains
- ✅ T1594 - Search Victim-Owned Websites
- ✅ T1598 - Phishing for Information

## Credential Access ⭐⭐⭐ (3/10)
- ✅ T1558.003 - Kerberoasting
- ⏳ T1558.004 - AS-REP Roasting (em progresso)
- ❌ T1003 - OS Credential Dumping (não iniciado)
- ❌ T1110 - Brute Force
- ❌ T1555 - Credentials from Password Stores
- ...

## Meu Progresso Geral: 45/186 (24%)
```

### Definir Metas

**Meta 1:** Dominar Reconnaissance (TA0043)  
**Prazo:** 2 semanas  
**Progresso:** 6/6 ✅

**Meta 2:** Dominar Credential Access (TA0006)  
**Prazo:** 1 mês  
**Progresso:** 3/10 ⏳

---

## 🔗 Correlacionar com APTs

### Ver APTs que Usam a Técnica

No site do MITRE ATT&CK:

1. Acesse a técnica (ex: T1558.003)
2. Role até **"Procedure Examples"**
3. Veja quais grupos APT usam essa técnica

**Exemplo - Kerberoasting:**
- **APT29 (Cozy Bear)** - usado em campanhas russas
- **APT32 (OceanLotus)** - usado em ataques no sudeste asiático
- **FIN7** - usado em ataques financeiros

### Emular APTs

Use o mapeamento para criar cenários:

```markdown
## Cenário de Red Team: Emulação APT29

**Objetivo:** Simular campanha APT29 em AD corporativo

**Técnicas (ATT&CK):**
1. T1598 - Phishing for Information
2. T1078 - Valid Accounts
3. T1558.003 - Kerberoasting
4. T1021.002 - SMB/Admin Shares
5. T1003 - Credential Dumping

**Execução:**
- Dia 1: Phishing educacional (autorizado)
- Dia 2: Usar credenciais obtidas
- Dia 3: Kerberoasting no AD
- Dia 4: Movimento lateral via SMB
- Dia 5: Dump de credenciais do DC

**Detecção Esperada:**
- EDR deve alertar em Dia 3 (Kerberoasting)
- SIEM deve correlacionar em Dia 4 (lateral movement)
```

---

## 📚 Integração com Certificações

### OSCP (Offensive Security Certified Professional)

**Técnicas Relevantes:**
- T1590, T1592 (Reconnaissance)
- T1548 (Privilege Escalation)
- T1059.001, T1059.004 (Execution)
- T1083 (Discovery)

**Como usar:**
1. Estude as técnicas cobertas aqui
2. Pratique em labs (HTB, PWK)
3. Use IDs em seus relatórios de lab

### CRTP (Certified Red Team Professional)

**Técnicas Relevantes:**
- T1087, T1069, T1482 (AD Discovery)
- T1558.003, T1558.004 (Kerberos Attacks)
- T1021.002, T1021.006 (Lateral Movement)
- T1550 (Pass-the-Hash/Ticket)

**Como usar:**
1. Foque no módulo 31-Active-Directory-Identidade
2. Use bloodhound_teoria.md
3. Pratique em GOAD lab

---

## 🛠️ Ferramentas Complementares

### ATT&CK Navigator
- **Web:** https://mitre-attack.github.io/attack-navigator/
- **GitHub:** https://github.com/mitre-attack/attack-navigator

### Atomic Red Team
- **GitHub:** https://github.com/redcanaryco/atomic-red-team
- **Integração:** Mapeia testes atômicos para ATT&CK
- **Uso:** Testar detecções para técnicas específicas

### MITRE CALDERA
- **GitHub:** https://github.com/mitre/caldera
- **Uso:** Plataforma de adversary emulation
- **Integração:** Plugins com ATT&CK

### VECTR
- **Site:** https://vectr.io/
- **Uso:** Tracking de Purple Team exercises
- **Integração:** Mapeia atividades para ATT&CK

---

## 💡 Dicas Avançadas

### 1. Criar Layers Customizados

Você pode editar o JSON para adicionar suas próprias notas:

```json
{
  "techniqueID": "T1558.003",
  "comment": "✅ Praticado em 22/11/2025 no GOAD lab. Quebrei 3 hashes!",
  "score": 100,
  "metadata": [
    {
      "name": "Data Praticado",
      "value": "2025-11-22"
    },
    {
      "name": "Lab",
      "value": "GOAD - DC01"
    }
  ]
}
```

### 2. Comparar com Outros Projetos

Crie layers de outros projetos e compare:
- Layer do RedTeam-Essentials
- Layer do Atomic Red Team
- Layer de um engagement real (anonimizado)

### 3. Visualizar Progressão

Salve snapshots mensais:
- `MITRE-ATTACK-MAPPING_2025-11.json`
- `MITRE-ATTACK-MAPPING_2025-12.json`
- Compare seu progresso!

---

## ❓ FAQ

### P: Posso usar este mapping em trabalho comercial?
**R:** Sim! Licença MIT permite uso comercial. Atribua créditos ao projeto.

### P: Como contribuir com novas técnicas?
**R:** 
1. Leia [CONTRIBUTING.md](CONTRIBUTING.md)
2. Implemente a técnica em um módulo
3. Atualize o JSON com a nova técnica
4. Submeta PR

### P: O mapping cobre todas as técnicas do ATT&CK?
**R:** Não. ATT&CK tem 186+ técnicas Enterprise. Cobrimos 28+ (15%). Veja ROADMAP.md para expansão futura.

### P: Posso usar para Blue Team?
**R:** Sim! As técnicas mapeadas mostram o que Red Team pode fazer. Use para:
- Implementar detecções
- Testar EDR/SIEM
- Validar controles

---

## 📞 Suporte

**Dúvidas sobre o mapping?**
- Abra uma [Issue](https://github.com/Samuel-Ziger/RedTeam-Essentials/issues)
- Consulte [MITRE ATT&CK Docs](https://attack.mitre.org/resources/getting-started/)

**Quer contribuir?**
- Leia [CONTRIBUTING.md](CONTRIBUTING.md)
- Veja issues com tag `help-wanted`

---

<div align="center">

**🎯 Use o Mapeamento ATT&CK para Estruturar seu Aprendizado!**

*"Se você não pode medir, você não pode melhorar."*

---

**Última Atualização:** 2025-11-22  
**Versão do Mapping:** 1.0  
**Técnicas Cobertas:** 28+

</div>
