# Caderno de práticas — dados e APIs

Este caderno transforma conceitos em pequenos experimentos antes dos
laboratórios formais. Faça em branch própria, use somente fixtures sintéticas e
registre a explicação, não apenas a saída.

## Formato de resposta

Para cada prática, entregue:

```text
previsão:
implementação/comando:
evidência essencial:
explicação:
caso-limite:
teste permanente:
cleanup:
```

Se a previsão estiver errada, não a apague. O contraste entre hipótese e
resultado é a parte mais valiosa do exercício.

## Bloco A — requisito, modelo e schema

### 1. Fato ou cópia?

Receba estes campos de um catálogo: SKU, nome atual, preço, quantidade,
quantidade disponível, total vendido, nome da categoria e relatório mensal.
Classifique cada um como fonte, derivado, cache ou projeção. Declare quem pode
alterá-lo e como reconstruí-lo.

**Prova:** uma tabela sem dois componentes competindo como fonte do mesmo fato.

### 2. Invariantes antes de tabelas

Para uma agenda de salas, escreva dez estados que nunca podem ser confirmados.
Classifique cada regra em tipo, nulabilidade, `CHECK`, unicidade, chave
estrangeira, exclusão temporal, transação ou aplicação.

**Armadilha:** usar validação do formulário como única proteção concorrente.

### 3. Identidade

Modele pessoa, conta e associação. Compare email como chave primária, UUID como
chave e email com `UNIQUE`. Simule mudança de email e fusão de contas.

**Prova:** decisão inclui estabilidade, exposição e custo de referências.

### 4. Dependências funcionais

Dada uma planilha fictícia de pedidos com dados do cliente e produto repetidos,
liste dependências, anomalias e decomponha até a forma normal necessária.
Depois proponha uma desnormalização consciente para leitura.

**Prova:** a cópia derivada tem processo de atualização e tolerância a atraso.

### 5. Migration expand/contract

Planeje dividir `full_name` em `given_name` e `family_name` sem parada. Inclua
colunas novas, dual read/write temporário, backfill em lotes, validação,
cutover e remoção posterior.

**Armadilha:** migration que exige reescrever tabela inteira no mesmo deploy.

## Bloco B — SQL correto

Use o fixture relacional do laboratório.

### 6. `NULL` e três valores lógicos

Preveja o resultado de comparar `NULL`, usar `NOT IN` com um `NULL` e usar
`NOT EXISTS`. Execute e explique por que uma consulta pode retornar zero linhas
inesperadamente.

**Teste:** inclua lista vazia, uma linha nula e uma linha correspondente.

### 7. Outer join preservado

Liste todos os autores, inclusive sem livros, e conte obras publicadas. Coloque
um filtro da tabela direita primeiro no `WHERE` e depois no `ON`; compare.

**Prova:** explique quando o filtro transforma efetivamente o outer join.

### 8. Agregação sem duplicação

Some valores de pedidos que possuem múltiplos itens e múltiplos pagamentos.
Mostre uma consulta incorreta que multiplica linhas e corrija pré-agregando
cada lado.

**Teste:** fixture com duas linhas em cada relação filha.

### 9. Anti-join

Encontre membros sem empréstimo aberto usando `NOT EXISTS`. Compare com `LEFT
JOIN ... IS NULL` e documente o tratamento de `NULL`.

### 10. Top N por grupo

Use `row_number()` particionado por categoria para obter os três itens mais
recentes. Defina desempate total; repita a consulta e confirme ordem estável.

### 11. CTE recursiva

Modele categorias pai/filha e percorra uma subárvore. Introduza um ciclo em
fixture descartável e acrescente detecção/limite.

**Armadilha:** assumir que todo grafo armazenado como hierarquia é acíclico.

### 12. Paginação

Compare `OFFSET` com keyset em `(created_at, id)`. Insira uma linha entre duas
páginas e observe duplicação ou omissão. Declare a semântica escolhida.

## Bloco C — transação, concorrência e plano

### 13. Atomicidade

Transfira quantidade entre dois estoques dentro de uma transação. Force erro
entre débito e crédito. O estado final deve ser igual ao inicial.

**Teste:** compare soma e valores individuais antes/depois.

### 14. Lost update

Abra duas sessões, leia a mesma versão e tente dois updates. Primeiro reproduza
sobrescrita silenciosa; depois corrija com `WHERE id = ? AND version = ?`.

**Prova:** exatamente uma alteração confirma para a versão antiga.

### 15. Write skew

Modele dois profissionais de plantão com a regra “ao menos um permanece”.
Execute transações concorrentes que desativam linhas diferentes. Compare
isolamentos e uma proteção adequada.

### 16. Deadlock controlado

Em duas sessões, bloqueie recursos A/B em ordem oposta. Registre a detecção e
a transação abortada. Repita adquirindo locks em ordem canônica.

**Armadilha:** retry infinito sem jitter, deadline ou prova de idempotência.

### 17. Plano e cardinalidade

