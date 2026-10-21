# 01 — Interfaces de linha de comando profissionais

Uma CLI é ao mesmo tempo interface para pessoas e contrato para automação.
Ela precisa ser descobrível, previsível, componível e compatível entre versões.
Neste capítulo, a primeira fatia vertical do Study Desk ganha comandos reais sem
misturar parsing, regra de negócio e formatação de saída.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- projetar comandos, subcomandos, argumentos e opções coerentes;
- separar `stdout`, `stderr` e código de saída;
- produzir saída humana e saída estruturada a partir do mesmo resultado;
- tratar TTY, prompts, cores e confirmações sem quebrar automação;
- definir compatibilidade e depreciação de um contrato de CLI;
- testar comportamento observável sem acoplar o teste ao parser.

## Pré-requisitos

Você precisa dominar funções, listas, dicionários, tratamento de erros e testes
básicos. Do capítulo 00, reutilizaremos `StudySession`, a separação entre
apresentação e caso de uso e as invariantes de título e duração.

## Modelo mental: protocolo textual de duas audiências

Uma pessoa tolera espaços e cores; um script precisa de estrutura estável. Trate
a CLI como um pequeno protocolo:

```text
argv -> parser -> comando tipado -> caso de uso -> resultado tipado
     -> apresentador humano ou JSON -> stdout/stderr + exit code
```

O parser traduz sintaxe. Ele não deve salvar dados, gerar identificadores ou
decidir invariantes. O apresentador traduz o resultado; ele não deve repetir
regra de domínio.

## Anatomia e gramática

```text
studydesk add --title "Grafos" --minutes 45 --format json
^         ^   ^       ^        ^         ^
programa  ação opção   valor    opção     valor
```

Use subcomandos para capacidades, opções para modificar comportamento e
argumentos posicionais apenas quando a ordem for natural e inequívoca. Um
contrato inicial do Study Desk:

```text
studydesk add --title TEXT --minutes INT [--format text|json]
studydesk list [--format text|json] [--limit INT]
studydesk export --output PATH [--force]
studydesk --help
studydesk --version
```

Prefira nomes longos claros; atalhos curtos só para ações frequentes. Evite uma
opção booleana cujo significado se inverte em combinação com outra. Defina se
opção repetida é erro, acumula valores ou usa o último valor. Defina também o
papel de `--`, que encerra opções e permite um valor iniciado por hífen.

## Ajuda é parte do produto

Uma boa ajuda deve funcionar sem configuração, dados ou efeitos externos e
conter:

- uma frase de propósito;
- sintaxe geral e subcomandos;
- opções, tipos, padrões e unidades;
- exemplos copiáveis, inclusive um caso com JSON;
- formatos de saída e códigos de saída;
- localização conceitual da configuração;
- versão e canal de suporte.

`--help` retorna sucesso e não executa a ação. Um erro de uso mostra resumo
curto e indica `--help`, mas não despeja uma página inteira inesperadamente.
Exemplos na ajuda também podem virar testes de documentação.

## Parsing sem acoplamento

Prefira bibliotecas maduras: `argparse` em Python, `util.parseArgs` em Node.js,
uma biblioteca adequada em Java ou C#, e `getopt` quando o contrato em C for
compatível. Parser manual cresce ao lidar com opções agrupadas, `--`, Unicode,
valores opcionais e mensagens consistentes.

Em Python, traduza `Namespace` para um comando imutável:

```python
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class AddCommand:
    title: str
    minutes: int
    output_format: Literal["text", "json"]


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="studydesk", description="Registra estudos locais")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="registra uma sessão")
    add.add_argument("--title", required=True)
    add.add_argument("--minutes", required=True, type=int)
    add.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def to_command(args: Namespace) -> AddCommand:
    if args.command != "add":
        raise ValueError("comando não suportado")
    return AddCommand(args.title, args.minutes, args.format)
```

`type=int` resolve apenas parsing. O intervalo 1..1440 continua sendo invariante
do domínio. Assim, uma futura GUI e uma importação obedecerão à mesma regra.

## Entrada, saída e códigos

Os três canais observáveis têm papéis diferentes:

- `stdout`: resultado solicitado, adequado a redirecionamento ou pipe;
- `stderr`: diagnóstico, aviso e progresso;
- código de saída: categoria estável do resultado.

Política do curso:

| Código | Significado | Exemplo |
|---:|---|---|
| 0 | sucesso | sessão criada |
| 2 | sintaxe ou entrada inválida | `--minutes abc` |
| 3 | conflito | revisão de dados mudou |
| 4 | dado ausente | sessão solicitada não existe |
| 10 | falha interna ou de persistência | arquivo não pôde ser atualizado |

Não use um código diferente para cada frase; use categorias que o consumidor
pode tratar. Documente-as e teste-as.

```bash
if output=$(studydesk list --format json 2>diagnostico.log); then
  printf '%s\n' "$output"
else
  status=$?
  printf 'studydesk falhou (código %s)\n' "$status" >&2
fi
```

O teste captura saída sem confundi-la com diagnóstico. Evite analisar o texto
humano para automação; ele pode mudar para melhorar clareza ou tradução.

## Um resultado, dois apresentadores

O caso de uso deve retornar dados, não imprimir. Exemplo em JavaScript:

```javascript
function present(result, format) {
  if (format === "json") {
    return JSON.stringify({
      schemaVersion: 1,
      id: result.id,
      title: result.title,
      minutes: result.minutes
    });
  }
  return `Sessão ${result.id} registrada: ${result.title} (${result.minutes} min)`;
}
```

No modo JSON, escreva somente um documento válido em `stdout`: sem spinner,
banner, ANSI ou aviso antes do `{`. Números devem continuar números; não produza
`"minutes": "45 min"`. Inclua versão do schema quando consumidores externos
dependem dele.

## Interatividade e automação

Uma CLI não deve abrir prompt quando entrada ou saída não é terminal, nem quando
`--non-interactive` foi solicitado. Para uma substituição destrutiva:

```text
terminal interativo + sem --force -> pedir confirmação
não interativo + sem --force      -> falhar sem alterar nada
com --force                        -> executar o contrato documentado
```

Não interprete “ausência de resposta” como consentimento. `--yes` ou `--force`
deve ser explícito e ter escopo claro. Outros sinais de automação amigável:

- ordem determinística de itens;
- animação e progresso apenas quando apropriados;
- cores desativáveis e nunca como única informação;
- modo silencioso que ainda relata falhas;
- resultado parcial marcado como parcial;
- tratamento de cancelamento sem gravar estado incompleto.

## Contratos e invariantes da CLI

Para `studydesk add`:

- `--title` e `--minutes` aparecem exatamente uma vez;
- parsing inválido não chama o caso de uso;
- falha do domínio não altera o repositório;
- sucesso em texto e JSON representa a mesma sessão;
- JSON válido não é contaminado por logs;
- o código de saída corresponde à categoria documentada;
- `--help` e `--version` não leem nem modificam dados.

Essas regras são testáveis invocando a função principal com vetores de argumentos
e fluxos em memória. Poucos testes ponta a ponta devem executar o processo real
para confirmar canais e códigos.

## Compatibilidade e evolução

Nome de opção, significado, valor padrão, campo JSON, ordenação prometida e
código de saída podem ser API pública. Para renomear `--duration` para
`--minutes`:

1. aceite ambos por um período;
2. rejeite o uso simultâneo se for ambíguo;
3. anuncie depreciação em `stderr`, nunca dentro do JSON;
4. atualize ajuda e exemplos para a forma nova;
5. teste ambas as formas durante a janela;
6. remova apenas em versão incompatível anunciada.

Adicionar campo JSON pode quebrar consumidores estritos. Defina se consumidores
devem ignorar campos desconhecidos e mantenha tipo e semântica dos existentes.

## Falhas comuns e diagnóstico

| Sintoma | Causa provável | Verificação |
|---|---|---|
| JSON não pode ser analisado | aviso ou cor vazou em `stdout` | capture canais separadamente |
| comando trava em pipeline | abriu prompt sem TTY | simule fluxos não interativos |
| `--help` falha sem arquivo | inicialização ocorreu antes do parsing | espione o repositório |
| código sempre é 1 | categorias não foram mapeadas | teste tabela erro→código |
| saída muda entre execuções | coleção sem ordenação contratada | use fixture e compare bytes |
| teste quebra por texto traduzido | automação depende de texto humano | valide JSON e categoria |

Para diagnosticar, reduza a invocação, capture `argv`, `stdout`, `stderr` e
código separadamente, e substitua o caso de uso por um falso determinístico. Isso
revela se a divergência está no parser, despacho ou apresentador.

## Exercícios em três níveis

### Nível 1 — contrato

Especifique uma CLI de lista de tarefas com três subcomandos, ajuda, tabela de
códigos e exemplos de texto/JSON.

**Critérios de aceite:** cada argumento tem tipo, obrigatoriedade e padrão; os
canais estão definidos; `--help` e erro de uso têm comportamentos diferentes.

### Nível 2 — implementação

Implemente `studydesk add` e `list` com repositório em memória. Teste opção
ausente, desconhecida, repetida, valor depois de `--`, texto e JSON.

**Critérios de aceite:** parsing não contém regra de duração; saída JSON é
analisável; erros vão para `stderr`; execução repetida tem ordem determinística.

### Nível 3 — compatibilidade

Adicione `export --output`, recusando sobrescrita sem confirmação. Planeje e
implemente a depreciação de uma opção, com modo não interativo.

**Critérios de aceite:** cancelamento e recusa não alteram arquivo; pipeline não
trava; forma antiga emite aviso apenas em `stderr`; testes documentam a janela de
compatibilidade.

## Checklist de domínio

- [ ] Distingo subcomando, opção, argumento e marcador `--`.
- [ ] Minha ajuda permite descobrir a tarefa sem consultar o código.
- [ ] Separo resultado, diagnóstico e categoria nos três canais da CLI.
- [ ] Produzo texto e JSON a partir do mesmo objeto de resultado.
- [ ] Evito prompts, cores e animações quando não são apropriados.
- [ ] Testo parser sem executar efeitos e efeitos sem depender do parser.
- [ ] Reconheço campos JSON e códigos de saída como contratos versionados.
- [ ] Sei localizar uma falha em parsing, despacho, caso de uso ou apresentação.
