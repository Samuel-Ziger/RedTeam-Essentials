# 10 — LLDP, PoE e borda

LLDP anuncia identidade, porta e capacidades a vizinhos diretamente conectados.
LLDP-MED adiciona informações úteis a voz/localização. Use-o para inventário e
validação, mas não como autenticação: dados podem ser falsificados.

PoE entrega energia pelo enlace Ethernet. Orçamento total, potência por porta,
classe, padrão, temperatura e UPS precisam suportar APs, telefones e câmeras.
Um switch com 48 portas PoE pode não alimentar 48 cargas máximas simultaneamente.

## Borda bem definida

Descrição, VLAN, modo access, edge STP, BPDU Guard, limite de MAC quando
adequado, 802.1X/MAB conforme política, storm control e portas ociosas desativadas
formam baseline. Não aplique uma receita sem testar telefones+PC, APs e hypervisors,
que podem precisar de múltiplas VLANs/identidades.
