# 15 — Rate limiting e quotas

Rate limit protege capacidade e jornadas. A regra precisa responder cinco
perguntas: qual operação, qual chave, qual algoritmo, qual janela/burst e qual
resposta.

## Algoritmos

- fixed window: simples, mas permite burst na fronteira;
- sliding window: mais fiel, com maior custo;
- leaky bucket: suaviza saída;
- token bucket: repõe tokens e permite burst controlado;
- concurrency limit: limita trabalho simultâneo, útil em operação cara.

A demonstração `token_bucket.py` usa tempo fornecido pela fixture. Assim, o
resultado é determinístico e não gera tráfego.

## Escolha de chave

IP sozinho pune redes compartilhadas e não cobre fontes distribuídas. Considere
tenant + conta + rota, token, sessão, dispositivo com privacidade e IP como
sinal adicional. Antes do login, combine chaves e aplique limite global de
proteção.

## Distribuição

Múltiplos edges precisam de estado coerente ou budget particionado. Aceite e
documente tolerância a overshoot, falha do storage e clock. Decida fail-open ou
fail-closed conforme risco da rota; indisponibilidade do limitador não deve
derrubar toda a aplicação por acidente.

## Resposta

Use status sem revelar existência de conta, inclua orientação de retry quando
apropriada e preserve request ID. Retry automático precisa de backoff e jitter;
caso contrário, cliente e servidor amplificam a falha.

## Exercício Purple

Red executa a fixture com burst, fluxo sustentado e dois tenants. Blue explica
cada decisão e alerta somente quando o impacto justificar. Purple testa
fronteira, refill, isolamento entre chaves, reinício e falha do backend.
