# Mesmo contrato em cinco linguagens

Os exemplos implementam uma entrada de aplicação mínima em Python, Java, C17,
C# e JavaScript. O valor didático está na equivalência observável: sintaxe e
bibliotecas mudam, mas precedência, validação, canais e códigos permanecem.

## Contrato comum

A aplicação resolve `profile` nesta ordem:

```text
--profile > APP_PROFILE > development
```

Valores aceitos: `development`, `testing` e `production`.

| Situação | `stdout` | `stderr` | Código |
|---|---|---|---:|
| `--help` | ajuda | vazio | 0 |
| execução válida em texto | resultado | vazio | 0 |
| execução válida em JSON | objeto JSON | vazio | 0 |
| opção/valor inválido | vazio | diagnóstico | 2 |
| `APP_PROFILE` inválido | vazio | diagnóstico | 2 |

O JSON de sucesso contém exatamente a decisão relevante:

```json
{"profile":"testing","source":"environment"}
```

`source` é `cli`, `environment` ou `default`. A origem faz parte do resultado
porque permite diagnosticar precedência sem imprimir todo o ambiente — algo que
poderia revelar credenciais.

## Por que validar duas vezes

O parser de argumentos restringe `--profile`, mas `resolve_profile` e
`resolveProfile` também validam valores recebidos diretamente. Uma função de
domínio exportada não deve depender de o único chamador atual ter validado antes:
testes, GUI ou biblioteca podem chamá-la sem passar pela CLI.

O ambiente é sempre validado quando vence. Se a CLI válida estiver presente,
ela vence um ambiente inválido. Essa política é deliberada: a fonte de maior
precedência define a configuração efetiva. Alterar essa regra exigiria atualizar
contrato e testes nas cinco linguagens.

## Executar tudo

Na raiz do repositório:

```bash
bash 03-AD-Notes/desenvolvimento-aplicacoes/testar-curso.sh
```

O runner compila com avisos como erro quando a toolchain permite, executa testes
unitários, verifica precedência e testa uma falha como processo real. Toolchain
ausente gera `SKIP`; ferramenta instalada que falha interrompe a validação.

## Execução por linguagem

### Python 3

```bash
cd 03-AD-Notes/desenvolvimento-aplicacoes/exemplos/python
python3 -m unittest -v
python3 app_config.py --help
APP_PROFILE=testing python3 app_config.py --format json
python3 app_config.py --profile production
```

`argparse` cuida da gramática externa; `resolve_profile` recebe um `Mapping`
injetado e pode ser testada sem modificar o ambiente global.

### Java 21+

```bash
build_dir="$(mktemp -d)"
javac -Xlint:all -Werror -d "$build_dir" \
  03-AD-Notes/desenvolvimento-aplicacoes/exemplos/java/AppConfig.java
APP_PROFILE=testing java -cp "$build_dir" AppConfig --format json
```

O exemplo usa somente a biblioteca padrão. O loop do parser explicita consumo
do próximo argumento e permite comparar ausência de valor com opção desconhecida.

### C17

```bash
build_dir="$(mktemp -d)"
cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  03-AD-Notes/desenvolvimento-aplicacoes/exemplos/c/app_config.c \
  -o "$build_dir/app_config"
APP_PROFILE=testing "$build_dir/app_config" --format json
```

Em C, ownership, terminação de strings e retorno de processo ficam visíveis. O
exemplo apenas referencia `argv`/`getenv`; uma aplicação que retivesse ou
transformasse valores precisaria declarar duração e memória.

### C# / .NET 10

```bash
dotnet run \
  --project 03-AD-Notes/desenvolvimento-aplicacoes/exemplos/csharp/AppConfig.csproj \
  --configuration Release -- --format json
```

Nullable e avisos como erro estão habilitados no projeto. `Console.Out`,
`Console.Error` e o retorno de `Main` materializam o contrato do processo.

### JavaScript / Node.js 24+

```bash
cd 03-AD-Notes/desenvolvimento-aplicacoes/exemplos/javascript
node --test app-config.test.mjs
APP_PROFILE=testing node app-config.mjs --format json
```

`node:util.parseArgs` trata a gramática externa; `main` aceita argumentos e
ambiente injetados. A execução direta apenas converte o retorno em
`process.exitCode`, mantendo a lógica chamável em teste.

## Comparação técnica

| Linguagem | Entrada da CLI | Ambiente | Resultado imutável/estruturado | Teste principal |
|---|---|---|---|---|
| Python | `argparse` | `Mapping` injetado | `dataclass(frozen=True)` | `unittest` |
| Java | loop sobre `String[]` | `System.getenv` | variáveis locais/`Set` imutável | runner de processo |
| C17 | `argc/argv` | `getenv` | valores simples | compilação estrita + processo |
| C# | loop sobre `string[]` | `Environment` | tipos nullable/coleção | build estrito + processo |
| JavaScript | `parseArgs` | objeto injetado | objeto de resultado | `node:test` |

Os exemplos pequenos de Java, C e C# não extraem ainda o resolver como unidade
independente. Essa é uma prática recomendada: mover parse/resolução/apresentação
para funções testáveis e manter `main` como composition root.

## Testes negativos reproduzíveis

Execute um comando inválido preservando os canais:

```bash
tmp_dir="$(mktemp -d)"
set +e
APP_PROFILE=unknown python3 \
  03-AD-Notes/desenvolvimento-aplicacoes/exemplos/python/app_config.py \
  >"$tmp_dir/stdout" 2>"$tmp_dir/stderr"
status=$?
set -e
printf 'status=%s stdout_bytes=%s stderr_bytes=%s\n' \
  "$status" "$(wc -c <"$tmp_dir/stdout")" "$(wc -c <"$tmp_dir/stderr")"
```

O esperado é código `2`, zero bytes em `stdout` e mensagem em `stderr`. Esse
teste captura regressões que uma chamada direta a função não vê: canal trocado,
exceção sem tratamento ou código do processo perdido.

## Vetores que toda implementação deve cobrir

1. nenhuma fonte → `development/default`;
2. ambiente válido → valor/environment;
3. CLI válida sobre ambiente válido → valor/cli;
4. CLI válida sobre ambiente inválido → valor/cli;
5. ambiente vazio/desconhecido → erro 2;
6. CLI vazia/desconhecida → erro 2;
7. formato inválido → erro 2;
8. opção desconhecida → erro 2;
9. `--help` → sucesso sem depender do ambiente;
10. JSON analisável por parser e sem diagnóstico misturado.

## Ambiguidades deliberadamente excluídas

- nomes de profile diferenciam maiúsculas/minúsculas;
- não há arquivo `.env` implícito;
- não há abreviação de opções;
- não há leitura interativa quando valor falta;
- não há cor ou formatação dependente de TTY;
- JSON não contém timestamp ou campos instáveis.

Essas restrições tornam o exemplo determinístico. Em um produto real, qualquer
flexibilidade adicional precisa de regra, ajuda e teste.

## Exercícios

1. Extraia resolver e presenter em Java, C e C# e escreva testes unitários.
2. Adicione `--config PATH` com precedência `CLI > ambiente > arquivo > padrão`.
3. Diferencie ausência de string vazia em todas as fontes.
4. Crie presenter JSON único por linguagem e valide com parser real.
5. Adicione uma falha operacional de leitura com código diferente de `2`.
6. Escreva teste que prove que um canário não aparece em nenhuma saída.

Consulte o [Lab 01](../laboratorios/lab-01-contrato-cli-configuracao.md) para
evoluir esse contrato até uma aplicação pequena e observável.
