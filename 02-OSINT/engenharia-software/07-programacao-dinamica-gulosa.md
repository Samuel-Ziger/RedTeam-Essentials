# 07 — Programação dinâmica e algoritmos gulosos

Programação dinâmica (DP) e algoritmos gulosos evitam enumerar todas as
sequências de decisões, mas por razões diferentes. DP armazena soluções de
estados sobrepostos e combina alternativas. Um algoritmo guloso toma uma decisão
local irrevogável; ele só é correto quando uma propriedade do problema garante
que alguma solução ótima começa com essa escolha.

## Objetivos verificáveis

Ao final, você deverá conseguir:

- definir estado, transição, casos base e ordem de avaliação de uma DP;
- provar correção por indução sobre estados ou ordem topológica;
- comparar memoização e tabulação com base em estados alcançados e pilha;
- reconstruir decisões, e não apenas calcular o valor ótimo;
- otimizar memória sem violar dependências da recorrência;
- reconhecer custos pseudopolinomiais e explosão do espaço de estados;
- provar uma escolha gulosa por troca, “fica à frente” ou invariante;
- produzir contraexemplos mínimos para estratégias gulosas falsas;
- calcular o caminho crítico do Dependency Planner em `O(V+E)`.

Pré-requisitos: complexidade, recursão, grafos/DAGs e invariantes. Antes de
codificar, escreva o significado de cada célula em uma frase completa.

## Modelo mental: um DAG de estados

Uma DP pode ser vista como um grafo acíclico:

- cada vértice é um estado suficiente para decidir o futuro;
- uma aresta representa uma transição para um subproblema;
- casos base são vértices com resposta direta;
- a solução combina resultados na ordem das dependências.

O estado precisa guardar toda informação que muda a resposta, mas nada
irrelevante. Se dois caminhos chegam ao mesmo estado, o restante do problema deve
ser idêntico. Caso contrário, memoizá-los sob a mesma chave é incorreto.

### Receita de modelagem

1. **Pergunta:** qual valor a função/tabela devolve?
2. **Estado:** quais variáveis determinam completamente esse valor?
3. **Escolhas:** que decisões partem do estado?
4. **Transição:** para quais estados menores cada escolha leva?
5. **Base:** quais estados têm resposta imediata?
6. **Ordem:** quando um estado é calculado, suas dependências já existem?
7. **Prova:** todas as soluções aparecem e nenhuma alternativa inválida entra?
8. **Reconstrução:** que decisão/predecessor deve ser guardado?
9. **Custo:** quantos estados existem e quanto custa cada transição?

“Use uma matriz” não é modelagem. A frase `dp[i][c] é o maior valor usando os
primeiros i itens com capacidade máxima c` é um contrato testável.

## Exemplo trabalhado: troco mínimo

Dadas moedas positivas, queremos a menor quantidade para somar `total`, com uso
ilimitado. Estado:

> `dp[v]` é a menor quantidade de moedas necessária para formar exatamente `v`;
> se impossível, vale infinito.

A última moeda de uma solução para `v` pode ser qualquer `m <= v`. Removê-la
deixa uma solução ótima de `v-m`; se não fosse ótima, substituí-la melhoraria a
solução original.

```text
dp[0] = 0
dp[v] = min(1 + dp[v - m]) para toda moeda m <= v
```

Implementação com reconstrução:

```python
def troco_minimo(moedas: list[int], total: int) -> list[int] | None:
    if total < 0 or not moedas or any(m <= 0 for m in moedas):
        raise ValueError("moedas positivas e total nao negativo")

    infinito = total + 1
    dp = [0] + [infinito] * total
    escolhida: list[int | None] = [None] * (total + 1)

    for valor in range(1, total + 1):
        for moeda in moedas:
            if moeda <= valor and dp[valor - moeda] + 1 < dp[valor]:
                dp[valor] = dp[valor - moeda] + 1
                escolhida[valor] = moeda

    if dp[total] == infinito:
        return None

    solucao: list[int] = []
    restante = total
    while restante > 0:
        moeda = escolhida[restante]
        assert moeda is not None
        solucao.append(moeda)
        restante -= moeda
    return solucao
```

Há `total + 1` estados e até `len(moedas)` transições por estado: tempo
`O(total × M)`, espaço `O(total)`. O algoritmo é **pseudopolinomial**: `total`
pode ser exponencial em sua quantidade de bits. Uma entrada `total=10^12` cabe
em poucos bytes, mas a tabela não.

