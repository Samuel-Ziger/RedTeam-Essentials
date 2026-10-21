# ADR-002: saída determinística e entrada limitada

- Status: aceito
- Data: 2026-10-03

## Contexto

Uma DAG pode possuir várias ordens corretas. Iteração de mapas/conjuntos pode
variar entre linguagens ou execuções, gerando diffs e testes instáveis. O adapter
também lia o arquivo inteiro sem uma política explícita, permitindo consumo de
memória desproporcional antes de validar o schema.

## Decisão

- escolher sempre o menor ID ordinal entre tarefas prontas;
- ordenar iterações que participam de erro ou desempate;
- limitar documento a 32 MiB, quantidade de itens a 100 mil e valores locais por
  constantes versionadas no código;
- ler no máximo `limite + 1` bytes antes de decodificar;
- traduzir inteiro gigante e estouro por aninhamento do parser em erros estáveis
  de validação;
- detectar caminho de ciclo com pilha explícita, sem depender do limite de
  recursão do runtime.

## Consequências

- saída é reproduzível e adequada a cache/diff;
- heap adiciona fator logarítmico em relação a uma fila simples;
- documentos acima da política são rejeitados mesmo se semanticamente válidos;
- limites são política do produto, não verdade universal;
- a pilha explícita torna a detecção de ciclo mais verbosa, mas suporta ciclos
  maiores que a pilha de chamadas.

## Alternativas

- qualquer ordem topológica: mais barata com fila, rejeitada pelo requisito de
  reprodutibilidade;
- ordenar toda a saída ao final: inválido, pois pode quebrar dependências;
- confiar no tamanho do arquivo do filesystem: existe janela de mudança e nem
  toda fonte futura terá `stat`; leitura limitada é a garantia efetiva;
- ciclo por DFS recursiva: simples, rejeitada pelo limite dependente do runtime.

## Gatilho de revisão

Reavaliar se medições representativas mostrarem que o heap domina a latência,
se a fonte deixar de ser arquivo local ou se requisitos reais ultrapassarem os
limites sem comprometer o orçamento de memória.
