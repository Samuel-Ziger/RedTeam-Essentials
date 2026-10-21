# 14 — Desempenho percebido, profiling e orçamento

Desempenho não é “código rápido” em abstrato. É a capacidade de concluir uma
jornada dentro de limites de tempo, memória, tamanho e energia que façam sentido
para o público. Uma busca de 5 ms não compensa uma inicialização de oito segundos;
reduzir 20% de uma função que representa 1% da jornada quase não altera o total.
O trabalho começa com uma pergunta mensurável, não com uma otimização favorita.

## Objetivos de aprendizagem

Ao final, você deverá ser capaz de:

- converter expectativas de uso em orçamento mensurável;
- construir um cenário, ambiente de referência e baseline reproduzíveis;
- distinguir latência, throughput, uso de memória, tamanho e responsividade;
- escolher CPU profiler, amostragem, alocação, heap snapshot ou timeline;
- localizar o caminho dominante antes de alterar o código;
- medir distribuição e percentis sem esconder variação na média;
- confirmar ganho e preservar correção, acessibilidade e manutenção;
- impedir regressões relevantes no Study Desk sem criar testes instáveis.

## Pré-requisitos

Revise complexidade e estruturas de dados no módulo 02. Neste módulo, releia
estado/eventos (capítulo 05), interface web (07), acessibilidade (08), clientes de
API (09) e logs (11). Use dados sintéticos; não copie documentos pessoais para um
perfil de desempenho.

## 1. Especifique a jornada e a pergunta

“A aplicação está lenta” ainda não é uma hipótese testável. Transforme o relato:

```text
Dado um catálogo sintético de 10.000 sessões,
no navegador e equipamento de referência,
quando o usuário digita três letras no filtro,
então o resultado visível deve estabilizar em até 100 ms no p95,
sem perder foco nem bloquear a digitação por mais de 50 ms.
```

A especificação contém conjunto de dados, ambiente, ação, marco inicial/final e
limiar. Para inicialização, decida se o fim é “HTML recebido”, “primeira pintura”
ou “interface utilizável”; são fenômenos diferentes.

Métricas comuns:

| Dimensão | Pergunta |
|---|---|
| latência | quanto uma operação individual demora? |
| throughput | quantas operações são concluídas por unidade de tempo? |
| responsividade | por quanto tempo a interface deixa de responder? |
| memória | qual pico, estado estável e crescimento após repetição? |
| tamanho | quantos bytes precisam ser distribuídos, lidos ou analisados? |
| erro | quantas operações falham sob a carga definida? |

Otimizar throughput pode piorar latência individual ao agrupar trabalho. Cache
pode reduzir CPU e aumentar memória. AOT pode diminuir início e aumentar tamanho
do pacote. Orçamento explicita qual troca é aceitável.

## 2. Orçamento de desempenho

Um orçamento reúne limites ligados à experiência:

```text
Ambiente: navegador suportado, perfil novo, equipamento de referência
Dados: 10.000 sessões sintéticas, títulos ASCII de 10 a 80 unidades UTF-16

- interface utilizável: p95 <= 1,5 s
- resposta visual a uma tecla: nenhuma tarefa principal > 50 ms
- filtro estabilizado: p95 <= 100 ms
- exportação JSON: p95 <= 750 ms e progresso/cancelamento acima disso
- memória após 30 ciclos de importar/limpar: sem tendência crescente > 10%
- artefato inicial comprimido: <= 200 KiB
```

Os números são exemplos, não leis. Defina-os com pesquisa, capacidade do produto
e equipamentos reais. Registre data e método: um limite sem ambiente não é
reproduzível. Inclua acessibilidade; uma “otimização” que remove anúncio ou foco
correto não passou no orçamento de qualidade.

Distribua o orçamento por componentes com folga. Se toda camada consome 100% do
limite, qualquer ruído quebra a jornada. Quando o limite deixa de representar o
público, altere-o por decisão documentada, não para tornar uma regressão verde.

## 3. Baseline e experimento

Antes da mudança:

1. fixe código, ferramenta, dados e configuração;
2. aqueça o runtime quando a pergunta não for cold start;
3. execute repetições suficientes;
4. registre medidas brutas, não apenas o resumo;
5. calcule mediana e percentis relevantes;
6. inspecione variação e outliers antes de descartá-los;
7. salve o baseline junto da hipótese.

Média pode esconder cauda: nove operações de 10 ms e uma de 910 ms têm média de
100 ms, embora 90% pareçam instantâneas e uma seja péssima. Mediana descreve o
centro; p95/p99 expõem a cauda, desde que haja amostra suficiente. Com dez valores,
um “p99” sofisticado transmite precisão que o experimento não possui.

Um microbenchmark JavaScript simples pode medir uma função pura:

```js
import {performance} from "node:perf_hooks";

function measure(label, operation, iterations = 100) {
  const samples = [];
  let observed;
  for (let index = 0; index < iterations; index += 1) {
    const start = performance.now();
    observed = operation();
    samples.push(performance.now() - start);
  }
  samples.sort((a, b) => a - b);
  const percentile = value => samples[Math.ceil(value * samples.length) - 1];
  return {label, observed, median: percentile(0.5), p95: percentile(0.95)};
}
```

Consuma o resultado (`observed`) para reduzir o risco de medir trabalho removido
por otimização. Não coloque `console.log` dentro da região medida. Ainda assim,
microbenchmark não representa DOM, armazenamento e percepção; confirme a jornada
integrada.

## 4. Profile antes de editar

Ferramentas diferentes respondem perguntas diferentes:

| Ferramenta | Mostra | Não conclui sozinha |
|---|---|---|
| CPU profiler/amostragem | onde o tempo de CPU se concentra | por que existe espera externa |
| tracing/timeline | sequência de tarefas, renderização e espera | qual algoritmo é ideal |
| contador de alocações | onde objetos são criados | quais permanecem vivos |
| heap snapshot | objetos retidos e caminhos de referência | quando foram criados |
| benchmark | duração/throughput do cenário | experiência completa do usuário |
| tamanho de bundle/pacote | contribuição por arquivo/dependência | custo de execução real |

Nos ecossistemas, procure ferramentas mantidas pelo runtime: `cProfile`/profilers
de Python, Java Flight Recorder/profilers da JVM, ferramentas do compilador e
profiler em C, `dotnet-trace`/`dotnet-counters` e painéis Performance/Memory do
navegador. O procedimento é mais durável do que decorar uma interface:

1. reproduza no cenário especificado;
2. marque início e fim da jornada;
3. capture sem alterar muitas variáveis;
4. localize caminho quente, alocação ou espera dominante;
5. formule uma causa provável;
6. mude uma coisa;
7. refaça correção, medição e perfil.

Um perfil é evidência para uma hipótese, não prova automática de causalidade.

## 5. Do perfil à explicação

Suponha que filtrar 10.000 sessões esteja lento. Possibilidades diferentes podem
produzir o mesmo sintoma:

- normalizar títulos novamente a cada tecla;
- ordenar a coleção inteira a cada renderização;
- reconstruir todos os nós do DOM;
- executar múltiplos listeners para o mesmo evento;
- persistir a lista inteira dentro do handler;
- medir com DevTools ou logs que distorcem o cenário.

Meça por camada. Instrumente temporariamente `deriveVisibleSessions`, renderização
e persistência com marcas estáveis. Se 90% está no DOM, trocar o algoritmo de
normalização não resolve a jornada. Pela ideia de Amdahl, o ganho total é limitado
pela parte que você de fato melhora. Acelerar dez vezes os 10% de uma operação
reduz o total de 100 unidades para aproximadamente 91, não para 10.

## 6. Otimizações algorítmicas e de representação

Primeiro elimine trabalho:

- calcule valor derivado uma vez por mudança relevante;
- use `Map`/`Set` quando a semântica pede consulta por chave/pertencimento;
- evite ordenar quando inserção já mantém a ordem necessária;
- normalize texto na fronteira adequada e preserve o valor de exibição;
- processe somente campos necessários;
- imponha paginação ou limite quando a jornada não precisa de tudo;
- escolha formato de dados compatível com acesso real.

Depois reduza custo do trabalho restante. Estrutura auxiliar acelera leitura, mas
exige memória e sincronização. Memoização serve quando entrada se repete e a chave
é estável; cache sem limite transforma ganho inicial em vazamento operacional.
Toda cache precisa de tamanho máximo, política de descarte, invalidação e métrica
de acerto. Se invalidar é mais caro ou arriscado do que recalcular, não use cache.

## 7. Responsividade na interface

No navegador, uma tarefa longa impede que eventos, foco e pintura avancem. As
estratégias dependem da semântica:

- **debounce:** espera pausa; útil para consulta que não precisa acompanhar cada
  tecla, mas adiciona atraso deliberado;
- **throttle:** limita frequência; útil para atualização contínua aproximada;
- **processamento incremental:** divide trabalho e permite feedback/cancelamento;
- **virtualização:** renderiza janela visível; exige cuidado com foco, leitura e
  dimensão para não destruir acessibilidade;
- **carregamento sob demanda:** adia código/dados; pode trocar início rápido por
  espera posterior e precisa de estado de erro.

Não use debounce para validação que deve responder imediatamente. Não virtualize
uma lista pequena. Não remova elementos focados durante uma renderização. Para o
Study Desk, um filtro rápido com 10.000 itens pode começar por valor derivado
eficiente e atualização agrupada; virtualização só entra depois de medir o custo
real e testar teclado/leitor de tela.

Skeleton ou spinner não torna operação mais rápida, mas pode tornar o estado
compreensível. Mostre progresso determinável quando souber total, ofereça
cancelamento quando a ação for longa e preserve o conteúdo anterior quando isso
reduzir desorientação.

