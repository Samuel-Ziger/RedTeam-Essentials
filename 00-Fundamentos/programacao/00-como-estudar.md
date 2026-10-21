# Como estudar programação e resolver problemas

Programar não começa pela sintaxe. Começa pela capacidade de descrever, sem
ambiguidades, uma transformação:

```text
entrada válida → regras → saída observável
```

Uma linguagem de programação é a notação usada para tornar essa descrição
executável. Memorizar comandos ajuda pouco se você ainda não consegue explicar
qual problema está resolvendo, quais dados entram, quais regras são aplicadas e
como reconhecer uma resposta correta.

Este capítulo ensina um método de trabalho que será reutilizado em todo o
curso. Os exemplos usam principalmente pseudocódigo e Python, mas o raciocínio
vale para Java, C, C# e JavaScript.

## Antes dos conceitos: faça seu primeiro programa rodar

Se você nunca programou, conclua este pequeno percurso antes de estudar
contratos, invariantes ou decomposição. A meta ainda não é memorizar Python:
é criar um arquivo, executá-lo e relacionar cada linha a um efeito visível.

### Crie e salve o arquivo

1. Abra um editor de texto ou de código.
2. Crie um arquivo chamado `primeiro_programa.py`. Confirme que o nome não
   terminou em `.py.txt`.
3. Digite o código abaixo. Mantenha os quatro espaços antes dos `print` que
   pertencem ao `if` e ao `else`.
4. Salve o arquivo.

```python
nome = "Lia"
pontos = 7

print("Olá,", nome)

if pontos >= 5:
    print("Meta alcançada")
else:
    print("Continue praticando")


def dobro(numero):
    return numero * 2


resultado = dobro(pontos)
print("Dobro:", resultado)

assert resultado == 14
```

### Execute no terminal

O terminal sempre possui uma **pasta atual**. Um comando que recebe apenas o
nome do arquivo procura nessa pasta; por isso, confirme onde você está antes de
executar. No Linux ou macOS:

```bash
pwd                         # mostra a pasta atual
ls                          # lista seus arquivos
cd /caminho/da/sua/pasta    # troque pelo caminho real em que salvou o arquivo
ls primeiro_programa.py     # confirme que o arquivo está aqui
```

No PowerShell do Windows, os equivalentes são:

```powershell
Get-Location
Get-ChildItem
Set-Location "C:\caminho\da\sua\pasta"
Get-ChildItem primeiro_programa.py
```

O texto antes do cursor é o *prompt*; você digita somente o comando. Caminhos
com espaços precisam de aspas. Não copie literalmente os caminhos ilustrativos:
use a pasta que o editor mostrou ao salvar o arquivo. Agora execute **um** dos
comandos:

```bash
# Linux ou macOS
python3 primeiro_programa.py

# Windows, quando o Python Launcher está instalado
py primeiro_programa.py
```

Em algumas instalações, o comando é `python primeiro_programa.py`. Você não
digita o comentário iniciado por `#`. Se o terminal disser que o comando ou o
arquivo não foi encontrado, anote a mensagem exata e consulte
[Terminal, editor e Git](02-ambiente-terminal-git.md). Execute novamente o
comando de localização e a listagem: se o arquivo não aparece, corrija a pasta;
se aparece, confirme qual comando do Python existe. Assim você separa problema
de navegação, runtime ausente e erro do programa.

A saída esperada é:

```text
Olá, Lia
Meta alcançada
Dobro: 14
```

O `assert` correto não imprime nada. O processo simplesmente termina sem erro.

### Leia o programa linha por linha

| Linha ou trecho | O que acontece |
|-----------------|----------------|
| `nome = "Lia"` | cria o nome `nome` e associa a ele o texto `"Lia"` |
| `pontos = 7` | cria outra variável e associa a ela o número inteiro `7` |
| `print("Olá,", nome)` | chama `print` para mostrar um texto e o valor atual de `nome` |
| `if pontos >= 5:` | compara `pontos` com `5`; os dois-pontos anunciam um bloco |
| primeiro `print` recuado | executa somente quando a comparação é verdadeira |
| `else:` | escolhe o caminho alternativo quando a comparação é falsa |
| segundo `print` recuado | executa somente no caminho do `else` |
| `def dobro(numero):` | define uma função chamada `dobro`; `numero` receberá um valor em cada chamada |
| `return numero * 2` | calcula o dobro e devolve o resultado a quem chamou a função |
| `resultado = dobro(pontos)` | chama a função com `7` e guarda o valor devolvido, `14` |
| `print("Dobro:", resultado)` | torna o resultado observável no terminal |
| `assert resultado == 14` | verifica uma expectativa; se for falsa, interrompe com `AssertionError` |