### Prova por indução

Base: `dp[0]=0` é ótimo, pois nenhuma moeda forma zero.

Hipótese: para todos os valores menores que `v`, `dp` contém a quantidade ótima.

Passo: qualquer solução de `v` termina em alguma moeda `m`; o prefixo forma
`v-m` e, pela hipótese, `dp[v-m]` é pelo menos tão bom quanto esse prefixo. A
transição considera toda moeda possível e escolhe o menor valor. Logo não é pior
que nenhuma solução válida e é construída de soluções válidas; portanto é ótima.

A prova também mostra por que moedas devem ser positivas: `v-m < v` garante
ordem acíclica. Moeda zero cria auto-dependência; negativa quebra a ordem.

## Memoização versus tabulação

Memoização é top-down: escreve a recorrência e calcula apenas estados alcançados.

```python
from functools import cache


def quantidade_minima(moedas: tuple[int, ...], total: int) -> int | None:
    infinito = total + 1

    @cache
    def resolver(restante: int) -> int:
        if restante == 0:
            return 0
        melhor = infinito
        for moeda in moedas:
            if moeda <= restante:
                melhor = min(melhor, 1 + resolver(restante - moeda))
        return melhor

    resposta = resolver(total)
    return None if resposta == infinito else resposta
```

Tabulação é bottom-up: controla ordem e evita call stack. Compare:

| Questão | Memoização | Tabulação |
|---|---|---|
| estados esparsos | pode calcular somente alcançados | pode desperdiçar células |
| pilha | proporcional à profundidade | normalmente constante fora da tabela |
| ordem | implícita na recursão | precisa ser derivada |
| overhead | chamada + hash/cache | acesso direto e laços |
| reconstrução | guarda escolha por chave | guarda predecessor por célula |

Não diga que top-down e bottom-up têm sempre o mesmo custo. Conte estados
realmente visitados, custo de chave e densidade da tabela.

## Estado suficiente: erro clássico

Suponha que tarefas possam usar recursos diferentes e a capacidade restante
dependa do conjunto já escolhido. Memoizar apenas por `indice` mistura caminhos
com capacidades diferentes. O estado talvez precise ser `(indice, capacidade)`.

Por outro lado, guardar a lista inteira escolhida torna quase todo caminho um
estado distinto e elimina sobreposição. Procure a informação mínima que determina
as escolhas futuras. Essa é a parte difícil da DP; preencher tabela é mecânico.

## Mochila 0/1 e direção da atualização

Estado bidimensional:

> `dp[i][c]` é o maior valor usando os primeiros `i` itens, capacidade `c`, cada
> item no máximo uma vez.

```text
dp[i][c] = dp[i-1][c]                              se peso_i > c
dp[i][c] = max(dp[i-1][c], valor_i + dp[i-1][c-p]) caso contrário
```

Tempo `O(nC)`, espaço `O(nC)`. Como uma linha depende somente da anterior, pode
usar `O(C)`, mas deve percorrer capacidade **de trás para frente**:

```python
def mochila(itens: list[tuple[int, int]], capacidade: int) -> int:
    dp = [0] * (capacidade + 1)
    for peso, valor in itens:
        for atual in range(capacidade, peso - 1, -1):
            dp[atual] = max(dp[atual], valor + dp[atual - peso])
    return dp[capacidade]
```

Da frente para trás, `dp[atual-peso]` pode já incluir o item corrente, convertendo
silenciosamente mochila 0/1 em mochila ilimitada. Otimização de memória altera a
proveniência dos dados; a ordem é parte da prova.

## DP em DAG: caminho crítico do Dependency Planner

No planejador, tarefas e dependências formam uma DAG. Para cada tarefa `v`:

> `fim[v]` é o instante mais cedo em que `v` termina, considerando durações e
> todas as dependências.

```text
fim[v] = duracao[v]                                se não há predecessores
fim[v] = duracao[v] + max(fim[u] para u -> v)      caso contrário
```

Processe em ordem topológica; assim todo `fim[u]` necessário já existe.

```python
def caminho_critico(
    ordem: list[str],
    predecessores: dict[str, tuple[str, ...]],
    duracao: dict[str, int],
) -> tuple[int, list[str]]:
    if not ordem:
        return 0, []

    fim: dict[str, int] = {}
    anterior: dict[str, str | None] = {}

    for tarefa in ordem:
        preds = predecessores[tarefa]
        predecessor = max(preds, key=fim.__getitem__) if preds else None
        inicio = fim[predecessor] if predecessor is not None else 0
        fim[tarefa] = inicio + duracao[tarefa]
        anterior[tarefa] = predecessor

    ultima = max(ordem, key=fim.__getitem__)
    caminho: list[str] = []
    atual: str | None = ultima
    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]
    caminho.reverse()
    return fim[ultima], caminho
```

