# Terminal, editor e Git: um ambiente de desenvolvimento previsível

Programar não é apenas escrever linhas em um editor. O sistema precisa localizar
arquivos, iniciar processos, entregar entradas, capturar saídas, selecionar uma
versão do runtime e registrar mudanças. Quando esse fluxo não é compreendido,
qualquer erro parece aleatório. Quando ele é explícito, quase toda falha pode ser
reduzida a uma hipótese testável.

Este capítulo usa apenas dados fictícios e uma pasta criada para estudo. Execute
os comandos dentro dessa pasta; nunca experimente comandos de remoção em uma
raiz, diretório pessoal ou projeto importante.

## Objetivos de aprendizagem

Ao terminar, você deverá conseguir:

- explicar a relação entre terminal, shell, comando, processo e código de saída;
- distinguir caminho absoluto, relativo, diretório atual e diretório no `PATH`;
- combinar programas com `stdin`, `stdout`, `stderr`, pipes e redirecionamentos;
- diagnosticar “comando não encontrado”, “arquivo não encontrado” e “permissão
  negada” sem tentativa aleatória;
- configurar editor, formatador, linter, testes e depurador como partes do mesmo
  ciclo de trabalho;
- explicar as três áreas locais do Git e recuperar erros comuns sem apagar
  trabalho;
- criar commits pequenos, revisar diferenças e resolver um conflito simples;
- preparar projetos reproduzíveis nas cinco linguagens da trilha.

## 1. O modelo mental: do texto digitado ao processo

O **terminal** é a interface de texto. O **shell** (Bash, Zsh ou PowerShell) lê
uma linha, interpreta sua sintaxe e solicita ao sistema operacional que inicie
um **processo**. O processo recebe argumentos, ambiente e três fluxos padrão:

```text
teclado/arquivo ──stdin──▶ programa ──stdout──▶ resultado normal
                                    └─stderr──▶ diagnóstico
                                             └─exit code──▶ shell
```

Considere:

```bash
python3 app.py --formato json
```

O shell:

1. separa o nome `python3` dos argumentos `app.py`, `--formato` e `json`;
2. procura o executável `python3` nos diretórios configurados em `PATH`;
3. cria um processo com diretório atual e variáveis de ambiente herdados;
4. conecta os três fluxos padrão ao terminal;
5. espera o processo terminar e recebe um código inteiro.

O shell interpreta aspas, curingas e redirecionamentos **antes** de iniciar o
programa. Por isso, `"relatorio final.txt"` é um argumento, enquanto
`relatorio final.txt` são dois.

> **Regra de diagnóstico:** sempre descubra qual programa recebeu quais
> argumentos, em qual diretório e com qual ambiente. Isso elimina grande parte
> dos problemas atribuídos vagamente ao “terminal”.

## 2. Crie um espaço de prática isolado

No Bash/Zsh, `mktemp -d` cria um diretório temporário com nome imprevisível:

```bash
LAB_PROGRAMACAO="$(mktemp -d)"
printf 'Laboratório: %s\n' "$LAB_PROGRAMACAO"
cd "$LAB_PROGRAMACAO"
mkdir -p curso-terminal/{src,tests,docs,dados}
cd curso-terminal
pwd
```

No PowerShell:

```powershell
$LabProgramacao = Join-Path ([System.IO.Path]::GetTempPath()) `
  ("curso-terminal-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $LabProgramacao | Out-Null
Set-Location $LabProgramacao
$Pastas = @(
  "curso-terminal/src",
  "curso-terminal/tests",
  "curso-terminal/docs",
  "curso-terminal/dados"
)
New-Item -ItemType Directory -Path $Pastas | Out-Null
Set-Location curso-terminal
Get-Location
```

O nome da variável é específico de propósito: não reutilize variáveis especiais
como `HOME`, `PATH` ou `USERPROFILE`.

## 3. Arquivos, diretórios e caminhos

O sistema de arquivos é uma árvore. Um caminho **absoluto** começa na raiz do
sistema; um caminho **relativo** é resolvido a partir do diretório atual.

```text
curso-terminal/
├── dados/
├── docs/
├── src/
└── tests/
```

Comandos equivalentes frequentes:

| Intenção | Bash/Zsh | PowerShell |
|----------|----------|------------|
| diretório atual | `pwd` | `Get-Location` |
| listar inclusive ocultos | `ls -la` | `Get-ChildItem -Force` |
| criar diretório | `mkdir -p src/modelo` | `New-Item -ItemType Directory -Force src/modelo` |
| criar arquivo | `touch README.md` | `New-Item -ItemType File README.md` |
| copiar | `cp README.md docs/guia.md` | `Copy-Item README.md docs/guia.md` |
| mover/renomear | `mv docs/guia.md docs/inicio.md` | `Move-Item docs/guia.md docs/inicio.md` |
| imprimir conteúdo | `sed -n '1,40p' README.md` | `Get-Content README.md -TotalCount 40` |

Símbolos importantes:

- `.`: diretório atual;
- `..`: diretório pai;
- `/` ou uma unidade como `C:\`: raiz;
- `~`: expansão feita pelo shell para o diretório pessoal;
- `.config`: nome oculto por convenção em sistemas Unix.

Compare conscientemente:

```bash
pwd                         # de onde o relativo parte?
printf 'rascunho\n' > docs/notas.txt
ls -l docs/notas.txt
realpath docs/notas.txt     # qual é o caminho absoluto resultante?
```

### Espaços, curingas e `--`

Aspas impedem divisão indevida:

```bash
mkdir -p "docs/notas da aula"
printf '%s\n' "primeira nota" > "docs/notas da aula/01.txt"
```

No Bash/Zsh, `*.txt` é expandido pelo shell para nomes existentes antes de o
programa ser executado. Não use curingas em operações destrutivas sem listar o
resultado primeiro. Para um nome iniciado por hífen, muitos comandos aceitam
`--` para encerrar as opções: `cat -- ./-exemplo.txt`.

## 4. Entrada, saída, erro e composição

Crie um programa pequeno em `src/resumo.py`:

```python
import sys

linhas = [linha.strip() for linha in sys.stdin if linha.strip()]

if not linhas:
    print("erro: nenhuma linha válida", file=sys.stderr)
    raise SystemExit(2)

print(f"quantidade={len(linhas)}")
print(f"primeiro={linhas[0]}")
```

Agora exercite cada canal:

```bash
printf 'Ana\nBeto\n' | python3 src/resumo.py
printf 'Ana\nBeto\n' | python3 src/resumo.py > dados/resumo.txt
printf '\n' | python3 src/resumo.py > dados/vazio.txt 2> dados/erro.txt
printf 'Código anterior: %s\n' "$?"
```

- `|` conecta o `stdout` do processo à esquerda ao `stdin` do processo à
  direita;
- `>` cria ou substitui o arquivo de saída;
- `>>` acrescenta ao final;
- `2>` redireciona apenas `stderr`;
- o código `0` significa sucesso por convenção; qualquer outro código comunica
  uma categoria de falha.

Use condicionais do shell em automação:

```bash
if printf 'Lia\n' | python3 src/resumo.py > dados/execucao.txt; then
  printf 'processamento concluído\n'
else
  printf 'processamento falhou\n' >&2
fi
```

Um pipeline é poderoso porque cada programa pode ter uma responsabilidade. Mas
ele também pode esconder falhas intermediárias. Em Bash, scripts rigorosos
costumam habilitar `set -o pipefail` e verificar resultados explicitamente.

## 5. Argumentos, ambiente e configuração

Três fontes têm papéis diferentes:

- **argumento:** escolha desta execução (`--arquivo dados.csv`);
- **variável de ambiente:** configuração fornecida pelo ambiente
  (`APP_LOG_LEVEL=debug`);
- **entrada padrão:** dados potencialmente grandes ou encadeados.

```bash
export APP_ENV=development
export APP_PORT=8000
python3 src/app.py --formato json < dados/entrada.txt
```

Ambiente é texto; o programa ainda precisa converter e validar `APP_PORT`.
Nunca coloque senha no código, no histórico do shell ou em um commit. Quando
uma aplicação precisa de `.env`, ignore o arquivo real e forneça somente um
`.env.example` com nomes e valores fictícios.

### Como o `PATH` funciona

```bash
command -v python3
python3 --version
printf '%s\n' "$PATH"
```

`PATH` é uma lista ordenada de diretórios. “Comando não encontrado” significa
que nenhum executável com aquele nome foi localizado nessa lista — não prova
que o software inexiste. Antes de alterar `PATH`, descubra onde a ferramenta foi
instalada e consulte a documentação do runtime.

Evite adicionar `.` ao início do `PATH`: um arquivo malicioso no diretório atual
poderia ser escolhido no lugar do programa esperado.

## 6. Permissões e processos

Em sistemas Unix, as permissões básicas são leitura (`r`), escrita (`w`) e
execução (`x`) para proprietário, grupo e demais usuários.

```bash
ls -l src/resumo.py
ps -ef
```

Um script pode ser executado com `python3 arquivo.py` sem bit executável, pois o
processo iniciado é o interpretador. Para executá-lo como `./arquivo.py`, ele
precisaria de uma linha *shebang* apropriada e permissão de execução.

“Permissão negada” não deve ser respondida automaticamente com `sudo`. Pergunte:

1. qual arquivo ou operação foi negado?
2. quem é o usuário atual?
3. quem é o proprietário e quais são as permissões?
4. o comando realmente deveria modificar esse local?

Privilégio elevado pode transformar um erro localizado em alteração no sistema
inteiro.

## 7. Editor, formatador, linter, teste e depurador

Uma configuração mínima de editor deve incluir:

- UTF-8, newline final e indentação consistente;
- destaque de espaços e arquivos alterados;
- formatador da linguagem;
- linter com diagnóstico no arquivo e na linha;
- execução do teste atual;
- depurador com breakpoint e inspeção de variáveis;
- integração Git exibindo o diff antes do commit.

Essas ferramentas respondem perguntas distintas:

| Ferramenta | Pergunta respondida |
|------------|---------------------|
| formatador | o código segue uma apresentação consistente? |
| linter/analisador | há padrão suspeito, erro provável ou regra violada? |
| compilador/type checker | operações e tipos são válidos antes de executar? |
| teste | o comportamento observado atende ao contrato? |
| depurador | qual era o estado quando o fluxo passou por esta linha? |

### Uma sessão de depuração consciente

Use este código deliberadamente incorreto:

```python
def media(valores: list[float]) -> float:
    total = 0.0
    for valor in valores:
        total += valor
    return total / len(valores)


print(media([]))
```

1. execute e leia a última linha da exceção;
2. localize a primeira linha do seu código na pilha;
3. coloque breakpoint antes do `return`;
4. inspecione `valores`, `total` e `len(valores)`;
5. formule a hipótese “lista vazia causa divisão por zero”;
6. defina o contrato: rejeitar vazio ou retornar um valor especial?
7. escreva o teste da decisão e só depois corrija.

`step over` executa uma chamada sem entrar nela; `step into` entra na função;
`step out` termina a função atual; a pilha de chamadas mostra como a execução
chegou ali. Depurar não é clicar em “continuar” até o erro sumir: é comparar
estado observado com uma hipótese.

## 8. Projeto reproduzível nas cinco linguagens

O objetivo não é instalar tudo agora, mas reconhecer as peças:

| Linguagem | Runtime/build | Manifesto comum | Artefato ignorado |
|-----------|---------------|-----------------|--------------------|
| Python | `venv`, `pip` | `pyproject.toml` | `.venv/`, `__pycache__/` |
| Java | Maven/Gradle | `pom.xml`, `build.gradle` | `target/`, `build/` |
| C | compilador, Make/CMake | `Makefile`, `CMakeLists.txt` | objetos e binários |
| C# | .NET CLI | `.csproj`, `.sln` | `bin/`, `obj/` |
| JavaScript | Node.js/npm | `package.json` | `node_modules/` |

Um projeto reproduzível registra:

1. versão mínima ou suportada do runtime;
2. dependências diretas e versões resolvidas em lockfile quando disponível;
3. comandos de build, teste e execução;
4. configuração de exemplo sem segredos;
5. artefatos gerados que não pertencem ao controle de versão.

Confirme origem, manutenção, licença e necessidade antes de adicionar uma
dependência. Um pacote é código executado com suas permissões, não apenas uma
linha conveniente no manifesto.

## 9. Git: conteúdo, não “botão de salvar”

Git registra *snapshots* endereçados pelo conteúdo. Localmente, pense em três
áreas:

```text
diretório de trabalho ──git add──▶ índice/staging ──git commit──▶ repositório
        ▲                    │                              │
        └──── editar ────────┘                    histórico local
```

- **diretório de trabalho:** arquivos que você está editando;
- **índice/staging:** seleção exata do próximo commit;
- **repositório:** commits, árvores e referências já registrados.

Crie um repositório descartável no laboratório:

```bash
git init -b main
git status --short
printf '# Curso de terminal\n' > README.md
git diff
git add README.md
git diff --staged
git commit -m "Documenta objetivo do laboratório"
git log --oneline --decorate -5
```

Se o Git solicitar identidade, configure nome e e-mail conforme a política do
seu ambiente. Não invente credenciais nem inclua token no endereço remoto.

### Leia os estados, não memorize receitas

```bash
git status
git diff                 # trabalho versus índice
git diff --staged        # índice versus último commit
git show --stat HEAD     # último commit
git log --oneline --graph --decorate --all -10
```

`git add` não significa apenas “adicionar arquivo”; ele copia a versão atual do
conteúdo para o índice. Se você editar depois, pode haver uma parte staged e
outra não staged do mesmo arquivo. Leia os dois diffs.

### Um commit de qualidade

Um bom commit:

- tem uma intenção coerente e pode ser revisado isoladamente;
- não mistura formatação em massa com mudança funcional;
- contém testes/documentação necessários à mudança;
- não contém segredos, arquivos gerados ou caminhos pessoais;
- possui mensagem imperativa que explica o resultado.

Antes de confirmar:

```bash
git status --short
git diff
git diff --staged
```

Depois, rode a verificação do projeto e revise `git show --stat HEAD`.

## 10. Branches, integração e conflitos

Uma branch é um nome móvel apontando para um commit, não uma cópia completa da
pasta. Crie uma linha de trabalho:

```bash
git switch -c feature/resumo-de-linhas
# edite, teste, revise e faça um commit pequeno
git switch main
git merge --no-ff feature/resumo-de-linhas
```

Se o branch principal do laboratório tiver outro nome, veja-o com
`git branch --show-current` e use o nome observado.

Um conflito indica que o Git não sabe combinar duas intenções. O procedimento é:

1. leia `git status` e identifique arquivos conflitantes;
2. abra cada marcador `<<<<<<<`, `=======`, `>>>>>>>`;
3. compreenda as duas mudanças e escreva a versão correta — não escolha um lado
   às cegas;
4. remova todos os marcadores;
5. execute formatação e testes;
6. adicione a resolução ao índice e conclua a operação;
7. leia o commit resultante.

Antes de usar qualquer comando que descarte alterações, faça `git status` e
`git diff`, e preserve o que ainda não está registrado. “Voltar tudo” quase
nunca é a primeira ação correta.

## 11. Diagnóstico sistemático

| Sintoma | Perguntas e verificações |
|---------|--------------------------|
| comando não encontrado | nome correto? `command -v` encontra? runtime instalado? `PATH` esperado? |
| arquivo não encontrado | qual é `pwd`? o caminho é relativo? `ls` confirma nome e maiúsculas? |
| permissão negada | usuário/proprietário/permissões? operação deveria ocorrer ali? |
| saída vazia | dados chegaram em `stdin`? foram para arquivo? programa retornou sucesso? |
| versão errada | qual executável foi escolhido? `--version`? ambiente virtual ativo? |
| Git não inclui mudança | arquivo ignorado? ainda não foi adicionado? está em outro repositório? |
| teste passa no editor, falha no terminal | diretório, comando, runtime e ambiente são os mesmos? |

Registre o comando exato, saída completa, código de retorno, diretório e versão.
Troque apenas uma variável por tentativa. Assim, o diagnóstico vira experimento.

## 12. Erros comuns e por que acontecem

- **Executar tudo como administrador:** mascara permissões incorretas e amplia o
  impacto de qualquer engano.
- **Não usar aspas em caminhos:** o shell divide um valor em vários argumentos.
- **Confundir `>` com `>>`:** o primeiro substitui; o segundo acrescenta.
- **Copiar comandos sem saber o diretório:** caminhos relativos passam a apontar
  para outros arquivos.
- **Adicionar `.env` ao Git:** segredo deixa de ser controlável mesmo após apagar
  do último commit.
- **Fazer `git add .` sem revisar:** arquivos gerados e dados locais podem entrar
  no índice.
- **Um commit com várias intenções:** revisão e reversão ficam arriscadas.
- **Instalar dependência pelo nome:** homônimos e pacotes abandonados podem
  introduzir risco de cadeia de suprimentos.

## 13. Laboratório guiado: ferramenta de resumo versionada

Construa uma pequena ferramenta sem dependência externa:

1. crie `src/resumo.py`, `tests/` e `docs/`;
2. faça o programa ler nomes por `stdin`, ignorar linhas vazias e escrever
   `quantidade=N` em `stdout`;
3. para entrada sem nomes, escreva diagnóstico em `stderr` e termine com código
   `2`;
4. crie testes para dois nomes, nomes com espaços e entrada vazia;
5. documente exemplos de pipe e redirecionamento;
6. registre três commits: estrutura, comportamento e testes/documentação;
7. crie uma branch, altere o formato da saída e integre-a após os testes;
8. produza `docs/evidencia.md` com versões, comandos e resultados — nunca com
   dados pessoais.

### Critérios de aceite

- a mesma entrada produz a mesma saída;
- `stdout` contém somente o resultado consumível;
- mensagens humanas de falha vão para `stderr`;
- códigos de sucesso e erro são diferentes e documentados;
- `git status --short` fica vazio ao terminar;
- cada commit possui uma intenção e seu diff pode ser explicado;
- nenhum arquivo contém segredo, caminho pessoal ou dado real.

## 14. Exercícios graduais

### Nível 1 — reconhecer

1. Explique, sem executar, o resultado de `pwd`, `cd ..` e `pwd`.
2. Preveja quantos argumentos existem em `printf '%s\n' "a b" c`.
3. Explique a diferença entre saída normal, diagnóstico e código de retorno.
4. Desenhe as três áreas locais do Git e situe `git diff --staged`.

### Nível 2 — aplicar

1. Leia um arquivo com cinco linhas por redirecionamento e grave o resumo em
   outro arquivo.
2. Faça um teste falhar, use breakpoint para observar a causa e registre a
   hipótese antes de corrigir.
3. Crie `.gitignore` adequado a uma linguagem e justifique cada padrão.
4. Faça dois commits independentes e explique por que não deveriam ser um só.

### Nível 3 — integrar

1. Crie uma ferramenta que recebe `--formato texto|json`, dados por `stdin` e
   retorna códigos diferentes para argumento inválido e entrada inválida.
2. Execute-a diretamente, por pipe e com arquivos redirecionados; documente os
   três fluxos.
3. Produza intencionalmente um conflito apenas no repositório descartável,
   resolva-o pelo significado e escreva um teste que preserve a decisão.
4. Reproduza o projeto em um novo diretório usando apenas os arquivos
   versionados e o README.

## Critério de conclusão do capítulo

Marque apenas quando conseguir demonstrar:

- [ ] Sei prever como o shell separará argumentos com e sem aspas.
- [ ] Sei explicar `stdin`, `stdout`, `stderr` e código de retorno com um exemplo.
- [ ] Diagnostico caminhos e runtimes usando evidência, não tentativa aleatória.
- [ ] Uso privilégios mínimos e não salvo segredos no repositório.
- [ ] Sei inspecionar diretório de trabalho, índice e histórico separadamente.
- [ ] Consigo formar commits pequenos e resolver um conflito simples.
- [ ] Um colega consegue executar meu projeto somente com a documentação.
- [ ] Consigo usar teste e depurador para confirmar uma hipótese.

## Conexão com os próximos capítulos

O ambiente agora deixa de ser uma variável invisível. Em
[Fundamentos comuns às linguagens](03-fundamentos-comuns.md), você usará essa
base para comparar tipos, controle de fluxo, funções, memória, erros e módulos.
Depois, em [Estruturas de dados e algoritmos](04-estruturas-dados-algoritmos.md),
medirá soluções reproduzíveis, e em
[Engenharia de software](05-engenharia-software.md) transformará Git, testes e
automação em um processo de entrega.
