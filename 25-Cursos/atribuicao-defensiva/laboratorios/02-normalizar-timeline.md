# Lab 02 — Normalizar tempo e construir timeline

1. preserve `timestamp` original;
2. converta todos os eventos para UTC;
3. registre precisão e `clock_offset_ms` quando existir;
4. use ingestão apenas como dado auxiliar;
5. ordene sem esconder empates;
6. marque relações causais somente quando há ID ou sequência sustentada.

## Teste negativo

Altere uma cópia para adicionar 90 segundos de skew ao endpoint. Compare uma
janela de 30 e de 120 segundos. Explique falso negativo e falso positivo.

## Evidência

Tabela com original, normalizado, fonte, offset e observação. Não sobrescreva a
fixture.

