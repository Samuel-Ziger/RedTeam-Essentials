# 07 — Interfaces web sem esconder os fundamentos

Uma interface web é um documento interativo. HTML comunica estrutura e
significado, CSS organiza apresentação e JavaScript coordena estado, eventos e
efeitos. Frameworks podem automatizar partes desse trabalho, mas não corrigem um
modelo de estado contraditório, um formulário sem contrato ou uma árvore sem
semântica.

O [Study Desk](projetos/study-desk/README.md) usa deliberadamente APIs nativas do
navegador. Ele permite enxergar as fronteiras que continuam presentes em React,
Vue, Angular ou outro framework: estado, renderização, efeitos, persistência e
acessibilidade.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. construir uma página com HTML semântico antes de adicionar comportamento;
2. criar layout fluido orientado pelo conteúdo, sem coordenadas rígidas;
3. separar domínio, estado, renderização, controladores e efeitos;
4. modelar carregamento, vazio, erro, sucesso, edição e confirmação;
5. renderizar texto e URLs sem transformar dado em código;
6. manter formulários utilizáveis durante validação e falhas;
7. testar reducers sem DOM e reservar testes de navegador para integração;
8. diagnosticar renderização repetida, listener duplicado e estado divergente.

## Pré-requisitos e mapa mental

Você deve conhecer HTML básico, seletores CSS, funções e módulos JavaScript, além
do modelo de estado do [capítulo 05](05-estado-eventos.md). Não é preciso conhecer
servidores web ou protocolos em profundidade; a trilha de Redes trata essa base.

```text
documento semântico
  + sistema visual responsivo
  + estado mínimo e transições explícitas
  + eventos traduzidos em intenção
  + efeitos nas fronteiras
  + renderização segura e acessível
  = interface verificável
```

Separe sempre três perguntas. **O que existe?** é respondida pelo HTML. **Como se
apresenta?** pertence ao CSS. **O que muda quando algo acontece?** pertence ao
modelo de estado e ao JavaScript. A separação não precisa ser absoluta, mas deve
deixar claro onde investigar cada falha.

## HTML é a primeira API da interface

Elementos nativos já carregam semântica, comportamento de teclado, nomes e estados
entendidos pelo navegador. Comece pelo fluxo funcional:

```html
<main>
  <h1>Study Desk</h1>

  <form id="session-form">
    <div>
      <label for="title">Assunto</label>
      <input id="title" name="title" required maxlength="80"
             aria-describedby="title-help title-error">
      <p id="title-help">Use um nome curto que você reconheça depois.</p>
      <p id="title-error" role="alert"></p>
    </div>

    <div>
      <label for="minutes">Duração em minutos</label>
      <input id="minutes" name="minutes" type="number"
             min="1" max="1440" required>
    </div>

    <button type="submit">Registrar sessão</button>
  </form>

  <section aria-labelledby="history-title">
    <h2 id="history-title">Histórico</h2>
    <p id="history-status" role="status" aria-live="polite"></p>
    <ul id="session-list"></ul>
  </section>
</main>
```

O `<button>` participa do formulário, recebe foco e responde ao teclado. Uma
`<div>` com clique exigiria reimplementar essas garantias e ainda poderia falhar
em tecnologia assistiva. Use ARIA para complementar uma lacuna, não para trocar
um elemento nativo por uma imitação.

Cabeçalhos descrevem a hierarquia, não o tamanho visual. Uma lista de sessões é
uma lista; navegação é `<nav>`; ação que muda estado é botão; destino navegável é
link. Esse vocabulário melhora acessibilidade, testes e manutenção ao mesmo tempo.

## CSS como sistema, não como coleção de correções

Defina decisões repetidas como propriedades customizadas e deixe o conteúdo
participar do layout:

```css
:root {
  color-scheme: light dark;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --measure: 70rem;
  --accent: #2859c5;
  --danger: #a51d2d;
  --radius: 0.5rem;
}

body {
  margin: 0;
  font: 100%/1.5 system-ui, sans-serif;
}

main {
  width: min(100% - 2rem, var(--measure));
  margin-inline: auto;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
  gap: var(--space-4);
}

:focus-visible {
  outline: 0.2rem solid var(--accent);
  outline-offset: 0.2rem;
}
```

Grid serve bem a relações em duas dimensões; Flexbox, a fluxos em uma dimensão.
Isso não é regra mecânica. O critério é se a estrutura continua compreensível
quando o viewport estreita, a fonte cresce, o idioma expande ou um bloco recebe
conteúdo inesperado.

