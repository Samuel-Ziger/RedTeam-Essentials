# 06 — Recursão e backtracking

Recursão resolve um problema chamando a mesma operação sobre uma instância
menor. Backtracking usa essa ideia para percorrer uma árvore de decisões,
descartar ramos impossíveis e restaurar o estado antes de tentar outra escolha.
Ambos são simples de escrever e fáceis de errar quando pilha, progresso,
mutabilidade ou tamanho do espaço de busca ficam implícitos.

## Objetivos verificáveis

Ao final, você deverá conseguir:

- identificar caso base, medida de progresso e hipótese indutiva;
- desenhar frames da call stack e calcular seu espaço assintótico;
- decidir entre recursão, pilha explícita e iteração;
- explicar por que recursão de cauda não garante espaço constante;
- implementar backtracking com escolha, restrição, restauração e término;
- provar que uma poda é segura e distinguir poda de heurística;
- estimar custo pela árvore de busca e pelo tamanho da saída;
- aplicar DFS ao grafo do Dependency Planner sem estourar a pilha.

Pré-requisitos: funções, escopo, listas, grafos e análise de complexidade. Execute
os exemplos com entradas pequenas e desenhe as chamadas antes de otimizar.

## Modelo mental: problema, frame e progresso

Cada chamada ativa ocupa um **frame**: argumentos, variáveis locais, endereço de
retorno e informações do runtime. Em uma chamada recursiva, o frame atual não
desaparece necessariamente; ele espera o resultado do próximo.

```python
def fatorial(n: int) -> int:
    if n < 0:
        raise ValueError("n deve ser nao negativo")
    if n <= 1:                  # caso base
        return 1
    return n * fatorial(n - 1)  # instância estritamente menor
```

Para `fatorial(4)`, a fase de descida acumula frames:

```text
fatorial(4)
  4 * fatorial(3)
        3 * fatorial(2)
              2 * fatorial(1)
                    1
```

Depois a pilha desenrola: `1`, `2`, `6`, `24`. O invariante da descida é que
`n` continua inteiro não negativo; a medida de término é `n`, que diminui a cada
passo e não pode diminuir para sempre nesse domínio.

Uma função recursiva correta precisa de três argumentos:

1. **caso base:** resolve diretamente a menor instância;
2. **progresso:** cada chamada se aproxima do caso base segundo uma medida
   bem-fundada;
3. **composição:** assumindo corretas as chamadas menores, o passo atual produz
   a solução correta.

Checar apenas “há um `if`” não prova término. Em `f(n - 2)` para números ímpares,
um caso base `n == 0` nunca é alcançado. Use `n <= 0` se o domínio permitir ou
rejeite a entrada antes.

## Custo: tempo não é profundidade

Fatorial executa `n` chamadas: tempo `O(n)` e profundidade `O(n)`. Cada frame
ocupa espaço constante neste exemplo, portanto pilha `O(n)`. Já uma divisão de
vetor pode manter referências ou temporários maiores; não presuma frame gratuito.

Fibonacci ingênuo ramifica:

```python
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

A profundidade é `O(n)`, mas a quantidade de nós da árvore é exponencial,
aproximadamente `O(φ^n)`. Espaço de pilha mede o maior caminho simultâneo, não a
quantidade total de chamadas. Memoização reduz estados repetidos a `n`, com
tempo `O(n)` e memória `O(n)`; uma iteração usa tempo `O(n)` e espaço `O(1)`.

### Limites reais da pilha

Não existe profundidade portátil “segura”. Ela depende de linguagem, runtime,
SO, tamanho do frame e configuração:

| Linguagem | Comportamento prático |
|---|---|
| Python | limite de recursão do interpretador; profundidade excessiva gera `RecursionError` |
| Java | pilha por thread; excesso gera `StackOverflowError` |
| C | limite depende da pilha; overflow é comportamento indefinido e perigoso |
| C# | excesso normalmente gera `StackOverflowException`, não recuperável de forma comum |
| JavaScript | limite depende do engine; costuma lançar `RangeError` |

Aumentar o limite do Python não aumenta a pilha nativa com segurança. Para uma
cadeia de milhões de tarefas recebida de entrada, use pilha explícita ou
algoritmo iterativo. Capturar stack overflow e continuar não é estratégia.

## Recursão de cauda

Uma chamada é de cauda quando é a última operação da função:

```python
def fatorial_cauda(n: int, acumulado: int = 1) -> int:
    if n <= 1:
        return acumulado
    return fatorial_cauda(n - 1, acumulado * n)
