# TaskBoard — laboratório integrador full stack

TaskBoard é pequeno o bastante para ser compreendido por inteiro e completo o
suficiente para mostrar uma requisição atravessando navegador, proxy, API,
validação, transação e banco. Ele usa somente HTML, CSS, JavaScript e biblioteca
padrão do Python; Docker e Nginx montam a aplicação completa.

> **Escopo seguro:** execute apenas localmente, com dados fictícios. O projeto
> não possui autenticação, autorização ou TLS e não deve ser publicado em uma
> interface externa, VPS ou internet.

## O que você aprenderá

Ao concluir o laboratório, você deverá conseguir:

- explicar cada componente e cada fronteira da aplicação;
- rastrear criação, listagem, conclusão e remoção de uma tarefa;
- prever status e corpo para entradas válidas e inválidas;
- diferenciar validação do navegador, API e constraint SQL;
- executar testes da API sem Docker;
- construir e operar o conjunto com Compose;
- diagnosticar processo, porta, proxy, DNS, permissão e banco por evidência;
- provar que containers não rodam como root e que a API não publica porta;
- provar persistência, criar backup e testar restauração;
- implementar uma evolução vertical com teste e migração.

Tempo sugerido:

- leitura e mapeamento: 2–3 horas;
- testes e operação base: 2–4 horas;
- diagnóstico e backup: 2–4 horas;
- primeira evolução: 6–12 horas.

## 1. Arquitetura executada

```text
Navegador ou curl
        |
        | HTTP http://127.0.0.1:8099
        v
+---------------- gateway ----------------+
| Nginx :8080                             |
|  /          -> HTML/CSS/JavaScript      |
|  /health    -> health do próprio Nginx  |
|  /api/*     -> proxy                    |
+-------------------+---------------------+
                    |
                    | HTTP para api:8000
                    | rede Docker backend
                    v
+------------------ api ------------------+
| Python ThreadingHTTPServer              |
| roteamento + JSON + validação         |
| funções de persistência               |
+-------------------+---------------------+
                    |
                    | SQL parametrizado
                    v
+--------------- persistência ------------+
| SQLite /data/tasks.db                   |
| volume Docker task-data                 |
+-----------------------------------------+
```

O gateway é o único ponto publicado. A API participa apenas da rede interna
`backend`. O navegador não precisa conhecer a porta 8000: chama `/api/...` na
mesma origem da página e o Nginx encaminha.

### Fronteiras de confiança

```text
entrada não confiável
    -> navegador (usabilidade, não segurança)
    -> Nginx (limite inicial de corpo/tempo)
    -> API (validação autoritativa e contrato)
    -> SQLite (constraints e atomicidade)
```

Cada camada preserva sua responsabilidade. O atributo HTML `required` pode ser
ignorado por um cliente HTTP; por isso a API valida. A constraint do banco
protege contra outro caminho de escrita; por isso a API e o banco validam.

## 2. Mapa do projeto

```text
taskboard/
|-- compose.yaml
|-- README.md
|-- api/
|   |-- .dockerignore
|   |-- Dockerfile
|   |-- server.py
|   `-- test_server.py
`-- web/
    |-- .dockerignore
    |-- Dockerfile
    |-- nginx.conf
    |-- index.html
    |-- styles.css
    |-- taskboard-core.mjs
    |-- taskboard-core.test.mjs
    `-- app.js
```

| Arquivo | Responsabilidade |
|---------|------------------|
| [`compose.yaml`](compose.yaml) | monta serviços, redes, volume, health e limites |
| [`api/server.py`](api/server.py) | HTTP, validação e persistência SQLite |
| [`api/test_server.py`](api/test_server.py) | testes de funções e ciclo HTTP real local |
| [`api/Dockerfile`](api/Dockerfile) | imagem da API sem privilégio |
| [`web/index.html`](web/index.html) | estrutura semântica e formulário |
| [`web/app.js`](web/app.js) | chamadas HTTP, eventos e DOM |
| [`web/taskboard-core.mjs`](web/taskboard-core.mjs) | regras puras de título e paginação |
| [`web/taskboard-core.test.mjs`](web/taskboard-core.test.mjs) | testes Node.js do contrato do frontend |
| [`web/styles.css`](web/styles.css) | apresentação e estados visuais |
| [`web/nginx.conf`](web/nginx.conf) | arquivos estáticos, health e proxy |
| [`web/Dockerfile`](web/Dockerfile) | imagem do gateway Nginx sem root |

Antes de executar, leia os arquivos nesta ordem: `compose.yaml`, `nginx.conf`,
`server.py`, `test_server.py`, `index.html`, `app.js` e os Dockerfiles.

## 3. Modelo de dados e invariantes

Schema real:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 120),
    done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tasks_done_id ON tasks(done, id DESC);

CREATE TABLE IF NOT EXISTS taskboard_meta (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    revision INTEGER NOT NULL CHECK (revision >= 0)
);

INSERT OR IGNORE INTO taskboard_meta (id, revision) VALUES (1, 0);
```

| Campo | Contrato |
|-------|----------|
| `id` | inteiro gerado pelo SQLite e estável |
| `title` | texto normalizado com 1–120 pontos de código Unicode |
| `done` | `0/1` no SQLite, booleano no JSON |
| `created_at` | texto ISO 8601 em UTC, milissegundos e sufixo `Z` |

`taskboard_meta` possui uma única linha. Sua `revision` aumenta na mesma
transação de cada criação, alteração ou remoção e identifica a versão lógica
da coleção usada pela paginação.

`normalize_title`:

1. exige `str`;
2. divide por whitespace e junta com um espaço;
3. exige comprimento entre 1 e 120 pontos de código Unicode;
4. devolve a forma normalizada.

Assim, `"  Estudar   HTTP\n"` vira `"Estudar HTTP"`. Isso é uma decisão de
produto: espaços internos repetidos não são preservados.

### Representação JSON

```json
{
  "id": 1,
  "title": "Estudar HTTP",
  "done": false,
  "createdAt": "2026-10-03T12:00:00.000Z"
}
```

O banco usa `created_at`; a API expõe `createdAt`. `serialize` é a fronteira que
converte nome e tipo (`0/1` para booleano).

A coleção sempre inclui metadados de página:

```json
{
  "tasks": [],
  "page": {
    "limit": 25,
    "offset": 0,
    "total": 0,
    "hasMore": false,
    "revision": 0
  }
}
```

## 4. Contrato HTTP completo

### Endpoints

| Método e caminho na API | Corpo | Sucesso |
|--------------------------|-------|---------|
| `GET /health` | nenhum | `200`, liveness do processo |
| `GET /ready` | nenhum | `200`, API e SQLite prontos |
| `GET /api/tasks?limit=25&offset=0&done=false` | nenhum | `200`, tarefas e metadados, incluindo `revision` |
| `GET /api/tasks/:id` | nenhum | `200`, uma tarefa |
| `POST /api/tasks` | `{"title":"..."}` | `201`, tarefa e `Location` |
| `PATCH /api/tasks/:id` | `{"title":"...","done":true}` | `200`, campos fornecidos atualizados |
| `DELETE /api/tasks/:id` | nenhum | `204`, sem corpo |
| `HEAD` nas rotas de leitura | nenhum | mesmos status/cabeçalhos de `GET`, sem corpo |
| `OPTIONS` em rota conhecida | nenhum | `204` e cabeçalho `Allow` |

Na coleção, `limit` aceita 1–100 (padrão 25), `offset` aceita 0–1.000.000
(padrão 0) e `done` aceita exatamente `true` ou `false`. A primeira página
devolve `revision`; páginas seguintes enviam esse inteiro no parâmetro opcional
`revision`. Se a coleção mudar entre requests, a API responde `409 stale_page`
para o cliente reiniciar da primeira página, evitando lacunas ou duplicatas
silenciosas do offset. Parâmetros desconhecidos ou repetidos são rejeitados; a
ordenação é por ID decrescente.

O `PATCH` aceita `title`, `done` ou ambos e exige ao menos um. Campos JSON
desconhecidos são rejeitados. Pelo gateway, `/api/health` e `/api/ready` são
reescritos para `/health` e `/ready` no upstream. `/health` do gateway devolve
`204` diretamente e não prova que a API ou o banco funcionam.

### Cabeçalhos e limites

- Escritas JSON exigem `Content-Type: application/json`; parâmetro como
  `charset=utf-8` é aceito porque o servidor compara o media type antes do `;`.
- Exatamente um `Content-Length` decimal é exigido; corpo aceita 1–16.384 bytes.
- `Transfer-Encoding` não é aceito por este servidor didático.
- `GET`, `HEAD`, `DELETE` e `OPTIONS` rejeitam corpo. Quando o framing declara
  bytes que não serão consumidos, a API responde erro e fecha explicitamente a
  conexão antes de qualquer efeito de domínio; assim esses bytes não podem ser
  reinterpretados como outro request HTTP/1.1 persistente.
- JSON exige UTF-8, objeto na raiz, chaves únicas, escalares Unicode válidos e
  não aceita `NaN`/`Infinity` nem surrogates isolados.
- Respostas JSON usam UTF-8, `Content-Length`, `Cache-Control: no-store`,
  `X-Content-Type-Options: nosniff` e `X-Request-ID`.
- Um `X-Request-ID` do cliente só é preservado se tiver 8–64 caracteres do
  conjunto ASCII documentado; caso contrário, a API gera outro.
- Criação inclui `Location: /api/tasks/:id`.
- Resposta `204` não possui corpo.
- A conexão recebe timeout de leitura de 10 segundos. Se o cliente interromper
  o envio de um corpo, a API responde `408 request_timeout`, fecha a conexão e
  não reaproveita bytes residuais como outro request.

Erro possui envelope estável e correlação:

```json
{
  "error": {
    "code": "invalid_title_length",
    "message": "title deve ter entre 1 e 120 caracteres após normalização",
    "requestId": "e7c5f27af6cc4ba2a731a3d4f4c223b1",
    "details": {"field": "title", "minLength": 1, "maxLength": 120}
  }
}
```

`details` é opcional; clientes devem decidir pelo `status` e `code`, não analisar
texto humano de `message`.

### Matriz de erro implementada

| Situação | Status | Corpo JSON |
|----------|--------|------------|
| rota/ID sintaticamente inválido ou tarefa ausente | `404` | `route_not_found` ou `task_not_found` |
| qualquer método não permitido em rota conhecida | `405` | `method_not_allowed` + `Allow` |
| alvo de requisição sintaticamente inválido | `400` e conexão fechada | `invalid_request_target` |
| media type diferente de JSON | `415` | `unsupported_media_type` |
| `Content-Length` ausente | `411` | `content_length_required` |
| `Content-Length` inválido/duplicado ou corpo vazio/incompleto | `400` | código específico de protocolo |
| corpo em `GET`, `HEAD`, `DELETE` ou `OPTIONS` | `400` e conexão fechada | `body_not_allowed` |
| corpo acima de 16 KiB | `413` | `payload_too_large` |
| `Transfer-Encoding` em `POST`/`PATCH` | `501` | `unsupported_transfer_encoding` |
| JSON malformado, não finito, com chave repetida ou raiz não objeto | `400` | código JSON específico |
| campo obrigatório ausente/desconhecido ou valor inválido | `422` | código de campo/valor |
| query desconhecida, repetida ou fora dos limites | `400` ou `422` | código de query específico |
| revisão mudou entre páginas | `409` | `stale_page` |
| SQLite indisponível em `/ready` | `503` | `database_unavailable` |
| falha inesperada/SQLite nas demais operações | `500` | `internal_error`; detalhe fica no log |

