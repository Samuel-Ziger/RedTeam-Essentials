# SSRF Deep Dive

> Server-Side Request Forgery: a aplicacao faz requisicoes HTTP (ou outros protocolos) para um destino controlado pelo atacante. Guia educacional para labs locais (`docker-lab`). **MITRE ATT&CK: T1190** (e frequentemente encadeado com acesso a metadados cloud / rede interna).

---

## Etica e escopo

- Pratique apenas em alvos autorizados do `docker-lab` ou ambientes de teste com contrato.
- Nao aponte scanners SSRF para IPs/hosts de producao, terceiros ou cloud accounts reais sem autorizacao.
- Em cloud: acessar IMDS (Instance Metadata Service) em conta do cliente exige escopo escrito e cuidado extremo — prefira labs/simulacoes.
- Documente impacto com evidencias minimas (status, headers, trecho nao sensivel). Sem dumps de secrets reais em relatorios compartilhados sem necessidade.

---

## 1. O que e SSRF

O servidor aceita uma URL (ou host) do usuario e a usa em `fetch`, `curl`, `HttpClient`, webhook, gerador de preview, importador de avatar, etc. O atacante redireciona essa chamada para:

- Servicos internos (`127.0.0.1`, `169.254.169.254`, rede VPC)
- Protocolos perigosos (`file://`, `gopher://`, `dict://` — depende da lib)
- Outros tenants / APIs internas

```text
Usuario -> App vulneravel -> Alvo interno (metadata, admin, Redis, ...)
                 ^
                 | URL controlada
```

**Mapeamento:**

| Framework | Referencia |
|-----------|------------|
| MITRE ATT&CK | T1190 (acesso inicial / abuso de app publica) |
| OWASP Top 10 2021 | A10:2021 — Server-Side Request Forgery |
| CWE | CWE-918 |

---

## 2. Tipos de SSRF

### 2.1 Basic / in-band

A resposta do alvo interno e refletida (parcial ou total) na resposta HTTP ao atacante. Ideal para leitura de paginas internas e, em cloud mal configurada, metadados.

### 2.2 Blind SSRF

A app nao devolve o corpo da resposta interna. Voce observa:

- Diferenca de tempo (host existe vs timeout)
- Codigo HTTP / mensagem generica
- Callback OOB (DNS/HTTP) se a app seguir redirects ou resolver DNS

Em lab, use listeners controlados (Burp Collaborator / Interactsh) **somente** se o ambiente permitir saida de rede — no `docker-lab` restrito, foque em alvos internos da rede compose (`172.28.0.0/24`).

### 2.3 Semi-blind

Vazam headers, tamanho, status ou erro parcial, sem o body completo.

### 2.4 SSRF via redirect / parser confusion

Filtros validam a URL inicial (`https://allowed.com`) mas a lib segue redirect para `http://169.254.169.254/`. Outro vetor: diferenca entre o que o validador parseia e o que o cliente HTTP realmente solicita (URL encoding, credenciais em URL, DNS rebinding — conceito avancado).

---

## 3. Cloud metadata risk (IMDS)

Instancias cloud expoe um endpoint link-local para metadados (credenciais temporarias, user-data, hostname).

| Cloud | Endpoint classico (conceito) | Nota |
|-------|------------------------------|------|
| AWS | `http://169.254.169.254/latest/meta-data/` | IMDSv2 exige token PUT — reduz SSRF simples |
| GCP | `http://169.254.169.254/computeMetadata/v1/` | Header `Metadata-Flavor: Google` obrigatorio |
| Azure | `http://169.254.169.254/metadata/instance` | Header `Metadata: true` |

**Por que importa:** SSRF + IMDS aberto (IMDSv1 / sem hop limit) pode levar a credenciais de role da instancia.

**Defesa cloud (resumo):**

1. Exigir **IMDSv2** (AWS) / headers obrigatorios (GCP/Azure).
2. Restringir rotas de egress da app (security groups / firewall).
3. Nao colocar secrets em user-data.
4. Least privilege nas instance roles.
5. Bloquear `169.254.169.254` no proxy HTTP da aplicacao.

