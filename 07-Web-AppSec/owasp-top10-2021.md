# OWASP Top 10 (2021) - Guia de Pentest

> Cada item: descricao curta, como detectar em pentest, exemplos praticos, MITRE ATT&CK, mitigacao.

---

## A01:2021 - Broken Access Control

**O que e.** Controles de acesso ausentes, fracos ou mal aplicados (BOLA/IDOR, falha de vertical/horizontal, force browsing).

**Como detectar (manual).**
- Trocar IDs em URLs e bodies (`/api/users/123` -> `/api/users/124`).
- Login com usuario "low" e tentar endpoints "admin".
- HTTP methods inesperados (`PUT/DELETE` onde so deveria haver `GET`).
- Bypass por cabecalho (`X-Original-URL`, `X-Forwarded-For`).

**Exemplos praticos.**

```http
GET /api/v1/orders/9000 HTTP/1.1
Authorization: Bearer <token-do-usuario-alvo-errado>
```

**Mitigacao.** Deny-by-default, RBAC/ABAC com checagem central, testes de regressao especificos para autorizacao.

**MITRE ATT&CK.** T1190, T1078.

---

## A02:2021 - Cryptographic Failures

**O que e.** Falhas que expoem dados sensiveis: TLS fraco, falta de criptografia em transito/repouso, hash sem sal, JWT alg=none.

**Como detectar.**
- `testssl.sh https://alvo`
- Inspecionar JWT (use `11-Python-Tools/jwt_analyzer.py`).
- Olhar cookies sem `Secure`/`HttpOnly`/`SameSite`.

**Mitigacao.** TLS 1.2+, HSTS, bcrypt/argon2 para senhas, KMS para chaves, criptografia em repouso.

---

## A03:2021 - Injection

**O que e.** SQLi, NoSQLi, LDAPi, OS command injection, SSTI, XPath injection.

**Como detectar.**
- Fuzz com `sqlmap`, `ffuf` carregando wordlists de [`12-Java-Tools/PayloadGenerator`](../12-Java-Tools/README.md).
- Time-based: `1' AND SLEEP(5) --` para SQL.
- Blind: bool delta entre `1' AND 1=1 --` e `1' AND 1=2 --`.

**Exemplo SSTI.**

```http
POST /render HTTP/1.1
template={{7*7}}
```

Se a resposta contiver `49`, o engine avaliou. Tente `{{config.items()}}` (Flask/Jinja2).

**Mitigacao.** Prepared statements / ORM com parametros, output encoding, allowlist de input, principle of least privilege no DB.

---

## A04:2021 - Insecure Design

**O que e.** Falhas na propria arquitetura - falta de threat modeling, ausencia de rate limit em endpoints sensiveis, designs que assumem cliente confiavel.

**Mitigacao.** Threat modeling (STRIDE, PASTA), security requirements antes do codigo, abuse cases por feature.

---

## A05:2021 - Security Misconfiguration

**O que e.** Default creds, debug endpoints expostos, headers de seguranca ausentes, mensagens de erro detalhadas, S3 buckets publicos.

**Como detectar.**
- Headers: `securityheaders.com` ou `nuclei -t http/misconfiguration/`.
- Debug: `/actuator/*` em Spring Boot, `/_debug` em Django, `/wp-json` em WordPress.

**Mitigacao.** Hardening baselines (CIS Benchmarks), config como codigo, scans automaticos.

---

## A06:2021 - Vulnerable and Outdated Components

**O que e.** Bibliotecas, frameworks ou serviços com CVE conhecido (Log4Shell, Spring4Shell, etc.).

**Como detectar.**
- SBOM + `trivy`, `grype`, `snyk`.
- `nuclei -t cves/`.
- Headers `Server`, `X-Powered-By` revelam versao.

**Mitigacao.** Inventario continuo, patch SLA, virtual patching via WAF.

---

## A07:2021 - Identification and Authentication Failures

**O que e.** Login com credentials weak, falta de MFA, session fixation, JWT mal validado, brute force sem lockout.

**Como detectar.**
- `hydra -L users -P passwords ...`
- Testar logout: token revalido?
- Token preditivel (UUIDv1 com timestamp, etc.).

**Mitigacao.** MFA obrigatorio, rate limit, lockout, password policies NIST 800-63B.

---

## A08:2021 - Software and Data Integrity Failures

**O que e.** Pipelines CI/CD sem verificacao, dependencias sem assinatura, deserializacao insegura.

**Como detectar.**
- Procurar `pickle.loads`, `ObjectInputStream.readObject`, `yaml.load` (Python sem `SafeLoader`).

**Mitigacao.** Sigstore, SLSA, dependency pinning + hash, sandboxing de deserialization.

---

## A09:2021 - Security Logging and Monitoring Failures

**O que e.** Logs incompletos, sem rotacao, sem alerta. Ataques bem-sucedidos passam despercebidos.

**Como detectar (red team).**
- Rode acoes ruidosas e veja se gera alerta.
- Verifique se logs registram IPs, user-agent, claims do JWT.

**Mitigacao.** SIEM + casos de uso (Sigma rules), retencao adequada, alertas correlacionados.

---

## A10:2021 - Server-Side Request Forgery (SSRF)

**O que e.** O servidor faz uma requisicao por ordem do atacante (URL parameter, webhook, image fetch).

**Como detectar.**
- Parametros tipo `url=`, `next=`, `redirect=`, `image=`.
- Tente `http://169.254.169.254/latest/meta-data/` (AWS), `http://metadata.google.internal/` (GCP), `http://[::]/`.
- Validar com OOB: usar Burp Collaborator ou requestbin/interactsh.

**Exemplo.**

```http
POST /api/preview HTTP/1.1
{"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
```

**Mitigacao.** Allowlist de dominios, resolver DNS server-side, bloqueio de RFC1918, IMDSv2 no AWS.

---

## Referencias

- [OWASP Top 10:2021](https://owasp.org/Top10/)
- [OWASP API Security Top 10:2023](https://owasp.org/API-Security/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/)