Todos os métodos implementados passam pelo mesmo dispatcher: erros esperados
mantêm o envelope; falhas internas são registradas com `request_id` e recebem
mensagem externa genérica.

## 5. Fluxo de criação, ponta a ponta

Leia este fluxo acompanhando os arquivos:

```text
1. Usuário envia o <form>
2. app.js cancela o submit/navegação padrão
3. app.js normaliza as bordas do título e chama api()
4. fetch envia POST /api/tasks com JSON
5. Nginx escolhe location /api/ e encaminha para api:8000
6. _dispatch cria/valida X-Request-ID e inicia a medição
7. TaskHandler._post valida rota e ausência de query
8. _read_json_object valida protocolo, tamanho e JSON estrito
9. _validate_fields aceita exatamente title
10. create_task normaliza o título novamente
11. SQLite executa INSERT parametrizado e incrementa `revision` na transação
12. SELECT recupera a linha criada
13. _send_json devolve 201 + Location + X-Request-ID + tarefa
14. _dispatch registra status e duração correlacionados
15. app.js limpa o form e chama loadTasks()
16. GET /api/tasks busca a página em ordem de ID decrescente
17. DOM é reconstruído com createElement/textContent
```

O frontend normaliza para usabilidade; a API normaliza como autoridade. O SQL
usa `?` e tupla de valores, portanto o título não é concatenado à instrução.

### Transação e fechamento

`create_task` combina:

```python
with closing(connect(db_path)) as connection, connection:
    ...
```

O primeiro context manager fecha a conexão. O segundo confirma no sucesso e faz
rollback se uma exceção escapar. No `sqlite3` do Python, usar somente
`with connection:` não fecha a conexão.

## 6. Backend por responsabilidade

### Inicialização

`initialize` cria o diretório, ativa WAL, aplica tabela e índice de forma
idempotente. `CREATE ... IF NOT EXISTS` basta para a instalação inicial, mas não
altera uma tabela antiga; campos futuros ainda exigem migrações versionadas.

### Conexões

`connect` abre uma conexão curta com timeout de cinco segundos, configura
`sqlite3.Row`, foreign keys, `busy_timeout=5000` e `synchronous=NORMAL`. Cada
função de persistência abre/fecha a sua conexão.

O servidor é uma subclasse de `ThreadingHTTPServer`: requests podem rodar em
threads diferentes e a fila de aceitação tem limite 64. As threads são
não-daemon (`daemon_threads = False`) e `block_on_close = True` faz
`server_close()` aguardar os handlers ativos. O Compose concede 15 segundos à
API antes de forçar sua parada. Não compartilhar uma conexão global respeita a
afinidade de thread do SQLite. WAL permite leitores junto de um escritor e
`busy_timeout` aguarda contenção breve; SQLite ainda serializa escrita e não
vira um banco distribuído.

`query_tasks` abre uma transação de leitura explícita para que `COUNT` e linhas
venham do mesmo snapshot. Isso evita metadados e itens de momentos diferentes.
O endpoint `/ready` exige que o arquivo exista, confirma a tabela `tasks`, lê
suas colunas esperadas e valida a linha singleton de `taskboard_meta`; arquivo
SQLite acessível sem todo o schema operacional não é considerado pronto.

### Funções de persistência

- `list_tasks`: helper completo preservado para testes do repositório;
- `query_tasks`: filtro, paginação, revisão e contagem no mesmo snapshot;
- `get_task`: busca um ID parametrizado;
- `create_task`: valida, insere e consulta a linha;
- `update_task`: altera `title`, `done` ou ambos na mesma transação;
- `delete_task`: remove por ID e devolve se alguma linha mudou.

Essas funções não conhecem HTTP. O handler traduz caminho/corpo em chamada e
resultado em status/JSON.

### Roteamento

O projeto usa comparação de caminhos e uma expressão regular:

```text
^/api/tasks/([0-9]+)$
```

Somente IDs ASCII entre 1 e o máximo inteiro do SQLite e caminho completo são
aceitos. `urlsplit(...).path` separa a query. `parse_list_query` rejeita query
malformada, chave desconhecida/repetida e valores fora dos limites.

`_allowed_methods` centraliza os métodos de cada rota. `405` e `OPTIONS` usam essa
mesma fonte para gerar `Allow`, evitando documentação divergente dentro da API.

### Configuração

| Variável | Padrão fora do container | Valor no container |
|----------|---------------------------|--------------------|
| `APP_HOST` | `127.0.0.1` | `0.0.0.0` |
| `APP_PORT` | `8000` | `8000` |
| `APP_DB_PATH` | `data/tasks.db` | `/data/tasks.db` |
| `LOG_LEVEL` | `INFO` | `INFO`, salvo override |

`APP_PORT` é validada como inteiro entre 1 e 65.535. Erro de configuração
encerra antes de servir requests, uma falha rápida e observável. `SIGTERM` e
`Ctrl+C` saem do loop, fecham o socket e registram início/fim do encerramento.

## 7. Frontend por responsabilidade