> Neste repositorio, o treino pratico de SSRF deve ficar no `docker-lab`. Nao use contas cloud reais como alvo de exercicio.

---

## 4. Superficies comuns

Procure parametros e features:

- `url`, `uri`, `path`, `dest`, `redirect`, `next`, `image`, `avatar`, `webhook`, `callback`, `feed`, `proxy`, `link`
- Importadores: "fetch from URL", "PDF from URL", "screenshot service"
- Integracoes: OpenID discovery, JWKS URL (`jku`/`x5u` — ver [auth-bypass-patterns.md](auth-bypass-patterns.md))
- Microservicos que "enriquecem" dados chamando APIs internas

Checklist de recon:

- [ ] Proxy Burp: observe requests com URL completa no body/query
- [ ] JS/Swagger: endpoints que aceitam URI
- [ ] Features de upload por URL
- [ ] Webhooks configuraveis pelo usuario

---

## 5. Bypass de filtros — overview (educacional)

Filtros fracos tentam blocklist de `localhost` / IPs privados. Ideias **conceituais** para lab (nao e lista de ataque a producao):

| Classe de bypass | Ideia |
|------------------|-------|
| Alternativas a localhost | `127.0.0.1`, `127.1`, `0`, `[::1]`, nome que resolve para loopback |
| Decimal / hex IP | Representacoes alternativas do mesmo IP (quando o parser aceita) |
| DNS / hostname interno | Nome de servico Docker (`dvwa`, `juiceshop`) na rede compose |
| Redirect | URL "permitida" que redireciona ao alvo |
| Scheme | Trocar `http` por outro suportado pela lib |
| Encoding | `%00`, double encoding, Unicode confusables — depende do parser |
| Credenciais na URL | `http://user@host` confundindo regexes ingenuas |

**Boa defesa nao e blocklist:** e allowlist de hosts/esquemas + HTTP client hardened (sem redirects perigosos, sem protocols exoticos) + rede segregada.

---

## 6. Labs no docker-lab

### 6.1 Mapa de alvos

| Servico | URL | Relevancia SSRF |
|---------|-----|-----------------|
| Juice Shop | http://127.0.0.1:8082 | Challenges OWASP; procure features que buscam URL / integracoes |
| VAmPI | http://127.0.0.1:8087 | API OWASP Top 10; combine com checklist de API |
| DVWA | http://127.0.0.1:8081 | Nem sempre SSRF dedicado; util como alvo interno da rede |
| Rede interna | `172.28.0.0/24` | Do ponto de vista de um servico vulneravel, peers do compose |

### 6.2 Exercicio conceitual — rede compose

1. Suba o lab: `cd docker-lab && docker compose up -d` (ver [docker-lab/README.md](../docker-lab/README.md)).
2. Identifique um parametro que aceite URL (Juice Shop challenge ou feature de lab documentada no score board).
3. Em vez de Internet, aponte para um peer interno (ex.: outro container na `172.28.0.x`) **somente** se o challenge pedir.
4. Documente: request, host interno alcancado, o que vazou (status/body minimo).
5. Relacione com risco cloud: "mesmo padrao contra IMDS em ambiente mal protegido".

### 6.3 Juice Shop

- Abra http://127.0.0.1:8082 e o **Score Board**.
- Filtre challenges por palavras-chave relacionadas a SSRF / request forgery / metadata (nomes mudam entre versoes).
- Objetivo educacional: completar a flag do challenge, nao varrer a Internet.
- Lab XSS relacionado: [labs/lab-02-juice-xss.md](labs/lab-02-juice-xss.md) — SSRF pode aparecer em outra trilha do mesmo app.

### 6.4 VAmPI

- API em http://127.0.0.1:8087 — explore OpenAPI/Swagger se exposto.
- Combine SSRF (se houver endpoint de fetch) com [labs/lab-03-vampi-api.md](labs/lab-03-vampi-api.md) (BOLA/auth).
- Use a [api-security-checklist.md](api-security-checklist.md) secao Input Validation (item SSRF).

