# Respostas orientativas

Consulte depois da primeira tentativa. Estas respostas descrevem propriedades,
decisões e evidências mínimas; elas não substituem implementação, medição ou
teste manual. Uma solução diferente é válida quando preserva o contrato e
explica o trade-off.

## Capítulos 00–16

### 00 — Do código ao produto

- **Nível 1:** um contrato útil nomeia usuário, tarefa, entradas, saídas,
  pré/pós-condições, limites, falhas, recuperação e não objetivos. “Rápido” vira
  cenário, ambiente, volume, percentil e limite.
- **Nível 2:** `StudySession` protege título/minutos no núcleo e recebe relógio e
  ID injetados. A fatia `add` liga entrada, caso de uso, porta e presenter sem o
  domínio importar UI ou arquivo.
- **Nível 3:** a descoberta cobre jornada feliz e falhas, fronteiras e matriz de
  exemplos. A decisão JSON versus memória distingue protótipo descartável de
  dado que exige retenção; hipótese não é apresentada como fato.

### 01 — CLI profissional

- **Nível 1:** a gramática declara posicionais, opções, repetição, `--`, vazio e
  desconhecido. Ajuda mostra propósito, sintaxe, padrões, exemplos e códigos.
- **Nível 2:** o parser produz um objeto tipado; o caso de uso não lê `argv`.
  Texto e JSON apresentam o mesmo resultado. O teste de processo afirma código,
  `stdout` e `stderr` simultaneamente.
- **Nível 3:** compatibilidade mantém alias antigo por período definido, avisa em
  `stderr` e registra remoção. TTY pode habilitar cor/interação, mas nunca muda a
  semântica ou quebra automação.

### 02 — Configuração, ambientes e segredos

- **Nível 1:** a matriz diferencia ausência, vazio, inválido e valor efetivo. A
  política típica é `CLI > ambiente > arquivo > padrão`, mas precisa estar
  documentada e testada.
- **Nível 2:** coleta, resolução, conversão e validação são fases separadas. O
  resultado é tipado/imutável e inclui proveniência sanitizada; falha ocorre
  antes de inicializar efeitos.
- **Nível 3:** segredo possui origem, escopo, consumidor, rotação e revogação.
  Valor-canário prova ausência em saídas e diagnóstico. `.env` é conveniência
  local ignorada pelo Git, não cofre nem formato universal.

### 03 — Validação, erros e feedback

- **Nível 1:** mensagem acionável diz o que falhou, por que pode ser corrigido e
  qual próximo passo; não culpa o usuário nem expõe detalhe interno.
- **Nível 2:** erros de campo preservam entrada e são associados aos controles.
  Tipos/códigos distintos evitam retry em entrada inválida e permitem tradução
  sem analisar texto humano.
- **Nível 3:** importação é validada em cópia, resumida e confirmada antes do
  commit. Cancelamento distingue interromper o interesse de interromper um efeito
  que pode já ter acontecido.

### 04 — Arquivos, serialização e dados locais

- **Nível 1:** schema inclui versão, tipos, limites, datas e política de campos
  desconhecidos. JSON sintaticamente válido ainda pode ser domínio inválido.
- **Nível 2:** round-trip verifica equivalência semântica. Escrita usa novo
  estado validado e preserva o anterior até o ponto de commit; fixtures cobrem
  truncamento, excesso, duplicata e versão futura.
- **Nível 3:** migração `v1 → v2` é pura, valida entrada/saída e conserva backup.
  JSON favorece documento pequeno/exportável; SQLite favorece consulta,
  transação e atualização parcial — a escolha parte do acesso real.

### 05 — Estado, eventos e fluxo de dados

- **Nível 1:** estado representa `idle/loading/success/error/cancelled` sem flags
  contraditórias; valores calculáveis são selectors, não segunda fonte de verdade.
- **Nível 2:** reducer é puro e rejeita evento impossível importante. Testes
  provam que o estado anterior não foi alterado.
- **Nível 3:** request ID impede resposta antiga de vencer. Operação otimista
  guarda snapshot ou inversa e trata confirmação, rollback e conflito como
  estados observáveis.

### 06 — GUI desktop

