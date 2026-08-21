# 🕵️ OSINT Tools - Lista Completa

> Ferramentas de Open Source Intelligence para coleta ética de informações públicas

---

## 📚 O que é OSINT?

**OSINT (Open Source Intelligence)** é a prática de coletar informações de **fontes publicamente disponíveis**. Diferente de hacking, OSINT usa apenas dados que já estão acessíveis legalmente na internet.

### Por que OSINT é importante?
- ✅ 100% Legal (quando feito corretamente)
- ✅ Não requer interação com o alvo
- ✅ Pode revelar informações sensíveis expostas
- ✅ Essencial para Red Team e Pentest
- ✅ Usado por jornalistas, investigadores e empresas

---

## 🌐 OSINT de Domínios e Infraestrutura

### DNS e Subdomínios

| Ferramenta | Descrição | Link | Tipo |
|------------|-----------|------|------|
| **crt.sh** | Certificate Transparency Logs | https://crt.sh | Web |
| **DNSDumpster** | Mapeamento visual de DNS | https://dnsdumpster.com | Web |
| **Sublist3r** | Enumeração de subdomínios | GitHub | CLI |
| **Amass** | OSINT e mapping de superfície | GitHub | CLI |
| **Subfinder** | Rápido e eficiente | GitHub | CLI |
| **Assetfinder** | Descoberta de assets | GitHub | CLI |

#### Comandos Práticos
```bash
# Sublist3r
sublist3r -d exemplo.com -o subdomains.txt

# Amass
amass enum -d exemplo.com -o amass_results.txt

# Subfinder
subfinder -d exemplo.com -o subfinder_output.txt
```

---

### Busca de IP e ASN

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **Shodan** | Motor de busca para dispositivos IoT | https://shodan.io |
| **Censys** | Pesquisa de certificados e hosts | https://censys.io |
| **FOFA** | Cyberspace mapping | https://fofa.info |
| **ZoomEye** | Cyberspace search engine | https://zoomeye.org |
| **GreyNoise** | Analisa tráfego de internet | https://greynoise.io |

#### Exemplos de Queries Shodan
```
org:"Nome da Empresa"
ssl:"exemplo.com"
product:"Apache httpd"
port:3389 country:"BR"
```

---

### WHOIS e Histórico DNS

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **WHOIS Lookup** | Informações de registro de domínio | Linha de comando |
| **SecurityTrails** | Histórico DNS e WHOIS | https://securitytrails.com |
| **ViewDNS.info** | Suite de ferramentas DNS | https://viewdns.info |
| **DomainTools** | Pesquisa avançada de domínios | https://domaintools.com |

---

## 📧 OSINT de Email e Pessoas

### Email Harvesting

| Ferramenta | Descrição | Tipo | Link |
|------------|-----------|------|------|
| **Hunter.io** | Encontra emails profissionais | Web | https://hunter.io |
| **theHarvester** | Coleta emails, hosts, pessoas | CLI | GitHub |
| **Phonebook.cz** | Busca de emails, URLs, domínios | Web | https://phonebook.cz |
| **Clearbit Connect** | Extensão para encontrar emails | Browser | Chrome/Firefox |

#### theHarvester - Uso Prático
```bash
# Buscar em múltiplas fontes
theHarvester -d exemplo.com -b google,bing,linkedin,twitter

# Salvar resultados
theHarvester -d exemplo.com -b all -f output.html

# Fontes disponíveis:
# google, bing, yahoo, linkedin, twitter, 
# hunter, baidu, virustotal, etc.
```

---

### Verificação de Vazamentos

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **HaveIBeenPwned** | Verifica se email foi vazado | https://haveibeenpwned.com |
| **DeHashed** | Database de credenciais vazadas | https://dehashed.com |
| **LeakCheck** | Busca em vazamentos | https://leakcheck.io |
| **IntelX** | Motor de busca de vazamentos | https://intelx.io |

⚠️ **ATENÇÃO**: Use apenas para verificar suas próprias credenciais ou com autorização!

---

### Análise de Pessoas

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **Pipl** | Busca de informações sobre pessoas | https://pipl.com |
| **TruePeopleSearch** | Busca de registros públicos (EUA) | https://truepeoplesearch.com |
| **Spokeo** | Agregador de dados públicos | https://spokeo.com |
| **LinkedIn** | Rede profissional | https://linkedin.com |

---

## 🔍 OSINT em Redes Sociais

### Ferramentas Multi-Plataforma

