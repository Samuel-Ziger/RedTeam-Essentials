# 04 — WAN, LAN, DHCP e DNS

A interface WAN recebe parâmetros da operadora; a LAN oferece gateway, DHCP e,
frequentemente, encaminhamento DNS aos clientes. Use prefixo privado que não
colida com redes acessadas por VPN. Defina pool, reservas, lease e exclusões.

Reservas são adequadas para impressora, NAS e automação, pois mantêm gestão
central. Se configurar IP estático no dispositivo, mantenha-o fora do pool e
registre gateway/DNS. Nunca crie dois DHCPs acidentalmente.

O roteador pode encaminhar consultas ao resolvedor da operadora, público ou
local. Escolha por política de privacidade, validação DNSSEC, filtragem desejada,
disponibilidade e suporte a DoT/DoH. DoH no aplicativo pode ignorar o resolvedor
local; documente o comportamento antes de diagnosticar.

## Exercício

Planeje `192.168.50.0/24`: infraestrutura `.1-.19`, reservas `.20-.79`, pool
`.100-.199` e espaço futuro. Explique vantagens e limites dessa convenção.
