# Fundamentos comuns às linguagens: do valor ao programa modular

Python, Java, C, C# e JavaScript escrevem a mesma ideia com sintaxes e modelos
de execução diferentes. Aprender apenas a posição das chaves produz código por
imitação. Aprender **estado, fluxo, contrato, representação e efeito** permite
entrar em uma linguagem nova e fazer as perguntas certas.

Neste capítulo, Python é usado para apresentar ideias com pouca cerimônia. As
comparações mostram onde as outras linguagens mudam garantias ou custos. Os
capítulos em [`linguagens/`](linguagens/) ensinam cada ecossistema em detalhe.

Este é um capítulo de **recuperação e comparação**, não a primeira exposição
a todos os termos. Condições, laços, funções e rastreamento foram construídos
passo a passo em [Como estudar](00-como-estudar.md) e
[Lógica e algoritmos](01-logica-algoritmos.md). Se um exemplo daqui parecer um
salto, volte ao conceito correspondente, implemente-o primeiro em Python e só
então retorne para comparar garantias entre linguagens. Classes, protocolos,
injeção de dependência e concorrência aparecem aqui como mapa; os guias de
linguagem e os capítulos 05–07 fornecem a prática aprofundada.

## Objetivos de aprendizagem

Ao concluir, você deverá conseguir:

- acompanhar uma execução linha a linha, anotando estado e próximo fluxo;
- escolher tipos que representem estados válidos e validar dados externos;
- usar condições e laços sem limites ambíguos ou loops infinitos;
- definir funções com contrato, retorno e efeitos explícitos;
- explicar escopo, pilha de chamadas, valor, referência, identidade e mutação;
- distinguir erros de sintaxe, compilação/tipo, execução e lógica;
- modelar objetos com invariantes e preferir composição a herança desnecessária;
- separar domínio puro de entrada/saída e dependências de infraestrutura;
- comparar uma solução equivalente nas cinco linguagens sem buscar uma
  “vencedora universal”.

## 1. O modelo mental mínimo: estado, instrução e fluxo

Um programa executa instruções que observam ou alteram **estado**. O fluxo
determina qual instrução vem a seguir.

```python
preco = 50.0
quantidade = 3
subtotal = preco * quantidade

if subtotal >= 100:
    desconto = subtotal * 0.10
else:
    desconto = 0.0

total = subtotal - desconto
```

Trace antes de executar:

| Passo | Instrução | Estado alterado |
|------:|-----------|-----------------|
| 1 | `preco = 50.0` | `preco` vale `50.0` |
| 2 | `quantidade = 3` | `quantidade` vale `3` |
| 3 | multiplicação | `subtotal` vale `150.0` |
| 4 | teste `150 >= 100` | condição verdadeira |
| 5 | cálculo de 10% | `desconto` vale `15.0` |
| 6 | subtração | `total` vale `135.0` |

Esse exercício simples — uma **tabela de rastreamento** — continua útil em
recursão, concorrência e algoritmos complexos. Se você não consegue prever uma
linha, transforme a dúvida em experimento pequeno.

## 2. Valores, variáveis e tipos

Um **valor** é um dado: `42`, `3.14`, `true`, `"Ana"`. Uma **variável** é um
nome associado a um valor ou localização, conforme a linguagem. Um **tipo**
define quais valores e operações fazem sentido.

Tipos frequentes:

- inteiro: contagens, índices e quantidades discretas;
- ponto flutuante: aproximações científicas, não dinheiro exato;
- booleano: verdadeiro/falso;
- caractere/string: texto codificado;
- enumeração: conjunto fechado de estados nomeados;
- coleção: zero ou mais valores;
- registro/objeto: valores relacionados com nomes;
- opcional/nulo: presença ou ausência quando o domínio permite.

### Tipagem estática, dinâmica e inferência

