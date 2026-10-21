# 08 — Acessibilidade e responsividade verificáveis

Acessibilidade não é uma camada aplicada depois que a interface “está pronta”.
Ela altera a estrutura do documento, o texto, a interação, os estados, a definição
de pronto e a arquitetura dos componentes. Responsividade também não significa
apenas caber em uma tela pequena: significa continuar compreensível diante de
largura, zoom, fonte, idioma, orientação e forma de entrada diferentes.

O [Study Desk](projetos/study-desk/README.md) será o laboratório contínuo. Na
versão executável, a jornada essencial é registrar uma sessão, encontrá-la,
importar/exportar dados e excluir com confirmação. A edição aparece adiante como
evolução proposta, não como recurso já entregue. Se as jornadas atuais só
funcionam com mouse, visão perfeita ou fonte padrão, o produto está incompleto.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. aplicar os princípios perceptível, operável, compreensível e robusto;
2. preferir semântica nativa e usar ARIA apenas para complementar;
3. projetar teclado, foco, mensagens e atualizações assíncronas;
4. criar layout orientado pelo conteúdo que suporte zoom e reflow;
5. comunicar estado sem depender exclusivamente de cor, posição ou movimento;
6. combinar testes automatizados, inspeção e jornadas manuais;
7. escrever critérios de aceite observáveis para acessibilidade;
8. diagnosticar falhas de nome, função, estado, foco e ordem de leitura.

## Pré-requisitos e modelo mental

Você deve conhecer HTML semântico, CSS fluido, formulários e estado de UI dos
[capítulos 05](05-estado-eventos.md) e [07](07-interfaces-web.md). Os mesmos
princípios se aplicam a GUI desktop, embora a API concreta dependa do toolkit.

```text
conteúdo e tarefa
  -> estrutura semântica
  -> nome, função, valor e estado
  -> operação por entradas diferentes
  -> feedback perceptível
  -> reflow e preferências
  -> teste automatizado + inspeção + uso real
```

Não trate acessibilidade como uma lista de atributos. Comece pela tarefa: “uma
pessoa consegue registrar uma sessão, entender o resultado e corrigir um erro?”.
Depois investigue como diferentes barreiras mudam essa tarefa. Deficiências podem
ser permanentes, temporárias ou situacionais: uma mão imobilizada, ambiente claro,
cansaço cognitivo e conexão instável também expõem interfaces frágeis.

## Os quatro princípios como perguntas de projeto

| Princípio | Pergunta prática | Exemplo no Study Desk |
|---|---|---|
| perceptível | a informação existe em forma que a pessoa percebe? | erro tem texto, associação e não apenas borda vermelha |
| operável | toda ação funciona com formas de entrada suportadas? | registrar, filtrar, importar e exportar funcionam por teclado |
| compreensível | texto e comportamento são previsíveis? | “Excluir sessão” identifica o efeito e pede confirmação |
| robusto | agentes diferentes entendem nome, função e estado? | botão e campo usam elementos nativos com estados válidos |

Esses princípios orientam decisões; critérios técnicos tornam o resultado
verificável. Conformidade mínima não garante uma boa experiência, e uma boa
intenção não substitui evidência. Critérios devem entrar na história de usuário,
no teste e na revisão visual desde o início.

## Semântica: nome, função, valor e estado

Tecnologia assistiva constrói uma representação a partir do documento. Um
controle precisa comunicar:

- **nome:** “Duração em minutos”;
- **função:** campo numérico, botão, link ou caixa de seleção;
- **valor:** `45`, quando aplicável;
- **estado:** inválido, expandido, selecionado, pressionado ou desabilitado.

Elementos nativos já implementam grande parte desse contrato. Compare:

```html
<!-- Correto para uma ação -->
<button type="button" aria-expanded="false" aria-controls="filters">
  Mostrar filtros
</button>

<!-- Imitação incompleta: evite -->
<div class="button" onclick="toggleFilters()">Mostrar filtros</div>
```

O segundo exemplo não recebe foco por padrão, não comunica função e não responde
automaticamente a Enter ou Espaço. Adicionar `role`, `tabindex` e handlers pode
recriar parte do botão, mas aumenta a superfície de falha sem benefício.

O nome acessível deve explicar a ação fora do contexto visual. Vários botões
chamados apenas “Editar” podem precisar de “Editar sessão Matemática”, desde que o
nome não fique verboso demais. Um ícone decorativo deve ficar fora da árvore
acessível; um ícone que é a única informação precisa de alternativa equivalente.

ARIA não muda comportamento. `aria-expanded="true"` não abre nada; o código deve
mostrar o painel e manter o atributo sincronizado. Um atributo desatualizado pode
ser pior que a ausência dele porque comunica uma realidade falsa.

## Teclado e foco como fluxo de estado

Uma interface operável por teclado exige mais que “tudo recebe Tab”. Verifique:

1. ordem de foco segue a ordem lógica de leitura;
2. foco é claramente visível em todos os temas;
3. controles usam teclas esperadas para sua função;
4. nenhum componente prende o foco indevidamente;
5. conteúdo revelado recebe foco apenas quando isso ajuda;
6. remoção de elemento escolhe destino lógico;
7. atalhos não conflitam com digitação ou tecnologia assistiva.

Não use `tabindex` positivo para reorganizar uma árvore visualmente confusa.
Corrija a ordem do DOM e use CSS para layout. `tabindex="0"` inclui algo na ordem
natural; `-1` permite foco programático sem criar uma parada permanente.

Um diálogo modal tem ciclo de vida próprio:

```text
acionador focado
  -> abre diálogo
  -> foco vai ao título, primeiro campo ou ação segura
  -> Tab permanece nas ações do diálogo
  -> Escape fecha quando não destrutivo
  -> foco retorna ao acionador existente
```

Se uma sessão é excluída da lista, devolver foco ao botão excluído é impossível.
Defina previamente: próximo item, item anterior ou título da lista. Essa decisão
pertence à transição de estado, não a um `setTimeout` espalhado.

## Formulários, erros e feedback assíncrono

Rótulos visíveis são melhores que placeholder como único nome. Placeholder some
durante a digitação, costuma ter baixo contraste e não explica formato ou erro.
Associe ajuda e erro ao campo:

```html
<label for="minutes">Duração em minutos</label>
<input id="minutes" name="minutes" type="number"
       aria-describedby="minutes-help minutes-error"
       aria-invalid="true">
<p id="minutes-help">Informe um valor de 1 a 1440.</p>
<p id="minutes-error">A duração não pode ser zero.</p>
```

No envio com vários erros, apresente um resumo focável com links para os campos e
mantenha mensagens inline. Não apague o formulário. Ao corrigir, sincronize
`aria-invalid` e mensagem; não deixe a árvore acessível presa ao erro antigo.

Use uma região `role="status"` ou `aria-live="polite"` para resultados que não
exigem interrupção, como “Sessão registrada”. `alert` é adequado a uma mensagem
urgente; usar alerta para toda atualização produz ruído. Um spinner precisa de
texto como “Salvando sessão”; animação sozinha não comunica progresso.

## Cor, contraste, movimento e carga cognitiva

Cor pode reforçar uma informação, mas não ser o único canal. Combine borda,
ícone com alternativa adequada e texto. Verifique contraste de texto, controles,
foco e estados; não presuma que um modo escuro automaticamente melhora tudo.

Respeite preferência por movimento reduzido:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Esse bloco é uma rede de segurança, não autorização para animações excessivas.
Movimento precisa ter propósito, permitir pausa quando necessário e não ser a
única forma de mostrar relação.

Acessibilidade cognitiva também pede linguagem direta, consistência e redução de
surpresas. Divida formulários longos, mostre progresso real, explique abreviações
e mantenha ações no mesmo lugar. Confirmação destrutiva deve dizer o que será
apagado e se há recuperação; frases vagas como “Tem certeza?” transferem todo o
trabalho de interpretação à pessoa.

## Responsividade orientada pelo conteúdo

Uma interface responsiva aceita variação em vez de prever cada aparelho:

```css
.session-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
  gap: clamp(0.75rem, 2vw, 1.5rem);
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.session-title {
  overflow-wrap: anywhere;
}
```

Use unidades relativas e limites de leitura. Deixe controles quebrarem linha em
vez de sumirem. Uma tabela larga pode virar cartões, permitir rolagem horizontal
identificada ou esconder colunas não essenciais por uma escolha explícita — nunca
corte dados silenciosamente.

Teste, no mínimo:

- largura estreita e orientação diferente;
- zoom de 200% e reflow equivalente a 400%;
- fonte padrão aumentada;
- título muito longo e sem espaços;
- tradução com aproximadamente 40% de expansão;
- teclado virtual ocupando parte da tela;
- preferência por alto contraste e movimento reduzido.

Responsividade não deve alterar a ordem semântica de modo enganoso. CSS pode mover
visualmente um botão, mas a leitura e o Tab continuam seguindo o DOM. Se a ordem
significativa muda por tamanho, revise a estrutura ou renderize uma composição
adequada mantendo uma única fonte de estado.

## Componentes complexos e decisão de construir

Combobox, grade editável, árvore e drag-and-drop têm contratos extensos de
teclado, foco e estado. Antes de criar um componente próprio, pergunte:

- um elemento nativo resolve a tarefa?
- uma composição simples resolve melhor?
- existe biblioteca madura, documentada e testada?
- a equipe consegue testar leitores de tela e combinações de entrada?

