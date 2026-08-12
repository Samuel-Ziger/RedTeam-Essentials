# Roadmap de conteúdo ofensivo seguro

## Entregue agora

- recon correlacionado a partir de fixtures;
- gate de escopo antes de atividade ativa;
- matriz de autorização BOLA/BFLA offline;
- operação integrada AD/cloud/identidade híbrida;
- revisão ofensiva de containers e CI/CD;
- pós-exploração com canário, kill list e cleanup;
- microemulação Purple Team com testes de regressão.
- análise offline de caminhos de pivot e segmentação;
- metodologia source-to-sink para code review ofensivo;
- planejamento de adversary emulation orientado por inteligência.
- movimentação lateral como grafo de principal, direito, protocolo e host.

## Próximos labs locais

### Web e APIs

1. OAuth/OIDC: redirect URI, state/nonce, audience e PKCE em servidor mock.
2. GraphQL: BOLA por node e limite de depth/complexity.
3. gRPC: autorização desigual por método e limites de streaming.
4. CSRF, SSTI, upload, deserialização e WebSockets em apps mínimas.
5. Request smuggling/cache somente em topologia local dedicada.

Cada lab deverá fornecer versão vulnerável, versão corrigida, request esperado,
telemetria, teste negativo e teardown.

### AD e identidade híbrida

- fixtures de grafo para ADCS, RBCD, consent grants e workload identity;
- análise de precondições e menor caminho, sem executar abuso em tenant real;
- exercício GOAD/sandbox separado, com snapshots e revogação verificável.

### Cloud e containers

- attack paths IAM como grafos AWS/Azure/GCP;
- manifests Kubernetes vulnerável/corrigido;
- Docker socket, capabilities e secrets em layers somente em VM local;
- relações workload identity entre pod e cloud.

### CI/CD supply chain

- workflow vulnerável executado apenas em runner descartável local;
- OIDC trust excessivo representado por policy sintética;
- cache/artifact substitution com arquivos canário;
- build corrigido com permissions mínimas, approval e provenance.

### Initial access e post-exploitation

- awareness com Mailpit/GoPhish local, contas sintéticas e sem captura de senha;
- mock de password spraying com rate limit e lockout controlados;
- pivot em rede Docker/VM isolada, canário e allowlist;
- persistência apenas simulada e cleanup automaticamente verificável.

### C2 e emulação

Continuará fora de escopo publicar implants, loaders, bypass de EDR ou malware.
Serão aceitos PCAPs sintéticos, periodicidade/jitter, arquitetura conceitual,
Atomic Red Team/Caldera em lab e logging completo do operador.

## Definition of Done

Nenhum conteúdo ofensivo é considerado pronto sem:

1. autorização/escopo e critério de parada;
2. fixture ou alvo local versionado;
3. precondição e resultado esperado;
4. evidência mínima sanitizada;
5. telemetria e falso positivo;
6. mitigação e versão corrigida quando aplicável;
7. teste de regressão offline;
8. cleanup e kill list;
9. revisão ética e referência primária.