- **Java, C e C#** verificam muitos tipos antes da execução;
- **Python e JavaScript** associam tipos aos valores durante a execução;
- **inferência** permite que compilador ou analisador descubra um tipo sem ele
  ser escrito em toda declaração;
- “forte” e “fraca” descrevem regras de conversão e coerção; não são escala de
  qualidade.

```python
quantidade = 3          # o valor atual é int
quantidade = "três"     # permitido em runtime; pode violar nosso contrato
```

```java
int quantidade = 3;
// quantidade = "três"; // rejeitado pelo compilador
```

Tipagem estática antecipa classes de falhas; tipagem dinâmica reduz cerimônia e
favorece certas formas de exploração. Ambas ainda exigem validação de entradas,
testes e modelagem correta.

### Representação não é o domínio

Dinheiro ilustra a diferença. `0.1 + 0.2` não é exatamente `0.3` em ponto
flutuante binário na maioria das linguagens. Para centavos, uma opção simples é
usar inteiro:

```python
preco_centavos = 1990
quantidade = 3
total_centavos = preco_centavos * quantidade  # 5970
```

Sistemas financeiros reais podem exigir decimal de precisão definida, regras de
arredondamento e moeda no próprio tipo. O tipo correto nasce do domínio, não de
qual ocupa menos caracteres.

### Overflow, precisão e conversão

Inteiros em C, Java e C# geralmente têm limites fixos. Algumas operações podem
transbordar, encerrar o programa, envolver o valor ou exigir contexto verificado,
conforme linguagem e configuração. JavaScript representa `number` como ponto
flutuante e perde precisão inteira além de certo intervalo; oferece `bigint`
para inteiros grandes. Python expande inteiros conforme a memória disponível.

Conversão explícita torna a intenção verificável:

```python
texto = "42"
try:
    idade = int(texto)
except ValueError:
    idade = None
```

Converter não é validar todo o domínio: `-8` vira inteiro corretamente, mas pode
ser uma idade inválida para a regra da aplicação.

## 3. Operadores, expressões e lógica booleana

Uma expressão produz valor. Precedência existe, mas parênteses comunicam melhor
uma regra:

```python
pode_comprar = idade >= 18 and possui_documento and not conta_bloqueada
```

Tabela para `A and B` e `A or B`:

| A | B | `A and B` | `A or B` |
|---|---|-------------|----------|
| falso | falso | falso | falso |
| falso | verdadeiro | falso | verdadeiro |
| verdadeiro | falso | falso | verdadeiro |
| verdadeiro | verdadeiro | verdadeiro | verdadeiro |

Em curto-circuito, `A and B` não avalia `B` quando `A` já é falso; `A or B` não
avalia `B` quando `A` já é verdadeiro. Isso pode proteger uma operação:

```python
if usuario is not None and usuario.ativo:
    liberar_painel()
```

Não esconda efeitos colaterais importantes no lado direito de `and`/`or`; a
chamada pode não ocorrer.

## 4. Entrada não é confiável até ser validada

Dados de teclado, arquivo, API, banco ou variável de ambiente atravessam uma
fronteira. Um processo robusto separa:

```text
texto externo → parsing → validação → tipo do domínio → regra de negócio
```

Exemplo:

```python
def interpretar_quantidade(texto: str) -> int:
    try:
        quantidade = int(texto)
    except ValueError as erro:
        raise ValueError("quantidade deve ser um inteiro") from erro

    if not 1 <= quantidade <= 100:
        raise ValueError("quantidade deve estar entre 1 e 100")
    return quantidade
```

Há duas decisões distintas: o texto é sintaticamente um inteiro? O inteiro
pertence ao intervalo válido? Depois dessa função, o restante do programa pode
trabalhar com uma garantia mais forte.

## 5. Decisão com `if`, `else if` e `else`

Uma cadeia de condições é avaliada de cima para baixo e executa o primeiro ramo
verdadeiro:

