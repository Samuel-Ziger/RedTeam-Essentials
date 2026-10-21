# 02 — Configuração, ambientes e segredos

Configuração é comportamento que pode variar entre execuções sem alterar o
código. Quando a aplicação lê valores de várias fontes sem uma política clara,
surge o erro clássico: “na minha máquina funciona”. Neste capítulo, o Study Desk
ganha uma configuração tipada, rastreável e segura, sem transformar segredo em
preferência comum.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- separar configuração, dado persistente, cache e segredo;
- definir e implementar precedência determinística entre fontes;
- distinguir ausência, valor vazio, valor padrão e valor inválido;
- converter texto em um objeto tipado antes de executar casos de uso;
- explicar a origem efetiva de cada opção sem revelar valores sensíveis;
- testar configuração por tabela, inclusive combinações de fontes.

## Pré-requisitos

Use a separação arquitetural do capítulo 00 e a CLI do capítulo 01. Você deve
conhecer tipos, funções puras, tratamento de erros e dicionários/mapas. Este
capítulo não ensina administração de ambientes nem detalhes de sistemas
operacionais; o foco é o contrato da aplicação.

## Modelo mental: coletar, resolver, converter, validar

Não espalhe leituras de variável ou arquivo por todo o programa. Construa a
configuração uma vez na borda:

```text
fontes brutas -> precedência -> valores efetivos -> parsing -> validação cruzada
             -> AppConfig imutável -> aplicação
```

As quatro etapas têm responsabilidades distintas:

1. **coleta:** obtém texto de fontes autorizadas;
2. **resolução:** escolhe qual fonte vence para cada chave;
3. **conversão:** transforma texto em inteiro, enum, caminho ou duração;
4. **validação:** verifica limites individuais e combinações.

Depois disso, o núcleo recebe um objeto completo. Nenhum caso de uso chama
`getenv` ou procura um arquivo por conta própria.

## Classifique antes de armazenar

Nem todo valor variável é a mesma coisa:

| Categoria | Exemplo | Propriedade principal |
|---|---|---|
| configuração | idioma, formato padrão | comportamento escolhido |
| dado | sessões registradas | deve sobreviver e ser recuperável |
| cache | resultado derivado | pode ser descartado e reconstruído |
| segredo | token de integração futura | exposição deve ser minimizada |
| estado de execução | comando atual | vida curta, não é configuração |

Guardar sessões no arquivo de configuração dificulta backup e migração.
Guardar token ao lado do tema trata risco como preferência. Nomear corretamente
a categoria ajuda a escolher ciclo de vida e proteção.

## Precedência explícita

Uma política comum para o Study Desk:

```text
argumento CLI > variável de ambiente > arquivo do usuário > padrão seguro
```

Essa ordem não é universal; ela é uma decisão do produto. Opções explícitas da
invocação normalmente vencem, enquanto o arquivo guarda preferências duráveis.
A origem deve acompanhar o valor:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

T = TypeVar("T")


class Source(Enum):
    CLI = "cli"
    ENVIRONMENT = "environment"
    FILE = "file"
    DEFAULT = "default"


@dataclass(frozen=True)
class Resolved(Generic[T]):
    value: T
    source: Source


def resolve(cli: T | None, env: T | None, file: T | None, default: T) -> Resolved[T]:
    for value, source in (
        (cli, Source.CLI),
        (env, Source.ENVIRONMENT),
        (file, Source.FILE),
    ):
        if value is not None:
            return Resolved(value, source)
    return Resolved(default, Source.DEFAULT)
```

Não use `cli or env or default` quando `""`, `0` ou `false` podem ter significado.
**Ausente** quer dizer “esta fonte não opinou”. **Vazio** é um valor presente,
que deve ser aceito ou rejeitado segundo o contrato.

## Configuração tipada e imutável

No núcleo, não passe mapas de strings. Modele as escolhas permitidas:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class AppConfig:
    data_file: Path
    output_format: Literal["text", "json"]
    default_limit: int
    locale: str

    def __post_init__(self) -> None:
        if not 1 <= self.default_limit <= 1000:
            raise ValueError("default_limit deve estar entre 1 e 1000")
        if self.output_format not in ("text", "json"):
            raise ValueError("output_format deve ser text ou json")
        if not self.locale.strip():
            raise ValueError("locale não pode ser vazio")
```

O pipeline transforma `"30"` em inteiro e valida o intervalo antes de criar o
objeto. Não faça fallback para o padrão quando uma fonte explicitou `"muitos"`:
isso esconderia um erro de operação.

Um erro de configuração precisa informar chave, origem e expectativa:

```text
Configuração inválida: STUDYDESK_DEFAULT_LIMIT, origem environment.
Esperado: inteiro entre 1 e 1000. Corrija o valor e execute novamente.
```

Para segredo, omita o valor. Para configuração não sensível, ainda prefira uma
mensagem resumida para evitar vazamento acidental de caminhos ou dados pessoais.

## Validação cruzada e falha atômica

Campos individualmente válidos podem formar uma combinação inválida. Exemplo:
`--format json` e `--interactive` podem ser incompatíveis porque prompts
contaminariam a saída de máquina. Valide depois de construir o candidato completo
e antes de iniciar efeitos.

O contrato de inicialização é:

- ou a configuração inteira é válida e a aplicação inicia;
- ou a aplicação relata todos os erros independentes que consegue coletar e não
  executa o comando;
