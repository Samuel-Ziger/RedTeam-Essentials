# Guia prático de depuração

Depurar não é experimentar alterações até a mensagem desaparecer. É reduzir a
incerteza com observações controladas. Este guia apresenta um processo que pode
ser usado em qualquer uma das linguagens do curso.

## Objetivos

Ao terminar, você deverá conseguir:

- classificar a falha antes de tentar corrigi-la;
- produzir uma reprodução mínima e determinística;
- interpretar código de saída, `stdout`, `stderr` e stack trace;
- formular uma hipótese que possa ser refutada;
- inspecionar estado sem alterar desnecessariamente o comportamento;
- criar um teste de regressão que falha antes e passa depois da correção;
- distinguir causa, sintoma e consequência.

## 1. Classifique a falha

| Classe | Momento | Exemplo | Primeira pergunta |
|--------|---------|---------|-------------------|
| sintaxe/compilação | antes de executar | delimitador ausente, tipo incompatível | qual arquivo e posição o diagnóstico aponta? |
| inicialização | ao carregar configuração | porta inválida, arquivo inexistente | qual dependência ou configuração faltou? |
| execução | durante uma operação | divisão por zero, referência nula | qual entrada e caminho chegaram à operação? |
| lógica | programa termina, mas responde errado | limite `>` em vez de `>=` | qual regra esperada foi violada? |
| integração | componentes isolados passam | JSON divergente, timeout, schema incompatível | qual contrato entre componentes divergiu? |
| concorrência | depende da ordem/tempo | atualização perdida | qual estado é compartilhado e sem coordenação? |
| desempenho | resultado correto, custo inadequado | consulta repetida em laço | qual recurso foi medido como gargalo? |
| ambiente | funciona em uma máquina | locale, versão ou permissão diferente | qual diferença de ambiente é relevante? |

A classe pode mudar durante a investigação. “A API caiu” é um sintoma; a causa
pode ser configuração, dado inválido, exaustão de recursos ou uma exceção não
tratada.

## 2. Processo científico em sete passos

### Passo 1 — descreva o esperado e o observado

Use valores concretos:

```text
Dado: notas [10, 8, 4]
Esperado: média 7.33 e três classificações
Observado: média 5.50 e processo encerra com código 0
Ambiente: Python 3.12, Linux x86_64
```

“Está errado” não define uma diferença verificável.

### Passo 2 — reproduza

Registre o comando exato, diretório de execução, entrada e configuração. Execute
novamente. Se a falha não for determinística, registre frequência e condições:

```bash
python3 programa.py 10 8 4
printf 'codigo=%s\n' "$?"
```

O código `0` normalmente significa sucesso; valores diferentes de zero indicam
classes de falha definidas pelo programa. Não descarte `stderr`: diagnósticos
devem ser separados da saída de dados quando a CLI faz parte de uma automação.

### Passo 3 — reduza

Remova entradas, dependências e etapas até chegar ao menor caso que ainda falha.
Se `[10, 8, 4]` falha, teste `[10]`, `[8, 4]`, limites `0` e `10` e um
valor inválido. Redução revela qual dimensão ativa o defeito.

### Passo 4 — localize a primeira divergência

Não comece pela última exceção visível. Rastreie da entrada à saída e encontre o
primeiro ponto em que o estado real diverge do esperado.

| Etapa | Estado esperado | Estado observado |
|-------|-----------------|------------------|
| parsing | `[10.0, 8.0, 4.0]` | `[10.0, 8.0, 4.0]` |
| soma | `22.0` | `22.0` |
| divisor | `3` | `4` |
| média | `7.33` | `5.50` |

Essa tabela transforma “a média está errada” em “o divisor contém uma unidade
extra”.

### Passo 5 — formule uma hipótese refutável

Boa hipótese:

> O laço incrementa o contador antes de processar a primeira nota; se eu
> registrar o contador a cada iteração, ele terminará em 4 para três entradas.

Hipótese fraca:

> Deve ser algum problema no laço.

Uma hipótese precisa prever uma observação. Se a previsão não ocorrer, descarte
a hipótese em vez de adaptar a história depois.

### Passo 6 — corrija a causa e crie regressão

Escreva primeiro um teste com o menor caso. Confirme que ele falha pelo motivo
esperado, faça a menor correção e execute:

1. o teste novo;
2. os testes relacionados;
3. a suíte completa;
4. o comando original da reprodução.

Não transforme uma exceção em valor padrão apenas para silenciar o erro. Isso
pode trocar uma falha visível por dado incorreto.

### Passo 7 — explique e previna

Registre:

- causa técnica;
- condição que ativava o defeito;
- por que os testes anteriores não o encontraram;
- alteração realizada;
- teste que impede regressão;
- riscos ou casos ainda não cobertos.

## 3. Como ler uma mensagem de erro

Comece pela primeira mensagem produzida pelo seu código e preserve o texto
completo. Em um stack trace:

1. identifique o tipo da exceção;
2. leia a mensagem;
3. encontre o primeiro frame pertencente ao seu projeto;
4. inspecione argumentos e estado nessa linha;
5. suba a pilha para entender quem forneceu o valor;
6. não assuma que a última função listada criou a causa.

Uma exceção em `calcular_media` pode ter sido causada por validação ausente no
adaptador de entrada. O lugar da manifestação e o lugar da decisão incorreta
podem ser diferentes.

## 4. Observação sem ruído

