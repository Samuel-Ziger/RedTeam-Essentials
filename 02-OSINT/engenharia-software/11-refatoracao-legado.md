# 11 — Refatoração segura e código legado

Refatorar é alterar a estrutura interna preservando o comportamento observável.
O trabalho não termina quando o código “parece mais limpo”: é preciso definir
qual comportamento deve permanecer, medir risco, limitar o tamanho de cada passo
e possuir evidência rápida para detectar regressão.

Código legado não é sinônimo de antigo. É código cuja mudança é arriscada porque
faltam entendimento, isolamento, observabilidade ou feedback confiável. Um
serviço criado ontem sem testes e sem forma de reproduzir falhas já é legado.

## Objetivos verificáveis

Ao final, você deverá conseguir:

- separar refatoração, correção de defeito e mudança de comportamento;
- criar testes de caracterização nas fronteiras observáveis;
- identificar costuras para tempo, rede, arquivo, aleatoriedade e processo;
- fazer refatorações mecânicas em passos reversíveis;
- planejar migração por branch by abstraction ou Strangler Fig;
- evoluir contratos e dados com expandir–migrar–contrair;
- definir compatibilidade, rollback e critérios de encerramento;
- medir se a mudança melhorou segurança, fluxo e capacidade de manutenção;
- aplicar o processo ao Dependency Planner sem reescrita total.

Pré-requisitos: Git, testes, design modular, contratos e noções de banco. Use a
implementação do [Dependency Planner](projetos/dependency-planner/README.md) como
caso controlado.

## Modelo mental: comportamento antes de estrutura

Uma refatoração preserva entradas, saídas e efeitos que fazem parte do contrato.
Isso pode incluir mais do que o valor retornado:

- tipo, conteúdo e ordem dos resultados;
- códigos de saída, `stdout` e `stderr`;
- arquivos gravados e transações realizadas;
- erros e sua classificação;
- chamadas externas quando observáveis;
- limites de desempenho e memória acordados;
- compatibilidade de formato ou API.

Nem todo detalhe atual é contrato. O texto exato de um log interno talvez não
seja; a ordem determinística da CLI talvez seja. Antes de congelar tudo em
testes, classifique cada observação:

| Classe | Ação |
|---|---|
| comportamento desejado e público | caracterizar e preservar |
| peculiaridade necessária por compatibilidade | caracterizar e registrar dívida |
| defeito conhecido | criar teste que descreve o comportamento correto e corrigir separadamente |
| detalhe interno | evitar teste acoplado |
| comportamento desconhecido | investigar com exemplos reais e proprietário |

O risco de um “golden test” indiscriminado é transformar qualquer acidente em
regra eterna. Caracterização captura fatos; decisão de produto define o que deve
continuar.

## O ciclo de mudança segura

Use passos pequenos e verificáveis:

1. reproduza o comportamento e registre ambiente/entrada;
2. encontre uma fronteira observável estreita;
3. escreva teste de caracterização que falha se ela mudar;
4. faça uma transformação estrutural pequena;
5. execute testes e análise estática;
6. compare métricas operacionais quando houver risco;
7. faça commit com uma intenção única;
8. repita até criar espaço para a nova regra;
9. implemente a mudança funcional em commit separado;
10. mantenha rollback possível até a evidência de produção.

“Primeiro refatore, depois altere” não exige dois grandes pull requests. Pode ser
uma sequência de commits revisáveis na mesma entrega. O ponto é saber qual passo
mudou comportamento quando algo falhar.

## Testes de caracterização

Um teste de caracterização pergunta “o que o sistema faz hoje?” antes de perguntar
“o que deveria fazer?”. Para a CLI do planejador:

```python
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def executar_cli(caminho: Path) -> subprocess.CompletedProcess[str]:
    ambiente = os.environ.copy()
    ambiente["PYTHONPATH"] = str(Path("projetos/dependency-planner/src").resolve())
    return subprocess.run(
        [sys.executable, "-m", "dependency_planner.cli", str(caminho), "--format", "json"],
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
        env=ambiente,
    )


def test_saida_valida_permanece_compativel() -> None:
    with tempfile.TemporaryDirectory() as diretorio:
        entrada = Path(diretorio) / "projeto.json"
        entrada.write_text(
            json.dumps({
                "items": [
                    {"id": "base", "title": "Base", "duration": 2, "dependencies": []},
                    {"id": "api", "title": "API", "duration": 3, "dependencies": ["base"]},
                ]
            }),
            encoding="utf-8",
        )
        processo = executar_cli(entrada)

    assert processo.returncode == 0
    assert processo.stderr == ""
    documento = json.loads(processo.stdout)
    assert documento["order"] == ["base", "api"]
```