Linhas vazias apenas separam ideias para facilitar a leitura. Já a indentação
tem significado em Python: ela informa quais linhas pertencem a um `if`,
`else` ou função.

Agora faça dois experimentos pequenos:

1. troque `pontos = 7` por `pontos = 3`, preveja a saída e execute;
2. mantenha `pontos = 3` e execute antes de corrigir o `assert`: observe a
   falha; depois mude a expectativa para `assert resultado == 6`.

Assim você praticou variável, saída, decisão, função e um teste mínimo. Neste
curso, `assert` será usado para verificar código; validação de dados recebidos
de uma pessoa ou de uma API exige tratamento explícito, estudado adiante.

Nos exemplos posteriores aparecerão anotações como `subtotal: float`,
`-> float` e `list[int]`. Elas são **dicas de tipo** (*type hints*). Na primeira
leitura, você pode ignorá-las e ler
`def calcular_frete(subtotal: float) -> float` como
`def calcular_frete(subtotal)`. Elas ajudam pessoas e ferramentas, mas, por si
só, não fazem Python rejeitar em tempo de execução todo valor de outro tipo.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- transformar um pedido informal em requisitos verificáveis;
- identificar entradas, saídas, estados, erros e limites;
- decompor um problema em funções pequenas;
- escrever pseudocódigo antes de decidir detalhes de sintaxe;
- formular invariantes e casos de teste;
- rastrear manualmente a execução de um algoritmo;
- depurar por evidências, sem alterar linhas ao acaso;
- estudar de forma ativa e medir o que realmente aprendeu.

## 1. O modelo mental: programa como contrato

Todo programa estabelece um contrato entre quem fornece dados e quem recebe o
resultado. Esse contrato responde a seis perguntas:

1. **Qual problema será resolvido?**
2. **Quais entradas são aceitas?**
3. **Quais saídas são produzidas?**
4. **Quais regras ligam entrada e saída?**
5. **O que acontece com uma entrada inválida?**
6. **Quais propriedades devem ser sempre verdadeiras?**

Considere o pedido informal:

> Calcule o preço de uma entrega e dê frete grátis para pedidos grandes.

Esse texto ainda não é implementável. “Grande” pode significar preço, peso ou
volume. Também não informa moeda, limites ou como tratar valores inválidos. Uma
versão verificável seria:

| Item | Definição |
|------|-----------|
| Entrada | `subtotal`, em reais, e `distancia_km`, em quilômetros |
| Domínio | `subtotal >= 0` e `0 < distancia_km <= 500` |
| Regra base | frete de R$ 8,00 mais R$ 0,75 por quilômetro |
| Benefício | subtotal a partir de R$ 200,00 recebe frete grátis |
| Saída | valor do frete arredondado para duas casas |
| Erro | rejeitar valores fora do domínio |

Agora existe um contrato. Antes de codificar, verifique exemplos:

| Subtotal | Distância | Resultado esperado | Motivo |
|----------|-----------|--------------------|--------|
| `50.00` | `10` | `15.50` | `8 + 10 × 0,75` |
| `199.99` | `1` | `8.75` | abaixo do limite gratuito |
| `200.00` | `500` | `0.00` | exatamente no limite gratuito |
| `-1.00` | `10` | erro | subtotal inválido |
| `50.00` | `0` | erro | distância inválida |

Os casos `199.99` e `200.00` são importantes porque exercitam a fronteira da
regra. Muitos defeitos aparecem exatamente em limites inclusivos e exclusivos.

### Pré-condição, pós-condição e invariante

Esses três termos ajudam a escrever contratos precisos:

- **pré-condição:** precisa ser verdadeira antes da operação;
- **pós-condição:** precisa ser verdadeira depois da operação;
- **invariante:** continua verdadeira durante toda a vida do dado ou processo.

Para o cálculo de frete:

```text
pré: subtotal >= 0 e 0 < distancia_km <= 500
pós: frete >= 0 e possui no máximo duas casas decimais
invariante: nenhum preço monetário armazenado é negativo
```

Uma pré-condição não documentada vira surpresa. Uma pós-condição não testada
vira promessa. Uma invariante não protegida pode ser quebrada por qualquer
função que altere o estado.

