# 00 — Como pensar problemas antes de programar

Programar começa antes do editor. Um programa pode compilar, passar pelos testes
escritos e ainda resolver a pergunta errada. Engenharia de software começa ao
transformar uma necessidade ambígua em um **contrato observável**, decompor esse
contrato em responsabilidades menores e reunir evidências de que a solução o
cumpre.

Este capítulo usa como exemplo contínuo o [Dependency Planner](projetos/dependency-planner/README.md),
uma aplicação que organiza tarefas respeitando dependências. O domínio é pequeno
o bastante para ser entendido por inteiro, mas contém ambiguidades, erros,
invariantes e escolhas iguais às encontradas em sistemas profissionais.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. converter uma frase informal em entradas, saídas, regras e exemplos testáveis;
2. separar requisito funcional, atributo de qualidade e restrição;
3. escrever pré-condições, pós-condições e invariantes sem depender da linguagem;
4. decompor a solução atribuindo uma responsabilidade e um tipo de falha a cada parte;
5. argumentar por que um algoritmo termina e preserva o contrato;
6. escolher casos normais, limites e inválidos que realmente discriminem soluções;
7. diagnosticar uma solução que parece correta, mas modelou o problema incorretamente.

## Pré-requisitos e mapa mental

Você precisa reconhecer funções, condicionais, laços, coleções e exceções. O
capítulo não exige conhecer grafos; quando necessário, uma dependência será apenas
uma relação entre duas tarefas.

```text
necessidade
  -> linguagem do domínio
  -> exemplos e contraexemplos
  -> contrato (entrada, saída, regras, erros)
  -> modelo de estado e invariantes
  -> decomposição em responsabilidades
  -> algoritmo e argumento de correção
  -> testes, medição e revisão do contrato
```

Esse fluxo não é estritamente linear. Descobrir que uma regra é cara ou impossível
de verificar pode exigir voltar ao requisito e negociar outra semântica.

## Da frase vaga ao vocabulário do domínio

Considere o pedido: “organize as tarefas de um projeto”. Antes de escolher uma
estrutura de dados, pergunte o que cada palavra significa:

- **tarefa:** unidade identificada por nome, número ou ambos?
- **organizar:** ordenar alfabeticamente, minimizar duração ou respeitar precedência?
- **dependência:** a tarefa anterior precisa começar ou terminar primeiro?
- **projeto:** pode estar vazio? pode ter milhares de tarefas?
- **resultado:** uma ordem, lotes paralelos, datas ou apenas validação?

Crie um glossário curto e use um termo para cada conceito. Neste curso:

> Uma tarefa possui um identificador único, título, duração inteira positiva e
> zero ou mais dependências. Uma dependência de `B` em `A` significa que `A`
> precisa terminar antes de `B` começar.

Essa frase elimina interpretações, mas ainda não diz tudo. Bons requisitos
combinam prosa precisa com exemplos observáveis:

```gherkin
Cenário: duas tarefas podem executar em paralelo
  Dado que "modelo" não depende de outra tarefa
  E que "documentacao" não depende de outra tarefa
  Quando o plano é calculado
  Então ambas pertencem ao primeiro lote

Cenário: uma referência desconhecida é rejeitada
  Dado que "api" depende de "banco"
  E que não existe tarefa identificada por "banco"
  Quando o projeto é carregado
  Então o resultado informa a dependência desconhecida
  E nenhum plano parcial é publicado
```

O segundo cenário define também **atomicidade observável**: falhar não deve
parecer um sucesso parcial.

## Três tipos de requisito

Misturar naturezas diferentes torna a especificação difícil de validar.

| Tipo | Pergunta | Exemplo no planejador | Evidência |
|---|---|---|---|
| funcional | o que o sistema faz? | calcula uma ordem válida | teste com uma cadeia conhecida |
| atributo de qualidade | quão bem deve fazer? | resposta determinística | repetir a entrada e comparar bytes |
| restrição | o que limita a solução? | entrada em JSON UTF-8 | teste de contrato do adaptador |

“Rápido”, “seguro” e “fácil” não são verificáveis sozinhos. Uma versão
melhor seria: “para até 100 mil tarefas e 500 mil dependências, o processo deve
usar no máximo 1 GiB e concluir em até 2 s no ambiente de referência”. Os números
podem mudar; o importante é existir uma condição que possa falhar.

Também registre o que **não** faz parte da primeira versão. Por exemplo:
calendário, feriados, pessoas e recursos compartilhados estão fora do escopo.
Sem esse limite, “calcular um plano” pode virar um problema de escalonamento muito
mais complexo que ordenar precedências.