Evite `height` fixa para texto, tamanho de fonte em pixels como única estratégia e
breakpoints baseados apenas em modelos de aparelhos. Adicione um breakpoint onde
o conteúdo deixa de funcionar. Teste zoom, reflow, preferência por menos movimento
e contraste; o [capítulo 08](08-acessibilidade-responsividade.md) aprofunda o tema.

## Arquitetura JavaScript por responsabilidades

Uma aplicação pequena já se beneficia desta divisão:

```text
domain.js       regras puras e tipos conceituais
state.js        estado inicial e reducer
repository.js   persistência por contrato
view.js         projeção do estado no DOM
controller.js   DOM event -> evento da aplicação
main.js         composição das dependências
```

O reducer não acessa `document`, relógio ou armazenamento:

```javascript
export function reducer(state, event) {
  switch (event.type) {
    case "SESSION_DRAFT_CHANGED":
      return {
        ...state,
        draft: { ...state.draft, [event.field]: event.value },
        phase: "editing",
      };
    case "SESSION_SAVE_STARTED":
      return { ...state, phase: "saving", formError: null };
    case "SESSION_SAVE_SUCCEEDED":
      return {
        ...state,
        phase: "saved",
        sessions: [...state.sessions, event.session],
        draft: { title: "", minutes: "" },
      };
    case "SESSION_SAVE_FAILED":
      return { ...state, phase: "failed", formError: event.message };
    default:
      return state;
  }
}
```

Isso torna transições reproduzíveis. O controlador valida o evento do navegador,
despacha `SESSION_SAVE_STARTED`, chama o repositório e traduz o resultado em
sucesso ou falha. O renderer recebe estado; não consulta armazenamento escondido.

Não use o DOM como banco de dados. Um atributo `data-session-id` pode ligar um
controle à entidade, mas o texto renderizado não deve ser relido para recuperar o
valor original. Também não esconda estados de negócio em classes como `.active`
ou no rótulo de um botão.

## Estado de UI e renderização determinística

Modele estados que a pessoa consegue observar:

| Fase | O que permanece visível | Ação principal | Erro possível |
|---|---|---|---|
| inicial | formulário e orientação | registrar | nenhum |
| salvando | rascunho, indicador | aguardar/cancelar | armazenamento indisponível |
| salvo | lista atualizada | registrar outra | nenhum |
| vazio | explicação | criar primeira sessão | nenhum |
| falha | rascunho e mensagem | corrigir/tentar novamente | falha conhecida |

Renderização determinística significa que o mesmo estado produz a mesma
interface relevante. Isso não exige reconstruir todo o DOM. Atualizações
incrementais são válidas, mas precisam preservar invariantes: IDs únicos,
listeners únicos, foco coerente e atributos acessíveis sincronizados.

Ao remover o item atualmente focado, defina o próximo foco antes da mutação: item
seguinte, anterior ou cabeçalho da lista. Ao abrir um diálogo, associe título e
descrição; ao fechar, devolva foco ao controle que o abriu, se ainda existir.

## Formulários: validação sem punir quem digita

A validação nativa é uma primeira camada, não todo o domínio. Use tipos, `required`,
`min`, `max` e `maxlength` quando correspondem ao contrato. Em seguida:

1. normalize apenas o que a regra permite;
2. valide todos os campos relevantes;
3. associe cada mensagem ao controle;
4. apresente resumo quando há muitos erros;
5. mova foco para um lugar que ajude a corrigir;
6. preserve valores em falha;
7. impeça submissão acidental duplicada;
8. anuncie sucesso sem interromper desnecessariamente.

Não valide agressivamente um campo incompleto a cada tecla. Uma estratégia comum
é validar no envio e, depois da primeira falha, atualizar aquele campo durante a
correção. Mensagens devem explicar como resolver: “Informe de 1 a 1440 minutos” é
mais útil que “valor inválido”.

## Renderização segura: dado não é marcação

Para conteúdo inserido pela pessoa, prefira `textContent`:

```javascript
export function renderSession(list, session) {
  const item = document.createElement("li");
  const title = document.createElement("strong");
  title.textContent = session.title;
  item.append(title, ` — ${session.minutes} min`);
  list.append(item);
}
```

Não forme HTML por concatenação. Contextos de texto, atributo, URL e CSS exigem
tratamentos diferentes. Se o produto realmente aceita rich text, defina um
formato limitado e use uma biblioteca de sanitização madura. Não crie um
“sanitizador” com substituições simples.

