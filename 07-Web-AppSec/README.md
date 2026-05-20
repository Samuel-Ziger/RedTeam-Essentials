# 07 - Web Application Security

> Modulo focado em recon, exploitation e validacao de vulnerabilidades em aplicacoes web modernas (SPA, REST/GraphQL, microsservicos).

## Conteudo

| Documento | Tema |
|-----------|------|
| [owasp-top10-2021.md](owasp-top10-2021.md) | OWASP Top 10 (2021) com como detectar e mitigar cada item. |
| [api-security-checklist.md](api-security-checklist.md) | Checklist de pentest para APIs REST/GraphQL (OWASP API Top 10). |
| [recon-web-pratico.md](recon-web-pratico.md) | Recon web pratico: ffuf, gobuster, katana, nuclei, gowitness. |
| [xss-deep-dive.md](xss-deep-dive.md) | XSS: contextos, bypasses de WAF, payloads modernos (Trusted Types). |
| [auth-bypass-patterns.md](auth-bypass-patterns.md) | Padroes de bypass de autenticacao/autorizacao (BOLA/IDOR). |

> Use a wordlist [`SecLists`](https://github.com/danielmiessler/SecLists) - instalada por `linux_postinstall.sh`.

## Fluxo recomendado

1. **Recon passivo** - subdominios, JS analysis, Github dorks (modulo 01-02).
2. **Recon ativo** - port scan, virtual hosts, technology fingerprint (`whatweb`, `wappalyzer`).
3. **Surface mapping** - crawl com `katana` ou `gospider`; salve URLs unicas.
4. **Vuln scan** - `nuclei -t cves/ -t exposures/` em low rate.
5. **Manual** - foco em logica de negocio (BOLA, business flaws), auth, file upload.
6. **Report** - usar `REPORT-TEMPLATE.md` da raiz.

## MITRE ATT&CK (parcial)

- T1190 - Exploit Public-Facing Application
- T1133 - External Remote Services
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process

## Etica e escopo

Apenas em aplicacoes com autorizacao formal e escopo definido. Cuidados especiais com:

- Dados de usuarios reais - PII/dados sensiveis precisam de tratamento.
- Endpoints de pagamento - jamais teste em ambiente de producao sem aval.
- Rate limit - configure no Burp/ffuf para nao derrubar o servico.
