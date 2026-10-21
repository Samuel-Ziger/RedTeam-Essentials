# 13 — Correlação e grafos

Correlação liga eventos por pivôs. Um grafo torna explícitas entidades e
relações:

```text
conta --autenticou--> sessão --usou--> dispositivo
sessão --gerou--> request --alterou--> recurso
processo --abriu--> fluxo --alcançou--> serviço
```

## Chaves fortes e fracas

Request/session ID emitido por sistema confiável é forte no seu domínio. Conta,
device ID e processo acrescentam contexto. IP e tempo sozinhos são fracos. Peso
não é verdade matemática: documente por que cada ligação existe.

## Janelas

Use janela coerente com clock skew e latência. O correlator do curso agrupa por
`session_id`, `request_id`, `actor` e `device`, nunca apenas por IP.

## Propagação de erro

Uma entidade mal normalizada contamina várias relações. Preserve evento original
e permita desfazer merge. Não use campos vazios como valor comum.

## Visualização

Grafos grandes parecem convincentes e podem esconder incerteza. Rotule fonte,
tempo, confiança e direção; filtre pela pergunta investigativa.

## Prática

Execute o correlator, escolha um cluster e desenhe o grafo. Marque cada aresta
como observada ou inferida.

