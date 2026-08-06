# 🔍 Módulo 01: Reconhecimento (Reconnaissance)

> **Fundamentos de coleta de informações sobre alvos**

---

## 📚 Sobre Este Módulo

O **reconhecimento** (recon) é a primeira fase de qualquer operação Red Team ou penetration test. Nesta etapa, você coleta o máximo de informações possíveis sobre o alvo **sem interagir diretamente** com seus sistemas.

### 🎯 Objetivos de Aprendizado

Ao completar este módulo, você será capaz de:
- [ ] Diferenciar reconhecimento passivo de ativo
- [ ] Realizar enumeração DNS completa
- [ ] Identificar subdomínios e infraestrutura
- [ ] Coletar informações de forma ética e legal
- [ ] Documentar achados de reconhecimento
- [ ] Usar ferramentas automatizadas de recon

---

## 📋 Pré-requisitos

### Conhecimentos Necessários
- ✅ Fundamentos de redes (TCP/IP, DNS, HTTP)
- ✅ Conhecimento básico de PowerShell ou Bash
- ✅ Compreensão de protocolos de internet

### Ferramentas Requeridas
- PowerShell 5.1+ (Windows) ou Bash (Linux)
- Acesso à internet
- Opcional: Kali Linux com ferramentas nativas

---

## 📁 Conteúdo do Módulo

### 1. Teoria e Conceitos

#### [`passive_recon_cheatsheet.md`](passive_recon_cheatsheet.md)
**Descrição:** Guia completo sobre reconhecimento passivo  
**Tópicos:**
- Diferença entre recon passivo e ativo
- Fontes de informação pública
- Técnicas de OSINT
- Ferramentas recomendadas
- Boas práticas

**Tempo estimado:** 2-3 horas de leitura

---

#### [`web_recon_notes.md`](web_recon_notes.md)
**Descrição:** Reconhecimento focado em aplicações web  
**Tópicos:**
- Enumeração de tecnologias web
- Identificação de frameworks
- Análise de cabeçalhos HTTP
- Mapeamento de estrutura de sites

**Tempo estimado:** 1-2 horas de leitura

---

### 2. Scripts e Automação (v2)

#### [`dns_enum.ps1`](dns_enum.ps1)
**Descrição:** Enumeração DNS cross-platform (PS 5.1 / 7+) com crt.sh e export JSON.  
**Parâmetros principais:** `-Domain`, `-IncludeSubdomains`, `-OutputDir`, `-Format json|txt`, `-DnsServer`, `-DryRun`, `-RecordTypes`.

```powershell
Import-Module ../lib/powershell/RTECommon.psm1
.\dns_enum.ps1 -Domain "exemplo.com" -IncludeSubdomains -Format json
.\dns_enum.ps1 -Domain "exemplo.com" -RecordTypes A,MX,TXT -DnsServer 1.1.1.1 -DryRun
```

#### [`dns_enum.sh`](dns_enum.sh)
**Descrição:** Alternativa Bash (`dig` + crt.sh + WHOIS opcional).

```bash
./dns_enum.sh -d exemplo.com --subs --whois -o ./output
./dns_enum.sh -d exemplo.com --dry-run
```

**MITRE ATT&CK:** T1590 / T1596

**Relacionado:** recon web avançado em [`07-Web-AppSec/recon-web-pratico.md`](../07-Web-AppSec/recon-web-pratico.md).

---

## 🧪 Exercícios Práticos

### Exercício 1: Reconhecimento DNS Básico
**Objetivo:** Enumerar DNS de um domínio público

**Passos:**
1. Escolha um domínio público (ex: `example.com`)
2. Execute o script `dns_enum.ps1`
3. Analise os resultados
4. Documente os achados

**Validação:**
- ✅ Identificou servidores DNS autoritativos?
- ✅ Encontrou registros MX (email)?
- ✅ Identificou registros SPF/DMARC?

---

### Exercício 2: Mapeamento de Infraestrutura
**Objetivo:** Criar mapa visual de infraestrutura de domínio

**Passos:**
1. Execute reconhecimento DNS completo
2. Identifique todos os IPs associados
3. Use WHOIS para informações de registro
4. Crie diagrama de infraestrutura

**Ferramentas:**
- `dns_enum.ps1` (incluído)
- WHOIS online
- Draw.io para diagrama

---

### Exercício 3: Comparação de Técnicas
**Objetivo:** Comparar reconhecimento passivo vs ativo

**Passos:**
1. **Passivo:** Use apenas DNS e WHOIS
2. **Ativo:** Use `nmap` para scan
3. Compare informações obtidas
4. Documente diferenças

**Questões para responder:**
- Qual método revelou mais informações?
- Qual é mais sigiloso?
- Qual é mais rápido?

---

## 🛡️ Considerações de Segurança

### ⚠️ Limites Éticos

**PERMITIDO (Reconhecimento Passivo):**
- ✅ Consultas DNS públicas
- ✅ Pesquisa WHOIS
- ✅ Busca em motores de pesquisa
- ✅ Certificate Transparency logs
- ✅ Informações em redes sociais públicas

**REQUER AUTORIZAÇÃO (Reconhecimento Ativo):**
- ❌ Port scanning (nmap, masscan)
- ❌ Enumeração de diretórios web
- ❌ Tentativas de conexão direta
- ❌ Fingerprinting de serviços
- ❌ Exploração de vulnerabilidades