---

## 7. Deteccao pratica (lab)

### 7.1 Sinais

- Parametro URL + delay quando aponta para porta fechada vs aberta
- Mensagens "connection refused", "timeout", "ENOTFOUND"
- Body que ecoa HTML de outro servico interno
- DNS query no seu listener (blind)

### 7.2 Metodologia segura

1. Baseline: URL legitima permitida pela feature.
2. Troque para um host interno **do lab** (ex. peer compose).
3. Meça tempo e status.
4. Se in-band, leia so o necessario para prova.
5. Pare — nao enumere toda a rede corporativa fora do escopo.

### 7.3 Encadeamentos

- SSRF → admin interno sem auth
- SSRF → Redis/memcached (conceitual; impacto alto)
- SSRF → IMDS → credenciais cloud
- XSS em admin + SSRF interno (vitima privilegiada)

---

## 8. Defesa

### 8.1 Controles preferidos

1. **Allowlist** de dominios/esquemas (`https` + hosts conhecidos).
2. Resolver DNS e **bloquear** ranges privados/link-local **depois** do resolve (cuidado com DNS rebinding: re-verifique IP no connect).
3. Desabilitar redirects ou validar cada hop.
4. Usar cliente HTTP sem `file://`, `gopher://`, etc.
5. Segmentacao: app em subnet sem rota para IMDS/metadata ou com iptables drop `169.254.169.254`.
6. IMDSv2 / headers obrigatorios na cloud.
7. Nao confiar em blocklist de string (`localhost` apenas).

### 8.2 Exemplo de validacao (conceitual)

```python
from urllib.parse import urlparse
import ipaddress
import socket

ALLOWED_HOSTS = {"images.lab.local", "cdn.lab.local"}

def is_public_ip(ip: str) -> bool:
    addr = ipaddress.ip_address(ip)
    return addr.is_global

def safe_url(url: str) -> bool:
    p = urlparse(url)
    if p.scheme != "https":
        return False
    if p.hostname not in ALLOWED_HOSTS:
        return False
    infos = socket.getaddrinfo(p.hostname, 443, proto=socket.IPPROTO_TCP)
    return all(is_public_ip(i[4][0]) for i in infos)
```

Ajuste a politica ao produto: muitos sistemas **precisam** chamar APIs internas — nesse caso, allowlist interna explicita e identidade de servico (mTLS), nao "URL livre do usuario".

### 8.3 Deteccao defensiva

- WAF/rules para parametros URL suspeitos (apoio, nao unica barreira)
- Alertas de egress da app para link-local / RFC1918 inesperado
- CSP/nao aplicavel diretamente; foque em network + app code

---

## 9. Como reportar

No [REPORT-TEMPLATE.md](../REPORT-TEMPLATE.md):

1. Titulo: SSRF em parametro `url` (feature X).
2. Severidade: tipicamente Alta/Critica se alcanca metadata ou admin interno.
3. Passos: request completo (lab), URL interna usada.
4. Evidencia: status + trecho nao sensivel.
5. Impacto: leitura de servico interno / hipotese IMDS em cloud.
6. Remediacao: allowlist, bloqueio IMDS, IMDSv2, least privilege.
7. MITRE: T1190.

---

## 10. Checklist rapido

- [ ] Mapear features que consomem URL
- [ ] Classificar in-band vs blind
- [ ] Testar apenas hosts do lab / escopo
- [ ] Avaliar risco metadata (conceitual + hardening cloud)
- [ ] Verificar redirects e schemes
- [ ] Prova minima documentada
- [ ] Remediacao com allowlist + rede

---

## Referencias

- [OWASP SSRF](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
- [PortSwigger SSRF](https://portswigger.net/web-security/ssrf)
- [AWS IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
- [OWASP A10:2021](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery/)
- Juice Shop / VAmPI no lab: [docker-lab/README.md](../docker-lab/README.md)
