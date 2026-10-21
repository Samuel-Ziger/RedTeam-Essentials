# 15 — Compromissos e árvores de Merkle

Um compromisso pretende esconder um valor até a abertura e impedir sua troca
posterior. `hash(valor)` sozinho pode vazar valores de espaço pequeno; inclua
aleatoriedade de abertura e um formato com domínio explícito.

Árvores de Merkle resumem folhas por hashes encadeados. Uma prova de inclusão
mostra que uma folha pertence a uma raiz sem enviar toda a árvore. Ordem,
prefixos de folha/nó, duplicação de folha ímpar e função hash fazem parte da
especificação; omiti-los cria incompatibilidades ou ambiguidades.

## Prática

Desenhe uma árvore de quatro arquivos e liste exatamente os bytes autenticados
em cada nível. A raiz prova autoria? Justifique.