Com listas de predecessores, cada vértice e aresta é examinado uma vez: tempo
`O(V+E)`, espaço `O(V)`. Empates em `max` precisam de política determinística se
a saída for contrato. Se o grafo contiver ciclo, não existe ordem topológica; a
validação deve ocorrer antes. Compare o resultado com a implementação real em
[graph.py](projetos/dependency-planner/src/dependency_planner/graph.py).

## Quando DP explode

Estados podem ser exponenciais: um estado por subconjunto custa `O(2^n)`. DP é
melhor que enumerar permutações `O(n!)`, mas ainda pode ser inviável. Antes de
implementar, estime:

```text
número de estados × transições por estado × bytes por célula
```

Considere formulação alternativa, compressão de estado, poda, aproximação,
algoritmo parametrizado ou limite de entrada. Dicionário esparso economiza
células não alcançadas, mas cada entrada tem overhead alto. Arrays compactos
exigem intervalo denso e índice conhecido.

## Algoritmos gulosos

Um algoritmo guloso escolhe o melhor passo local e nunca volta. Eficiência não
prova correção. Para aceitá-lo, procure:

- **propriedade de escolha gulosa:** existe solução ótima que começa com a
  escolha feita;
- **subestrutura ótima:** após a escolha, o restante é uma instância do mesmo
  tipo cuja solução ótima completa a original.

### Seleção de atividades

Problema: maximizar a quantidade de intervalos não sobrepostos. Estratégia:
ordenar por horário de término e escolher o próximo que começa após o último fim.

```python
def selecionar(intervalos: list[tuple[int, int]]) -> list[tuple[int, int]]:
    escolhidos: list[tuple[int, int]] = []
    ultimo_fim: int | None = None
    for inicio, fim in sorted(intervalos, key=lambda item: (item[1], item[0])):
        if ultimo_fim is None or inicio >= ultimo_fim:
            escolhidos.append((inicio, fim))
            ultimo_fim = fim
    return escolhidos
```

Ordenação custa `O(n log n)`; varredura, `O(n)`.

### Prova por argumento de troca

Seja `g` a atividade que termina primeiro e `o` a primeira atividade de uma
solução ótima. Como `fim(g) <= fim(o)`, substituir `o` por `g` não impede nenhuma
atividade posterior. Portanto existe solução ótima que começa por `g`. Removendo
atividades incompatíveis, resta o mesmo problema; repetir preserva otimalidade.

A prova depende do objetivo ser **quantidade**, não valor total. Com pesos,
terminar primeiro pode não maximizar valor.

## Contraexemplos para gulosos plausíveis

No troco com moedas `[1, 3, 4]` e total `6`, escolher sempre a maior moeda gera
`4+1+1` (três), enquanto `3+3` usa duas. O sistema canônico `[1,5,10,25]` em
alguns intervalos não prova a estratégia para entradas arbitrárias.

Na mochila 0/1, escolher maior valor por peso falha com capacidade `50` e itens
`(peso,valor)`: `(10,60)`, `(20,100)`, `(30,120)`. O guloso pega os dois primeiros
e vale `160`; o ótimo pega os dois últimos e vale `220`. A estratégia funciona
para mochila fracionária porque itens podem ser divididos — uma mudança de
invariante muda a prova.

Para encontrar contraexemplos:

1. escreva um oráculo exato por força bruta para entradas pequenas;
2. gere casos pequenos sistematicamente;
3. compare o guloso ao ótimo;
4. reduza a primeira falha até o menor caso explicativo.

Testes aleatórios não provam o guloso correto, mas encontram premissas falsas.

## Outras formas de prova gulosa

- **fica à frente:** após cada passo, a solução gulosa é pelo menos tão boa em
  uma medida parcial quanto qualquer concorrente;
- **invariante:** cada prefixo pode ser estendido a alguma solução ótima;
- **estrutura:** propriedades como matroides justificam gulosos para uma classe;
- **cut property:** em árvore geradora mínima, certa aresta leve é segura.

“Funcionou em exemplos” não entra na lista.

## Comparação entre abordagens