- **Nível 1:** escolha de toolkit considera plataformas, licença, distribuição,
  acessibilidade, equipe e ciclo de vida — não apenas aparência do exemplo.
- **Nível 2:** view liga widgets; presenter expõe estado/comandos; domínio não
  conhece thread de UI. Trabalho longo usa o mecanismo do toolkit e retorna à
  thread correta.
- **Nível 3:** teclado, foco, escala e leitor de tela compõem o aceite. Fechamento
  oferece salvar/descartar/cancelar; falha ao salvar mantém janela e dado.

### 07 — Interfaces web

- **Nível 1:** `form`, `label`, `button`, headings e landmarks expressam a
  estrutura antes de ARIA. CSS parte de conteúdo, unidades relativas e reflow.
- **Nível 2:** reducer e casos de uso não acessam `document`; render recebe estado
  e usa `textContent` para dado externo. Erro não apaga formulário.
- **Nível 3:** progressive enhancement define uma base honesta; quando JavaScript
  é requisito, carregamento/falha são estados explícitos e testáveis.

### 08 — Acessibilidade e responsividade

- **Nível 1:** nome, papel, valor e estado vêm primeiro de elementos nativos.
  Contraste ou automação isolados não provam acessibilidade.
- **Nível 2:** sequência por teclado, foco visível, retorno após atualização,
  erro associado/anunciado e zoom 400% são evidências manuais mínimas.
- **Nível 3:** componente complexo só é construído com padrão conhecido, matriz
  de teclado e tecnologias assistivas. Pseudolocalização e preferências de
  movimento/cores entram no teste.

### 09 — Clientes de API e offline

- **Nível 1:** primeira carga, refresh, vazio, stale, offline, erro e conflito
  são estados distintos. Refresh preserva dado anterior.
- **Nível 2:** timeout encerra espera; cancelamento encerra interesse; request ID
  evita corrida. Retry usa limite/backoff/jitter e apenas operação idempotente ou
  chave reconhecida pelo servidor.
- **Nível 3:** fila persiste IDs e estados `pending/sending/confirmed/conflict`.
  Reinício não duplica confirmação; conflito preserva versões e pede política.

### 10 — Internacionalização, tempo e dinheiro

- **Nível 1:** catálogo e regras plurais substituem concatenação. Locale afeta
  texto, número, data, moeda e ordenação, não somente tradução.
- **Nível 2:** instante representa evento ocorrido; agenda civil preserva
  data/hora local e zona IANA. Dinheiro usa inteiro menor/decimal e arredondamento
  explícito.
- **Nível 3:** pseudolocale revela texto embutido e layout rígido. Testes cobrem
  transição de offset, separadores, zero/um/muitos, fallback e collation.

### 11 — Logs, diagnóstico e observabilidade

- **Nível 1:** evento estruturado tem nome/versão, nível, instante, correlação e
  razão enumerada. Mensagem humana não é o schema.
- **Nível 2:** política minimiza dados e define retenção. Canário não aparece em
  log, exceção ou pacote; conteúdo livre e token ficam fora.
- **Nível 3:** pacote de suporte é local, pré-visualizável e selecionável. Métrica
  só é útil quando ligada a decisão, limite e runbook.

### 12 — Plugins e extensibilidade

- **Nível 1:** primeiro compare configuração, Strategy e processo. Plugin
  in-process só se justifica para extensão profunda e confiável.
- **Nível 2:** manifesto declara ID, versões e capacidades; registry rejeita
  duplicata/incompatibilidade, ordena deterministicamente e reverte inicialização
  parcial.
- **Nível 3:** host/API/plugin evoluem separadamente. Suíte de contrato cobre
  cancelamento, dado excessivo e falha; desativar todas as extensões mantém o
  núcleo correto. Processo separado melhora contenção, não é sandbox automática.

### 13 — Empacotamento, distribuição e atualização

- **Nível 1:** biblioteca, CLI, desktop e web têm artefatos/expectativas distintos.
  O contrato inclui instalação, primeira execução, upgrade, remoção e dados.
- **Nível 2:** build fecha toolchain, lockfile, flags e conteúdo; artefato recebe
  hash/inventário e é testado fora do checkout.