## O contrato pelo modelo IPO

Organize a fronteira da operação em entrada, processamento e saída:

| Parte | Contrato do planejador |
|---|---|
| entrada | objeto com uma lista `items`; cada item tem campos e tipos definidos |
| processamento | valida unicidade, referências, duração e ausência de ciclo |
| saída válida | ordem, lotes paralelos e duração do caminho crítico |
| saída inválida | erro estruturado; a CLI escreve em `stderr` e retorna código não zero |

Especifique o **domínio da entrada**, não apenas um exemplo feliz:

- `id` e `title` são strings não vazias;
- `duration` é inteiro positivo, e booleano não conta como inteiro;
- `dependencies` é uma lista de identificadores sem repetição;
- campos desconhecidos são rejeitados;
- a lista vazia é válida e produz plano vazio;
- tamanho máximo precisa ser imposto na borda se a entrada não for confiável.

Decisões como normalizar espaços, distinguir maiúsculas ou aceitar Unicode não
devem ficar escondidas em um `strip()` ou `lower()`. Normalização altera a noção
de identidade e precisa estar no contrato.

## Pré-condição, pós-condição e efeito colateral

- **Pré-condição:** verdade exigida antes da operação.
- **Pós-condição:** verdade garantida quando ela termina com sucesso.
- **Invariante:** verdade preservada durante toda transição válida.
- **Efeito colateral:** mudança observável além do valor retornado.

```python
def total_duration(durations: list[int]) -> int:
    """Return the sum without changing ``durations``.

    Pre: every element is an int greater than zero; bool is rejected.
    Post: result is non-negative and equals the mathematical sum.
    """
    if any(isinstance(value, bool) or not isinstance(value, int) or value <= 0
           for value in durations):
        raise ValueError("durations must contain only positive integers")
    return sum(durations)
```

O tipo `list[int]` ajuda ferramentas, mas não protege a função em tempo de
execução. O contrato explica por que existe validação. A lista vazia retorna
zero: a pós-condição correta é “não negativo”, não “positivo”.

Funções puras, como essa, facilitam testes. Sistemas também leem arquivos,
consultam relógios e gravam bancos. Isole esses efeitos nas bordas e injete os
valores de que o núcleo precisa. Assim um erro de leitura não se confunde com uma
regra de negócio.

## Invariantes como ferramenta de raciocínio

No planejador, antes do algoritmo principal:

1. cada identificador representa exatamente uma tarefa;
2. toda dependência aponta para uma tarefa existente;
3. uma tarefa não depende diretamente de si mesma;
4. cada relação lógica aparece uma vez;
5. a estrutura de vizinhança e as contagens de dependências descrevem o mesmo grafo.

Durante a construção da ordem:

1. toda tarefa emitida possui zero dependências ainda não emitidas;
2. cada tarefa entra e sai da fila no máximo uma vez;
3. uma aresta é retirada logicamente exatamente uma vez;
4. nenhuma contagem se torna negativa;
5. o prefixo já emitido é uma ordem válida para seus elementos.

Uma invariante permite localizar defeitos. Se uma contagem fica negativa, o erro
não está na escolha da próxima tarefa: uma aresta duplicada entrou, foi processada
duas vezes ou as duas representações divergiram.

## Decompor por responsabilidade e falha

“Processar projeto” é amplo demais. Prefira um fluxo em que cada etapa tenha uma
razão diferente para mudar:

```text
ler bytes do arquivo
  -> decodificar JSON
  -> validar forma e tipos
  -> criar objetos do domínio
  -> validar referências globais
  -> construir relações
  -> calcular ordem, lotes e caminho crítico
  -> serializar resultado
  -> apresentar ao processo chamador
```

Associe falhas à etapa que pode explicá-las:

| Etapa | Falha | Tratamento apropriado |
|---|---|---|
| abrir arquivo | permissão ou caminho ausente | erro de infraestrutura com contexto |
| decodificar | JSON truncado | erro de formato com local aproximado |
| criar tarefa | duração negativa | erro de validação do campo |
| validar projeto | ID referenciado não existe | erro de domínio com IDs envolvidos |
| ordenar | ciclo | erro de domínio; não produzir ordem parcial como sucesso |
| escrever saída | pipe fechado | erro de I/O, não de planejamento |

Camadas não significam criar uma classe para cada seta. Significam impedir que
uma função misture parsing, regra, algoritmo e apresentação de tal maneira que
nenhum deles possa ser entendido isoladamente.

## Do exemplo manual ao algoritmo

Resolva primeiro uma instância pequena:

```text
modelo (sem dependências, duração 3)
api (depende de modelo, duração 5)
web (depende de modelo, duração 4)
entrega (depende de api e web, duração 1)
```

No início apenas `modelo` está disponível. Depois dele, `api` e `web` ficam
disponíveis. `entrega` só fica disponível depois das duas. Esse procedimento
manual revela o estado mínimo: a quantidade de dependências pendentes por tarefa
e a lista de tarefas liberadas por cada conclusão.

```text
para cada tarefa t:
    pendentes[t] = quantidade de dependências distintas de t
    para cada dependência d de t:
        dependentes[d].adicione(t)

disponiveis = todas as tarefas com pendentes igual a zero
enquanto disponiveis não estiver vazio:
    t = retire uma tarefa disponível
    emita t
    para cada sucessora s em dependentes[t]:
        pendentes[s] -= 1
        se pendentes[s] == 0:
            adicione s a disponiveis

se quantidade emitida for menor que quantidade de tarefas:
    rejeite: existe pelo menos um ciclo
```

O pseudocódigo deliberadamente deixa uma decisão aberta: qual tarefa retirar
quando há várias disponíveis? Fila preserva uma ordem de descoberta; heap escolhe
a menor chave; conjunto pode variar entre execuções. Se reprodutibilidade é
requisito, a coleção passa a fazer parte da semântica, não apenas do desempenho.

## Argumentar correção e terminação

Um teste encontra exemplos de defeito; não prova todos os casos. Um argumento
curto melhora o projeto:

- **Inicialização:** antes da primeira iteração, `pendentes[t]` equivale ao número
  de predecessoras não emitidas; portanto somente tarefas válidas estão na fila.
- **Preservação:** ao emitir `t`, cada aresta de `t` para uma sucessora é
  processada uma vez. Uma sucessora entra na fila apenas quando a última
  predecessora foi emitida; o prefixo continua válido.
- **Terminação:** cada iteração remove uma tarefa que nunca volta. Existem
  finitas tarefas, logo o laço termina.
- **Conclusão:** se todas foram emitidas, toda aresta aponta de uma posição
  anterior para uma posterior. Se algumas restaram sem a fila ter itens, elas
  dependem circularmente entre si ou de uma região circular.

Esse argumento depende das invariantes de entrada. Com dependência inexistente
ou duplicada, a contagem pode não representar as arestas e a conclusão deixa de
ser válida.

## Casos que revelam decisões escondidas

Não crie dezenas de variações do mesmo caso feliz. Particione o domínio:

| Classe | Exemplo | O que discrimina |
|---|---|---|
| mínimo válido | projeto vazio | identidade e ausência de acesso indevido |
| unidade | uma tarefa isolada | inicialização e finalização |
| cadeia | `A -> B -> C` | precedência transitiva |
| leque | `A -> {B,C,D}` | paralelismo e desempate |
| junção | `{A,B} -> C` | contagem de mais de uma dependência |
| componente isolado | cadeia mais tarefa solta | cobertura de todo o projeto |
| autorreferência | `A -> A` | ciclo de tamanho um |
| ciclo indireto | `A -> B -> C -> A` | detecção global |
| referência ausente | `B` depende de `X` | fronteira do modelo |
| estresse | cadeia e leque enormes | profundidade, memória e crescimento |

Use também testes metamórficos: renomear todos os IDs de forma bijetiva não
deve mudar a estrutura do plano; permutar a ordem do JSON não deve mudar uma
saída declarada determinística; adicionar tarefa isolada não deve invalidar as
relações existentes.

## Trade-offs antes da implementação

| Decisão | Alternativa A | Alternativa B | Pergunta decisiva |
|---|---|---|---|
| entrada inválida | falhar cedo | acumular todos os erros | consumidor corrige interativamente ou em lote? |
| IDs | preservar exatamente | normalizar | identidade é técnica ou digitada por humanos? |
| desempate | mais simples | determinístico | saída será comparada, cacheada ou auditada? |
| efeitos | núcleo puro | acesso direto a I/O | precisa testar regras sem ambiente? |
| ciclo | indicar existência | devolver caminho do ciclo | diagnóstico justifica custo e complexidade? |
| grandes entradas | carregar tudo | processar em fluxo | o algoritmo requer visão global? |

Uma boa decisão não é universalmente correta; ela é rastreável ao requisito e
pode ser revista quando a hipótese mudar.

## Falhas comuns e como diagnosticá-las

### Codificar a primeira interpretação

**Sintoma:** discussão tardia sobre o significado da saída.  
**Diagnóstico:** peça a duas pessoas que produzam manualmente o resultado para o
mesmo exemplo. Se divergem, o contrato não decidiu algo importante.

