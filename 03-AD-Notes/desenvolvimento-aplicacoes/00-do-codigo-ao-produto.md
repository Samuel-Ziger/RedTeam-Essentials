# 00 — Do código ao produto

Uma função resolve um cálculo. Uma aplicação precisa sobreviver ao uso por
outra pessoa: primeira execução, configuração, entrada inválida, interrupção,
atualização, diagnóstico e remoção fazem parte do produto. Neste módulo,
construiremos progressivamente o **Study Desk**, uma aplicação local para
registrar sessões de estudo. O objetivo não é escolher um framework cedo, mas
aprender a transformar uma necessidade em contratos verificáveis.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- distinguir código funcional de produto utilizável e sustentável;
- descrever usuário, problema, jornada, limites e evidências de sucesso;
- separar domínio, aplicação, adaptadores e apresentação;
- transformar adjetivos como “rápido” e “confiável” em medidas testáveis;
- identificar invariantes antes de implementar interface ou persistência;
- entregar uma fatia vertical pequena sem esconder riscos importantes.

## Pré-requisitos

Este capítulo pressupõe funções, tipos, coleções, exceções e testes básicos,
além da separação arquitetural apresentada no módulo 02. Não é necessário
conhecer interface gráfica, sistema operacional ou redes. Tudo aqui pode ser
praticado em memória e com uma CLI simples.

## Modelo mental: produto é um contrato ao longo do tempo

Pense na aplicação como um serviço prestado ao usuário, não como um conjunto de
telas. Esse serviço possui cinco contratos complementares:

| Contrato | Pergunta que responde | Evidência |
|---|---|---|
| utilidade | resolve uma tarefa real? | cenário concluído por uma pessoa |
| comportamento | o que aceita e produz? | exemplos e testes de aceitação |
| qualidade | quão rápido, seguro e recuperável? | medidas e limites |
| operação | como instalar, atualizar, diagnosticar e remover? | procedimento repetível |
| evolução | como mudar sem destruir dados ou automações? | versão e compatibilidade |

Uma implementação pode estar correta para uma entrada feliz e ainda falhar
como produto. Por exemplo, um registrador de estudos que soma minutos, mas perde
tudo ao fechar, não informa por que recusou um valor e muda o formato exportado a
cada versão, resolve apenas o cálculo central.

## O contrato do Study Desk

Antes da interface, escreva quem usa, qual tarefa quer concluir e como reconhece
o resultado. Um primeiro contrato pode ser:

```text
Usuário: estudante que organiza o próprio aprendizado.
Tarefa: registrar assunto e duração de uma sessão em menos de 20 segundos.
Sucesso: a sessão válida recebe um identificador e aparece no histórico.
Entrada: título de 1 a 80 unidades UTF-16 e duração inteira de 1 a 1440 minutos.
Falha esperada: nenhum estado muda e a mensagem informa campo e correção.
Persistência: dados locais, exportáveis em formato versionado.
Privacidade: nenhuma telemetria ou sincronização implícita.
Recuperação: importação inválida preserva os dados anteriores.
```

O contrato delimita o produto inicial. Busca, metas, sincronização e colaboração
podem ser boas ideias, mas ainda não pertencem à primeira entrega. Dizer
explicitamente o que está fora reduz complexidade acidental.

### Histórias não substituem exemplos

“Como estudante, quero registrar uma sessão” comunica intenção, mas não resolve
ambiguidades. Complete-a com exemplos:

| Caso | Entrada | Resultado esperado |
|---|---|---|
| mínimo válido | `title="C"`, `minutes=1` | sessão criada |
| limite válido | título ASCII com 80 unidades UTF-16, `minutes=1440` | sessão criada |
| título em branco | `title="   "` | erro em `title`; estado intacto |
| fração | `minutes=2.5` | erro de tipo; sem arredondar |
| repetição | mesma sessão enviada duas vezes | duas sessões distintas por enquanto |

Exemplos nas fronteiras viram testes e impedem decisões improvisadas durante a
implementação.

## Jornadas, não telas

Uma tela bonita pode falhar na jornada. Mapeie o fluxo observável:

```text
descobrir -> iniciar -> entender estado vazio -> registrar -> corrigir erro
          -> reencontrar -> exportar -> restaurar -> remover
```

Para cada etapa, considere ao menos:

- estado vazio e primeira execução;
- entrada válida, inválida e no limite;
- cancelamento antes e depois de confirmar;
- interrupção enquanto há trabalho pendente;
- formato antigo, dado incompleto ou documento corrompido;
- repetição da mesma ação;
- evidência de sucesso e caminho de recuperação.

O caminho feliz é apenas uma linha em uma matriz de estados. Desenhar os demais
caminhos cedo custa menos que descobri-los depois que existem dados reais.

## Fronteiras da aplicação

Separe decisão de negócio de tecnologia:

| Área | Responsabilidade | Exemplo no Study Desk |
|---|---|---|
| domínio | entidades, valores e invariantes | `StudySession`, `Duration` |
| aplicação | coordena casos de uso | `RegisterSession` |
| portas | contratos de dependências | `SessionRepository`, `Clock` |
| adaptadores | implementam as portas | repositório em memória ou arquivo |
| apresentação | traduz interação | CLI, GUI ou web |

A apresentação não decide se 1500 minutos são válidos. O domínio não
conhece botão, terminal, arquivo ou `localStorage`. Essa fronteira permite trocar
a interface e testar regras sem infraestrutura.

Exemplo seguro em Python, ainda sem persistência:

```python
import re
from dataclasses import dataclass
from datetime import datetime, timezone


SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$")


def utf16_units(value: str) -> int:
    return len(value.encode("utf-16-le")) // 2


@dataclass(frozen=True)
class StudySession:
    session_id: str
    title: str
    minutes: int
    recorded_at: datetime

    def __post_init__(self) -> None:
        normalized = self.title.strip()
        if not SAFE_ID.fullmatch(self.session_id):
            raise ValueError("session_id inválido")
        if not 1 <= utf16_units(normalized) <= 80:
            raise ValueError("title deve ter entre 1 e 80 unidades UTF-16")
        if isinstance(self.minutes, bool) or not isinstance(self.minutes, int):
            raise TypeError("minutes deve ser inteiro")
        if not 1 <= self.minutes <= 1440:
            raise ValueError("minutes deve estar entre 1 e 1440")
        if self.recorded_at.tzinfo is None or self.recorded_at.utcoffset() is None:
            raise ValueError("recorded_at deve possuir fuso explícito")
        object.__setattr__(self, "title", normalized)
        object.__setattr__(self, "recorded_at", self.recorded_at.astimezone(timezone.utc))
```

O `bool` merece tratamento explícito porque, em Python, é subtipo de `int`. As
invariantes de formato pertencem ao objeto: qualquer caminho que crie uma sessão
recebe a mesma proteção. O caso de uso fornece identificador e relógio, o que
permite testes determinísticos; o repositório/agregado ainda precisa garantir
unicidade entre sessões.

## Contratos e invariantes

Uma **pré-condição** precisa ser satisfeita pelo chamador; uma **pós-condição**
deve ser garantida pela operação; uma **invariante** deve permanecer verdadeira
durante toda a vida de um objeto válido.

Para `register_session(title, minutes)`:

- pré-condição: entrada pode ser analisada como texto e inteiro dentro dos
  limites documentados;
- pós-condição de sucesso: exatamente uma sessão foi adicionada e pode ser
  reencontrada por seu identificador;
- pós-condição de falha: nenhuma sessão foi adicionada;
- invariantes do objeto: identificador bem-formado, título normalizado, duração
  no intervalo e instante com fuso explícito normalizado para UTC;
- invariante da coleção: identificadores únicos no estado confirmado.

Não confunda “a interface impede” com invariante. A entrada também pode chegar
por importação, teste ou futura API.

## Qualidade observável

Adjetivos não são requisitos suficientes. Defina condição, medida, percentil ou
limite e ambiente de referência:

| Adjetivo | Exemplo verificável |
|---|---|
| rápido | feedback inicial em até 100 ms para ações locais |
| robusto | importação inválida nunca altera o estado confirmado |
| acessível | tarefa principal executável apenas com teclado |
| previsível | mesma entrada e estado produzem o mesmo resultado |
| recuperável | falha de gravação preserva a última versão válida |
| privado | dados não deixam o dispositivo sem ação explícita |

