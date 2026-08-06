# 07 - Web Application Security

> Modulo focado em recon, exploitation e validacao de vulnerabilidades em aplicacoes web modernas (SPA, REST/GraphQL, microsservicos).

## Conteudo

| Documento | Tema |
|-----------|------|
| [owasp-top10-2021.md](owasp-top10-2021.md) | OWASP Top 10 (2021) com como detectar e mitigar cada item. |
| [api-security-checklist.md](api-security-checklist.md) | Checklist de pentest para APIs REST/GraphQL (OWASP API Top 10). |
| [recon-web-pratico.md](recon-web-pratico.md) | Recon web pratico: ffuf, gobuster, katana, nuclei, gowitness. |
| [xss-deep-dive.md](xss-deep-dive.md) | XSS: contextos, bypasses de WAF, payloads modernos (Trusted Types). |
| [sqli-deep-dive.md](sqli-deep-dive.md) | SQL Injection: tipos, deteccao, sqlmap em lab, defesa (T1190). |
| [ssrf-deep-dive.md](ssrf-deep-dive.md) | SSRF: tipos, risco IMDS, bypass overview, labs e defesa. |
| [auth-bypass-patterns.md](auth-bypass-patterns.md) | Padroes de bypass de autenticacao/autorizacao (BOLA/IDOR). |

### Labs guiados (`docker-lab`)

| Lab | Alvo local | Foco |
|-----|------------|------|
| [labs/lab-01-dvwa-sqli.md](labs/lab-01-dvwa-sqli.md) | http://127.0.0.1:8081 | DVWA SQLi Low → Medium |
| [labs/lab-02-juice-xss.md](labs/lab-02-juice-xss.md) | http://127.0.0.1:8082 | Juice Shop XSS / DOM (Score Board) |
| [labs/lab-03-vampi-api.md](labs/lab-03-vampi-api.md) | http://127.0.0.1:8087 | VAmPI BOLA / auth bypass |

> Use a wordlist [`SecLists`](https://github.com/danielmiessler/SecLists) - instalada por `linux_postinstall.sh`.
> Lab: [`docker-lab/README.md`](../docker-lab/README.md) — `cd docker-lab && docker compose up -d --build`.

## Fluxo recomendado

1. **Recon passivo** - subdominios, JS analysis, Github dorks (modulo 01-02).
2. **Recon ativo** - port scan, virtual hosts, technology fingerprint (`whatweb`, `wappalyzer`).
3. **Surface mapping** - crawl com `katana` ou `gospider`; salve URLs unicas. Ver [recon-web-pratico.md](recon-web-pratico.md).
4. **Vuln scan** - `nuclei -t cves/ -t exposures/` em low rate.
5. **Fundamentos OWASP** - [owasp-top10-2021.md](owasp-top10-2021.md) + [api-security-checklist.md](api-security-checklist.md).
6. **Deep dives manuais** (teoria → lab):
   1. XSS → [xss-deep-dive.md](xss-deep-dive.md) → [labs/lab-02-juice-xss.md](labs/lab-02-juice-xss.md)
   2. SQLi → [sqli-deep-dive.md](sqli-deep-dive.md) → [labs/lab-01-dvwa-sqli.md](labs/lab-01-dvwa-sqli.md) (WebGoat `:8084` no deep dive)
   3. SSRF → [ssrf-deep-dive.md](ssrf-deep-dive.md) (Juice Shop / VAmPI / rede compose)
   4. AuthZ → [auth-bypass-patterns.md](auth-bypass-patterns.md) → [labs/lab-03-vampi-api.md](labs/lab-03-vampi-api.md)
7. **Manual avancado** - logica de negocio, file upload, encadeamentos.
8. **Report** - usar [`REPORT-TEMPLATE.md`](../REPORT-TEMPLATE.md) da raiz (evidencias minimas; sem dumps massivos).

## MITRE ATT&CK (parcial)

- T1190 - Exploit Public-Facing Application
- T1133 - External Remote Services
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process

## Etica e escopo

Apenas em aplicacoes com autorizacao formal e escopo definido. Para treino deste modulo, use **somente** o `docker-lab` em `127.0.0.1`. Cuidados especiais com:

- Dados de usuarios reais - PII/dados sensiveis precisam de tratamento.
- Endpoints de pagamento - jamais teste em ambiente de producao sem aval.
- Rate limit - configure no Burp/ffuf para nao derrubar o servico.
- Dumps - prove impacto com evidencia minima; nao exfiltre bases inteiras.