- **Nível 3:** assinatura ocorre em etapa protegida após testes. Atualização é
  máquina de estados; migração, rollout e rollback possuem critérios e não
  sobrescrevem formato futuro.

### 14 — Desempenho percebido e profiling

- **Nível 1:** orçamento inclui ambiente, volume, interação, percentil e limite.
  Média ou execução única não bastam.
- **Nível 2:** baseline vem antes do profiler; perfil localiza o caminho
  dominante; uma mudança é medida sob o mesmo cenário e seguida de teste funcional.
- **Nível 3:** responsividade separa trabalho, agenda e renderização. Memória é
  observada após ciclos/GC comparáveis; benchmark tolera ruído sem esconder
  regressão grande.

### 15 — Qualidade, release e suporte

- **Nível 1:** release gate cobre artefato, schema, acessibilidade, diagnóstico,
  desempenho, segurança de dados, documentação e suporte.
- **Nível 2:** matriz app/schema/plugin/plataforma torna compatibilidade explícita.
  Release note descreve benefício/impacto, não classes internas.
- **Nível 3:** rollout possui observação, condição de abortar e responsável;
  rollback é ensaiado. Suporte pede versão, passos e diagnóstico sanitizado,
  nunca senha ou documento pessoal.

### 16 — Projetos e avaliação

- **Nível 1:** proposta pequena define quatro casos essenciais, não objetivos,
  dados, falhas e evidência. Mais telas não compensam perda silenciosa.
- **Nível 2:** walking skeleton atravessa entrada, caso de uso, porta e saída com
  adapter falso. Cada evolução preserva suíte e documentação.
- **Nível 3:** capstone funciona fora do workspace, por teclado, com entrada
  incompatível e falha de persistência/rede. Instalação, diagnóstico, profiling,
  upgrade e rollback são demonstrados por outra pessoa.

## Caderno de 32 práticas

### 01–08 — Contrato, CLI, configuração e erros

1. Cada adjetivo precisa de jornada, ambiente, volume, medida, percentil/limite e
   condição de invalidação; “pareceu rápido” não é evidência.
2. Conversão em lote declara unidade de commit. O item 87 pode abortar tudo,
   deixar saída parcial identificada ou continuar e gerar relatório; misturar as
   três políticas silenciosamente é o erro.
3. A gramática define subcomando, opção repetível, `--`, stdin e duplicata.
   Vetores negativos devem ser rejeitados antes de efeito.
4. Teste via subprocesso captura três coisas: código, bytes de `stdout` e bytes de
   `stderr`. Chamar somente `main()` não prova contrato do processo.
5. Resolva fontes em ordem, mas valide o valor vencedor. Documente se fonte de
   maior precedência válida pode ocultar fonte inferior inválida.
6. Faça o canário atravessar uma credencial falsa e procure em todas as saídas.
   O teste deve imprimir apenas onde encontrou, não o segredo completo.
7. Entrada/domínio não recebem retry; dependência transitória pode receber;
   conflito pede reconciliação; defeito exige correção/rollback.
8. Parse e valide em estrutura nova. O ponteiro/conteúdo confirmado permanece
   igual se o último item falhar; commit acontece uma vez no final.

### 09–16 — Dados, estado e GUI

9. Schema exato recusa ausência e excesso; limites incluem coleção e documento.
   Importação/exportação chamam o mesmo validador.
10. Round-trip compara significado. Bytes podem mudar por espaços/ordem; se byte
    estável for requisito, canonicalização precisa ser especificada.
11. Migração pura não toca o original, recebe `v1`, produz/valida `v2` e é
    testada com limites. Reaplicar deve recusar `v2` ou ser idempotente por regra.
12. O resultado depende do limite: rename pode ser atômico no mesmo filesystem;
    Storage de uma chave troca snapshot; nenhum deles oferece transação mágica
    entre recursos distintos.
13. Tabela de transições é o oráculo. `SUCCESS` em `idle` deve falhar ou ter
    política explícita, não ser ignorado por acidente.
14. Controle as promises/futuros: libere resposta 2 e depois 1. Somente o ID atual
    altera estado; nenhum `sleep` é necessário.
15. Presenter expõe dados/comandos e recebe portas. A view falsa registra chamadas;
    domínio e teste não importam widget nem exigem display.
