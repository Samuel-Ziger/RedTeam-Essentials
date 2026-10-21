# Lógica de programação e algoritmos

Um algoritmo é uma sequência finita e não ambígua de passos que transforma
entradas em saídas. Um programa é a implementação de um ou mais algoritmos em
uma linguagem que o computador consegue executar.

Este capítulo parte do zero, mas não para na memorização de `if`, `else` e
laços. O objetivo é aprender a justificar por que um algoritmo termina, por que
seu resultado está correto e como seus dados se comportam durante a execução.

## Objetivos de aprendizagem

Ao concluir, você deverá conseguir:

- distinguir valor, tipo, variável, expressão e instrução;
- construir condições booleanas e explicar sua tabela-verdade;
- usar `if/elif/else`, `for` e `while` sem erros de fronteira;
- projetar funções com contrato, retorno e efeitos explícitos;
- escolher entre lista, mapa, conjunto, fila e pilha;
- rastrear estado, escopo, mutabilidade e referências compartilhadas;
- tratar entradas inválidas no limite do sistema;
- argumentar sobre correção, término e custo de um algoritmo;
- traduzir a mesma lógica para Python, Java, C, C# e JavaScript.

Pré-requisito recomendado: ter concluído
[Como estudar programação e resolver problemas](00-como-estudar.md).

## 1. Como um programa executa

Em um modelo simplificado, o runtime repete:

```text
obter instrução → interpretar seus operandos → executar → avançar
```

O fluxo normal é de cima para baixo. Três estruturas mudam esse fluxo:

- **decisão:** escolhe um caminho;
- **repetição:** retorna a um ponto anterior enquanto uma condição vale;
- **chamada de função:** transfere o controle para outra unidade e depois volta.

Considere:

```python
preco = 80.0
quantidade = 3
subtotal = preco * quantidade

if subtotal >= 200:
    desconto = subtotal * 0.10
else:
    desconto = 0.0

total = subtotal - desconto
print(total)
```

O programa não “entende vendas”. Ele apenas:

1. associa `80.0` a `preco`;
2. associa `3` a `quantidade`;
3. calcula `240.0`;
4. compara `240.0 >= 200`;
5. executa o bloco verdadeiro;
6. calcula e imprime `216.0`.

Aprender lógica é conseguir realizar esse rastreamento e, depois, abstraí-lo
sem perder precisão.

## 2. Valores, tipos, variáveis e constantes

### Valores e tipos

Um **valor** é um dado concreto. O **tipo** define sua representação e quais
operações fazem sentido.

| Categoria | Exemplos | Operações comuns |
|-----------|----------|------------------|
| inteiro | `-3`, `0`, `42` | soma, divisão inteira, resto |
| ponto flutuante | `3.14`, `-0.5` | medidas e aproximações |
| booleano | `true`, `false` | `e`, `ou`, `não` |
| texto/string | `"Ana"`, `""` | concatenar, buscar, medir |
| ausência | `None`, `null` | representar “sem valor” |

O mesmo símbolo pode ter significado diferente conforme o tipo:

```python
print(2 + 3)        # 5: soma de inteiros
print("2" + "3")    # "23": concatenação de textos
```

Não confunda o número `42` com o texto `"42"`. O primeiro participa de contas;
o segundo é uma sequência de caracteres que precisa ser validada e convertida.

### Variável é um nome associado a um valor

```python
idade = 20
nome = "Ana"
ativo = True
```

Uma variável não é necessariamente “uma caixa universal”. Em Python e
JavaScript, o nome referencia um valor em tempo de execução. Em Java, C e C#,
o tipo declarado também restringe quais valores podem ser associados.

```java
int idade = 20;
String nome = "Ana";
boolean ativo = true;
```

Escolha nomes pelo papel no problema:

```text
x                 ruim: exige descobrir o significado
preco_total       bom: revela domínio e intenção
usuarios_ativos   bom: indica coleção e critério
```

### Atribuição não é igualdade matemática

```python
contador = 2
contador = contador + 1
```

