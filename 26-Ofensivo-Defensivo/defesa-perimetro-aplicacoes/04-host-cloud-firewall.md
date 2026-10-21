# 04 — Firewalls de host e cloud

Camadas se complementam. O firewall de host conhece processos, perfis e
interfaces; o de rede controla caminhos; security groups, NACLs e firewalls de
nuvem aplicam política no plano virtual. O nome do recurso varia por provedor,
assim como estado, precedência, logging e comportamento de retorno.

## Linux e Windows

No Linux moderno, `nftables` organiza tabelas, chains, hooks, sets e regras.
`firewalld` oferece zonas e serviços sobre um backend. No Windows, Defender
Firewall usa perfis Domain/Private/Public, direção, programa, serviço, porta e
endereço. Não desative o firewall para diagnosticar; crie um teste e uma regra
temporária estreita.

Exemplo declarativo, não comando de produção:

```text
regra: APP-HTTPS-FROM-EDGE
entrada: edge-subnet -> tcp/8443
programa: app-server
perfis: privado/domínio
log: conexão negada e amostra de aceita
```

## Nuvem

Pergunte se a regra é stateful, em qual objeto se associa, como IPv6 é tratado,
quem pode mudá-la e onde os flow logs aparecem. Evite endereço administrativo
global. Use bastion, acesso just-in-time ou plano de gestão autenticado.

## Deriva e prova

Compare estado desejado com efetivo. Uma revisão de IaC não detecta mudança
manual se você nunca consulta o plano real. Alertas devem apontar identidade,
objeto, diferença, ticket e risco.

## Teste Purple

Red fornece matriz de conectividade positiva e negativa. Blue verifica contador,
flow log e regra responsável. Purple inclui reinício/redeploy, IPv6 e remoção da
regra temporária. O teste termina com evidência de que a porta não ficou aberta.