Uma mensagem temporária deve responder a uma pergunta:

```python
print(f"indice={indice} total={total!r} nota={nota!r}", file=sys.stderr)
```

Evite dezenas de `print("aqui")`. Inclua nomes, valores e uma identidade da
operação. Remova instrumentação temporária depois ou converta-a em log com nível
adequado.

Para aplicações, prefira eventos estruturados:

```text
evento=tarefa_criada request_id=abc123 tarefa_id=42 duracao_ms=8
```

Não registre senha, token, cookie, corpo sensível ou dados pessoais. Um
identificador de correlação ajuda a seguir uma operação sem expor seu conteúdo.

## 5. Ferramentas por linguagem

### Python

```bash
python3 -m unittest discover -v \
  -s 00-Fundamentos/programacao/exemplos/python \
  -p 'test_*.py'
python3 -m pdb caminho/do/programa.py 10 8 4
python3 -X dev caminho/do/programa.py 10 8 4
```

No `pdb`, use `n` para próxima linha, `s` para entrar na função, `p expressao`
para inspecionar e `c` para continuar. Leia o traceback de baixo para cima para
ver a exceção, mas acompanhe o fluxo de chamadas de cima para baixo.

### JavaScript e Node.js

```bash
node --check arquivo.mjs
node --test arquivo.test.mjs
node --inspect-brk arquivo.mjs 10 8 4
```

Promises rejeitadas precisam ser aguardadas ou retornadas pelo teste. Se o teste
termina antes da Promise, um falso positivo é possível.

### Java

```bash
javac -Xlint:all -Werror Fundamentos.java
java Fundamentos 10 8 4
jdb Fundamentos 10 8 4
```

O primeiro bloco `Caused by` costuma revelar a falha mais interna, mas o frame
do projeto mostra onde o contrato foi violado. Não capture `Exception` apenas
para imprimir e continuar.

### C

Compile uma versão de investigação separada da versão otimizada:

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror -g -O0 programa.c -o programa
cc -std=c17 -g -O1 -fsanitize=address,undefined programa.c -o programa-san
gdb --args ./programa 10 8 4
./programa-san 10 8 4
```

No `gdb`, comece com `break main`, `run`, `next`, `step`, `print variavel` e
`backtrace`. Sanitizers detectam várias violações de memória, mas não provam a
ausência de todas elas. Nunca ignore warning de compilação sem entender a
conversão, o lifetime ou o acesso envolvido.

### C# e .NET

```bash
dotnet build
dotnet run -- 10 8 4
dotnet test
```

Use breakpoints condicionais e a janela de variáveis do editor. Em código
assíncrono, acompanhe a exceção original e o ponto de `await`; bloquear uma
`Task` com `.Result` pode introduzir comportamento diferente.

## 6. Estratégias que localizam a causa

### Particionamento de entrada

Separe classes válidas e inválidas:

- abaixo do mínimo;
- exatamente no mínimo;
- valor comum;
- exatamente no máximo;
- acima do máximo;
- vazio, ausente, tipo incorreto e valor não finito.

Testar apenas `7` não exercita as fronteiras `0`, `5`, `7`, `9` e `10`
usadas pelas classificações.

### Busca binária na mudança

Se a falha surgiu após muitos commits, encontre um commit conhecido como bom e
outro ruim. Teste o ponto intermediário e repita. `git bisect` automatiza essa
busca, desde que exista um comando confiável que retorne sucesso ou falha.

### Substituição controlada

Troque uma dependência instável por uma implementação determinística: relógio
fixo, arquivo temporário, banco isolado ou servidor local simulado. A substituição
deve preservar o contrato relevante; caso contrário, o teste deixa de representar
a integração real.

### Medição antes da otimização

Para desempenho, registre tamanho da entrada, ambiente, aquecimento, número de
repetições e distribuição dos tempos. Uma única medição inclui ruído. Primeiro
encontre o recurso limitante — CPU, memória, disco, rede ou contenção — e só
então altere o algoritmo ou arquitetura.

## 7. Erros comuns durante a depuração

- mudar várias linhas antes de testar a hipótese;
- testar com dados diferentes a cada execução;
- capturar e ignorar a exceção;
- culpar biblioteca ou runtime antes de criar caso mínimo;
- confundir correlação temporal com causa;
- corrigir apenas o exemplo sem cobrir a classe de entradas;
- deixar logs com segredos;
- otimizar antes de medir;
- não executar a suíte completa após a correção;
- apagar a evidência que explicava a falha.

## 8. Laboratório guiado

Escolha um exemplo da pasta `exemplos/` e trabalhe em uma cópia.

1. altere uma comparação de limite (`>=` para `>`);
2. execute a suíte e identifique qual caso detecta a mudança;
3. se nenhum teste falhar, escreva o teste ausente;
4. registre a tabela de rastreamento;
5. reproduza pelo CLI e anote código de saída, `stdout` e `stderr`;
6. use o depurador para parar na decisão;
7. restaure a regra;
8. execute toda a suíte;
9. escreva uma explicação de cinco linhas ligando requisito, defeito e teste.

### Critério de conclusão

- [ ] A reprodução usa um comando e uma entrada exatos.
- [ ] A primeira divergência foi identificada.
- [ ] A hipótese previu uma observação verificável.
- [ ] O teste falhou antes e passou depois.
- [ ] A suíte completa permaneceu verde.
- [ ] A explicação diferencia causa, sintoma e correção.