Na segunda linha, o valor atual de `contador` é lido, soma-se `1`, e o nome
passa a apontar para o resultado `3`. Em matemática, `x = x + 1` seria
impossível; em programação, `=` normalmente significa atribuição.

### Constantes expressam regras estáveis

```python
LIMITE_TENTATIVAS = 3
TAXA_DESCONTO = 0.10
```

Python usa convenção de maiúsculas; Java, C e C# possuem mecanismos adicionais
como `final`, `const` e `readonly`. O benefício principal é dar nome à regra e
evitar números mágicos repetidos.

### Números têm limites e aproximações

Ponto flutuante binário não representa exatamente toda fração decimal:

```python
print(0.1 + 0.2)  # normalmente 0.30000000000000004
```

Por isso, use uma representação apropriada para dinheiro, como centavos
inteiros ou um tipo decimal da linguagem:

```python
preco_centavos = 1990
quantidade = 3
total_centavos = preco_centavos * quantidade
assert total_centavos == 5970
```

Quando o domínio é uma medida aproximada em ponto flutuante, compare com uma
tolerância coerente com o problema:

```python
def aproximadamente_iguais(a: float, b: float, tolerancia: float = 1e-9) -> bool:
    return abs(a - b) <= tolerancia
```

Inteiros também podem ter limite fixo em C, Java e C#. Somar além do intervalo
pode causar overflow. Conhecer o tipo faz parte do contrato do dado.

## 3. Expressões e operadores

Uma **expressão** é uma combinação que produz um valor:

```python
preco * quantidade
idade >= 18
usuario_ativo and possui_permissao
```

Uma **instrução** provoca uma ação, como associar, retornar ou controlar o
fluxo:

```python
total = preco * quantidade
return total
```

### Famílias de operadores

- aritméticos: `+`, `-`, `*`, `/`, divisão inteira `//`, resto `%`;
- comparação: `==`, `!=`, `<`, `<=`, `>`, `>=`;
- lógicos: `and`, `or`, `not` em Python;
- atribuição: `=`, além de abreviações como `+=`;
- associação/acesso: índices, atributos e chamadas.

Use parênteses quando a precedência não estiver imediatamente óbvia:

```python
total = (preco_unitario * quantidade) - desconto
permitido = usuario_ativo and (administrador or possui_permissao)
```

Parênteses bem usados comunicam agrupamento; não são apenas uma correção para
quem esqueceu a tabela de precedência.

## 4. Lógica booleana

Uma expressão booleana produz verdadeiro ou falso. Estas são as tabelas
fundamentais:

| `A` | `B` | `A and B` | `A or B` |
|-----|-----|-----------|----------|
| falso | falso | falso | falso |
| falso | verdadeiro | falso | verdadeiro |
| verdadeiro | falso | falso | verdadeiro |
| verdadeiro | verdadeiro | verdadeiro | verdadeiro |

| `A` | `not A` |
|-----|---------|
| falso | verdadeiro |
| verdadeiro | falso |

Exemplo de regra:

```python
pode_entrar = idade >= 18 and possui_documento
```

As duas condições precisam ser verdadeiras. Já uma recuperação pode aceitar
uma de duas provas:

```python
pode_recuperar = possui_email_verificado or possui_codigo_reserva
```

### Curto-circuito

Em muitas linguagens, `and`/`&&` para na primeira condição falsa, e `or`/`||`
para na primeira verdadeira:

```python
if usuario is not None and usuario.ativo:
    print("usuário ativo")
```

Se `usuario` for `None`, a segunda parte não é avaliada. A ordem importa:
inverter as condições tentaria acessar `.ativo` em uma ausência.

### Leis de De Morgan

Negar uma condição composta troca `and` por `or` e nega cada parte:

```text
not (A and B) == (not A) or (not B)
not (A or B)  == (not A) and (not B)
```

Exemplo:

```python
# formas equivalentes
if not (idade >= 18 and possui_documento):
    negar_entrada()

if idade < 18 or not possui_documento:
    negar_entrada()
```

