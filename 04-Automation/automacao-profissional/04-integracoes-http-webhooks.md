# 04 — Integrações HTTP e webhooks confiáveis

Uma integração externa é uma fronteira distribuída: a rede falha, a resposta pode
se perder, o fornecedor evolui e nenhum dos lados compartilha uma transação. Um
cliente profissional traduz esse protocolo para conceitos do domínio.

## Objetivos

- projetar clients com timeout, limites, paginação e validação;
- classificar transporte, protocolo, aplicação e estado incerto;
- aplicar retry apenas quando a semântica permitir;
- verificar assinatura, frescor e replay de webhook;
- isolar formatos externos atrás de adapters e testes de contrato.

## 1. Adapter na fronteira

O núcleo não deve conhecer nomes específicos do fornecedor:

~~~text
caso de uso -> porta CustomerDirectory
                    ^
                    |
           HttpVendorAdapter -> HTTP/JSON externo
~~~

O adapter converte request, autentica, valida a resposta e traduz para tipos
internos. Se o fornecedor renomear customer_ref para customerId, somente a borda
muda.

## 2. Orçamento de tempo

“Tem timeout” é insuficiente. Considere:

- resolução/conexão;
- negociação TLS;
- espera por cabeçalhos;
- leitura do corpo;
- tempo total do caso de uso;
- tempo restante antes de cada retry.

Se a operação possui 10 segundos e cada tentativa pode usar 10, três tentativas
violam o contrato. Propague deadline e não inicie tentativa que não cabe no orçamento.

Cancelamento e timeout não provam que o servidor não aplicou uma escrita. O estado
pode ser uncertain até consulta ou chave idempotente confirmar.

## 3. Validação de resposta

Para toda chamada, valide em camadas:

1. transporte concluiu;
2. status é esperado para aquela operação;
3. Content-Type é compatível;
4. Content-Length e leitura respeitam limite;
5. corpo pode ser decodificado;
6. schema e versão são suportados;
7. invariantes de domínio são verdadeiros.

Status 200 com HTML de um proxy não é sucesso JSON. Resposta 204 não deve passar
por parser de JSON. Corpo de erro pode estar ausente ou fora do schema normal.

## 4. Taxonomia de falha

| Classe | Exemplos | Ação inicial |
|---|---|---|
| configuração | URL ou credencial ausente | falha permanente local |
| transporte | DNS, conexão, TLS | retry condicionado |
| protocolo | status/content-type inesperado | classificar por contrato |
| rate limit | 429 e Retry-After | aguardar dentro do orçamento |
| servidor transitório | 502, 503, 504 | retry idempotente e limitado |
| cliente permanente | 400, 401, 403, 404 | corrigir, não repetir cegamente |
| schema | JSON válido, dado incompatível | quarentena/alerta de contrato |
| incerta | timeout após escrita | reconciliar antes de repetir |

Status HTTP isolado não conta toda a história. Um 409 pode representar conflito
esperado e recuperável; um 404 pode ser transitório em consistência eventual. O
contrato específico decide.

## 5. Método, idempotência e concorrência

GET e HEAD possuem semântica segura; PUT e DELETE são definidos como idempotentes
em HTTP, mas o serviço ainda precisa implementar a semântica corretamente. POST
pode ser repetível quando o servidor aceita uma chave idempotente.

Para evitar sobrescrita perdida:

~~~text
GET recurso -> ETag "v7"
PUT recurso com If-Match: "v7"
servidor -> 200 ou 412 se outro ator alterou
~~~

Não transforme 412 em retry automático com o mesmo corpo: existe um conflito a
ser reconciliado.

## 6. Paginação

Offset pode duplicar ou perder itens quando a coleção muda. Cursor opaco costuma
ser mais estável, mas também exige limites:

