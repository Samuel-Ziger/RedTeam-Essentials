# 02 — Tabela de rotas e longest-prefix match

A RIB pode conter várias rotas candidatas; preferência administrativa escolhe
entre fontes e métrica escolhe dentro do protocolo, conforme plataforma. A FIB
recebe rotas instaladas e estruturas resolvidas para encaminhamento.

O lookup seleciona primeiro o prefixo mais longo. Para `10.20.30.40`, uma rota
`10.20.30.0/24` vence `10.20.0.0/16` e `0.0.0.0/0`, independentemente de a
default ter métrica numericamente menor.

Next hop pode exigir resolução recursiva: a rota aponta a um IP e outra rota
encontra sua interface. Blackhole/null routes descartam deliberadamente e podem
suportar sumarização, desde que rotas mais específicas legítimas existam.

## Prática

```bash
python3 exemplos/route_policy.py lookup fixtures/routes.json 10.20.30.40
```

Preveja resultado antes de executar e explique prefixo, preferência e métrica.