```

Matematicamente ela pode ser convertida em laço. Contudo, Python não elimina
frames de cauda; Java e C# não oferecem garantia geral; JavaScript especificou
proper tail calls em condições estritas, mas suporte prático varia; compiladores
C podem otimizar, sem obrigação semântica na forma geral. Portanto, não prometa
`O(1)` de pilha só porque a chamada está na cauda.

Versão iterativa explícita:

```python
def fatorial_iterativo(n: int) -> int:
    if n < 0:
        raise ValueError("n deve ser nao negativo")
    acumulado = 1
    for valor in range(2, n + 1):
        acumulado *= valor
    return acumulado
```

Ela preserva tempo `O(n)` e usa espaço auxiliar `O(1)`. Ainda há crescimento do
inteiro em Python; complexidade aritmética com inteiros arbitrários não é
rigorosamente constante por multiplicação.

## DFS recursiva e pilha explícita

Detectar ciclo no grafo de dependências pode usar três cores:

- branco: não visitado;
- cinza: está na pilha ativa;
- preto: concluído.

Uma aresta para cinza é um ciclo. Invariante: todo vértice cinza pertence ao
caminho DFS atual; todo preto teve seus descendentes processados.

```python
def tem_ciclo(grafo: dict[str, tuple[str, ...]]) -> bool:
    cor = {vertice: "branco" for vertice in grafo}

    def visitar(vertice: str) -> bool:
        cor[vertice] = "cinza"
        for vizinho in grafo[vertice]:
            if cor[vizinho] == "cinza":
                return True
            if cor[vizinho] == "branco" and visitar(vizinho):
                return True
        cor[vertice] = "preto"
        return False

    return any(
        cor[vertice] == "branco" and visitar(vertice)
        for vertice in grafo
    )
```

Tempo `O(V + E)`, memória `O(V)` para cores e até `O(V)` de call stack. Para
grafos profundos, uma pilha explícita precisa guardar também qual vizinho será o
próximo, não somente o vértice; caso contrário, fica fácil marcar preto cedo.
O Dependency Planner usa ordenação de Kahn, que também detecta ciclo e evita
recursão. Compare com
[graph.py](projetos/dependency-planner/src/dependency_planner/graph.py).

## Backtracking como busca em árvore

Backtracking mantém uma solução parcial. Em cada nível:

1. verifica se a solução está completa;
2. enumera escolhas candidatas;
3. rejeita candidatas que violam restrições;
4. aplica uma escolha;
5. explora recursivamente;
6. desfaz exatamente a escolha.

```text
buscar(estado):
    se completo(estado): produza uma solução
    senão:
        para escolha em candidatas(estado):
            se promissora(estado, escolha):
                aplicar(estado, escolha)
                buscar(estado)
                desfazer(estado, escolha)
```

O invariante central é: ao iniciar cada iteração, `estado` é exatamente o estado
recebido naquele nível. Se `desfazer` não for simétrico, um ramo contamina outro.
Uma alternativa é criar estado imutável por chamada; simplifica raciocínio, mas
pode copiar dados e aumentar memória.

## Exemplo trabalhado: combinações com poda

Queremos todas as combinações de tamanho `k`, sem repetir posição:

```python
from collections.abc import Iterator, Sequence
from typing import TypeVar

T = TypeVar("T")


def combinacoes(valores: Sequence[T], k: int) -> Iterator[tuple[T, ...]]:
    if k < 0 or k > len(valores):
        return

    atual: list[T] = []

    def visitar(inicio: int) -> Iterator[tuple[T, ...]]:
        if len(atual) == k:
            yield tuple(atual)       # snapshot: não vaza a lista mutável
            return

        faltam = k - len(atual)
        ultimo_inicio = len(valores) - faltam
        for indice in range(inicio, ultimo_inicio + 1):
            atual.append(valores[indice])
            yield from visitar(indice + 1)
            removido = atual.pop()
            assert removido == valores[indice]

    yield from visitar(0)
