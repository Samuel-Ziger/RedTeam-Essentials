# 08 — RSTP, MSTP e proteções

RSTP (802.1w incorporado ao 802.1Q) usa papéis root, designated, alternate e
backup e converge rapidamente com proposal/agreement. MSTP mapeia várias VLANs
a um número menor de instâncias, equilibrando caminhos sem uma árvore por VLAN.

Região MST exige nome, revision e mapeamento VLAN-instância idênticos. Uma
divergência cria fronteira; valide digest/estado segundo a plataforma.

## Proteções

- BPDU Guard bloqueia porta de borda que recebe BPDU;
- Root Guard impede que uma porta torne o vizinho raiz;
- Loop Guard reduz forwarding indevido quando BPDUs somem;
- storm control limita broadcast/multicast/unknown unicast;
- UDLD ou mecanismo equivalente detecta enlace unidirecional.

Nomes e comportamentos variam. Proteção sem procedimento de recuperação pode
transformar erro transitório em indisponibilidade prolongada.
