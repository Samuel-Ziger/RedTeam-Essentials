# 🔍 Passive Recon Cheatsheet

> Guia completo de reconhecimento passivo - coletando informações sem interagir diretamente com o alvo

---

## 📚 O que é Reconhecimento Passivo?

**Reconhecimento Passivo** é a fase onde coletamos informações sobre um alvo **sem enviar pacotes diretamente** para os sistemas dele. É como observar de longe, usando fontes públicas e dados já disponíveis na internet.

### Por que é importante?
- ✅ **Discreto**: O alvo não sabe que está sendo pesquisado
- ✅ **Seguro**: Não há risco de ser detectado por IDS/IPS
- ✅ **Legal**: Usa apenas informações públicas
- ✅ **Eficiente**: Pode revelar muito sem tocar no alvo

---

## 🌐 DNS - Domain Name System

### WHOIS Lookup
Consulta informações sobre o proprietário de um domínio.

```bash
# Linux/macOS
whois exemplo.com

# Windows PowerShell
# Instale o módulo primeiro: Install-Module -Name DomainTools
Resolve-DnsName -Name exemplo.com -Type ALL
```

**O que você encontra:**
- Nome do registrante
- Email de contato
- Data de registro e expiração
- Servidores DNS autoritativos
- Informações da organização

---

### DNS Records Enumeration

#### A Records (IPv4)
```bash
# Linux
dig exemplo.com A

# Windows
nslookup exemplo.com
```

#### AAAA Records (IPv6)
```bash
dig exemplo.com AAAA
nslookup -type=AAAA exemplo.com
```

#### MX Records (Mail Servers)
```bash
dig exemplo.com MX
nslookup -type=MX exemplo.com
```
**Útil para:** Identificar servidores de email, possíveis alvos para phishing educacional

#### TXT Records (SPF, DMARC, DKIM)
```bash
dig exemplo.com TXT
nslookup -type=TXT exemplo.com
```
**Útil para:** Verificar configurações de segurança de email

#### NS Records (Name Servers)
```bash
dig exemplo.com NS
nslookup -type=NS exemplo.com
```

#### SOA Records (Start of Authority)
```bash
dig exemplo.com SOA
```

---

### Subdomain Enumeration (Passivo)

#### Usando Certificate Transparency Logs
Sites como `crt.sh` mostram certificados SSL públicos:

```
Acesse: https://crt.sh/?q=%25.exemplo.com
```

Isso revela subdomínios como:
- `mail.exemplo.com`
- `vpn.exemplo.com`
- `admin.exemplo.com`
- `dev.exemplo.com`

#### Google Dorking para Subdomínios
```
site:exemplo.com -www
```

#### Usando APIs Públicas
- **VirusTotal**: `https://www.virustotal.com/gui/domain/exemplo.com/relations`
- **SecurityTrails**: API para histórico de DNS
- **DNSDumpster**: `https://dnsdumpster.com/`

---

## 🌍 IP Address Intelligence

### Geolocalização
```bash
# Usando serviços web
curl https://ipapi.co/8.8.8.8/json/

# Resultado esperado:
# - País
# - Cidade
# - ISP
# - Organização
# - Fuso horário
```

### ASN Lookup (Autonomous System Number)
```bash
whois -h whois.cymru.com " -v 8.8.8.8"
```
**Útil para:** Descobrir blocos de IP da organização

### Reverse DNS
```bash
# Linux
dig -x 8.8.8.8

# Windows
nslookup 8.8.8.8
```

---

## 📧 Email Harvesting (Coleta de Emails)

### Google Dorking
```
"@exemplo.com" site:linkedin.com
"@exemplo.com" filetype:pdf
```

### theHarvester (Ferramenta)
```bash
# Coleta emails, subdomínios, hosts de várias fontes
theHarvester -d exemplo.com -b google,bing,linkedin
```

### Hunter.io
- Site: `https://hunter.io/`
- Encontra padrões de email da empresa
- Exemplo: `nome.sobrenome@empresa.com`

