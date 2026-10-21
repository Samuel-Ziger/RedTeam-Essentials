# Dados distribuídos, consistência e integrações confiáveis

Quando dados atravessam processos, bancos ou regiões, falhas deixam de ser
totais e ordenadas. Uma chamada pode ter sido executada mesmo que a resposta se
perca; duas réplicas podem discordar; um evento pode chegar duas vezes ou fora
de ordem. Este capítulo ensina a declarar garantias realistas e a recuperar a
consistência sem prometer “exactly once” por conveniência.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- raciocinar sobre falhas parciais e resultados desconhecidos;
- distinguir consistência, isolamento, durabilidade e disponibilidade;
- projetar outbox/inbox, consumidores idempotentes e reconciliação;
- escolher estratégia de replicação, particionamento e leitura;
- modelar sagas com compensações e intervenção manual;
- evoluir eventos sem quebrar consumidores;
- testar convergência sob queda, duplicação e reordenação.

## O salto de um processo para uma rede

Dentro de um processo, uma chamada retorna ou levanta erro. Na rede, o chamador
pode observar timeout enquanto o servidor:

- nunca recebeu a mensagem;
- recebeu, mas ainda não executou;
- executou e falhou antes do commit;
- confirmou o commit e perdeu a resposta;
- respondeu, mas a resposta se perdeu;
- continua executando depois do cancelamento do cliente.

Logo, “tentar novamente” é uma decisão de semântica, não apenas de biblioteca.
Comandos precisam de identidade estável, deduplicação e resultado recuperável.

## Propriedades que costumam ser confundidas

| Propriedade | Pergunta |
|---|---|
| atomicidade | todas as mudanças locais ocorrem ou nenhuma? |
| consistência do banco | constraints permanecem verdadeiras? |
| isolamento | quais estados transações concorrentes observam? |
| durabilidade | um commit sobrevive às falhas prometidas? |
| consistência distribuída | quando leitores/réplicas observam uma escrita? |
| disponibilidade | o sistema responde sob as falhas consideradas? |
| idempotência | repetir a intenção duplica o efeito? |

Uma transação serializable em um banco não torna uma projeção em outro banco
imediatamente consistente. Um broker durável não torna o efeito do consumidor
exatamente uma vez.

## Modelos de consistência observável

- **forte/linearizável:** uma operação concluída parece ocorrer em um ponto
  único entre início e fim;
- **eventual:** sem novas atualizações, réplicas convergem;
- **read-your-writes:** um cliente observa sua própria escrita subsequente;
- **monotonic reads:** depois de observar uma versão, não volta a uma anterior;
- **consistent prefix:** leituras não veem uma sequência causalmente invertida;
- **bounded staleness:** atraso é limitado por tempo ou versões.

Não diga apenas “temos consistência eventual”. Declare entidade, operação,
janela esperada, comportamento durante falha e como o cliente detecta atraso.

### Linearizabilidade e serializabilidade

Linearizabilidade fala da ordem externa de operações em um objeto. Isolamento
serializable fala do resultado de transações concorrentes como alguma execução
serial. São conceitos relacionados, mas não intercambiáveis; o banco e o driver
precisam documentar exatamente as garantias utilizadas.

## Tempo, ordem e versão

Relógios de máquinas divergem e podem saltar. Timestamp de parede é útil para
auditoria e expiração com tolerância, mas não resolve sozinho a ordem causal.

Use conforme o problema:

- versão monotônica por agregado para updates/eventos daquele agregado;
- offset do log para posição em uma partição;
- ID único para deduplicação;
- timestamp UTC para observação humana e retenção;
- relógio monotônico local para medir duração.

Não compare timestamps de hosts como prova absoluta de causalidade. Se B foi
produzido ao processar A, carregue a relação por metadado/versão apropriado.

## CAP sem slogan

