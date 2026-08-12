# Labs de detecção para containers

## Lab 01 — Kubernetes audit log sintético

Analise [`fixtures/k8s-audit.jsonl`](fixtures/k8s-audit.jsonl). Os namespaces,
tokens e IPs são fictícios e o exercício não exige cluster.

### Perguntas

1. Qual evento representa leitura normal e qual representa criação de pod?
2. Que campo indica decisão de autorização?
3. Por que `privileged: true` aumenta o risco?
4. Escreva uma regra que alerte apenas quando um pod privilegiado for criado.
5. Qual contexto reduziria falsos positivos?

Compare depois com [`answers/lab-01-k8s-audit.md`](answers/lab-01-k8s-audit.md).

### Cleanup

Não há cluster ou recurso para destruir. Remova consultas/arquivos derivados e
preserve a fixture original para que o hash e o exercício continuem repetíveis.

