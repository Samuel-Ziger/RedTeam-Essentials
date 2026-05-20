# Padroes de Bypass de Autenticacao & Autorizacao

> Compilacao de padroes recorrentes em pentests. Cada item tem detection hint, exemplo e mitigation.

---

## 1. SQL Injection no login

```http
POST /login
username=admin' --&password=anything
```

**Detection.** Time-based em campo de login (`admin' AND SLEEP(5) --`).

**Mitigation.** Prepared statements. Tambem: rate limit + logging diferencia "auth fail" de "DB error".

---

## 2. Header Spoofing

```http
GET /admin HTTP/1.1
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Original-URL: /admin
X-Rewrite-URL: /admin
```

Apps que confiam em headers reverse-proxy sem validar a fonte podem ser bypassadas.

**Mitigation.** Trust apenas o `X-Forwarded-For` do load balancer conhecido; assine headers internos.

---

## 3. JWT - bypass por algoritmo

- `alg: none` aceito.
- HS256 com chave fraca (use [`jwt_analyzer.py --bruteforce-secrets`](../11-Python-Tools/jwt_analyzer.py)).
- HS256 com chave publica como secret quando a app deveria validar com RS256.
- `kid` injection: `kid=../../../dev/null` -> chave vazia.
- `jku` ou `x5u` apontando para atacante.

**Mitigation.** `alg` whitelisted no servidor; valide JWK; nao confie em `kid` para path lookup.

---

## 4. OAuth2 / OIDC

- `redirect_uri` validado por `startsWith` -> use `https://attacker.com.alvo.com` ou `https://alvo.com.attacker.com`.
- Falta `state` -> CSRF no flow.
- Falta PKCE em public clients.
- Code reuse aceito (deve ser one-shot).
- Implicit flow ativo (deprecated, vaza token na URL).

**Mitigation.** PKCE obrigatorio, `redirect_uri` exact-match, `state`+`nonce` validados, code TTL <= 60s.

---

## 5. Cookies Mal Configurados

- Sem `Secure`: leaked em HTTP.
- Sem `HttpOnly`: roubado por XSS.
- Sem `SameSite=Lax/Strict`: CSRF.
- Cookie persistente vs sessao.

**Detection.** Burp Proxy + inspecao no DevTools.

---

## 6. Path-based Auth Bypass

```http
GET //admin
GET /./admin
GET /;/admin
GET /admin..;/
GET /admin/.
GET /admin/%20
GET /admin%2f
```

Front-end (Nginx/CDN) faz uma normalizacao, backend (Spring/Tomcat) outra. O middleware de auth pode estar so na borda.

**Mitigation.** Same path-parsing em todas as camadas. Defense-in-depth: auth tambem no backend.

---

## 7. Mass Assignment

```http
POST /signup
{"username":"alice","password":"...","isAdmin":true}
```

API aceita campos nao expostos no front. Tente sempre adicionar `role`, `isAdmin`, `tier`, `verified`.

**Mitigation.** Allowlist explicito de campos por endpoint (DTOs no Java/Python).

---

## 8. Race Conditions

- Aplicar mesmo cupom em paralelo: ganha credito multiplo.
- Pular MFA: race entre `verifyOTP` e `loginComplete`.
- Saque concorrente: saldo fica negativo.

**Tools.** Turbo Intruder (Burp) com `engine=Engine.BURP2` e `concurrentConnections=...`. Tambem `silver-burp-race-condition`.

**Mitigation.** Locks otimistas no DB, idempotency keys.

---

## 9. Session Fixation

Atacante define `JSESSIONID=ATTACKER` no browser da vitima (via XSS/MITM), vitima loga, atacante reusa o ID.

**Mitigation.** Sempre regenerate session ID apos login (`request.changeSessionId()` no Java, `session.regenerate()` no PHP).

---

## 10. Reset de Senha Quebrado

- Token previsivel (UUIDv1, MD5(email+timestamp), counter).
- Sem TTL.
- Pode trocar email/usuario no body sem revalidar token.
- Host header injection no email link (`Host: attacker.com`).

**Mitigation.** Token cripto-seguro (>=128 bits), TTL curto (15-30m), invalidado apos uso/troca.

---

## 11. Account takeover via OAuth pre-account

1. Atacante registra com email `victim@vitima.com` via OAuth com provider que nao verifica email (X, Discord).
2. Vitima depois registra com mesmo email via email/senha.
3. Provider confia no atacante -> takeover.

**Mitigation.** Forcar verificacao por email antes de qualquer privilegio.

---

## 12. IDOR / BOLA - Indirect

Mesmo com UUID, sometimes:
- IDs aparecem em JS embutido.
- IDs sao retornados em outras chamadas (`/api/users` para tier free retorna IDs do tier paid).
- ID pode ser localizado via fuzz (`/api/comments/{uuid}` se nao houver auth check, todos sao acessiveis).

---

## Checklist Express

- [ ] Login com SQLi/NoSQLi.
- [ ] User enumeration por mensagem ou timing.
- [ ] Brute force sem lockout.
- [ ] JWT analise estatica + bruteforce HS\*.
- [ ] OAuth flow: redirect_uri, state, PKCE, code reuse.
- [ ] Cookies: Secure/HttpOnly/SameSite.
- [ ] Headers: trust em XFF/XRI/Host.
- [ ] Path bypass: //, /;/, /admin..;/.
- [ ] Mass assignment (isAdmin, role).
- [ ] Race conditions em endpoints sensiveis.
- [ ] Reset de senha: TTL, single-use, host header.
- [ ] BOLA/IDOR cross-tenant.
- [ ] MFA bypass via API direta.

---

## Referencias

- [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [PortSwigger Auth Labs](https://portswigger.net/web-security/authentication)
- [Bugcrowd VRT](https://bugcrowd.com/vulnerability-rating-taxonomy)