Quando existe uma partição de rede relevante, um sistema distribuído não pode
simultaneamente garantir a todos os lados resposta bem-sucedida e uma visão
linearizável única. Ele precisa rejeitar/esperar em algum lado ou aceitar estado
temporariamente divergente.

CAP não diz que um sistema é sempre “CP” ou “AP” para toda operação. Um produto
pode aceitar leitura obsoleta do catálogo e recusar confirmação de pagamento sem
quorum. Declare a escolha por operação e falha.

Latência existe mesmo sem partição. Metas de prazo também forçam escolhas entre
esperar por consistência e responder com informação possivelmente defasada.

## O problema do dual write

Este fluxo é incorreto quando ambos os efeitos precisam existir juntos:

```text
1. COMMIT do produto no PostgreSQL
2. publicar product.created no broker
```

Se o processo cai entre os passos, o produto existe sem evento. Inverter cria o
problema oposto: consumidor pode observar um produto que nunca confirmou. Retry
cego pode duplicar publicação.

Transações distribuídas existem em alguns ecossistemas, mas trazem requisitos de
coordenação, disponibilidade e operação. Não as presuma; escolha conscientemente
e entenda as garantias reais dos participantes.

## Transactional outbox

Grave a mudança e a intenção de publicar na mesma transação local:

```sql
BEGIN;

WITH changed AS (
    UPDATE product
    SET stock = stock - 1,
        version = version + 1
    WHERE id = :id
      AND stock >= 1
      AND version = :expected_version
    RETURNING id, stock, version
)
INSERT INTO outbox_event (
    event_id, aggregate_id, aggregate_version,
    event_type, schema_version, payload, occurred_at
)
SELECT
    :event_id,
    id,
    version,
    'stock.adjusted',
    1,
    jsonb_build_object('delta', -1, 'newStock', stock),
    CURRENT_TIMESTAMP
FROM changed
RETURNING aggregate_version;

COMMIT;
```

A aplicação precisa exigir exatamente uma linha retornada. Zero linhas
significa produto ausente, estoque insuficiente ou versão obsoleta; nesse caso,
ela aborta a transação e não confirma evento algum. O `INSERT ... SELECT` impede
que a intenção de publicação exista sem a mudança correspondente.

Um relay publica depois. Propriedades e obrigações:

- estado e intenção de publicar são atômicos localmente;
- mais de um worker precisa coordenar claim do lote;
- publicação pode repetir;
- `event_id` permanece estável em todo retry;
- tentativas usam backoff e chegam a uma política de falha;
- idade do evento mais antigo é monitorada;
- retenção/limpeza não remove evento ainda necessário.

Padrões de relay incluem polling com locking apropriado ou captura de mudanças
do log do banco. A escolha altera latência, operação e acoplamento, não a
necessidade de consumidor idempotente.

## Inbox e consumidor idempotente

Um consumidor pode registrar IDs processados na mesma transação do efeito:

```sql
BEGIN;

WITH claimed AS (
    INSERT INTO consumed_event (consumer_name, event_id, consumed_at)
    VALUES (:consumer, :event_id, CURRENT_TIMESTAMP)
    ON CONFLICT DO NOTHING
    RETURNING 1
),
applied AS (
    UPDATE product_projection
    SET stock = :new_stock,
        version = :aggregate_version
    WHERE product_id = :aggregate_id
      AND version + 1 = :aggregate_version
      AND EXISTS (SELECT 1 FROM claimed)
    RETURNING 1
)
SELECT
    EXISTS (SELECT 1 FROM claimed) AS is_new,
    EXISTS (SELECT 1 FROM applied) AS was_applied;

COMMIT;
```

A aplicação interpreta o resultado antes do commit:

- `is_new=false`: duplicata; confirma sem repetir o efeito;
- `is_new=true` e `was_applied=true`: próxima versão aplicada;
- `is_new=true` e `was_applied=false`: versão com lacuna, agregada ausente ou
  conflito; faz rollback para desfazer também o claim e agenda
  espera/reconstrução.