[`web/index.html`](web/index.html) usa link de salto, `main`, `header`, `form`,
`label`, controles nativos, `output`, `section`, lista e `noscript`. Status
normal e erro possuem regiões distintas (`role="status"` e `role="alert"`).

[`web/app.js`](web/app.js):

- mantém estado explícito de tarefas, página, filtro, carga e request ativo;
- centraliza `fetch` na função `api`, com timeout de 8 s e cancelamento;
- envia `Accept`, usa `cache: "no-store"` e credenciais apenas da mesma origem;
- lê `X-Request-ID` e apresenta a referência quando a API falha;
- distingue cancelamento, timeout, rede, HTTP e resposta JSON inválida;
- valida em runtime a forma de tarefa e página recebida;
- cria elementos com DOM API e usa `textContent` para dados;
- filtra todas/pendentes/concluídas e pagina com “Carregar mais”;
- ancora páginas seguintes na `revision` inicial e, diante de `409 stale_page`,
  reinicia pela primeira página para não omitir ou duplicar tarefas;
- cancela a listagem anterior para impedir resposta antiga de sobrescrever a nova;
- usa delegação de eventos na lista para concluir/reabrir e remover;
- desabilita somente os controles ocupados e preserva/recoloca foco;
- reage aos eventos `online`/`offline` do navegador.

As regras puras de normalização Unicode, query de paginação e detecção de
snapshot obsoleto ficam em [`web/taskboard-core.mjs`](web/taskboard-core.mjs),
sem acesso ao DOM, para serem verificadas também pelo test runner do Node.js.

### Por que `textContent` importa

Se o título for:

```text
<strong>texto</strong>
```

ele aparece como texto literal. Usar `innerHTML = task.title` interpretaria
marcação controlada pela entrada e criaria risco de XSS. Validação de tamanho
não torna HTML seguro; a API do contexto de saída é o controle correto.

### Acessibilidade observável

- o link de salto leva diretamente ao conteúdo principal;
- cada checkbox recebe ID e nome acessível que inclui o título;
- botão de remover recebe nome acessível específico;
- filtro, checkbox e botões nativos funcionam por teclado;
- lista/itens informam `aria-busy` durante operações;
- status e falha são anunciados sem misturar as mensagens;
- contador de título participa de `aria-describedby`;
- estado vazio é textual e o status não depende apenas de cor;
- `required` e a validação JavaScript oferecem retorno imediato, mas a API
  normaliza e valida novamente. O limite é contado semanticamente em pontos de
  código, inclusive para texto fora do BMP, em vez de depender do modo como um
  atributo HTML conta unidades UTF-16.

Teste: navegue apenas com `Tab`, `Shift+Tab`, espaço e Enter. Confirme link de
salto, foco, criação, filtros, paginação, conclusão, remoção e mensagens.

### Limitações do frontend atual

- a UI ainda não oferece edição de título, embora a API aceite;
- criação e mudança sob filtro podem recarregar a primeira página;
- detecta `offline`, mas não possui cache offline nem fila de sincronização;
- existe um único orçamento de 8 s para receber cabeçalhos e ler o corpo; o
  prazo ainda é fixo e não pode ser configurado por operação;
- não faz retry automático;
- possui testes unitários das regras puras, mas ainda não tem teste automatizado
  de DOM em navegador real;
- não possui autenticação.

Declare a limitação antes de sofisticar a implementação.

## 8. Nginx por responsabilidade

O [`web/nginx.conf`](web/nginx.conf):

- executa workers e grava PID/temporários em caminhos compatíveis com root read-only;
- envia access log JSON para stdout, com request ID, status, duração e upstream;
- envia error log para stderr;
- esconde token de versão do Nginx;
- usa DNS interno do Docker para resolver `api` em runtime;
- limita corpo a 16 KiB, buffers de cabeçalho e tempos de cliente/upstream;
- serve arquivos de `/usr/share/nginx/html`;
- responde `/health` localmente;
- reescreve `/api/health` e `/api/ready` para probes da API;
- encaminha `/api/*` preservando URI;
- gera/substitui `X-Request-ID` e o encaminha à API;
- substitui `X-Forwarded-For` pelo cliente observado, em vez de confiar na entrada;
- assume a propriedade de `Cache-Control` e `X-Content-Type-Options` na borda,
  ocultando os equivalentes do upstream para não duplicar cabeçalhos;
- converte corpo excessivo e upstream indisponível em erros JSON estáveis;
- aplica CSP, COOP, Permissions Policy, Referrer Policy, anti-sniffing e anti-frame;
- bloqueia arquivos ocultos e listagem de diretório;
- usa `sendfile`, ETag e conexões persistentes com limites;
- usa `index.html` como fallback de rotas da interface.

Correspondência:

| Request no gateway | Destino |
|--------------------|---------|
| `/health` | resposta `204` do Nginx |
| `/api/health` | `http://api:8000/health` |
| `/api/ready` | `http://api:8000/ready` |
| `/api/tasks` | `http://api:8000/api/tasks` |
| `/api` | `404` JSON do gateway |
| `/.arquivo` | `404`, sem servir arquivo oculto |
| `/app.js` | arquivo estático |
| `/qualquer-rota` | fallback `/index.html` |

O Nginx e a API possuem limite de 16 KiB. Um corpo grande pode ser recusado no
gateway antes de chegar ao Python; a validação da API ainda é necessária caso
outro cliente interno a acesse. Com `proxy_intercept_errors`, `502/504` viram
`503 api_unavailable` para o cliente, enquanto o error log preserva o diagnóstico.

## 9. Containers e Compose por responsabilidade

### Imagens

