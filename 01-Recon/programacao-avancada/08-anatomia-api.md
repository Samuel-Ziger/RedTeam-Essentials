# Anatomia completa de uma API

Uma API não é apenas uma função que recebe JSON e devolve JSON. Ela é um
contrato observável atravessado por rede, proxies, autenticação, regras de
negócio, transações e dependências. Este capítulo acompanha uma requisição do
cliente ao armazenamento e de volta, explicitando onde cada garantia deve ser
aplicada.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- decompor uma chamada em DNS, conexão, TLS, HTTP, aplicação e persistência;
- distinguir representação, recurso, comando, evento e caso de uso;
- localizar autenticação, autorização, validação e transação;
- desenhar deadlines e timeouts sem criar retries ilimitados;
- definir invariantes que continuam válidos sob concorrência e falha;
- diagnosticar em qual camada uma requisição falhou.

## Vocabulário mínimo

| Termo | Significado neste curso |
|---|---|
| recurso | entidade identificável exposta pela API, como um produto |
| representação | forma serializada de um recurso, como JSON |
| comando | intenção de alterar estado, como reservar estoque |
| consulta | leitura que não pretende alterar o estado do servidor |
| evento | fato imutável que já ocorreu |
| contrato | conjunto de entradas, saídas, erros e semânticas prometidas |
| invariante | condição que deve permanecer verdadeira em todo estado válido |
| middleware | etapa transversal executada ao redor da lógica da rota |
| deadline | instante máximo para a operação inteira terminar |

## Uma requisição antes do controller

Considere `https://api.example.test/v1/products?limit=20`. Antes que qualquer
controller execute, o cliente normalmente:

1. interpreta esquema, host, porta, caminho e query da URL;
2. consulta cache ou resolvedor DNS para obter endereços;
3. escolhe um endereço e abre TCP, ou QUIC no caso de HTTP/3;
4. negocia TLS, valida cadeia, hostname e validade do certificado;
5. negocia a versão HTTP e envia headers e, se houver, body;
6. atravessa CDN, WAF, balanceador, ingress ou gateway;
7. alcança o socket do processo ou proxy local da aplicação.

Isso produz uma primeira regra operacional:

> `timeout` não prova que a operação não aconteceu; prova apenas que o
> chamador não recebeu uma conclusão dentro do prazo.

Uma falha descrita como “a API caiu” pode estar em DNS, rota, handshake, fila do
gateway, pool de conexões, lock, dependência, serialização ou download lento.
Registre tempos por etapa quando o cliente ou a plataforma permitir.

### URL e target não são dados inocentes

```text
https://api.example.test:443/v1/products/42?include=stock#details
\___/   \________________/\__/\______________/\___________/\_____/
scheme         host       port       path          query    fragment
```

O fragmento não é enviado ao servidor HTTP. Query strings e paths costumam
aparecer em histórico, analytics e logs; por isso, não transporte token, senha,
documento pessoal ou outro segredo neles.

## A mensagem HTTP

Um request HTTP/1.1, exibido de forma didática, contém linha inicial, headers,
linha vazia e body:

```http
POST /api/v1/products HTTP/1.1
Host: api.example.test
Content-Type: application/json
Accept: application/json
Idempotency-Key: 01J8CXW77KVM9R2M97REZQ1X2V
X-Request-ID: 3bb0a764bd9a
Content-Length: 60

{"sku":"BOOK-001","name":"Banco de Dados","priceCents":4500}
```

Mesmo em HTTP/2 ou HTTP/3, onde a codificação no fio é diferente, os conceitos
de método, target, headers, status e conteúdo permanecem. Não programe supondo
que capitalização ou ordem dos headers seja significativa.

### Cada parte tem uma responsabilidade

- método e path selecionam a semântica da operação;
- query restringe, ordena, pagina ou seleciona representação;
- headers carregam metadados e precondições;
- `Content-Type` descreve o conteúdo enviado;
- `Accept` declara representações que o cliente aceita;
- body transporta representação ou comando;
- status, headers e body da resposta formam uma unidade contratual.

`Content-Type` e `Accept` não são sinônimos. Um cliente pode enviar JSON e
pedir uma resposta CSV, caso a API suporte ambos.

## O pipeline dentro da aplicação

```text
socket / servidor HTTP
  -> limites de linha, headers, body e tempo
  -> parsing HTTP e descompressão controlada
  -> correlação, logging e tracing
  -> proteção de capacidade / rate limiting
  -> autenticação
  -> roteamento
  -> autorização contextual
  -> desserialização e validação do schema
  -> caso de uso e transação
  -> repositório / pool / dependência
  -> mapeamento para resposta
  -> serialização e compressão
  -> proxy / cliente
```

