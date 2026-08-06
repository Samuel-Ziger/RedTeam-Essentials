# SQL Injection Deep Dive

> Guia educacional de SQL Injection para labs locais autorizados (`docker-lab`). Foco em detecção, classificação, sqlmap em ambiente controlado e defesa com parameterized queries. **MITRE ATT&CK: T1190 — Exploit Public-Facing Application.**

---

## Etica e escopo

- Execute apenas em alvos do `docker-lab` (DVWA `:8081`, WebGoat `:8084`) ou outros ambientes com autorização explícita.
- Não use dumps massivos de dados reais. Em lab, prove impacto com **contagem de linhas**, **versão do SGBD** ou **um registro sintético**.
- Rate-limit em ferramentas automatizadas; evite `sqlmap --dump` completo em bases de treino grandes sem necessidade pedagógica.
- Em engagements reais: escopo escrito, regras de engajamento e tratamento de PII conforme o contrato.

---

## 1. O que e SQL Injection

SQLi ocorre quando entrada do usuario e concatenada na query SQL sem separacao clara entre **codigo** e **dados**. O SGBD interpreta parte do input como SQL.

```text
Intentado:  SELECT * FROM users WHERE id = '1'
Injetado:   SELECT * FROM users WHERE id = '1' OR '1'='1'
```

Impacto tipico: leitura nao autorizada, bypass de autenticacao, alteracao/exclusao de dados, em alguns stacks RCE via funcoes do SGBD (raro e fora do escopo deste guia de lab).

**Mapeamento:**

| Framework | Referencia |
|-----------|------------|
| MITRE ATT&CK | T1190 |
| OWASP Top 10 2021 | A03:2021 — Injection |
| CWE | CWE-89 |

---

## 2. Tipos principais

### 2.1 In-band (a resposta volta no mesmo canal)

O resultado da injecao aparece na propria resposta HTTP (pagina, JSON, erro).

| Subtipo | Como funciona | Sinal no lab |
|---------|---------------|--------------|
| **Error-based** | Forca erro do SGBD que vaza dados/estrutura | Mensagem SQL na pagina |
| **Union-based** | Usa `UNION SELECT` para anexar resultado | Colunas extras na tabela/HTML |
| **Boolean / content** | Condicao verdadeira/falsa muda o HTML | Conteudo diferente para `AND 1=1` vs `AND 1=2` |

Payload classico de lab (DVWA Low):

```text
' OR '1'='1
```

### 2.2 Blind (sem vazamento direto do resultado)

A aplicacao nao mostra dados SQL, mas o comportamento muda.

| Subtipo | Canal de observacao | Exemplo conceitual (lab) |
|---------|---------------------|--------------------------|
| **Boolean-based blind** | Diferenca de conteudo/status | Condicao verdadeira retorna "existe"; falsa, "nao existe" |
| **Time-based blind** | Delay na resposta | Condicao verdadeira provoca `SLEEP`/`WAITFOR` controlado |

Fluxo tipico de time-based (apenas lab):

1. Confirmar baseline de latencia.
2. Injetar condicao com delay curto (ex.: 3–5 s).
3. Inferir bit a bit (caractere da versao, nome de tabela) — lento; use sqlmap com `--technique=T` no lab.

### 2.3 Out-of-band (OOB)

O SGBD inicia conexao externa (DNS/HTTP) para exfiltrar. Comun em ambientes restritos onde in-band e blind falham, mas o host do banco alcanca a rede.

- Em lab local puro, OOB e menos pratico (sem canal DNS externo). Entenda o conceito; nao dependa dele no `docker-lab`.
- Em engagements reais, OOB exige autorizacao clara (infra do cliente + seu listener).

### 2.4 Second-order

O payload e armazenado "seguro" e so e interpretado como SQL em outro fluxo (relatorio, job, admin). Teste: injete em cadastro e acione a feature que reusa o valor em query.

---

## 3. Deteccao (manual, lab-first)

### 3.1 Onde procurar

- Parametros GET/POST (`id`, `user`, `sort`, `order`, `search`).
- Headers pouco validados (`X-Forwarded-For` em logs SQL — raro).
- Cookies usados em queries.
- GraphQL/REST com filtros (`filter`, `q`).

### 3.2 Sondas seguras de lab

Comece com quebras sintaticas leves e observe erros ou mudancas:

```text
'
"
')
'--
' OR '1'='1
' AND '1'='1
' AND '1'='2
```

Checklist de observacao:

