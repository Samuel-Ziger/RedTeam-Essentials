# 02 — Tabela MAC e encaminhamento

Ao receber um quadro, o switch aprende **MAC de origem -> porta/VLAN**. Se o MAC
de destino estiver na tabela, envia pela porta correspondente; se desconhecido,
faz flooding apenas dentro da VLAN; broadcast/multicast sem tratamento específico
também é replicado nesse domínio.

Entradas dinâmicas expiram por aging. Um MAC que muda rapidamente entre portas
pode indicar loop, dispositivo móvel, virtualização ou cabeamento incorreto.
Tabela cheia pode aumentar flooding. A tabela MAC não é ARP: uma associa MAC a
porta; a outra associa IP a vizinho.

## Método de leitura

Para cada entrada, confirme VLAN, tipo (dinâmica/estática), porta, idade e
contexto. Compare com LLDP, inventário e tabela de vizinhos no gateway; nenhum
artefato isolado identifica com certeza o usuário.

## Exercício

Simule A enviando para B quando a tabela está vazia, B respondendo e A repetindo.
Liste o estado da tabela após cada quadro.
