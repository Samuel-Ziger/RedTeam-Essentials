# Cheatsheet WireGuard e operação

## Geração local de chaves

```bash
umask 077
wg genkey | tee private.key | wg pubkey > public.key
```

Não execute com histórico/captura compartilhada. Uma chave por dispositivo;
revogue o peer perdido, não compartilhe a mesma chave com a equipe.

## Estado

```bash
sudo wg show
ip address show dev wg0
ip route show table all
sudo nft list ruleset
resolvectl status
```

`latest handshake` indica comunicação recente, não saúde completa da aplicação.

## Ordem de diagnóstico

1. relógio e chaves públicas;
2. UDP liberado e endpoint correto;
3. handshake;
4. IP do túnel e `AllowedIPs`;
5. forwarding;
6. firewall/NAT;
7. DNS;
8. MTU;
9. IPv6 e comportamento na falha.

## Mudança segura

Backup → console fora de banda → janela → aplicar → testar em nova sessão →
observar → confirmar persistência → documentar → rollback se necessário.