| Ferramenta | Descrição | Tipo |
|------------|-----------|------|
| **Sherlock** | Encontra username em 300+ sites | CLI (Python) |
| **WhatsMyName** | Enumeração de usernames | Web/CLI |
| **Social-Analyzer** | Análise de perfis sociais | CLI |
| **Twint** | Twitter OSINT sem API | CLI (Python) |

#### Sherlock - Busca de Username
```bash
# Instalar
pip install sherlock-project

# Buscar username em todas as plataformas
sherlock usuario123

# Salvar resultados
sherlock usuario123 -o usuario_results.txt
```

---

### Plataformas Específicas

#### Twitter/X
| Ferramenta | Descrição |
|------------|-----------|
| **TweetDeck** | Dashboard nativo do Twitter |
| **Twint** | Scraping sem usar API oficial |
| **Social Bearing** | Análise de tweets e tendências |

#### LinkedIn
| Ferramenta | Descrição |
|------------|-----------|
| **LinkedIn Search** | Busca avançada nativa |
| **theHarvester** | Coleta de emails do LinkedIn |
| **CrossLinked** | Enumeração de funcionários |

#### Instagram
| Ferramenta | Descrição |
|------------|-----------|
| **Osintgram** | OSINT framework para Instagram |
| **InstaDP** | Download de fotos de perfil |

---

## 🗺️ OSINT de Geolocalização

### Imagens e Localização

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **Google Earth** | Imagens de satélite | Desktop/Web |
| **Google Street View** | Fotos 360° de ruas | Web |
| **Yandex Images** | Busca reversa de imagens | https://yandex.com/images |
| **TinEye** | Busca reversa de imagens | https://tineye.com |

### Metadados de Imagens

