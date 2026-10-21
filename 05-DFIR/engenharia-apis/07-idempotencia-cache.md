# 07 — Idempotência, concorrência e cache

Falhas distribuídas criam incerteza: o cliente pode perder a resposta depois do
commit. Repetição segura exige identidade da intenção, registro durável e
reconciliação. Cache e precondições reutilizam representações e protegem
atualizações, mas não substituem idempotência de comando.

## Objetivos

- modelar chave idempotente e seu ciclo de vida;
- impedir mesma chave com comandos diferentes;
- aplicar ETag e If-Match contra lost update;
- usar cache sem cruzar identidade ou representação;
- distinguir deduplicação, idempotência e exactly-once.

## 1. Estado da operação idempotente

Para POST, associe a chave a escopo, operação e digest canônico:

~~~text
(tenant, consumer, operation, key)
  -> requestDigest
  -> processing | completed | terminal-failure
  -> status, headers, bodyDigest/body
  -> createdAt, expiresAt
~~~

Primeira tentativa reserva a chave atomicamente. Repetição com mesmo digest
aguarda ou devolve o resultado registrado. Mesmo identificador com digest
diferente recebe 409. A chave não deve ser gerada novamente a cada retry.

A gravação do efeito e do registro precisa compartilhar transação ou protocolo
de recuperação. Se o efeito confirma e o registro some, a repetição duplica.

## 2. Canonicalização e escopo

Hash de bytes brutos trata ordem de propriedades ou espaços como comandos
distintos. Normalize o comando validado e serialize deterministicamente.
Inclua versão da operação para que semântica futura não reaproveite registros
antigos.

Escopo por usuário pode ser correto para comandos pessoais; por tenant ou client
credential pode ser melhor em integrações. Escopo amplo causa conflito entre
consumidores; estreito permite duplicidade. Registre a decisão.

Retenção precisa cobrir a maior janela realista de retry. Expiração precoce
reabre duplicidade; retenção infinita custa armazenamento e pode guardar dados.

## 3. Concorrência otimista

~~~http
GET /v1/items/42
ETag: "item-42-v7"

PATCH /v1/items/42
If-Match: "item-42-v7"
~~~

O servidor aplica compare-and-set. Se a versão atual é v8, retorna 412. Isso
impede que edição baseada em estado antigo sobrescreva mudança de outra pessoa.
No repositório, a condição precisa estar na escrita:

~~~sql
UPDATE items
SET title = :title, version = version + 1
WHERE id = :id AND version = :expected_version
~~~

Zero linhas indica precondição perdida. Ler e depois atualizar sem condição
mantém a corrida.

## 4. Cache correto

Cache-Control define armazenamento e reutilização:

- no-store: não armazenar;
- private: cache compartilhado não deve guardar;
- no-cache: pode guardar, mas deve revalidar antes de reutilizar;
- max-age: frescor em segundos;
- stale-while-revalidate: extensão quando suportada.

ETag e Last-Modified são validadores. Vary inclui dimensões de negociação que
mudam a resposta. Autorização e tenant precisam entrar na chave do cache ou
impedir cache compartilhado. Nunca use URL sozinha para conteúdo personalizado.

Invalidação pode usar TTL curto, versão na chave ou evento. O contrato deve
declarar frescor aceitável; “cache atualizado” não é mensurável.

## 5. Interação entre mecanismos

ETag da representação não é idempotency key. If-Match pergunta se o estado base
ainda vale. Idempotency-Key pergunta se esta intenção já foi processada. Em uma
atualização financeira, ambos podem ser necessários: a chave evita duplicidade
do comando e a versão protege a base.

Exactly-once ponta a ponta raramente existe como propriedade simples. Prefira:

~~~text
entrega ao menos uma vez
+ operação idempotente
+ registro durável
+ reconciliação
= efeito de negócio controlado
~~~

## 6. Falhas por momento

| Momento | Estado | Próxima ação |
|---|---|---|
| antes de reservar chave | nenhum efeito | retry |
| chave processing, antes do efeito | pendente | takeover com lease/política |
| depois do efeito, antes da resposta | completed durável | replay da resposta |
| timeout em dependência | incerto | consultar/reconciliar |
| chave igual, digest diferente | conflito | rejeitar |

Não marque automaticamente timeout como failed; o efeito pode ter ocorrido.

## Falhas comuns

| Falha | Risco | Correção |
|---|---|---|
| chave sem digest | comando diferente reaproveitado | canonicalização |
| registro fora da transação | duplicidade após crash | atomicidade/reconciliação |
| If-Match checado em memória | corrida no banco | compare-and-set |
| cache por URL | vazamento entre usuários | chave completa/private |
| ETag derivada só da versão errada | 304 incorreto | representar bytes/estado |

## Exercícios

### Nível 1 — state machine

Modele estados da chave e respostas. **Aceite:** crash antes/depois do efeito e
payload divergente têm comportamento.

### Nível 2 — concorrência

Dispare dois PATCH com a mesma ETag. **Aceite:** exatamente uma mudança vence e
a outra recebe 412.

### Nível 3 — cache por identidade

Simule dois tenants na mesma URL. **Aceite:** nenhuma resposta cruza tenant e
304 só ocorre para a representação correspondente.

## Checklist

- [ ] Chave tem escopo, digest, estado e retenção.
- [ ] Efeito e registro têm garantia conjunta.
- [ ] If-Match é imposto na escrita atômica.
- [ ] Cache possui chave e frescor corretos.
- [ ] Timeout incerto leva a reconciliação.
- [ ] Nenhuma promessa genérica de exactly-once foi feita.