- [ ] Erro SQL / stack trace
- [ ] Diferenca de HTML entre condicao T/F
- [ ] Tempo de resposta (time-based)
- [ ] Mudanca de status HTTP
- [ ] Login bem-sucedido sem credencial valida (auth bypass)

### 3.3 Identificar SGBD (lab)

Sinais uteis (mensagens de erro, sintaxe):

| SGBD | Hint tipico |
|------|-------------|
| MySQL/MariaDB | `You have an error in your SQL syntax` |
| PostgreSQL | `ERROR: syntax error at or near` |
| MSSQL | `Unclosed quotation mark` / `Microsoft OLE DB` |
| SQLite | `unrecognized token` / `SQLITE_ERROR` |

DVWA usa MySQL/MariaDB no stack padrao do container.

### 3.4 Contar colunas (union-based, lab)

Abordagem educacional em DVWA Low:

1. Confirmar injecao com `' OR '1'='1`.
2. Descobrir numero de colunas com `ORDER BY N` incrementando N ate falhar, **ou** `UNION SELECT NULL,NULL,...`.
3. Localizar colunas refletidas na pagina.
4. Extrair metadados de lab (ex.: versao) — **nao** dump completo de usuarios reais.

---

## 4. sqlmap basics (apenas lab)

> Pre-req: `docker-lab` no ar; cookie de sessao DVWA; security level conhecido.

### 4.1 Preparacao DVWA

```bash
cd docker-lab && docker compose up -d
# Browser: http://127.0.0.1:8081
# Login padrao do lab: admin / password
# Setup/Create DB se pedido; Security -> Low
```

Capture `PHPSESSID` e cookie `security=low` no DevTools ou Burp.

### 4.2 Comandos basicos (lab)

Substitua o cookie pelo da sua sessao. Prefira a rede do compose a partir do container `attacker`, ou `127.0.0.1` no host.

```bash
# Deteccao + fingerprint (sem dump)
sqlmap -u "http://127.0.0.1:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="security=low; PHPSESSID=SEU_COOKIE" \
  --batch --level=1 --risk=1 \
  --technique=BEUST \
  --dbs

# Apenas banners / versao
sqlmap -u "http://127.0.0.1:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="security=low; PHPSESSID=SEU_COOKIE" \
  --batch --banner --current-db --current-user
```

Boas praticas no lab:

| Flag / habito | Por que |
|---------------|---------|
| `--batch` | Menos prompts interativos |
| `--level` / `--risk` baixos primeiro | Menos ruido |
| `--threads` baixo (1–2) | Nao sobrecarregar o container |
| Evitar `--dump` completo | Prova com `--banner` / contagem |
| `--tamper` so se filtro exigir | Medium DVWA bloqueia espacos |

Exemplo conceitual Medium (espacos filtrados) — sqlmap pode usar tamper de espaco; prefira tambem entender o bypass manual (comentarios `/**/` no lugar de espaco) antes de automatizar.

### 4.3 WebGoat (Java)

```text
URL: http://127.0.0.1:8084/WebGoat
```

Siga as licoes de SQL Injection do WebGoat: o objetivo e completar o challenge educacional, nao vazar dados externos. Documente a licao, o parametro vulneravel e a prova minima (mensagem de sucesso / flag de lab).

---

## 5. Exercicios guiados no docker-lab

### Exercicio A — DVWA SQLi Low

1. Suba o lab: `cd docker-lab && docker compose up -d`.
2. Acesse http://127.0.0.1:8081 — login lab, Security **Low**.
3. Menu **SQL Injection**.
4. Teste `' OR '1'='1` e observe multiplos usuarios de treino.
5. Documente no [REPORT-TEMPLATE](../REPORT-TEMPLATE.md): request, evidencia (screenshot redactado), impacto, remediacao.
6. Lab completo: [labs/lab-01-dvwa-sqli.md](labs/lab-01-dvwa-sqli.md).

### Exercicio B — DVWA SQLi Medium

1. Security **Medium**.
2. Observe que o input e `POST` / dropdown — ainda injete via Burp interceptando o body.
3. Note filtros simples (ex.: espaco). Experimente `/**/` ou quebras que o filtro nao cobre.
4. Compare com Low: mesma classe, superficie diferente.

### Exercicio C — WebGoat SQLi

1. http://127.0.0.1:8084/WebGoat — crie usuario de lab.
2. Complete uma licao de SQL Injection (String / Numeric conforme o curriculum atual).
3. Anote: tipo (in-band/blind), parametro, prova sem dump massivo.

### Exercicio D — sqlmap fingerprint only

