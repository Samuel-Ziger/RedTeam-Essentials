# 09 — Design modular e dependências

Dividir um programa em arquivos não o torna modular. Modularidade existe quando
cada parte tem uma responsabilidade compreensível, protege suas decisões e se
comunica por um contrato menor e mais estável que sua implementação. O objetivo
não é obter o maior número de camadas: é permitir que uma mudança previsível
atinja poucos lugares e que uma falha tenha um dono identificável.

## Objetivos verificáveis

Ao final, você deverá conseguir:

- medir coesão e acoplamento a partir de razões reais de mudança;
- desenhar fronteiras que preservem invariantes, em vez de apenas getters;
- diferenciar dependência de código, fluxo de execução e fluxo de dados;
- definir portas na linguagem do consumidor e adaptadores para mecanismos;
- montar todas as dependências em uma **composition root** explícita;
- detectar ciclos, dependências transitivas indevidas e abstrações vazias;
- trocar JSON por memória ou banco sem editar a política do planejador;
- justificar quando uma função simples é melhor que uma nova interface.

Pré-requisitos: funções, módulos, objetos, exceções, grafos e testes de unidade.
Use o [Dependency Planner](projetos/dependency-planner/README.md) como laboratório.

## Modelo mental: decisões que mudam juntas

Um módulo deve esconder uma decisão. O algoritmo de ordenação topológica muda
quando a política de planejamento muda; o parser muda quando o formato externo
muda; a CLI muda quando a experiência do terminal muda. Essas são três razões
de mudança e, portanto, três fronteiras naturais.

**Coesão** é a proximidade entre as responsabilidades de uma unidade. Um módulo
coeso tem uma frase curta como propósito e seus elementos tendem a mudar juntos.
**Acoplamento** é o conhecimento que uma unidade precisa ter sobre outra. Quanto
mais detalhes, ordem de chamadas e estados internos um consumidor conhece, mais
cara é a mudança.

Uma heurística útil é completar estas frases:

```text
Este módulo existe para ____________________.
Ele muda quando ____________________________.
Seus consumidores precisam saber apenas ____.
Ele não decide _____________________________.
```

Se a primeira frase precisa de vários “e”, a coesão provavelmente é baixa. Se a
terceira enumera tabelas, campos privados, sequência de chamadas e biblioteca,
o contrato provavelmente vaza implementação.

### Invariantes de uma boa fronteira

Uma fronteira modular saudável procura manter:

1. o domínio pode executar sem framework, arquivo, rede ou banco;
2. estados inválidos são rejeitados por quem possui a regra;
3. dependências obrigatórias aparecem na construção do componente;
4. o mecanismo externo é traduzido uma vez na borda;
5. uma troca de mecanismo não altera o significado da política;
6. erros atravessam a fronteira em termos que o consumidor entende.

São metas verificáveis. Por exemplo, se o teste do caminho crítico precisa criar
um arquivo temporário, a primeira invariante foi violada.

## Encapsulamento protege comportamento

Encapsular não é tornar campos privados e gerar setters para todos. É impedir
transições que quebram as regras do objeto.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Tarefa:
    id: str
    duracao: int
    dependencias: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.id or self.id != self.id.strip():
            raise ValueError("id vazio ou com espaco externo")
        if any(not dep or dep != dep.strip() for dep in self.dependencias):
            raise ValueError("dependencia vazia ou com espaco externo")
        if self.duracao <= 0:
            raise ValueError("duracao deve ser positiva")
        if self.id in self.dependencias:
            raise ValueError("tarefa nao pode depender de si mesma")
        if len(set(self.dependencias)) != len(self.dependencias):
            raise ValueError("dependencia duplicada")
```

O objeto garante invariantes locais. A existência de cada dependência e a
ausência de ciclos envolvem várias tarefas; pertencem ao agregado ou serviço que
enxerga o grafo inteiro. Colocar tudo no construtor de `Tarefa` seria impossível,
pois ele não possui o conjunto completo.

Compare:

```text
ruim: tarefa.dependencias.append(id)
frágil: tarefa.set_dependencias(lista_sem_validacao)
bom: plano.adicionar_dependencia(origem, destino)
     -> valida existência, duplicata e ciclo conforme o contrato
