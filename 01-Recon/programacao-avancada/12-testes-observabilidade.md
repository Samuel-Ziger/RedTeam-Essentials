# Testes, contratos e observabilidade de APIs

Testes respondem antes do deploy se o sistema cumpre propriedades conhecidas.
Observabilidade ajuda a formular e responder perguntas durante a execução.
Uma não substitui a outra: teste não reproduz toda falha de produção, e um
dashboard não compensa um contrato nunca verificado.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- montar uma estratégia de testes orientada a risco;
- verificar contrato, banco, concorrência e falhas de dependência;
- separar logs, métricas e traces e correlacioná-los;
- definir SLIs e SLOs a partir da experiência do consumidor;
- criar alertas acionáveis com runbooks;
- executar carga e injeção de falha em ambiente autorizado e controlado.

## Teste propriedades, não detalhes acidentais

Antes de escolher ferramenta, escreva as garantias:

- duas criações simultâneas não violam unicidade;
- repetir uma chave idempotente não duplica efeito;
- uma identidade de outro tenant nunca observa o recurso;
- uma página não repete itens sob a concorrência prometida;
- um update com versão antiga não sobrescreve mudança nova;
- queda do consumidor não perde evento confirmado na outbox;
- uma falha inesperada produz correlação sem vazar internals.

Testar apenas “retornou 200” deixa as propriedades importantes sem evidência.

## Camadas de teste por risco

| Camada | Prova melhor | Não prova sozinha |
|---|---|---|
| unidade | regra pura, casos-limite, estados | wiring, driver e schema real |
| componente | API + casos de uso com fakes | SQL, migrations e rede real |
| integração | adaptador com dependência real | gateway e jornada completa |
| contrato | forma e compatibilidade produtor/consumidor | regra interna inteira |
| ponta a ponta | poucos fluxos pelo stack implantado | todas as combinações |
| carga/resiliência | comportamento sob pressão/falha | correção funcional total |

A “pirâmide” é heurística. Uma API orientada a dados pode precisar de mais
integração porque isolamento, índice e consulta só existem no banco real.
Mantenha a maior parte rápida, mas invista onde o risco está.

## Testes de unidade do domínio

Um teste deve declarar cenário, ação e propriedade:

```python
def test_withdrawal_cannot_make_stock_negative() -> None:
    product = Product.with_stock(quantity=2)

    with raises(InsufficientStock):
        product.withdraw(quantity=3)

    assert product.stock == 2
```

Observe a segunda asserção: além de levantar erro, o objeto não ficou
parcialmente alterado. Teste limites (`0`, máximo, um acima), transições de
estado e invariantes, não getters triviais.

Injete clock, gerador de ID e aleatoriedade. O teste deve reproduzir a falha com
o mesmo seed e sem depender do relógio da máquina.

## Testes de componente HTTP

Inicie a aplicação em memória com adaptadores controlados. Verifique a resposta
inteira:

```python
def test_create_product_contract(client) -> None:
    response = client.post(
        "/api/v1/products",
        headers={"Idempotency-Key": "test-create-001"},
        json={"sku": "BOOK-001", "name": "Databases", "priceCents": 4500},
    )

    payload = response.json()
    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")
    assert response.headers["location"].startswith("/api/v1/products/")
    assert response.headers["location"].endswith(payload["id"])
    assert response.headers["etag"] == '"1"'
    assert set(payload) == {"id", "sku", "name", "priceCents", "version"}
    assert payload == {
        "id": payload["id"],
        "sku": "BOOK-001",
        "name": "Databases",
        "priceCents": 4500,
        "version": 1,
    }
```

Não use assert parcial por padrão: um campo inesperado pode vazar dado. Quando
campos adicionais são permitidos pelo contrato, explicite essa decisão.

### Matriz mínima por endpoint

- sucesso com status, headers e body exatos;
- media type ausente/incorreto;
- JSON malformado;
- campo ausente, extra, tipo errado e limites;
- recurso ausente e objeto ocultado;
- autenticação e autorização negativas;
- conflito de unicidade/estado;
- precondição atual e obsoleta;
- timeout e indisponibilidade de dependência;
- correlação e sanitização de erro.

## Banco real para o que depende do banco

Mocks não provam:

- sintaxe SQL e bind de parâmetros;
- constraints e triggers;
- isolamento e locks;
- encoding e timezone;
- tipo decimal e precisão;
- plano de execução e índice;
- migrations.

Execute integração com a mesma tecnologia e, idealmente, a mesma versão
principal da produção. Cada teste precisa de isolamento determinístico:
transação revertida, schema/banco efêmero ou dados com IDs exclusivos. O
isolamento escolhido não pode esconder commits e concorrência que o teste quer
observar.

### Migrations

Teste pelo menos:

1. banco vazio até a versão atual;
2. versão anterior com dados representativos até a atual;
3. aplicação antiga durante a fase expand;
4. backfill interrompido e retomado;
5. constraints depois do backfill;
6. rollback ou roll-forward praticado conforme a política.

## Concorrência de verdade

Um teste sequencial não prova propriedade concorrente. Coordene duas conexões
para alcançarem a mesma barreira antes da operação:

```text
worker A: carregar/reservar ---- espera ---- confirmar
worker B: carregar/reservar ---- espera ---- confirmar
                                     |
                                 libera ambos
```

Depois verifique estado final e resultados aceitos. Para estoque 1 e duas
retiradas de 1, exatamente uma deve vencer; a outra recebe conflito/regra, e o
estoque final é 0. Repita o teste para aumentar a chance de expor scheduling,
mas use sincronização deliberada em vez de `sleep` arbitrário.

## Idempotência sob falha

Casos essenciais:

1. mesma chave e mesmo body depois de sucesso;
2. mesma chave e body diferente;
3. duas requisições simultâneas com a mesma chave;
4. desconexão do cliente depois do commit e antes de ler resposta;
5. falha antes do commit;
6. processo reiniciado com registro em `processing`;
7. chave expirada conforme a política;
8. mesma chave em tenant/operação diferente.

Conte efeitos persistidos, não apenas status HTTP. O teste deve provar que
existe um produto e um evento, e que o resultado repetido representa a mesma
operação lógica.

## Paginação e contrato temporal

Crie dados com empate no campo principal de ordenação. Percorra todas as
páginas e confirme:

- nenhum ID repetido;
- nenhum ID omitido dentro da promessa de consistência;
- ordem global respeitada;
- `next` ausente no fim;
- cursor alterado, expirado ou incompatível é rejeitado;
- trocar filtros/tenant invalida o cursor;
- inserção/remoção entre páginas tem comportamento documentado.

Compare o conjunto por IDs, não pela quantidade apenas: uma duplicação e uma
omissão podem manter o mesmo total.

## Testes de contrato

Há três perspectivas complementares:

- **schema:** requests/responses respeitam OpenAPI/JSON Schema;
- **compatibilidade:** a nova especificação não remove garantias publicadas;
- **consumidor:** interações reais necessárias continuam satisfeitas.

No pipeline:

```text
lint do contrato
  -> diff breaking contra contrato publicado
  -> testes do provider contra exemplos/schemas
  -> contratos dos consumidores relevantes
  -> publicação versionada do artefato
```

Contract test não substitui teste funcional. Uma resposta pode obedecer ao
schema e ainda debitar o produto errado.

### Compatibilidade não é apenas estrutural

Teste também:

- significado e unidade de campos;
- ordenação e paginação;
- defaults;
- novos valores de enum;
- status e códigos de erro;
- autenticação/escopos;
- limites operacionais.

## Testes generativos e fuzzing defensivo

Property-based testing gera muitos casos e reduz uma falha a um exemplo mínimo.
Boas propriedades:

- serializar e desserializar um DTO válido preserva o significado;
- qualquer quantidade aceita mantém estoque dentro do intervalo;
- qualquer cursor produzido pelo servidor é aceito com os mesmos filtros;
- entrada rejeitada nunca altera o banco;
- parser sempre termina dentro de limites para payload limitado.

Fuzzing deve ocorrer em parser/componente próprio, em ambiente isolado, com
limites e corpus sem dados sensíveis. O resultado esperado é resposta controlada
ou rejeição, nunca crash, consumo ilimitado ou stack trace ao cliente.

## Dados de teste

- fixtures pequenas e legíveis para cenários essenciais;
- factories com defaults seguros e overrides explícitos;
- seeds registrados para geração aleatória;
- timestamps e IDs determinísticos quando o valor exato importa;
- volume e distribuição representativos em desempenho;
- nenhum segredo ou cópia direta de produção.