### 🔒 Melhores Práticas

1. **Sempre documente:** Mantenha registro de todas as consultas
2. **Use VPN/Tor quando apropriado:** Privacidade é importante
3. **Respeite rate limits:** Não sobrecarregue servidores
4. **Obtenha autorização:** Mesmo para recon passivo em contextos corporativos

---

## 📚 Recursos Adicionais

### Ferramentas Recomendadas

#### DNS Enumeration
- **dnsrecon** (Python): https://github.com/darkoperator/dnsrecon
- **DNSdumpster** (Web): https://dnsdumpster.com/
- **Sublist3r** (Python): https://github.com/aboul3la/Sublist3r

#### WHOIS
- **whois** (Linux): `apt install whois`
- **who.is** (Web): https://who.is/

#### Certificate Transparency
- **crt.sh** (Web): https://crt.sh/
- **Censys** (Web): https://censys.io/

#### Search Engines
- **Google Dorking:** `site:exemplo.com filetype:pdf`
- **Shodan:** https://www.shodan.io/
- **Censys:** https://search.censys.io/

---

### Leituras Recomendadas

📖 **Livros:**
- "The Web Application Hacker's Handbook" - Capítulo sobre Reconnaissance
- "Red Team Field Manual (RTFM)" - Seção de Recon

📺 **Vídeos:**
- IppSec (YouTube): Análise de máquinas HTB com foco em recon
- STÖK (YouTube): Bug bounty reconnaissance

🔗 **Artigos:**
- OWASP Testing Guide: Information Gathering
- PTES: Intelligence Gathering

---

## 🎯 MITRE ATT&CK Mapping

Este módulo cobre as seguintes táticas e técnicas:

### TA0043 - Reconnaissance
- **T1590:** Gather Victim Network Information
  - T1590.001 - Domain Properties
  - T1590.002 - DNS
  - T1590.005 - IP Addresses

- **T1592:** Gather Victim Host Information
  - T1592.002 - Software

- **T1593:** Search Open Websites/Domains
  - T1593.001 - Social Media
  - T1593.002 - Search Engines

- **T1596:** Search Open Technical Databases
  - T1596.001 - DNS/Passive DNS
  - T1596.003 - Digital Certificates

---

## ✅ Checklist de Progresso

### Teoria
- [ ] Li `passive_recon_cheatsheet.md` completamente
- [ ] Entendi diferença entre recon passivo e ativo
- [ ] Li `web_recon_notes.md`
- [ ] Compreendi fontes de informação pública

### Prática
- [ ] Executei `dns_enum.ps1` com sucesso
- [ ] Fiz reconhecimento de 3+ domínios diferentes
- [ ] Documentei achados de forma organizada
- [ ] Criei diagrama de infraestrutura

### Ferramentas
- [ ] Instalei e testei dnsrecon
- [ ] Usei crt.sh para encontrar subdomínios
- [ ] Realizei consultas WHOIS
- [ ] Pratiquei Google Dorking

---

## 📝 Anotações e Dicas

### Dica 1: Automatize Tudo
> "Se você faz algo mais de 2 vezes, automatize."

Crie scripts para:
- Coletar dados de múltiplas fontes
- Consolidar resultados
- Gerar relatórios automáticos

### Dica 2: Organize Seus Dados
Estrutura recomendada:
```
Recon/
├── Target_Name/
│   ├── DNS/
│   │   ├── dns_records.txt
│   │   └── subdomains.txt
│   ├── WHOIS/
│   │   └── whois_info.txt
│   ├── Web/
│   │   ├── technologies.txt
│   │   └── screenshots/
│   └── Notes/
│       └── findings.md
```

### Dica 3: Correlacione Informações
Não apenas colete dados, **correlacione**:
- IPs → ASN → Organização
- Emails → Funcionários → LinkedIn
- Subdomínios → Tecnologias → Vulnerabilidades

---

## 🔄 Próximos Passos

### Depois de completar este módulo:

1. **Prosseguir para:** [Módulo 02 - OSINT](../02-OSINT/README.md)
2. **Aprofundar:** Estudar OSINT para complementar recon
3. **Praticar:** TryHackMe room "Passive Reconnaissance"
4. **Certificações:** eJPT (basic recon)

---

## 📞 Suporte e Dúvidas

### Recursos de Ajuda
- 💬 **Discord:** Comunidades de InfoSec
- 🐦 **Twitter:** @_JohnHammond, @IppSec
- 📺 **YouTube:** Busque por "DNS enumeration tutorial"

### Contribuições
Encontrou um erro ou quer melhorar este módulo?
- Abra uma issue no GitHub
- Envie um Pull Request
- Consulte [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 📊 Status do Módulo

```
[████████████████████] 100% Completo

✅ Teoria documentada
✅ Scripts funcionais
✅ Exercícios criados
✅ Mapeamento MITRE ATT&CK
✅ Recursos adicionais listados
```

---

<div align="center">

**🎯 Lembre-se: Reconnaissance é a base de um ataque bem-sucedido**

*"Give me six hours to chop down a tree and I will spend the first four sharpening the axe." - Abraham Lincoln*

---

**Próximo:** [02-OSINT →](../02-OSINT/README.md)

</div>