### Validar somente a sintaxe

JSON bem formado pode conter IDs repetidos ou dependências inexistentes. Separe
validade sintática, estrutural e semântica e teste uma falha de cada camada.

### Função “faz tudo”

**Sintoma:** um teste do algoritmo precisa criar arquivos e capturar terminal.  
**Diagnóstico:** marque em cores diferentes I/O, transformação, regra e
apresentação. Se estão intercalados, extraia limites guiados pelo fluxo de dados.

### Exceção genérica ou retorno ambíguo

`None` pode significar projeto vazio, ciclo ou falha de leitura. Defina resultados
distintos e traduza-os somente na borda. Preserve contexto sem expor rastros
internos ao usuário final.

### Otimizar sem perfil ou sem escala declarada

Uma estrutura sofisticada amplia a superfície de erro. Primeiro estabeleça
correção; depois declare o volume, analise crescimento e meça o gargalo real.

### Confundir exemplo com especificação

Três exemplos nunca descrevem todo o domínio. Combine exemplos, regras gerais,
limites numéricos, erros e propriedades que valem para qualquer resultado.

## Aplicação no Dependency Planner

Abra o [contrato do projeto](projetos/dependency-planner/README.md) e produza uma
tabela de rastreabilidade:

| Requisito | Parte responsável | Evidência esperada |
|---|---|---|
| rejeitar duração não positiva | modelo/adaptador | teste unitário de fronteira |
| rejeitar referência desconhecida | validação do grafo | teste com ID ausente |
| respeitar toda dependência | algoritmo | propriedade para cada aresta |
| produzir ordem repetível | política da fila | teste com entradas permutadas |
| erro não contamina `stdout` | CLI | teste de integração e código de saída |

Não altere o projeto ainda. Primeiro escreva uma especificação para uma nova
opção `--target ID`, que deve planejar apenas a tarefa-alvo e suas dependências.
Decida o comportamento para alvo inexistente, componentes irrelevantes com ciclo,
ordem de desempate e projeto vazio. Essa atividade demonstra como uma pequena
opção altera o universo que precisa ser validado.

## Exercícios por nível

### Nível 1 — compreender

1. Reescreva “o sistema deve ser rápido e fácil” como dois requisitos mensuráveis.
2. Classifique dez regras do planejador em pré-condição, pós-condição,
   invariante ou atributo de qualidade.
3. Modele entrada, saída e erros de uma função que valida parênteses.

**Aceite:** cada requisito possui condição de teste; nenhuma definição usa
“correto” para explicar “correção”.

### Nível 2 — aplicar

1. Especifique um encurtador de URLs com pelo menos cinco exemplos, cinco limites
   e cinco entradas inválidas.
2. Escreva o pseudocódigo da opção `--target` e marque as invariantes do laço.
3. Desenhe as responsabilidades de uma rotina que lê CSV e grava um relatório;
   identifique todos os efeitos colaterais.

**Aceite:** outra pessoa consegue criar testes compatíveis sem perguntar regras
essenciais; cada falha possui uma categoria e uma fronteira responsável.

### Nível 3 — analisar e defender

1. Crie duas especificações incompatíveis, mas plausíveis, para “remover tarefa”:
   rejeitar se houver dependentes ou remover as relações em cascata.
2. Escolha uma, registre hipóteses e construa uma matriz de decisão.
3. Escreva um argumento de correção e terminação para a solução escolhida.
4. Proponha um teste metamórfico e um teste de estresse.

**Aceite:** a decisão é sustentada por requisitos, o argumento cita invariantes e
o teste falharia em pelo menos uma implementação plausível, porém errada.

## Checklist de domínio

Antes de seguir, verifique se você consegue, sem consultar o texto:

- [ ] distinguir necessidade, requisito funcional, atributo e restrição;
- [ ] definir o domínio de entrada, inclusive vazios, limites e inválidos;
- [ ] escrever pré-condição, pós-condição e invariante de uma função;
- [ ] decompor um fluxo por responsabilidade e tipo de falha;
- [ ] explicar por que o laço central do planejador preserva uma ordem válida;
- [ ] justificar determinismo como requisito ou descartá-lo conscientemente;
- [ ] criar casos que cubram classes distintas, não apenas variações felizes;
- [ ] separar correção funcional de desempenho e de experiência operacional.

Se algum item ainda depende de memorizar uma frase, aplique o método a outro
domínio pequeno. A habilidade central não é reproduzir o planejador; é tornar
explícito o raciocínio que permite construir e revisar qualquer solução.
