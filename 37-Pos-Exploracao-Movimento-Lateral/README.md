# 37 — Pós-exploração, pivoting e movimentação lateral

O módulo modela caminhos entre hosts e identidades depois de um acesso
simulado. A meta é medir alcance, contenção e observabilidade, com impacto
mínimo e sem persistência fora do laboratório.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Red, Blue e Purple Team, arquitetura e segmentação. |
| Pré-requisitos | Módulos `27`, `31`, `32`, `33`, `35` e `36`. |
| Tempo estimado | 50–80 horas. |
| Ambiente | Topologias e grafos sintéticos; rede local explicitamente autorizada. |
| Foco | Caminhos, segmentação, credenciais, coleta mínima e contenção. |
| Evidência final | Grafo antes/depois, telemetria e recomendações priorizadas. |
| Critério de conclusão | Caminhos reduzidos e detecções comprovadas após o reteste. |

## Conteúdo curricular

- [Pós-exploração, pivoting e lateralidade](pos-exploracao-pivoting-lateral/README.md)
- [Pós-exploração](acervo/pos-exploracao/LEGADO-POST-EXPLOITATION.md)
- [Persistência: visão defensiva](acervo/pos-exploracao/persistence-overview.md)
- [Coleta e exfiltração: riscos e controles](acervo/pos-exploracao/collection-exfil.md)
- [Análise de pivoting](acervo/pivoting/LEGADO-NETWORK-PIVOTING.md)
- [Analisador de topologia](acervo/pivoting/path_analyzer.py)
- [Movimentação lateral](acervo/movimento-lateral/LEGADO-LATERAL-MOVEMENT.md)
- [Analisador de grafo lateral](acervo/movimento-lateral/lateral_path_analyzer.py)
- [Lateralidade em Windows](acervo/movimento-lateral/windows_lateral_movement_teoria.md)

Próximo: [Módulo 38 — DFIR e resposta a incidentes](../38-DFIR-Resposta-Incidentes/README.md).