A operação exata depende do banco. O princípio é que deduplicação e efeito
compartilhem commit, e que zero linhas alteradas nunca seja aceito como sucesso.
Guardar IDs em memória perde proteção no restart. Para o primeiro evento de um
agregado, crie a projeção com uma operação condicional equivalente.

### Idempotência natural e artificial

- definir projeção para a versão 8 apenas se a atual for menor pode ser
  naturalmente idempotente;
- incrementar saldo em `delta` exige deduplicação por evento;
- enviar e-mail não possui rollback real; registre o comando de envio com ID
  idempotente e aceite a garantia do provedor.

## “Exactly once” e o limite da promessa

Um broker pode oferecer exactly-once dentro de um escopo específico, como seu
log e seus produtores/consumidores cooperantes. Isso não torna automaticamente
atômico um efeito externo em banco, e-mail ou pagamento.

Em sistemas práticos, busque:

```text
entrega ao menos uma vez
+ identidade estável
+ efeito idempotente
+ reconciliação
= resultado de negócio efetivamente uma vez dentro do escopo declarado
```

Documente o escopo: “uma reserva por `reservationId`” é verificável; “tudo
exactly once” não é.

## Ordenação de eventos

Ordem global costuma ser cara e desnecessária. Muitas invariantes precisam
apenas de ordem por agregado. Particione mensagens por `aggregate_id` quando o
broker e o volume permitirem.

Mesmo assim, reprocessamento e integrações podem produzir eventos atrasados.
Inclua `aggregate_version` e trate:

- versão igual: duplicata;
- próxima versão: aplicar;
- versão menor: evento antigo, ignorar/auditar;
- versão maior com lacuna: esperar, buscar/reconstruir ou alertar.

Não use timestamp como único critério de last-write-wins em dados que não podem
perder alteração. Uma política de conflito precisa refletir o domínio.

## Schema e envelope de evento

```json
{
  "eventId": "evt_01J8D1...",
  "type": "stock.adjusted",
  "schemaVersion": 1,
  "aggregateId": "prd_42",
  "aggregateVersion": 8,
  "occurredAt": "2026-09-29T18:00:00Z",
  "correlationId": "ord_17",
  "causationId": "cmd_88",
  "payload": {
    "delta": -2,
    "newStock": 8
  }
}
```

- `eventId` identifica o fato para deduplicação;
- `aggregateVersion` ajuda a ordenar por entidade;
- `correlationId` liga uma jornada;
- `causationId` aponta a causa imediata;
- `schemaVersion` pertence ao contrato do evento;
- `occurredAt` registra quando o fato foi confirmado no modelo adotado.

Não coloque access token, senha ou dado pessoal desnecessário no evento. Filas
e logs possuem retenção e audiência diferentes da resposta HTTP.

### Evolução compatível

- adicione campo opcional com default semântico claro;
- consumidores toleram campos adicionais;
- não reutilize nome antigo com significado novo;
- preserve eventos históricos ou mantenha upcaster quando necessário;
- teste produtor e consumidores antes de publicar;
- versionamento não substitui janela de coexistência;
- retire versão somente com telemetria e política.

Eventos são fatos no passado. `ProductCreated` não deve mandar outro serviço
“criar produto” de modo disfarçado. Um comando tem destinatário e pode ser
rejeitado; um evento anuncia algo que já ocorreu.

## Sagas

Uma saga divide uma transação de negócio em transações locais:

```text
pedido criado
  -> reservar estoque
  -> autorizar pagamento
  -> confirmar expedição
```

Falha no pagamento pode liberar a reserva. Isso é uma **compensação**, não um
rollback: o histórico de reserva e liberação continua existindo. Reembolso é um
novo fato e pode falhar separadamente.

Para cada passo defina:

| Item | Pergunta |
|---|---|
| comando | qual intenção e ID idempotente? |
| sucesso | qual fato confirma conclusão? |
| timeout | quando o estado vira desconhecido? |
| consulta | como descobrir o resultado depois? |
| retry | quais falhas, limite e backoff? |
| compensação | qual novo fato reduz o efeito? |
| falha da compensação | quem tenta e quando escala? |
| intervenção manual | qual fila, contexto e auditoria? |

### Orquestração e coreografia

- **orquestrada:** um componente persiste o estado e envia o próximo comando;
  facilita visualizar fluxo, mas centraliza coordenação;
- **coreografada:** serviços reagem a eventos; reduz coordenador explícito, mas
  o fluxo pode ficar difícil de entender e mudar.

Persistir o estado da saga evita perder o progresso em restart. Evite uma cadeia
longa de eventos sem dono que ninguém consegue explicar em incidente.

## Replicação

### Leader e followers

Escritas passam pelo leader; followers replicam e podem servir leitura. Questões:

- qual perda é possível no failover?
- commit espera quantas réplicas?
- quanto lag é aceitável para cada leitura?
- como oferecer read-your-writes?
- como detectar split-brain/fencing conforme a tecnologia?

Após escrita, o cliente pode ler do leader por uma janela, carregar um token de
posição e esperar a réplica alcançá-lo, ou aceitar resposta defasada sinalizada.

### Multi-leader

Aceita escrita em múltiplas regiões, aumentando conflitos. Defina resolução
por entidade: merge, dono por região, versão causal, CRDT aplicável ou rejeição.
Last-write-wins pode perder dado e depende de relógio; use somente quando essa
semântica é aceitável.

### Leaderless e quorums

Em um modelo simplificado com `N` réplicas, escrita confirmada por `W` e leitura
de `R`, `R + W > N` favorece sobreposição de quorums. Isso não garante sozinho
linearizabilidade: sloppy quorum, escrita concorrente, clock, reparo e falhas do
sistema real importam. Use a documentação da tecnologia, não apenas a fórmula.

## Particionamento e sharding

Shard key decide distribuição, localidade e consultas eficientes.

| Escolha | Risco |
|---|---|
| timestamp crescente puro | todas as escritas chegam ao shard atual |
| baixa cardinalidade | poucas partições e hotspots |
| hash do ID | distribui bem, perde consultas por faixa/localidade |
| tenant | tenant grande pode dominar um shard |
| chave composta | mais flexível, exige consulta alinhada |

Antes de escolher, estime cardinalidade, crescimento, skew, operações por
chave e necessidade de consulta cross-shard. Planeje:

- roteamento e metadata;
- rebalanceamento sem indisponibilidade excessiva;
- chave quente e tenant excepcional;
- unicidade global ou por shard;
- transação e join cross-shard;
- backup/restore por shard;
- resharding futuro.

Adicionar shards não corrige automaticamente uma query sem índice; pode apenas
executá-la em mais lugares.

## Cache e invalidação

Cache adiciona outra cópia distribuída. Defina:

- chave incluindo tenant, versão de representação e variações;
- TTL e stale aceitável;
- cache-aside, write-through ou outra estratégia;
- comportamento na queda do cache;
- prevenção de stampede;
- invalidação após escrita;
- se resultado negativo pode ser cacheado;
- limites para impedir uso de cache como armazenamento ilimitado.

Cache-aside possui janela entre commit e invalidação. Uma chave versionada ou
evento pode reduzir a janela, mas falhas ainda exigem TTL/reconciliação.

## Reconciliação

Reconciliação compara fonte de verdade e projeção por ID/versão:

```text
para cada faixa de IDs/tempo:
  ler versão da fonte
  ler versão da projeção
  se ausente/antiga: reconstruir ou republicar
  se inesperadamente nova/divergente: isolar e alertar
  registrar checkpoint e contagem
```

Ela deve ser:

- idempotente e retomável;
- paginada e limitada para não derrubar produção;
- observável por progresso, divergência e erro;
- auditável em toda correção;
- testada com dados ausentes, duplicados e fora de ordem.

