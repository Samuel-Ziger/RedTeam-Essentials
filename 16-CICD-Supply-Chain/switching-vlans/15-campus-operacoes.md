# 15 — Projeto de campus e operações

Uma arquitetura hierárquica separa acesso, distribuição e core; em ambientes
menores, distribuição/core podem ser colapsados. Acesso conecta endpoints;
distribuição agrega política/limites L3; core transporta com simplicidade e alta
disponibilidade.

Estenda camada 2 apenas quando o requisito superar o custo de falha. Encerrar
VLANs perto do acesso reduz domínio de falha; roteamento nos uplinks facilita
uso de caminhos paralelos. Redundância precisa de chassis, energia, caminho,
fibra e software independentes.

## Operações

Mantenha source of truth, padrão de nomes, backup, NTP, syslog, telemetria,
controle de acesso administrativo, imagens aprovadas, janela e rollback.
Monitore erros/descartes, utilização, PoE, temperatura, mudanças STP, MAC
flapping e estado de agregados.

Toda VLAN e porta deve ter dono/ciclo de vida. Portas ociosas e VLANs antigas
são dívida operacional e de segurança.