Ambas as imagens base estão fixadas por digest e possuem labels OCI descritivos.
Usuários e arquivos têm dono explícito. API roda como UID/GID 10001; gateway
usa `nginx`.

Durante o build, a API executa `py_compile`; o gateway executa `nginx -t` e
remove escrita da configuração/arquivos estáticos. A API inicia Python em modo
isolado (`-I`), sem buffer para logs (`-u`) e sem gravar bytecode em runtime
(`-B`). As flags são explícitas porque `-I` ignora variáveis de ambiente
`PYTHON*`. Dockerfiles também declaram healthchecks e sinais de parada:
`SIGTERM` para a API e `SIGQUIT` para encerramento gracioso do Nginx.

### Redes

- `backend` é interna e conecta API/gateway;
- `access` conecta apenas o gateway e permite a porta publicada;
- o nome `api` é DNS interno; IP do container não é contrato;
- `127.0.0.1:${TASKBOARD_PORT:-8099}:8080` limita acesso ao loopback e permite
  trocar apenas a porta do host; os comandos do curso assumem o padrão 8099;
- `expose: 8000` documenta a porta interna da API, mas não a publica no host.

### Escrita e privilégios

Os dois containers usam root filesystem read-only, `/tmp` em `tmpfs` de 16 MiB
com `noexec,nosuid,nodev`, removem capabilities e proíbem novos privilégios.
Somente `/data` é persistente e gravável na API.

Limites de CPU/memória evitam consumo acidental ilimitado no laboratório, mas
o suporte efetivo varia conforme engine/plataforma. Cada serviço também limita
PIDs a 64, usa init mínimo e rotaciona logs locais em até três arquivos de
10 MiB. A API possui 15 s para encerrar seus workers; o gateway possui 10 s.
Verifique os limites efetivos com inspeção.

### Healthchecks

- API consulta `http://127.0.0.1:8000/ready` dentro do próprio container;
- gateway consulta `http://127.0.0.1:8080/health` dentro do próprio container;
- `depends_on` espera API saudável no start;
- isso não garante saúde permanente nem reinicia serviços (`restart: "no"`).

O volume possui labels `app=taskboard` e `purpose=sqlite-data`, úteis para
inventário; labels não substituem backup nem controle de acesso.

## 10. Rota A — testes e API sem Docker

Esta rota isola Python/SQLite antes de adicionar proxy e containers.

### Verifique a versão

```bash
python3 --version
```

O curso suporta Python 3.12+. Entre no diretório:

```bash
cd 00-Fundamentos/programacao/projetos/taskboard/api
```

### Execute os testes

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

A suíte cria diretórios/bancos temporários e cobre:

- schema/WAL idempotentes e CRUD de persistência;
- normalização, limites, campos parciais e rollback de validação;
- SQL metacharacters como dados e escritores concorrentes;
- parser estrito, filtro, ordem, paginação, snapshot e revisão concorrente;
- servidor real em porta efêmera local;
- liveness, readiness, `HEAD`, `OPTIONS` e ciclo HTTP completo;
- request ID, headers, métodos/rotas e contrato de erros;
- limites de corpo, JSON estrito, campos e query;
- timeout durante corpo parcial, com resposta `408` e fechamento da conexão;
- framing HTTP/1.1: corpo em método sem corpo é rejeitado antes de qualquer
  efeito e nunca vira um segundo request residual, inclusive em rota ausente;
- método arbitrário, alvo inválido e surrogate JSON mantêm erro JSON estável,
  sem traceback ou queda silenciosa da conexão.

O número exato cresce conforme novos casos de regressão são acrescentados. A
saída final deve informar que todos os testes descobertos passaram:

```text
Ran ... tests
OK
```

Se sockets locais forem proibidos pelo ambiente, os testes HTTP são marcados
como `skipped`; isso não equivale a terem passado. Execute-os em ambiente local
que permita loopback antes de considerar o laboratório completo.

As regras puras do frontend têm uma suíte independente:

```bash
node --test ../web/taskboard-core.test.mjs
```

### Execute a API

```bash
APP_HOST=127.0.0.1 \
APP_PORT=8000 \
APP_DB_PATH=/tmp/taskboard-study.db \
python3 server.py
```

O processo fica no primeiro plano. Em outro terminal:

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/ready

curl -i -X POST http://127.0.0.1:8000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Entender o fluxo HTTP"}'

curl -i 'http://127.0.0.1:8000/api/tasks?limit=10&offset=0'
```

Interrompa o servidor com `Ctrl+C`. O handler principal fecha o servidor no
bloco `finally`. Esse modo executa somente a API; não há Nginx nem interface web.

## 11. Rota B — aplicação completa com Docker

### Pré-flight

```bash
docker version
docker compose version

cd 00-Fundamentos/programacao/projetos/taskboard
docker compose config
```

O primeiro build pode precisar baixar imagens. Em runtime, o projeto não chama
serviços externos. Os exemplos mantêm `TASKBOARD_PORT` ausente e usam 8099. Se
a porta estiver ocupada, execute o Compose com, por exemplo,
`TASKBOARD_PORT=8100` e use a mesma porta nos requests.

### Construir e iniciar

```bash
docker compose up --build -d
docker compose ps
```

Espere `api` e `gateway` ficarem `healthy`. Se não ficarem:

```bash
docker compose ps -a
docker compose logs --tail=100 api gateway
```

### Provar saúde por camada

```bash
curl -i http://127.0.0.1:8099/health
curl -i http://127.0.0.1:8099/api/health
curl -i http://127.0.0.1:8099/api/ready
curl -i http://127.0.0.1:8099/api/tasks
```

Espere, respectivamente: `204` do gateway, `200` de liveness da API, `200` de
readiness com SQLite e `200` com a primeira página de tarefas.

Abra `http://127.0.0.1:8099` no navegador.

