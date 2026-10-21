# 12 — Alta disponibilidade e recuperação

HA reduz interrupção por falha local; DR restaura serviço após evento maior.
RTO define tempo de recuperação; RPO, perda de dados aceitável. Rede participa,
mas aplicação, dados, identidade, DNS e operação precisam do mesmo objetivo.

Ativo/ativo oferece capacidade e falhas complexas; ativo/passivo simplifica
estado, mas pode esconder standby quebrado. Quorum evita split brain. Replicar
erro/configuração ruim não é backup.

## Dependências ocultas

Energia, dutos, meet-me room, operadora, DNS, NTP, PKI, route reflector,
controller, AAA, licença e equipe on-call podem ser single points of failure.

Exercícios tabletop e failover controlado devem medir detecção, decisão,
convergência, capacidade residual e retorno ao normal. Evite “testar DR” sem
critério de parada e rollback.