Prefira a forma que descreve a regra com menor esforço mental.

## 5. Decisão com `if`, `elif` e `else`

Uma decisão seleciona exatamente um caminho entre alternativas ordenadas:

```python
def classificar_temperatura(temperatura: float) -> str:
    if temperatura >= 35:
        return "muito quente"
    elif temperatura >= 25:
        return "quente"
    else:
        return "amena"
```

As condições são avaliadas de cima para baixo. Para `36`, a primeira é
verdadeira e as demais nem são testadas. Se `temperatura >= 25` viesse antes,
a categoria “muito quente” se tornaria inalcançável.

### Transforme regras em tabela de decisão

Antes do código:

| Temperatura | Resultado |
|-------------|-----------|
| `>= 35` | muito quente |
| `>= 25` e `< 35` | quente |
| `< 25` | amena |

Uma tabela ajuda a detectar intervalos descobertos e sobrepostos. Para regras
com várias condições, liste as combinações relevantes:

| Cliente ativo | Total `>= 500` | Desconto |
|---------------|----------------|----------|
| não | qualquer | 0% |
| sim | não | 5% |
| sim | sim | 10% |

Implementação com cláusulas de guarda:

```python
def calcular_desconto(total: float, cliente_ativo: bool) -> float:
    if total < 0:
        raise ValueError("total não pode ser negativo")
    if not cliente_ativo:
        return 0.0
    if total >= 500:
        return total * 0.10
    return total * 0.05
```

As verificações que encerram cedo são chamadas de **guard clauses**. Elas
evitam blocos profundamente aninhados e deixam o caminho principal visível.

### Limites inclusivos e exclusivos

Compare cuidadosamente:

```text
idade > 18    exclui 18
idade >= 18   inclui 18
0 <= nota <= 10  inclui ambos os limites em Python
```

Para cada limite `L`, teste pelo menos `L - 1`, `L` e `L + 1` quando o domínio
permitir. Com decimais, escolha valores representativos, como `6.99`, `7.00` e
`7.01`.

## 6. Repetição: `for` e `while`

Use repetição quando a mesma regra se aplica a vários valores ou enquanto um
estado satisfaz uma condição.

### `for`: percorrer uma coleção ou faixa

```python
total = 0
for valor in [10, 20, 30]:
    total += valor
print(total)  # 60
```

O padrão usado é um **acumulador**:

1. começa no elemento neutro, `0` para soma;
2. incorpora um item por iteração;
3. ao fim, representa o agregado de todos os itens vistos.

Outros padrões frequentes:

```python
def apenas_pares(valores: list[int]) -> list[int]:
    resultado = []
    for valor in valores:
        if valor % 2 == 0:
            resultado.append(valor)
    return resultado


def contem_negativo(valores: list[int]) -> bool:
    for valor in valores:
        if valor < 0:
            return True  # encerra assim que encontra evidência
    return False
```

O primeiro é **filtragem**; o segundo é **busca com término antecipado**.

### `while`: repetir enquanto o estado exigir

```python
tentativas = 0
autenticado = False

while tentativas < 3 and not autenticado:
    autenticado = verificar_credencial_sintetica()
    tentativas += 1
```

Todo `while` precisa de três elementos:

1. estado inicial;
2. condição de continuação;
3. progresso que aproxima a condição de falso.

Sem progresso, o laço pode ser infinito:

```python
# incorreto: tentativas nunca muda
tentativas = 0
while tentativas < 3:
    print(tentativas)
```

### Invariante de laço

Uma invariante de laço é verdadeira antes e depois de cada iteração. No
algoritmo de soma:

```python
total = 0
for valor in valores:
    total += valor
```

A invariante é:

> `total` contém a soma de todos os elementos já processados.

No início nenhum elemento foi processado e a soma é `0`. Cada iteração mantém a
afirmação. Quando o laço termina, todos foram processados; portanto, `total` é a
soma da coleção inteira. Essa é uma pequena prova de correção.

### Erro de uma posição