Arrastar pode ser uma conveniência, nunca o único modo de reordenar. No Study
Desk, botões “Mover para cima/baixo” ou um campo de posição oferecem alternativa
determinística. Uma visualização por cartões não deve substituir a lista sem
preservar nomes e relações.

Em GUI desktop, aplique a mesma análise por meio das propriedades de
acessibilidade do toolkit. Python, Java, C, C# e JavaScript usam APIs diferentes,
mas todos precisam expor nome, função, valor e estado e preservar foco. Testar
somente a aparência não comprova nenhum deles.

## Estratégia de teste em camadas

Automação encontra parte das falhas, principalmente ausência de nome, atributos
inválidos e algum contraste. Ela não decide se o rótulo é claro, a ordem faz
sentido ou a jornada é cognitivamente viável.

Use uma sequência repetível:

1. validação de HTML e lint acessível;
2. testes por função/nome acessível, não por classe visual;
3. navegação completa só com teclado;
4. inspeção da árvore de acessibilidade;
5. contraste, zoom, reflow, tema e movimento reduzido;
6. leitor de tela nas plataformas declaradas;
7. teste com pessoas, incluindo pessoas com deficiência, quando possível;
8. regressão registrada com passos, resultado e evidência.

Uma auditoria precisa de escopo. Para o Study Desk atual, use quatro jornadas:
criar, filtrar, importar e exportar. Registre navegador/toolkit, versão, zoom, tecnologia
assistiva, passos, esperado, observado, severidade e correção. Não marque “passou”
apenas porque uma ferramenta retornou zero alertas.

## Falhas frequentes e diagnóstico

| Sintoma | Hipótese | Verificação | Correção |
|---|---|---|---|
| leitor anuncia “botão” sem nome | ícone sem nome acessível | árvore de acessibilidade | texto visível ou nome equivalente |
| foco desaparece após render | nó focado foi substituído | observe `activeElement` | preservar nó ou mover foco deliberadamente |
| erro não é percebido | depende de cor/posição | teclado e leitor de tela | associação, texto e anúncio apropriado |
| ordem de Tab parece aleatória | DOM e layout divergem | percorra sem mouse | reorganizar documento, remover tabindex positivo |
| zoom cria duas rolagens | largura/altura rígida | 400% e viewport estreito | layout fluido e wrapping |
| estado anunciado está errado | ARIA não acompanha reducer | comparar DOM e estado | renderizar atributo da mesma fonte |

Ao diagnosticar, reduza o componente ao HTML mínimo e teste nome, função e estado
antes do estilo. Depois adicione layout e comportamento um de cada vez. Esse
método separa falha semântica de falha de foco ou renderização.

## Exercícios em três níveis

### Nível 1 — Auditoria guiada

Audite o formulário do Study Desk: rótulos, ajuda, mensagens, teclado, foco, cor,
zoom e texto longo. Corrija pelo menos cinco barreiras e explique o princípio
afetado.

**Critérios de aceite:** toda ação recebe nome e função corretos; jornada funciona
sem mouse; erro não depende de cor; foco é visível; zoom não oculta conteúdo;
relatório inclui passos antes/depois e evidência.

### Nível 2 — Componente com estados

Implemente um diálogo de edição e uma notificação de salvamento. Modele abertura,
validação, salvando, sucesso, falha e fechamento. Adicione preferência por
movimento reduzido e teste texto 40% maior.

**Critérios de aceite:** foco entra, permanece e retorna corretamente; Escape não
descarta alteração sem política explícita; erros são associados; sucesso é
anunciado uma única vez; reducer e integração possuem testes; layout suporta
zoom e tradução longa.

### Nível 3 — Plano de conformidade por risco

Crie uma matriz das jornadas essenciais do Study Desk com critérios, método de
teste, plataformas e severidade. Execute a matriz, corrija os bloqueadores e
publique limitações conhecidas com plano de correção.

**Critérios de aceite:** matriz cobre percepção, operação, compreensão e robustez;
combina automação e teste manual; nenhum bloqueador impede criar, localizar,
importar ou exportar; a evolução de edição é rotulada separadamente; componente complexo tem alternativa simples; evidências são
reproduzíveis e não contêm dados pessoais.

## Checklist de conclusão

- [ ] Acessibilidade faz parte dos requisitos e da definição de pronto.
- [ ] Elementos nativos são a primeira escolha.
- [ ] Nome, função, valor e estado permanecem sincronizados.
- [ ] Jornada principal funciona por teclado e foco nunca desaparece.
- [ ] Erros têm texto, associação e instrução de correção.
- [ ] Atualizações assíncronas são anunciadas sem excesso.
- [ ] Cor e movimento não são os únicos canais de informação.
- [ ] Layout suporta zoom, fonte, idioma e largura variáveis.
- [ ] Componentes complexos têm justificativa e alternativa operável.
- [ ] Automação, inspeção, leitor de tela e teste humano se complementam.
