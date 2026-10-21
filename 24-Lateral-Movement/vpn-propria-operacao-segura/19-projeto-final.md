# 19 — Projeto final e runbook

Implante primeiro em duas VMs; a etapa VPS é opcional e exige ativo próprio.

## Entregáveis

1. requisitos e modelo de ameaça;
2. diagrama e fronteiras de confiança;
3. matriz full/split e decisão;
4. plano IPv4, IPv6, DNS e rotas;
5. inventário de peers sem segredos;
6. templates gerados e revisão de `AllowedIPs`;
7. firewall, forwarding e rollback;
8. testes de handshake, serviço, DNS, MTU e queda;
9. monitoramento e retenção;
10. runbooks de patch, revogação, restauração e encerramento.

## Gate de produção

- [ ] console fora de banda comprovado;
- [ ] nenhuma chave privada no repositório;
- [ ] acesso administrativo testado em nova sessão;
- [ ] regras mínimas e persistência verificadas após reinício;
- [ ] IPv4/IPv6/DNS têm comportamento explícito;
- [ ] owner e revisão de cada peer definidos;
- [ ] backup restaurado em ambiente descartável;
- [ ] riscos residuais comunicados.

## Critério final

O serviço deve cumprir o objetivo de conectividade e confidencialidade do
túnel. O relatório não pode afirmar anonimato: deve explicar ISP, provedor VPS,
gateway, destino, aplicação e conta como posições de observação distintas.

