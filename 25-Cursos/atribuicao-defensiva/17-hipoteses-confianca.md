# 17 — Hipóteses, confiança e falsos positivos

Uma investigação madura tenta refutar a própria conclusão. Mantenha uma tabela:

| Hipótese | Evidência a favor | Contra | Ausente | Próximo teste |
|---|---|---|---|---|
| token roubado | sessão nova | MFA válido | device posture | revogar e revisar emissão |
| uso legítimo via VPN | ASN VPN | ação rara | ticket | confirmar com owner |
| falso positivo | regra ampla | baseline similar | contexto | executar negativo |

## Bayes sem falsa precisão

Evidência muda plausibilidade a partir de uma taxa-base. Não atribua porcentagens
inventadas. Classes baixa/média/alta com critérios explícitos são melhores que
“93%” sem calibração.

## Vieses

Confirmação, ancoragem no primeiro IoC, autoridade, disponibilidade e estereótipo
geográfico afetam análise. Revisão por pares e hipótese concorrente reduzem dano.

## Falso positivo e negativo

Meça regra em dados históricos, mantenha casos negativos e observe cobertura.
Tunar somente para reduzir volume pode esconder incidentes; alertar tudo satura
analistas.

## Linguagem final

“Com alta confiança, a sessão S do dispositivo gerenciado D realizou A; não há
evidência suficiente para afirmar quem controlava fisicamente D.”

## Prática

Classifique as conclusões da fixture e escreva uma condição que reduziria cada
nível de confiança.