O exemplo parte da raiz `02-OSINT/engenharia-software`; por isso configura o
`PYTHONPATH` explicitamente e usa apenas a biblioteca padrão, como o runner real.

Comparar JSON estruturalmente evita congelar espaços e quebras de linha que não
fazem parte do contrato. Já para uma interface textual deliberadamente estável,
um snapshot pode ser apropriado. Revise snapshots: aprovar uma diferença inteira
sem lê-la apenas converte regressão em nova referência.

### Golden master com amostragem responsável

Quando o legado é grande e não há especificação, capture pares de entrada/saída
representativos. Remova dados pessoais e segredos, fixe tempo/locale e armazene
uma origem rastreável. Inclua:

- caso comum;
- valores de fronteira e coleções vazias;
- erros conhecidos;
- dados máximos realistas;
- Unicode, ordenação e timezone quando relevantes.

Golden master detecta diferença; não explica correção. Complemente-o com testes
menores à medida que entende as regras.

## Costuras: onde substituir sem reescrever

Uma **costura** (*seam*) é um ponto em que o comportamento pode ser substituído
sem alterar o núcleo testado. Interfaces são uma opção, mas não a única:

- parâmetro de função;
- wrapper em torno de biblioteca;
- objeto injetado no construtor;
- variável de ambiente lida na composição;
- limite de processo ou protocolo;
- linkagem/ponteiro de função em C;
- substituição temporária de chamada em código realmente intratável.

### Exemplo: retire tempo global

Código acoplado:

```python
from datetime import datetime


def esta_atrasada(prazo: datetime) -> bool:
    return datetime.now() > prazo
```

Costura mínima:

```python
from collections.abc import Callable
from datetime import datetime


Relogio = Callable[[], datetime]


def esta_atrasada(prazo: datetime, agora: Relogio) -> bool:
    return agora() > prazo
```

O chamador real fornece `datetime.now`; o teste fornece um instante fixo. Não é
necessário criar seis classes. Para rede, um wrapper pode traduzir timeout,
status e corpo em um resultado do domínio. Para arquivos, injete um leitor ou
extraia primeiro uma função pura que recebe texto.

### Characterize and wrap

Se uma biblioteca antiga é chamada em cem lugares, não a substitua de uma vez.
Crie um wrapper com o contrato que você deseja, caracterize alguns usos e migre
chamadas gradualmente. Novos usos entram pelo wrapper; usos antigos diminuem.

Uma costura ruim apenas move o problema: mockar uma função privada, monkey-patch
global ou herdar de classe concreta pode produzir teste frágil. Prefira uma
fronteira que faça sentido no design futuro.

## Refatorações mecânicas e invariantes

Refatorações comuns:

- renomear símbolo com ferramenta consciente da linguagem;
- extrair variável ou função;
- mover função para o módulo proprietário;
- substituir aninhamento por cláusulas de guarda;
- encapsular coleção;
- introduzir objeto de valor;
- substituir condicional por Strategy quando a variação é real;
- remover código morto comprovado por busca, cobertura e telemetria;
- dividir dependência por uma porta pequena.

Exemplo com guard clauses:

```python
def validar(tarefa: Tarefa, ids: set[str]) -> None:
    if not tarefa.id:
        raise TarefaInvalida("id vazio")
    ausentes = set(tarefa.dependencias) - ids
    if ausentes:
        raise TarefaInvalida(f"dependencias ausentes: {sorted(ausentes)}")
```

A transformação torna pré-condições visíveis, mas deve preservar qual erro vence
quando há duas violações. A ordem pode ser parte do contrato. Execute testes após
cada passo; não acumule renome, movimento, formatação e regra nova num diff que
ninguém consegue revisar.

## Code smells são hipóteses