```python
def classificar_nota(nota: float) -> str:
    if not 0 <= nota <= 10:
        raise ValueError("nota fora do intervalo 0..10")
    if nota >= 9:
        return "excelente"
    if nota >= 7:
        return "aprovado"
    if nota >= 5:
        return "recuperação"
    return "reprovado"
```

A ordem é parte do algoritmo. Se `nota >= 5` vier primeiro, uma nota 9 será
classificada incorretamente. Teste fronteiras: `0`, `4.999`, `5`, `7`, `9`,
`10` e valores inválidos.

Comparação equivalente:

```java
if (idade >= 18) {
    System.out.println("maior");
} else {
    System.out.println("menor");
}
```

```c
if (idade >= 18) {
    printf("maior\n");
} else {
    printf("menor\n");
}
```

```csharp
Console.WriteLine(idade >= 18 ? "maior" : "menor");
```

```javascript
console.log(idade >= 18 ? "maior" : "menor");
```

O operador ternário é adequado para escolher um valor curto; não para esconder
várias regras e efeitos numa linha.

## 6. Repetição e invariantes de laço

Um laço precisa responder:

1. qual é o estado inicial?
2. enquanto qual condição ele continua?
3. o que muda a cada iteração?
4. por que ele termina?
5. qual propriedade permanece verdadeira?

```python
def somar_nao_negativos(valores: list[int]) -> int:
    total = 0
    for valor in valores:
        if valor < 0:
            continue
        total += valor
    return total
```

Invariante: antes de cada iteração, `total` é a soma dos valores não negativos
já percorridos. Ao terminar, todos foram percorridos; logo, o resultado cobre a
lista inteira.

Use `for` quando percorre uma coleção ou intervalo conhecido. Use `while` quando
a continuação depende de estado:

```python
tentativas = 0
sucesso = False

while tentativas < 3 and not sucesso:
    sucesso = executar_tarefa_local()
    tentativas += 1
```

O incremento garante limite. Em tarefas externas, repetição real também exige
timeout, intervalo e definição de quais erros são recuperáveis.

Erros clássicos são *off-by-one*. Para índices de uma lista com `n` elementos,
o intervalo válido costuma ser `0..n-1`. Teste vazio, um item e último item.

## 7. Funções como contratos

Uma função bem desenhada possui:

- nome que descreve a intenção;
- entradas com significado e domínio;
- saída definida;
- pré-condições e pós-condições;
- erros previstos;
- efeitos colaterais explícitos.

```python
def calcular_total_centavos(
    preco_centavos: int,
    quantidade: int,
    desconto_percentual: int = 0,
) -> int:
    """Retorna total em centavos, com desconto inteiro de 0 a 100%."""
    if preco_centavos < 0:
        raise ValueError("preço não pode ser negativo")
    if quantidade < 0:
        raise ValueError("quantidade não pode ser negativa")
    if not 0 <= desconto_percentual <= 100:
        raise ValueError("desconto deve estar entre 0 e 100")

    subtotal = preco_centavos * quantidade
    desconto = subtotal * desconto_percentual // 100
    return subtotal - desconto
```

Observe decisões que precisam estar no contrato: desconto usa percentual
inteiro e divisão truncada. Se a regra exigir arredondamento diferente, o teste
e a implementação devem mudar juntos.

### A mesma função em cinco linguagens

Versões reduzidas, assumindo entradas já validadas:

```python
def subtotal(preco: int, quantidade: int) -> int:
    return preco * quantidade
```

```java
static long subtotal(long preco, int quantidade) {
    return preco * quantidade;
}
```

```c
#include <stdint.h>

int64_t subtotal(int64_t preco, int32_t quantidade) {
    return preco * quantidade;
}
```

```csharp
static long Subtotal(long preco, int quantidade) => preco * quantidade;
```

```javascript
function subtotal(preco, quantidade) {
  return preco * quantidade;
}
```

O algoritmo é igual. As diferenças relevantes incluem declaração de tipos,
faixa numérica, convenção de nomes e momento da validação. Em JavaScript, por
exemplo, o contrato deve impedir strings e valores não finitos em runtime.

