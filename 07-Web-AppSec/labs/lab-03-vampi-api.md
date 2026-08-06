# Lab 03 — VAmPI API: BOLA / Auth Bypass (checklist)

> Lab guiado na API VAmPI (OWASP API Top 10) do docker-lab. Foque em **Broken Object Level Authorization (BOLA/IDOR)** e bypass de autenticacao/autorizacao. Sem dumps massivos nem abuso fora do lab.

**Teoria:** [../auth-bypass-patterns.md](../auth-bypass-patterns.md) · [../api-security-checklist.md](../api-security-checklist.md)

---

## Pre-requisitos

```bash
cd docker-lab
docker compose up -d
docker compose ps
```

| Item | Valor |
|------|--------|
| Base URL | http://127.0.0.1:8087 |
| Docs | Verifique `/` , `/docs` , `/openapi.json` ou Swagger exposto pela imagem |
| Ferramentas | `curl`, Bruno/Postman/Insomnia, ou Burp |
| Escopo | Somente `127.0.0.1:8087` |

Crie **duas contas de lab** distintas (User A e User B) sempre que o fluxo de registro existir — BOLA exige comparacao cross-user.

---

## Objetivos de aprendizado

1. Mapear a superficie da API VAmPI (rotas, auth, versoes).
2. Obter tokens/sessoes para dois usuarios de treino.
3. Percorrer um checklist pratico de BOLA e auth bypass.
4. Registrar achados no REPORT-TEMPLATE com request/response minimos (IDs de lab, sem PII real).

---

## Parte 0 — Recon da API

Execute e anote o que responder (paths podem variar por versao da imagem):

```bash
curl -sS http://127.0.0.1:8087/
curl -sS http://127.0.0.1:8087/openapi.json | head -c 500
# Se Swagger UI existir:
# abra http://127.0.0.1:8087/docs no browser
```

Checklist de mapeamento:

- [ ] OpenAPI/Swagger encontrado (ou rotas listadas na home)
- [ ] Prefixo de versao identificado (`/v1`, `/books`, `/users`, etc.)
- [ ] Metodo de auth identificado (JWT Bearer, API key, nenhum em alguns endpoints)
- [ ] Endpoints de registro / login / listagem anotados

Consulte tambem a secao "Coleta de Surface" em [../api-security-checklist.md](../api-security-checklist.md).

---

## Parte 1 — Autenticacao (baseline)

### Passos

1. Registre **User A** e **User B** pelos endpoints de signup do lab
2. Faca login com cada um; guarde os tokens em variaveis (nao commite tokens em git)

```bash
# Exemplo generico — ajuste path/JSON ao OpenAPI da sua instancia
TOKEN_A="..."
TOKEN_B="..."
```

3. Chame um endpoint "me" / perfil autenticado com `Authorization: Bearer $TOKEN_A`
4. Repita com token B e confirme identidades diferentes

### Checklist auth (pratico)

- [ ] Endpoint de login responde diferente para user inexistente vs senha errada? (enumeracao)
- [ ] Token JWT? Cole no [jwt.io](https://jwt.io) **offline/lab** ou use [`jwt_analyzer.py`](../../11-Python-Tools/jwt_analyzer.py) se disponivel
- [ ] Endpoint sensivel funciona **sem** `Authorization`?
- [ ] Token de A funciona em rota admin (se existir)?
- [ ] Metodos HTTP alternativos (`GET` vs `PUT`/`DELETE`) mudam a checagem de auth?

Documente apenas fatos observados no lab — sem bruteforce agressivo.

---

## Parte 2 — Checklist BOLA / IDOR

BOLA: User A acessa objeto de User B trocando o identificador.

### Preparacao

1. Com User A, crie ou localize um recurso proprio (livro, post, pedido — conforme VAmPI)
2. Anote o `id` do recurso A (`ID_A`)
3. Com User B, crie/localize recurso B (`ID_B`)

### Testes (marque cada item)

| # | Teste | Como | Resultado esperado seguro |
|---|-------|------|---------------------------|
| 1 | Ler objeto do outro | `GET /.../{ID_B}` com token A | 403/404 |
| 2 | Listar e filtrar | List endpoints; ver se vazam objetos de outros users | So objetos autorizados |
| 3 | Update cross-user | `PUT/PATCH` no `ID_B` com token A | 403/404 |
| 4 | Delete cross-user | `DELETE` no `ID_B` com token A (lab!) | 403/404 |
| 5 | ID previsivel | Sequencial? Tente `ID_B ± 1` | Negado |
| 6 | Body vs path | Path diz A, body diz `user_id=B` | Servidor ignora escalacao |
| 7 | Mass assignment | Enviar `"admin": true` / role no JSON de update | Campo ignorado |
| 8 | Sem auth | Mesmo GET de objeto **sem** token | 401 |

> Em lab, se o delete cross-user **funcionar**, pare apos a prova (um objeto de treino) e documente — nao limpe a base inteira.

### Modelo de request (ajuste ao OpenAPI real)

```bash
curl -sS -H "Authorization: Bearer $TOKEN_A" \
  "http://127.0.0.1:8087/<recurso>/$ID_B"
```

Anote status code e se o body trouxe dados de B.

---

## Parte 3 — Auth bypass patterns (API)

Percorra rapidamente (detalhes em [../auth-bypass-patterns.md](../auth-bypass-patterns.md)):

- [ ] Rota "admin" ou debug exposta sem auth
- [ ] Versao antiga da API (`/v1` vs `/v2`) com checagem mais fraca
- [ ] Headers de spoofing (`X-Original-URL`, `X-User-Id`) — so se a app parecer confiar neles
- [ ] JWT: `alg` / claims de role manipulaveis **no lab** (nao use secrets de producao)
- [ ] Parameter pollution / duplicata de `user_id`

Para cada hit: **um** request de prova, status, impacto em uma frase.

---

## Parte 4 — Documentar no REPORT-TEMPLATE

| Campo | Exemplo |
|-------|---------|
| Titulo | BOLA em `GET /<recurso>/{id}` (VAmPI lab) |
| Severidade | Alta (leitura/escrita cross-user) |
| OWASP API | API1:2023 Broken Object Level Authorization |
| MITRE | T1190 / abuso de credencial valida T1078 conforme caso |
| Passos | Criar users A/B; obter tokens; GET id de B com token A |
| Evidencia | Status 200 + trecho JSON com id de B (redija campos desnecessarios) |
| Impacto | User A leu/alterou recurso de User B |
| Remediacao | Authorization check por objeto no servidor; testes automatizados cross-tenant; IDs opacos nao bastam sozinhos |

### Evidencia minima

```text
User A token -> GET /<recurso>/<id_de_B> -> HTTP 200
Body contem identificador do recurso de B (lab).
Nao foi exportada a base completa.
```

---

## Criterios de sucesso

- [ ] VAmPI no ar em `:8087`
- [ ] Dois usuarios de lab com tokens
- [ ] Checklist BOLA percorrido (tabela) com resultados
- [ ] Pelo menos um achado BOLA **ou** auth bypass documentado (se a instancia for vulneravel por design — esperado)
- [ ] Relatorio sem dumps massivos

---

## Encerramento

```bash
cd docker-lab
docker compose down
```

Voltar ao fluxo do modulo: [../README.md](../README.md)

---

## Referencias

- [VAmPI](https://github.com/erev0s/VAmPI)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [docker-lab/README.md](../../docker-lab/README.md)
- [../api-security-checklist.md](../api-security-checklist.md)
- [REPORT-TEMPLATE.md](../../REPORT-TEMPLATE.md)
