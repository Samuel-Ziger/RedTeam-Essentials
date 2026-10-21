# NoSQL: modelos, distribuição e decisões

“NoSQL” agrupa bancos com modelos e garantias muito diferentes. Não significa
“sem SQL”, “sem schema”, “mais rápido” nem “escala infinita”. Uma escolha
profissional começa pelas operações, invariantes, volume, distribuição e custo
operacional; o nome do produto vem depois.

O objetivo não é substituir automaticamente PostgreSQL. É reconhecer quando
chave-valor, documento, wide-column, grafo, busca ou série temporal representa
melhor um padrão de acesso — e assumir conscientemente o que se perde.

## Objetivos

Ao concluir, você deverá conseguir:

- distinguir as principais famílias sem tratá-las como intercambiáveis;
- modelar a partir de agregado, consulta e chave de partição;
- analisar atomicidade e consistência por operação;
- reconhecer hot keys, hot partitions e crescimento sem limite;
- desenhar cache com invalidação, TTL e proteção contra stampede;
- planejar idempotência, retry, reconciliação e reparo;
- justificar persistência poliglota pelo ganho medido e custo total.

## 1. Todo dado útil possui schema

Mesmo quando o servidor aceita qualquer documento, a aplicação pressupõe:

- nomes e tipos de campos;
- campos obrigatórios e opcionais;
- identidade e unicidade;
- intervalo e unidade de valores;
- versão do formato;
- relações e ciclo de vida;
- operações atômicas permitidas;
- política de evolução.

Isto é schema, ainda que esteja no código, numa biblioteca de validação ou apenas
na cabeça da equipe. Schema implícito é mais difícil de descobrir e migrar.

Compare:

```json
{"price": 45.9}
```

```json
{
  "schemaVersion": 2,
  "price": {"amountMinor": 4590, "currency": "BRL"}
}
```

O segundo explicita unidade e versão. Ainda precisa de validação, limites e
regra de atualização.

## 2. A unidade de atomicidade orienta o modelo

Um agregado é o conjunto que precisa manter suas invariantes numa alteração.
Em banco documental, um documento costuma ser uma boa fronteira de atomicidade.
Em chave-valor, é frequentemente a chave. Em wide-column, pode ser uma partição
ou linha, dependendo do produto. Não assuma transação multidocumento/multichave:
verifique escopo, isolamento, limites e custo.

Perguntas:

1. quais campos mudam juntos?
2. qual conjunto é lido junto?
3. o conjunto tem limite de tamanho/cardinalidade?
4. há um único proprietário do agregado?
5. qual operação exige coordenação entre agregados?

Modelar “tudo do cliente” em um documento parece conveniente até pedidos,
eventos ou anexos crescerem sem limite e cada update mover um documento enorme.

## 3. Chave-valor

Modelo:

```text
session:01J... -> {
  userId,
  permissionsVersion,
  createdAt,
  expiresAt
}
```

Forças:

- acesso direto quando a chave é conhecida;
- baixa latência;
- TTL;
- contadores e estruturas atômicas específicas;
- cache, sessão, deduplicação e coordenação limitada.

Limitações:

- consultas arbitrárias por campo geralmente não são o objetivo;
- distribuição e expiração precisam de semântica;
- valores grandes/keys quentes concentram carga;
- persistência e replicação variam por configuração.

### Chave e namespace

Uma chave deve ser:

- determinística para a operação;
- limitada em tamanho;
- namespaced (`session:v2:<id>`);
- incapaz de colidir entre tenants;
- não derivada diretamente de segredo;
- distribuída o suficiente para evitar hot key.

Não inclua dado pessoal legível na chave: chaves aparecem em métricas, logs e
ferramentas operacionais.

### Operação atômica, não read-modify-write

Para contador, use incremento atômico oferecido pelo banco em vez de:

```text
GET counter -> 7
calcular 8
SET counter -> 8
```

Duas sessões poderiam gravar 8. Scripts/transactions condicionais podem agrupar
operações, mas sua semântica precisa ser estudada no produto.

## 4. Cache é uma cópia descartável

O cache acelera leitura; não deve ser a única fonte de um fato que não pode ser
perdido.

### Cache-aside

```text
1. GET cache
2. hit -> responder
3. miss -> ler fonte
4. preencher cache com TTL
5. responder
```

Na escrita, costuma-se confirmar a fonte e invalidar/atualizar o cache. Há
janelas de corrida: uma leitura antiga pode repopular depois da invalidação.
Versão no valor/chave, invalidação após commit e tolerância definida reduzem o
risco.