Anonimização é um processo verificável, não uma troca manual de nomes. Dados
raros e combinações podem reidentificar pessoas. Prefira dados sintéticos quando
eles representam o comportamento necessário.

## Injeção de falhas

Introduza falhas deliberadas nas fronteiras controladas:

- pool sem conexão disponível;
- consulta excede statement timeout;
- commit falha;
- resposta remota demora ou retorna erro transitório;
- broker aceita publicação, mas confirmação se perde;
- worker encerra entre efeito e checkpoint;
- disco/armazenamento atinge limite simulado;
- shutdown chega durante operação.

Para cada falha, verifique estado, resposta, retry, log, métrica e trace. Restrinja
experimentos ao laboratório ou ambiente com autorização, blast radius e abort
definidos.

## Observabilidade: logs, métricas e traces

Cada sinal responde melhor a perguntas diferentes:

| Sinal | Força | Exemplo |
|---|---|---|
| log | detalhe discreto de um evento | por que request 3bb falhou? |
| métrica | agregação barata ao longo do tempo | p99 piorou nesta rota? |
| trace | causalidade e tempo entre componentes | onde os 800 ms foram gastos? |

Correlacione-os com request/trace ID e atributos controlados. Não transforme
todo ID em label de métrica.

## Logs estruturados

```json
{
  "timestamp": "2026-09-29T18:00:00.125Z",
  "level": "INFO",
  "event": "request_finished",
  "service": "inventory-api",
  "requestId": "3bb0a764bd9a",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "method": "POST",
  "route": "/api/v1/products",
  "status": 201,
  "durationMs": 18
}
```

Use template da rota, não path bruto, em agregações. Defina um schema de log,
tipos, nomes e severidades. Uma exceção esperada de regra não é necessariamente
`ERROR`; uma falha inesperada não deve desaparecer como `INFO`.

Sanitize em uma biblioteca central e aplique allowlist de campos. Truncar depois
de registrar não remove o vazamento original.

## Métricas

Comece pelos sinais de serviço:

- **taxa:** requisições/segundo e operações de negócio;
- **erros:** por classe, rota e resultado controlado;
- **duração:** histograma e percentis;
- **saturação:** CPU, memória, fila, pool e workers.

Para banco:

- conexões usadas, livres e tempo de espera;
- duração/erros de transação;
- locks e deadlocks;
- cache hit, lag e queries lentas;
- linhas/documentos examinados versus retornados;
- storage e crescimento.

Para assíncrono:

- profundidade e idade da mensagem mais antiga;
- taxa de entrada/saída;
- retries e dead-letter;
- atraso da outbox;
- tempo até projeção convergir.

### Cardinalidade

Labels devem ter conjunto pequeno e previsível: `route`, `method`, classe do
status, região limitada. `user_id`, `request_id`, URL completa e mensagem de
erro produzem séries ilimitadas, elevando custo e podendo derrubar a telemetria.
Guarde detalhe em logs/traces e ligue por exemplars quando a plataforma suportar.

Média esconde cauda. Leia p50, p95/p99 junto com volume, erros e saturação. Um
p99 sem tamanho de amostra também pode enganar.

## Tracing distribuído

Um trace pode conter:

```text
gateway  0 ms --------------------------------------------- 120 ms
  api       5 ms -------------------------------------- 112 ms
    pool       8 ms ------- 30 ms
    sql                       31 ms ---------------- 90 ms
    serialize                                      92 -- 98 ms
```

Crie spans nas fronteiras relevantes e inclua atributos de baixa cardinalidade:
serviço, operação, rota, tipo de banco e resultado. Não registre query com
valores, token ou body sensível.

Valide formato/tamanho do contexto recebido antes de propagá-lo. Trace ID não
é credencial. Sampling reduz custo: preserve uma amostra representativa e uma
política para erros/rotas críticas, entendendo que decisão tardia exige suporte
da infraestrutura.

## SLI, SLO, SLA e error budget

- **SLI:** medição de um comportamento percebido;
- **SLO:** objetivo interno para o SLI em uma janela;
- **SLA:** compromisso externo, possivelmente contratual;
- **error budget:** quantidade de resultado não bom tolerada pelo SLO.

Exemplo para leituras válidas:

```text
good = respostas 2xx/404 concluídas em até 300 ms
valid = requests bem formadas que chegaram ao serviço
SLI = good / valid
SLO = 99,9% em janela móvel de 30 dias
```

Decida conscientemente se 4xx entram no denominador. Uma credencial inválida
não prova indisponibilidade, mas um aumento de 401 por regressão de autenticação
pode representar impacto real e requer outro indicador.

Um SLO de 99,9% admite 0,1% de eventos não bons na janela. **Burn rate** compara
o consumo atual com essa taxa tolerada. Alertas de múltiplas janelas detectam
queima rápida sem reagir a cada pico curto.

## Alertas e runbooks

Um alerta bom possui:

- impacto ou risco claro para usuário/SLO;
- limiar baseado em taxa e janela, não exceção individual;
- serviço, ambiente e dashboard vinculados;
- runbook com diagnóstico, mitigação e escalonamento;
- dono e severidade;
- teste periódico e revisão de ruído.

Exemplo de runbook para fila atrasada:

1. confirmar idade, taxa de entrada e taxa de processamento;
2. verificar erros, retries, pool e dependência;
3. estimar tempo de recuperação;
4. reduzir entrada ou escalar worker dentro de limite seguro;
5. isolar mensagem venenosa sem perder ordem exigida;
6. acompanhar convergência e registrar causa.

## Dashboards por pergunta

Em vez de agrupar gráficos por tecnologia, responda:

1. consumidores estão recebendo resultados corretos e rápidos?
2. qual rota/tenant agregado/região explica o impacto?
3. o serviço está saturado ou depende de outro?
4. deploy/configuração coincide com a mudança?
5. filas e projeções estão convergindo?

Anote deploys e mudanças relevantes na linha do tempo.

## Teste de carga seguro

1. obtenha autorização e defina ambiente/blast radius;
2. escolha jornadas, distribuição, tamanho de dados e objetivo;
3. defina critério de parada para erro/saturação;
4. aqueça caches e pools de modo reproduzível;
5. aumente carga gradualmente;
6. registre latência, erro, throughput e saturação;
7. mantenha uma variável principal por experimento;
8. investigue o primeiro gargalo, altere e repita.

Diferencie:

- **load:** carga esperada;
- **stress:** procura o limite e a degradação;
- **spike:** aumento brusco;
- **soak:** execução longa para vazamento/acúmulo;
- **capacity:** estima recursos para uma meta.

Nunca aponte gerador de carga para ambiente de terceiros ou produção sem
autorização formal, isolamento e proteções.

## Exercícios

1. Escreva testes unitários para todas as transições de um produto.
2. Monte a matriz HTTP de criação e atualização.
3. Crie um teste concorrente que prove estoque não negativo.
4. Cubra oito cenários de idempotência, contando efeitos no banco.
5. Teste paginação com empates e inserção concorrente.
6. Defina um diff de contrato que bloqueie remoção de campo.
7. Injete falha no commit e na confirmação do broker.
8. Proponha cinco métricas sem labels de alta cardinalidade.
9. Defina SLI, SLO e burn-rate para leitura e para processamento assíncrono.
10. Crie dashboard e runbook para saturação do pool.
11. Planeje um teste de carga com hipótese e critério de parada.

## Critérios de conclusão

- cada invariante crítica possui ao menos um teste de falha;
- integração usa banco/driver real onde o comportamento depende deles;
- concorrência é coordenada sem depender de sleeps frágeis;
- contrato é validado e comparado automaticamente;
- logs, métricas e traces se correlacionam sem expor segredo;
- SLIs representam a experiência do consumidor;
- alertas apontam para runbook executável e possuem dono;
- carga/falha possuem autorização, limite e abort condition;
- uma regressão relevante faz o pipeline falhar antes do deploy.

## Checklist de revisão

- [ ] Testo propriedades e estado final, não apenas status.
- [ ] Banco, migrations e concorrência recebem testes reais.
- [ ] OpenAPI e consumidores participam da verificação de compatibilidade.
- [ ] Telemetria tem schema, retenção e sanitização.
- [ ] Labels de métrica possuem cardinalidade limitada.
- [ ] SLO, error budget, alerta e runbook formam um sistema coerente.
- [ ] Testes de carga e falha são restritos a ambiente autorizado.
