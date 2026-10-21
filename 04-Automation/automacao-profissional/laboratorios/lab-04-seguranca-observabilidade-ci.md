# Laboratório 04 — Segurança, observabilidade, testes e CI

## Objetivo

Transformar a automação dos labs anteriores em um produto revisável e operável.

## Etapa A — threat model

Mapeie entradas, trust boundaries, identidades, dados e sinks. Corrija qualquer
concatenação de shell, caminho ou template. Defina matriz identidade × ação ×
ambiente e retenção de temporários, logs e quarentena.

## Etapa B — segredos

Use apenas canário sintético. Provoque erro de HTTP, parser, logger e empacotamento.
Busque o canário em stdout, stderr, JSONL, traces, screenshots, caches e artifacts.

## Etapa C — telemetria

Implemente eventos versionados, resumo reconciliado e métricas sem IDs como labels.
Simule sink indisponível; fallback deve ser terminal, limitado e sanitizado.

Crie dois alertas: janela atrasada e dead-letter antiga. Cada um aponta para runbook.

## Etapa D — suíte de risco

Monte matriz risco → controle → teste. Injete falhas antes/depois de cada commit,
race de destino, cancelamento e config futura. Execute CLI como subprocesso.

## Etapa E — CI

Crie DAG lint → unit/contract/integration → package → verify. Use permissões
mínimas, timeout, dependências fixadas, artifact identificado e relatórios mesmo
na falha. Não use segredo de publicação em contribuição.

## Aceite

- canário ausente em toda evidência;
- contagens do resumo fecham;
- falha do logger segue contrato sem recursão;
- matriz cobre sobrescrita, duplicata, vazamento e perda;
- artifact tem digest e inventário;
- CI separa trust zones e promove o mesmo artifact.