Rode sqlmap com `--banner --current-db` (sem `--dump`). Anexe ao relatorio apenas metadados de lab.

---

## 6. Defesa: parameterized queries

### 6.1 Principio

Separe SQL da entrada: o SGBD recebe a query com placeholders e os valores em canal separado (bind).

**PHP (PDO):**

```php
$stmt = $pdo->prepare('SELECT first_name, surname FROM users WHERE user_id = :id');
$stmt->execute(['id' => $userId]);
$rows = $stmt->fetchAll();
```

**Python:**

```python
cur.execute("SELECT first_name, surname FROM users WHERE user_id = %s", (user_id,))
```

**Java (PreparedStatement):**

```java
PreparedStatement ps = conn.prepareStatement(
    "SELECT first_name, surname FROM users WHERE user_id = ?");
ps.setString(1, userId);
ResultSet rs = ps.executeQuery();
```

**Node (pg):**

```javascript
const res = await client.query(
  'SELECT first_name, surname FROM users WHERE user_id = $1',
  [userId]
);
```

### 6.2 Armadilhas

- Concatenar nomes de coluna/`ORDER BY` com input do usuario **mesmo** com prepared statements — use whitelist de colunas.
- Escapar manualmente com `addslashes` / replace de aspas — fragil; nao e substituto de bind.
- ORM mal usado: raw queries (`queryRaw`, `execute`) com interpolacao.
- Stored procedures que montam SQL dinamico interno.

### 6.3 Controles complementares

| Controle | Papel |
|----------|-------|
| Menor privilegio no DB | App nao usa conta `root`/`sa` |
| WAF / input validation | Defesa em profundidade, nao unica |
| Logging de erros SQL | Sem stack trace para o cliente |
| Allowlist em sort/filter | Evita injecao em clausulas dinamicas |
| Testes SAST/DAST + code review | Catch em CI |

### 6.4 Exemplo inseguro vs seguro

```php
// INSEGURO (nao use)
$id = $_GET['id'];
$query = "SELECT * FROM users WHERE user_id = '$id'";
mysqli_query($conn, $query);

// SEGURO
$stmt = $conn->prepare('SELECT user_id, first_name, surname FROM users WHERE user_id = ?');
$stmt->bind_param('s', $id);
$stmt->execute();
```

---

## 7. Como reportar (REPORT-TEMPLATE)

Preencha a secao de achados com:

1. **Titulo:** SQL Injection em parametro `id` (DVWA lab).
2. **Severidade:** Critica/Alta (contexto lab: demonstre impacto).
3. **CVSS / narrativa:** leitura nao autorizada de registros de treino.
4. **Passos de reproducao:** URL, metodo, cookie `security`, payload minimo.
5. **Evidencia:** screenshot ou trecho de response **sem** colar dumps longos / senhas.
6. **Causa raiz:** concatenacao de string na query.
7. **Remediacao:** prepared statements + least privilege + testes.
8. **MITRE:** T1190.

Evite anexar: dumps CSV completos, hashes de senha reais, PII.

---

## 8. Checklist rapido de pentest (lab)

- [ ] Mapear parametros refletidos em queries
- [ ] Sondas `'` / boolean T-F
- [ ] Classificar: in-band / blind / (OOB se aplicavel)
- [ ] Confirmar SGBD
- [ ] Prova minima (banner / count / um registro lab)
- [ ] sqlmap fingerprint com cookie de sessao
- [ ] Testar Medium/filtros (bypass educacional)
- [ ] Documentar remediacao com exemplo de codigo seguro
- [ ] Limpar sessao / `docker compose down` se necessario

---

## 9. Lab map

| Alvo | URL | Uso |
|------|-----|-----|
| DVWA | http://127.0.0.1:8081 | SQLi Low/Medium (PHP/MySQL) |
| WebGoat | http://127.0.0.1:8084/WebGoat | Licoes Java / SQLi |
| Juice Shop | http://127.0.0.1:8082 | Challenges (SQLi em score board — opcional) |
| VAmPI | http://127.0.0.1:8087 | API; SQLi pode aparecer em endpoints de filtro |

Guia passo a passo: [labs/lab-01-dvwa-sqli.md](labs/lab-01-dvwa-sqli.md).

---

## Referencias

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)
- [sqlmap docs](https://github.com/sqlmapproject/sqlmap/wiki)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
- [DVWA](https://github.com/digininja/DVWA) / [WebGoat](https://github.com/WebGoat/WebGoat)
- Lab local: [docker-lab/README.md](../docker-lab/README.md)
