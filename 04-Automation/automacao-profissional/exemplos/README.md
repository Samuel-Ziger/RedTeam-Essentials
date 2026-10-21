# Exemplos nas cinco linguagens — contrato comum

Python, Java, C17, C# e JavaScript implementam batch-plan, um planejador pequeno
usado para comparar o mesmo contrato entre runtimes. Ele não executa jobs: valida,
normaliza, deduplica e ordena IDs.

## Contrato

~~~text
batch-plan --items ID[,ID...] [--format text|json]
~~~

- ID aceita apenas ASCII A–Z, a–z, 0–9, underscore e hífen;
- campo vazio, espaço, ponto, barra e opção desconhecida são inválidos;
- duplicatas são removidas por comparação ordinal;
- saída é ordenada ascendentemente por bytes ASCII;
- text: count=N items=id1,id2;
- JSON: objeto com count inteiro e items array;
- sucesso retorna 0;
- erro de uso retorna 2, stdout vazio e diagnóstico em stderr;
- nenhuma implementação lê rede, ambiente, arquivo ou diretório de trabalho.

O limite didático é 64 IDs e entrada de até 1023 bytes. As implementações devem
recusar excesso em vez de truncar. O exemplo usa ASCII de propósito para que regex,
ordem e JSON sejam equivalentes nas cinco linguagens.

## Execução

### Python

~~~bash
python3 exemplos/python/batch_plan.py --items build,test,build --format json
~~~

### Java

~~~bash
javac exemplos/java/BatchPlan.java
java -cp exemplos/java BatchPlan --items build,test,build
~~~

### C17

~~~bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  exemplos/c/batch_plan.c -o /tmp/batch-plan
/tmp/batch-plan --items build,test,build
~~~

### C#

~~~bash
dotnet run --project exemplos/csharp/BatchPlan.csproj -- \
  --items build,test,build
~~~

### JavaScript

~~~bash
node exemplos/javascript/batch-plan.mjs --items build,test,build --format json
~~~

## Vetores de conformidade

| Entrada | Resultado |
|---|---|
| z,a,z | a,z; count 2 |
| build_test,a-1 | aceito |
| vazio | erro 2 |
| a,,b | erro 2 |
| ../x | erro 2 |
| a b | erro 2 |
| format yaml | erro 2 |
| opção extra | erro 2 |

JSON deve ser analisado por parser no teste, não por substring. O runner do curso
também verifica que falha escreve somente em stderr.

## O que comparar

| Aspecto | Python | Java | C17 | C# | JavaScript |
|---|---|---|---|---|---|
| argumentos | argparse | loop explícito | loop explícito | loop explícito | parseArgs |
| conjunto ordenado | set + sorted | TreeSet | qsort + compactação | Distinct + Order | Set + sort |
| JSON | json | serialização limitada | escrita limitada | System.Text.Json | JSON.stringify |
| ausência | None | null | ponteiro NULL | nullable | undefined |
| erro esperado | ValueError/parser | retorno 2 | retorno 2 | retorno 2 | exceção capturada |

Java e C usam serialização manual apenas porque o alfabeto aceito impede aspas e
controle. Isso não é um modelo para JSON geral; use biblioteca para dados livres.

## Exercício de comparação

Adicione max-items configurável entre 1 e 64 nas cinco linguagens. Antes do código,
defina gramática, precedência, limites e erros. A entrega passa quando os mesmos
vetores produzem stdout, stderr e código equivalentes.

