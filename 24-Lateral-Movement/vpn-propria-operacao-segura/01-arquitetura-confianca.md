# 01 — Arquitetura e fronteiras de confiança

Arquitetura mínima de acesso remoto:

```text
cliente --- UDP/Internet ---> VPS:wg0 ---> rede/serviço autorizado
   |                              |
chave privada                 firewall, rotas, DNS e observabilidade
```

O cliente autentica a chave pública do servidor e vice-versa. O túnel protege o
trecho entre os peers. Depois do gateway, HTTPS/SSH continuam responsáveis pela
proteção de aplicação.

## Decisões

- **road warrior:** clientes móveis chegam a um gateway;
- **site-to-site:** gateways anunciam redes atrás deles;
- **full tunnel:** todo tráfego segue ao gateway;
- **split tunnel:** apenas prefixos corporativos seguem ao gateway;
- **egress:** gateway fornece saída para a internet;
- **acesso privado:** gateway apenas alcança redes internas.

Cada decisão altera `AllowedIPs`, firewall, DNS, capacidade e privacidade.

## Fronteiras

Considere dispositivo cliente, rede de acesso, internet, provedor VPS, sistema
da VPS, rede de destino, aplicação e identidade. O provedor pode observar a
conexão à VPS e metadados operacionais; o destino vê o IP do gateway. Contas e
cookies continuam existindo.

## Prática

Desenhe um caso full-tunnel e um split-tunnel. Marque terminação WireGuard,
terminação TLS, fluxo DNS e ponto de registro de cada evento.