Faixas costumam usar início inclusivo e fim exclusivo:

```python
list(range(1, 4))  # [1, 2, 3]
```

Pergunte sempre:

- o primeiro índice válido é qual?
- o último valor deve ser incluído?
- o que acontece com uma coleção vazia?
- quantas iterações deveriam ocorrer?

Evite iterar por índice quando o item basta:

```python
for nome in nomes:
    print(nome)
```

Use índice quando ele fizer parte do problema:

```python
for indice, nome in enumerate(nomes):
    print(indice, nome)
```

## 7. Funções e contratos

Uma função dá nome a uma regra, recebe entradas e produz um resultado ou efeito.

```python
def media(valores: list[float]) -> float:
    """Retorna a média de uma lista não vazia sem alterá-la."""
    if not valores:
        raise ValueError("a lista não pode ser vazia")
    return sum(valores) / len(valores)
```

Contrato:

- entrada: lista de números;
- pré-condição: lista não vazia;
- efeito: nenhum; a lista não é modificada;
- saída: número entre o menor e o maior item;
- erro: `ValueError` para lista vazia.

### Parâmetro, argumento e retorno

Em `media([7, 8, 9])`:

- `valores` é o **parâmetro** definido pela função;
- `[7, 8, 9]` é o **argumento** fornecido na chamada;
- `8.0` é o valor de **retorno**.

Imprimir não é retornar:

```python
def dobro_incorreto(numero: int) -> None:
    print(numero * 2)


def dobro(numero: int) -> int:
    return numero * 2


resultado = dobro(4) + 1  # 9; o retorno pode ser composto
```

### Função pura e efeito colateral

Uma função pura:

- produz o mesmo resultado para os mesmos argumentos;
- não altera estado externo observável.

```python
def area_retangulo(largura: float, altura: float) -> float:
    return largura * altura
```

Ler arquivo, imprimir, gravar banco, consultar relógio e modificar uma coleção
recebida são efeitos. Eles são necessários em aplicações, mas devem ficar
explícitos e, quando possível, nas bordas.

### Escopo

Escopo define onde um nome pode ser usado:

```python
def calcular() -> int:
    resultado_local = 42
    return resultado_local

# resultado_local não existe aqui
```

Prefira estado local e parâmetros. Uma variável global mutável cria dependência
oculta: qualquer parte do programa pode mudar seu valor e afetar outras partes.

### Pilha de chamadas

Quando uma função chama outra, o runtime preserva o ponto de retorno e as
variáveis locais de cada chamada:

```text
programa principal
└── calcular_total
    └── calcular_desconto
```

Quando `calcular_desconto` termina, seu quadro é removido e o controle volta a
`calcular_total`. Uma exceção não tratada percorre essa pilha, razão pela qual o
traceback mostra a cadeia de chamadas.

### Recursão

Uma função recursiva chama a si mesma. Ela precisa de:

- caso-base que encerra;
- passo que reduz o problema em direção ao caso-base.

```python
def fatorial(n: int) -> int:
    if n < 0:
        raise ValueError("n deve ser não negativo")
    if n == 0:
        return 1
    return n * fatorial(n - 1)
```

Para tarefas simples, um laço pode ser mais legível e evitar excesso de frames.
Recursão é especialmente natural em árvores e problemas definidos
recursivamente; não é uma versão “mais avançada” de todo laço.

## 8. Coleções fundamentais

Escolha a estrutura pela operação necessária, não pelo costume.

| Estrutura | Propriedade principal | Operações típicas | Exemplo |
|-----------|-----------------------|------------------|---------|
| lista/array | ordem e repetição | acessar, percorrer, anexar | tarefas ordenadas |
| mapa/dicionário | chave → valor | localizar por chave | usuário por ID |
| conjunto | elementos únicos | pertinência, união, interseção | tags únicas |
| fila | primeiro a entrar, primeiro a sair | enfileirar, desenfileirar | trabalhos pendentes |
| pilha | último a entrar, primeiro a sair | empilhar, desempilhar | desfazer ações |

