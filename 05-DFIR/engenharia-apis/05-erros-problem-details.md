# 05 — Erros previsíveis com Problem Details

Erro é parte do contrato. O consumidor precisa distinguir entrada corrigível,
conflito, identidade inválida, falta de permissão, limite, indisponibilidade e
falha interna sem analisar texto humano. RFC 9457 define Problem Details para
erros HTTP e substitui o antigo RFC 7807.

## Objetivos

- modelar erros como contrato estável;
- usar corretamente type, title, status, detail e instance;
- criar extensões seguras para código, campos e correlação;
- mapear domínio e infraestrutura sem vazar detalhes;
- orientar retry e diagnóstico sem acoplar cliente a mensagens.

## 1. Documento de problema

~~~json
{
  "type": "https://example.test/problems/validation",
  "title": "Requisição inválida",
  "status": 422,
  "detail": "Um ou mais campos são inválidos.",
  "instance": "/v1/items",
  "code": "validation_failed",
  "requestId": "req_01",
  "errors": [
    {"field": "body.title", "code": "too_short"}
  ]
}
~~~

O media type é application/problem+json. **type** identifica a categoria e
precisa de significado estável. **title** resume a categoria. **status** repete o
status HTTP e ajuda quando o corpo é armazenado fora da resposta. **detail**
descreve esta ocorrência. **instance** identifica a ocorrência por referência;
não precisa ser uma URL pública.

Extensões são permitidas. code deve ser estável e documentado. requestId liga a
resposta à telemetria, mas não concede acesso ao log. errors aponta campos de
forma segura e não deve reproduzir valores sensíveis.

## 2. Taxonomia

Evite um tipo para cada frase. Crie categorias acionáveis:

| Tipo | Status típico | Ação do consumidor |
|---|---:|---|
| malformed | 400 | corrigir mensagem |
| validation | 422 | corrigir campos |
| unauthenticated | 401 | obter/renovar credencial |
| forbidden | 403 | parar ou pedir acesso |
| not-found | 404 | corrigir referência |
| state-conflict | 409 | recarregar/reconciliar |
| precondition-failed | 412 | obter nova versão |
| rate-limited | 429 | aguardar conforme política |
| unavailable | 503 | retry limitado |
| internal | 500 | reportar request ID |

Status não é suficiente para lógica de domínio; type/code diferencia conflito de
chave idempotente e transição inválida, por exemplo. Mensagem localizada pode
mudar sem quebrar o cliente.

## 3. Fronteiras de mapeamento

Domínio não precisa conhecer HTTP. Ele emite erros como ItemNotFound,
TransitionNotAllowed ou VersionConflict. O adapter os converte em status e
Problem Details. Erros de banco, stack trace e nome de tabela ficam nos logs
internos com acesso controlado.

~~~text
erro de domínio -> catálogo público -> Problem Details
erro inesperado -> internal genérico -> request ID -> log protegido
~~~

Não transforme indiscriminadamente qualquer exceção em 400. Isso esconde defeito
do servidor, reduz alerta e induz o consumidor a corrigir entrada válida.

## 4. Validação por campo

Paths precisam ser estáveis. Escolha JSON Pointer, caminho lógico ou localização
por segmento e documente. Não exponha mensagem bruta da biblioteca: versões
mudam texto, detalhes podem conter input e clientes passam a depender dele.

Exemplo:

~~~json
{"field": "/title", "code": "min_length", "meta": {"min": 3}}
~~~

meta deve conter apenas dados públicos. Para regras entre campos, use field vazio
ou liste os campos envolvidos sem duplicar o payload.

## 5. Retry e Retry-After

Documente se a classe é transitória. 429 e 503 podem incluir Retry-After; 409
pode exigir nova leitura; 412 exige representação atual; 401 pode permitir uma
renovação. Não marque todo 5xx como repetível: POST sem idempotência pode já ter
efeito.

O cliente aplica limite, jitter e deadline total. A resposta nunca deve ordenar
retry infinito. Um erro persistente após o orçamento vira estado observável e
ação de suporte.

## 6. Segurança e privacidade

Não exponha:

- stack trace, SQL, hostname ou caminho interno;
- segredo, token, cookie ou cabeçalho completo;
- confirmação de existência quando isso viola privacidade;
- dado recebido sem encoding e limite;
- regra de detecção que facilite contorno desnecessário.

401 e 403 têm semânticas distintas, mas 404 pode esconder recurso alheio quando
o modelo de ameaça exige. A escolha deve ser uniforme e testada.

## 7. Catálogo e documentação

Cada tipo registra URI, owner, status, código, condições, campos de extensão,
retry, exemplo e data de mudança. OpenAPI referencia o mesmo schema em todas as
operações. Monitoramento agrega por code/type, nunca por detail de alta
cardinalidade.

O URI type pode resolver para documentação humana, mas o cliente deve comparar
o identificador, não depender de abrir a URL durante a falha.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| HTTP 200 para erro | intermediários e métricas erram | status real |
| cliente analisa detail | tradução quebra integração | type/code |
| exceção crua na resposta | vazamento | catálogo e mapeamento |
| formato diferente no gateway | lógica duplicada | envelope comum |
| request ID só na resposta feliz | incidente sem correlação | middleware e handlers |
| type muda a cada ocorrência | cardinalidade infinita | tipo por categoria |

## Exercícios

### Nível 1 — catálogo

Defina dez tipos com status, code, ação e retry. **Aceite:** mensagens humanas não
são usadas como identificador.

### Nível 2 — mapeamento

Implemente handlers para validação, domínio e erro inesperado. **Aceite:** todos
retornam media type correto, request ID e nenhum detalhe interno.

### Nível 3 — caos

Injete timeout antes e depois do commit. **Aceite:** o problema não afirma
fracasso quando o efeito é incerto e oferece reconciliação segura.

## Checklist

- [ ] RFC 9457 e media type correto são usados.
- [ ] type/code são estáveis e detail é apenas humano.
- [ ] Validação não ecoa valores sensíveis.
- [ ] Erros inesperados não viram 4xx.
- [ ] Request ID aparece em sucesso, erro e log.
- [ ] Retry é explícito e respeita idempotência.
