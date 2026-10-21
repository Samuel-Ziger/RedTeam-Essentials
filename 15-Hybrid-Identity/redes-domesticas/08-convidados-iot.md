# 08 — Convidados, IoT e segmentação

Uma rede de convidados deve separar visitantes da LAN, aplicar isolamento entre
clientes quando apropriado e permitir somente Internet/serviços explícitos.
IoT merece segmento próprio porque ciclos de atualização e modelos de confiança
diferem de notebooks e telefones.

Segmentar não basta: defina matriz de fluxos. Uma TV pode precisar de Internet,
DNS, NTP e descoberta/controlador local; uma câmera pode falar apenas com NVR.
mDNS/SSDP não atravessam sub-redes automaticamente; refletor/proxy de descoberta
amplia alcance e risco, então habilite apenas onde entendido.

Em roteadores simples, “rede de convidados” pode ser apenas outro SSID com
isolamento parcial. Valide se há sub-rede distinta, bloqueio LAN e IPv6 coberto.

## Matriz mínima

| Origem | Destino | Serviço | Decisão |
|---|---|---|---|
| convidados | LAN | qualquer | negar |
| IoT | Internet | DNS/NTP/HTTPS | permitir conforme necessidade |
| administração | IoT | gestão | permitir |

Teste os dois sentidos e registre exceções.
