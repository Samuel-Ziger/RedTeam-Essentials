# ADR 001 — Plan/apply e manifesto

## Status

Aceita.

## Contexto

Simulação separada da execução tende a divergir. Manifestos com caminhos
absolutos vazam informação e não são portáteis.

## Decisão

Planner produz Plan imutável consumido por dry-run e apply. A representação
canônica inclui apenas caminhos relativos, IDs, tamanhos, hashes e actions. O digest
é SHA-256 do JSON canônico sem timestamps ou raízes absolutas.

## Consequências

Plan continua contendo caminhos absolutos em memória para o executor, mas as_dict
não os expõe. Estado pode mudar entre plan e apply, então o executor revalida.

