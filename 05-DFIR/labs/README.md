# Labs DFIR com dados sintéticos

## Lab 01 — Timeline de autenticação

O arquivo [`fixtures/auth-events.csv`](fixtures/auth-events.csv) contém eventos
inventados de um domínio `LAB.LOCAL`. Nenhum registro veio de sistema real.

### Objetivo

Produzir uma timeline, separar observação de hipótese e apontar os dados que
faltam para confirmar ou refutar a hipótese.

### Procedimento

1. Verifique o SHA-256 do CSV e registre horário UTC da análise.
2. Ordene por `timestamp_utc` e agrupe por usuário, origem e event ID.
3. Explique a sequência 4625 → 4624 → 4672 sem afirmar causalidade absoluta.
4. Proponha duas fontes complementares e uma ação de contenção proporcional.
5. Compare com [`answers/lab-01-auth-timeline.md`](answers/lab-01-auth-timeline.md).

### Critério de conclusão

- [ ] Timeline reproduzível e hash documentado.
- [ ] Fatos, inferências e lacunas aparecem separados.
- [ ] Pelo menos um falso positivo é considerado.
- [ ] A fixture não é alterada; arquivos derivados são removidos no cleanup.