### Provar rede e identidade

```bash
docker compose port gateway 8080
docker compose port api 8000
docker compose exec gateway wget -qO- http://api:8000/health
docker compose exec api id
docker compose exec gateway id
docker compose top
```

Evidência esperada:

- gateway publicado em `127.0.0.1:8099`;
- API sem porta publicada;
- gateway alcança `api` pelo nome interno;
- processos usam identidades sem root.

## 12. Roteiro funcional por `curl`

### Criar

```bash
curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Praticar contratos HTTP"}'
```

Anote o `id` retornado. Nos comandos seguintes, substitua o exemplo:

```bash
TASK_ID=1
```

### Listar

```bash
curl -i 'http://127.0.0.1:8099/api/tasks?limit=25&offset=0'
curl -i 'http://127.0.0.1:8099/api/tasks?done=false&limit=10&offset=0'
```

Confira `page.limit`, `offset`, `total` e `hasMore`. Obtenha apenas o recurso:

```bash
curl -i "http://127.0.0.1:8099/api/tasks/$TASK_ID"
```

### Editar e concluir atomicamente

```bash
curl -i -X PATCH "http://127.0.0.1:8099/api/tasks/$TASK_ID" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Contrato HTTP praticado","done":true}'
```

Verifique descoberta de métodos e semântica de `HEAD`:

```bash
curl -i -X OPTIONS "http://127.0.0.1:8099/api/tasks/$TASK_ID"
curl -I "http://127.0.0.1:8099/api/tasks/$TASK_ID"
```

### Remover

```bash
curl -i -X DELETE "http://127.0.0.1:8099/api/tasks/$TASK_ID"
```

Confirme `204` e corpo vazio. Repetir DELETE deve produzir `404`, mas o estado
final continua “a tarefa não existe”; essa é a idempotência do DELETE.

## 13. Laboratório de validação e erro

Antes de executar cada caso, preveja status e camada responsável.

### Media type errado

```bash
curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: text/plain' \
  --data 'texto'
```

Esperado: `415` da API.

### JSON malformado

```bash
curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  --data '{invalido'
```

Esperado: `400` da API.

### Raiz JSON errada

```bash
curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  --data '["tarefa"]'
```

Esperado: `400`, pois a raiz deve ser objeto.

### Valor semanticamente inválido

```bash
curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  --data '{"title":"   "}'
```

Esperado: `422` depois da normalização.

### Tipo booleano incorreto

```bash
curl -i -X PATCH http://127.0.0.1:8099/api/tasks/999 \
  -H 'Content-Type: application/json' \
  --data '{"done":"sim"}'
```

Esperado: `422` antes de verificar se o ID existe. A ordem de validação faz
parte do comportamento atual.

### Chave JSON repetida e campo desconhecido

```bash
curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  --data-binary '{"title":"primeiro","title":"segundo"}'

curl -i -X POST http://127.0.0.1:8099/api/tasks \
  -H 'Content-Type: application/json' \
  --data '{"title":"teste","admin":true}'
```

Espere `400 duplicate_json_key` e `422 unknown_fields`. Aceitar silenciosamente
a última chave ou ignorar campos esconderia erro do cliente.

### Query e método fora do contrato

```bash
curl -i 'http://127.0.0.1:8099/api/tasks?limit=10&limit=20'
curl -i -X PUT http://127.0.0.1:8099/api/tasks/1 \
  -H 'Content-Type: application/json' \
  --data '{"title":"teste"}'
```

Espere `422 duplicate_query_parameter` no primeiro e `405` com `Allow` no
segundo.

### Rota inexistente

```bash
curl -i http://127.0.0.1:8099/api/ausente
```

Esperado: `404` JSON da API, encaminhado pelo Nginx.

### Corpo acima do limite

Gere apenas dados sintéticos:

```bash
python3 -c 'print("x" * 20000)' | \
  curl -i -X POST http://127.0.0.1:8099/api/tasks \
    -H 'Content-Type: application/json' \
    --data-binary @-
```

Esperado pelo gateway: `413`. Observe os logs para provar que o Nginx recusou
antes da API.

## 14. Observar o banco sem instalar cliente SQLite

Liste schema e linhas dentro do container:

```bash
docker compose exec -T api python -c \
  "import sqlite3; connection=sqlite3.connect('/data/tasks.db'); print(connection.execute(\"SELECT sql FROM sqlite_master WHERE name='tasks'\").fetchone()[0]); print(connection.execute('SELECT id,title,done,created_at FROM tasks ORDER BY id').fetchall()); connection.close()"
```

Use apenas no laboratório. Em sistemas reais, consultas diagnósticas precisam de
controle de acesso e cuidado para não exibir dados.

Prove o plano da listagem:

```bash
docker compose exec -T api python -c \
  "import sqlite3; connection=sqlite3.connect('/data/tasks.db'); print(connection.execute('EXPLAIN QUERY PLAN SELECT id,title,done,created_at FROM tasks ORDER BY id DESC').fetchall()); connection.close()"
```

Não crie índice apenas porque viu uma varredura: a tabela é pequena e `id` já é
chave. Índices devem responder a carga/consulta medida.

## 15. Logs e diagnóstico

Acompanhe durante uma requisição:

```bash
docker compose logs -f api gateway
```

Interromper com `Ctrl+C` encerra apenas o acompanhamento. Procure:

- access log JSON do Nginx com `requestId`, método, caminho, status, bytes,
  duração e status do upstream;
- log HTTP da API com o mesmo request ID, cliente, método, status e duração;
- `database_error` com stack apenas no log interno;
- erros de DNS/upstream no Nginx.

### Árvore de decisão

```text
curl /health conecta?
|-- não -> gateway iniciou? porta 8099 está publicada/ocupada?
`-- sim
    |
    `-- curl /api/health funciona?
        |-- não -> API healthy? nome api resolve? rede backend? logs de upstream?
        `-- sim
            |
            `-- curl /api/ready funciona?
                |-- não -> SQLite, mount e permissão de /data
                `-- sim -> endpoint funcional funciona?
                    |-- 4xx -> contrato da requisição/valor
                    |-- 5xx -> correlacione logs do gateway e API
                    `-- 2xx, mas UI falha -> Network/Console/DOM no navegador
```

### Casos controlados

Pare a API:

```bash
docker compose stop api
curl -i http://127.0.0.1:8099/health
curl -i http://127.0.0.1:8099/api/health
curl -i http://127.0.0.1:8099/api/ready
docker compose logs --tail=50 gateway
docker compose start api
```

O primeiro health continua `204`; os dois probes da API recebem
`503 api_unavailable` do gateway. Isso demonstra por que health de processo,
liveness de dependência e readiness respondem perguntas diferentes.

Valide Nginx:

```bash
docker compose exec gateway nginx -t
```

## 16. Persistência

1. Crie pelo menos duas tarefas fictícias.
2. Liste e guarde a saída.
3. Recrie os containers preservando volumes:

```bash
docker compose down
docker compose up --build -d
```

4. Espere health e liste novamente:

```bash
curl -sS http://127.0.0.1:8099/api/tasks
```

O volume `task-data` preservou `/data/tasks.db`. Inspecione o mount:

```bash
docker inspect --format '{{json .Mounts}}' "$(docker compose ps -q api)"
```

Container removido não é banco removido. Volume, porém, também pode ser apagado
e não protege contra erro lógico; ele não é backup.

## 17. Backup e restauração

### Snapshot consistente

```bash
docker compose exec -T api python -c \
  "import sqlite3; source=sqlite3.connect('/data/tasks.db'); target=sqlite3.connect('/tmp/taskboard-backup.db'); source.backup(target); target.close(); source.close()"

docker compose cp api:/tmp/taskboard-backup.db ./taskboard-backup.db
```

### Verificar

```bash
python3 -c \
  "import sqlite3; connection=sqlite3.connect('file:taskboard-backup.db?mode=ro', uri=True); print(connection.execute('PRAGMA quick_check').fetchone()[0]); print(connection.execute('SELECT count(*) FROM tasks').fetchone()[0]); connection.close()"
```

Espere `ok` e a quantidade conhecida. O arquivo contém todos os dados; não o
publique nem o versione.

### Restaurar no volume do laboratório

Esta operação substitui o estado atual. Confirme diretório, arquivo e que os
dados são descartáveis:

```bash
test -f ./taskboard-backup.db
docker compose stop api

docker compose run --rm --no-deps \
  --volume "$PWD/taskboard-backup.db:/backup.db:ro" \
  api python -c \
  "import sqlite3; source=sqlite3.connect('file:/backup.db?mode=ro', uri=True); assert source.execute('PRAGMA quick_check').fetchone()[0] == 'ok'; target=sqlite3.connect('/data/tasks.db'); source.backup(target); target.close(); source.close()"

docker compose up -d
curl -sS http://127.0.0.1:8099/api/tasks
```

API parada impede escrita simultânea. O backup é montado read-only. A prova final
é a aplicação ler corretamente os dados restaurados.

## 18. Modelo de ameaça e controles existentes

| Risco no escopo local | Controle atual | Limitação |
|-----------------------|----------------|-----------|
| SQL injection no título | parâmetros SQL | revisar todo novo SQL |
| injeção de HTML pelo título | `textContent` | manter em todo novo sink DOM |
| corpo excessivo | 16 KiB no Nginx e API | não limita quantidade total de requests |
| JSON/campos ambíguos | parser estrito e allowlist de campos/query | contrato precisa evoluir junto do cliente |
| processo privilegiado | usuários sem root, capabilities removidas | runtime/host continuam parte da confiança |
| escrita no filesystem | root read-only, volume e tmpfs específicos | `/data` precisa ser gravável |
| exposição de rede | bind em `127.0.0.1`, API interna | processos locais podem acessar gateway |
| detalhe interno em erro | dispatcher uniforme, mensagem genérica e correlação | logs técnicos também precisam ser protegidos |
| contenção de escrita | transações, WAL e `busy_timeout` | SQLite mantém apenas um escritor por vez |
| clickjacking/sinks no navegador | CSP, `frame-ancestors`, `X-Frame-Options`, DOM seguro | headers não substituem revisão do código |
| cadeia de imagem muda | digest fixado | digest precisa ser atualizado e analisado |
| perda ao recriar container | volume | volume não substitui backup |

Fora do escopo atual:

- identidade, login, autorização e isolamento entre usuários;
- HTTPS, certificados e headers completos de produção;
- CSRF associado a sessões autenticadas;
- rate limit e proteção contra abuso;
- alta disponibilidade, replicação e failover;
- gestão de segredos;
- migrações versionadas;
- monitoramento, tracing e alertas.

Não resolva esses temas copiando snippets aleatórios. Cada um exige um modelo
de ameaça e operação próprios.

## 19. Evolução guiada — campo de prioridade

Implemente uma mudança por vez em branch/cópia de estudo.

