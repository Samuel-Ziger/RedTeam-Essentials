# 06 — DDoS e disponibilidade

DDoS tenta esgotar enlace, estado, CPU, conexões ou uma operação cara da
aplicação. Um WAF pode ajudar em abuso HTTP, mas não recupera um link saturado
antes de o tráfego chegar. Proteção volumétrica precisa estar a montante.

## Camadas de pressão

| Camada | Exemplo de recurso | Controles |
|---|---|---|
| L3/L4 | banda, PPS, tabela de estado | scrubbing/anycast, ACL, SYN protection |
| TLS/HTTP | handshakes, conexões, workers | CDN, cache, limites, timeouts |
| Aplicação | busca, export, login, checkout | quotas, filas, cache, custo por operação |
| Dependência | banco, e-mail, API externa | circuit breaker, budget, degradação |

## Engenharia de resiliência

Defina SLO, capacidade normal, sinais de saturação, prioridades e modos
degradados. Uma página estática pode permanecer disponível quando busca ou
recomendação estiverem limitadas. Coloque limites de corpo, cabeçalhos,
conexão, fila e tempo em todos os saltos, de forma coerente.

Bloqueio por IP tem efeito limitado com NAT compartilhado, IPv6 e fontes
distribuídas. Rate limit deve escolher uma chave adequada e proteger o recurso
caro, não apenas a URL externa.

## Teste seguro

Nunca gere volume contra Internet ou produção. Use modelo de capacidade,
replay de fixture, load test aprovado em homologação e teto pequeno. Pare por
erro, latência, fila ou consumo — não espere indisponibilidade.

## Exercício Purple

Red identifica uma operação assimétrica na arquitetura e descreve um estímulo
limitado. Blue define quatro sinais e um modo degradado. Purple registra quem
pode acionar proteção emergencial, quando desfazer e como confirmar recuperação.
