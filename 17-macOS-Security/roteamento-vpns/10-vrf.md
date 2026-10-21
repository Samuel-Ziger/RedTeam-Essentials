# 10 — VRF e segmentação L3

VRF cria tabelas de roteamento separadas no mesmo equipamento. Prefixos podem se
repetir entre VRFs sem colidir. Interfaces, rotas, protocolos e serviços precisam
ser associados ao contexto correto.

VRF-Lite oferece separação local sem MPLS. L3VPN MPLS usa route distinguishers
para unicidade e route targets para política de importação/exportação. RD não
é política; RT não é identificador de segurança por si só.

Route leaking conecta VRFs deliberadamente, por exemplo a DNS compartilhado ou
firewall. Cada vazamento deve ser mínimo, documentado e filtrado nos dois
sentidos. Uma default compartilhada pode criar caminho de retorno inesperado.

## Exercício

Modele corp, guest, IoT e management em VRFs. Permita DNS/NTP compartilhados via
firewall e negue comunicação direta. Desenhe rotas de ida e volta.