| Sinal | Pergunta | Possível refatoração | Contraexemplo |
|---|---|---|---|
| função longa | há mais de uma razão de mudança? | extrair função | pipeline linear pode ser mais legível junto |
| parâmetros demais | falta um conceito estável? | parameter object | agrupar valores sem coesão esconde contrato |
| condição repetida | há política com vários donos? | extrair função/Strategy | condições parecidas podem ter regras distintas |
| obsessão por primitivos | o valor tem invariantes? | value object | wrapper sem regra só aumenta navegação |
| dependência global | quem controla ciclo de vida? | injeção/composition root | constante imutável não exige interface |
| herança profunda | substituição é válida? | composição | hierarquia fechada e estável pode ser clara |
| comentários extensos | o código pode expressar intenção? | renomear/extrair | “por quê” histórico deve permanecer documentado |

Smell não é veredito. Use histórico de mudanças, defeitos, tempo de onboarding e
necessidades futuras para priorizar.

## Branch by abstraction

Quando dois componentes precisam coexistir no mesmo processo:

1. introduza uma abstração diante da implementação antiga;
2. faça consumidores usarem essa abstração sem mudar comportamento;
3. implemente a versão nova atrás do mesmo contrato;
4. execute comparação em sombra ou selecione por flag;
5. migre gradualmente;
6. remova implementação antiga, flag e compatibilidade temporária.

No planejador, `LeitorDeTarefas` pode envolver primeiro o parser antigo. Depois,
um parser rigoroso é adicionado. Em modo sombra, ambos leem a mesma entrada e
seus resultados são comparados, mas só o antigo responde. Não execute em sombra
efeitos irreversíveis como cobrança ou envio de mensagem.

Flags precisam de proprietário, data de remoção e comportamento seguro quando o
serviço de configuração falha. Uma flag permanente cria dois sistemas e dobra
combinações de teste.

## Strangler Fig: migração por capacidade

O padrão Strangler direciona gradualmente solicitações do legado para um novo
componente:

```text
entrada -> roteador/façade -> capacidade antiga
                         \-> capacidade nova
```

Escolha uma fatia vertical pequena, não uma camada horizontal inteira. Migrar
“toda a persistência” antes de entregar comportamento cria projeto longo e sem
feedback. Uma capacidade como “exportar plano em JSON” tem entrada, regra, saída
e métrica próprias.

Antes de migrar, defina:

- unidade de roteamento: usuário, projeto, operação ou percentual;
- compatibilidade de contrato;
- fonte de verdade durante a transição;
- sincronização e reconciliação de dados;
- métricas lado a lado;
- condição de rollback;
- critério e data para desligar o legado.

Dual write ingênuo não é atomicidade: uma gravação pode funcionar e outra não.
Prefira uma fonte de verdade com replicação/outbox, escrita idempotente e rotina
de reconciliação. Se dual write for inevitável, trate estados parciais como um
caso explícito.

## Migrações de contrato e dados

Para alterar um campo usado por versões em implantação simultânea, use
**expandir–migrar–contrair**:

1. **expandir:** novo código aceita formato antigo e novo; schema aceita ambos;
2. **migrar:** grave o novo formato, converta dados antigos em lotes e monitore;
3. **contrair:** pare de produzir o antigo, verifique ausência de consumidores e
   só então remova coluna/campo/código de compatibilidade.

Exemplo: trocar `duration` por `durationMinutes`.

```text
release A: lê ambos; grava ambos
backfill:  preenche durationMinutes de modo idempotente
release B: lê o novo; ainda grava ambos para consumidores antigos
evidência: nenhum leitor antigo e 100% dos registros migrados
release C: para de gravar e depois remove duration
```

Não renomeie coluna em uma única implantação se aplicação antiga ainda roda.
Backfill deve ter checkpoint, limite de carga, retry e verificação. Rollback de
código não restaura automaticamente dados apagados; por isso a contração é a
última etapa.

## Compatibilidade e versionamento

Classifique mudanças:

- aditiva: campo opcional novo;
- comportamental: mesma forma, nova semântica;
- destrutiva: remoção, renome ou restrição;
- operacional: latência, volume, ordenação ou retry alterado.

Mudança “aditiva” pode quebrar clientes que rejeitam campos desconhecidos.
Mudança de ordenação pode quebrar snapshots ou paginação. Compatibilidade precisa
ser testada com consumidores reais ou contratos compartilhados, não assumida.

## Métricas que orientam a refatoração

Não use apenas cobertura ou complexidade ciclomática. Combine sinais:

**Segurança da mudança**

- taxa de falha e rollback após deploy;
- tempo para detectar e recuperar;
- testes de caracterização sobre fluxos críticos;
- diferenças no modo sombra.

**Fluxo de engenharia**

