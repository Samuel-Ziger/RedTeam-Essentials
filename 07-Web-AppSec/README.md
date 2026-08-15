# 07 - Web Application Security

> Modulo focado em recon, exploitation e validacao de vulnerabilidades em aplicacoes web modernas (SPA, REST/GraphQL, microsservicos).

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários com fundamentos de HTTP, terminal e escopo. |
| Pré-requisitos | Módulos [00](../00-Fundamentos/README.md) e [01](../01-Recon/README.md). |
| Tempo estimado | 12 horas de leitura e 8 horas nos três labs guiados. |
| Ambiente | Exclusivamente os alvos locais do `docker-lab`. |
| Evidência final | Três achados sanitizados com requisição, resposta, impacto e correção. |
| Critério de conclusão | Concluir os três labs, relacionar telemetria e executar o reset do ambiente. |

## Conteudo

| Documento | Tema |
|-----------|------|
| [owasp-top10-2021.md](owasp-top10-2021.md) | OWASP Top 10 (2021) com como detectar e mitigar cada item. |
| [api-security-checklist.md](api-security-checklist.md) | Checklist de pentest para APIs REST/GraphQL (OWASP API Top 10). |
| [recon-web-pratico.md](recon-web-pratico.md) | Recon web pratico: ffuf, gobuster, katana, nuclei, gowitness. |
| [enum-web-avancado.md](enum-web-avancado.md) | Enum avancada: dirs/vhosts/params (gobuster/ferox/wfuzz) + AXFR em lab. |
| [xss-deep-dive.md](xss-deep-dive.md) | XSS: contextos, bypasses de WAF, payloads modernos (Trusted Types). |
| [sqli-deep-dive.md](sqli-deep-dive.md) | SQL Injection: tipos, deteccao, sqlmap em lab, defesa (T1190). |
| [ssrf-deep-dive.md](ssrf-deep-dive.md) | SSRF: tipos, risco IMDS, bypass overview, labs e defesa. |
| [path-traversal-lfi.md](path-traversal-lfi.md) | Path traversal / LFI (wrappers PHP, defesa, lab DVWA/WebGoat). |
| [auth-bypass-patterns.md](auth-bypass-patterns.md) | Padroes de bypass de autenticacao/autorizacao (BOLA/IDOR). |
| [api-moderna-oauth-graphql-grpc.md](api-moderna-oauth-graphql-grpc.md) | OAuth/OIDC, GraphQL e gRPC: validação, autorização, limites e telemetria. |

### Labs guiados (`docker-lab`)

| Lab | Alvo local | Foco |
|-----|------------|------|
| [labs/lab-01-dvwa-sqli.md](labs/lab-01-dvwa-sqli.md) | http://127.0.0.1:8081 | DVWA SQLi Low → Medium |
| [labs/lab-02-juice-xss.md](labs/lab-02-juice-xss.md) | http://127.0.0.1:8082 | Juice Shop XSS / DOM (Score Board) |
| [labs/lab-03-vampi-api.md](labs/lab-03-vampi-api.md) | http://127.0.0.1:8087 | VAmPI BOLA / auth bypass |

Depois da tentativa, use a [rubrica e respostas orientativas](labs/answers/README.md)
para revisar evidência, causa, mitigação, telemetria e falsos positivos.

> Use a wordlist [`SecLists`](https://github.com/danielmiessler/SecLists) - instalada por `linux_postinstall.sh`.
> Lab: [`docker-lab/README.md`](../docker-lab/README.md) — `cd docker-lab && docker compose up -d --build`.

## Fluxo recomendado

1. **Recon passivo** - subdominios, JS analysis, Github dorks (modulo 01-02).
2. **Recon ativo** - port scan, virtual hosts, technology fingerprint (`whatweb`, `wappalyzer`).
3. **Surface mapping** - crawl com `katana` ou `gospider`; salve URLs unicas. Ver [recon-web-pratico.md](recon-web-pratico.md).
4. **Enum avancada** - dirs/vhosts/params e (se autorizado) AXFR. Ver [enum-web-avancado.md](enum-web-avancado.md).
5. **Vuln scan** - `nuclei -t cves/ -t exposures/` em low rate.
6. **Fundamentos OWASP** - [owasp-top10-2021.md](owasp-top10-2021.md) + [api-security-checklist.md](api-security-checklist.md).
7. **Deep dives manuais** (teoria → lab):
   1. XSS → [xss-deep-dive.md](xss-deep-dive.md) → [labs/lab-02-juice-xss.md](labs/lab-02-juice-xss.md)
   2. SQLi → [sqli-deep-dive.md](sqli-deep-dive.md) → [labs/lab-01-dvwa-sqli.md](labs/lab-01-dvwa-sqli.md) (WebGoat `:8084` no deep dive)
   3. SSRF → [ssrf-deep-dive.md](ssrf-deep-dive.md) (Juice Shop / VAmPI / rede compose)
   4. Path traversal / LFI → [path-traversal-lfi.md](path-traversal-lfi.md) (DVWA File Inclusion / WebGoat)
   5. AuthZ → [auth-bypass-patterns.md](auth-bypass-patterns.md) → [labs/lab-03-vampi-api.md](labs/lab-03-vampi-api.md)
8. **Manual avancado** - logica de negocio, file upload, encadeamentos.
9. **Report** - [`REPORT-TEMPLATE.md`](../REPORT-TEMPLATE.md) + PDF via [`report/README.md`](../report/README.md) (evidencias minimas; sem dumps massivos).

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

## Resultado esperado, telemetria e cleanup

Cada lab deve terminar com uma evidência reproduzível e não destrutiva. Registre
requisição, resposta, usuário de teste, horário UTC e limitação. Correlacione a
ação com logs HTTP/reverse proxy, logs da aplicação e eventos de autenticação;
explique pelo menos um falso positivo possível e uma mitigação verificável.

```bash
cd docker-lab
docker compose logs --since=10m <servico>
docker compose down -v
```

### Autoavaliação

- [ ] Concluí SQLi, XSS e BOLA somente nos alvos locais indicados.
- [ ] Diferenciei autenticação de autorização no achado de API.
- [ ] Coletei evidência mínima e removi tokens/dados desnecessários.
- [ ] Relacionei cada ação a uma fonte de telemetria e mitigação.
- [ ] Destruí volumes e confirmei que as portas do lab foram fechadas.


## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Metodologia OWASP para Pentest: Garantindo a Segurança das Aplicações Web](https://www.youtube.com/watch?v=DOQdWHtjMT4) — **Perícia Hacker**.
2. [OWASP TOP 10: As Falhas MAIS CRÍTICAS em Aplicações Web](https://www.youtube.com/watch?v=n8nI_IsH7rM) — **HackStation**.
3. [OWASP ASVS - O que é e como aumentar a segurança em Aplicações WEB #1](https://www.youtube.com/watch?v=BxeJgKalsiE) — **Sistema Inseguro**.
4. [Como utilizar o OWASP para realizar pentest](https://www.youtube.com/watch?v=ouERLpaCvbQ) — **Redbelt Security**.
5. [💀 TOP 10 Ameaças de Segurança em Aplicações Web - DICAS DE PREVENÇÃO!](https://www.youtube.com/watch?v=OzBy8nYLY-I) — **Código Fonte TV**.
=======