Crie fixture pequeno e depois representativo. Capture `EXPLAIN (ANALYZE,
BUFFERS)` de uma consulta, compare estimativa/real, rode `ANALYZE` e adicione um
índice derivado do filtro/ordem.

**Prova:** inclua também o custo de INSERT/UPDATE e tamanho do índice.

## Bloco D — documentos e MongoDB

### 18. Embed ou reference

Para pedido/itens, usuário/endereços e produto/avaliações, decida por relação.
Use leitura conjunta, frequência de mudança, cardinalidade, crescimento e
atomicidade.

### 19. Array sem limite

Modele histórico embutido e estime crescimento. Transforme-o em bucket ou
coleção referenciada com página temporal.

**Prova:** limite e política de retenção ficam explícitos.

### 20. Schema validation

Crie validator para evento de auditoria. Tente campo ausente, tipo errado,
evento desconhecido e documento válido. Explique validação estrita versus
evolução compatível.

### 21. Índice composto

Parta de uma consulta com igualdade, sort e range. Crie índice na ordem
justificada, execute `explain("executionStats")` e compare documentos/chaves
examinados.

### 22. Pipeline

Construa relatório por categoria e mês. Antecipe `$match`, trate documentos sem
campo e evite `$unwind` que multiplica resultados sem necessidade.

**Teste:** resultado conhecido calculado manualmente num fixture mínimo.

## Bloco E — contrato HTTP e clientes

### 23. Recurso versus comando

Modele “reservar estoque” como alteração de recurso e como sub-recurso de
operação. Compare identidade, retry, auditoria e cancelamento.

### 24. Tabela de resultados

Para `PATCH /products/{id}`, escreva status e Problem Details para: ID malformado,
ausente, body inválido, sem `If-Match`, versão obsoleta, violação de regra e
sucesso.

**Prova:** nenhum erro previsível depende de stack trace.

### 25. Idempotency key

Defina escopo, expiração, hash da intenção, resposta persistida e conflito.
Teste duas tentativas simultâneas e reuso com corpo diferente.

### 26. ETag

Faça GET, PATCH condicional e novo GET. Depois envie a ETag antiga. Diferencie
`409 Conflict` de `412 Precondition Failed` na sua política.

### 27. Cursor opaco

Codifique ordenação total em cursor. Rejeite cursor malformado, incompatível
com filtro e fora do limite. O cliente nunca precisa interpretar seu conteúdo.

### 28. Cliente hostil ao caminho feliz

Para uma das cinco linguagens, teste: timeout, `404` Problem Details, media type
errado, JSON truncado, corpo acima do limite e inteiro grande.

### 29. Compatibilidade

Adicione campo opcional a uma resposta e confirme clientes antigos. Depois
renomeie/remova campo obrigatório em branch descartável e prove que contract
test detecta a quebra.

## Bloco F — arquitetura, falha e operação

### 30. Fronteiras de camada

Desenhe dependências de controller, DTO, caso de uso, domínio, repositório e
driver. Remova framework do teste de uma regra de domínio.

### 31. Pool e backpressure

Limite o pool local e execute chamadas concorrentes controladas. Meça espera,
latência total e erros. Não aumente o pool; implemente limite de concorrência ou
falha precoce e compare.

### 32. Outbox

Pare MongoDB, confirme uma mudança PostgreSQL, observe evento pendente e restaure
o serviço. Meça convergência e repita a entrega do mesmo evento.

**Prova:** projeção possui exatamente um documento por `eventId`.

### 33. Health e readiness

Pare cada dependência isoladamente. Registre liveness, readiness e rota de
negócio. Explique por que uma falha de projeção pode ou não retirar a API de
tráfego conforme o contrato adotado.

### 34. SLI e SLO

Defina SLIs de disponibilidade válida, latência e atraso do outbox. Especifique
eventos bons, total, janela e exclusões. Crie um SLO e duas ações quando o
orçamento de erro for consumido.

### 35. Backup, restore e reconciliação

Gere backup da fonte, restaure em destino novo e valide constraints/contagens.
Apague apenas a projeção descartável e reconstrua-a da fonte/eventos.

**Armadilha:** validar somente que o comando de backup retornou zero.

### 36. Runbook sem autor

Entregue o projeto a outra pessoa ou a uma shell limpa. Ela deve iniciar,
executar testes, reproduzir uma falha, restaurar e limpar sem explicação oral.
Registre toda ambiguidade encontrada como bug de documentação.

## Autoavaliação por bloco

Use esta escala:

- **0 — reconheço:** sei definir, mas não executar;
- **1 — reproduzo:** executo uma receita e obtenho a saída;
- **2 — explico:** prevejo e relaciono resultado ao mecanismo;
- **3 — transfiro:** aplico em domínio diferente e justifico trade-offs;
- **4 — diagnostico:** encontro falha, crio prova e evito regressão.

Não avance ao projeto final com nota abaixo de 2 em transação, contrato,
idempotência, concorrência ou restore. Retorne ao capítulo, reduza o fixture e
repita o ciclo previsão–evidência–explicação.
