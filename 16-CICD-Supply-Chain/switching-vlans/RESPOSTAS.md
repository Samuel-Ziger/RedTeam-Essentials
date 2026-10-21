# Respostas orientativas

## Capítulo 02

Com tabela vazia, A->B é inundado e o switch aprende A. Na resposta B->A, ele
aprende B e encaminha apenas à porta de A. A repetição A->B é unicast conhecido.

## Capítulo 03

Cada switch replica o broadcast pela outra ligação; o quadro retorna e não tem
TTL L2. Cópias crescem, MACs alternam de porta e o plano de controle/dados satura.

## Projeto

Uma solução forte define root e gateway deliberadamente, calcula PoE/oversubscription
no estado de falha, limita VLANs nos trunks e especifica fail mode do 802.1X. A
quantidade de VLANs é consequência de políticas, não objetivo.