Exemplo com dicionário para contagem:

```python
def contar_palavras(palavras: list[str]) -> dict[str, int]:
    frequencias: dict[str, int] = {}
    for palavra in palavras:
        chave = palavra.casefold()
        frequencias[chave] = frequencias.get(chave, 0) + 1
    return frequencias


assert contar_palavras(["Sol", "sol", "Lua"]) == {"sol": 2, "lua": 1}
```

Uma lista de pares também representaria frequências, mas exigiria procurar a
palavra repetidamente. O dicionário expressa diretamente a intenção: localizar
uma contagem por chave.

## 9. Mutabilidade, cópia e aliasing

Valores imutáveis, como inteiros e strings em Python, não mudam internamente;
uma “alteração” produz outro valor. Listas são mutáveis.

```python
original = [1, 2]
apelido = original
apelido.append(3)

print(original)  # [1, 2, 3]
```

`apelido` e `original` referenciam o mesmo objeto. Isso é **aliasing**. Para uma
cópia rasa independente da lista externa:

```python
copia = original.copy()
```

Se a lista contiver outras coleções mutáveis, a cópia rasa ainda compartilha os
objetos internos. O importante é documentar propriedade e mutação:

```python
def ordenar_copia(valores: list[int]) -> list[int]:
    return sorted(valores)  # não altera a lista recebida
```

Efeitos inesperados sobre argumentos estão entre as causas mais comuns de
defeitos em programas com estado.

## 10. Entrada, validação e erros

Tudo que entra pelo terminal, arquivo, formulário ou rede deve ser tratado como
dado não confiável. Validação possui camadas:

1. **presença:** existe algum valor?
2. **sintaxe:** pode ser convertido para o tipo esperado?
3. **domínio:** está dentro dos limites permitidos?
4. **regra de negócio:** a operação é permitida neste estado?

```python
def converter_idade(texto: str) -> int:
    texto_limpo = texto.strip()
    if not texto_limpo:
        raise ValueError("idade é obrigatória")

    try:
        idade = int(texto_limpo)
    except ValueError as erro:
        raise ValueError("idade deve ser um número inteiro") from erro

    if not 0 <= idade <= 130:
        raise ValueError("idade deve estar entre 0 e 130")
    return idade
```

Existem três categorias básicas de falha:

1. **sintaxe:** o código não pode ser analisado ou compilado;
2. **execução:** ocorre divisão por zero, arquivo ausente ou conversão inválida;
3. **lógica:** executa, mas retorna uma resposta incorreta.

Capture apenas o erro para o qual existe uma resposta correta. Evite:

```python
try:
    executar_tudo()
except Exception:
    pass  # esconde causa, contexto e estado do programa
```

Tratar erro não significa fingir sucesso. Pode significar devolver uma mensagem
clara, registrar contexto não sensível, liberar um recurso ou propagar uma
exceção mais específica.

## 11. Um problema completo: resumo de medições

### Requisito

Receber medições numéricas já convertidas, aceitar apenas valores de `0` a
`100`, ignorar os inválidos e retornar:

- quantidade válida;
- mínimo e máximo válidos;
- média dos válidos;
- quantidade rejeitada.

Se não houver medição válida, mínimo, máximo e média devem ser ausência.

### Exemplos

| Entrada | Saída resumida |
|---------|----------------|
| `[10, 20, 30]` | 3 válidas, média 20, 0 rejeitadas |
| `[-1, 50, 101]` | 1 válida, média 50, 2 rejeitadas |
| `[]` | 0 válidas, média ausente, 0 rejeitadas |

### Pseudocódigo

```text
iniciar lista validas vazia
iniciar rejeitadas com zero

para cada medicao
    se 0 <= medicao <= 100
        adicionar a validas
    senão
        incrementar rejeitadas

se validas estiver vazia
    retornar contagem zero e estatísticas ausentes

retornar contagem, mínimo, máximo, média e rejeitadas
```

### Implementação