- nunca existe um objeto parcialmente válido circulando pelo núcleo.

Coletar vários erros melhora a experiência, mas não continue validações
dependentes de um parsing que falhou.

## Arquivos, localização e caminho explícito

Configuração editável, dados, cache e diagnóstico possuem destinos conceituais
distintos. Use bibliotecas apropriadas da plataforma para descobrir locais;
não concatene um diretório pessoal manualmente. Ao mesmo tempo, aceite caminho
explícito para teste, uso portátil e recuperação:

```text
studydesk --config caminho/config.json --data-file caminho/studies.json list
```

Um caminho relativo deve ter base documentada. Resolva-o uma vez e preserve a
forma normalizada no diagnóstico. Não deixe cada componente interpretar a base de
modo diferente.

Ao analisar documento de configuração:

- limite tamanho e profundidade;
- valide encoding e schema;
- decida se chave desconhecida é erro ou aviso;
- não interprete conteúdo como código;
- não carregue automaticamente arquivo encontrado em diretório inesperado.

## Segredo não é configuração comum

O Study Desk local não precisa de segredo em sua primeira versão. Essa ausência
é uma boa decisão: não invente token para parecer “profissional”. Se uma futura
integração exigir credencial:

- não grave no repositório, exemplo ou pacote;
- não passe em argumento de processo;
- não inclua em log, stack trace ou pacote de diagnóstico;
- use mecanismo de credenciais ou secret manager apropriado;
- limite escopo e duração;
- planeje rotação, revogação e remoção;
- nunca devolva o segredo em comando `config show`.

Variável de ambiente pode ser um canal de injeção, mas não se torna cofre por
isso. Pode aparecer em diagnósticos, processos filhos ou ferramentas. O modelo de
ameaça e o ambiente decidem a solução.

## Perfis e ambientes sem booleanos mágicos

Evite `if production` espalhado. Um nome de perfil deve selecionar valores que,
depois, formam um `AppConfig` comum. O núcleo trabalha com timeout, diretório e
nível de diagnóstico, não com um rótulo misterioso.

Não desligue validações em um perfil supostamente “confiável”. Não faça fallback
silencioso para dados reais quando um perfil de demonstração está incompleto.
Ambiente deve alterar endereços ou integrações, não invariantes do domínio.

## `.env`: conveniência, não cofre

Um arquivo `.env` pode simplificar desenvolvimento local. Forneça apenas
`.env.example` com nomes e valores falsos, mantenha o real fora do versionamento
e defina se ele é carregado explicitamente. Não o copie para artefatos. Um valor
presente em `.env`, ambiente e CLI precisa obedecer à mesma precedência.

## Diagnóstico com proveniência

Um comando `config explain` pode mostrar:

```text
data_file       = <caminho resumido>   source=cli
output_format   = json                 source=file
default_limit   = 20                   source=default
integration_key = <configured>         source=credential-store
```

Ele mostra presença e origem de segredo, nunca valor. Para investigar uma
configuração inesperada:

1. reproduza com fontes controladas;
2. liste chaves e origens efetivas;
3. remova fontes de maior precedência uma por vez;
4. teste parsing e validação isoladamente;
5. confirme que o objeto final é o passado ao caso de uso.

| Sintoma | Hipótese | Teste direcionado |
|---|---|---|
| CLI não vence arquivo | ordem invertida | tabela com duas fontes presentes |
| `false` vira padrão | uso de truthiness | caso explícito com `false` |
| erro aparece tarde | parsing ficou no caso de uso | teste inicialização sem efeitos |
| segredo aparece no log | objeto inteiro foi serializado | teste com sentinela secreta |
| teste usa preferência real | fonte global oculta | injete mapa e caminho temporários |

## Exercícios em três níveis

### Nível 1 — resolução

Implemente `resolve` em duas linguagens e construa uma tabela cobrindo ausência,
string vazia, zero, `false` e as quatro fontes.

**Critérios de aceite:** todas as combinações relevantes têm resultado e origem;
valor inválido não é confundido com ausência; a ordem está documentada.

### Nível 2 — configuração tipada

Crie `AppConfig` para arquivo de dados, formato, limite e idioma do Study Desk.
Leia mapas fornecidos pelo teste, sem depender do ambiente real.

**Critérios de aceite:** conversão ocorre na borda; objeto final é imutável;
erros citam chave/origem; nenhuma operação é executada com config parcial.

### Nível 3 — segurança e diagnóstico

Implemente `config explain`, adicione uma credencial falsa e testes de não
exposição em saída, exceção e serialização. Modele uma regra cruzada.

**Critérios de aceite:** a sentinela secreta não aparece em nenhuma captura; a
origem ainda é visível; combinação inválida falha antes de ler ou gravar dados.

## Checklist de domínio

- [ ] Distingo configuração, dado, cache, segredo e estado de execução.
- [ ] Defino precedência e preservo a origem do valor efetivo.
- [ ] Não confundo ausência com vazio, zero ou `false`.
- [ ] Converto e valido antes de construir uma configuração imutável.
- [ ] Valido combinações e impeço inicialização parcial.
- [ ] Consigo explicar configuração efetiva sem expor segredos.
- [ ] Não trato `.env` ou variável de ambiente como cofre universal.
- [ ] Testo todas as fontes sem depender da configuração real da máquina.
