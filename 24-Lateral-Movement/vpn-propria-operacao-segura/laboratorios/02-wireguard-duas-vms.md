# Lab 02 — Túnel entre duas VMs

Crie duas VMs em rede isolada: servidor e cliente. Gere chaves dentro de cada
VM, configure apenas o prefixo `10.66.0.0/24` e não habilite rota padrão.

## Passos

1. instale WireGuard pelos repositórios;
2. confirme relógio e interfaces;
3. configure servidor e um peer;
4. configure cliente com `AllowedIPs = 10.66.0.0/24`;
5. suba servidor, depois cliente;
6. valide handshake, endereço e alcance ao IP do túnel;
7. derrube ambos e confirme remoção das rotas.

## Evidência sanitizada

Versão, estado da interface, presença de handshake e contadores. Redija chaves
públicas/endpoints se a evidência sair do ambiente.

## Cleanup

Destrua as chaves e VMs descartáveis. Não publique `wg0.conf` real.

