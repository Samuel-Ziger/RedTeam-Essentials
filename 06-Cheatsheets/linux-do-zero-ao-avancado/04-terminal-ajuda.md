# 04 — Terminal, shell e documentação

## Objetivos

- distinguir terminal, shell, builtin, função, alias e programa externo;
- prever parsing, expansão, quoting e divisão de argumentos;
- encontrar documentação local e interpretar synopsis e código de saída;
- executar comandos com nomes hostis sem transformar dados em opções.

## Terminal não é shell

O emulador de terminal exibe caracteres e transmite entrada. A shell interpreta
uma linguagem, expande argumentos e inicia programas. Bash, Dash, Zsh e Fish
não são idênticas. Um script com `#!/bin/sh` deve obedecer à shell POSIX do
sistema; recursos exclusivos de Bash exigem `#!/usr/bin/env bash` ou um caminho
definido pela política do ambiente.

```bash
printf 'terminal=%s shell=%s\n' "${TERM:-desconhecido}" "$SHELL"
ps -p "$$" -o comm=
readlink -f /bin/sh
```

`$SHELL` costuma indicar a shell de login configurada, não necessariamente o
processo que interpreta o comando atual.

## Estrutura de um comando

```text
comando [opções] [operandos...]
```

```bash
ls -l --time-style=long-iso -- /etc/hosts
```

`--` encerra opções e permite tratar um nome iniciado por `-` como operando.
Nem todo programa segue as convenções GNU; consulte seu manual.

## Como a shell encontra comandos

```bash
type -a printf
command -V ls
printf '%s\n' "$PATH" | tr ':' '\n'
command -v python3
```

A ordem conceitual envolve sintaxe reservada, aliases, funções, builtins,
cache e busca em `PATH`, com detalhes dependentes da shell. Não coloque `.` no
início de `PATH`: isso permite que um arquivo no diretório atual substitua um
comando esperado.

## Quoting e expansões

```bash
nome='Ana Silva'
printf '<%s>\n' "$nome"       # um argumento
printf '<%s>\n' $nome         # dois argumentos: evite
printf '%s\n' '*.log'         # texto literal
printf '%s\n' ./*.log         # glob, se houver correspondência
printf '%s\n' "$HOME"         # expansão de variável
printf '%s\n' 'valor=$HOME'   # literal
```

Aspas simples preservam tudo literalmente. Aspas duplas permitem expansões
como `$variavel` e `$(comando)`, mas impedem separação em palavras e glob.
Variáveis que contêm caminho ou entrada devem quase sempre ser expandidas entre
aspas duplas.

## Histórico e atalhos

- `Ctrl-C`: envia interrupção ao job em primeiro plano.
- `Ctrl-D`: indica fim de entrada; numa shell vazia pode encerrar a sessão.
- `Ctrl-Z`: suspende o job; não o encerra.
- `Ctrl-R`: pesquisa histórico em Bash/readline.
- `Ctrl-L`: limpa a tela visualmente.
- Tab: completa comandos e caminhos.

Não digite segredo diretamente na linha de comando quando outra interface
segura existir: argumentos podem aparecer em histórico, logs ou listagem de
processos.

## Documentação local

```bash
man man
man 1 printf
man 2 open
man 5 passwd
man 7 signal
apropos 'copy files'
whatis chmod
info coreutils 'cp invocation' 2>/dev/null
help printf                    # builtin Bash
```

Seções comuns de manual:

| Seção | Conteúdo |
|---------|----------|
| 1 | comandos de usuário |
| 2 | chamadas de sistema |
| 3 | funções de biblioteca |
| 4 | dispositivos |
| 5 | formatos e configurações |
| 7 | convenções e visões gerais |
| 8 | administração do sistema |

Dentro do `man`, use `/texto`, `n`, `N`, `g`, `G` e `q`. Procure primeiro
`SYNOPSIS`, `DESCRIPTION`, `OPTIONS`, `EXIT STATUS`, `FILES` e `SEE ALSO`.

## Saída e código de retorno

Por convenção, zero indica sucesso e valor não zero indica alguma classe de
falha, mas o significado exato pertence ao programa.

```bash
test -r /etc/hosts
status=$?
printf 'status=%d\n' "$status"

if command -v git >/dev/null 2>&1; then
    git --version
else
    printf '%s\n' 'git não está instalado' >&2
fi
```

`stdout` transporta resultado; `stderr` transporta diagnóstico. Separá-los
permite compor ferramentas sem misturar dados com mensagens.

## TTY, sessões e multiplexação

```bash
tty
w
stty -a
```

`tmux` ou `screen` mantêm sessões e múltiplos painéis, úteis em administração
remota. Eles não substituem logs nem execução supervisionada por systemd.

## Exercícios

1. Descubra se `test`, `printf` e `time` são builtins, externos ou ambos.
2. Crie arquivos chamados `normal` e `-n`; leia o segundo usando `--`.
3. Compare `man 1 printf` com `help printf`.
4. Demonstre, em diretório temporário, a diferença entre `"*.txt"` e
   `./*.txt`.
5. Execute um comando inexistente e investigue o status retornado.

## Checklist de domínio

Você deve conseguir decompor um comando em argumentos, prever expansões,
encontrar a documentação correta e preservar stdout, stderr e status.
