# 08 — NAT, CGNAT e registros de tradução

NAT associa temporariamente uma tupla interna a outra externa. Em CGNAT, muitos
assinantes compartilham endereço público. Para resolver uma conexão de volta a
um assinante, normalmente são essenciais:

- IP público e porta de origem após tradução;
- protocolo;
- destino, quando o esquema de log exigir;
- instante preciso, fuso e duração;
- registro de mapeamento e período de validade.

O RFC 6888 discute o volume e implicações de logs de CGN. A obtenção de dados de
provedor depende de processo autorizado/legal; Blue Team não tenta acessar
sistemas externos.

## Dois NATs

Um cliente doméstico pode atravessar NAT no roteador e CGNAT no provedor. O log
do serviço vê somente a tupla pública. O roteador local e o provedor guardam
partes diferentes.

## DHCP e inventário

Dentro da empresa, DHCP, Wi-Fi/NAC e inventário ajudam a ligar IP privado a
dispositivo em determinado momento. Endereço estático sem inventário também é
ambíguo.

## Limite da conclusão

Mesmo mapeamento correto indica conexão atribuída a circuito/dispositivo,
possivelmente comprometido ou compartilhado. Não prova intenção de uma pessoa.

## Prática

Receba um caso sem porta de origem e escreva por que a consulta é inconclusiva.
Liste o pedido mínimo que jurídico poderia avaliar.