```

Encapsulamento também define propriedade. Uma coleção devolvida diretamente
pode permitir alteração externa silenciosa. Use cópia, visão somente leitura ou
valor imutável conforme o custo. Copiar sempre uma lista de milhões de itens não
é gratuito; a decisão precisa considerar volume e frequência.

## Dependência de código não é fluxo de execução

No planejador, a CLI chama o caso de uso, que chama um repositório JSON. O fluxo
de execução segue para fora, mas o núcleo não precisa importar JSON:

```text
fluxo de chamada
CLI -> PlanejarProjeto -> JsonTaskRepository -> sistema de arquivos

dependência de código
CLI -> aplicação -> domínio
                   ^
adaptador JSON ----|  (implementa a porta definida para a aplicação)
```

A seta de dependência aponta para a política mais estável. Isso não significa
que “o domínio depende da infraestrutura ao contrário”; significa que ambos
dependem de um contrato expresso na linguagem da política.

### Porta orientada ao consumidor

Defina apenas o que o caso de uso precisa:

```python
from collections.abc import Sequence
from typing import Protocol


class LeitorDeTarefas(Protocol):
    def listar(self) -> Sequence[Tarefa]: ...


class PlanejarProjeto:
    def __init__(self, leitor: LeitorDeTarefas) -> None:
        self._leitor = leitor

    def executar(self) -> tuple[str, ...]:
        tarefas = self._leitor.listar()
        return ordenar_dependencias(tarefas)
```

Não exponha `execute_sql`, `find_document` ou `read_json`. Esses nomes fazem o
caso de uso conhecer o mecanismo. `listar` expressa sua necessidade. Tampouco
crie uma interface CRUD gigante se ele só lê: isso viola a segregação por
consumidor e aumenta implementações falsas.

Um adaptador realiza a tradução anticorrupção:

```python
import json
from pathlib import Path


class LeitorJson:
    def __init__(self, caminho: Path) -> None:
        self._caminho = caminho

    def listar(self) -> tuple[Tarefa, ...]:
        documento = json.loads(self._caminho.read_text(encoding="utf-8"))
        return tuple(
            Tarefa(
                id=item["id"],
                duracao=item["duration"],
                dependencias=tuple(item["dependencies"]),
            )
            for item in documento["items"]
        )
```

Em produção, valide schema, campos desconhecidos, limites e erros com contexto,
como faz o adaptador real em
[repository.py](projetos/dependency-planner/src/dependency_planner/repository.py).
O dicionário externo não deve atravessar a borda: se `duration` mudar de nome,
apenas o adaptador muda.

## Composition root: onde o concreto é escolhido

Injeção de dependência é fornecer uma colaboração de fora. A **composition
root** é o único lugar responsável por escolher e montar implementações reais.
Para uma CLI pequena, ela pode estar em `main`:

```python
def main(argv: list[str]) -> int:
    opcoes = parsear_argumentos(argv)
    leitor = LeitorJson(opcoes.arquivo)
    caso_de_uso = PlanejarProjeto(leitor)
    plano = caso_de_uso.executar()
    imprimir(plano, formato=opcoes.formato)
    return 0
```

Criar `LeitorJson` dentro de `PlanejarProjeto.executar` esconderia uma
dependência obrigatória, acoplaria política a arquivo e forçaria I/O em todos os
testes. Um container de injeção pode automatizar a montagem de sistemas grandes,
mas não substitui um grafo de dependências compreensível. Para um projeto
pequeno, construtores explícitos são mais fáceis de rastrear.

### Teste da substituição

```python
class LeitorEmMemoria:
    def __init__(self, tarefas: tuple[Tarefa, ...]) -> None:
        self._tarefas = tarefas

    def listar(self) -> tuple[Tarefa, ...]:
        return self._tarefas


def test_planeja_sem_arquivo() -> None:
    tarefas = (
        Tarefa("modelo", 2, ()),
        Tarefa("api", 3, ("modelo",)),
    )
    assert PlanejarProjeto(LeitorEmMemoria(tarefas)).executar() == (
        "modelo",
        "api",
    )