~~~python
def fetch_all(client, max_pages: int = 100):
    cursor = None
    seen_cursors = set()
    for _ in range(max_pages):
        page = client.fetch(cursor=cursor, limit=100)
        yield from page.items
        if page.next_cursor is None:
            return
        if page.next_cursor in seen_cursors:
            raise RuntimeError("cursor repetido")
        seen_cursors.add(page.next_cursor)
        cursor = page.next_cursor
    raise RuntimeError("limite de paginas excedido")
~~~

Defina consistência: snapshot, watermark, updatedSince ou best effort. Deduplicar
por ID pode esconder mudança de versão; use identidade e versão apropriadas.

## 7. Autenticação e segredos

Credenciais vão em mecanismo documentado, geralmente cabeçalho, nunca em query se
puderem aparecer em histórico e logs. Não registre Authorization, cookies, URL
assinada ou corpo sensível. Prefira tokens curtos e escopo mínimo.

Renovação precisa de concorrência controlada: dez chamadas recebendo 401 não devem
disparar dez refreshes. Diferencie token expirado de permissão insuficiente.

## 8. Webhooks

Receber webhook com HTTPS não autentica o emissor no nível da aplicação. Um fluxo
comum:

1. leia bytes brutos com limite;
2. capture cabeçalhos necessários;
3. verifique timestamp dentro da tolerância;
4. calcule HMAC sobre o formato exato documentado;
5. compare em tempo constante;
6. verifique event ID contra replay;
7. persista/enfileire antes de responder sucesso;
8. processe idempotentemente fora da requisição curta.

Verifique a assinatura **antes** de parsear e reserializar: espaços ou ordem podem
mudar os bytes. Guarde chaves de replay pela janela definida. Dois segredos podem
coexistir durante rotação, com identificador de chave.

### Ordem e entrega

Webhooks podem chegar duplicados, atrasados ou fora de ordem. Use versão do recurso
ou busque o estado atual quando o evento for apenas notificação. Não conclua que
evento recebido depois descreve estado mais novo.

## 9. Testes de contrato

Use servidor fake local para testar timeout, resposta truncada, corpo excessivo,
Content-Type errado, paginação cíclica e 429. Fixtures devem ser sanitizadas e
versionadas. Um sandbox real complementa, mas não substitui testes determinísticos.

Consumer contract tests registram o subconjunto de resposta que o cliente exige.
Tolere campos adicionais quando permitido; rejeite tipo alterado e versão futura
sem adaptar silenciosamente.

## Falhas e diagnóstico

| Sintoma | Hipótese | Evidência segura |
|---|---|---|
| duplicata após timeout | escrita foi aplicada | chave, request ID e consulta |
| loop de paginação | cursor repetido | hash do cursor, não token bruto |
| parser falha em 200 | HTML/schema novo | status, content-type e tamanho |
| webhook rejeitado | bytes/timestamp/segredo | key ID e razão enumerada |
| todos fazem refresh | falta single-flight | contagem concorrente |

## Exercícios

### Nível 1 — cliente limitado

Implemente GET com timeout, limite e schema. **Aceite:** testes cobrem HTML em 200,
corpo excessivo, JSON truncado e campo de tipo errado.

### Nível 2 — paginação e retry

Implemente cursor com detecção de ciclo. **Aceite:** não perde nem duplica itens,
respeita Retry-After e encerra no deadline.

### Nível 3 — webhook

Verifique HMAC, timestamp e replay usando segredo sintético. **Aceite:** assinatura
é calculada sobre bytes brutos, comparação é segura e evento duplicado não repete
o efeito.

## Checklist

- [ ] O adapter impede que o JSON externo vaze ao domínio.
- [ ] Timeout, tamanho, status, tipo e schema são validados.
- [ ] Retry depende de semântica e de orçamento.
- [ ] Paginação tem limite, consistência e detecção de ciclo.
- [ ] Webhook verifica assinatura, frescor e replay.
- [ ] Logs excluem credenciais e payload sensível.

