# Contrato de query nas cinco linguagens

Python, Java, C17, C# e JavaScript implementam exatamente o mesmo programa local.
O objetivo é comparar validação, tipos, buffers, CLI, saída e códigos sem esconder
o contrato em um client HTTP.

## Contrato

~~~text
api-query --limit 1..100 [--after TOKEN] [--status active|archived]
~~~

- limit é obrigatório e inteiro entre 1 e 100;
- after é Base64URL sem padding, não vazio e com até 512 caracteres;
- status aceita somente active ou archived;
- opções desconhecidas, repetidas ou sem valor são inválidas;
- sucesso escreve uma única linha em stdout e termina 0;
- erro de uso deixa stdout vazio, explica em stderr e termina 2;
- a ordem canônica é limit, after, status.

~~~text
GET /v1/items?limit=20&after=abc_123&status=active
~~~

O token restrito pode ser anexado sem codificação adicional. Um cliente geral
deve usar o construtor de URI da biblioteca, nunca concatenar entrada livre.

## Por que o exemplo é deliberadamente pequeno

O mesmo problema revela diferenças:

| Tema | Python | Java | C17 | C# | JavaScript |
|---|---|---|---|---|---|
| inteiro inválido | argparse/type | parse com catch | strtol + errno | TryParse | Number + isInteger |
| memória | gerenciada | gerenciada | buffers explícitos | gerenciada | gerenciada |
| ausência | None | null | ponteiro NULL | nullable | null/undefined |
| código de processo | SystemExit | System.exit | return/exit | retorno top-level | process.exitCode |

Linguagem gerenciada não elimina limites. C torna ownership visível, mas todas
precisam rejeitar token enorme, duplicate option e enum desconhecido.

## Execução

~~~bash
python3 exemplos/python/api_query.py --limit 20 --after abc_123 --status active

javac exemplos/java/ApiQuery.java
java -cp exemplos/java ApiQuery --limit 20 --after abc_123 --status active

cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  exemplos/c/api_query.c -o /tmp/api-query
/tmp/api-query --limit 20 --after abc_123 --status active

dotnet run --project exemplos/csharp/ApiQuery.csproj -- \
  --limit 20 --after abc_123 --status active

node exemplos/javascript/api-query.mjs \
  --limit 20 --after abc_123 --status active
~~~

Execute a partir do diretório engenharia-apis ou ajuste os caminhos.

## Casos negativos

~~~bash
python3 exemplos/python/api_query.py --limit nope
python3 exemplos/python/api_query.py --limit 1 --limit 2
python3 exemplos/python/api_query.py --limit 1 --after 'bad=token'
python3 exemplos/python/api_query.py --limit 1 --status unknown
~~~

Repita nas outras linguagens e confira três dimensões: código 2, stdout vazio e
diagnóstico em stderr. Mensagem idêntica não é exigida; comportamento é.

## Relação com o Contract Lab

O exemplo aceita Base64URL simples para fins didáticos. O Contract Lab usa cursor
mais forte: payload versionado, filtro vinculado e HMAC. Um cliente deve tratar
cursor como string opaca, devolvê-lo sem editar e descartar quando muda a
consulta.

## Exercícios

1. Adicione filtro titlePrefix usando codificador de URI padrão.
2. Escreva teste de processo para todos os erros em uma linguagem.
3. Faça property test garantindo ordem canônica dos parâmetros.
4. Troque a saída textual por objeto RequestPlan e serialize em JSON.
5. Compare inteiros maiores que 2^53 entre JavaScript, Java e C#.

## Checklist

- [ ] As cinco versões aceitam e rejeitam os mesmos casos.
- [ ] Nenhum parser ignora opção desconhecida ou repetida.
- [ ] Token possui limite de tamanho.
- [ ] stdout é estável e contém apenas dado.
- [ ] stderr contém somente diagnóstico.
- [ ] O runner compila/executa sem acesso à Internet.
