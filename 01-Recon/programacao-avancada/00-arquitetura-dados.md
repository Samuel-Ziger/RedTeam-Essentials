# Arquitetura de dados e persistência

Este capítulo parte de uma pergunta anterior à escolha de PostgreSQL, MongoDB
ou qualquer outro produto: **qual estado o sistema precisa preservar e quais
garantias cada operação exige?** O módulo 00 já apresentou programas, arquivos,
HTTP e processos. Aqui esses fundamentos passam a ser tratados como um sistema
de dados que continuará correto sob concorrência, reinício e falha parcial.

## Objetivos

Ao concluir, você deverá conseguir:

- separar dado, informação, estado, evento, comando e projeção;
- transformar regras de negócio em invariantes verificáveis;
- reconhecer os componentes essenciais de um SGBD;
- comparar modelos de persistência por padrão de acesso e garantia;
- definir fonte de verdade, RPO, RTO e procedimento de restauração;
- raciocinar sobre consistência e disponibilidade sem reduzir CAP a um slogan;
- registrar uma decisão de arquitetura com premissas e consequências.

## 1. Dado não é significado

O valor `42` isolado não informa se representa reais, centavos, itens, graus ou
uma versão. Um dado útil possui pelo menos:

- **tipo:** inteiro, texto, instante, identificador, documento;
- **unidade:** centavos, bytes, metros, UTC;
- **identidade:** a entidade ou ocorrência à qual pertence;
- **contexto temporal:** quando era verdadeiro e quando foi registrado;
- **proveniência:** quem ou qual processo o produziu;
- **regra:** quais valores e transições são permitidos.

Compare os registros:

```json
{"productId":"p-17","stock":8}
```

```json
{
  "productId": "p-17",
  "quantity": 8,
  "unit": "item",
  "observedAt": "2026-10-03T14:25:00Z",
  "source": "inventory-ledger-v2"
}
```

O segundo ainda não é automaticamente verdadeiro, mas contém informação
suficiente para interpretação e auditoria. Em sistemas reais, boa parte dos
erros atribuídos ao banco nasce de semântica indefinida na aplicação.

### Estado, comando e evento

- **Estado** descreve o que o sistema considera verdadeiro agora: estoque 8.
- **Comando** pede uma mudança e pode ser rejeitado: reservar 2 unidades.
- **Evento** registra algo que já ocorreu: 2 unidades foram reservadas.
- **Consulta** pede uma representação sem intenção de alterar estado.

Não confunda evento com comando. `ReserveStock` pode falhar; somente depois da
mudança confirmada faz sentido publicar `StockReserved`. Também não trate toda
linha alterada como evento de domínio: um evento precisa de significado,
identidade, instante e política de evolução.

## 2. Comece pelas invariantes

Uma **invariante** é uma condição que deve continuar verdadeira antes e depois
de toda operação válida. Exemplos do domínio de inventário:

```text
I1: um SKU identifica no máximo um produto
I2: price_cents >= 0
I3: stock >= 0
I4: version aumenta exatamente uma unidade a cada alteração do produto
I5: todo movimento pertence a um produto existente
I6: a soma dos movimentos reconciliáveis explica o saldo materializado
```

Invariantes diferentes podem exigir mecanismos diferentes:

| Invariante | Proteção adequada | Por que |
|---|---|---|
| SKU único | `UNIQUE` no banco | cobre todos os escritores concorrentes |
| preço não negativo | tipo + `CHECK` + validação de entrada | protege armazenamento e melhora o erro HTTP |
| estoque não negativo | atualização condicional na transação | leitura seguida de escrita separada sofre corrida |
| versão monotônica | expressão atômica `version = version + 1` | evita cálculo com valor obsoleto |
| evento publicado após commit | outbox transacional | elimina janela entre commit e publicação |

Validar apenas na interface não basta: outro processo, migration ou console
administrativo pode escrever diretamente. Validar apenas no banco também não é
ideal: a aplicação deve devolver erro de domínio compreensível. As camadas são
complementares, e a regra crítica deve terminar em uma proteção atômica.