Reconciliação é parte da arquitetura, não um script improvisado depois do
incidente.

## Backup, restauração e desastre

Replicação não é backup: uma deleção ou corrupção pode ser replicada.

- **RPO:** quanto dado confirmado o negócio aceita perder;
- **RTO:** quanto tempo a recuperação pode levar.

Alinhe snapshot, log, retenção, região e runbook a esses objetivos. Teste
restore, integridade, credenciais, chaves e retomada de consumidores. Ao voltar
um banco para um ponto anterior, eventos e sistemas derivados podem estar à
frente; planeje a reconciliação do conjunto, não apenas de um banco.

## Matriz de falhas distribuídas

| Falha | Risco | Mecanismo |
|---|---|---|
| resposta perdida após commit | efeito duplicado no retry | chave idempotente |
| queda entre estado e mensagem | evento ausente | outbox |
| confirmação do broker perdida | evento duplicado | inbox/efeito idempotente |
| evento fora de ordem | projeção regressiva | versão por agregado |
| réplica atrasada | leitura antiga | roteamento/token/sinalização |
| partição de rede | divergência ou indisponibilidade | política por operação |
| chave quente | latência/saturação | reparticionamento/limite/modelagem |
| saga parada | recurso reservado indefinidamente | timeout, retry, fila manual |
| projeção divergente | decisão com dado incorreto | reconciliação |
| restore parcial | sistemas em eras diferentes | plano de desastre integrado |

## Invariantes distribuídas

- todo comando repetível possui ID estável e escopo;
- todo evento possui ID, tipo, versão e agregado;
- efeito e deduplicação do consumidor compartilham commit quando possível;
- uma versão antiga nunca sobrescreve uma projeção mais nova;
- lag e backlog possuem SLO e alerta;
- toda compensação também é idempotente;
- estado desconhecido pode ser consultado e reconciliado;
- nenhum componente promete uma garantia mais forte que suas dependências.

## Exercícios

1. Modele cinco resultados possíveis de um timeout depois de enviar comando.
2. Force queda entre produto e publicação no desenho de dual write.
3. Implemente outbox e prove recuperação depois do restart.
4. Publique o mesmo evento duas vezes e prove apenas um efeito de negócio.
5. Entregue versões `2`, `1`, `3`, `3` e documente o estado da projeção.
6. Projete saga de reserva, pagamento e expedição com compensações.
7. Defina read-your-writes quando leituras normalmente usam follower.
8. Compare três shard keys usando volume e consultas esperadas.
9. Evolua o schema de `stock.adjusted` sem quebrar consumidor antigo.
10. Escreva reconciliador retomável para fonte e projeção.
11. Simule restore da fonte para um ponto anterior e planeje convergência.
12. Declare RPO/RTO e teste se backup atual realmente os atende.

## Critérios de conclusão

- cada operação declara consistência e comportamento sob timeout/partição;
- nenhum dual write crítico depende de duas chamadas sem recuperação;
- duplicatas e reordenação possuem testes determinísticos;
- consumidores sobrevivem a restart sem perder deduplicação;
- saga persiste estado, possui timeout e escala falha de compensação;
- escolha de réplica/shard está ligada a consultas e invariantes reais;
- backlog, lag e divergência são mensuráveis;
- reconciliação e restore foram executados, não apenas documentados;
- toda promessa de “uma vez” informa exatamente seu escopo.

## Checklist de revisão

- [ ] Trato timeout como resultado desconhecido.
- [ ] Distingo isolamento local de consistência entre sistemas.
- [ ] Uso outbox e consumidor idempotente onde existe dual write.
- [ ] Eventos carregam identidade, versão e causalidade suficientes.
- [ ] Ordenação necessária está definida por agregado/partição.
- [ ] Replicação, lag e read-your-writes possuem política explícita.
- [ ] Shard key foi avaliada com distribuição e consultas.
- [ ] Existe reconciliação, backup e restore testado.
