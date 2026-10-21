# Web, HTTP, APIs e bancos de dados

Uma aplicação web é uma sequência de contratos: URL, resolução de nome,
conexão, HTTP, validação, regra de negócio, transação e representação da
resposta. Quando você enxerga essas fronteiras, deixa de tratar a web como uma
caixa-preta e consegue construir e depurar APIs com método.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- decompor uma URL e descrever o caminho do navegador até a aplicação;
- ler e produzir uma troca HTTP, incluindo método, status, cabeçalhos e corpo;
- escolher métodos e códigos de status de acordo com o contrato;
- modelar recursos, erros, paginação e compatibilidade de uma API;
- criar tabelas com chaves, constraints, relações e transações;
- executar CRUD parametrizado em SQLite;
- explicar quando um índice ajuda e qual custo ele adiciona;
- distinguir validação de interface de validação na fronteira confiável;
- localizar falhas por camada usando navegador, `curl`, logs e consultas.

Pré-requisitos: terminal, funções, dicionários/objetos, exceções e noções
de processos. O laboratório final usa o [TaskBoard](projetos/taskboard/README.md).

## 1. Anatomia de uma URL

Considere:

```text
http://127.0.0.1:8099/api/tasks?done=false&limit=20#resultado
```

| Parte | Valor | Função |
|-------|-------|--------|
| Esquema | `http` | protocolo e regras de comunicação |
| Host | `127.0.0.1` | máquina de destino; aqui, a própria máquina |
| Porta | `8099` | processo/serviço de destino no host |
| Caminho | `/api/tasks` | recurso dentro do serviço |
| Query | `done=false&limit=20` | parâmetros da requisição |
| Fragmento | `resultado` | navegação no cliente; não é enviado no HTTP |

Portas padrão são 80 para HTTP e 443 para HTTPS, mas desenvolvimento local
costuma usar portas altas. `localhost` normalmente resolve para loopback IPv4
(`127.0.0.1`) e/ou IPv6 (`::1`). Ele nunca significa “a máquina de outra pessoa”.

### Endereço de bind não é endereço de destino

- Um servidor ligado a `127.0.0.1` aceita conexões apenas da máquina local.
- Um servidor ligado a `0.0.0.0` escuta em todas as interfaces IPv4 disponíveis.
- Um cliente não acessa `0.0.0.0`; ele usa um endereço real do destino.
- Em container, a aplicação geralmente liga em `0.0.0.0`, enquanto a porta pode
  ser publicada apenas em `127.0.0.1` no host.

Essa distinção aparece no TaskBoard: a API escuta dentro do container, mas
somente o Nginx publica uma porta no host.

## 2. O caminho de uma requisição

Ao abrir uma URL HTTPS, de forma simplificada:

1. o navegador interpreta a URL;
2. consulta cache e DNS para resolver o host, quando ele não é um IP literal;
3. abre uma conexão de transporte ao IP e à porta;
4. em HTTPS, negocia TLS, valida o certificado e cria o canal protegido;
5. envia a mensagem HTTP;
6. proxy e servidor encaminham a operação para a aplicação;
7. a aplicação valida, executa a regra e acessa persistência;
8. a resposta percorre o caminho inverso;
9. o navegador interpreta HTML e solicita CSS, JavaScript, fontes e imagens;
10. JavaScript pode iniciar novas requisições com `fetch`.

HTTP descreve mensagens de aplicação. TCP, QUIC, TLS, DNS e roteamento possuem
responsabilidades diferentes. Um erro “HTTP 500” prova que houve uma resposta
HTTP; “connection refused” acontece antes de existir uma resposta HTTP.

```text
Navegador
   | HTTP :8099
   v
Nginx (arquivos estáticos + proxy)
   | HTTP na rede interna
   v
API (validação + regra)
   | SQL parametrizado
   v
SQLite (estado persistente)
```

## 3. HTTP por dentro

Uma requisição HTTP/1.1 possui linha inicial, cabeçalhos, linha vazia e,
opcionalmente, corpo:

```http
POST /api/tasks HTTP/1.1
Host: 127.0.0.1:8099
Content-Type: application/json
Accept: application/json
Content-Length: 24

{"title":"Estudar HTTP"}
```

Resposta correspondente:

```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: 83
Location: /api/tasks/1
Cache-Control: no-store

{"id":1,"title":"Estudar HTTP","done":false,"createdAt":"2026-10-03T12:00:00.000Z"}
```

- `Content-Type` descreve o corpo que está sendo enviado.
- `Accept` declara quais representações o cliente aceita.
- `Content-Length` mede bytes, não caracteres.
- `Location` aponta para o recurso criado.
- `Cache-Control: no-store` pede que a resposta não seja armazenada em cache.
- Cabeçalhos não substituem validação do corpo.

HTTP/2 e HTTP/3 codificam e transportam mensagens de forma diferente, mas os
conceitos de método, caminho, status, cabeçalhos e corpo continuam aplicáveis.

### Observe com `curl`

Com o TaskBoard em execução:

```bash
curl -i http://127.0.0.1:8099/api/tasks

curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Observar HTTP"}'

curl -sS http://127.0.0.1:8099/api/tasks
```

`-i` inclui os cabeçalhos da resposta. `-sS` remove o medidor de progresso, mas
mantém erros. Para depurar conexão e cabeçalhos enviados, use `curl -v`; leia a
saída antes de compartilhá-la, pois ela pode conter credenciais em outros
sistemas.

## 4. Semântica dos métodos

| Método | Intenção comum | Seguro? | Idempotente? |
|--------|------------------|---------|--------------|
| `GET` | obter representação | sim | sim |
| `HEAD` | obter apenas cabeçalhos | sim | sim |
| `POST` | criar/processar comando | não | geralmente não |
| `PUT` | substituir o recurso no URI | não | sim |
| `PATCH` | alterar parcialmente | não | depende do contrato |
| `DELETE` | remover | não | sim quanto ao estado final |

**Seguro** significa que a intenção não é alterar estado do recurso.
**Idempotente** significa que repetir a mesma requisição produz o mesmo estado
final, embora logs e timestamps possam mudar. Idempotência importa para retry.

Um `PATCH {"done": true}` é idempotente no TaskBoard porque repetir mantém
`done=true`. Um `PATCH {"increment": 1}` não seria.

Nunca use `GET /delete?id=7`: crawlers, prefetch e cache podem executar `GET`.

## 5. Códigos de status como parte do contrato

| Grupo | Significado | Exemplos relevantes |
|-------|-------------|---------------------|
| `2xx` | operação aceita | `200`, `201`, `204` |
| `3xx` | redirecionamento/cache | `301`, `304`, `307`, `308` |
| `4xx` | requisição não pode ser atendida como enviada | `400`, `401`, `403`, `404`, `409`, `413`, `415`, `422`, `429` |
| `5xx` | servidor/dependência falhou | `500`, `502`, `503`, `504` |

Distinções importantes:

- `200 OK`: resposta normal com corpo.
- `201 Created`: recurso criado; normalmente inclui `Location`.
- `204 No Content`: sucesso sem corpo; não tente decodificar JSON.
- `400 Bad Request`: sintaxe/formato da mensagem inválido.
- `401 Unauthorized`: autenticação ausente/inválida; o nome histórico confunde.
- `403 Forbidden`: identidade conhecida, mas operação não permitida.
- `404 Not Found`: recurso/rota não encontrado.
- `409 Conflict`: conflito com o estado atual, como versão desatualizada.
- `413 Content Too Large`: corpo excedeu o limite.
- `415 Unsupported Media Type`: servidor esperava outro `Content-Type`.
- `422 Unprocessable Content`: formato entendido, valor semanticamente inválido.
- `429 Too Many Requests`: limite de taxa excedido.
- `500 Internal Server Error`: defeito/falha inesperada; não use para entrada inválida.
- `502 Bad Gateway`: proxy recebeu resposta inválida ou não conectou ao upstream.
- `503 Service Unavailable`: serviço temporariamente indisponível.
- `504 Gateway Timeout`: proxy excedeu o tempo esperando o upstream.

O cliente deve usar o status para a classe do resultado e o corpo para detalhes
seguros e acionáveis.

## 6. Recursos e contratos de API

Modele substantivos como recursos:

```text
GET    /api/tasks          lista tarefas
POST   /api/tasks          cria tarefa
GET    /api/tasks/42       obtém uma tarefa
PATCH  /api/tasks/42       altera campos permitidos
DELETE /api/tasks/42       remove a tarefa
```

Uma API previsível define:

- IDs estáveis, nunca a posição atual na lista;
- tipos e campos obrigatórios/opcionais;
- tamanho máximo e normalização;
- formato de erro estável;
- ordenação, filtro e paginação;
- autenticação e autorização, se houver;
- timeout, idempotência e limite de taxa;
- compatibilidade e depreciação;
- logs e correlação sem dados sensíveis.

### Ausente, `null` e vazio não são sinônimos

No JSON abaixo, `apelido` existe sem valor, `nome` existe como texto vazio e
`email` não existe:

```json
{"apelido": null, "nome": ""}
```

Defina a semântica de cada caso. Em um `PATCH`, campo ausente costuma significar
“não alterar” e `null` pode significar “limpar”. Isso precisa estar documentado.

JSON possui objeto, array, string, número, booleano e `null`; não possui um tipo
próprio para data ou decimal monetário. Datas devem usar formato documentado,
normalmente ISO 8601 com fuso. Para dinheiro, escolha unidade inteira mínima ou
decimal com regras explícitas; ponto flutuante binário pode introduzir arredondamento.

### Paginação

Sem limite, uma lista cresce até consumir memória e tempo. Um contrato inicial:

```text
GET /api/tasks?limit=20&offset=40
```

Valide `1 <= limit <= 100`, imponha ordenação estável e devolva informação
suficiente para a próxima página. Offset é simples, mas pode ficar caro e mudar
sob inserções concorrentes. Cursor baseado na ordenação é mais estável em
grandes conjuntos.

## 7. HTML, CSS, DOM e JavaScript

HTML descreve estrutura e significado; CSS controla apresentação; JavaScript
coordena eventos e atualiza o DOM.

```html
<form id="task-form">
  <label for="title">Nova tarefa</label>
  <input id="title" name="title" required aria-describedby="title-help">
  <small id="title-help">Use de 1 a 120 caracteres.</small>
  <button type="submit">Adicionar</button>
</form>
<p id="message" role="status" aria-live="polite"></p>
<ul id="tasks"></ul>
```

`label`, `button` e `role="status"` oferecem significado, teclado e suporte a
tecnologias assistivas. Uma `div` clicável exigiria reimplementar semântica,
foco e teclado.

Um cliente mínimo:

```javascript
async function listTasks() {
  const response = await fetch("/api/tasks", {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const { tasks } = await response.json();
  const list = document.querySelector("#tasks");
  list.replaceChildren();

  for (const task of tasks) {
    const item = document.createElement("li");
    item.textContent = task.title;
    list.append(item);
  }
}
```

`fetch` resolve a promessa mesmo para `404` ou `500`; por isso verifique
`response.ok`. Ele rejeita para falhas de rede, cancelamento e alguns erros de
política do navegador. Use `textContent` para texto não confiável. Montar
`innerHTML` com entrada do usuário cria risco de injeção de HTML/script.

### Microprática: da página estática ao primeiro evento

Antes de modificar o TaskBoard, crie uma pasta com `index.html`, `styles.css` e
`app.js`. Use o formulário acima no HTML, carregue os outros arquivos com
`<link rel="stylesheet" href="styles.css">` e
`<script type="module" src="app.js"></script>`. Sirva somente em loopback:

```bash
python3 -m http.server --bind 127.0.0.1 8081
```

Evolua em três passos que podem ser verificados separadamente:

1. **HTML/CSS sem JavaScript:** navegue com `Tab`, associe cada `label` ao
   controle e confirme zoom de 200% sem perder conteúdo. CSS deve melhorar a
   apresentação, não substituir semântica HTML.
2. **Evento com dados sintéticos:** intercepte `submit`, use
   `event.preventDefault()`, normalize o texto, conte pontos de código Unicode
   com `[...texto].length`, aceite de 1 a 120, crie um `li` com `textContent` e
   limpe o campo. Teste vazio, espaços, 120 e 121 caracteres, incluindo emoji.
   Ainda não use `fetch`.
3. **Fronteira HTTP:** mantenha renderização e evento, mas troque a lista local
   pelo `fetch` mostrado acima quando a API estiver disponível. Acrescente
   estados visíveis de carregando, vazio e erro; um erro de rede não pode
   apagar a lista anterior silenciosamente.