```

Para `valores=[A,B,C,D]` e `k=2`, o primeiro caminho produz `(A,B)`, restaura
para `[A]`, tenta `C`, depois `D`. O limite do laço é poda segura: se restam
menos posições que elementos necessários, nenhum descendente completa a solução.

Existem `C(n,k)` resultados. Qualquer algoritmo que enumera todos custa ao menos
`Ω(C(n,k) × k)` para materializá-los. O gerador evita guardar todos de uma vez,
mas retém estado e pilha `O(k)`. “Usa pouca memória” não significa “é rápido”.

### Duplicatas por valor

Se a entrada contém `[A, A, B]`, posições distintas produzem combinações iguais.
Para eliminar duplicatas, ordene e, no mesmo nível, ignore um valor igual ao
anterior. Isso exige que os valores sejam ordenáveis ou uma chave. Usar um
`set` ao final é mais simples, mas materializa toda a saída e pode esconder
trabalho exponencial.

## Poda correta, limite e heurística

**Poda** prova que um ramo não contém solução relevante. **Branch and bound**
compara um limite otimista do ramo com a melhor solução conhecida. **Heurística**
muda a ordem ou aproxima a busca, mas não necessariamente elimina ramos com prova.

Exemplo em seleção de tarefas sob orçamento: se a soma das durações já excedeu o
limite, durações positivas garantem que adicionar tarefas nunca recupera o ramo;
a poda é segura. Se houver durações negativas, a mesma poda fica incorreta.

Ordenar escolhas “mais promissoras” pode encontrar uma solução cedo e melhorar
branch and bound, mas não altera o pior caso por si só. Memoizar estados ajuda
quando diferentes caminhos alcançam o mesmo subproblema; se o estado usado na
chave omite uma restrição, o cache devolve resposta inválida.

### Prova de completude do backtracking

Para defender um algoritmo:

1. cada solução válida corresponde a uma sequência de escolhas;
2. o laço considera toda escolha permitida em cada prefixo;
3. a poda remove apenas prefixos que não podem chegar a solução;
4. a restauração permite explorar irmãos independentemente;
5. a profundidade é limitada, portanto a busca termina.

Se quiser apenas a primeira solução, propague `True` e pare. Se quiser todas,
não encerre o pai após o primeiro sucesso. Esses contratos produzem algoritmos
diferentes.

## Comparação entre linguagens

- **Python:** geradores expressam enumeração preguiçosa; cuidado com limite de
  recursão e listas mutáveis capturadas por closure.
- **Java:** iteradores preguiçosos exigem mais estado explícito; arrays/objetos
  mutáveis precisam de cópia ao registrar solução.
- **C:** controle da pilha e ownership é manual; valide profundidade e limites,
  desfaça alocações em todos os caminhos de erro.
- **C#:** `yield return` combina bem com enumeração; o estado do iterador é
  transformado pelo compilador, mas recursão ainda consome pilha.
- **JavaScript:** generators com `function*` permitem `yield*`; `async` não
  resolve profundidade recursiva nem transforma busca CPU-bound em paralela.

## Falhas comuns e diagnóstico

| Sintoma | Causa provável | Diagnóstico |
|---|---|---|
| recursão nunca termina | medida não diminui/caso base incompleto | registre argumento por nível e prove limite |
| `RecursionError`/stack overflow | entrada profunda | meça profundidade e converta para pilha explícita |
| soluções “herdam” escolhas | faltou desfazer mutação | faça assert do estado antes/depois da chamada |
| todas as soluções ficam iguais | referência mutável foi armazenada | registre cópia/tupla no caso completo |
| solução válida desaparece | poda sem prova | encontre menor contraexemplo por força bruta |
| saída contém duplicatas | escolhas equivalentes por valor | ordene e pule repetição no mesmo nível |
| busca continua lenta com heurística | árvore ainda exponencial | conte nós visitados, não só tempo em um caso |

Instrumente `chamadas`, `profundidade_maxima`, `podas` e `solucoes`. Uma
otimização deve reduzir uma métrica explicável, sem alterar o conjunto esperado.

## Laboratórios

### Básico — pilha e equivalência

Implemente DFS recursiva e iterativa em um grafo pequeno.

**Critérios de aceite:** ambas visitam o mesmo conjunto; ordem é documentada;
tempo é `O(V+E)`; a versão iterativa processa cadeia com 100 mil vértices sem
recursão; testes cobrem vazio, desconectado e ciclo.

### Intermediário — permutações únicas

Gere permutações sem duplicatas para valores repetidos.

**Critérios de aceite:** `[1,1,2]` produz exatamente três resultados; cada ramo
restaura o estado; implementação pode produzir sob demanda; contadores mostram
o efeito da poda; custo é explicado em função da saída.

### Avançado — planejamento com restrições

Crie uma extensão isolada do Dependency Planner que encontre um lote de tarefas
disponíveis sob um limite de duração, maximizando a duração ocupada.

**Critérios de aceite:** dependências continuam respeitadas; uma solução por
força bruta serve de oráculo para entradas pequenas; toda poda tem justificativa;
há contraexemplo para uma heurística gulosa; benchmark informa nós, podas e
tempo; entrada grande possui limite/cancelamento.

## Checklist de domínio

- [ ] Identifico caso base, progresso e composição de uma recursão.
- [ ] Diferencio quantidade de chamadas, profundidade e tamanho da saída.
- [ ] Não presumo otimização de cauda na linguagem escolhida.
- [ ] Converto uma recursão profunda em estado/pilha explícitos.
- [ ] Declaro o invariante de restauração de um backtracking.
- [ ] Provo que uma poda não remove soluções válidas.
- [ ] Distingo poda, branch and bound, memoização e heurística.
- [ ] Trato ownership de soluções mutáveis corretamente.
- [ ] Instrumento a árvore de busca antes de afirmar que otimizei.
- [ ] Escolho recursão pela clareza e segurança, não pela aparência matemática.