---

## 🔐 SSL/TLS Certificate Analysis

### Online Tools
- **Censys.io**: Pesquisa de certificados e dispositivos
- **Shodan.io**: Motor de busca para dispositivos conectados
- **SSL Labs**: Análise de configuração SSL

### Comandos Manuais
```bash
# Verificar certificado SSL
openssl s_client -connect exemplo.com:443 -showcerts

# Extrair informações do certificado
echo | openssl s_client -connect exemplo.com:443 2>/dev/null | openssl x509 -noout -text
```

**O que analisar:**
- Subject Alternative Names (SANs) - revela outros domínios
- Organização emissora
- Data de validade
- Algoritmos de criptografia

---

## 🗺️ Web Archive & Historical Data

### Wayback Machine
```
https://web.archive.org/web/*/exemplo.com
```

**Útil para:**
- Ver versões antigas do site
- Encontrar páginas removidas
- Descobrir tecnologias antigas
- Identificar mudanças na infraestrutura

### GitHub Search
```
# Buscar por organização
org:nome-empresa senha
org:nome-empresa API key
org:nome-empresa password

# Buscar em código
"exemplo.com" password
"exemplo.com" api_key
```

⚠️ **ATENÇÃO**: Use isso apenas para fins educacionais e éticos!

---

## 🏢 OSINT de Organização

### LinkedIn
- Buscar funcionários da empresa
- Identificar estrutura organizacional
- Encontrar tecnologias mencionadas
- Descobrir parceiros e fornecedores

### Glassdoor / Indeed
- Vagas de emprego revelam tecnologias usadas
- Exemplo: "Conhecimento em AWS, Active Directory, VMware"

### Crunchbase
- Informações sobre investimentos
- Parceiros comerciais
- Aquisições e fusões

---

## 🛠️ Ferramentas Passivas Recomendadas

### DNS & Subdomínios
| Ferramenta | Descrição | Tipo |
|------------|-----------|------|
| **DNSDumpster** | Mapa visual de DNS | Web |
| **crt.sh** | Certificate Transparency | Web |
| **Sublist3r** | Enumeração de subdomínios | CLI |
| **Amass** | Mapping de ataque surface | CLI |

### OSINT Geral
| Ferramenta | Descrição | Tipo |
|------------|-----------|------|
| **theHarvester** | Coleta de emails e subdomínios | CLI |
| **Maltego** | Correlação de dados OSINT | GUI |
| **Recon-ng** | Framework de reconhecimento | CLI |
| **SpiderFoot** | Automação OSINT | GUI/CLI |

### Análise de Infraestrutura
| Ferramenta | Descrição | Tipo |
|------------|-----------|------|
| **Shodan** | Motor de busca de dispositivos | Web |
| **Censys** | Análise de certificados e hosts | Web |
| **BuiltWith** | Tecnologias usadas no site | Web |
| **Wappalyzer** | Identificação de tecnologias | Browser Extension |

---

## 📊 Metodologia de Recon Passivo

