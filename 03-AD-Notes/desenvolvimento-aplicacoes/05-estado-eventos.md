# 05 — Estado, eventos e fluxo de dados

Interfaces reagem a eventos ao longo do tempo. Sem um modelo explícito, cada ação
altera variáveis livremente e combinações impossíveis aparecem: “carregando” e
“salvo” ao mesmo tempo, erro antigo depois de um novo sucesso ou botão habilitado
durante confirmação. Neste capítulo, o Study Desk ganha estado mínimo, eventos
tipados, reducer puro e efeitos controlados.

## Objetivos de aprendizagem

Ao final, você deverá conseguir:

- separar estado de domínio, apresentação, operação e valores derivados;
- modelar estados mutuamente exclusivos com tipos discriminados;
- nomear eventos como intenções ou fatos e definir seus contratos;
- implementar transições puras e manter efeitos nas bordas;
- impedir respostas obsoletas, submissão duplicada e transições proibidas;
- avaliar atualização otimista, rollback e compensação com seus trade-offs.

## Pré-requisitos

Use o resultado tipado do capítulo 03 e a persistência do capítulo 04. O exemplo
ampliado deste capítulo adota, como evolução proposta, um repositório revisionado
que não existe no schema v1 executável. Você deve conhecer funções puras, tipos,
coleções imutáveis e testes. O foco é a lógica da aplicação; frameworks de GUI e
web entram nos próximos capítulos.

## Modelo mental: estado + evento = novo estado e comandos

Uma aplicação interativa pode ser vista como uma função:

```text
update(estado_atual, evento) -> (novo_estado, comandos)
```

O reducer calcula. O runtime executa comandos externos e converte seus resultados
em novos eventos:

```text
evento -> reducer puro -> novo estado -> renderização
                    \-> comando -> adaptador -> evento de resultado --+
```

Esse ciclo cria rastreabilidade. Dado estado inicial e sequência de eventos, o
resultado deve ser determinístico. Relógio, IDs, leitura e escrita entram como
resultados de comandos, não como chamadas escondidas dentro do reducer.

## Inventário de estado

Classifique antes de criar variáveis:

| Categoria | Exemplos no Study Desk | Ciclo de vida |
|---|---|---|
| domínio | sessões confirmadas, revisão | persistente |
| apresentação | filtro, item selecionado | enquanto a interface vive |
| entrada | título e minutos digitados | até salvar/cancelar |
| operação | idle, saving, failed | durante um fluxo |
| derivado | total filtrado, botão habilitado | recalculado |

Não armazene `filteredSessions`, `totalMinutes` e `canSubmit` se podem ser
derivados de forma barata. Cópias exigem sincronização e permitem divergência:

```javascript
const visibleSessions = state.sessions.filter((session) =>
  session.title.toLocaleLowerCase().includes(state.query.toLocaleLowerCase())
);

const totalMinutes = visibleSessions.reduce(
  (total, session) => total + session.minutes,
  0
);

const canSubmit =
  state.save.status !== "saving" &&
  state.form.title.trim().length > 0 &&
  Number.isInteger(state.form.minutes);
```

Derivação cara pode ser memorizada com chave explícita, mas o cache continua
descartável; a fonte da verdade permanece mínima.

## Modele estados, não combinações de booleanos

Três booleanos `loading`, `hasError` e `hasData` formam oito combinações, várias
sem sentido. Um tipo discriminado limita as possibilidades:

```typescript
type SaveState =
  | { status: "idle" }
  | { status: "saving"; operationId: string; draftId: string }
  | { status: "saved"; sessionId: string }
  | { status: "failed"; errors: readonly [AppError, ...AppError[]]; draftId: string }
  | { status: "cancelling"; operationId: string };
```

Uma variante contém apenas os dados que fazem sentido naquele estado. Não existe
`failed` sem erros nem `saving` sem identidade da operação. Em Java, use tipos
selados; em C#, records derivados; em Python, dataclasses e união. Mesmo sem
checagem estática, valide o discriminante na fronteira.

## Eventos: intenção versus fato

Um evento de interface pode representar intenção:

```text
TITLE_CHANGED { value }
SAVE_REQUESTED
CANCEL_REQUESTED
```

Um evento retornado por efeito representa algo que ocorreu:

```text
SAVE_SUCCEEDED { operationId, session, revision }
SAVE_FAILED { operationId, errors }
SAVE_CANCELLED { operationId }
```

Nomes no passado não tornam um fato verdadeiro. `SESSION_SAVED` só deve nascer
depois de a porta de persistência confirmar. O clique é `SAVE_REQUESTED`, não
`SESSION_SAVED`.

Todo evento tem contrato:

- emissor autorizado;
- payload mínimo e validado;
- estados em que é aceito;
- transição resultante;
- comandos produzidos;
- comportamento se chegar atrasado ou repetido.

