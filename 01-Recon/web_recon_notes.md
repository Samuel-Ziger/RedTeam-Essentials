# 🌐 Web Reconnaissance - Notas Completas

> Guia detalhado sobre reconhecimento de aplicações web de forma passiva e ativa

---

## 📋 Índice

1. [Introdução ao Web Recon](#introdução)
2. [Footprinting Passivo](#footprinting-passivo)
3. [Identificação de Tecnologias](#identificação-de-tecnologias)
4. [Enumeração de Diretórios e Arquivos](#enumeração)
5. [Análise de Aplicação](#análise-de-aplicação)
6. [Web Crawling](#web-crawling)
7. [Ferramentas Essenciais](#ferramentas)
8. [Metodologia Completa](#metodologia)

---

## 🎯 Introdução

**Web Reconnaissance** é o processo de coletar informações sobre uma aplicação web para entender sua estrutura, tecnologias, possíveis pontos de entrada e superfície de ataque.

### Objetivos do Web Recon
- 🔍 Descobrir tecnologias utilizadas
- 📂 Mapear estrutura de diretórios
- 🔐 Identificar mecanismos de autenticação
- 🚪 Encontrar possíveis pontos de entrada
- 📝 Coletar informações sobre a aplicação

---

## 🕵️ Footprinting Passivo

### 1. Análise Inicial da URL

```
https://www.exemplo.com:443/login.php?redirect=/dashboard

Breakdown:
├─ Protocolo: https (SSL/TLS)
├─ Subdomínio: www
├─ Domínio: exemplo.com
├─ Porta: 443 (padrão HTTPS)
├─ Recurso: /login.php
└─ Parâmetros: ?redirect=/dashboard
```

**O que observar:**
- Uso de HTTPS vs HTTP
- Estrutura de subdomínios
- Extensões de arquivo (.php, .aspx, .jsp)
- Parâmetros GET sensíveis

---

### 2. Robots.txt

O arquivo `robots.txt` indica aos crawlers quais áreas **não** devem ser indexadas.

```
Acesso: https://exemplo.com/robots.txt
```

**Exemplo de robots.txt:**
```
User-agent: *
Disallow: /admin/
Disallow: /backup/
Disallow: /config/
Disallow: /private/
Allow: /public/

Sitemap: https://exemplo.com/sitemap.xml
```

**Por que é importante:**
- Revela diretórios sensíveis
- Mostra áreas que o site quer esconder
- Pode conter caminhos interessantes

⚠️ **ATENÇÃO**: Robots.txt NÃO é medida de segurança! É apenas uma sugestão para crawlers.

---

### 3. Sitemap.xml

Lista estruturada de todas as páginas do site.

```
Acesso: https://exemplo.com/sitemap.xml
```

**Exemplo:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://exemplo.com/</loc>
    <lastmod>2025-01-15</lastmod>
  </url>
  <url>
    <loc>https://exemplo.com/produtos/</loc>
    <lastmod>2025-01-10</lastmod>
  </url>
  <url>
    <loc>https://exemplo.com/admin/dashboard/</loc>
    <lastmod>2025-01-05</lastmod>
  </url>
</urlset>
```

**Informações úteis:**
- Estrutura completa do site
- Páginas ocultas não linkadas
- Datas de modificação

---

### 4. Análise de Cabeçalhos HTTP

```bash
# Usando curl
curl -I https://exemplo.com

# Resultado esperado:
HTTP/2 200
server: nginx/1.18.0
date: Fri, 22 Nov 2025 10:00:00 GMT
content-type: text/html; charset=UTF-8
x-powered-by: PHP/7.4.3
set-cookie: PHPSESSID=abc123; HttpOnly; Secure
strict-transport-security: max-age=31536000
x-frame-options: SAMEORIGIN
x-content-type-options: nosniff
```

**O que analisar:**

| Cabeçalho | Informação Revelada |
|-----------|---------------------|
| `Server` | Servidor web (nginx, Apache, IIS) |
| `X-Powered-By` | Linguagem/Framework (PHP, ASP.NET) |
| `Set-Cookie` | Flags de segurança (HttpOnly, Secure) |
| `X-Frame-Options` | Proteção contra Clickjacking |
| `Content-Security-Policy` | Políticas de segurança |

---

## 🔧 Identificação de Tecnologias

### Ferramentas Automatizadas

#### 1. Wappalyzer (Extensão Browser)
- Detecta CMS (WordPress, Joomla, Drupal)
- Frameworks (React, Angular, Vue.js)
- Servidores web
- Analytics e tracking

#### 2. BuiltWith
```
https://builtwith.com/exemplo.com
```
Mostra:
- Stack tecnológico completo
- Serviços de hospedagem
- CDNs utilizadas
- Plugins e widgets

#### 3. WhatWeb (CLI)
```bash
whatweb https://exemplo.com

# Saída exemplo:
https://exemplo.com [200 OK] 
  Country: UNITED STATES
  HTTPServer: nginx/1.18.0
  IP: 93.184.216.34
  PoweredBy: PHP/7.4.3
  Title: Exemplo Site
  WordPress: 5.8
```

---

### Detecção Manual

#### Assinaturas no HTML
```html
<!-- WordPress -->
<meta name="generator" content="WordPress 5.8" />

<!-- Joomla -->
<meta name="generator" content="Joomla! - Open Source Content Management" />

<!-- Drupal -->
<meta name="Generator" content="Drupal 9" />
```

#### Estrutura de Diretórios Padrão
```
WordPress:
├─ /wp-admin/
├─ /wp-content/
├─ /wp-includes/
└─ /wp-login.php

Joomla:
├─ /administrator/
├─ /components/
├─ /modules/
└─ /templates/

Drupal:
├─ /core/
├─ /modules/
├─ /sites/
└─ /themes/
```

---

## 📂 Enumeração

### Diretórios e Arquivos Comuns

```
Arquivos de Configuração:
├─ .env
├─ config.php
├─ settings.py
├─ web.config
└─ application.yml

Arquivos Sensíveis:
├─ .git/
├─ .svn/
├─ backup.sql
├─ database.sql
└─ phpinfo.php

Painéis Admin:
├─ /admin/
├─ /administrator/
├─ /manager/
├─ /cpanel/
└─ /dashboard/
```

### Ferramentas de Directory Bruteforce

⚠️ **ATENÇÃO**: Use apenas em ambientes autorizados!

#### Gobuster
```bash
gobuster dir -u https://exemplo.com -w /path/to/wordlist.txt

Opções úteis:
-t 50          # 50 threads
-x php,html    # Buscar extensões específicas
-s 200,301     # Filtrar por status code
-o output.txt  # Salvar resultados
```

#### Dirsearch
```bash
dirsearch -u https://exemplo.com -e php,html,js

Opções:
-t 50          # Threads
-r             # Recursivo
-x 403,404     # Excluir status codes
```

#### Feroxbuster (Rápido e Recursivo)
```bash
feroxbuster -u https://exemplo.com -w wordlist.txt -t 100 -d 2

-d 2           # Profundidade de recursão
-t 100         # Threads
```

---

### Wordlists Recomendadas

```
SecLists (GitHub):
├─ Discovery/Web-Content/
│  ├─ common.txt
│  ├─ big.txt
│  ├─ directory-list-2.3-medium.txt
│  └─ raft-large-directories.txt
│
└─ Discovery/DNS/
   ├─ subdomains-top1million.txt
   └─ dns-Jhaddix.txt
```

---

## 🔍 Análise de Aplicação

### 1. Formulários e Inputs

```html
<form action="/login.php" method="POST">
    <input type="text" name="username" />
    <input type="password" name="password" />
    <input type="hidden" name="csrf_token" value="abc123" />
    <button type="submit">Login</button>
</form>
```

**O que observar:**
- ✅ Método (GET vs POST)
- ✅ Presença de CSRF tokens
- ✅ Validação client-side (JavaScript)
- ✅ Campos hidden
- ✅ Autocomplete habilitado

---

### 2. JavaScript e APIs

#### Encontrar Endpoints de API
```javascript
// Procurar no código-fonte por:
fetch('/api/users')
axios.get('/api/data')
$.ajax({url: '/api/search'})

// Padrões comuns:
/api/v1/
/rest/
/graphql
/api/internal/
```

#### Ferramentas para Análise JS
- **JSParser** - Extrai endpoints de arquivos JS
- **LinkFinder** - Encontra URLs em JavaScript
- **Browser DevTools** - Aba Network para ver requests

```bash
# LinkFinder
python linkfinder.py -i https://exemplo.com -o cli
```

---

### 3. Cookies e Sessões

```
Análise de Cookie:
PHPSESSID=abc123def456; Path=/; HttpOnly; Secure; SameSite=Strict

Flags de Segurança:
├─ HttpOnly → Previne acesso via JavaScript (XSS)
├─ Secure → Só envia via HTTPS
├─ SameSite → Previne CSRF
└─ Path → Escopo do cookie
```

**Ferramenta:** Browser Developer Tools → Application → Cookies

---

## 🕷️ Web Crawling

### Crawlers Automatizados

#### Burp Suite Spider
1. Configure o proxy (127.0.0.1:8080)
2. Navegue pelo site manualmente
3. Target → Site Map
4. Right-click → Spider this host

#### OWASP ZAP Spider
```
1. Quick Start → Automated Scan
2. Ou: Tools → Spider → Add URL
```

#### Scrapy (Python)
```python
import scrapy

class ExemploSpider(scrapy.Spider):
    name = 'exemplo'
    start_urls = ['https://exemplo.com']
    
    def parse(self, response):
        # Extrai todos os links
        for link in response.css('a::attr(href)').getall():
            yield {'url': link}
        
        # Segue links
        for href in response.css('a::attr(href)').getall():
            yield response.follow(href, self.parse)
```

---

### Crawling Manual

**Áreas importantes:**
```
├─ Páginas de Login/Registro
├─ Formulários de contato
├─ Upload de arquivos
├─ Perfis de usuário
├─ Painel administrativo
├─ API endpoints
├─ Documentação
└─ Páginas de erro (404, 500)
```

---

## 🛠️ Ferramentas Essenciais

### Suite Completa - Burp Suite
```
Recursos principais:
├─ Proxy → Interceptar requests
├─ Spider → Crawler automático
├─ Repeater → Replay requests
├─ Intruder → Fuzzing e brute force
├─ Scanner → Detectar vulnerabilidades (Pro)
└─ Extensions → Expandir funcionalidades
```

### Alternativa Open Source - OWASP ZAP
```
Funcionalidades:
├─ Active Scanner
├─ Passive Scanner
├─ Spider
├─ Fuzzer
├─ API Support
└─ Add-ons
```

### Linha de Comando

| Ferramenta | Uso |
|------------|-----|
| **curl** | Requests HTTP manuais |
| **wget** | Download recursivo |
| **httpie** | HTTP client user-friendly |
| **nuclei** | Scanner de vulnerabilidades |
| **ffuf** | Fuzzing rápido |

---

## 📋 Metodologia Completa

### Fase 1: Reconhecimento Passivo
```
1. [ ] Acessar site e navegar manualmente
2. [ ] Verificar robots.txt
3. [ ] Analisar sitemap.xml
4. [ ] Inspecionar código-fonte HTML
5. [ ] Analisar cabeçalhos HTTP
6. [ ] Identificar tecnologias (Wappalyzer)
7. [ ] Buscar no Wayback Machine
8. [ ] Google Dorking do site
```

### Fase 2: Mapeamento Ativo
```
1. [ ] Spider/Crawler automático
2. [ ] Enumeração de diretórios
3. [ ] Busca de arquivos sensíveis
4. [ ] Identificar parâmetros GET/POST
5. [ ] Mapear formulários
6. [ ] Extrair endpoints de APIs
7. [ ] Analisar JavaScript
8. [ ] Testar páginas de erro
```

### Fase 3: Análise Profunda
```
1. [ ] Testar autenticação
2. [ ] Verificar HTTPS/TLS
3. [ ] Analisar cookies e sessões
4. [ ] Buscar comentários no código
5. [ ] Verificar versionamento (.git, .svn)
6. [ ] Testar upload de arquivos
7. [ ] Verificar CORS
8. [ ] Analisar CSP headers
```

### Fase 4: Documentação
```
1. [ ] Criar mapa visual do site
2. [ ] Listar todas as URLs encontradas
3. [ ] Documentar tecnologias
4. [ ] Anotar possíveis vetores de ataque
5. [ ] Organizar screenshots
6. [ ] Preparar relatório
```

---

## 🎯 Checklist de Web Recon

### Informações Básicas
- [ ] URL principal e subdomínios
- [ ] Servidor web (nginx, Apache, IIS)
- [ ] Linguagem backend (PHP, Python, .NET)
- [ ] Framework (Laravel, Django, Express)
- [ ] CMS (WordPress, Drupal, Joomla)
- [ ] Frontend framework (React, Vue, Angular)

### Arquivos Sensíveis
- [ ] robots.txt
- [ ] sitemap.xml
- [ ] .git/ ou .svn/
- [ ] backup files (.bak, .old, ~)
- [ ] config files (.env, config.php)
- [ ] phpinfo.php
- [ ] README, CHANGELOG

### Segurança
- [ ] HTTPS configurado corretamente
- [ ] Cabeçalhos de segurança presentes
- [ ] Cookies com flags corretas
- [ ] CSRF tokens implementados
- [ ] Rate limiting em formulários
- [ ] Captcha em áreas sensíveis

---

## 💡 Dicas de Ouro

### 1. Combine Ferramentas
Não dependa de uma única ferramenta:
```
Wappalyzer + WhatWeb + BuiltWith = Visão completa das tecnologias
Gobuster + Dirsearch + Feroxbuster = Enumeração abrangente
```

### 2. Use Wordlists Contextuais
```
Site em PHP? Use wordlist focada em PHP
WordPress? Use wordlist de plugins/themes do WP
API? Use wordlist de endpoints REST
```

### 3. Preste Atenção aos Detalhes
```
404 personalizado pode revelar framework
Mensagens de erro expõem paths internos
Comentários HTML podem ter TODOs dos devs
```

### 4. Documente TUDO
```
Tire screenshots
Salve responses completas
Anote comportamentos estranhos
Mantenha log de timestamps
```

---

## ⚠️ Avisos Legais

### Reconhecimento Ativo vs Passivo

**Passivo** (Geralmente Legal):
- Acessar site normalmente
- Ver código-fonte HTML
- Consultar robots.txt, sitemap
- Usar ferramentas públicas (Wappalyzer)

**Ativo** (Requer Autorização):
- Directory bruteforce
- Fuzzing de parâmetros
- Testes de vulnerabilidade
- Scanning automatizado

### Regra de Ouro
> **Sempre tenha autorização por escrito antes de fazer testes ativos!**

---

## 📚 Recursos para Estudo

### Laboratórios Práticos
- **PortSwigger Web Security Academy** - Labs gratuitos
- **HackTheBox** - Máquinas web reais
- **TryHackMe** - Rooms de web hacking
- **PentesterLab** - Exercícios focados

### Leituras Recomendadas
- OWASP Testing Guide
- Web Application Hacker's Handbook
- Real-World Bug Hunting

### YouTube Channels
- NahamSec
- STÖK
- InsiderPhD
- PwnFunction

---

<div align="center">

**🌐 Web Recon é a fundação de todo web pentest**

*Conhecer a aplicação é o primeiro passo para protegê-la*

---

*Conteúdo educacional | Use responsavelmente*

</div>