## 8. Escopo, tempo de vida e pilha de chamadas

**Escopo** responde onde um nome pode ser usado. **Tempo de vida** responde por
quanto tempo seu valor existe. Eles se relacionam, mas não são idênticos.

```python
taxa_padrao = 10

def aplicar(valor: int, taxa: int) -> int:
    desconto = valor * taxa // 100
    return valor - desconto

resultado = aplicar(1000, taxa_padrao)
```

`valor`, `taxa` e `desconto` são locais à chamada. Cada chamada ganha um quadro
na **pilha de chamadas**, com parâmetros, variáveis locais e ponto de retorno.
Quando a função retorna, o quadro é removido. Objetos referenciados podem
continuar vivos se houver outras referências.

Evite estado global mutável: ele cria dependência oculta, dificulta testes e
torna a ordem das chamadas importante. Passe dependências por parâmetros.

## 9. Valor, referência, identidade e mutação

Duas variáveis podem representar valores iguais sem serem o mesmo objeto; ou
podem referenciar o mesmo objeto mutável.

```python
original = [1, 2]
apelido = original
copia = original.copy()

apelido.append(3)

assert original == [1, 2, 3]
assert copia == [1, 2]
assert apelido is original
assert copia is not original
```

- **igualdade** pergunta se os conteúdos são equivalentes;
- **identidade** pergunta se é a mesma instância;
- **mutação** altera uma instância existente;
- **cópia superficial** cria contêiner novo, mas compartilha elementos internos;
- **cópia profunda** tenta copiar a árvore, com custo e semântica próprios.

```python
a = [[1], [2]]
b = a.copy()
b[0].append(9)
assert a == [[1, 9], [2]]
```

Em Java, C# e JavaScript, objetos também são acessados por referências, embora a
linguagem sempre passe argumentos por valor — o valor copiado pode ser uma
referência. C expõe endereços por ponteiros, exigindo ainda mais clareza sobre
propriedade e tempo de vida.

Prefira valores imutáveis quando uma alteração compartilhada não representa o
domínio. Ao aceitar coleção mutável, documente se a função a modifica.

## 10. Strings, Unicode e ausência

Texto não é “um array universal de letras”. Unicode permite que um símbolo
visual tenha mais de um ponto de código, e UTF-8 usa quantidade variável de
bytes. `len`, índice e tamanho em bytes podem significar coisas diferentes entre
linguagens. Não corte texto por bytes sem entender a codificação.

Na fronteira com arquivo ou rede, declare codificação:

```python
with open("dados/nomes.txt", "r", encoding="utf-8") as arquivo:
    nomes = [linha.rstrip("\n") for linha in arquivo]
```

Ausência também precisa de significado. `None`, `null` ou `nullptr` pode querer
dizer “não encontrado”, “ainda não carregado” ou “não se aplica”. Se esses
estados exigem tratamentos diferentes, um único nulo é modelagem insuficiente.

Em JavaScript, `undefined` e `null` são distintos; coerções implícitas tornam
comparações frouxas surpreendentes. Como padrão, use `===`/`!==` e valide tipos.

## 11. Erros: falha esperada, defeito e recuperação

Classifique antes de tratar:

| Categoria | Exemplo | Resposta típica |
|-----------|---------|-----------------|
| sintaxe | parêntese ausente | corrigir fonte |
| tipo/compilação | somar tipos incompatíveis | corrigir contrato ou conversão |
| entrada inválida | quantidade `-2` | rejeitar com mensagem útil |
| falha operacional | arquivo inexistente | tratar, propagar ou tentar alternativa |
| defeito lógico | desconto invertido | teste falha; corrigir algoritmo |
| invariante quebrada | saldo interno impossível | interromper fluxo e investigar |

