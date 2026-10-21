# Laboratórios — Engenharia de APIs

Os cinco laboratórios são cumulativos. Cada entrega amplia a mesma API e deixa
evidência verificável. Use dados fictícios, loopback e dependências fake. Não
aponte testes de carga, abuso, webhook ou fuzz para serviços externos.

| Lab | Resultado | Gate |
|---|---|---|
| 01 | contrato HTTP executável | semântica e erros previsíveis |
| 02 | contrato evolutivo e seguro | identidade, autorização e OpenAPI |
| 03 | serviço operável | dados, resiliência, sinais e testes |
| 04 | integrações e clientes | duplicidade, deadline e compatibilidade |
| 05 | capstone | operação e defesa completas |

## Padrão de evidência

Cada pasta de entrega contém:

~~~text
README.md
contract/
src/
tests/
evidence/
  commands.txt
  results/
  decision-log.md
RUNBOOK.md
~~~

Comandos não carregam token real. Saídas são pequenas, redigidas e
reproduzíveis. Screenshot não substitui teste ou artifact textual.

## Regras

1. Leia os pré-requisitos do lab.
2. Declare hipóteses e critérios antes de implementar.
3. Execute casos feliz, inválido e de falha.
4. Preserve request/event IDs e versões.
5. Peça a outra pessoa para reproduzir o gate.
6. Consulte respostas orientativas somente depois.