Evento não é sinônimo de event sourcing. Aqui ele organiza transições em
memória; o arquivo atual continua guardando o estado materializado. Persistir todo
evento como fonte da verdade é outra arquitetura, com ordenação, versão e replay
próprios.

## Tabela da máquina de estados

Antes do código, escreva as transições da operação de salvar:

| Estado | Evento | Próximo estado | Comando/observação |
|---|---|---|---|
| idle | `SAVE_REQUESTED` válido | saving | persistir candidato |
| idle | `SAVE_REQUESTED` inválido | failed | nenhum efeito |
| saving | `SAVE_REQUESTED` | saving | ignorar ou sinalizar já em curso |
| saving | `SAVE_SUCCEEDED` correspondente | saved | atualizar sessões/revisão |
| saving | `SAVE_FAILED` correspondente | failed | preservar rascunho |
| saving | `CANCEL_REQUESTED` | cancelling | solicitar cancelamento |
| cancelling | `SAVE_CANCELLED` correspondente | idle | preservar rascunho |
| failed | `SAVE_REQUESTED` válido | saving | nova identidade de operação |
| saved | `TITLE_CHANGED` | idle | iniciar novo rascunho |

Eventos de resultado cujo `operationId` não coincide com a operação atual são
obsoletos e não alteram o estado. Registre uma contagem diagnóstica sem tratar
isso automaticamente como defeito.

## Reducer puro com comandos explícitos

Um exemplo reduzido em JavaScript:

```javascript
function update(state, event) {
  switch (event.type) {
    case "TITLE_CHANGED":
      return [{
        ...state,
        form: { ...state.form, title: event.value },
        save: { status: "idle" }
      }, []];

    case "SAVE_REQUESTED": {
      if (state.save.status === "saving") return [state, []];
      const errors = validateDraft(state.form);
      if (errors.length > 0) {
        return [{ ...state, save: { status: "failed", errors, draftId: state.form.id } }, []];
      }
      const operationId = event.operationId;
      return [
        { ...state, save: { status: "saving", operationId, draftId: state.form.id } },
        [{ type: "PERSIST_SESSION", operationId, draft: state.form, revision: state.revision }]
      ];
    }

    case "SAVE_SUCCEEDED":
      if (state.save.status !== "saving" ||
          state.save.operationId !== event.operationId) return [state, []];
      return [{
        ...state,
        sessions: [...state.sessions, event.session],
        revision: event.revision,
        form: emptyDraft(),
        save: { status: "saved", sessionId: event.session.id }
      }, []];

    default:
      return [state, []];
  }
}
```

`validateDraft`, `emptyDraft` e o gerador de `operationId` precisam ser puros ou
ter suas entradas fornecidas. O comando `PERSIST_SESSION` descreve intenção; um
interpretador chama o repositório e emite sucesso, conflito ou falha.

Em aplicação pequena, retornar comandos formalmente pode ser excessivo. Uma
camada de controlador que chama reducer, executa efeito e despacha resultado
preserva o mesmo princípio. O requisito é manter I/O fora da função de transição.

## Invariantes: base atual e evolução proposta

O Study Desk executável deste curso mantém hoje `sessions`, `query` e `theme`.
Após qualquer evento aceito nessa base:

- IDs de sessão confirmada são únicos;
- estado e coleções expostas pelo domínio são imutáveis;
- filtro e resumo são derivados das sessões, sem segunda fonte de verdade;
- evento desconhecido ou payload inválido falha antes do commit;
- falha do repositório restaura a referência do estado anterior.

O modelo ampliado do exemplo anterior é uma **evolução proposta**, ainda não
implementada em `projetos/study-desk/src/domain.mjs`. Se o aluno adicionar
salvamento assíncrono, revisão e cancelamento, então passam a valer também estas
invariantes:

- `revision` nunca diminui;
- somente uma operação de salvamento está ativa;
- `saving` e `cancelling` sempre possuem `operationId`;
- rascunho não some em falha ou cancelamento;
- sessão só entra na lista após confirmação do repositório;
- evento obsoleto não muda sessões, revisão nem feedback atual;
- valores derivados correspondem ao estado fonte.

Teste invariantes sobre sequências, não apenas eventos isolados. Exemplo:
editar → salvar → cancelar → resposta tardia → editar novamente.

## Fluxo unidirecional e estado local

Fluxo unidirecional não exige loja global. Estado de um campo que somente um
componente usa deve permanecer perto dele. Ele sobe quando duas partes precisam
coordenar uma fonte da verdade. Estado global excessivo aumenta acoplamento,
renderizações e sequências possíveis.

Pergunte antes de promover estado:

1. quem precisa ler?
2. quem pode alterar?
3. qual é a fonte da verdade?
4. precisa sobreviver à interface?
5. pode ser derivado?
6. qual evento explica a mudança?

O repositório persistente não é automaticamente a loja de UI. A UI pode manter
rascunho que ainda não pertence ao domínio confirmado.

## Concorrência lógica e resultados fora de ordem

