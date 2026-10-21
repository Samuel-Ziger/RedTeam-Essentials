# 09 — Atomics, locks e modelo de memória

## Objetivos

- separar atomicidade, ordenação e exclusão mútua;
- escolher mutex, spinlock, rwsem, seqlock ou completion por contexto;
- raciocinar com happens-before e memory barriers;
- usar lockdep e sanitizers em VM.

## Três problemas diferentes

Uma operação atômica não é interrompida no meio, mas isso não garante que
outras operações sejam vistas na ordem imaginada nem preserva uma invariante
multicampo. Exclusão mútua, visibilidade e lifetime precisam ser tratados.

Exemplo incorreto conceitual:

```text
atomic_increment(refs)
if state == READY: use(object)
```

Se publicação, estado e lifetime não tiverem uma relação de ordenação, o
contador atômico sozinho não torna o objeto seguro.

## Primitivas

| Primitiva | Pode dormir | Uso típico |
|-----------|-------------|------------|
| mutex | sim | exclusão em contexto de processo |
| spinlock | não | seção curta e contexto atômico |
| rwsem | sim | leitores/escritor com operações longas |
| seqlock | leitor repete | estado pequeno, leitura frequente |
| completion | espera evento | handoff de uma ocorrência |
| atomic/refcount | não | contador com semântica definida |

Spinlock não é “mutex mais rápido”. Girar por uma operação que pode dormir
desperdiça CPU e pode deadlockar.

## Modelo de memória

Compilador e CPU podem reordenar operações quando o comportamento permitido não
muda localmente. Padrões acquire/release criam uma ordem de publicação e consumo.
Barreira deve documentar quais duas operações ordena e por quê. Adicionar
`mb()` até um teste passar não é engenharia.

## Ferramentas de verificação

- lockdep encontra classes e ordens de locks problemáticas;
- KCSAN procura data races por amostragem;
- KASAN encontra classes de erro de memória;
- UBSAN detecta comportamento indefinido selecionado;
- herd7/litmus ajuda a estudar o Linux Kernel Memory Model.

Essas opções mudam timing e custo; use kernel de diagnóstico separado.

## Invariante antes da primitiva

Escolha primeiro o que precisa permanecer verdadeiro. Se dois campos representam
um único estado, proteger apenas cada escrita atomicamente permite combinações
impossíveis. Documente quais acessos participam, o contexto, se podem dormir e
qual é a ordem global dos locks. Só então escolha a primitiva.

Mutex fornece exclusão e relações de memória definidas no lock/unlock. Spinlock
é apropriado para região curta quando dormir é proibido; variantes `_irq` ou
`_bh` existem porque concorrência local pode vir de outros contextos. Seqlock
favorece leitores que repetem, mas não serve para dados com ponteiros cujo
lifetime possa acabar durante a repetição. Refcount possui semântica contra
overflow e ressurreição que um atomic genérico não expressa.

## Publicação e lifetime

Um padrão release/acquire publica dados inicializados antes de tornar o ponteiro
visível e garante que o consumidor veja a inicialização após adquiri-lo. Isso
não decide quando o objeto pode ser liberado. Lifetime exige referência, RCU ou
outro protocolo independente. `READ_ONCE` e `WRITE_ONCE` limitam otimizações e
tearing em casos definidos; não transformam sequência em transação.

Deadlocks não se restringem a AB/BA. Espera por completion segurando lock que o
completador precisa, flush de workqueue dentro do próprio worker e reclaim sob
lock também formam ciclos. Modele recursos e arestas de espera.

## Falhas comuns

- escolher spinlock porque “é mais rápido”;
- usar atomic para proteger invariante multicampo;
- adicionar barreira sem nomear operações ordenadas;
- confiar em teste sem falha como prova de ausência de race;
- ignorar teardown concorrente.

## Prática B/C

Implemente em user space um contador compartilhado nas versões: sem proteção,
mutex e atomic. Execute com ThreadSanitizer quando disponível. Depois descreva por
que o resultado correto do contador não prova que uma estrutura composta está
protegida.

## Exercícios

1. Escreva a invariante de uma fila com contador e demonstre uma interleaving que
   atomics independentes não impedem.
2. Construa grafo AB/BA, imponha ordem global e indique onde lockdep aprenderia
   cada aresta.
3. Proponha publicação release/acquire de objeto imutável e trate seu lifetime
   separadamente.
4. Compare mutex, rwsem, seqlock e RCU para uma tabela 99% leitura, justificando
   custo e complexidade.

## Checklist de domínio

- [ ] Escrevo a invariante antes de escolher lock ou atomic.
- [ ] Distingo atomicidade, ordenação, exclusão e lifetime.
- [ ] Sei por que contexto define se posso dormir.
- [ ] Uso lockdep e sanitizers como evidência, não prova matemática.
- [ ] Reconheço ciclos de espera além do caso AB/BA simples.

Fonte: [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html).