### Perguntas de descoberta

Antes de desenhar tabelas ou coleções, responda:

1. Quais fatos existem e quem é o dono de cada um?
2. Quais transições são válidas? Há uma máquina de estados?
3. Quais regras cruzam mais de uma entidade?
4. Quais consultas sustentam caminhos críticos?
5. Qual volume atual, crescimento, distribuição e retenção?
6. A carga é dominada por leitura, escrita ou varredura analítica?
7. Qual latência de cauda é aceitável (`p95`, `p99`), não apenas a média?
8. Quanto dado desatualizado cada operação tolera?
9. Quais dados são pessoais, secretos, regulados ou apagáveis?
10. O que acontece se processo, nó, zona ou região falhar?

Uma resposta como “precisa ser rápido e escalável” não é requisito mensurável.
Prefira: “95% das consultas por SKU terminam em até 80 ms, com 300 operações
por segundo e leitura imediatamente posterior à própria escrita”.

## 3. Do processo ao SGBD

Um dicionário em memória desaparece ao terminar o processo. Um arquivo oferece
persistência, mas deixa para a aplicação concorrência, busca, integridade,
recuperação e evolução de formato. Um Sistema Gerenciador de Banco de Dados
(SGBD) concentra mecanismos difíceis de implementar corretamente.

Em uma consulta relacional, o caminho simplificado é:

```text
SQL recebido
  -> parser valida a gramática
  -> binder resolve tabelas, colunas e tipos
  -> rewriter aplica regras/views
  -> otimizador estima cardinalidades e escolhe plano
  -> executor acessa heap e índices
  -> controle transacional decide quais versões são visíveis
  -> resultado é codificado e enviado pelo protocolo
```

Componentes importantes:

- **catálogo:** metadados de schemas, tipos, constraints e permissões;
- **buffer pool:** mantém páginas acessadas na memória;
- **índices:** estruturas auxiliares para localizar ou ordenar registros;
- **WAL/journal:** registra mudanças antes das páginas finais, permitindo
  recuperação após falha;
- **controle de concorrência:** locks, versões ou combinação dos dois;
- **checkpoints e vacuum/compactação:** limitam recuperação e recuperam espaço;
- **replicação:** mantém cópias com garantias específicas;
- **autenticação, autorização e auditoria:** controlam e registram acesso.

O `COMMIT` não significa necessariamente “todas as páginas de dados já foram
reescritas”. Em um banco com write-ahead log, significa que o registro durável
necessário à recuperação foi confirmado conforme a configuração. A garantia
real depende de `fsync`, hardware, replicação e política de confirmação.

## 4. Modelos de persistência

“Banco SQL versus NoSQL” é uma comparação pobre. Compare o modelo, as
operações e as garantias concretas.

| Família | Unidade/modelo | Ponto forte | Custo ou risco típico |
|---|---|---|---|
| Relacional | relações, linhas e constraints | integridade, joins, transações e consulta ad hoc | migrations e escala exigem disciplina |
| Documento | agregado BSON/JSON-like | recuperar e alterar um agregado junto | duplicação e documentos sem limite |
| Chave-valor | chave → valor/estrutura | acesso direto, TTL e baixa latência | consultas secundárias limitadas |
| Wide-column | partição e clustering key | escrita distribuída orientada à consulta | hot partitions e duplicação por consulta |
| Grafo | vértices e arestas | travessias variáveis e relações de primeira classe | operação e linguagem especializadas |
| Busca | índice invertido | texto, ranking, facets e relevância | atualização assíncrona; não é ledger |
| Série temporal | medida + tempo + labels | retenção, compressão e janelas temporais | cardinalidade explosiva de labels |
| Objeto/blob | objeto opaco por chave | arquivos grandes, durabilidade e custo | sem consulta interna transacional |