Use as ferramentas do navegador: painel **Network** para a mensagem HTTP,
**Console** para exceções e **Elements** para estrutura/foco. Abrir o arquivo
diretamente como `file://` muda a origem e não reproduz o mesmo comportamento
de uma página HTTP.

### Mesma origem, CORS e CSRF

Uma origem é a combinação esquema + host + porta. O frontend e a API do
TaskBoard aparecem sob `http://127.0.0.1:8099`, pois o Nginx faz o proxy; isso
evita CORS no laboratório.

- **CORS** controla quais origens podem ler determinadas respostas no navegador.
  Não é autenticação nem firewall.
- **CSRF** explora credenciais que o navegador anexa automaticamente, como
  cookies. A defesa depende do modelo de autenticação (`SameSite`, token
  anti-CSRF e validação de origem são mecanismos comuns).
- **XSS** executa conteúdo não confiável como código no contexto da página;
  codificar saída e evitar sinks perigosos são controles centrais.

O TaskBoard não possui autenticação e foi projetado apenas para loopback local.

## 8. Modelo relacional

Uma tabela representa um conjunto de fatos com colunas tipadas. A chave
primária identifica uma linha; chave estrangeira relaciona fatos; constraints
protegem invariantes no banco.

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 120),
    done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
    created_at TEXT NOT NULL
);
```

A API ainda valida o título porque precisa produzir erro de domínio claro. A
constraint é a última defesa caso outro caminho tente gravar dados inválidos.

### Relação muitos-para-muitos

Livros podem ter vários autores e autores vários livros. Não armazene uma lista
de IDs separada por vírgula; use tabela associativa:

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE book_authors (
    book_id INTEGER NOT NULL REFERENCES books(id),
    author_id INTEGER NOT NULL REFERENCES authors(id),
    PRIMARY KEY (book_id, author_id)
);
```

Uma chave composta impede duplicar o mesmo par. No SQLite, declarar
`REFERENCES` não basta: a verificação de chaves estrangeiras deve ser ativada
em **cada conexão** com `PRAGMA foreign_keys = ON`, antes da transação. Confira
`PRAGMA foreign_keys`; o resultado deve ser `1`.

## 9. CRUD SQLite executável

Este exemplo cria um banco temporário, confirma duas tarefas e lista o resultado:

```python
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path


SCHEMA = """
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 120),
    done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
)
"""

with tempfile.TemporaryDirectory() as directory:
    db_path = Path(directory) / "tasks.db"
    with closing(sqlite3.connect(db_path)) as connection, connection:
        connection.execute(SCHEMA)
        connection.executemany(
            "INSERT INTO tasks (title) VALUES (?)",
            [("Ler sobre HTTP",), ("Praticar SQL",)],
        )
        connection.execute(
            "UPDATE tasks SET done = ? WHERE title = ?",
            (1, "Ler sobre HTTP"),
        )

        rows = connection.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()

    print(rows)
```

Saída esperada:

```text
[(1, 'Ler sobre HTTP', 1), (2, 'Praticar SQL', 0)]
```

Execute após salvar como `sqlite_demo.py`:

```bash
python3 sqlite_demo.py
```

### Parâmetros não são formatação de string

Inseguro e incorreto:

```python
query = f"SELECT id FROM tasks WHERE title = '{user_input}'"
```

Correto:

```python
row = connection.execute(
    "SELECT id FROM tasks WHERE title = ?",
    (user_input,),
).fetchone()
```

O driver envia instrução e valor separadamente. Aspas dentro do valor continuam
dados, não viram sintaxe SQL. O marcador varia por biblioteca; não invente um
por concatenação.

## 10. Transações e concorrência

Uma transação agrupa mudanças que devem ser confirmadas ou revertidas juntas.
No exemplo de transferência, debitar sem creditar deixaria o estado inconsistente.

```python
def transfer(connection, source_id: int, target_id: int, cents: int) -> None:
    if cents <= 0:
        raise ValueError("valor deve ser positivo")

    with connection:  # COMMIT no sucesso; ROLLBACK se houver exceção
        cursor = connection.execute(
            """
            UPDATE accounts
               SET balance_cents = balance_cents - ?
             WHERE id = ? AND balance_cents >= ?
            """,
            (cents, source_id, cents),
        )
        if cursor.rowcount != 1:
            raise ValueError("saldo insuficiente ou conta inexistente")

        cursor = connection.execute(
            "UPDATE accounts SET balance_cents = balance_cents + ? WHERE id = ?",
            (cents, target_id),
        )
        if cursor.rowcount != 1:
            raise ValueError("conta de destino inexistente")
```