### Outros padrões

- **read-through:** cache carrega por meio de um componente integrado;
- **write-through:** escrita atualiza cache e armazenamento no caminho síncrono;
- **write-behind:** cache aceita e persiste depois; menor latência, maior risco;
- **refresh-ahead:** renova antes do vencimento para chaves previsíveis.

### Problemas obrigatórios

- **stampede:** muitos misses recalculam o mesmo valor; use single-flight/lock
  curto, TTL com jitter ou refresh antecipado;
- **avalanche:** muitas chaves expiram juntas; distribua TTL;
- **cache penetration:** consultas repetidas a ausentes; cache negativo curto,
  validação e rate limit;
- **stale data:** defina freshness máxima e invalidação;
- **eviction:** memória cheia remove valores antes do TTL;
- **poisoning:** chave/tenant/autorização incorretos expõem ou misturam dados.

Nunca reutilize resposta autorizada para um usuário sob uma chave que ignora
identidade/escopo. Não armazene segredo sem necessidade e proteção equivalentes
à fonte.

## 5. Documento

Um documento representa um agregado:

```json
{
  "_id": "order:o-123",
  "schemaVersion": 2,
  "customerSnapshot": {
    "id": "c-9",
    "displayName": "Cliente fictício"
  },
  "items": [
    {
      "sku": "BOOK-1",
      "quantity": 2,
      "unitPriceCents": 3500,
      "currency": "BRL"
    }
  ],
  "totalCents": 7000,
  "currency": "BRL",
  "status": "paid",
  "createdAt": "2026-10-03T12:00:00Z"
}
```

Duplicar `displayName` e preço pode ser correto: são snapshots da compra. Não
devem acompanhar automaticamente cadastro e preço atuais.

### Embutir quando

- dados pertencem ao mesmo agregado;
- são lidos/alterados juntos;
- cardinalidade e tamanho são limitados;
- atomicidade no documento atende a invariante;
- elemento não precisa de vida/consulta independente.

### Referenciar quando

- o conjunto cresce sem limite;
- item é compartilhado entre agregados;
- possui ciclo de vida próprio;
- atualização global da duplicata seria cara;
- consulta frequentemente começa pelo item;
- permissões/retention diferem.

Modelagem documental não elimina joins; ela decide quais joins são pagos na
escrita por duplicação e quais permanecem na leitura.

## 6. Wide-column

Em bancos wide-column distribuídos, o modelo começa pela consulta:

```text
consulta:
  eventos de um dispositivo em um dia, ordenados por instante

partition key:
  (device_id, event_date)

clustering/order:
  occurred_at, event_id
```

Uma tabela conceitual:

```text
device_id | event_date | occurred_at | event_id | payload
```

A chave de partição decide onde os dados vivem. Ela deve distribuir carga e
manter a consulta em poucas partições.

Riscos:

- **hot partition:** uma chave recebe volume desproporcional;
- **unbounded partition:** a partição cresce sem limite;
- partição minúscula em excesso gera overhead;
- consulta ad hoc fora da chave exige scan/índice/projeção adicional;
- mesma informação é duplicada em tabelas orientadas a consultas diferentes.

Bucket temporal reduz crescimento, mas escolha dia/hora pela carga real. Uma
celebridade, tenant gigante ou dispositivo defeituoso ainda pode ser quente;
salting/sharding adicional complica leitura e ordenação.

## 7. Grafo

Grafo modela vértices, arestas e propriedades como elementos de primeira classe:

```text
(person)-[:MEMBER_OF]->(team)
(team)-[:CAN_ACCESS]->(resource)
```

É útil quando o valor está em travessias variáveis:

- caminhos e rotas;
- dependências;
- autorização com relações complexas;
- detecção de comunidades ou padrões de fraude;
- recomendação baseada em conexões.

Se toda pergunta é “pedidos de um cliente” ou “pai imediato de uma categoria”,
foreign key e CTE recursiva podem ser mais simples. Bancos de grafo também
precisam de índices de ponto de partida; começar a travessia sem seletividade
pode explorar uma parcela enorme do grafo.

Defina profundidade, direção, ciclos, limite de resultado e custo máximo.

## 8. Busca

Um motor de busca mantém índice invertido:

```text
termo -> documentos/posições/frequências
```

Oferece:

- tokenização e análise linguística;
- relevância/ranking;
- stemming, sinônimos e autocomplete;
- facets/agregações;
- consulta textual distribuída.

Normalmente é uma **projeção**, não fonte de verdade. Depois de escrever na
fonte, refresh e replicação criam janela antes de o item aparecer. Defina:

- atraso aceitável;
- idempotência da indexação;
- alias/versionamento para reindex;
- reconstrução integral;
- reconciliação por contagem/hash/amostra;
- comportamento quando busca está indisponível.

Não use resultado de busca desatualizado para decidir saldo, autorização ou
unicidade.

## 9. Série temporal

Métricas e medidas no tempo pedem:

- ingestão alta e predominantemente append;
- filtros por intervalo;
- agregações por janela;
- retenção/downsampling;
- compressão;
- labels/dimensões.

```text
measurement: http_request_duration
labels: service, route, status_class
timestamp: ...
value: ...
```

Não use user ID, request ID ou URL completa como label de métrica: cardinalidade
explode memória e índice. Valores de alta cardinalidade pertencem a logs/traces
com política apropriada.

Eventos podem chegar atrasados ou fora de ordem. Defina watermark, correção,
timezone e diferença entre event time e ingestion time.

## 10. Particionamento, sharding e replicação

- **particionamento:** divide dados por regra;
- **sharding:** distribui partições por nós administrativos/físicos;
- **replicação:** mantém cópias para disponibilidade/leitura;
- **rebalancing:** move partições quando topologia/carga muda.

Uma chave de shard afeta:

- distribuição de escrita;
- consultas que tocam um ou vários nós;
- transações;
- unicidade;
- crescimento e rebalancing;
- isolamento de tenant.

Chave monotônica pode concentrar novas escritas; chave puramente aleatória
distribui, mas destrói localidade de intervalo. Hash + bucket/range combina
trade-offs, ao custo de consulta mais complexa.

### Hot key e “celebrity problem”

Mesmo distribuição uniforme no conjunto não impede uma chave muito popular.
Estratégias incluem:

- cache local/edge para leitura;
- replicar valor imutável;
- dividir contadores e agregar;
- rate limit/backpressure;
- isolar tenant quente;
- pré-computar projeção.

Cada estratégia altera freshness ou complexidade. Meça o skew, não apenas o
volume total.

## 11. Consistência por operação

Pergunte concretamente:

- após escrever, o mesmo cliente lê a própria versão?
- outro cliente pode ler versão anterior? Por quanto tempo observado?
- confirmação exige quantas réplicas?
- se líder cai após aplicar e antes de responder, o resultado é incerto?
- conflitos concorrentes são rejeitados, mesclados ou “último vence”?
- alteração de múltiplos itens é atômica?
- retry repete efeito?

### Quorum não é fórmula universal

Em alguns sistemas replicados, lê-se a heurística `R + W > N`. Ela depende de
premissas: réplicas sobrepostas, resolução/versionamento, membership, falhas e
implementação. Não conclua “fortemente consistente” apenas pelos números.
Consulte a garantia concreta do produto e configuração.

### Last-write-wins

“Última escrita vence” precisa definir último por qual relógio. Clock skew pode
fazer escrita posterior perder. Mesmo com timestamp coordenado, descartar uma
edição concorrente pode ser semanticamente errado. Versão condicional, CRDT ou
resolução de domínio atendem casos diferentes.

### Consistência eventual exige mecanismo

Convergência não acontece por desejo. Um pipeline robusto possui:

- evento durável;
- ID único e consumidor idempotente;
- retry com backoff e limite;
- fila/registro de falhas persistentes;
- observabilidade de atraso;
- reprocessamento;
- reconciliação periódica com a fonte;
- procedimento para rebuild.

“Eventualmente” também precisa de SLO: por exemplo, 99% das projeções em até
30 segundos, com alerta acima de 5 minutos.

## 12. Idempotência e deduplicação

Entrega “at least once” pode repetir mensagem. Uma operação idempotente produz o
mesmo efeito observável quando repetida com a mesma intenção.

Estratégias:

- ID do evento com constraint/registro de processado;
- upsert condicional por versão;
- chave de idempotência ligada ao hash do comando;
- operação natural como “definir status” em vez de “alternar status”;
- compare-and-set.

Deduplicação com TTL só protege dentro da janela. Se uma mensagem antiga pode
reaparecer depois, a retenção da chave deve cobrir esse cenário ou o efeito
precisa ser naturalmente idempotente.

