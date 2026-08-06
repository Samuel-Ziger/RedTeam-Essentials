# Lab 01 — DVWA SQL Injection (Low → Medium)

> Lab guiado, passo a passo, **apenas** no docker-lab local. Objetivo: entender SQLi in-band, diferenca Low vs Medium, e documentar no REPORT-TEMPLATE sem dumps massivos.

**Teoria:** [../sqli-deep-dive.md](../sqli-deep-dive.md) · **MITRE:** T1190

---

## Pre-requisitos

- Docker Engine + Compose plugin
- Repo clonado; pasta `docker-lab/`
- Navegador + (recomendado) Burp Community/Pro ou DevTools
- Opcional: `sqlmap` no host ou no container `rte-attacker`

```bash
cd docker-lab
docker compose up -d
docker compose ps
```

| Item | Valor |
|------|--------|
| URL | http://127.0.0.1:8081 |
| Credenciais lab | `admin` / `password` (padrao DVWA) |
| Escopo | Somente `127.0.0.1:8081` neste exercicio |

> Se a porta estiver ocupada, ajuste no `docker-compose.yml` local — nao exponha o container na Internet.

---

## Objetivos de aprendizado

Ao final voce deve ser capaz de:

1. Configurar DVWA (DB + security level).
2. Explorar SQLi **Low** com payload classico de lab e interpretar o resultado.
3. Adaptar o ataque em **Medium** (POST / filtro simples) via proxy.
4. Produzir evidencias minimas (sem dump completo de tabelas).
5. Preencher um achado no [REPORT-TEMPLATE.md](../../REPORT-TEMPLATE.md).

---

## Parte 0 — Setup DVWA

1. Abra http://127.0.0.1:8081
2. Login com `admin` / `password`
3. Se pedido, va em **Setup / Reset DB** e clique para criar o banco de lab
4. Menu **DVWA Security** → escolha **Low** → Submit
5. Confirme o cookie `security=low` (DevTools → Application → Cookies)

---

## Parte 1 — SQL Injection Low

### Passos

1. Menu **SQL Injection**
2. No campo User ID, envie um valor legitimo de lab, ex.: `1` — observe a resposta (nome de usuario de treino)
3. Envie a sonda de aspas: `'`
   - Anote se aparece erro SQL ou pagina em branco/diferente
4. Envie o payload classico de lab:

```text
' OR '1'='1
```

5. Observe: a pagina lista **varios** usuarios de treino (prova de injecao in-band)
6. (Opcional) Identifique o SGBD pela mensagem de erro da sonda `'`
7. (Opcional) Com sqlmap, apenas fingerprint — **sem** `--dump`:

```bash
sqlmap -u "http://127.0.0.1:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="security=low; PHPSESSID=SEU_COOKIE" \
  --batch --banner --current-db --current-user
```

### O que NAO fazer

- Nao rode `--dump` de todas as tabelas "por curiosidade"
- Nao cole hashes/senhas longas no relatorio — diga "N usuarios de treino retornados" ou mostre **um** registro redactado
- Nao aponte sqlmap para outros hosts

### Checkpoint Low

- [ ] Payload `' OR '1'='1` retorna multiplos registros de lab
- [ ] Voce anotou URL, metodo GET, parametro `id`, cookie `security=low`
- [ ] Evidencia: screenshot com dados de treino (pode ocultar campos extras)

---

## Parte 2 — SQL Injection Medium

### Passos

1. **DVWA Security** → **Medium** → Submit
2. Volte em **SQL Injection** — a UI muda (tipicamente dropdown / POST)
3. Selecione um ID valido e envie; capture o request no Burp (Intercept ou HTTP history)
4. Observe: o parametro ainda vai no body (ex.: `id=1`). O frontend limita opcoes, mas o servidor pode aceitar valores alterados
5. No Burp, altere o body para incluir injecao de lab, por exemplo:

```text
id=1+OR+1=1&Submit=Submit
```

ou, se o filtro remover espacos, experimente variantes educacionais documentadas no [sqli-deep-dive.md](../sqli-deep-dive.md) (ex.: comentarios `/**/` no lugar de espaco).

6. Compare resultados com Low: mesma classe de vulnerabilidade, controles de UI/filtro insuficientes
7. Anote qual filtro voce observou (se houver) e como o bypass de lab funcionou **em alto nivel**

### Checkpoint Medium

- [ ] Request POST interceptado e modificado
- [ ] Injecao confirmada sem depender do dropdown
- [ ] Diferenca Low vs Medium descrita em 2–3 frases

---

## Parte 3 — Documentar no REPORT-TEMPLATE

Use a secao **Achados Detalhados**. Sugestao de campos:

| Campo | Exemplo de conteudo (lab) |
|-------|---------------------------|
| Titulo | SQL Injection no parametro `id` (DVWA) |
| Severidade | Critica (lab) / Alta |
| Componente | `http://127.0.0.1:8081/vulnerabilities/sqli/` |
| MITRE | T1190 |
| Passos | Security Low; GET `id`; payload `' OR '1'='1`; repetir Medium via POST |
| Evidencia | Screenshot ou trecho HTML com 1–2 linhas de resultado de treino |
| Impacto | Leitura nao autorizada de registros da aplicacao de lab |
| Causa raiz | Concatenacao de input na query SQL |
| Remediacao | Prepared statements / PDO bind; least privilege no MySQL; testes |

### Texto minimo de evidencia (modelo)

```text
Requisicao: GET /vulnerabilities/sqli/?id=...&Submit=Submit
Cookie: security=low; PHPSESSID=<redatado>
Resultado: resposta listou multiplos usuarios de treino (prova de SQLi in-band).
Nao foi realizado dump completo da base.
```

---

## Criterios de sucesso

- [ ] Lab subiu com `docker compose up -d`
- [ ] Low explorado com payload classico
- [ ] Medium explorado via proxy
- [ ] Achado escrito no template **sem** dump massivo
- [ ] Remediacao mencionada (parameterized queries)

---

## Encerramento

```bash
# Opcional: derrubar o lab apos o treino
cd docker-lab
docker compose down
```

Proximo lab sugerido: [lab-02-juice-xss.md](lab-02-juice-xss.md) ou teoria [../ssrf-deep-dive.md](../ssrf-deep-dive.md).

---

## Referencias

- [DVWA](https://github.com/digininja/DVWA)
- [docker-lab/README.md](../../docker-lab/README.md)
- [REPORT-TEMPLATE.md](../../REPORT-TEMPLATE.md)
