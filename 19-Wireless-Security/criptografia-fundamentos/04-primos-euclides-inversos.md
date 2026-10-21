# 04 — Primos, Euclides e inversos

O algoritmo de Euclides calcula o máximo divisor comum repetindo divisões. A
versão estendida encontra `x` e `y` tais que `ax + by = mdc(a,b)`. Se o MDC é
um, `x mod b` é o inverso de `a` módulo `b`.

Primos criam estruturas com inversos previsíveis, mas “número primo” não
significa automaticamente “parâmetro seguro”. Tamanho, geração uniforme,
subgrupos e validação importam. Em produção, gere chaves por APIs de alto nível;
não escreva seu próprio teste de primalidade ou gerador RSA.

## Prática

Use `number_theory.py inverse 7 26`; verifique que `7 × resultado mod 26 = 1` e
observe a falha controlada para `inverse 6 26`.