### Passo 1: contrato

```text
Campo: priority
Valores: low | normal | high
Criação sem campo: normal
Valor/tipo inválido: 422 e nenhuma inserção
Resposta: sempre inclui priority
Tarefas existentes: normal
Interface: valor textual, não apenas cor
```

Decida se PATCH poderá alterar prioridade. Não deixe implícito.

### Passo 2: teste vermelho

Acrescente testes para:

- default `normal`;
- cada valor permitido;
- tipo/valor inválido;
- persistência e serialização;
- tarefa anterior à migração;
- interface apresenta o texto com segurança.

Confirme que falham porque o recurso ainda não existe.

### Passo 3: migração

`CREATE TABLE IF NOT EXISTS` não adiciona coluna em tabela existente. Crie um
mecanismo versionado. Uma estratégia simples de estudo:

1. leia `PRAGMA user_version`;
2. em transação, aplique a migração seguinte;
3. adicione coluna com default compatível e constraint quando suportado;
4. atualize `user_version` apenas depois do sucesso;
5. teste banco novo e fixture da versão anterior;
6. faça backup antes de experimentar com dados importantes.

### Passo 4: backend

Altere normalização, insert/select/serialize e contrato de erro. Mantenha SQL
parametrizado. Não aceite silenciosamente valor desconhecido.

### Passo 5: frontend

Use `label` e controle nativo; apresente prioridade como texto; preserve teclado;
crie DOM com `textContent`; mostre erro vindo da API.

### Passo 6: operação

```bash
python3 -m unittest -v api/test_server.py
docker compose up --build -d
docker compose ps
curl -i http://127.0.0.1:8099/api/tasks
```

Teste migração em cópia, persistência após recriar, backup/restauração e
rollback documentado. Atualize este contrato junto com o código.

## 20. Outras evoluções, em ordem sugerida

1. interface para editar título usando o PATCH já existente;
2. migrações versionadas com fixtures de versão anterior;
3. exportação JSON consistente e limitada;
4. chave de idempotência para criação;
5. controle otimista com versão e conflito `409`;
6. teste automatizado de navegador para a jornada principal;
7. métricas de quantidade, erro e latência sem cardinalidade explosiva;
8. teste de carga local controlado para contenção do SQLite;
9. paginação por cursor e comparação com offset;
10. runbook automatizado de backup, verificação e restauração.

Para cada evolução: contrato → teste vermelho → backend → frontend → operação
→ documentação. Não combine tudo em um commit.

## 21. Avaliação prática

### Nível essencial

- [ ] Todos os testes descobertos passam sem skip.
- [ ] Sei explicar schema, índice, WAL e invariantes principais.
- [ ] Executo o CRUD por `curl` e prevejo status.
- [ ] Identifico Nginx, API e SQLite nos logs/fluxo.
- [ ] Provo que API não possui porta publicada.
- [ ] Recrio containers preservando tarefas.

### Nível intermediário

- [ ] Provoco `400`, `404`, `413`, `415` e `422` conscientemente.
- [ ] Diagnostico API/banco sem confundir gateway health, API liveness e readiness.
- [ ] Explico transação e fechamento de conexão.
- [ ] Crio e verifico backup consistente.
- [ ] Restauro em ambiente descartável.
- [ ] Opero a interface apenas com teclado.

### Nível avançado

- [ ] Implemento prioridade ou outra mudança vertical.
- [ ] Banco antigo migra sem perder tarefas.
- [ ] Contrato e erros permanecem consistentes.
- [ ] Testes cobrem default, fronteiras, persistência e falha.
- [ ] Logs permitem correlacionar a operação sem expor corpo.
- [ ] Runbook permite a outra pessoa subir, diagnosticar e restaurar.

## 22. Perguntas para defesa

1. Por que `APP_HOST` muda de `127.0.0.1` para `0.0.0.0` no container?
2. Qual é a diferença entre `EXPOSE 8000` e publicar uma porta?
3. Como o gateway encontra `api` se o IP do container muda?
4. Por que `/health` pode funcionar quando `/api/health` falha?
5. Onde o título é validado e por que existe mais de uma camada?
6. Como SQL parametrizado e `textContent` protegem contextos diferentes?
7. Por que cada request abre sua própria conexão SQLite?
8. Qual race/limite ainda existe com escritas concorrentes?
9. Por que root filesystem read-only não impede gravar tarefas?
10. Por que volume não é backup?
11. Como uma coluna nova chega a um banco já existente?
12. O que precisaria mudar antes de qualquer exposição fora do loopback?

## 23. Encerramento e limpeza

Preservar banco:

```bash
docker compose down
```

Apagar também o volume do **projeto atual**:

```bash
docker compose down --volumes
```

O segundo comando é destrutivo para o banco do laboratório. Confirme o diretório
e o backup antes. Evite `docker system prune` como limpeza rotineira: ele pode
atingir recursos de outros projetos.

## Critério de conclusão

O TaskBoard está concluído quando você consegue, sem depender de tentativa e erro:

- [ ] desenhar e explicar o fluxo completo;
- [ ] executar testes e interpretar cada caso;
- [ ] operar o contrato HTTP feliz e inválido;
- [ ] localizar uma falha na primeira camada quebrada;
- [ ] demonstrar rede, identidade, filesystem e limites dos containers;
- [ ] provar persistência, backup e restauração;
- [ ] implementar uma mudança vertical testada e migrável;
- [ ] declarar honestamente o que o projeto não protege.

Rodar o comando prova que o software iniciou. Explicar, quebrar de forma
controlada, diagnosticar, recuperar e evoluir prova que você o compreendeu.