16. Fechamento com dirty state oferece três escolhas. Se salvar falha, a janela
    permanece e permite retry/exportação; “fechar mesmo assim” exige confirmação.

### 17–25 — Web, acessibilidade, resiliência e locale

17. Elementos nativos removem handlers de teclado e ARIA reconstruída. A árvore
    deve mostrar nome/papel corretos e Enter/Espaço conforme semântica.
18. O texto parecido com HTML aparece literalmente via `textContent`. Busque no
    código por `innerHTML`, `insertAdjacentHTML` ou parsing usado com dado externo.
19. O roteiro registra sequência e destino após cada ação. Modal devolve foco ao
    acionador; item removido move foco para vizinho lógico ou título da região.
20. Com 400%/pseudo, conteúdo reflowa e ações permanecem visíveis. Tabela pode ter
    região própria rolável e rotulada, sem forçar toda a página.
21. Use união discriminada, não flags independentes. `refreshing` carrega dado;
    `loadingInitial` não; `staleOffline` informa idade; `conflict` preserva versões.
22. Relógio/scheduler e jitter são injetados. O teste afirma atrasos, máximo,
    desistência e cancelamento instantaneamente.
23. IDs de operação persistem antes do envio. Depois de reiniciar, confirmação da
    mesma chave marca o item; não cria outro. Conflito guarda local/remoto.
24. “24 horas” usa duração sobre instante. “Amanhã 09:00” preserva intenção civil,
    zona e política para horário inexistente/ambíguo.
25. Catálogo usa plural rules; apresentação usa locale. Cálculo mantém inteiro
    menor/decimal, e arredondamento acontece em fronteira documentada.

### 26–32 — Diagnóstico, extensão e entrega

26. `document_import_failed.v1` contém correlação, etapa, razão e limites, não o
    conteúdo. Mensagem traduzida pode mudar sem quebrar consumidor do evento.
27. Pacote tem manifesto e prévia, funciona offline e nada envia. Itens são
    desmarcáveis e o teste procura canário/paths pessoais antes de fechar arquivo.
28. Registry valida antes de ativar, ordena por chave estável e captura falha com
    ID/fase. Remover plugin defeituoso restaura o host e não deixa contribuição.
29. Cada célula diz aceita/migra/recusa. Downgrade sobre schema futuro recusa
    preservando; não tenta “entender o suficiente” e sobrescrever.
30. Artefato contém só inventário esperado, recebe hash e executa sem checkout,
    cache global ou caminho absoluto. Esse teste encontra dependência implícita.
31. Relatório guarda hipótese/baseline/perfil/alteração/nova medida e correção.
    Se o perfil não sustenta a causa, a hipótese é descartada.
32. O ensaio registra sinal de abortar e pós-verificação. Versão antiga não abre
    o dado futuro para escrita; recuperação usa backup/migração compatível.

## Orientação para os laboratórios

### Lab 01

Avalie o processo, não apenas funções. `focus-report` deve ter contrato antes do
código, fixtures, JSON analisável, precedência e falhas que deixam `stdout` vazio.
Comparar linguagens significa identificar onde a mesma garantia vive, não contar
linhas ou escolher vencedora.

### Lab 02

O ponto central é o commit. Uma importação cujo último item falha preserva o
snapshot anterior. Reducer e presenter rodam sem Storage/widget. O ADR relaciona
escolha de persistência ao padrão de acesso e à recuperação.

### Lab 03

Aprovação exige teclado, foco, reflow e status verificados manualmente, mais
adapter de rede determinístico. “Offline” tem limite honesto. Retry não duplica
escrita; locale e zona são dados do contrato, não decoração final.

### Lab 04

O canário precisa estar ausente de todas as evidências. Plugin defeituoso não
derruba o host. O artefato executa fora do workspace. A otimização apresenta
baseline/perfil/depois, e o rollback é ensaiado com dado versionado.

### Lab 05

Use a rubrica e os requisitos eliminatórios. Uma aplicação pequena com quatro
casos completos vale mais que muitas telas sem recuperação. A defesa técnica
deve mostrar falha real, preservação do estado, diagnóstico, acessibilidade,
artefato e rollback reproduzíveis por quem avalia.
