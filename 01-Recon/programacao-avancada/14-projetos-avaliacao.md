# Projetos, evidências e avaliação técnica

Projeto neste módulo não é apenas código que responde no caminho feliz. Ele
precisa demonstrar que modelo, banco, API e operação preservam o mesmo contrato
quando há entrada inválida, concorrência, retry e dependência indisponível.

Todos os projetos usam somente dados fictícios e ambiente local. Não publique
porta, credencial, dump ou imagem em serviço externo para concluir a atividade.

## Como a avaliação funciona

Você entregará quatro projetos guiados e um projeto autoral. Os guiados isolam
competências; o autoral prova que você consegue combiná-las sem seguir uma
receita linha por linha.

Cada entrega precisa conter:

```text
projeto/
|-- README.md              # executar, validar, recuperar e limpar
|-- docs/
|   |-- requisitos.md      # casos, invariantes e fora de escopo
|   |-- modelo.md          # diagrama e dicionário
|   |-- contrato.md        # API, erros, concorrência e compatibilidade
|   |-- ameacas.md         # ativos, fronteiras e controles
|   `-- adr/               # decisões e alternativas
|-- migrations/            # mudanças ordenadas e reproduzíveis
|-- fixtures/              # somente dados sintéticos
|-- src/                   # implementação
|-- tests/                 # unidade, contrato e integração
|-- evidence/              # saídas essenciais, sem segredo
`-- compose.yaml           # quando o projeto exigir serviços reais
```

Não salve volumes, bancos, venv, builds ou logs integrais no repositório. A
pasta `evidence/` guarda apenas recortes reproduzíveis: plano JSON sanitizado,
resultado esperado, versões e explicação.

## Evidência forte e evidência fraca

| Afirmação | Evidência fraca | Evidência forte |
|-----------|-----------------|------------------|
| “A constraint funciona” | imagem de uma tabela | teste que tenta violá-la e verifica o erro |
| “O índice melhora a consulta” | tempo isolado | fixture, planos antes/depois e custo de escrita |
| “Não duplica” | dois curls manuais | teste repetível com mesma chave e estado final |
| “Controla concorrência” | ETag na resposta | dois clientes disputando a mesma versão |
| “Tem backup” | arquivo `.dump` | restore em destino limpo mais verificação |
| “É observável” | muitos logs | pergunta operacional respondida por sinais correlacionados |

Uma captura pode complementar a prova, mas não substitui comando, fixture,
asserção e explicação.

## Projeto 1 — biblioteca relacional

Modele autores, obras, edições, exemplares, membros, empréstimos, devoluções
e multas. Diferencie a obra intelectual da edição publicada e do exemplar
físico. Essa separação é parte da avaliação.

### Regras mínimas

- ISBN pertence à edição e, quando informado, é único;
- um exemplar possui identidade própria e um estado permitido;
- somente um empréstimo aberto pode existir por exemplar;
- data de devolução não antecede a retirada;
- multa não usa `float` binário;
- exclusão de membro não apaga silenciosamente histórico financeiro;
- dois clientes não podem emprestar o mesmo exemplar simultaneamente.

### Entregáveis

1. modelo conceitual com cardinalidades e opcionalidade;
2. dicionário de dados com tipo, nulabilidade, default e invariante;
3. migrations forward-only e estratégia de rollback operacional;
4. fixtures pequenas para correção e maiores para plano/desempenho;
5. pelo menos dez consultas, incluindo:
   - joins interno e externo;
   - agregação por período;
   - CTE;
   - window function;
   - anti-join com `NOT EXISTS`;
   - paginação determinística;
6. cenário concorrente de dois empréstimos;
7. planos antes/depois de um índice justificado;
8. backup e restore em banco vazio.

### Testes obrigatórios

- duplicar ISBN não cria duas edições;
- inserir estado desconhecido falha;
- abrir segundo empréstimo do exemplar falha;
- rollback não deixa estado intermediário;
- a consulta de itens atrasados não perde membro sem empréstimo;
- o restore produz as mesmas contagens e invariantes.

Critério: explique qual regra fica em constraint simples, índice parcial,
transação ou aplicação e por que as alternativas seriam mais fracas.

## Projeto 2 — catálogo documental

Modele um catálogo com categorias, variações, atributos por categoria, preço e
histórico sintético no MongoDB. Comece pelos acessos, não por um documento
gigante.

### Matriz de acessos

Documente, para cada operação:

| Operação | Filtro/ordem | Frequência | Consistência | Volume esperado |
|----------|--------------|------------|---------------|-----------------|
| detalhe por SKU | `sku` | alta | atual | um documento |
| busca por categoria | categoria + preço | alta | segundos | página |
| atualizar preço | SKU/variação | média | atômica | um agregado |
| relatório | categoria/período | baixa | eventual | agregação |

Substitua valores ilustrativos pelos requisitos do seu projeto.

### Entregáveis

- decisão embed/reference para cada relação;
- tamanho e crescimento máximo previstos;
- `$jsonSchema` com campos exigidos e valores limitados;
- índice único e ao menos um composto derivado da matriz;
- explicação da regra ESR para a consulta principal;
- três pipelines com `$match` antecipado e projeção explícita;
- estratégia de evolução com `schemaVersion`;
- migração idempotente de duas versões de documento;
- comparação explícita com o modelo PostgreSQL.

### Experimentos obrigatórios

1. tente inserir documento inválido e explique a falha;
2. use `explain("executionStats")` antes/depois do índice;
3. mostre como array sem limite poderia exceder o agregado;
4. repita a migração e prove que o segundo ciclo não altera o estado;
5. restaure um archive em namespace separado.

Critério: flexibilidade de documento não pode significar estado arbitrário.

## Projeto 3 — API contract-first

Projete uma agenda de reservas antes de escolher o framework. O domínio precisa
ter recursos com capacidade limitada, cancelamento e concorrência realista.

### Contrato mínimo

- recursos, identificadores, estados e transições permitidas;
- request/response schemas e limites de cada campo;
- status HTTP por resultado, inclusive `409`, `412`, `422` e `429` quando
  aplicáveis;
- erros em `application/problem+json` com código estável;
- autenticação pretendida e matriz de autorização;
- paginação estável e regra de ordenação total;
- criação repetível por idempotency key;
- alteração condicional por `ETag`/`If-Match`;
- política de compatibilidade e depreciação;
- limites de corpo, timeout e rate limit por operação.

### Sequência obrigatória

1. escreva exemplos de request e response;
2. transforme exemplos em OpenAPI;
3. escreva contract tests contra um stub;
4. implemente em Python, Java, C# ou JavaScript;
5. execute os mesmos testes contra a implementação;
6. gere ou escreva cliente e valide compatibilidade;
7. introduza uma mudança incompatível propositalmente e prove que o teste a
   detecta antes de revertê-la.

Critério: o consumidor deve entender o contrato sem ler controller, ORM ou
modelo interno.

## Projeto 4 — auditoria da Inventory API

Use o [projeto integrador](projetos/inventory-api/README.md) como sistema a ser
explicado, quebrado de forma controlada e estendido.

### Linha de base

1. registre versões das imagens e toolchains;
2. valide Compose antes de construir;
3. suba os serviços e execute o smoke test sem alterações;
4. inventarie rotas, schemas, constraints, índices e sinais;
5. confirme que somente o gateway publica porta em loopback;
6. confirme identidades sem root e filesystems read-only previstos.

### Falhas controladas

- pare MongoDB, crie produto e prove outbox pendente;
- restaure MongoDB e meça o tempo até a projeção convergir;
- reutilize chave idempotente com o mesmo corpo e depois com corpo diferente;
- faça dois PATCH com o mesmo ETag e explique o vencedor;
- use cursor antigo depois de inserir novos itens e descreva a semântica;
- torne uma dependência indisponível e compare liveness com readiness;
- restaure um backup em ambiente descartável.

Não simule indisponibilidade apagando volumes. Pare o serviço correspondente e
preserve o estado necessário para observar recuperação.

### Mudança vertical

Implemente uma destas evoluções:

- categoria de produto;
- reserva de estoque com expiração;
- desativação de produto sem apagar histórico;
- cursor opaco assinado;
- reconciliação explícita da projeção;
- métricas e trace correlacionados.

A mudança só termina quando atravessa migration, domínio, repositório, caso
de uso, contrato, teste, telemetria e documentação. Registre compatibilidade e
estratégia de rollback.

## Projeto final autoral

Escolha um domínio benigno: biblioteca, estudos, estoque doméstico, oficina,
agenda de salas ou eventos. O projeto deve possuir ao menos:

- uma invariante concorrente que não cabe em validação superficial;
- uma fonte relacional de verdade;
- uma projeção documental derivada e reconstruível;
- API versionada e contrato OpenAPI;
- paginação, idempotência e controle de concorrência;
- testes unitários, contrato, integração e falha;
- logs estruturados, ao menos três SLIs e um SLO;
- backup, restore, reconciliação e runbook;
- threat model e controles proporcionais;
- ADRs e retrospectiva técnica.

### Marcos

1. **Descoberta:** requisitos, fora de escopo, riscos e acessos.
2. **Design:** modelo, invariantes, contrato e ADRs.
3. **Esqueleto:** migrations, health/readiness e primeiro teste vertical.
4. **Consistência:** concorrência, idempotência e outbox.
5. **Operação:** telemetria, falhas, backup e restore.
6. **Defesa:** execução limpa, demonstração e perguntas.

Cada marco deve deixar o repositório executável; evite uma grande integração
somente no final.

## Rubrica — 100 pontos

| Dimensão | Pontos | Evidência de excelência |
|----------|-------:|--------------------------|
| Requisitos e invariantes | 10 | regras inequívocas, estados e falhas previstos |
| Modelagem relacional | 12 | chaves, cardinalidades, constraints e migrations justificadas |
| SQL, índices e planos | 10 | consultas corretas, planos comparados e trade-offs medidos |
| Modelagem documental | 8 | acessos dirigem embed/reference, validação e evolução |
| Contrato HTTP | 12 | recursos, erros, paginação e compatibilidade consistentes |
| Concorrência e consistência | 13 | conflito, retry, idempotência e convergência demonstrados |
| Arquitetura e código | 10 | dependências apontam para dentro e recursos têm lifecycle claro |
| Testes | 10 | pirâmide coerente, bancos reais e falhas determinísticas |
| Operação e recuperação | 10 | sinais acionáveis, health correto e restore provado |
| Comunicação | 5 | README, ADRs, evidências e defesa reproduzíveis |

Faixas:

- **90–100:** domina decisões, limites e operação; evidência reproduzível;
- **75–89:** competente, com lacunas não críticas documentadas;
- **60–74:** comportamento parcial ou justificativas insuficientes;
- **abaixo de 60:** refaça os checkpoints antes de avançar.

## Portões críticos

Independentemente da soma, o projeto não é aprovado se:

- permite estado inválido em uma invariante central;
- concatena entrada do cliente em SQL ou consulta perigosa;
- perde atualização concorrente silenciosamente;
- duplica efeito ao repetir uma operação declarada idempotente;
- expõe banco, segredo ou stack trace ao cliente;
- não consegue iniciar do zero pela documentação;
- chama de backup um arquivo que nunca foi restaurado;
- deixa containers, volumes temporários ou credenciais reais sem controle;
- possui teste verde que não executa a regra alegada.

Corrija o portão e repita a defesa; pontos extras não compensam falha crítica.

## Roteiro de defesa

Uma segunda pessoa deve clonar/copiar o projeto em ambiente limpo e executar o
runbook. Durante a defesa, responda com código e evidência:

1. Qual banco é fonte de verdade de cada fato?
2. Qual invariante mais importante e quem a aplica atomicamente?
3. Qual consulta determinou cada índice?
4. Que anomalia o isolamento escolhido ainda permite?
5. O que acontece se o processo morrer antes e depois de cada commit?
6. Como retry distingue repetição de uma nova intenção?
7. Como um cliente detecta alteração concorrente?
8. Quanto tempo uma projeção pode ficar defasada e como isso é medido?
9. Qual sinal detecta saturação do pool antes de indisponibilidade total?
10. Como restaurar a fonte e reconstruir a projeção?
11. Qual mudança incompatível você rejeitou e por quê?
12. Qual risco ficou aceito e qual evidência justificou a decisão?

## Checklist final

- [ ] Uma pessoa sem contexto executou o runbook.
- [ ] O ambiente nasceu de volumes vazios.
- [ ] Todas as migrations foram aplicadas na ordem.
- [ ] Testes falharam quando a proteção foi removida experimentalmente.
- [ ] Planos e medições registram versão e tamanho do fixture.
- [ ] Nenhuma evidência contém segredo ou dado pessoal.
- [ ] Backup foi restaurado em destino diferente.
- [ ] Falha de dependência e recuperação foram demonstradas.
- [ ] Containers e volumes temporários foram removidos conscientemente.
- [ ] Limitações e trabalho futuro estão explícitos.

Conclusão recomendada: pelo menos 75 pontos, nenhum portão crítico aberto e
todas as evidências obrigatórias reproduzíveis.