## 2. Do pedido ao algoritmo, passo a passo

Use esta sequência antes de abrir o editor:

### Passo 1 — reescreva o objetivo em uma frase

Use um verbo observável:

```text
Calcular o valor do frete a partir do subtotal e da distância.
```

“Criar um sistema moderno de entregas” não é um objetivo verificável. “Receber
dois valores e devolver o frete” é.

### Passo 2 — liste exemplos antes das regras internas

Exemplos revelam ambiguidades rapidamente. Inclua:

- um caso comum;
- o menor valor válido;
- o maior valor válido;
- valores imediatamente antes e depois de cada limite;
- entrada vazia, tipo errado e valor fora do domínio.

Essa técnica é chamada de **exemplificação**. Ela aproxima requisitos e testes:
se não é possível dizer qual saída um exemplo deve produzir, o requisito ainda
não está claro.

### Passo 3 — escreva pseudocódigo

```text
função calcular_frete(subtotal, distancia_km)
    se subtotal não é finito ou subtotal < 0
        sinalizar "subtotal inválido"
    se distancia_km não é finita ou distancia_km <= 0 ou distancia_km > 500
        sinalizar "distância inválida"
    se subtotal >= 200
        retornar 0
    retornar arredondar(8 + distancia_km * 0,75, 2)
```

O pseudocódigo não precisa compilar. Ele separa decisões do problema de
detalhes como chaves, ponto e vírgula ou tipos da linguagem.

### Passo 4 — traduza uma regra por vez

```python
import math


def calcular_frete(subtotal: float, distancia_km: float) -> float:
    """Calcula frete para dados já convertidos em números."""
    if not math.isfinite(subtotal) or subtotal < 0:
        raise ValueError("subtotal deve ser finito e não negativo")
    if not math.isfinite(distancia_km) or not 0 < distancia_km <= 500:
        raise ValueError("distância deve estar entre 0 (exclusivo) e 500 km")
    if subtotal >= 200:
        return 0.0
    return round(8.0 + distancia_km * 0.75, 2)
```

O uso de `float` mantém este primeiro exemplo curto, mas não define uma
arquitetura financeira. Em uma aplicação real, represente valores monetários em
centavos inteiros ou com um tipo decimal e uma regra explícita de arredondamento.
O capítulo de fundamentos retoma essa decisão de representação.

Observe a separação entre **converter texto** e **aplicar a regra**. A função
recebe números; terminal, formulário ou API cuidam da conversão. Isso permite
reutilizar e testar a regra sem simular uma pessoa digitando.

### Passo 5 — transforme exemplos em testes

```python
def testar_calcular_frete() -> None:
    assert calcular_frete(50.0, 10.0) == 15.50
    assert calcular_frete(199.99, 1.0) == 8.75
    assert calcular_frete(200.0, 500.0) == 0.0

    try:
        calcular_frete(-1.0, 10.0)
        raise AssertionError("era esperado ValueError")
    except ValueError:
        pass

    for invalido in (float("nan"), float("inf"), float("-inf")):
        for subtotal, distancia in ((invalido, 10.0), (50.0, invalido)):
            try:
                calcular_frete(subtotal, distancia)
                raise AssertionError("era esperado ValueError")
            except ValueError:
                pass
```

Um teste tem três partes, frequentemente lembradas como AAA:

1. **Arrange:** preparar dados e dependências;
2. **Act:** executar uma operação;
3. **Assert:** comparar o resultado observado com o esperado.

Neste exemplo simples, preparação e execução cabem na mesma linha. Em sistemas
maiores, manter as três fases visíveis facilita a leitura.

### Passo 6 — só então melhore a estrutura

Primeiro faça o comportamento correto ficar observável. Depois melhore nomes,
extraia funções e remova duplicação, executando os testes após cada mudança.
Essa melhoria sem alterar comportamento recebe o nome de **refatoração**.

## 3. Decomposição: transformar verbos em unidades

Problemas grandes quase sempre escondem operações menores. Sublinhe os verbos:

> Ler tarefas, validar títulos, salvar, ordenar e apresentar um resumo.

Uma primeira decomposição pode ser:

```text
ler_tarefas()
validar_titulo(titulo)
salvar_tarefa(tarefa)
ordenar_tarefas(tarefas)
gerar_resumo(tarefas)
```

Uma boa unidade possui:

- um nome que revela intenção;
- entradas explícitas;
- uma responsabilidade principal;
- resultado ou efeito documentado;
- comportamento que pode ser verificado isoladamente.

Use a pergunta “o que teria de mudar para esta função mudar?”. Se a resposta
for “a regra de validação, o banco de dados, a interface ou o formato do
relatório”, existem responsabilidades demais agrupadas.

### Núcleo funcional e bordas com efeitos

Uma organização útil é separar:

- **núcleo:** calcula e transforma valores;
- **bordas:** leem teclado, arquivos, relógio, rede ou banco de dados;
- **orquestração:** conecta núcleo e bordas.

```python
def classificar_media(media: float) -> str:  # núcleo previsível
    if not 0 <= media <= 10:
        raise ValueError("média fora de 0..10")
    return "aprovado" if media >= 7 else "revisar"


def executar() -> None:  # borda: entrada e saída
    texto = input("Média: ")
    media = float(texto)
    print(classificar_media(media))
```

`classificar_media` não depende do terminal e pode ser chamada por uma API,
uma interface gráfica ou um teste. Efeitos não são ruins; apenas precisam ficar
visíveis e controlados.

## 4. Estado, identidade e invariantes

**Estado** é a informação que pode mudar: saldo, tarefas, tentativas restantes
ou posição atual. **Identidade** distingue entidades mesmo quando seus dados
são parecidos. **Invariante** é uma regra que deve continuar verdadeira após
qualquer operação.

Exemplos de invariantes:

- saldo nunca é `NaN`;
- ID de tarefa é único e não muda;
- título não fica vazio depois de remover espaços;
- porcentagem permanece entre 0 e 100;
- quantidade em estoque é um inteiro não negativo.

Considere um saque:

```text
estado antes: saldo = 100
comando: sacar 30
estado depois: saldo = 70
invariante: saldo >= 0
```

Se dois trechos alteram o mesmo estado sem uma regra central, fica difícil
garantir a invariante. Encapsule a mudança:

```python
def sacar(saldo: float, valor: float) -> float:
    if valor <= 0:
        raise ValueError("valor deve ser positivo")
    if valor > saldo:
        raise ValueError("saldo insuficiente")
    novo_saldo = saldo - valor
    assert novo_saldo >= 0  # verifica uma condição interna do algoritmo
    return novo_saldo
```

`ValueError` trata entradas que podem vir do chamador. `assert` registra uma
suposição interna que, se falhar, indica defeito de programação. Não use
`assert` como única validação de dados externos: algumas configurações podem
desativá-la.

## 5. Rastrear a execução

O computador executa instruções segundo regras exatas; ele não preenche a
intenção do autor. Quando um algoritmo não está claro, simule-o em uma tabela.

```python
def somar_positivos(valores: list[int]) -> int:
    total = 0
    for valor in valores:
        if valor > 0:
            total += valor
    return total
```

Para `[4, -2, 7, 0]`:

| Iteração | `valor` | `valor > 0` | `total` antes | `total` depois |
|----------|---------|-------------|---------------|----------------|
| inicial | — | — | — | `0` |
| 1 | `4` | verdadeiro | `0` | `4` |
| 2 | `-2` | falso | `4` | `4` |
| 3 | `7` | verdadeiro | `4` | `11` |
| 4 | `0` | falso | `11` | `11` |

Ao rastrear, registre somente variáveis que influenciam a decisão ou o
resultado. O objetivo não é copiar cada detalhe da memória, mas tornar o fluxo
visível.

## 6. Depuração orientada por evidências

Depurar é localizar a primeira diferença entre o comportamento esperado e o
observado. Use o ciclo:

1. descreva o esperado em uma frase;
2. reproduza a falha de forma consistente;
3. reduza para a menor entrada que ainda falha;
4. leia a primeira mensagem de erro relevante por inteiro;
5. localize a primeira etapa em que esperado e obtido divergem;
6. formule uma hipótese específica;
7. faça uma observação com teste, log ou depurador;
8. altere apenas uma causa possível;
9. execute também os testes que já passavam;
10. preserve um teste de regressão.

Hipótese útil:

> O último item não é processado porque o limite superior de `range` é
> exclusivo.

Hipótese pouco útil:

> O Python se perdeu.

### Exemplo: defeito de limite

```python
def contar_de_um_ate(limite: int) -> list[int]:
    return list(range(1, limite))  # defeito: exclui o limite
```