Links gerados precisam de política de esquemas e destinos permitidos. O mesmo
princípio vale nas cinco linguagens: JavaFX `WebView`, componentes C#, bindings
Python e shells desktop baseados em JavaScript não transformam entrada não
confiável em código ou marcação por conveniência.

## Progressive enhancement e limites honestos

Progressive enhancement começa com conteúdo e ações semanticamente claros e
adiciona conveniência. Uma aplicação local complexa pode depender de JavaScript;
isso não torna HTML correto irrelevante. Semântica continua ajudando leitores de
tela, navegação por teclado, automação e futuras migrações.

Não prometa funcionamento offline só porque os arquivos da interface estão em
cache. A jornada, os dados e a resolução de conflitos precisam de contrato. O
[capítulo 09](09-clientes-api-offline.md) diferencia disponibilidade da tela e
consistência da operação.

## Estratégia de testes

- **funções puras:** regra, formatação e reducer com `node:test`;
- **DOM integrado:** semântica produzida, atributos, foco e eventos;
- **navegador real:** teclado, formulários, armazenamento e jornadas críticas;
- **manual assistivo:** zoom, contraste, leitor de tela e conteúdo variável.

O Study Desk deve ter muitos testes do reducer, alguns testes de adaptador e poucos
testes de jornada. Um teste que procura uma classe CSS é frágil se o requisito é
“a sessão registrada aparece com nome acessível”. Teste pelo comportamento e pela
semântica observável.

## Falhas frequentes e diagnóstico

| Sintoma | Causa provável | Como confirmar | Correção |
|---|---|---|---|
| clique dispara duas vezes | listener registrado a cada render | conte registros e comandos | registrar uma vez ou descartar corretamente |
| lista e total divergem | valores derivados armazenados | reproduza sequência mínima | recalcular a partir da fonte de verdade |
| formulário limpa após erro | reset ocorre antes da confirmação | injete falha no repositório | limpar apenas em sucesso |
| teclado não abre controle | elemento não nativo | inspecione semântica e eventos | usar botão/link apropriado |
| conteúdo quebra layout | dimensões fixas | texto longo e zoom | layout intrínseco e wrapping |
| texto vira marcação | uso de `innerHTML` | entrada sintética com caracteres especiais | APIs de texto/atributo seguras |

Registre eventos de aplicação e fases, não cada movimento ou tecla. Um contador de
renderizações, a identidade do evento e a transição anterior/próxima costumam ser
suficientes para localizar loops sem coletar conteúdo do formulário.

## Exercícios em três níveis

### Nível 1 — Documento funcional

Implemente o formulário e a lista do exemplo sem framework. Adicione validação,
CSS fluido e um módulo puro que cria uma sessão válida.

**Critérios de aceite:** funciona com teclado; rótulos são associados; HTML é
válido e semântico; texto digitado é inserido por `textContent`; zoom de 200% não
oculta ações; regra possui testes sem DOM.

### Nível 2 — Estado e falhas

Extraia reducer, repositório em memória e renderer. Modele vazio, salvando, salvo
e falha. Injete latência e falha; impeça envio duplo sem apagar o rascunho.

**Critérios de aceite:** transições têm testes; listener não duplica após dez
renders; falha preserva os campos; foco após erro é previsível; lista e total
sempre derivam da mesma fonte; mensagem de sucesso é anunciada.

### Nível 3 — Evolução do Study Desk

Implemente filtro, edição, exclusão reversível e importação com prévia. Produza uma
matriz estado × ação e uma auditoria manual de teclado. Compare a solução nativa
com um framework sem reescrever: quais fronteiras permaneceriam e que custo seria
adicionado?

**Critérios de aceite:** não há regra no DOM; importação inválida não altera dados;
desfazer restaura exatamente a sessão; resultado de filtro é derivado; jornada
principal funciona em viewport estreito, zoom e texto longo; decisão sobre
framework usa requisitos e evidências.

## Checklist de conclusão

- [ ] HTML expressa a estrutura antes do CSS e do JavaScript.
- [ ] Elementos nativos substituem controles personalizados quando possível.
- [ ] Estado, reducer, efeitos, repositório e renderização têm fronteiras claras.
- [ ] Vazio, espera, sucesso e falha são estados projetados.
- [ ] Formulário preserva entrada e associa mensagens aos campos.
- [ ] Conteúdo da pessoa nunca vira HTML por concatenação.
- [ ] Layout suporta zoom, texto longo e largura estreita.
- [ ] Foco é visível e continua lógico depois de mutações.
- [ ] Testes puros cobrem regras; navegador cobre apenas integração relevante.
- [ ] Diagnóstico registra transições sem capturar conteúdo pessoal.