```
┌─────────────────────────────────────────────────────────┐
│                   FASE 1: DNS                           │
│  ├─ WHOIS                                               │
│  ├─ DNS Records (A, MX, TXT, NS)                        │
│  └─ Subdomínios (crt.sh, DNS Brute)                     │
└─────────────────────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   FASE 2: IP & ASN                      │
│  ├─ Geolocalização                                      │
│  ├─ ASN Lookup                                          │
│  └─ Blocos de IP da organização                         │
└─────────────────────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   FASE 3: Web & Tech                    │
│  ├─ Wayback Machine                                     │
│  ├─ Tecnologias (BuiltWith, Wappalyzer)                 │
│  └─ SSL/TLS Certificates                                │
└─────────────────────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   FASE 4: People & Org                  │
│  ├─ Email Harvesting                                    │
│  ├─ LinkedIn Recon                                      │
│  └─ Job Postings                                        │
└─────────────────────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│              FASE 5: Documentação & Análise             │
│  ├─ Organizar dados coletados                           │
│  ├─ Identificar pontos de interesse                     │
│  └─ Preparar para fase ativa (se autorizado)            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Checklist de Recon Passivo

### Informações de Domínio
- [ ] WHOIS do domínio principal
- [ ] Registros DNS (A, AAAA, MX, TXT, NS, SOA)
- [ ] Enumeração de subdomínios
- [ ] Histórico de DNS (SecurityTrails)

### Informações de IP
- [ ] Ranges de IP da organização
- [ ] ASN lookup
- [ ] Geolocalização
- [ ] Reverse DNS

### Análise Web
- [ ] Tecnologias utilizadas
- [ ] Certificados SSL/TLS
- [ ] Wayback Machine
- [ ] Robots.txt e sitemap.xml

### OSINT Humano
- [ ] Funcionários no LinkedIn
- [ ] Vagas de emprego
- [ ] Emails públicos
- [ ] Estrutura organizacional

### Segurança
- [ ] Vazamentos de dados (HaveIBeenPwned)
- [ ] GitHub/GitLab leaks
- [ ] Pastebin dumps
- [ ] Configurações de SPF/DMARC

---

## 💡 Dicas de Ouro

### 1. Sempre Documente
Mantenha notas organizadas de tudo que encontrar. Use ferramentas como:
- **CherryTree** (notas hierárquicas)
- **Obsidian** (notas em markdown)
- **Notion** (colaborativo)

### 2. Use Múltiplas Fontes
Não confie em uma única ferramenta. Cross-reference seus dados:
```
crt.sh → confirmar com DNSDumpster → validar com Amass
```

### 3. Automatize com Cautela
Scripts podem acelerar o processo, mas:
- Respeite rate limits de APIs
- Não faça requisições excessivas
- Use delays entre requests

### 4. Pense como Atacante
Perguntas a fazer:
- Quais tecnologias têm vulnerabilidades conhecidas?
- Há informações sensíveis expostas?
- Funcionários compartilham demais nas redes sociais?
- Há configurações de segurança fracas?

---

## ⚠️ Considerações Legais e Éticas

### ✅ É Legal:
- Consultar WHOIS público
- Usar Google e motores de busca
- Acessar informações públicas
- Pesquisar em redes sociais públicas

### ❌ NÃO É Legal (sem autorização):
- Acessar sistemas sem permissão
- Explorar vulnerabilidades
- Usar dados para fins maliciosos
- Violar termos de serviço

### Regra de Ouro
> **Se você não tem autorização por escrito, não faça!**

---

## 📚 Recursos Adicionais

### Livros
- "Open Source Intelligence Techniques" - Michael Bazzell
- "OSINT Techniques" - nihilism

### Cursos
- TCM Security - Practical Ethical Hacking
- TryHackMe - OSINT Room
- HackTheBox - Recon Machines

### Blogs
- [OSINT Curious](https://osintcurio.us/)
- [Bellingcat](https://www.bellingcat.com/)
- [IntelTechniques](https://inteltechniques.com/)

---

## 🎓 Exercícios Práticos

### Nível Iniciante
1. Faça WHOIS lookup de 5 domínios diferentes
2. Enumere subdomínios usando crt.sh
3. Identifique tecnologias de 3 sites

### Nível Intermediário
1. Crie um mapa visual de infraestrutura de um domínio
2. Encontre 10 emails de uma organização
3. Documente o histórico de mudanças de um site

### Nível Avançado
1. Automatize coleta de dados de múltiplas fontes
2. Correlacione dados de DNS, SSL e OSINT
3. Crie relatório completo de superfície de ataque

---

<div align="center">

**🔍 Reconhecimento é a base de todo pentest bem-sucedido**

*Quanto melhor o recon, mais fácil a exploração*

---

*Desenvolvido para fins educacionais | Use com responsabilidade*

</div>
