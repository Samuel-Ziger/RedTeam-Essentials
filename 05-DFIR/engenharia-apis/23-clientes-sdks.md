# 23 — Clientes resilientes e SDKs

SDK transforma protocolo em interface idiomática, mas não deve esconder falhas
distribuídas. Consumidor precisa controlar timeout, cancelamento, paginação,
retry e idempotência. Gerar tipos é começo, não produto final.

## Objetivos

- projetar configuração e lifecycle do cliente;
- mapear problemas para erros tipados;
- implementar retry e paginação lazy;
- gerar código de forma reproduzível;
- comparar decisões em cinco linguagens.

## 1. Superfície do cliente

Um cliente precisa de:

- base URL configurada por código confiável;
- credencial/provider sem exposição;
- timeout/deadline e cancelamento;
- pool/conexões com lifecycle;
- headers de user-agent/versão;
- serialização conforme contrato;
- limites de resposta;
- erros tipados com status, type/code e request ID;
- política de retry opt-in/segura;
- telemetria sem payload.

Não aceite base URL derivada de dado não confiável. Não crie novo client HTTP por
requisição; reutilize conforme biblioteca e feche no final.

## 2. Erros tipados

~~~text
ApiError
  ValidationError(fields)
  AuthenticationError
  AuthorizationError
  ConflictError(code)
  RateLimitError(retryAfter)
  UnavailableError
  ProtocolError
~~~

ProtocolError indica resposta incompatível: JSON inválido, media type errado ou
schema inesperado. Preserve request ID para suporte e trecho seguro limitado,
nunca token/corpo inteiro.

Cliente decide por campos estáveis. Expor somente exception com texto força
parsing frágil.

## 3. Retry e idempotência

Default conservador: repetir GET/HEAD em falhas transitórias dentro de deadline.
POST só repete com idempotency key estável e contrato do provider. PATCH/PUT
dependem de precondição e semântica.

Cada tentativa consome orçamento restante. Respeite cancelamento e Retry-After
com teto. Instrumente attempt count. Não esconda cinco tentativas que tornam uma
chamada de 200 ms em 20 s.

## 4. Paginação lazy

Iterator assíncrono ou síncrono busca página conforme consumo:

~~~python
for item in client.items.iter(status="active", page_size=50):
    process(item)
~~~

Não carregue toda coleção. Detecte cursor repetido para evitar loop, preserve
filtro, limite páginas/itens opcionalmente e permita cancelamento. Exponha também
método page-level quando consumidor precisa do token.

## 5. Geração e camada manual

Pipeline:

~~~text
OpenAPI fixado -> generator fixado -> código gerado
               -> formatter/tests -> wrapper idiomático -> pacote
~~~

Nunca edite gerado manualmente. Templates e versões ficam no repositório; diff é
revisado. Wrapper adiciona ergonomia, autenticação, retry e observabilidade sem
duplicar modelos.

SemVer do SDK não é automaticamente versão da API. Documente matriz de
compatibilidade e suporte.

## 6. Cinco linguagens

- Python: context manager, typing, iterator e exceções.
- Java: client lifecycle, Optional consciente e CompletionStage/streams.
- C17: buffers explícitos, ownership, códigos de erro e limpeza.
- C#: HttpClient reutilizado, CancellationToken e IAsyncEnumerable.
- JavaScript: AbortSignal, async iterator, Number versus inteiros grandes.

O diretório exemplos implementa a mesma query canônica para tornar diferenças
visíveis. Codificação percentual deve usar biblioteca correta; concatenar
parâmetro permite ambiguidades.

## 7. Distribuição e suporte

Pacote contém licença, changelog, SBOM/proveniência conforme processo, exemplos,
versões de runtime e política de fim de suporte. Assine/publice pelo pipeline.

Telemetria de versão ajuda inventário, respeitando privacidade. Nunca envie uso
externo sem consentimento/política.

## 8. Teste de compatibilidade

Mantenha uma matriz provider atual × SDK suportado e execute exemplos publicados
como testes. O cliente deve tolerar campo adicional e enum desconhecido conforme
contrato, mas rejeitar resposta que viola tipo ou campo obrigatório. Teste ainda
proxy, compressão, resposta vazia e charset. Uma versão só pode sair de suporte
depois de comunicação, alternativa e telemetria suficiente; baixar o pacote não
prova que ele continua em uso.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| retry invisível | latência/duplicidade | política explícita |
| lista inteira | memória | iterator lazy |
| editar gerado | regen perde correção | wrapper/template |
| erro textual | cliente frágil | tipos/codes |
| token no log | vazamento | redação/teste canário |

## Exercícios

### Nível 1 — cliente

Implemente GET com timeout e erro tipado. **Aceite:** 404, 429, 503 e protocolo
inválido são distinguíveis.

### Nível 2 — iterator

Percorra páginas lazy com cancelamento. **Aceite:** cursor repetido é detectado e
memória não cresce com total.

### Nível 3 — duas linguagens

Gere SDK e crie wrapper em duas linguagens. **Aceite:** contrato, retry e
cancelamento produzem comportamento equivalente.

## Checklist

- [ ] Cliente tem lifecycle, deadline e cancelamento.
- [ ] Erros preservam type/code/request ID.
- [ ] Retry não esconde duplicidade.
- [ ] Paginação é lazy e limitada.
- [ ] Código gerado é reproduzível e não editado.
- [ ] Pacote possui matriz de compatibilidade.