A ordem de middleware é parte da arquitetura. Um limite de body aplicado depois
do parser já permitiu consumir memória; autorizar apenas no controller pode
deixar outra rota desprotegida; registrar body antes de sanitizar pode vazar
credenciais.

### Correlação sem confiar no cliente

Um request ID recebido pode ser preservado apenas se cumprir formato e tamanho
definidos. Caso contrário, gere outro. Nunca permita que o valor controle quebra
de linha no log. O ID correlaciona logs; ele não autentica a chamada e não deve
ser usado como chave de idempotência.

## Validação em camadas

Uma entrada deve cruzar filtros diferentes. Misturá-los produz erros vagos e
regras fáceis de contornar.

| Camada | Pergunta | Exemplo de falha |
|---|---|---|
| framing | a mensagem termina onde deveria? | `Content-Length` ambíguo |
| transporte | tamanho e tipo são aceitos? | body maior que 1 MiB |
| sintaxe | o conteúdo pode ser lido? | JSON truncado |
| schema | campos, tipos e formatos são válidos? | `priceCents` como string |
| domínio | a intenção é permitida nesse contexto? | preço negativo |
| autorização | essa identidade pode agir nesse objeto? | outro tenant |
| persistência | a invariante resiste à concorrência? | SKU duplicado |

Limite o tamanho antes de alocar e desserializar. Verifique tipo antes de regra
semântica. Preserve no banco as invariantes que precisam sobreviver a dois
workers concorrentes.

### Exemplo de contrato de entrada

```json
{
  "sku": "BOOK-001",
  "name": "Banco de Dados",
  "priceCents": 4500
}
```

Regras possíveis:

- o objeto não aceita campos desconhecidos nesta versão;
- `sku` tem de 1 a 40 caracteres e um alfabeto documentado;
- `name` tem de 1 a 120 pontos de código Unicode após a normalização escolhida;
- `priceCents` é inteiro entre 0 e um limite de negócio;
- o par `(tenant_id, sku)` é único no banco.

Documente se espaços são preservados, removidos nas pontas ou proibidos. Não
aplique lowercase, coerção numérica ou normalização Unicode silenciosa sem uma
decisão de domínio: transformações também alteram identidade.

## Controller, caso de uso, domínio e repositório

Um bom limite de responsabilidade é:

- **controller/adaptador HTTP:** traduz request e resultado para HTTP;
- **caso de uso:** coordena política, transação e dependências;
- **domínio:** protege regras e invariantes sem depender de HTTP;
- **repositório:** expressa operações de persistência necessárias;
- **driver:** executa SQL, chamada remota ou acesso ao broker.

O controller não deve decidir desconto, e o domínio não deve retornar status
HTTP. A tradução explícita permite reutilizar o caso de uso por fila, CLI ou job.

```text
create_product(command, principal, idempotency_key)
  -> autorizar principal para o tenant
  -> validar regra contextual
  -> begin
  -> reservar chave + hash da intenção
  -> inserir produto sob constraint de unicidade
  -> inserir evento na outbox
  -> armazenar resultado idempotente
  -> commit
  -> mapear resultado
```

### Onde termina a transação

O limite transacional acompanha a invariante, não um método arbitrário do
repositório. Se produto e evento outbox precisam existir juntos, ambos entram na
mesma transação. Evite manter transação de banco aberta durante uma chamada de
rede lenta: isso retém conexão e lock sem oferecer atomicidade entre sistemas.

## Construção da resposta

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/products/1b67c73e
ETag: "1"
X-Request-ID: 3bb0a764bd9a
Cache-Control: no-store

{"id":"1b67c73e","sku":"BOOK-001","version":1}
```

Cada parte comunica algo:

- `201` significa que a criação terminou;
- `Location` identifica o recurso criado;
- `ETag` permite leitura condicional ou controle otimista;
- `Cache-Control` define tratamento por caches;
- o request ID permite correlacionar suporte e telemetria.

Não retorne dados antes do commit. Caso o commit falhe depois de montar o
objeto, o cliente não pode receber sucesso. Depois que headers começam a ser
enviados, trocar para um erro estruturado pode ser impossível; prefira preparar
e validar a resposta antes de iniciar o streaming.

### HEAD, 204 e respostas sem body

- `HEAD` deve ter os headers correspondentes ao `GET`, sem enviar o body;
- `204 No Content` não leva representação no body;
- erros devem conservar seu media type, por exemplo
  `application/problem+json`;
- representações sensíveis normalmente usam `Cache-Control: no-store`.

## O que acontece depois da resposta

Responder não significa que todo trabalho terminou. O processo pode exportar
trace, agregar métrica ou publicar uma outbox. Separe:

- trabalho descartável, como envio eventual de telemetria com buffer limitado;
- trabalho durável, como publicar um evento de negócio;
- trabalho que deveria ter terminado antes do sucesso, como confirmar o commit.

Uma task somente em memória desaparece no restart. Se não puder ser perdida,
registre a intenção em armazenamento durável antes de responder.

## Deadline, timeout, cancelamento e retry

**Timeout** limita uma etapa. **Deadline** limita a operação inteira. Suponha
um deadline de 800 ms:

```text
cliente: 800 ms total
  gateway: até 700 ms
    aplicação: até 600 ms
      adquirir pool: 50 ms
      SQL: 300 ms
      serializar + margem: restante
