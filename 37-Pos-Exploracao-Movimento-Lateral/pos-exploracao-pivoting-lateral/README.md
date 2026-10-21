# Pós-exploração, pivoting e movimentação lateral

O percurso usa grafos e fixtures para estudar alcance sem transformar o lab em
uma sequência de comandos. Cada aresta precisa de precondição, evidência e
controle defensivo.

## Sequência

1. Leia o [modelo de pós-exploração](../acervo/pos-exploracao/LEGADO-POST-EXPLOITATION.md),
   [persistência](../acervo/pos-exploracao/persistence-overview.md) e
   [coleta/exfiltração](../acervo/pos-exploracao/collection-exfil.md).
2. Modele rotas com o [percurso de pivoting](../acervo/pivoting/LEGADO-NETWORK-PIVOTING.md),
   o [analisador](../acervo/pivoting/path_analyzer.py) e sua
   [topologia](../acervo/pivoting/fixtures/topology.json).
3. Compare com o [percurso lateral](../acervo/movimento-lateral/LEGADO-LATERAL-MOVEMENT.md),
   o [analisador de grafo](../acervo/movimento-lateral/lateral_path_analyzer.py) e
   a [fixture lateral](../acervo/movimento-lateral/fixtures/lateral-graph.json).
4. Relacione a [teoria Windows](../acervo/movimento-lateral/windows_lateral_movement_teoria.md)
   e [Linux](../acervo/movimento-lateral/linux-lateral-movement.md) aos controles.

## Entrega

Apresente caminhos antes/depois da remediação, pontos de detecção, impacto
mínimo demonstrado e plano de contenção. Não persista nem exfiltre dados reais.
