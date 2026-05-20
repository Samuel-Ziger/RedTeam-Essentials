# API Security Checklist - Pentest REST & GraphQL

> Baseado em OWASP API Security Top 10 (2023) + experiencias de campo. Use durante engagements em APIs publicas e internas.

---

## 1. Coleta de Surface

- [ ] Subir todas as rotas via Burp Proxy + walkthrough do front-end.
- [ ] Buscar `swagger.json`, `openapi.json`, `/v1/api-docs`, `/graphql` (introspection).
- [ ] Procurar arquivos: `/.well-known/openid-configuration`, `/oauth2/.well-known/jwks.json`.
- [ ] JS analysis: extrair URLs com `linkfinder` ou `katana -jc`.
- [ ] Verificar versionamento: `/v1`, `/v2`, `/api/legacy`.

---

## 2. Autenticacao

- [ ] Endpoint de login: rate limit? Lockout? `username enumeration` por mensagem ou timing?
- [ ] Token: JWT? Cookie? Header? Onde e armazenado? (LocalStorage = expose to XSS).
- [ ] JWT: rodar [`jwt_analyzer.py`](../11-Python-Tools/jwt_analyzer.py).
- [ ] OAuth2/OIDC: state/PKCE presentes? `redirect_uri` validado estritamente?
- [ ] Reset de senha: token tem TTL? Pode reutilizar? E previsivel?
- [ ] MFA: obrigatorio? Bypass via API direta (`/api/v1/login` aceita sem fator)?

---

## 3. Autorizacao (API1:2023 BOLA / API5:2023 BFLA)

- [ ] Use 2 contas distintas (low e mid). Tente acessar recursos cross-tenant.
- [ ] Mude IDs em paths (`/orders/{id}`) e bodies (`"userId":`).
- [ ] UUID e melhor que int? Tente IDOR mesmo em UUIDs (chumbados no JS).
- [ ] HTTP methods alternativos (`PUT /users/me` -> mude `role` no payload).
- [ ] Mass assignment: campos sensiveis (`isAdmin`, `accountStatus`) sao ignorados ou aceitos?

---

## 4. Input Validation

- [ ] SQLi: try classic + time-based em campos de filtro/order/sort.
- [ ] NoSQL injection: `{"$ne": null}` ou `{"$gt": ""}` em campos de login MongoDB.
- [ ] SSRF: parametros que aceitam URL (webhook, avatar URL, fetch).
- [ ] SSTI: encontrar engines (`{{...}}`, `${...}`).
- [ ] File upload: tipo MIME, magic bytes, antivirus, path traversal no nome.

---

## 5. Rate Limit & DoS (API4:2023)

- [ ] Endpoints sem limite? (login, /search, /export).
- [ ] Resposta cresce O(n^2) com parametro `limit=100000`?
- [ ] Compressao habilitada com input controlavel? (zip bomb).
- [ ] GraphQL: query alias bombing, deeply nested queries.

---

## 6. GraphQL especifico

- [ ] Introspection habilitada em prod? (`{ __schema { types { name } } }`).
- [ ] Use [`graphw00f`](https://github.com/dolevf/graphw00f) para fingerprint.
- [ ] Batch queries / aliases (auth bypass: `query { a: login(...) b: login(...) }`).
- [ ] Mutations expostas (`deleteUser`, `setRole`) sem checagem de role.

---

## 7. Sessoes e Cookies

- [ ] Cookies: `Secure`, `HttpOnly`, `SameSite=Lax/Strict`, `__Host-` prefix.
- [ ] Logout invalida token server-side?
- [ ] CSRF: APIs com cookie-auth precisam de token CSRF ou `SameSite=Strict`.

---

## 8. Logging & Monitoring (API10:2023)

- [ ] PII em logs? (passwords, tokens, CPF).
- [ ] Tentativas falhas geram alerta? (login brute force).
- [ ] Endpoint de admin tem audit trail?

---

## 9. Hardening de transporte

- [ ] `testssl.sh https://api.alvo` - sem TLS < 1.2.
- [ ] HSTS preload.
- [ ] CORS: `Access-Control-Allow-Origin: *` com `Allow-Credentials: true`? (perigoso).

---

## 10. Cenarios de Negocio

- [ ] Webhook injection - servidor faz outbound para URL atacante-controlada.
- [ ] Race conditions - aplicar cupom 2x com requests paralelos.
- [ ] Time-of-check time-of-use (TOCTOU) em saldo, estoque, votos.

---

## Ferramentas

| Tarefa | Ferramenta |
|--------|------------|
| Proxy interceptador | Burp Suite Pro / Caido |
| Fuzz | ffuf, wfuzz, Burp Intruder |
| GraphQL | graphw00f, InQL, clairvoyance |
| JWT | jwt_tool, jwt_analyzer.py |
| OAuth | EvilOAuth, OAuth-Toolkit |
| Recon JS | linkfinder, katana, gospider |

---

## Saida do pentest

Use [`REPORT-TEMPLATE.md`](../REPORT-TEMPLATE.md) e inclua mapeamento ATT&CK por finding. Lembre-se de PoCs reproduziveis (curl/HTTP raw) e impacto de negocio.