Reprodução mínima:

```python
assert contar_de_um_ate(1) == [1]  # obtido: []
```

O teste revela que a divergência ocorre já no menor limite válido. A hipótese é
que `range` exclui o segundo argumento. A correção pode ser verificada sem
alterar outras partes:

```python
def contar_de_um_ate(limite: int) -> list[int]:
    return list(range(1, limite + 1))
```

Mantenha o teste de `1`; ele impede que o mesmo erro retorne silenciosamente.

### Sintoma não é necessariamente causa

Se um relatório mostra total errado, a causa pode estar na leitura, conversão,
filtragem ou soma. Instrumente as fronteiras:

```text
texto lido → número convertido → valor validado → valor acumulado → saída
```

Procure a primeira seta incorreta. Corrigir apenas a formatação final pode
esconder o defeito em vez de removê-lo.

### Registro seguro durante a depuração

Não imprima senhas, tokens, documentos pessoais ou conteúdo sensível. Prefira
metadados úteis, como quantidade, tipo, etapa e identificador sintético:

```python
print({"etapa": "validacao", "quantidade": len(itens), "lote": "exemplo-01"})
```

## 7. Como ler código que você não escreveu

Leia em camadas, não linha por linha desde o início:

1. leia o README e descubra como executar os testes;
2. identifique o ponto de entrada;
3. encontre entradas, saídas e efeitos externos;
4. marque estruturas de dados e os lugares onde elas mudam;
5. siga um caso comum com papel e lápis;
6. siga entrada vazia, fronteiras e erro;
7. só então investigue detalhes de implementação.

Para cada função, responda:

```text
Qual é o contrato?
Quem a chama?
O que ela chama?
O que ela retorna?
Que estado altera?
Que erro pode produzir?
Como seu comportamento é testado?
```

Se não consegue responder, registre a dúvida em vez de inventar uma explicação.
Uma hipótese claramente marcada pode ser verificada; uma suposição silenciosa
vira conhecimento falso.

## 8. Como estudar de forma ativa

Reconhecer uma explicação não é o mesmo que conseguir produzi-la. Para cada
conceito, use este ciclo:

1. **prever:** diga o resultado antes de executar;
2. **executar:** digite o exemplo, sem apenas copiar e colar;
3. **explicar:** descreva o papel de cada linha;
4. **variar:** mude entrada, condição ou estrutura;
5. **quebrar:** crie intencionalmente um caso que falha;
6. **diagnosticar:** encontre a causa com evidência;
7. **reconstruir:** feche o material e refaça uma versão menor;
8. **revisar:** retorne depois de um intervalo.

Uma sessão de 60 minutos pode ser organizada assim:

| Tempo | Atividade |
|-------|-----------|
| 5 min | recuperar de memória o conceito anterior |
| 15 min | estudar uma ideia nova e prever exemplos |
| 25 min | implementar, testar e variar |
| 10 min | resolver um exercício sem consultar |
| 5 min | registrar evidência, dúvida e próximo passo |

### Recuperação espaçada

Releia menos e tente lembrar mais. Uma sugestão de revisão:

- no mesmo dia: explique sem olhar;
- no dia seguinte: refaça um exemplo curto;
- após uma semana: resolva uma variação;
- após um mês: use o conceito em um projeto.

O intervalo não precisa ser exato. O ponto é recuperar o conhecimento quando
ele já exige algum esforço.

### Diário de engenharia

Ao fim da sessão, registre algo concreto:

```text
Objetivo: validar três notas e calcular a média.
Previsão: nota 10, 8 e 6 produz média 8.
Erro observado: texto vazio causou ValueError na conversão.
Causa: a borda não tratava ausência de entrada.
Correção: validação antes de chamar a regra de negócio.
Evidência: 7 testes passando.
Próximo passo: separar cálculo e classificação.
```

“Estudei funções” mede tempo. “Implementei duas funções, testei quatro limites e
consigo explicar retorno versus impressão” mede aprendizagem.

## 9. Como usar documentação, fóruns e assistentes

Use ajuda externa para remover bloqueios, não para terceirizar toda a solução.
Antes de perguntar, reúna:

- objetivo esperado;
- exemplo mínimo reproduzível;
- saída obtida e mensagem completa;
- versões do runtime e do sistema;
- hipótese já verificada.

Ao receber uma solução:

1. leia antes de executar;
2. confira se acessa arquivos, rede ou comandos;
3. execute apenas com dados sintéticos;
4. explique cada trecho;
5. escreva pelo menos um teste novo;
6. reconstrua a ideia sem consultar.

Nunca publique credenciais, arquivos `.env`, dados reais, cookies, chaves ou
dumps. Uma resposta que funciona mas que você não consegue explicar ainda não
é conhecimento adquirido.

## 10. Erros comuns de quem está começando

| Hábito | Consequência | Substituição útil |
|--------|--------------|-------------------|
| começar pela interface | regra fica misturada com entrada e saída | implemente primeiro uma função pura |
| copiar projeto inteiro | reconhecimento sem recuperação | reconstrua uma versão mínima |
| testar apenas o caso feliz | limites quebram em produção | teste vazio, fronteiras e inválidos |
| mudar várias linhas | causa da correção fica desconhecida | uma hipótese e uma mudança por vez |
| ignorar a primeira exceção | erros derivados confundem o diagnóstico | leia a pilha do início relevante |
| escolher nomes como `x1` e `aux2` | intenção se perde | nomeie pelo papel no domínio |
| capturar qualquer erro | falhas reais ficam escondidas | trate somente erros recuperáveis |
| estudar cinco linguagens de uma vez | sintaxes competem com o conceito | domine o núcleo em uma linguagem |
| medir apenas horas | cria falsa sensação de progresso | preserve código, testes e explicações |

## 11. Exercícios graduais

Faça os exercícios em ordem. Use dados locais e sintéticos.

### Nível 1 — especificar

1. Para uma calculadora de média, escreva objetivo, entradas, domínio, regras,
   saída, dois erros e três invariantes.
2. Reescreva “criar uma agenda fácil” como cinco comportamentos observáveis.
3. Crie uma tabela de exemplos para desconto de 10% a partir de R$ 100,00,
   incluindo `99.99`, `100.00`, zero e valor negativo.

### Nível 2 — decompor

4. Divida uma agenda de contatos em pelo menos seis funções. Para cada uma,
   documente parâmetros, retorno e possíveis erros.
5. Separe uma calculadora CLI em núcleo, borda e orquestração. Nenhuma regra
   matemática deve chamar `input` ou `print`.
6. Defina invariantes para uma fila de atendimento que usa senhas numéricas.

### Nível 3 — rastrear e testar

7. Rastreie manualmente a soma de `[3, 1, 4, 1, 5]`, mostrando acumulador antes
   e depois de cada iteração.
8. Crie partições de teste para uma função `pode_dirigir(idade, habilitado)`.
9. Encontre o defeito em `range(1, limite)` quando o requisito diz “até o
   limite, inclusive” e preserve um teste de regressão.

### Nível 4 — investigar

10. Pegue um erro antigo ou introduza um defeito simples. Registre reprodução
    mínima, hipótese, observação, causa, correção e teste.
11. Leia um programa pequeno deste curso sem executá-lo. Desenhe seu fluxo e
    preveja a saída; depois compare com a execução.
12. Implemente o cálculo de frete deste capítulo sem consultar o exemplo. Mude
    a regra de gratuidade para combinar subtotal e distância, atualizando a
    especificação antes do código.

## Evidência e critério de conclusão

Crie uma pasta de estudo contendo:

- uma especificação com exemplos e limites;
- um pseudocódigo;
- uma implementação com núcleo separado de entrada/saída;
- pelo menos seis testes, incluindo fronteiras e erro;
- uma tabela de rastreamento;
- um relato curto de depuração.

Considere o capítulo concluído quando você puder, sem consultar o texto:

- [ ] transformar um pedido ambíguo em contrato verificável;
- [ ] explicar pré-condição, pós-condição e invariante com exemplos;
- [ ] decompor um problema em funções coesas;
- [ ] prever e rastrear a execução de um laço simples;
- [ ] diferenciar sintoma, hipótese, evidência e causa;
- [ ] produzir um teste que falha antes de corrigir o defeito;
- [ ] explicar por que regras de negócio não devem depender diretamente da UI.

O critério final é simples: outra pessoa deve conseguir implementar uma solução
compatível usando apenas sua especificação, seu pseudocódigo e seus exemplos.

## Próximo capítulo

Com o método de resolução estabelecido, avance para
[Lógica e algoritmos](01-logica-algoritmos.md). Lá você transformará contratos
em expressões, decisões, repetições, funções e estruturas de dados.