- lead time da mudança;
- tempo da suíte e feedback local;
- tamanho/frequência de pull requests;
- quantidade de arquivos tocados por uma mudança típica.

**Estrutura**

- ciclos de dependência;
- fan-in/fan-out e superfície pública;
- duplicação de regra, não apenas de texto;
- hotspots: alta frequência de mudança combinada a alta complexidade.

**Operação**

- latência e throughput por percentil;
- erro por categoria;
- consumo de CPU/memória;
- fila, saturação e timeout.

Uma refatoração pode aumentar linhas e diminuir risco. Cobertura de 90% pode não
testar uma única asserção relevante. Defina baseline, hipótese e limite aceitável.

## Dívida técnica com decisão explícita

Registre contexto, benefício imediato, juros observados, risco, área afetada,
gatilho de pagamento e proprietário. “Código feio” não é item acionável.

Exemplo:

```text
Decisão: manter leitura síncrona do JSON nesta versão.
Benefício: entregar CLI sem dependência adicional.
Juros: bloqueia arquivos grandes e impede streaming.
Gatilho: arquivo p95 > 20 MiB ou leitura > 500 ms.
Quitação: adaptar leitura incremental, com benchmark e limite de memória.
```

## Falhas comuns e diagnóstico

| Sintoma | Causa provável | Próxima ação |
|---|---|---|
| suíte verde, usuário quebrado | fronteira errada foi testada | reproduza fluxo externo e adicione contrato |
| snapshot muda em toda edição | detalhe interno congelado | compare estrutura/semântica relevante |
| refatoração nunca termina | escopo grande sem fatias | escolha costura e entrega vertical menor |
| sistema novo diverge em sombra | semântica implícita | classifique diferenças e caracterize legado |
| rollback falha | migração destrutiva adiantada | restaurar compatibilidade e usar expansão |
| flag permanece por meses | sem critério de encerramento | atribuir dono, métrica e data de remoção |
| métrica média parece boa | cauda ou categoria escondida | analisar percentis e erros segmentados |

## Laboratórios

### Básico — caracterizar antes de extrair

Escolha um fluxo da CLI do Dependency Planner e caracterize sucesso e ciclo.
Depois extraia uma função pura.

**Critérios de aceite:**

- testes capturam código de saída, canal e estrutura do resultado;
- pelo menos um detalhe irrelevante não é congelado;
- commits de teste e refatoração são separados;
- saída observável permanece idêntica;
- teste da função pura não cria processo nem arquivo.

### Intermediário — criar três costuras

Isole sistema de arquivos, relógio e destino de relatório.

**Critérios de aceite:**

- nenhum teste depende do horário atual ou de diretório global;
- implementações reais são montadas apenas na composition root;
- falhas de cada dependência são classificadas e preservam a causa;
- existe teste de integração para cada adaptador real;
- o design usa função ou protocolo mínimo, sem framework de mocks próprio.

### Avançado — migração gradual

Substitua o leitor JSON por uma versão com schema mais rigoroso usando branch by
abstraction ou faça uma migração Strangler para um novo relatório.

**Critérios de aceite:**

- baseline e hipótese estão documentados;
- legado e novo podem ser comparados com dados sanitizados;
- divergências são métricas, não apenas logs soltos;
- flag possui dono, fallback, data e critério de remoção;
- plano trata compatibilidade e migração de dados;
- rollback foi ensaiado antes da contração;
- código legado e compatibilidade temporária são removidos após estabilização.

## Checklist de domínio

- [ ] Distingo refatoração de mudança funcional no diff e no histórico.
- [ ] Sei definir quais observações pertencem ao contrato.
- [ ] Escrevo teste de caracterização sem congelar detalhes irrelevantes.
- [ ] Encontro uma costura menor que uma reescrita.
- [ ] Faço passos pequenos com feedback após cada transformação.
- [ ] Sei quando usar branch by abstraction e quando usar Strangler Fig.
- [ ] Planejo expandir–migrar–contrair sem depender de deploy simultâneo.
- [ ] Trato dual write, backfill, idempotência e rollback explicitamente.
- [ ] Uso métricas de estrutura, fluxo, segurança e operação em conjunto.
- [ ] Removo flags, adaptadores temporários e código morto ao concluir.

Refatoração segura não elimina incerteza; transforma uma mudança opaca em uma
série de hipóteses pequenas, observáveis e reversíveis.