Não capture toda exceção e continue como se nada tivesse ocorrido. Trate apenas
quando souber produzir um resultado correto, acrescentar contexto ou liberar um
recurso. Caso contrário, propague.

Recursos devem ser liberados mesmo em falha:

- Python: `with`;
- Java: `try-with-resources`;
- C#: `using`;
- JavaScript: `try/finally` e APIs de lifecycle;
- C: funções com propriedade explícita e caminho de cleanup bem delimitado.

Nunca exponha senha, token ou dado pessoal em mensagem de erro e log.

## 12. Funções puras e efeitos nas bordas

Uma função pura depende apenas dos parâmetros e não altera estado externo:

```python
def com_imposto(valor_centavos: int, taxa_percentual: int) -> int:
    return valor_centavos + valor_centavos * taxa_percentual // 100
```

Relógio, aleatoriedade, console, arquivo, rede e banco são efeitos. Isole-os:

```python
def gerar_resumo(valores: list[int]) -> dict[str, int]:
    return {"quantidade": len(valores), "total": sum(valores)}


def executar(caminho: str) -> None:
    with open(caminho, encoding="utf-8") as arquivo:
        valores = [int(linha) for linha in arquivo]
    print(gerar_resumo(valores))
```

Agora `gerar_resumo` é testável sem sistema de arquivos. Isso não significa que
todo programa deve ser funcional; significa que efeitos ficam visíveis e
concentrados nas bordas.

## 13. Objetos, invariantes e composição

Use classe quando dados possuem identidade, ciclo de vida ou regras que devem
permanecer juntas:

```python
class Conta:
    def __init__(self, saldo_centavos: int = 0) -> None:
        if saldo_centavos < 0:
            raise ValueError("saldo inicial inválido")
        self._saldo_centavos = saldo_centavos

    @property
    def saldo_centavos(self) -> int:
        return self._saldo_centavos

    def depositar(self, valor_centavos: int) -> None:
        if valor_centavos <= 0:
            raise ValueError("depósito deve ser positivo")
        self._saldo_centavos += valor_centavos

    def sacar(self, valor_centavos: int) -> None:
        if valor_centavos <= 0:
            raise ValueError("saque deve ser positivo")
        if valor_centavos > self._saldo_centavos:
            raise ValueError("saldo insuficiente")
        self._saldo_centavos -= valor_centavos
```

A invariante é `saldo_centavos >= 0`. O objeto não expõe um setter que permita
quebrá-la. Encapsulamento é proteger regras, não apenas trocar atributos públicos
por métodos vazios.

Prefira composição: um `Pedido` **tem** itens e uma política de desconto.
Herança é adequada quando o subtipo realmente preserva o contrato do tipo base;
hierarquias profundas criam acoplamento e estados difíceis de prever.

## 14. Interfaces, polimorfismo e injeção de dependência

Um serviço de relatório precisa de uma capacidade de salvar, não de conhecer
todos os detalhes de arquivo ou banco:

```python
from typing import Protocol


class Destino(Protocol):
    def salvar(self, conteudo: str) -> None: ...


class GeradorDeRelatorio:
    def __init__(self, destino: Destino) -> None:
        self._destino = destino

    def gerar(self, valores: list[int]) -> None:
        self._destino.salvar(f"total={sum(valores)}")
```

Fornecer `destino` no construtor é **injeção de dependência**. Em produção ele
pode gravar arquivo; no teste, guardar em memória. Java e C# costumam expressar
esse contrato com `interface`; C pode usar uma `struct` com ponteiros de função;
JavaScript frequentemente usa *duck typing* ou contratos por convenção.

Polimorfismo não exige herança: exige que diferentes implementações atendam ao
mesmo contrato observável.

## 15. Módulos, visibilidade e arquitetura em camadas

Um módulo reúne conceitos coesos e expõe uma API pequena. O restante deve ser
detalhe interno. Uma divisão inicial útil:

```text
entrada/          CLI ou HTTP: converte dados externos
dominio/          regras e tipos, idealmente sem infraestrutura
aplicacao/        coordena casos de uso
infraestrutura/   arquivo, banco, rede, relógio
testes/           comportamento observável
```

As dependências devem apontar para dentro: domínio não deveria importar framework
HTTP ou driver de banco. Isso permite trocar mecanismo sem reescrever regra.

Evite dois extremos:

- arquivo único com responsabilidades misturadas;
- dezenas de módulos de uma função sem fronteira conceitual.

Extraia um módulo quando houver nome de domínio claro, API pequena ou motivo de
mudança independente.

## 16. Compilação e execução

Modelo simplificado:

| Linguagem | Caminho comum |
|-----------|---------------|
| C | pré-processamento → compilação → montagem → link → processo nativo |
| Java | fonte → bytecode → JVM interpreta/JIT compila |
| C# | fonte → IL → runtime .NET/JIT |
| Python | fonte → representação/bytecode interno → máquina virtual |
| JavaScript | parse → interpretação/JIT no navegador ou Node.js |

“Interpretada” e “compilada” não são caixas absolutas: implementações combinam
etapas. O que importa no diagnóstico é saber onde a falha ocorreu:

- parser: sintaxe inválida;
- compilador/analisador: contrato de tipo quebrado;
- linker/loader: símbolo ou biblioteca indisponível;
- runtime: entrada/caminho específico falhou;
- regra: executou sem erro técnico, mas produziu resposta errada.

## 17. Concorrência e assincronicidade: distinção inicial

Esses conceitos serão aprofundados depois, mas não os confunda:

- **concorrência:** várias tarefas fazem progresso em períodos sobrepostos;
- **paralelismo:** trabalho realmente executado ao mesmo tempo;
- **assíncrono:** uma operação pode suspender e permitir outro trabalho enquanto
  aguarda, sem exigir uma thread por tarefa.

Estado mutável compartilhado exige sincronização. Uma função pura evita essa
classe de disputa. Não adicione threads ou `async` para “deixar rápido” sem
medir onde o tempo é gasto e sem compreender cancelamento, erros e limites.

## 18. Estudo de caso: total de um pedido

### Requisitos

- cada item tem produto, quantidade e preço em centavos;
- quantidade precisa estar entre 1 e 100;
- preço deve ser não negativo;
- cupons aceitos são `SEM_CUPOM` e `PROMO10`;
- a função retorna dados; a camada de entrada imprime;
- o resultado não depende de relógio ou rede.

### Decomposição

```text
entrada textual
  └─ interpretar e validar itens
       └─ calcular subtotal puro
            └─ aplicar política de desconto
                 └─ devolver ResultadoPedido
                      └─ formatar na borda
```

### Implementação de referência em Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    produto: str
    quantidade: int
    preco_centavos: int

    def __post_init__(self) -> None:
        if not self.produto.strip():
            raise ValueError("produto é obrigatório")
        if not 1 <= self.quantidade <= 100:
            raise ValueError("quantidade deve estar entre 1 e 100")
        if self.preco_centavos < 0:
            raise ValueError("preço não pode ser negativo")


def totalizar(itens: list[Item], cupom: str = "SEM_CUPOM") -> int:
    subtotal = sum(i.quantidade * i.preco_centavos for i in itens)

    if cupom == "SEM_CUPOM":
        return subtotal
    if cupom == "PROMO10":
        return subtotal - subtotal * 10 // 100
    raise ValueError("cupom desconhecido")