| Ferramenta | Descrição | Tipo |
|------------|-----------|------|
| **ExifTool** | Extrai metadados EXIF | CLI |
| **[Metadata Remover Viewer](https://metadataremover.ai/metadata-viewer)** | Analisa EXIF/IPTC/XMP localmente no navegador; confirme achados importantes com outra ferramenta | Web |
| **Jeffrey's Image Metadata Viewer** | Análise online | Web |
| **Geo Imager** | Localização via EXIF | Web |

```bash
# ExifTool - extrair todos os metadados
exiftool foto.jpg

# Remover metadados
exiftool -all= foto.jpg

# Mostrar apenas GPS
exiftool -gps:all foto.jpg
```

---

## 📄 OSINT de Documentos

### Análise de Arquivos

| Ferramenta | Descrição | Tipo |
|------------|-----------|------|
| **FOCA** | Fingerprinting Organizations | Windows |
| **Metagoofil** | Extrai metadados de docs públicos | CLI (Python) |
| **ExifTool** | Metadados de múltiplos formatos | CLI |

#### Metagoofil - Coleta de Documentos
```bash
# Buscar PDFs de um domínio
metagoofil -d exemplo.com -t pdf -l 100 -o output -f results.html

# Opções:
# -d : domínio alvo
# -t : tipo de arquivo (pdf, doc, xls, ppt)
# -l : limite de resultados
# -o : pasta de output
# -f : arquivo HTML com resultados
```

---

### Google Dorking

**Google Dorks** são queries avançadas para encontrar informações específicas.

#### Operadores Úteis
```
site:        Busca em site específico
filetype:    Tipo de arquivo
intitle:     Texto no título
inurl:       Texto na URL
intext:      Texto no corpo
cache:       Versão em cache do Google
related:     Sites relacionados
```

#### Dorks Práticos
```
# Encontrar PDFs de um domínio
site:exemplo.com filetype:pdf

# Buscar documentos sensíveis
site:exemplo.com "confidencial" filetype:doc

# Encontrar arquivos de configuração expostos
filetype:env "DB_PASSWORD"

# Painéis de login expostos
intitle:"index of" "admin"

# Arquivos SQL expostos
filetype:sql "INSERT INTO" "VALUES"

# Cameras IP públicas
intitle:"webcamXP 5"

# Servidores com directory listing
intitle:"index of /" "parent directory"
```

⚠️ **ATENÇÃO**: Apenas visualize, não baixe ou use informações sensíveis!

---

## 🛠️ Frameworks OSINT Completos

### Ferramentas All-in-One

| Ferramenta | Descrição | Tipo | Curva Aprendizado |
|------------|-----------|------|-------------------|
| **Maltego** | Visualização e correlação de dados | GUI | Média |
| **Recon-ng** | Framework modular estilo Metasploit | CLI | Média |
| **SpiderFoot** | Automação OSINT completa | Web/CLI | Baixa |
| **OSINT Framework** | Coleção de ferramentas | Web | Baixa |
| **theHarvester** | Coleta multi-fonte | CLI | Baixa |

---

### Maltego

**Descrição**: Ferramenta visual para correlacionar dados OSINT.

```
Recursos:
├─ Transforms (plugins para coleta)
├─ Grafos visuais de relacionamentos
├─ Integração com APIs
├─ Community Edition (gratuita)
└─ Exportação de dados
```

**Casos de Uso:**
- Mapear relacionamentos entre pessoas
- Visualizar infraestrutura de rede
- Correlacionar emails, domínios e IPs

---

### Recon-ng

**Descrição**: Framework modular para reconhecimento web.

```bash
# Iniciar Recon-ng
recon-ng

# Criar workspace
workspaces create empresa_alvo

# Carregar módulo
marketplace install recon/domains-hosts/bing_domain_web

# Usar módulo
modules load recon/domains-hosts/bing_domain_web
options set SOURCE exemplo.com
run

# Listar hosts descobertos
show hosts
```

**Módulos Populares:**
- `recon/domains-hosts/*` - Descoberta de hosts
- `recon/hosts-hosts/*` - Enumeração de hosts
- `harvester` - Coleta de emails
- `whois_pocs` - WHOIS contacts

---

### SpiderFoot

**Descrição**: Scanner OSINT automatizado com interface web.

```bash
# Instalar
git clone https://github.com/smicallef/spiderfoot.git
cd spiderfoot
pip3 install -r requirements.txt

# Executar
python3 sf.py -l 127.0.0.1:5001

# Acessar via browser
http://127.0.0.1:5001
```

**Recursos:**
- 200+ módulos de coleta
- Interface web intuitiva
- Correlação automática
- Alertas e notificações
- API REST

---

## 🔐 OSINT de Segurança

### Análise de Vulnerabilidades

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **CVE Details** | Database de CVEs | https://cvedetails.com |
| **Exploit-DB** | Database de exploits | https://exploit-db.com |
| **Vulners** | Busca de vulnerabilidades | https://vulners.com |
| **GreyNoise** | Análise de scanners maliciosos | https://greynoise.io |

---

### Threat Intelligence

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **VirusTotal** | Análise de malware e URLs | https://virustotal.com |
| **URLScan.io** | Análise de URLs suspeitas | https://urlscan.io |
| **Any.run** | Sandbox de malware | https://any.run |
| **Hybrid Analysis** | Análise de arquivos | https://hybrid-analysis.com |

---

## 📊 OSINT de Empresas

### Informações Corporativas

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| **Crunchbase** | Informações de startups | https://crunchbase.com |
| **OpenCorporates** | Database de empresas | https://opencorporates.com |
| **Companies House** | Empresas UK | https://companieshouse.gov.uk |
| **SEC EDGAR** | Empresas US (públicas) | https://sec.gov/edgar |

---

### Vagas de Emprego (Tech Stack)

```
Buscar em:
├─ LinkedIn Jobs
├─ Indeed
├─ Glassdoor
├─ AngelList
└─ Site da empresa

O que procurar:
├─ Tecnologias mencionadas (AWS, Azure, etc.)
├─ Ferramentas de segurança usadas
├─ Linguagens de programação
├─ Frameworks e bibliotecas
└─ Estrutura do time
```

---

## 🎯 Metodologia OSINT Completa

### Fase 1: Definir Objetivos
```
1. O que você está buscando?
   ├─ Informações sobre domínio?
   ├─ Dados de pessoas?
   ├─ Infraestrutura técnica?
   └─ Vazamentos de dados?

2. Qual o escopo?
   ├─ Domínio principal
   ├─ Subdomínios
   ├─ Funcionários
   └─ Parceiros
```

---

### Fase 2: Coleta Passiva
```
1. [ ] WHOIS e DNS
2. [ ] Subdomínios (crt.sh, DNSDumpster)
3. [ ] Histórico (Wayback Machine)
4. [ ] Tecnologias (BuiltWith, Wappalyzer)
5. [ ] Shodan e Censys
6. [ ] Google Dorking
7. [ ] Redes Sociais
8. [ ] Vazamentos de dados
```

---

### Fase 3: Análise e Correlação
```
1. Organizar dados coletados
2. Criar mapa de infraestrutura
3. Identificar padrões
4. Correlacionar informações
5. Validar dados (cross-reference)
```

---

### Fase 4: Documentação
```
1. Screenshots de evidências
2. Salvar arquivos e outputs
3. Manter log de fontes
4. Criar timeline se necessário
5. Relatório final com achados
```

---

## 📝 Checklist OSINT

### Domínio e Infraestrutura
- [ ] WHOIS lookup
- [ ] DNS records completos
- [ ] Enumeração de subdomínios
- [ ] Certificados SSL/TLS
- [ ] Histórico DNS (SecurityTrails)
- [ ] Shodan/Censys scan
- [ ] Tecnologias web identificadas
- [ ] Wayback Machine

### Email e Pessoas
- [ ] Email harvesting (theHarvester, Hunter.io)
- [ ] Verificação de vazamentos (HIBP)
- [ ] LinkedIn dos funcionários
- [ ] Usernames em redes sociais (Sherlock)
- [ ] Informações públicas de pessoas-chave

### Documentos e Metadados
- [ ] Google Dorking (PDFs, DOCs)
- [ ] Download e análise de metadados (FOCA)
- [ ] Busca em repositórios GitHub
- [ ] Documentos em sites de terceiros

### Segurança
- [ ] CVEs conhecidos das tecnologias
- [ ] Vazamentos no GitHub
- [ ] Configurações expostas (.env, config)
- [ ] Credenciais em Pastebin
- [ ] Análise de SSL/TLS (SSL Labs)

---

## 💡 Dicas Profissionais

### 1. Automatize, mas Valide
```
Ferramentas automatizadas economizam tempo, MAS:
├─ Podem ter falsos positivos
├─ Podem perder informações
└─ Precisam de validação manual
```

### 2. Documente TUDO
```
Para cada informação coletada, registre:
├─ Fonte (onde encontrou)
├─ Data e hora
├─ Screenshot/evidência
├─ URL ou comando usado
└─ Contexto
```

### 3. Respeite Rate Limits
```
Ao usar APIs e ferramentas:
├─ Use delays entre requests
├─ Respeite ToS (Terms of Service)
├─ Considere usar proxies/VPN
└─ Evite banimentos
```

### 4. Pense em Pivot
```
Um dado leva a outro:
Email → Nome → LinkedIn → Outros emails → Domínios → Subdomínios
```

---

## ⚠️ Considerações Legais e Éticas

### ✅ É Legal e Ético:
- Buscar informações publicamente disponíveis
- Usar motores de busca
- Acessar redes sociais públicas
- Consultar databases públicos
- Usar ferramentas OSINT em dados próprios

### ❌ NÃO É Legal:
- Acessar contas sem autorização
- Fazer engenharia social sem permissão
- Usar dados para fins maliciosos
- Violar termos de serviço
- Coletar dados protegidos por LGPD/GDPR sem consentimento

### Princípios Éticos
```
1. Respeite a privacidade das pessoas
2. Não use OSINT para assédio ou stalking
3. Obtenha autorização quando necessário
4. Use dados responsavelmente
5. Siga as leis locais e internacionais
```

---

## 📚 Recursos para Aprendizado

### Sites e Blogs
- **OSINT Framework** - https://osintframework.com
- **Bellingcat** - https://bellingcat.com
- **OSINT Curious** - https://osintcurio.us
- **IntelTechniques** - https://inteltechniques.com

### Livros
- "Open Source Intelligence Techniques" - Michael Bazzell
- "OSINT Techniques: Resources for Uncovering Online Information"
- "The OSINT Handbook"

### Cursos
- TCM Security - External Pentest
- TryHackMe - OSINT Room
- SANS SEC487 - Open-Source Intelligence Gathering

### Comunidades
- Reddit: r/OSINT
- Twitter: #OSINT
- Discord: OSINT communities

---

## 🎓 Exercícios Práticos

### Nível Iniciante
1. Faça OSINT completo do seu próprio domínio
2. Encontre 10 subdomínios de uma empresa pública
3. Use Sherlock para buscar seu próprio username

### Nível Intermediário
1. Crie mapa de infraestrutura usando Maltego
2. Automatize coleta com Recon-ng
3. Documente stack tecnológico completo de um site

### Nível Avançado
1. Correlacione dados de múltiplas fontes
2. Crie script Python para automatizar coleta
3. Faça análise completa de superfície de ataque

---

<div align="center">

**🕵️ OSINT é a arte de encontrar o que está escondido à vista de todos**

*90% do OSINT é paciência e criatividade*

---

*Conteúdo educacional | Use com responsabilidade e ética*

</div>
