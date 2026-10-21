# 07 — WPA2, WPA3, credenciais e WPS

Use WPA3-Personal (SAE) quando todos os clientes suportarem; caso contrário,
WPA2-Personal com AES/CCMP e senha longa, aleatória e exclusiva. Modo de
transição aumenta compatibilidade, mas herda limites para clientes WPA2. Evite
WEP, WPA/TKIP e redes abertas para dados confiáveis.

WPA protege o enlace Wi-Fi, não o tráfego depois do AP. HTTPS e protocolos
seguros continuam necessários. SSID oculto não é controle de segurança; filtragem
por MAC é fraca porque MACs são observáveis/alteráveis.

Desative WPS se não houver necessidade. Separe senha de administração da senha
Wi-Fi, limite administração à LAN, use MFA quando o serviço cloud oferecer e
não exponha painel na Internet. Atualize firmware e remova contas padrão.

## Rotacionar sem caos

Inventarie clientes, crie janela, altere primeiro AP/roteador, reprovisione por
grupos, valide dispositivos críticos e remova a credencial anterior. Uma rede de
IoT separada reduz impacto de dispositivos difíceis de atualizar.