```

O fake não imita detalhes de JSON; implementa o contrato sem I/O. Ainda é
necessário um teste de integração do adaptador real, pois o fake não prova
encoding, permissões, parsing nem validação do documento.

## API pública de um módulo

Uma API de módulo saudável:

- usa nomes do domínio e tipos que deixam ausência e erro explícitos;
- mantém pequena a superfície pública;
- documenta mutabilidade, ordenação, complexidade e ownership;
- valida pré-condições ou declara claramente quem as garante;
- não oferece vários caminhos equivalentes para a mesma operação;
- evita retornar estruturas internas mutáveis;
- evolui por compatibilidade deliberada, não por acidente.

Considere `planejar(tarefas) -> Plano`. Retornar um objeto nomeado permite
acrescentar lotes, duração e caminho crítico sem uma tupla posicional misteriosa.
Mas criar `Request`, `Response`, `Manager`, `Provider` e `Facade` para devolver
uma lista acrescenta cerimônia sem proteger decisão alguma.

Evite `utils`, `helpers` e `common` como depósitos. Se três funções calculam
duração, folga e caminho crítico, o conceito pode ser `cronograma`. Se uma
função só serve ao parser JSON, ela pertence ao adaptador JSON.

## Organização: por capacidade ou por camada

Em um sistema pequeno, estes arquivos podem ser claros:

```text
dependency_planner/
  domain.py
  graph.py
  ports.py
  service.py
  repository.py
  cli.py
```

Quando o sistema cresce, pastas globais `controllers/`, `services/` e
`repositories/` espalham uma mudança por toda a árvore. Agrupar por capacidade
mantém o que muda junto:

```text
planning/
  domain.py
  use_cases.py
  adapters.py
reporting/
  domain.py
  use_cases.py
  adapters.py
```

Não há estrutura universal. A pergunta é: “para acrescentar uma regra de
planejamento, quantos conceitos não relacionados preciso abrir?”. Mudar cedo
demais para uma árvore profunda também custa navegação.

## Dependências cíclicas e estabilidade

Se `planning` importa `reporting` e `reporting` importa `planning`, nenhum pode
ser entendido, testado ou publicado isoladamente. Soluções possíveis:

1. mover a regra para o módulo que de fato a possui;
2. extrair um contrato pequeno para o lado mais estável;
3. fazer um orquestrador superior coordenar ambos;
4. publicar um evento quando a relação não exige resposta imediata.

Não extraia automaticamente `shared`. Um terceiro módulo genérico pode apenas
esconder o ciclo e se tornar uma dependência onipresente.

Dependências também têm custo transitivo. Se o domínio usa um tipo de uma
biblioteca de ORM em sua assinatura, todo consumidor herda essa tecnologia. Em
C, um `#include` público amplia recompilações; use declarações antecipadas e
tipos opacos quando apropriado. Em Java/C#, limite pacotes/namespaces e evite
interfaces que expõem classes do framework. Em JavaScript, ciclos ES modules
podem produzir bindings parcialmente inicializados. Python tolera alguns ciclos
até o momento de importação falhar; isso não torna o design saudável.

## Comparação entre linguagens

| Necessidade | Python | Java | C | C# | JavaScript |
|---|---|---|---|---|---|
| contrato | `Protocol`/duck typing | `interface` | struct de funções | `interface`/delegate | duck typing/JSDoc |
| montagem | construtor/função | construtor/factory | `init` + contexto | construtor/container | factory/import |
| ocultação | módulo/convenção | packages/modifiers | header + tipo opaco | assemblies/modifiers | export selecionado |
| erro esperado | resultado/exceção | resultado/exceção | código + saída | resultado/exceção | resultado/throw |

O mecanismo varia; a força de design é a mesma: consumidor conhece o contrato,
não a decisão volátil. Em C, sempre deixe claro quem aloca e libera memória. Em
JavaScript, não use um objeto sem contrato como “injeção” se qualquer chave pode
faltar silenciosamente. Em Python, type hints e verificação estática ajudam a
tornar o protocolo visível, mas testes continuam necessários.

## Custo e trade-offs

Uma chamada indireta normalmente é irrelevante perto de I/O, mas a indireção
cognitiva importa. Cada porta cria nomes, arquivos e caminhos de navegação. Uma
abstração se paga quando isola volatilidade, estabelece um limite de equipe,
protege uma regra ou viabiliza teste relevante.

