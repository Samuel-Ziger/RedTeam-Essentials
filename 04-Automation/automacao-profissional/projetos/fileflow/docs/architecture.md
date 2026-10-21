# Arquitetura do FileFlow

~~~text
cli -> planner -> Plan imutável -> executor -> filesystem
 |        |                               -> audit JSONL
 |        -> descoberta/hash/decisão
 -> apresentação text/JSON e código de processo
~~~

## Fronteiras

Planner observa filesystem e produz copy, skip ou conflict. Ele não altera destino.
Plan guarda caminhos absolutos somente em memória para executar; as representações
serializadas usam relativePath, operationId, tamanho e hash.

Executor recusa conflito, valida run ID, revalida **todas** as fontes e só então
começa efeitos. Cada copy usa temporário, confirma hash e publica com hard-link
exclusivo. O temporário é removido no finally.

## Invariantes

- source e target não são iguais nem aninhados;
- extensões pertencem ao alfabeto seguro;
- quantidade e bytes totais são limitados;
- symlink não é seguido;
- plano é ordenado e tem digest canônico;
- conflito conhecido impede toda cópia;
- fonte alterada invalida apply;
- destino existente nunca é sobrescrito;
- repetir converte copies confirmadas em skips;
- manifesto/audit não expõem caminhos absolutos nem conteúdo.

## Limites de garantia

O projeto didático usa APIs portáveis de alto nível. Existe uma janela entre
lstat/hash e abertura em que um adversário local com acesso à mesma árvore poderia
trocar a fonte. Para ameaça local hostil, use primitivas relativas a descritor,
no-follow e sandbox da plataforma. O FileFlow assume workspace controlado.

A publicação por hard link requer mesmo filesystem entre temporário e destino;
o temporário é criado no diretório alvo para satisfazer isso. Audit JSONL é
append-only pela aplicação, mas não é armazenamento inviolável.

## Decisões

- [ADR 001 — Plan/apply e manifesto](adr/001-plan-apply-manifest.md)
- [ADR 002 — Publicação exclusiva](adr/002-exclusive-publication.md)

