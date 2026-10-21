# Segurança em nuvem

Compare AWS, Azure e GCP por conceitos — identidade, política, recurso,
telemetria e limite de confiança — em vez de memorizar nomes de produtos.

## Sequência

1. Leia o [mapa do percurso](LEGADO-CLOUD-RED-TEAM.md).
2. Compare caminhos em [AWS](aws-attack-paths.md),
   [Azure](azure-attack-paths.md) e
   [GCP](gcp-attack-paths.md).
3. Avalie as [ferramentas de reconhecimento](cloud-recon-tools.md)
   quanto a permissões, custo, paginação, limites de taxa e registro.
4. Execute o [lab multicloud](labs/README.md) com o
   [analisador local](labs/analyze_events.py) e as
   fixtures versionadas.
5. Compare sua análise à
   [resposta orientativa](labs/answers/iam-changes.md).

## Entrega

Crie uma matriz que relacione permissão, caminho de risco, evento observável,
controle preventivo, detecção e rollback. Contas reais exigem orçamento,
alertas de custo e autorização explícita.
