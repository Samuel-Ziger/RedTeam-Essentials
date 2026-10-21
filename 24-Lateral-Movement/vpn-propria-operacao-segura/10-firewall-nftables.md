# 10 — Firewall e NAT com nftables

Descubra nomes reais de interface antes de adaptar o exemplo. Uma política
mínima separa entrada no host e encaminhamento:

```nft
table inet filter {
  chain input {
    type filter hook input priority filter; policy drop;
    ct state established,related accept
    iif "lo" accept
    tcp dport 22 ip saddr <REDE_ADMIN> accept
    udp dport 51820 accept
    ip protocol icmp accept
    ip6 nexthdr ipv6-icmp accept
  }

  chain forward {
    type filter hook forward priority filter; policy drop;
    ct state established,related accept
    iifname "wg0" oifname "ens3" ip saddr 10.66.0.0/24 accept
  }
}

table ip nat {
  chain postrouting {
    type nat hook postrouting priority srcnat; policy accept;
    oifname "ens3" ip saddr 10.66.0.0/24 masquerade
  }
}
```

Substitua `<REDE_ADMIN>` e `ens3`. Se o SSH não tem origem estável, projete
bastion/VPN administrativa antes de restringir; não copie uma regra que cause
lockout.

## Aplicação segura

Valide sintaxe com `sudo nft --check -f arquivo.nft`. Mantenha console fora de
banda e uma cópia do ruleset anterior. Só habilite persistência após testar
entrada, forwarding, retorno e reinício.

## Menor privilégio

Para acesso apenas a uma rede privada, troque saída ampla pelo prefixo e portas
necessários. `AllowedIPs` e firewall devem concordar.

## Prática

Adapte em arquivo temporário de VM, valide com `--check` e explique cada regra e
seu rollback antes de carregar.