Mesmo sem discutir threads, efeitos podem terminar fora da ordem em que foram
iniciados. Considere buscas locais ou importações sucessivas:

```text
op A inicia -> op B inicia -> B termina -> A termina
```

Sem identidade, A sobrescreve resultado mais novo. Soluções:

- cancelar a operação anterior e ainda verificar identidade;
- aceitar somente o `operationId` atual;
- ordenar por revisão quando a semântica permite;
- serializar operações que não podem coexistir.

Cancelamento sozinho não basta: o resultado pode ter sido produzido antes de o
cancelamento ser observado. A verificação no reducer é a última defesa.

## Atualização otimista

Atualização otimista mostra o resultado antes da confirmação. Pode melhorar
fluidez, mas cria dois estados: pendente e confirmado. Exige:

- operação reversível ou compensação conhecida;
- ID idempotente para reconciliar;
- marca visual que não dependa apenas de cor;
- cópia do estado anterior ou inversa da operação;
- tratamento de conflito e falha;
- mensagem clara se ocorrer rollback.

Para o Study Desk atual, salvar uma sessão é síncrono e rápido; o estado novo é
calculado, persistido e só então renderizado. Não existe indicador `saving` na
interface entregue. Uma evolução assíncrona conservadora deveria tornar esse
estado visível e adicionar à lista somente após confirmação. Use otimismo por
medida de experiência, não por padrão.

Em ação irreversível, “rollback” pode ser mentira. Uma operação compensatória
cria um novo fato que reduz o efeito; não apaga necessariamente o anterior.

## Eventos de interface e ciclo de vida

Na futura interface web, não dependa de estrutura acidental do DOM. Use seletores
estáveis, `currentTarget` quando o handler pertence ao controle e passe IDs de
domínio para o evento. Remova listeners, timers e assinaturas quando deixam de ser
necessários.

Evite emitir evento de domínio para cada tecla se somente o rascunho local mudou.
`TITLE_CHANGED` é evento de apresentação; `SESSION_REGISTERED` é fato confirmado.
Essa distinção impede que telemetria, persistência ou plugins confundam intenção
com resultado.

## Falhas comuns e diagnóstico

| Sintoma | Hipótese | Como confirmar |
|---|---|---|
| botão habilita durante save | booleanos independentes | enumere estados alcançáveis |
| erro antigo substitui sucesso | resultado sem `operationId` | inverta ordem em teste controlado |
| sessão aparece duplicada | duplo clique iniciou dois efeitos | conte comandos por evento |
| filtro mostra total errado | valor derivado armazenado | recalcule a partir da fonte |
| teste é intermitente | reducer chama relógio/ID global | injete ambos no evento/comando |
| cancelar apaga rascunho | transição não preserva entrada | compare rascunho antes/depois |

Para depurar, registre em desenvolvimento uma linha segura por transição:
estado anterior, tipo do evento, `operationId`, próximo estado e comandos. Não
registre texto de sessão. Reproduza a sequência em um teste puro; se o reducer
estiver correto, investigue o interpretador do efeito.

## Exercícios em três níveis

### Nível 1 — modelagem

Modele a importação do Study Desk com idle, selecting, validating, preview,
committing, succeeded, failed e cancelled. Produza tabela de transições.

**Critérios de aceite:** cada estado carrega apenas dados válidos; eventos
proibidos têm política; cancelamento antes e depois da confirmação é distinguido.

### Nível 2 — reducer

Implemente o fluxo de `SAVE_REQUESTED` com reducer puro e interpretador falso.
Teste sucesso, validação, conflito, duplo clique e resposta obsoleta.

**Critérios de aceite:** testes não usam temporizador nem arquivo; exatamente um
comando nasce da primeira solicitação; resultado antigo não altera nenhum campo.

### Nível 3 — evolução do Study Desk

Projete uma versão futura e conecte CLI, configuração, repositório revisionado e
máquina de estados. Simule duas edições concorrentes, falha de gravação,
cancelamento e nova tentativa. Não atribua essas capacidades à versão v1.

**Critérios de aceite:** invariantes permanecem verdadeiras para toda sequência;
conflito não perde rascunho; diagnóstico permite reconstruir tipos de eventos sem
expor conteúdo; a apresentação não acessa arquivo diretamente.

## Checklist de domínio

- [ ] Distingo estado persistente, rascunho, operação e valor derivado.
- [ ] Modelo alternativas exclusivas com variantes, não booleanos independentes.
- [ ] Sei diferenciar intenção de interface e fato confirmado.
- [ ] Meu reducer é puro e efeitos retornam como novos eventos.
- [ ] Defino transições permitidas, proibidas, repetidas e obsoletas.
- [ ] Uso identidade de operação para impedir resultados fora de ordem.
- [ ] Avalio atualização otimista pelo custo de rollback e reconciliação.
- [ ] Reproduzo falhas complexas como sequências determinísticas de eventos.
