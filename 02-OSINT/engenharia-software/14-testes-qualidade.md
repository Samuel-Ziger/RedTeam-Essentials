# 14 — Testes e qualidade: evidência contra riscos

Teste não prova ausência de defeitos. Ele reduz incerteza sobre comportamentos
específicos em condições específicas. Uma boa estratégia liga risco a uma
evidência confiável, rápida o bastante para orientar mudanças e ampla o bastante
para detectar falhas nas fronteiras reais.

Este capítulo usa a suíte do
[Dependency Planner](projetos/dependency-planner/README.md). Leia primeiro
[Requisitos e modelagem](12-requisitos-modelagem.md) e
[Arquitetura](13-arquitetura.md).

## Objetivos

Ao concluir, você deverá conseguir:

- escolher níveis de teste pelo risco, não por uma proporção universal;
- escrever testes de unidade, integração, contrato e ponta a ponta;
- derivar propriedades e relações metamórficas de invariantes;
- usar cobertura, mutation testing e fuzzing sem métricas de vaidade;
- desenhar testes de desempenho reproduzíveis;
- diagnosticar e eliminar testes flaky;
- definir quality gates que protegem mudança sem paralisar a equipe.

## Pré-requisitos e modelo mental

Use o ciclo:

```text
risco
  -> comportamento observável
  -> oráculo
  -> nível de teste mais barato que reproduz a falha
  -> execução determinística
  -> diagnóstico
  -> decisão
```

Um **oráculo** decide se o resultado está correto. “Não lançou exceção” é um
oráculo fraco quando o requisito exige ordem, lotes e duração exatos.

Qualidade também inclui requisitos, design, revisão, tipos, análise estática,
observabilidade e operação. A suíte é uma parte do sistema de feedback.

## 1. Estratégia por risco

Crie uma matriz:

| Risco | Impacto | Probabilidade | Evidência principal |
|---|---:|---:|---|
| dependente antes do pré-requisito | alto | média | propriedades + exemplos unitários |
| ciclo gera plano parcial | alto | média | unidade + CLI end-to-end |
| JSON aceita campo ignorado | médio | média | integração do adaptador |
| stdout mistura diagnóstico | alto em CI | baixa | teste de contrato da CLI |
| algoritmo degrada em grafo grande | médio | média | benchmark controlado |
| alteração de saída quebra consumidor | alto | média | contrato/snapshot semântico |

Impacto alto merece redundância em níveis diferentes quando cada teste detecta
uma classe de falha distinta. Repetir a mesma asserção em cinco lugares só
aumenta manutenção.

## 2. Pirâmide e test trophy

### Pirâmide

- muitos testes unitários rápidos;
- menos integrações reais;
- poucos testes ponta a ponta essenciais.

Funciona bem quando o domínio contém regras ricas e as bordas são relativamente
estreitas, como no Planner.

### Test trophy

Enfatiza testes de integração: confiança vem de componentes colaborando como em
produção, apoiados por análise estática e algumas unidades/E2E. É útil em
aplicações onde erros aparecem mais na integração entre UI, API e dados.

Não escolha um desenho como dogma. Para o Planner:

- algoritmo puro: muitas unidades e propriedades;
- parser JSON: integração real com arquivo temporário;
- CLI: poucos fluxos ponta a ponta com stdout/stderr/exit code;
- futura API/banco: testes reais de protocolo/driver;
- deploy: smoke test mínimo.

Mocks de filesystem não provam encoding, JSON ou erro de arquivo. E2E para todas
as combinações tornaria diagnóstico lento. Distribua pelo risco.

## 3. Unidade: comportamento pequeno e rápido

O teste existente é legível:

```python
def test_dependencia_aparece_antes_do_dependente(self) -> None:
    plan = build_plan(
        [
            WorkItem("model", "Modelar", 3),
            WorkItem("api", "Construir API", 5, ("model",)),
        ]
    )

    position = {item_id: index for index, item_id in enumerate(plan.order)}
    self.assertLess(position["model"], position["api"])
```