Um mesmo produto pode combinar modelos: PostgreSQL como fonte canônica,
Redis para cache efêmero, MongoDB para uma projeção documental e um motor de
busca para texto. Isso se chama persistência poliglota, não ausência de schema.
Cada novo mecanismo adiciona backup, monitoramento, atualização, driver,
permissões, custo e um novo modo de falha.

### Heurística de escolha

1. Escreva invariantes e padrões de acesso.
2. Escolha o modelo mais simples que os atende.
3. Verifique atomicidade e consistência por operação.
4. Teste com volume e concorrência representativos.
5. Calcule o custo operacional, não apenas a latência do benchmark.
6. Registre por que a alternativa padrão não foi suficiente.

Não adote um segundo banco para evitar aprender o primeiro. Adote-o quando uma
necessidade medida supera de forma clara a complexidade adicional.

## 5. Fonte de verdade, projeção e cache

A **fonte de verdade** (system of record) é o local autorizado a decidir o
valor de um fato. Uma **projeção** reorganiza fatos para outra leitura. Um
**cache** pode ser descartado e reconstruído sem perder fatos canônicos.

No projeto desta trilha:

```text
PostgreSQL: produto, saldo, movimento e outbox (canônicos)
       |
       | worker lê evento confirmado
       v
MongoDB: histórico documental para consulta (projeção)
```

MongoDB não deve aceitar uma alteração independente do estoque. Se duas bases
forem donas do mesmo fato, uma partição de rede produz duas verdades e exige
uma regra explícita de resolução.

O fluxo de outbox resolve uma janela clássica:

```text
ERRADO
1. COMMIT do produto
2. processo cai antes de publicar evento       -> evento perdido

ERRADO
1. publica evento
2. ROLLBACK da alteração                       -> evento fantasma

OUTBOX
1. altera produto + insere evento na mesma transação
2. COMMIT de ambos
3. worker publica com retry e consumidor idempotente
```

A outbox garante registro conjunto, não exatamente uma entrega. A publicação
pode ocorrer mais de uma vez; o consumidor deve deduplicar por `eventId` ou
tornar o efeito idempotente. Também são necessários monitoramento de atraso,
retenção e reconciliação.

## 6. Durabilidade, alta disponibilidade e backup

São propriedades distintas:

- **durabilidade:** mudanças confirmadas sobrevivem às falhas cobertas;
- **alta disponibilidade:** o serviço continua acessível dentro de um cenário;
- **backup:** cópia recuperável em outro momento/domínio de falha;
- **replicação:** cópia continuamente atualizada, que também pode replicar uma
  exclusão ou corrupção;
- **archive:** retenção longa, normalmente imutável e orientada a conformidade.

Um volume Docker não é backup. Uma réplica na mesma máquina também não protege
contra falha do host. Uma estratégia precisa definir:

- **RPO (Recovery Point Objective):** perda máxima de dados tolerada;
- **RTO (Recovery Time Objective):** tempo máximo para restaurar o serviço;
- escopo e frequência da cópia;
- criptografia, acesso, retenção e localização;
- restore completo e recuperação ponto no tempo, quando aplicável;
- teste periódico com evidência de integridade e tempo real.

Exemplo: “RPO de 5 minutos e RTO de 60 minutos” exige que a arquitetura produza
e preserve material de recuperação nessa janela. Declarar valores sem executar
um restore cronometrado é apenas intenção.

## 7. Consistência em sistemas distribuídos

Consistência não é uma opção binária. Algumas garantias comuns:

- **linearizabilidade:** operações parecem ocorrer instantaneamente entre
  invocação e resposta, respeitando ordem real;
- **serializabilidade:** resultado equivale a alguma execução serial de
  transações, sem necessariamente respeitar ordem de relógio externo;
- **read-your-writes:** um cliente observa as próprias escritas confirmadas;
- **monotonic reads:** o cliente não volta a uma versão mais antiga;
- **eventual:** sem novas escritas, as réplicas convergem sob as premissas do
  sistema — não garante prazo nem corrige eventos perdidos por si só.

### CAP com a premissa correta