```

### Casos que revelam o contrato

| Caso | Resultado esperado |
|------|--------------------|
| lista vazia | `0` ou erro? decida e documente; acima retorna `0` |
| item de valor zero | permitido |
| quantidade zero | rejeitada |
| `PROMO10` em 999 centavos | `900` pela divisão inteira usada |
| cupom desconhecido | erro explícito |
| alterar item após criar | impedido por `frozen=True` no uso comum |

Reimplemente em uma linguagem tipada. Compare como ela representa `Item`,
imutabilidade, enumeração de cupom, coleção e erro.

## 19. Erros comuns e correções de raciocínio

- **Condição sempre verdadeira:** escreva tabela verdade e teste ambos os lados.
- **Limite errado:** teste vazio, primeiro, último e imediatamente fora.
- **Converter e assumir válido:** parsing e regra de domínio são etapas distintas.
- **Comparar ponto flutuante por igualdade exata:** use representação adequada e
  tolerância quando o domínio for aproximado.
- **Modificar coleção durante iteração:** pode saltar itens ou invalidar iterador;
  produza nova coleção ou use operação específica.
- **Parâmetro mutável como padrão:** pode ser compartilhado entre chamadas em
  Python; use `None` e crie internamente.
- **Capturar erro genérico e ignorar:** o programa perde a causa e pode continuar
  em estado incorreto.
- **Classe sem invariante:** dados simples podem pedir registro, não objeto cheio
  de getters e setters.
- **Estado global:** testes influenciam uns aos outros e chamadas dependem da
  ordem.
- **Abstrair cedo demais:** primeiro observe repetição conceitual e contratos.

## 20. Exercícios graduais

### Nível 1 — rastrear e explicar

1. Faça a tabela de estado do exemplo de desconto para subtotais `99`, `100` e
   `101`.
2. Escreva a tabela verdade de `(ativo and autorizado) or administrador`.
3. Encontre os limites válidos de uma lista de cinco itens.
4. Explique igualdade versus identidade com dois objetos.
5. Classifique cinco falhas como sintaxe, tipo, runtime ou lógica.

### Nível 2 — implementar

1. Implemente `interpretar_idade` separando parsing de intervalo `0..130`.
2. Crie `media` com contrato explícito para coleção vazia e testes de fronteira.
3. Modele um `Carrinho` que nunca aceita quantidade negativa.
4. Separe leitura de CSV, cálculo puro e impressão em três funções.
5. Implemente o total de pedido em Python e em Java, C, C# ou JavaScript.

### Nível 3 — projetar

1. Crie duas políticas de desconto intercambiáveis sem condicional gigante.
2. Injete um relógio em um serviço que registra data, permitindo teste
   determinístico.
3. Modele os estados de um pedido (`rascunho`, `pago`, `cancelado`) de forma que
   transições inválidas sejam rejeitadas.
4. Compare versão mutável e imutável do mesmo modelo: clareza, cópias e risco.
5. Desenhe dependências de entrada, aplicação, domínio e infraestrutura; elimine
   uma dependência do domínio para fora.

## Critério de conclusão do capítulo

- [ ] Consigo rastrear estado e fluxo de um programa sem executá-lo.
- [ ] Sei justificar tipos e representação, inclusive para dinheiro e ausência.
- [ ] Testo condições e laços nas fronteiras.
- [ ] Escrevo funções com pré-condições, retorno, erros e efeitos claros.
- [ ] Explico escopo, pilha, identidade, referência, mutação e cópia superficial.
- [ ] Distingo falha esperada de defeito lógico e não escondo exceções.
- [ ] Modelo uma classe que protege pelo menos uma invariante real.
- [ ] Separo regra pura de console, arquivo, relógio ou rede.
- [ ] Implemento a mesma regra em duas linguagens e comparo trade-offs técnicos.
- [ ] Consigo explicar cada decisão do estudo de caso e seus testes de fronteira.

## Conexão com os próximos capítulos

Agora você possui o vocabulário comum para estudar
[Python, Java, C, C# e JavaScript](linguagens/). Em
[Estruturas de dados e algoritmos](04-estruturas-dados-algoritmos.md), a pergunta
deixa de ser apenas “o resultado está correto?” e passa a incluir “como tempo e
memória crescem?”. Em [Engenharia de software](05-engenharia-software.md), os
contratos, módulos, testes e dependências formam uma base de código sustentável.