```python
def resumir_medicoes(medicoes: list[float]) -> dict[str, int | float | None]:
    validas: list[float] = []
    rejeitadas = 0

    for medicao in medicoes:
        if 0 <= medicao <= 100:
            validas.append(medicao)
        else:
            rejeitadas += 1

    if not validas:
        return {
            "quantidade": 0,
            "minimo": None,
            "maximo": None,
            "media": None,
            "rejeitadas": rejeitadas,
        }

    return {
        "quantidade": len(validas),
        "minimo": min(validas),
        "maximo": max(validas),
        "media": sum(validas) / len(validas),
        "rejeitadas": rejeitadas,
    }
```

### Testes

```python
def testar_resumo() -> None:
    comum = resumir_medicoes([10, 20, 30])
    assert comum == {
        "quantidade": 3,
        "minimo": 10,
        "maximo": 30,
        "media": 20,
        "rejeitadas": 0,
    }

    limites = resumir_medicoes([0, 100])
    assert limites["quantidade"] == 2
    assert limites["media"] == 50

    parcial = resumir_medicoes([-1, 50, 101])
    assert parcial["quantidade"] == 1
    assert parcial["rejeitadas"] == 2

    vazio = resumir_medicoes([])
    assert vazio["media"] is None
    assert vazio["rejeitadas"] == 0
```

### Análise

Se existem `n` medições, o laço examina cada uma uma vez: tempo proporcional a
`n`, escrito como **O(n)**. A lista `validas` pode guardar até `n` itens, então o
espaço adicional também é **O(n)**.

Uma versão mais econômica poderia calcular contagem, soma, mínimo e máximo em
uma passagem sem guardar todas as válidas, usando **O(1)** de espaço adicional.
Essa otimização só deve ser feita preservando o contrato e os testes.

## 12. A mesma decisão em cinco linguagens

A lógica abaixo classifica uma nota válida de `0` a `10`. Observe que o
algoritmo permanece; mudam tipos, operadores, blocos e forma de sinalizar erro.

### Python

```python
from math import isfinite


def classificar_nota(nota: float) -> str:
    if not isfinite(nota) or not 0 <= nota <= 10:
        raise ValueError("nota deve ser finita e estar em 0..10")
    if nota >= 7:
        return "aprovado"
    if nota >= 5:
        return "recuperacao"
    return "reprovado"
```

### Java

```java
static String classificarNota(double nota) {
    if (!Double.isFinite(nota) || nota < 0 || nota > 10) {
        throw new IllegalArgumentException("nota deve ser finita e estar em 0..10");
    }
    if (nota >= 7) {
        return "aprovado";
    }
    if (nota >= 5) {
        return "recuperacao";
    }
    return "reprovado";
}
```

### C

Em C, uma opção é separar validade do resultado e usar um `enum`:

```c
#include <math.h>
#include <stdbool.h>
#include <stddef.h>

typedef enum {
    REPROVADO,
    RECUPERACAO,
    APROVADO
} Situacao;

bool classificar_nota(double nota, Situacao *saida) {
    if (!isfinite(nota) || nota < 0.0 || nota > 10.0 || saida == NULL) {
        return false;
    }
    if (nota >= 7.0) {
        *saida = APROVADO;
    } else if (nota >= 5.0) {
        *saida = RECUPERACAO;
    } else {
        *saida = REPROVADO;
    }
    return true;
}
```

### C#

```csharp
static string ClassificarNota(double nota)
{
    if (!double.IsFinite(nota) || nota < 0 || nota > 10)
        throw new ArgumentOutOfRangeException(nameof(nota));

    if (nota >= 7)
        return "aprovado";
    if (nota >= 5)
        return "recuperacao";
    return "reprovado";
}
```

### JavaScript

```javascript
function classificarNota(nota) {
  if (typeof nota !== "number" || !Number.isFinite(nota) || nota < 0 || nota > 10) {
    throw new RangeError("nota deve ser um número finito entre 0 e 10");
  }
  if (nota >= 7) return "aprovado";
  if (nota >= 5) return "recuperacao";
  return "reprovado";
}
```