CAP se aplica quando há **partição de comunicação** entre nós. Nesse período,
um sistema distribuído não pode oferecer simultaneamente:

- consistência linearizável para todas as operações; e
- resposta bem-sucedida de todos os nós não falhos a toda requisição.

“CP” ou “AP” não descreve todas as operações de um produto para sempre. Um
banco pode aceitar escrita com quorum, permitir leitura local obsoleta e ter
configurações diferentes por operação. A pergunta útil é: durante uma partição,
esta leitura ou escrita falha, espera ou responde potencialmente obsoleta?

PACELC lembra outro trade-off: **se** há partição, disponibilidade versus
consistência; **caso contrário**, latência versus consistência. Mesmo sem falha,
esperar confirmação de réplicas distantes custa tempo.

### Relógios e identificadores

Relógios de máquinas divergem. “Último timestamp vence” pode perder uma escrita
válida quando o relógio está incorreto. Use relógio para observabilidade, mas
não assuma que ele cria ordem causal global. Versões, sequências, tokens de
concorrência e clocks lógicos resolvem problemas específicos de ordenação.

## 8. Erros de arquitetura recorrentes

- escolher tecnologia antes de descobrir invariantes e consultas;
- chamar réplica, volume ou snapshot não testado de backup;
- permitir escrita do mesmo fato em duas fontes independentes;
- tratar cache ou motor de busca como ledger canônico;
- acreditar que “schema flexível” dispensa versão e validação;
- fazer dual write sem outbox, reconciliação ou idempotência;
- usar consistência eventual como desculpa para resultado indefinidamente errado;
- dimensionar pela média e ignorar picos, distribuição e latência de cauda;
- prometer RPO/RTO sem ensaio de restauração;
- armazenar dados pessoais “porque talvez sejam úteis”, sem retenção definida.

## 9. Prática progressiva

Use apenas dados fictícios e ambientes sob seu controle.

### Nível 1 — vocabulário

1. Para sessão, pedido, log, catálogo e recomendação, marque: fato canônico,
   projeção, cache ou dado descartável.
2. Para cada exemplo, defina tipo, unidade, identidade, tempo e proprietário.
3. Diferencie em uma frase comando, evento e estado.

### Nível 2 — garantias

1. Escreva cinco invariantes para uma biblioteca.
2. Associe cada uma a validação da aplicação, constraint, transação ou
   reconciliação. Justifique combinações.
3. Defina uma operação que tolera leitura obsoleta e outra que não tolera.

### Nível 3 — falhas

Desenhe API, PostgreSQL, worker e MongoDB. Para cada seta, responda:

- o que acontece em timeout antes e depois do efeito;
- se retry pode duplicar a operação;
- como detectar atraso ou perda;
- qual componente reconcilia o estado.

### Nível 4 — decisão profissional

Escreva uma ADR curta para um sistema de biblioteca contendo:

```text
Título e status
Contexto e requisitos mensuráveis
Invariantes e padrões de acesso
Alternativas consideradas
Decisão
Consequências positivas e negativas
Riscos, métricas e condição de revisão
```

Compare ao menos PostgreSQL sozinho e PostgreSQL com uma projeção adicional.

## Critério de conclusão

Você concluiu este capítulo quando consegue, sem consultar o texto:

- [ ] explicar o caminho de uma consulta pelos componentes do SGBD;
- [ ] escrever invariantes testáveis em vez de requisitos vagos;
- [ ] distinguir fonte, projeção, cache, réplica e backup;
- [ ] justificar um modelo de dados pelos acessos e garantias;
- [ ] explicar a falha de dual write e o papel da outbox/idempotência;
- [ ] definir RPO/RTO e um teste de restauração coerente;
- [ ] analisar uma partição com operações concretas, sem rotular o banco apenas
      como “CP” ou “AP”;
- [ ] apresentar uma ADR com trade-offs e condição de revisão.

Continue em [Modelagem relacional](01-modelagem-relacional.md). As fontes
oficiais complementares estão em [Referências](REFERENCIAS.md).