| Abordagem | Decisões | Evidência de correção | Custo típico |
|---|---|---|---|
| força bruta | enumera todas | exaustão | exponencial/fatorial |
| backtracking | enumera com poda | completude + poda segura | pior caso exponencial |
| DP | combina estados | recorrência + ordem/indução | estados × transições |
| guloso | escolha irrevogável | troca/invariante/propriedade | frequentemente ordenação + varredura |

Uma DP pode ser desnecessária se não há estados repetidos. Memoizar busca em uma
árvore sem convergência apenas adiciona memória. Um guloso correto costuma ser
mais simples e econômico; um guloso sem prova é apenas uma heurística.

## Comparação entre linguagens

- **Python:** `functools.cache` facilita memoização, mas tuplas/chaves e inteiros
  têm overhead; listas densas costumam ser mais rápidas.
- **Java:** arrays primitivos evitam boxing; profundidade recursiva ainda limita
  top-down; use `long` quando somas podem exceder `int`.
- **C:** inicialize sentinelas sem overflow (`INF + 1` é perigoso); documente
  alocação e verifique multiplicação de dimensões.
- **C#:** arrays e `Dictionary` cobrem denso/esparso; `checked` ajuda a detectar
  overflow quando o contrato exige.
- **JavaScript:** `Number` perde precisão além de `2^53-1`; use `BigInt` quando
  necessário, sem misturá-lo com `Number`; `Map` é preferível para chaves gerais.

## Falhas comuns e diagnóstico

| Sintoma | Causa | Diagnóstico |
|---|---|---|
| DP retorna ótimo impossível | transição aceita estado inválido | reconstrua decisões e valide-as |
| memoização dá resposta errada | chave omite parte do estado | encontre caminhos iguais na chave e futuros diferentes |
| resultado muda após otimizar memória | ordem sobrescreve dependência | desenhe quais células antigas cada atualização lê |
| memória explode | estado tem dimensão/intervalo excessivo | estime estados e bytes antes de alocar |
| guloso falha raro | propriedade não provada | compare com oráculo em casos pequenos |
| caminho crítico quebra em ciclo | ordem topológica inexistente | valide DAG e reporte ciclo antes da DP |
| overflow vira valor mínimo | tipo/sentinela inadequados | teste limites e use soma segura |

## Laboratórios

### Básico — duas formas de troco

Implemente memoização e tabulação com reconstrução.

**Critérios de aceite:** mesmo resultado em casos alcançáveis; `None` nos
impossíveis; moedas não positivas são rejeitadas; estados visitados são medidos;
estado/transição/base/prova e `O(total×M)` estão documentados.

### Intermediário — subsequência comum

Implemente LCS, reconstrua uma subsequência e reduza memória do valor.

**Critérios de aceite:** tabela segue a definição dos prefixos; reconstrução é
testada; versão de memória reduzida explica por que não consegue reconstruir sem
informação adicional; Unicode e vazios são cobertos; custo `O(nm)` é declarado.

### Avançado — caminho crítico e contraponto guloso

O Dependency Planner de referência já calcula término mínimo e caminho crítico.
Sem consultar `graph.py`, reimplemente primeiro a recorrência em um módulo de
exercício e valide-a com um oráculo exaustivo para DAGs pequenas. Depois compare
as duas implementações, explique qualquer diferença e acrescente ao projeto um
relatório opcional com o término de cada tarefa; não duplique a regra no adapter.

**Critérios de aceite:** cálculo é `O(V+E)` depois da ordem topológica; empates
são determinísticos; ciclo e duração inválida falham antes; um algoritmo de
referência valida DAGs pequenas; proponha uma regra gulosa de escalonamento e
apresente contraexemplo ou prova sob premissas explícitas.

## Checklist de domínio

- [ ] Defino cada estado em uma frase sem mencionar “célula qualquer”.
- [ ] Derivo a transição a partir da última/primeira decisão.
- [ ] Provo bases, cobertura das alternativas e ordem de avaliação.
- [ ] Distingo memoização, tabulação e busca sem sobreposição.
- [ ] Reconstruo uma solução e valido suas decisões.
- [ ] Otimizo memória sem reutilizar dados da iteração errada.
- [ ] Reconheço algoritmo pseudopolinomial e estimo bytes.
- [ ] Não aceito uma estratégia gulosa sem argumento de correção.
- [ ] Produzo contraexemplo com oráculo exato para casos pequenos.
- [ ] Conecto DP em DAG ao caminho crítico do Dependency Planner.
