# Lab 03 — Roteamento e firewall

Adicione uma terceira VM como serviço de destino. Não use internet pública.

1. habilite forwarding por arquivo `sysctl.d`;
2. aplique policy drop em `forward`;
3. permita somente cliente VPN → porta fictícia do serviço;
4. escolha rota de retorno ou NAT e documente a consequência;
5. prove caso permitido e duas negativas;
6. reinicie e valide persistência;
7. execute rollback.

## Testes negativos

- outra porta deve falhar;
- outro peer deve falhar;
- origem forjada fora do `AllowedIPs` deve ser rejeitada pelo desenho;
- SSH administrativo deve continuar acessível pelo canal planejado.

## Aceite

Contadores mostram somente a regra esperada. Uma regra `accept` ampla não passa.