Contraexemplos:

- uma função pura de dez linhas não precisa de interface e factory;
- dois algoritmos que nunca são intercambiáveis não precisam compartilhar base;
- repository genérico CRUD pode apagar operações importantes do domínio;
- eventos podem trocar acoplamento de código por acoplamento temporal e
  consistência eventual;
- microsserviços não corrigem módulos mal definidos; adicionam rede e operação.

Meça o resultado: arquivos tocados por mudança, ciclos no grafo de imports,
tempo dos testes, tamanho da API pública e defeitos por fronteira. Contar classes
ou interfaces não mede qualidade.

## Falhas comuns e diagnóstico

| Sintoma | Hipótese | Experimento |
|---|---|---|
| regra exige banco no teste | domínio importa infraestrutura | execute regra com objetos em memória |
| mudança de JSON invade vários módulos | formato externo vazou | procure acesso a chaves fora do adaptador |
| muitos mocks encadeados | contrato expõe colaboração interna | teste pela saída pública e reduza a porta |
| import circular | responsabilidades ou direção ambíguas | gere grafo de imports e identifique o dono |
| interface muda em toda tarefa | abstração instável/prematura | compare consumidores e necessidades reais |
| objeto aceita estado inválido | encapsulamento só sintático | teste construção e transições inválidas |
| inicialização ocorre ao importar | composition root dispersa | procure conexões/globais no topo dos módulos |

Antes de “adicionar uma camada”, trace uma mudança concreta. Se trocar JSON por
PostgreSQL toca apenas composição e adaptador, o limite funcionou. Se tornar a
CLI uma API exige reescrever o algoritmo, a apresentação vazou para o núcleo.

## Laboratório: modularize o Dependency Planner

### Básico — separar regra e I/O

Parta de um script que lê JSON, ordena e imprime. Extraia uma função que receba
tarefas já válidas e devolva o plano.

**Critérios de aceite:**

- a função não importa `json`, `pathlib`, `argparse` nem usa `print`;
- há testes para DAG válida, tarefa ausente e ciclo;
- o adaptador mantém exatamente a saída externa anterior;
- a complexidade assintótica não piora.

### Intermediário — porta e dois adaptadores

Implemente `LeitorDeTarefas` com JSON e memória. Monte o adaptador somente na
composition root.

**Critérios de aceite:**

- o caso de uso aceita ambos sem `if tipo_do_repositorio`;
- nenhum dicionário JSON entra no domínio;
- erro de arquivo é traduzido com caminho e causa, sem stack trace ao usuário;
- testes do caso de uso não acessam sistema de arquivos;
- teste de integração cobre documento real válido e inválido.

### Avançado — nova saída sem contaminar o núcleo

Adicione exportação DOT ou uma API HTTP mínima como novo adaptador de saída.
Registre uma decisão arquitetural explicando a fronteira.

**Critérios de aceite:**

- `domain.py` e `graph.py` não importam tecnologia de apresentação;
- saída é determinística para a mesma entrada;
- o contrato declara escaping, ordenação e erros;
- há um teste de contrato do adaptador;
- o diff demonstra que a política central não precisou ser editada.

## Checklist de domínio

Você domina este capítulo quando consegue, sem consultar uma definição:

- [ ] explicar coesão e acoplamento usando uma mudança concreta;
- [ ] identificar e colocar uma invariante no proprietário correto;
- [ ] desenhar separadamente fluxo de chamada e dependência de código;
- [ ] criar uma porta mínima orientada ao caso de uso;
- [ ] traduzir um formato externo em um adaptador;
- [ ] localizar a composition root e listar o grafo de objetos criado nela;
- [ ] substituir JSON por memória sem editar algoritmo ou caso de uso;
- [ ] diagnosticar um ciclo de imports e propor mais de uma solução;
- [ ] rejeitar uma abstração cujo custo excede a variação que ela isola;
- [ ] comprovar modularidade por testes e pelo alcance de uma mudança.

No próximo capítulo, esses limites serão usados para aplicar SOLID e padrões sem
transformá-los em dogmas.