Uma meta sem método de medição é apenas desejo. O ambiente real pode mudar os
números; o contrato deve declarar o conjunto de dados e o cenário usados.

## Fatia vertical e decisões

Uma fatia vertical atravessa as fronteiras necessárias para entregar uma jornada
pequena. A primeira fatia do Study Desk será:

```text
CLI add -> parse e validação -> RegisterSession -> repositório local
        -> resultado estruturado -> mensagem/código de saída
```

Ela é melhor evidência que seis camadas parcialmente prontas sem jornada
executável. Ainda assim, evite atalhos que contradigam o contrato. Um protótipo
descartável pode ignorar migração; a primeira versão que salva dados reais não.

Decisões têm trade-offs:

- **CLI primeiro:** fácil de testar e automatizar; menos visual para iniciantes;
- **armazenamento em memória:** iteração rápida; não demonstra recuperação;
- **JSON local:** transparente e portável; exige schema, limites e escrita segura;
- **framework cedo:** acelera convenções; pode esconder fundamentos e acoplar o
  domínio.

Registre decisões reversíveis em notas curtas. Para uma decisão cara de reverter,
inclua contexto, opções, consequências e gatilho de revisão.

## Falhas comuns e diagnóstico

| Sintoma | Hipótese provável | Como confirmar |
|---|---|---|
| regras diferentes na CLI e importação | validação ficou na apresentação | teste o domínio por ambos os caminhos |
| teste depende da hora atual | relógio global oculto | injete um relógio fixo |
| novo formato quebra dados antigos | arquivo espelha objeto interno | teste fixtures de cada versão |
| erro limpa o formulário | jornada de falha não foi modelada | teste valor preservado após rejeição |
| equipe discute framework sem decidir limites | contrato de produto ausente | escreva exemplos de fronteira primeiro |

Diagnostique atravessando a jornada: reproduza, registre entrada segura, identifique
a primeira fronteira em que esperado e observado divergem e formule uma hipótese
testável. Não altere várias camadas antes de localizar a divergência.

## Exercícios em três níveis

### Nível 1 — compreensão

Escreva o contrato de um conversor local de unidades: usuário, tarefa, entradas,
saídas, limites, falhas e cinco exemplos de fronteira.

**Critérios de aceite:** há pelo menos uma pós-condição de falha; “rápido” e
“fácil” foram substituídos por medidas; itens fora do escopo estão registrados.

### Nível 2 — aplicação

Modele `StudySession` em uma linguagem do curso e escreva testes para título vazio,
espaços externos, limites 1/1440 e tipos indevidos. Desenhe as fronteiras da fatia
`add` sem implementar arquivo.

**Critérios de aceite:** as invariantes vivem no domínio; os testes não dependem
de hora aleatória; nenhuma classe do domínio importa biblioteca de interface.

### Nível 3 — projeto

Produza um documento de descoberta do Study Desk: jornada principal e três de
falha, mapa de fronteiras, cinco atributos mensuráveis, matriz de exemplos e uma
decisão arquitetural comparando JSON e memória para a primeira entrega.

**Critérios de aceite:** outra pessoa consegue explicar uso, falhas, dados e
recuperação sem discutir framework; cada requisito possui uma evidência que pode
ser coletada; riscos e hipóteses estão separados de fatos.

## Checklist de domínio

- [ ] Consigo explicar por que uma função correta ainda pode ser um produto ruim.
- [ ] Escrevo pré-condições, pós-condições e invariantes sem citar uma tela.
- [ ] Mapeio caminho feliz, falhas, cancelamento, recuperação e remoção.
- [ ] Separo domínio, caso de uso, porta, adaptador e apresentação.
- [ ] Transformo atributos subjetivos em medidas reproduzíveis.
- [ ] Reconheço a diferença entre protótipo descartável e dado de produção.
- [ ] Consigo definir uma fatia vertical pequena e demonstrável.
- [ ] Localizo uma falha pela primeira fronteira divergente, não por tentativa.
