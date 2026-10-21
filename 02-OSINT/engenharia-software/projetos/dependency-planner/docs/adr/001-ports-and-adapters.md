# ADR-001: núcleo independente de mecanismos externos

- Status: aceito
- Data: 2026-09-30

## Contexto

O planejador precisa demonstrar algoritmos e design sem depender de framework ou
banco. A fonte inicial é JSON, mas exercícios futuros devem poder usar CSV, SQL
ou HTTP. As regras precisam de testes rápidos e determinísticos.

## Decisão

Manter objetos e algoritmos no núcleo. O caso de uso depende de uma porta
`WorkItemRepository`, declarada em `ports.py`; o adaptador JSON implementa essa
porta em `repository.py`. A CLI compõe as partes e traduz erros para o processo.

## Consequências

- algoritmos são executáveis sem I/O;
- trocar a entrada não altera regras;
- existem mais módulos e contratos que em um script único;
- transações e concorrência precisarão de novas decisões se houver escrita.

## Alternativas

- Script único: menor início, rejeitado porque mistura validação, regra e saída.
- Framework web: rejeitado porque não existe requisito HTTP e esconderia o fluxo.
