# Consulta rápida

## Porta de endpoint

Modo access, VLAN explícita, edge STP, BPDU Guard, 802.1X/MAB conforme política,
storm control, descrição, PoE e porta ociosa desativada.

## Trunk

Modo fixo, VLAN nativa coerente, allowlist mínima, MTU, LACP, STP e descrição
iguais nas duas pontas. Valide operacionalmente.

## Ordem de diagnóstico

Físico/erros -> agregação -> STP -> modo/VLAN -> tabela MAC -> ARP/NDP -> SVI
e rota -> ACL/firewall -> serviço.

## Mudança

Intenção, diff, revisão, backup, janela, acesso out-of-band, comandos de
validação, gatilho de rollback e evidência final.