Propriedades ACID, em linguagem prática:

- **atomicidade:** tudo ou nada;
- **consistência:** constraints e regras permanecem verdadeiras;
- **isolamento:** transações concorrentes não observam qualquer estado parcial;
- **durabilidade:** após confirmação, o banco preserva o resultado conforme sua
  configuração e garantias de armazenamento.

O nível de isolamento define quais interações concorrentes são permitidas.
“Consultar e depois inserir” em transações separadas cria uma janela de corrida.
Prefira constraint ou decisão atômica no banco quando a invariante depender de
concorrência.

No `sqlite3` do Python, `with connection:` controla commit/rollback, mas não
fecha a conexão. Feche explicitamente ou combine com `contextlib.closing`.

## 11. Índices e planos de consulta

Sem índice adequado, o banco pode examinar todas as linhas. Um índice mantém
estrutura auxiliar ordenada para acelerar certas buscas.

```sql
CREATE INDEX idx_tasks_done_id ON tasks(done, id);

EXPLAIN QUERY PLAN
SELECT id, title FROM tasks
WHERE done = 0
ORDER BY id
LIMIT 20;
```

A ordem das colunas importa. O índice `(done, id)` ajuda a filtrar `done` e
percorrer `id`; não é automaticamente ideal para uma busca apenas por `title`.

Custos de um índice:

- ocupa disco e cache;
- toda inserção/atualização relevante precisa mantê-lo;
- adiciona complexidade operacional;
- pode nunca ser escolhido pelo otimizador.

Crie a partir de consultas reais, volume representativo e plano medido. Em tabela
minúscula, varredura completa pode ser corretamente mais barata.

## 12. Relacional, documento, chave-valor e outros modelos

SQL e NoSQL não são níveis de maturidade; são famílias com trade-offs.

| Modelo | Força comum | Pergunta antes de escolher |
|--------|-------------|----------------------------|
| Relacional | relações, constraints, transações e consultas flexíveis | as invariantes atravessam entidades? |
| Documento | agregado JSON evolui como unidade | quais campos precisam de consulta/indexação? |
| Chave-valor | acesso simples por chave e baixa latência | como consultar algo sem conhecer a chave? |
| Grafo | travessias entre muitas relações | o problema central realmente é caminhar no grafo? |
| Séries temporais | eventos indexados por tempo | retenção e agregação temporal dominam? |

Não escolha tecnologia apenas por “escalar”. Defina consistência, padrões de
acesso, volume, latência, operação, backup e competência da equipe. O módulo 01
aprofunda bancos relacionais, não relacionais e APIs.

## 13. Cache e estado

HTTP é stateless no sentido de que cada requisição precisa ser compreensível
pelo servidor. A aplicação ainda pode manter estado em banco, sessão ou outro
serviço.

Cache exige responder:

1. qual é a chave?
2. por quanto tempo o valor é válido?
3. quem invalida depois de uma escrita?
4. dado obsoleto é aceitável por quanto tempo?
5. dado privado pode ser armazenado nessa camada?

`Cache-Control`, `ETag` e `If-None-Match` ajudam no cache HTTP. “Guardar para
sempre” não é estratégia de invalidação.

## 14. Segurança básica nas fronteiras

- limite tamanho do corpo antes de carregá-lo em memória;
- valide `Content-Type`, estrutura JSON, tipos, faixas e comprimento;
- normalize apenas com regra documentada; não “limpe” dados arbitrariamente;
- use SQL parametrizado e constraints;
- apresente texto não confiável com APIs seguras do DOM;
- não retorne stack trace, caminho interno ou SQL ao cliente;
- defina timeout em chamadas externas;
- aplique autenticação e autorização no servidor quando existirem identidades;
- limite taxa/custo de operações expostas;
- use HTTPS fora do loopback controlado;
- registre metadados suficientes sem guardar segredos e corpos sensíveis.

Validação não significa bloquear caracteres “especiais”. Significa aceitar a
estrutura prevista, manter dados como dados e codificar no contexto de saída.

## 15. Depuração por camada

Quando “a tela não carrega”, encontre a primeira fronteira quebrada:

1. **processo:** o serviço está executando?
2. **porta:** ele escuta no endereço esperado?
3. **HTTP:** `curl -i /health` recebe qual status?
4. **proxy:** health do gateway funciona, mas `/api/health` falha?
5. **contrato:** corpo e `Content-Type` estão corretos?
6. **aplicação:** logs mostram validação ou exceção?
7. **banco:** consulta e constraint aceitam o valor?
8. **frontend:** aba Network mostra request, status e resposta esperados?
9. **DOM:** Console mostra exceção após a resposta correta?

Tabela rápida:

| Sintoma | Camada provável | Primeira observação |
|---------|------------------|------------------------|
| `connection refused` | processo/bind/porta | processo e porta publicada |
| `404` | rota/caminho | linha da requisição e config do proxy |
| `415` | representação | `Content-Type` enviado |
| `422` | semântica da entrada | corpo e regra de validação |
| `502` no Nginx | upstream | saúde/log da API e DNS interno |
| `500` | aplicação/banco | log correlacionado, sem expor ao cliente |
| HTTP correto, tela errada | JavaScript/DOM | Network e Console do navegador |

## 16. Laboratório guiado com o TaskBoard

Suba o projeto seguindo o [guia operacional](projetos/taskboard/README.md) e
execute os experimentos na ordem.

### Nível 1: ler o protocolo

1. Execute `curl -i` em `/health`, `/api/health` e `/api/tasks`.
2. Identifique linha de status, `Content-Type`, `Content-Length` e corpo.
3. Crie uma tarefa e anote `Location`.
4. Remova a tarefa e confirme que `204` não possui corpo.

**Evidência:** arquivo Markdown com quatro trocas HTTP comentadas.

### Nível 2: provocar erros previstos

```bash
curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: text/plain' \
  --data 'texto'

curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  --data '{invalido'

curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  --data '{"title":"   "}'
```

Preveja antes de executar: `415`, `400` e `422`, respectivamente. Compare a
previsão com o resultado e localize no backend onde cada decisão ocorre.

### Nível 3: observar persistência

1. Crie duas tarefas.
2. Liste pela API.
3. Recrie apenas os containers sem remover volumes.
4. Liste novamente.
5. Explique por que o dado sobreviveu e onde está montado.

**Evidência:** comandos, saídas essenciais e diagrama navegador→Nginx→API→SQLite.

## 17. Exercícios

### Essenciais

1. Decomponha cinco URLs e diga se possuem a mesma origem.
2. Explique a diferença entre `Content-Type` e `Accept`.
3. Classifique dez operações como seguras/idempotentes.
4. Modele autores e livros com relação muitos-para-muitos.
5. Implemente CRUD parametrizado em um SQLite temporário.
6. Opere o formulário do TaskBoard somente com teclado.

### Intermediários

1. Defina um formato de erro com `code`, `message` e `requestId`.
2. Acrescente paginação a um contrato, incluindo limites e ordenação.
3. Use `EXPLAIN QUERY PLAN` antes e depois de um índice e registre a diferença.
4. Teste rollback provocando uma falha na segunda de duas escritas.
5. Explique por que validação HTML não protege uma API.
6. Modele `PATCH`: diferencie campo ausente, `null`, vazio e valor válido.

### Avançados

1. Modele atualização otimista com um campo de versão e erro `409`.
2. Implemente `ETag`/`If-None-Match` em um servidor de estudo.
3. Compare offset e cursor sob inserções concorrentes.
4. Defina threat model de uma API local que passará a ser exposta em rede.
5. Projete migração aditiva para tornar um novo campo obrigatório.

## Critério de conclusão

- [ ] Descrevo o caminho completo de uma requisição e separo falha de conexão de erro HTTP.
- [ ] Leio requisição e resposta brutas sem depender do navegador.
- [ ] Escolho método e status e justifico a semântica.
- [ ] Defino contrato para campos, limites, erros e paginação.
- [ ] Uso SQL parametrizado, constraints e transação corretamente.
- [ ] Explico o plano de uma consulta e o custo de um índice.
- [ ] Sei por que `textContent`, limites e validação do servidor importam.
- [ ] Localizo uma falha na primeira camada quebrada com evidência observável.
- [ ] Completei os três níveis do laboratório sem usar dados reais.