Estrutura Arrange–Act–Assert é um guia, não exigência visual. O nome declara a
regra. O teste usa API pública do módulo e não inspeciona heap/indegree internos.

### Particionamento de equivalência

Para duração:

- válidos: inteiros positivos;
- limite válido: 1;
- inválidos: 0, negativos, booleano, float, string, `None`.

Python considera `bool` subtipo de `int`; por isso o teste de `True` protege
uma decisão deliberada do domínio.

### Tabela de exemplos

```python
def test_rejects_invalid_durations(self) -> None:
    invalid_values = (0, -1, True, 1.5, "3", None)

    for value in invalid_values:
        with self.subTest(value=value):
            with self.assertRaises(ValidationError):
                WorkItem("api", "Construir API", value)  # type: ignore[arg-type]
```

Não agrupe casos se eles deveriam produzir diagnósticos diferentes. `subTest`
preserva qual entrada falhou.

### Teste de erro completo

Ao testar ciclo, valide mais que o tipo:

```python
with self.assertRaises(CycleError) as captured:
    build_plan(
        [
            WorkItem("A", "A", 1, ("C",)),
            WorkItem("B", "B", 1, ("A",)),
            WorkItem("C", "C", 1, ("B",)),
        ]
    )

path = captured.exception.path
self.assertEqual(path[0], path[-1])
self.assertEqual(set(path[:-1]), {"A", "B", "C"})
```

Assim o teste permite qualquer ciclo verdadeiro se o contrato não fixa um
caminho específico, mas rejeita mensagem inventada.

## 4. Dublês e fronteiras

- **stub:** devolve resposta preparada;
- **spy:** registra chamadas;
- **mock:** exige interações;
- **fake:** implementação funcional simplificada;
- **dummy:** ocupa parâmetro sem participar.

Fake para porta do Planner:

```python
class InMemoryRepository:
    def __init__(self, items: tuple[WorkItem, ...]) -> None:
        self._items = items

    def list_items(self) -> tuple[WorkItem, ...]:
        return self._items


def test_use_case_reads_repository_and_returns_plan() -> None:
    repository = InMemoryRepository(
        (
            WorkItem("model", "Modelar", 2),
            WorkItem("api", "API", 3, ("model",)),
        )
    )

    plan = PlanProject(repository).execute()

    assert plan.order == ("model", "api")
```

Esse teste mostra colaboração do caso de uso sem filesystem. Não use mock para
afirmar a ordem exata de chamadas internas quando apenas o plano é contrato.
Mocks excessivos acoplam testes à refatoração.

## 5. Integração: mecanismo real

O adaptador JSON merece arquivo real temporário:

```python
def test_repository_rejects_unknown_field(self) -> None:
    path = self._write(
        {
            "items": [
                {
                    "id": "A",
                    "title": "Tarefa A",
                    "duration": 2,
                    "dependencies": [],
                    "silentlyIgnored": True,
                }
            ]
        }
    )

    with self.assertRaisesRegex(ValidationError, "campos desconhecidos"):
        JsonWorkItemRepository(path).list_items()
```

Ele atravessa serialização, UTF-8, filesystem e parser. Acrescente:

- JSON truncado e raiz não objeto;
- campo ausente;
- lista com item não objeto;
- caracteres Unicode;
- arquivo inexistente/permissão;
- tamanho máximo, se requisito;
- symlink/caminho permitido, se houver fronteira de segurança.

Use diretório temporário único e cleanup automático. Não dependa do diretório de
execução nem de arquivo deixado por outro teste.

Integração com PostgreSQL deve usar PostgreSQL real da versão suportada, não
SQLite fingindo equivalência de SQL, locks e tipos.

## 6. Contratos

Contrato é o que um consumidor pode observar:

- schema do arquivo de entrada;
- campos/tipos da saída JSON;
- códigos de saída;
- separação stdout/stderr;
- erros estruturados;
- API de módulo;
- eventos e versões.

Teste da CLI:

```python
def test_cycle_has_no_partial_stdout(self) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = main(
            [str(PROJECT_ROOT / "fixtures" / "cyclic-project.json")]
        )

    self.assertEqual(code, 2)
    self.assertEqual(stdout.getvalue(), "")
    self.assertIn("ciclo de dependencias", stderr.getvalue())
```

Um snapshot textual completo fica frágil a espaços e tradução. Para JSON,
desserialize e compare semântica. Fixe texto integral somente quando o texto é
contrato público.

### Consumer-driven contract

Quando produtor e consumidor são implantados separadamente, o consumidor pode
publicar expectativas verificadas pelo produtor. Isso detecta incompatibilidade,
mas não prova semântica de negócio, performance ou disponibilidade.

Versione fixtures de contrato e evite dados sensíveis.

## 7. Ponta a ponta

Um E2E do Planner invoca o processo como usuário:

```text
PYTHONPATH=02-OSINT/engenharia-software/projetos/dependency-planner/src \
  python3 -m dependency_planner.cli \
  02-OSINT/engenharia-software/projetos/dependency-planner/fixtures/valid-project.json \
  --format json
```

Verifique:

- código 0;
- stderr vazio;
- stdout é JSON válido;
- `minimum_duration == 14`;
- caminho termina em `release`;
- toda dependência precede seu dependente.

Para ciclo: código 2, stdout vazio e erro útil. Poucos fluxos cobrem wiring,
entrypoint e contrato. Não tente diagnosticar toda regra por subprocesso.

## 8. Propriedades

Exemplos isolados não cobrem todos os DAGs. Propriedades do Planner:

1. cada ID de entrada aparece exatamente uma vez na ordem;
2. para toda dependência `d` de `v`, `position[d] < position[v]`;
3. cada ID aparece exatamente uma vez entre todos os lotes;
4. lote de uma tarefa vem depois dos lotes de suas dependências;
5. duração mínima é ao menos a maior duração individual;
6. caminho crítico é um caminho válido e sua soma iguala a duração mínima;
7. entrada vazia produz estruturas vazias e duração zero;
8. o resultado é determinístico.

Um teste gerativo precisa gerar DAG, não grafo arbitrário acidentalmente cíclico:

```python
def generated_dag(seed: int, size: int) -> list[WorkItem]:
    randomizer = random.Random(seed)
    items: list[WorkItem] = []
    for index in range(size):
        predecessors = tuple(
            f"T{previous}"
            for previous in range(index)
            if randomizer.random() < 0.15
        )
        items.append(
            WorkItem(f"T{index}", f"Tarefa {index}", index % 7 + 1, predecessors)
        )
    return items
```

IDs anteriores como dependências garantem aciclicidade. Ao falhar, registre
semente e reduza o exemplo. Bibliotecas como Hypothesis automatizam geração e
shrinking, mas a propriedade continua sendo responsabilidade humana.

## 9. Testes metamórficos

Quando não é fácil saber toda a saída, transforme a entrada e preveja uma
relação:

- permutar tarefas não muda o plano semântico;
- renomear IDs por mapeamento bijetivo preserva relações e duração;
- multiplicar todas as durações por `k > 0` multiplica duração mínima por `k`;
- adicionar tarefa isolada não invalida ordem das dependências existentes;
- adicionar dependência redundante transitiva não muda caminhos executáveis,
  embora possa alterar representação interna;
- aumentar duração fora de qualquer caminho crítico não pode reduzir o total.

Tenha cuidado: renomear IDs muda o desempate lexicográfico e pode mudar uma
ordem topológica igualmente válida. A propriedade correta compara precedência,
lotes ou resultado mapeado conforme o contrato, não bytes cegamente.

## 10. Mutation testing

Mutation testing altera código, por exemplo:

- `duration <= 0` para `duration < 0`;
- remove verificação de ID duplicado;
- troca decremento de indegree;
- usa `min` no caminho crítico;
- muda exit code 2 para 0.

Se a suíte continua verde, o mutante **sobreviveu**. Investigue:

- falta um teste;
- asserção é fraca;
- código está morto;
- mutante é semanticamente equivalente;
- requisito é ambíguo.

Mutation score não deve virar meta cega. Exclua código gerado e analise mutantes
equivalentes. Rode uma seleção no PR e campanha mais ampla em agenda se o custo
for alto.

## 11. Fuzzing

Fuzzing explora entradas malformadas e combinações inesperadas. Para o adaptador:

- bytes que não são UTF-8;
- JSON truncado;
- profundidade extrema;
- arrays grandes;
- strings Unicode e caracteres de controle;
- números enormes;
- campos com tipos trocados.

Propriedades de segurança:

- processo não trava por exceção não controlada;
- não escreve arquivo;
- não produz plano parcial;
- termina dentro do orçamento;
- erro não inclui segredo/conteúdo integral;
- consumo de memória tem limite.

Execute em ambiente isolado, com corpus fictício, timeout e limite de memória.
Um fuzzer encontrar crash não autoriza testar serviços alheios.

## 12. Desempenho

Defina workload antes da ferramenta:

| Forma | Característica |
|---|---|
| cadeia | profundidade `V`, uma tarefa pronta por vez |
| leque | muitas tarefas liberadas simultaneamente |
| esparso | poucas arestas por vértice |
| denso acíclico | muitas arestas, memória dominante |
| ciclo tardio | validação percorre grande parte antes de falhar |

Métrica:

- tempo de parede p50/p95, não uma execução;
- CPU;
- pico de memória;
- tamanho `V/E`;
- versão/runtime/hardware;
- warm-up e carga concorrente;
- saída desabilitada ou incluída explicitamente.

Benchmark não deve misturar geração da fixture com planejamento, a menos que
isso faça parte do caminho medido.

```text
baseline: commit, Python, máquina, V, E, distribuição
hipótese: heap domina quando há muitos empates
mudança: ...
resultado: mediana/p95/memória
decisão: manter/reverter
```

Use limiar com tolerância a ruído e ambiente dedicado para gate de regressão.
Microbenchmark instável em runner compartilhado não deve bloquear por 2%.

## 13. Testes flaky

Um teste flaky alterna sem mudança relevante. Fontes:

- tempo real e timezone;
- aleatoriedade sem semente;
- ordem compartilhada;
- porta/processo/arquivo global;
- concorrência e race condition;
- dependência externa;
- timeout apertado;
- vazamento de estado/cache.

Diagnóstico:

1. preserve logs, seed e ambiente da falha;
2. execute isolado e em ordem variada;
3. repita com concorrência;
4. procure estado global e espera por tempo;
5. substitua `sleep` por espera de condição com deadline;
6. controle clock/random quando não forem o objeto;
7. corrija a causa.

Quarentena pode restaurar sinal temporariamente, com dono e prazo. “Retry até
passar” esconde defeito e reduz confiança.

## 14. Cobertura

Cobertura responde “esta linha/ramo executou?”, não “a regra foi verificada?”.
Use-a para:

- encontrar ramos nunca exercitados;
- revisar código crítico com baixa evidência;
- evitar queda grande inexplicada.

Não use 100% como sinônimo de qualidade. Este teste cobre sem afirmar nada:

```python
def test_calls_planner() -> None:
    build_plan([])
```

Branch coverage ajuda validações; mutation testing avalia força das asserções.
Requisitos críticos podem exigir 100% de caminhos conhecidos mesmo quando a meta
global é menor.

## 15. Quality gates

Pipeline em ordem de feedback/custo:

1. formato, lint e arquivos proibidos;
2. análise estática, tipos e segredos;
3. unidades/propriedades rápidas;
4. integração e contrato;
5. build/empacotamento reproduzível;
6. E2E/smoke;
7. dependências e artefato;
8. desempenho/mutação/fuzz em estágio adequado.

Gate útil é:

- automatizado;
- reproduzível;
- rápido no caminho crítico;
- ligado a risco;
- com mensagem acionável;
- impossível de contornar silenciosamente;
- proprietário e revisado.

Exemplo:

```text
PR:
  lint + type check + unit + integração do adaptador + 2 E2E

main:
  tudo do PR + build limpo + contrato + smoke

noturno:
  mutation + propriedades extensas + fuzz + performance
```

Falha de infraestrutura deve ser distinta de regressão. Artefato promovido deve
ser o mesmo testado, não recompilado de forma diferente.

## 16. Falhas comuns e diagnóstico

| Sinal | Causa | Correção |
|---|---|---|
| suíte verde, produção falha | mocks nas fronteiras reais | integração/contrato real |
| refatoração quebra muitos testes | teste conhece internals | afirmar comportamento público |
| snapshot muda sempre | saída volátil ampla | comparar semântica/campos estáveis |
| cobertura alta, mutantes vivem | asserções fracas | derivar propriedades/requisitos |
| CI lento | E2E redundante/sem seleção | mover regra a unidade e paralelizar com isolamento |
| flaky “resolvido” por retry | não determinismo oculto | capturar seed/clock/estado |
| benchmark contraditório | workloads/ambiente diferentes | protocolo e baseline versionados |

Quando um teste falha, primeiro reproduza e classifique: defeito do produto,
defeito do teste, ambiente ou requisito alterado.

## 17. Exercícios em três níveis

### Nível 1 — exemplos e fronteiras

1. Complete a matriz de durações inválidas.
2. Teste projeto vazio, ID duplicado, referência ausente e ciclo.
3. Teste o repositório com JSON real temporário e Unicode.
4. Teste contrato da CLI nos dois formatos.

**Evidência:** testes são determinísticos, falham com mutação manual relevante e
terminam em tempo curto.

### Nível 2 — propriedades e integração

1. Gere 100 DAGs por sementes registradas.
2. Verifique as oito propriedades deste capítulo.
3. Crie três transformações metamórficas e explique seus limites.
4. Troque mock do repositório por fake ou integração, justificando.
5. Injete cinco mutações deliberadas e registre quais sobreviveram.

**Evidência:** toda falha imprime seed/caso mínimo e cada mutante importante é
morto ou justificado como equivalente.

### Nível 3 — estratégia profissional

1. Crie threat/risk matrix do Planner.
2. Defina suíte por nível e orçamento de duração.
3. Escreva protocolo de performance para cadeia, leque, esparso e denso.
4. Faça fuzz local do adaptador com limites.
5. Proponha gates de PR, main e noturno.
6. Simule um flaky test e produza análise causal, não apenas retry.

**Evidência:** documento liga cada risco a teste, frequência, proprietário,
diagnóstico e condição de bloqueio.

## Checklist de domínio

- [ ] Cada teste protege comportamento ou risco nomeado.
- [ ] Uso o nível mais barato que reproduz a falha real.
- [ ] SQL, filesystem e protocolo relevantes têm integração real.
- [ ] Contratos verificam tipos, códigos e canais observáveis.
- [ ] Propriedades cobrem invariantes além de exemplos escolhidos.
- [ ] Mutation testing avalia a força das asserções.
- [ ] Fuzzing possui isolamento, limite e corpus não sensível.
- [ ] Benchmarks registram forma, ambiente, repetição e distribuição.
- [ ] Flaky tests têm causa corrigida, dono e evidência.
- [ ] Quality gates são rápidos, acionáveis e proporcionais ao risco.

Continue em [Colaboração, Git e documentação](15-colaboracao-documentacao.md) para
transformar esse feedback em um fluxo seguro de equipe.