## 13. Persistência poliglota e custo total

Adicionar um banco cria trabalho contínuo:

- provisionamento, patch e upgrade;
- driver, pool e compatibilidade;
- autenticação, autorização e rotação de segredo;
- backup e restore;
- replicação e disaster recovery;
- observabilidade e capacity planning;
- schema/versionamento;
- desenvolvimento local e CI;
- resposta a incidente;
- consistência entre cópias e direito de apagamento.

Scorecard antes da decisão:

| Critério | Pergunta verificável |
|---|---|
| Invariante | qual operação precisa ser atômica? |
| Acesso | quais queries e distribuições dominam? |
| Escala | volume, throughput, picos e crescimento? |
| Consistência | qual leitura pode estar obsoleta? |
| Operação | equipe sabe restaurar e atualizar? |
| Segurança | como isola tenant e audita acesso? |
| Custo | infraestrutura + pessoas + migração? |
| Saída | como exportar/reconstruir os dados? |

Faça um benchmark pequeno com distribuição realista, incluindo falha e escrita.
Benchmark do fornecedor com payload diferente não prova adequação.

## 14. Segurança e privacidade

O modelo NoSQL não reduz os controles:

- autenticação forte e TLS;
- menor privilégio por serviço;
- rede restrita;
- limites de consulta, documento e resultado;
- validação de operadores/estrutura recebidos;
- proteção contra NoSQL injection;
- criptografia e rotação;
- log sem segredo/payload pessoal;
- backup protegido e testado;
- retenção e remoção em fonte, cache e projeções.

Nunca passe um objeto de filtro vindo do cliente diretamente ao driver. Construa
uma consulta a partir de campos e operadores em allowlist.

## 15. Erros recorrentes

- escolher NoSQL para “não ter schema”;
- modelar entidades sem começar pelas consultas;
- criar documento ou partição de crescimento ilimitado;
- usar cache como fonte canônica;
- ignorar hot keys porque o hash distribui chaves comuns;
- chamar busca de consistente sem medir refresh;
- usar quorum/last-write-wins como slogan;
- presumir exactly-once sem idempotência e reconciliação;
- duplicar fatos sem dono nem rebuild;
- adicionar bancos antes de demonstrar insuficiência da solução atual;
- ignorar deleção de dados em caches, backups e projeções.

## 16. Exercícios progressivos

### Nível 1 — classificação

Escolha e justifique o modelo inicial para:

1. sessão com TTL;
2. ledger financeiro;
3. catálogo textual;
4. telemetria de dispositivos;
5. caminho de autorização em relações;
6. pedido com itens históricos.

Liste também por que uma alternativa seria inadequada.

### Nível 2 — modelagem por acesso

Para um feed fictício:

1. escreva as três consultas críticas;
2. escolha partition/clustering keys;
3. estime tamanho máximo da partição;
4. identifique usuário celebridade;
5. desenhe fan-out on write e fan-out on read com seus trade-offs.

### Nível 3 — cache e consistência

1. desenhe cache-aside para catálogo com TTL e jitter;
2. reproduza a corrida de invalidação/repopulação;
3. adicione versão e single-flight;
4. escreva o SLO de freshness;
5. explique por que o mesmo desenho não serve automaticamente para saldo.

### Nível 4 — operação

Desenhe fonte relacional e projeção de busca/documento:

- contrato de evento e versão;
- deduplicação;
- retry e erro persistente;
- métrica de lag;
- reconciliação;
- rebuild;
- exclusão de dado pessoal;
- comportamento durante indisponibilidade.

Produza uma ADR comparando uma base única com persistência poliglota.

## Critério de conclusão

- [ ] Diferencio modelo chave-valor, documento, wide-column, grafo, busca e série temporal.
- [ ] Para cada escolha, documento agregado, chave e limite de crescimento.
- [ ] Sei localizar hot key/partition e explicar a mitigação.
- [ ] Cache possui fonte, TTL, invalidação, stampede e regra de autorização.
- [ ] Consistência é descrita por operação e falha, não por rótulo.
- [ ] Retry possui idempotência; projeção possui reconciliação/rebuild.
- [ ] O custo operacional de cada banco aparece na decisão.
- [ ] Segurança, retenção e exclusão cobrem todas as cópias.
- [ ] A ADR mostra evidência, alternativa e condição de revisão.

O próximo capítulo aplica essas decisões a um banco documental específico:
[MongoDB em profundidade](07-mongodb.md).