Não tente aprender as cinco sintaxes simultaneamente. Primeiro explique o
algoritmo em linguagem natural e pseudocódigo. Implemente em Python; quando o
comportamento estiver claro, compare uma linguagem tipada e depois as demais.

## 13. Correção, término e eficiência

Um algoritmo útil precisa responder a três perguntas:

1. **Termina?** Existe progresso mensurável em direção ao fim?
2. **Está correto?** Se receber entrada válida, cumpre a pós-condição?
3. **Cabe nos recursos?** Tempo e memória crescem de forma aceitável?

Para uma busca linear:

```python
def encontrar_indice(valores: list[int], procurado: int) -> int | None:
    for indice, valor in enumerate(valores):
        if valor == procurado:
            return indice
    return None
```

- termina porque a lista possui quantidade finita de itens;
- se retorna um índice, o elemento naquele índice é o procurado;
- se percorre tudo sem encontrar, retorna ausência;
- no pior caso examina `n` itens: **O(n)**;
- usa quantidade constante de memória adicional: **O(1)**.

Notação O descreve crescimento, não segundos exatos. O próximo capítulo de
estruturas de dados aprofundará análise de complexidade; aqui basta reconhecer
uma passagem, laços aninhados e armazenamento proporcional à entrada.

## 14. Estratégias de teste

Não escolha casos aleatoriamente. Derive-os do contrato.

### Partições de equivalência

Separe entradas que deveriam se comportar da mesma forma. Para nota de `0` a
`10`:

- menor que `0`: inválida;
- `0` a menor que `5`: reprovado;
- `5` a menor que `7`: recuperação;
- `7` a `10`: aprovado;
- maior que `10`: inválida.

### Análise de fronteira

Teste ao redor das divisões:

```text
-0.01, 0, 4.99, 5, 6.99, 7, 10, 10.01
```

### Propriedades

Além de exemplos específicos, verifique afirmações gerais:

- a média de uma lista não vazia fica entre mínimo e máximo;
- ordenar não muda a quantidade de elementos;
- adicionar e depois remover o mesmo item de um conjunto restaura o estado;
- o desconto nunca deixa o total final negativo.

Essas propriedades ajudam a encontrar casos que exemplos individuais não
anteciparam.

## 15. Erros comuns e como diagnosticá-los

| Erro | Sintoma | Pergunta de diagnóstico |
|------|---------|-------------------------|
| usar `=` no lugar da comparação apropriada | atribuição ou erro de sintaxe | estou associando ou comparando? |
| condição ampla antes da específica | ramo específico nunca executa | algum ramo anterior já cobre este caso? |
| limite errado | primeiro ou último caso falha | o limite é inclusivo ou exclusivo? |
| `while` sem progresso | programa não termina | qual variável aproxima o laço do fim? |
| acumulador não inicializado | erro ou valor contaminado | qual é o elemento neutro da operação? |
| retorno ausente | chamador recebe ausência | todos os caminhos retornam? |
| mutar argumento sem documentar | dados mudam “sozinhos” | dois nomes apontam para o mesmo objeto? |
| comparar float com igualdade exata | resultado surpreendente | devo usar tolerância ou decimal? |
| capturar erro genérico | falha desaparece | qual exceção consigo realmente recuperar? |
| misturar entrada e regra | teste exige terminal | posso passar dados como argumentos? |

## 16. Exercícios graduais

Implemente primeiro em Python. Depois escolha três exercícios para portar a uma
segunda linguagem.

### Nível 1 — valores e decisões

1. Classifique um número como negativo, zero ou positivo.
2. Retorne o maior entre três números, incluindo empates.
3. Verifique se um ano é bissexto pelas regras completas.
4. Converta uma nota em A, B, C, D ou F e documente todos os limites.
5. Calcule o preço final com desconto sem permitir resultado negativo.

### Nível 2 — repetição

