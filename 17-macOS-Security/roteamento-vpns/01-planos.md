# 01 — Plano de dados, controle e gestão

O plano de **dados** encaminha pacotes conforme FIB. O plano de **controle**
aprende topologia/rotas e constrói RIB. O plano de **gestão** configura, atualiza
e observa o equipamento. Separá-los ajuda a raciocinar sobre falhas.

Uma adjacência OSPF ativa não prova que a rota chegou à FIB; uma rota na FIB
não prova que ACL, ARP/NDP ou caminho de volta permitem o fluxo. CPU do plano de
controle pode saturar enquanto forwarding em hardware continua parcialmente.

Proteja gestão em rede/VRF dedicada quando possível, com AAA, MFA via bastion,
protocolos cifrados, allowlist, logs e backups. Out-of-band deve ser realmente
independente de caminhos, energia e credenciais da produção.

## Exercício

Classifique: lookup de pacote, SPF do OSPF, commit de configuração, SNMP, BGP
UPDATE, ARP e atualização de firmware. Alguns atravessam mais de um plano.
