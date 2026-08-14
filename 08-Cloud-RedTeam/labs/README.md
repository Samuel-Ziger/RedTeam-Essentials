# Labs cloud offline com eventos sintéticos

> Estes exercícios não criam recursos, não exigem credenciais e não geram
> custos. Todos os nomes, endereços e identificadores das fixtures são fictícios.

## Objetivo

Analisar uma mudança IAM de alto risco em cada provedor, explicar o contexto
necessário e validar uma detecção simples sem consultar AWS, Azure ou GCP.

| Lab | Fixture | Comportamento |
|-----|---------|--------------|
| AWS | [`fixtures/aws-cloudtrail.jsonl`](fixtures/aws-cloudtrail.jsonl) | `AttachUserPolicy` com `AdministratorAccess`. |
| Azure | [`fixtures/azure-activity.jsonl`](fixtures/azure-activity.jsonl) | Role assignment de `Owner`. |
| GCP | [`fixtures/gcp-audit.jsonl`](fixtures/gcp-audit.jsonl) | IAM policy inclui `roles/owner`. |

## Procedimento reproduzível

```bash
python3 08-Cloud-RedTeam/labs/analyze_events.py \
  08-Cloud-RedTeam/labs/fixtures/aws-cloudtrail.jsonl

python3 08-Cloud-RedTeam/labs/analyze_events.py \
  08-Cloud-RedTeam/labs/fixtures/azure-activity.jsonl

python3 08-Cloud-RedTeam/labs/analyze_events.py \
  08-Cloud-RedTeam/labs/fixtures/gcp-audit.jsonl
```

Para cada alerta, responda:

1. Qual principal iniciou a mudança e qual identidade recebeu privilégio?
2. Qual campo prova sucesso ou falha da operação?
3. Quais change tickets, origem, MFA ou dados de workload reduziriam incerteza?
4. Como revogar a concessão sem destruir evidência?
5. Que controle preventivo reduziria o risco?

Compare depois com [`answers/iam-changes.md`](answers/iam-changes.md).

## Critérios de conclusão

- [ ] O analisador encontra um evento perigoso e ignora um evento benigno por provedor.
- [ ] Observação, hipótese e contexto ausente aparecem separados.
- [ ] A resposta proposta preserva logs e revoga somente a concessão indevida.
- [ ] Nenhuma credencial, conta ou API cloud foi utilizada.

## Cleanup

Remova apenas resultados derivados. Preserve fixtures versionadas; não há
recurso cloud para destruir nem custo a encerrar.