```

Esses números são exemplo, não padrão universal. O importante é deixar margem
para a camada externa responder de forma controlada.

Retry seguro requer simultaneamente:

1. falha classificada como transitória;
2. operação idempotente ou chave de idempotência;
3. limite de tentativas;
4. backoff exponencial com jitter;
5. respeito ao deadline restante;
6. telemetria que diferencia tentativa de operação lógica.

Retries em todas as camadas multiplicam carga. Três tentativas no cliente, no
gateway e no serviço podem chegar a 27 chamadas internas. Defina um dono.

Propague cancelamento para fila, consulta e chamada remota quando a biblioteca
oferecer suporte. Cancelamento poupa trabalho, mas não desfaz automaticamente um
commit já realizado.

## Matriz de falhas

| Falha | O que o cliente sabe | Resposta/conduta esperada |
|---|---|---|
| JSON inválido | pedido não foi entendido | 400 estruturado |
| regra de domínio inválida | intenção foi rejeitada | 422 estruturado |
| chave única concorrente | houve conflito conhecido | 409 |
| pool esgotado | serviço sem capacidade no prazo | 503 ou timeout controlado |
| cliente desconectou antes do commit | nada conclusivo | cancelar se possível |
| cliente desconectou depois do commit | operação ocorreu | retry deve ser idempotente |
| outbox ainda não publicada | escrita local ocorreu | responder conforme consistência prometida |
| serialização falhou após commit | estado mudou, resposta falhou | incidente + retry idempotente |

## Invariantes de uma criação robusta

Para o exemplo de produto, escreva antes do código:

- um `sku` pertence a no máximo um produto por tenant;
- uma chave idempotente representa uma única intenção;
- produto e evento outbox aparecem na mesma transação;
- nenhum sucesso é enviado antes do commit;
- toda resposta possui correlação, inclusive erros inesperados;
- token, cookie e segredo nunca entram no log;
- timeout não é interpretado como prova de rollback.

Essas frases são mais valiosas que uma lista de classes: orientam banco,
testes, observabilidade e tratamento de falhas.

## Prática guiada

Envie uma requisição para uma API local do curso e preserve os detalhes:

```bash
curl --verbose \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --header 'Idempotency-Key: aula-08-intencao-001' \
  --data '{"sku":"BOOK-001","name":"Banco de Dados","priceCents":4500}' \
  http://127.0.0.1:8000/api/v1/products
```

Use somente um serviço local autorizado. No relatório, separe:

1. o que foi escrito pelo cliente;
2. o que foi adicionado pelo cliente HTTP;
3. o que veio do servidor ou proxy;
4. o que identifica contrato e o que é detalhe operacional.

## Exercícios

1. Desenhe o percurso de uma criação desde a resolução DNS até o commit.
2. Para cada etapa, indique timeout, responsável e telemetria.
3. Defina schema, regras de domínio e constraints para cadastro de livros.
4. Simule banco indisponível e descreva status, corpo e log esperados.
5. Explique três formas pelas quais um e-mail numa URL pode vazar.
6. Modele o caso “commit terminou, conexão caiu antes da resposta”.
7. Compare trabalho pós-resposta descartável e durável com dois exemplos.
8. Encontre um pipeline cuja autorização ocorre tarde demais e reorganize-o.

## Critérios de conclusão

Seu trabalho está completo quando:

- o diagrama nomeia todas as fronteiras de confiança e dependências;
- cada falha retorna um resultado contratual ou gera incidente observável;
- os limites de entrada são aplicados antes da alocação cara;
- as invariantes concorrentes estão protegidas no armazenamento;
- retry tem dono, limite, backoff, jitter e requisito de idempotência;
- nenhuma conclusão depende de “timeout significa que nada aconteceu”.

## Checklist de revisão

- [ ] Consigo explicar request line, headers, body, status e representação.
- [ ] Sei onde ficam validação, autenticação e autorização.
- [ ] Consigo justificar o limite transacional do caso de uso.
- [ ] Diferencio timeout, deadline, cancelamento e retry.
- [ ] Sei o que precisa ser durável antes de responder.
- [ ] Escrevi invariantes e cenários de falha antes da implementação.