6. Some apenas os pares de `1` a `100`, inclusive.
7. Conte vogais sem diferenciar maiúsculas e minúsculas.
8. Gere a tabuada de `1` a `10` sem duplicar código.
9. Implemente FizzBuzz de `1` a `100` e teste `3`, `5`, `15` e um número comum.
10. Encontre mínimo e máximo sem usar as funções prontas; rejeite lista vazia.

### Nível 3 — funções e coleções

11. Conte frequências de palavras usando dicionário e `casefold`.
12. Remova duplicatas preservando a primeira ocorrência.
13. Implemente uma fila com `adicionar`, `remover` e erro para fila vazia.
14. Verifique se parênteses estão balanceados usando uma pilha.
15. Valide CPF somente quanto ao formato e dígitos verificadores, com valores
    totalmente sintéticos. Não armazene nem solicite documentos reais.

### Nível 4 — raciocínio e qualidade

16. Reescreva `resumir_medicoes` usando O(1) de espaço adicional e mantenha os
    mesmos testes.
17. Para busca linear, escreva pré-condição, pós-condição, argumento de término
    e complexidade.
18. Crie testes de partição e fronteira para `converter_idade`.
19. Demonstre aliasing com uma coleção aninhada e explique cópia rasa versus
    profunda.
20. Compare uma solução com dois laços aninhados e outra baseada em conjunto.
    Meça entradas sintéticas crescentes e explique a tendência, sem concluir
    apenas por uma execução.

## 17. Projeto de consolidação: analisador de pedidos

Construa uma biblioteca pequena que recebe pedidos sintéticos:

```python
pedidos = [
    {"id": "P-001", "subtotal_centavos": 12000, "itens": 3, "status": "pago"},
    {"id": "P-002", "subtotal_centavos": 25000, "itens": 5, "status": "pendente"},
]
```

Implemente funções independentes para:

1. validar campos e domínio;
2. rejeitar IDs duplicados;
3. filtrar por status;
4. calcular subtotal geral;
5. calcular ticket médio;
6. localizar o maior pedido;
7. gerar um resumo sem modificar a entrada.

Critérios de aceite:

- [ ] entrada vazia tem comportamento documentado;
- [ ] subtotal em centavos negativo, itens menores que 1 e status desconhecido
      são rejeitados;
- [ ] IDs duplicados são detectados com conjunto;
- [ ] regra de negócio não chama `input` nem `print`;
- [ ] cada função possui contrato curto;
- [ ] testes cobrem caso comum, vazio, limites e inválidos;
- [ ] um teste demonstra que a coleção original não foi alterada;
- [ ] a complexidade das operações principais está registrada.

Desafio adicional: crie uma CLI separada que converte entrada textual, chama a
biblioteca e apresenta o resumo. Erros de entrada devem produzir mensagem clara
sem expor traceback ao usuário final; os testes da biblioteca não devem
depender dessa interface.

## Critério de conclusão

Considere o capítulo concluído quando conseguir, sem copiar uma solução:

- [ ] prever o valor e o tipo de expressões simples;
- [ ] montar e simplificar uma condição booleana;
- [ ] desenhar uma tabela de decisão antes do `if`;
- [ ] explicar estado inicial, condição e progresso de um `while`;
- [ ] formular uma invariante para um acumulador;
- [ ] diferenciar retorno de impressão e função pura de efeito;
- [ ] escolher uma coleção justificando a operação dominante;
- [ ] explicar referência compartilhada e mutabilidade;
- [ ] derivar testes de partições e fronteiras;
- [ ] justificar término, correção e custo de um algoritmo simples;
- [ ] portar uma decisão e um laço para uma segunda linguagem.

## Conexão com os próximos capítulos

Agora você possui o vocabulário lógico usado em todas as linguagens. Siga para
[Terminal, editor e Git](02-ambiente-terminal-git.md) para aprender a executar,
inspecionar e versionar seus programas. Depois, consolide a tradução entre
linguagens em [Fundamentos comuns](03-fundamentos-comuns.md) e aprofunde custo e
escolha de estruturas em
[Estruturas de dados e algoritmos](04-estruturas-dados-algoritmos.md).