## 8. Memória e vazamentos de ciclo de vida

Uso alto não é automaticamente vazamento. Vazamento é memória que deveria estar
liberada mas permanece alcançável. Teste por ciclos:

1. abra e feche a mesma visão;
2. force apenas o mecanismo de coleta disponível na ferramenta de laboratório,
   sem criar dependência disso no produto;
3. capture snapshots comparáveis;
4. repita 20–30 vezes;
5. observe tendência e caminhos de retenção.

Fontes comuns em UI: listeners não removidos, timers, subscribers, closures que
capturam grandes coleções, nós destacados ainda referenciados e caches ilimitados.
Um snapshot mostra que o objeto está retido; o caminho até a raiz explica por
quem. Corrija o ciclo de vida e execute novamente a jornada funcional.

No sistema de plugins do capítulo 12, cada registro precisa retornar cleanup. No
Study Desk, listeners globais devem ser registrados uma vez ou removidos. Não
“resolva” vazamento apagando estado que o usuário espera conservar.

## 9. Regressão sem benchmark instável

Tempos absolutos em CI compartilhada variam. Combine técnicas:

- teste determinístico de complexidade estrutural, como número de chamadas;
- orçamento largo para detectar regressão grosseira, não diferenças mínimas;
- benchmark dedicado em ambiente controlado para decisões finas;
- comparação com baseline executado na mesma rodada;
- tendência ao longo do tempo, com intervalo e investigação humana;
- limite de bundle e contagem de assets, que são mais estáveis.

Uma falha de performance deve mostrar cenário, amostras, baseline e valor atual.
Reexecutar até passar apaga evidência. Primeiro descubra se houve ruído, mudança
de ambiente ou regressão real.

## 10. Roteiro de diagnóstico

Quando uma jornada viola o orçamento:

1. confirme que é a mesma versão, dataset e ambiente;
2. separe cold start de execução aquecida;
3. identifique se o limite é CPU, espera, renderização, memória ou tamanho;
4. procure erro/retry que se apresenta como lentidão;
5. capture perfil na jornada, não em um exemplo menor;
6. compare o maior contribuinte com o baseline;
7. verifique se instrumentação mudou o resultado;
8. aplique uma alteração e rode testes de correção/acessibilidade;
9. repita medidas brutas e calcule o mesmo resumo;
10. registre ganho, custo e condição em que ele existe.

Pare quando o orçamento estiver atendido com margem razoável. Código mais
complexo sem impacto material é dívida, não vitória.

## Exercícios em três níveis

### Nível 1 — Orçamento e baseline

Defina três jornadas do Study Desk, gere conjuntos sintéticos de 100, 1.000 e
10.000 sessões e escreva ambiente, marcos e orçamentos. Colete no mínimo 30
amostras para a operação principal.

**Aceite:** dados são reproduzíveis; medidas brutas acompanham mediana/p95; cold e
warm não se misturam; o orçamento inclui responsividade e correção funcional.

### Nível 2 — Perfil e melhoria comprovada

Escolha a jornada que mais excede o orçamento. Capture timeline ou CPU profile,
formule a causa, altere apenas o maior contribuinte e compare antes/depois.

**Aceite:** o relatório relaciona perfil à mudança; testes permanecem verdes; a
melhora aparece em repetição independente; custo em memória/tamanho/manutenção é
declarado; acessibilidade por teclado é retestada.

### Nível 3 — Memória e porta de regressão

Crie uma falha de laboratório com listener ou cache não liberado, detecte-a em 30
ciclos, corrija o lifecycle e acrescente uma verificação de regressão adequada à
CI ou ao ambiente de benchmark.

**Aceite:** snapshots mostram o caminho de retenção antes e ausência de tendência
depois; a verificação não depende de limiar irreal; existe procedimento para
distinguir ruído de regressão; nenhuma sessão real entra nos artefatos.

## Checklist de conclusão

- [ ] A métrica representa uma jornada e possui início/fim inequívocos.
- [ ] Ambiente, dados, versão e configuração estão registrados.
- [ ] Baseline contém medidas brutas, mediana e percentil apropriado.
- [ ] Sei qual ferramenta responde à pergunta atual.
- [ ] O perfil foi capturado na jornada que apresenta o problema.
- [ ] A mudança ataca o maior contribuinte observado.
- [ ] Ganho foi confirmado com o mesmo método e repetição independente.
- [ ] Correção, acessibilidade e consumo de memória continuam aceitos.
- [ ] Cache possui limite, invalidação e motivo mensurado.
- [ ] Listener, timer e assinatura têm lifecycle de descarte.
- [ ] A porta de regressão considera variação do ambiente.
- [ ] O relatório registra também trade-offs e condições do ganho.

O objetivo do profiling não é produzir um gráfico bonito. É encurtar o caminho
entre um sintoma percebido, uma causa demonstrável e uma melhoria verificável.
