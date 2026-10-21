# 01 — Semântica HTTP

HTTP transporta intenção e resultado. HTTP/1.1, HTTP/2 e HTTP/3 têm diferenças de
transporte, mas compartilham métodos, status, campos, representações e regras
condicionais definidos pela semântica HTTP. Uma API que conhece apenas URL e JSON
perde mecanismos importantes do protocolo.

## Objetivos

- ler uma troca HTTP sem confundir mensagem com transporte;
- escolher métodos e status por semântica;
- aplicar negociação, cache, precondições e redirecionamento;
- distinguir segurança, idempotência e cacheabilidade;
- diagnosticar respostas tecnicamente válidas, porém semanticamente erradas.

## 1. Anatomia de uma troca

~~~http
GET /v1/items/itm_42 HTTP/1.1
Host: api.example.test
Accept: application/json
If-None-Match: "item-42-v3"
Authorization: Bearer REDACTED
~~~

~~~http
HTTP/1.1 304 Not Modified
ETag: "item-42-v3"
Cache-Control: private, max-age=60
Vary: Accept
~~~

Método e alvo formam a intenção. Campos carregam metadados. O corpo é uma
representação, não “o recurso em si”. Content-Type descreve o corpo enviado;
Accept descreve formatos aceitos para a resposta. A ausência de corpo em 304 é
parte da semântica, não um JSON vazio.

## 2. Métodos e propriedades

| Método | Intenção usual | Seguro | Idempotente |
|---|---|---:|---:|
| GET | obter representação | sim | sim |
| HEAD | obter os metadados de GET | sim | sim |
| POST | processar ou criar sob coleção | não | não por padrão |
| PUT | criar/substituir no alvo conhecido | não | sim |
| PATCH | aplicar modificação parcial | não | depende do formato |
| DELETE | remover associação/estado | não | sim no efeito desejado |
| OPTIONS | descobrir opções do recurso | sim | sim |

Seguro quer dizer que o cliente não solicita mudança de estado. Logs e métricas
ainda podem mudar. Idempotente quer dizer que repetir a mesma intenção tem o
mesmo efeito desejado; respostas e timestamps podem diferir. Essas propriedades
orientam intermediários e retry. Não torne GET destrutivo.

PUT não significa “update completo” automaticamente: a URI final é conhecida e
a representação enviada substitui o estado conforme contrato. PATCH precisa
declarar media type e regra. JSON Merge Patch e JSON Patch têm semânticas
diferentes para ausência, null e listas.

## 3. Status como decisão do protocolo

- **200**: sucesso com representação;
- **201**: recurso criado; normalmente inclui Location;
- **202**: processamento aceito, ainda não concluído; ofereça recurso de status;
- **204**: sucesso sem conteúdo;
- **304**: representação não modificada para requisição condicional;
- **400**: requisição malformada segundo contrato da aplicação;
- **401**: autenticação ausente ou inválida, com desafio quando aplicável;
- **403**: identidade válida, ação não permitida;
- **404**: recurso não encontrado ou existência deliberadamente ocultada;
- **409**: conflito com estado ou identidade da operação;
- **412**: precondição como If-Match avaliou falso;
- **415**: media type enviado não suportado;
- **422**: conteúdo entendido, porém semanticamente inválido;
- **429**: limite excedido; Retry-After pode orientar nova tentativa;
- **503**: indisponibilidade temporária do serviço.

Não use 200 com campo success=false para todas as falhas. O status permite que
clientes, caches, proxies e telemetria ajam sem entender o domínio.

## 4. Representação e negociação

Uma resposta deve ter media type coerente com os bytes. Se a API suporta JSON e
CSV, escolha usando Accept e devolva 406 quando nenhuma representação aceita
puder ser produzida. Se o corpo enviado tem formato não suportado, use 415.

Charset, linguagem e compressão também podem ser negociados. Quando a seleção
depende de um campo de requisição e a resposta é cacheável, Vary informa essa
dimensão ao cache. Vary: Authorization não torna conteúdo privado seguro por si
só; política de cache precisa impedir compartilhamento indevido.

## 5. Cache e validação condicional

Cache-Control define quem pode armazenar, por quanto tempo e quando revalidar.
ETag identifica uma representação. Um cliente pode enviar If-None-Match em GET:
se a tag ainda corresponde, o servidor responde 304 e economiza corpo.

~~~text
GET -> 200 + ETag "v7"
GET + If-None-Match "v7" -> 304
PATCH + If-Match "v7" -> 200 + ETag "v8"
PATCH + If-Match "v7" depois da mudança -> 412
~~~

Validação de cache e controle de concorrência usam campos parecidos, mas têm
objetivos diferentes. Uma ETag forte precisa mudar quando os bytes relevantes
da representação mudam. Dados pessoais normalmente usam private e uma política
conservadora de revalidação.

## 6. Redirecionamento e localização

301/308 indicam mudança permanente; 302/307, temporária. 307 e 308 preservam
método e corpo. Alterar POST para GET em um redirecionamento pode mudar a
intenção, portanto não dependa de comportamento histórico ambíguo. Location em
201 aponta o recurso criado; em 202 pode apontar o job consultável.

## 7. Retry e incerteza

Uma conexão perdida não revela se o servidor executou a escrita. Métodos
idempotentes podem ser repetidos com mais segurança, mas ainda exigem orçamento,
backoff e limite. POST precisa de chave de idempotência ou consulta de
reconciliação quando duplicidade é perigosa.

Retry-After pode ser data HTTP ou segundos. O cliente precisa validar, aplicar
um teto e respeitar cancelamento. Repetir 400, 401 ou 403 sem mudar algo tende a
ser inútil.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| Content-Type ignorado | parser interpreta corpo errado | validar antes de decodificar |
| 202 sem recurso de status | conclusão impossível de consultar | fornecer Location/status |
| GET com efeito | prefetch ou crawler muda estado | usar método não seguro |
| 204 com corpo | clientes divergem | remover corpo ou usar 200 |
| cache público de usuário | vazamento entre consumidores | private/no-store conforme risco |
| retry de POST cru | duplicidade | idempotency key e reconciliação |

## Exercícios

### Nível 1 — classificação

Classifique doze operações por método, status feliz, segurança, idempotência e
cacheabilidade. **Aceite:** cada escolha explica a intenção, não o nome da rota.

### Nível 2 — troca condicional

Implemente GET com ETag e PATCH com If-Match. **Aceite:** há 200, 304, atualização
válida e 412 para versão antiga.

### Nível 3 — falha ambígua

Simule perda de conexão após commit de POST. **Aceite:** a repetição com a mesma
chave não duplica, corpo diferente conflita e o resultado pode ser consultado.

## Checklist

- [ ] Método representa a intenção.
- [ ] Status e corpo não se contradizem.
- [ ] Content-Type, Accept e Vary estão corretos.
- [ ] Cache privado não vaza entre identidades.
- [ ] Precondições evitam lost update.
- [ ] Retry considera idempotência, orçamento e incerteza.

