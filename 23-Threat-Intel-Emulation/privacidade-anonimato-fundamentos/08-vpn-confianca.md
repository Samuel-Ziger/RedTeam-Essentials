# 08 — VPN: túnel e troca de confiança

Uma VPN cria uma interface lógica e protege pacotes entre cliente e gateway.
No modo de túnel completo, a rota padrão aponta para essa interface. No split
tunnel, somente prefixos selecionados passam por ela.

```text
cliente == túnel cifrado ==> gateway VPN ----> destino HTTPS
```

Para a rede local e o ISP, o destino imediato passa a ser o gateway. Para o
site, o IP de origem aparente passa a ser o IP de saída do gateway. O gateway,
porém, ocupa uma posição privilegiada: conhece o IP do cliente e participa do
encaminhamento ao destino. HTTPS continua necessário.

## O que avaliar

- propriedade e jurisdição do provedor;
- software cliente, atualizações e permissões;
- protocolo, autenticação e gestão de chaves;
- DNS, IPv6, split tunneling e comportamento na falha;
- política verificável de logs e retenção;
- conta, pagamento e suporte como metadados administrativos;
- resposta a incidentes e transparência.

“Sem logs” é uma afirmação de governança, não uma propriedade matemática do
túnel. Uma VPN própria aumenta controle operacional, mas o provedor da VPS e os
destinos permanecem no modelo de ameaça.

## Casos legítimos

Acesso remoto à empresa, interligação de sites, administração de infraestrutura
e proteção do enlace em rede não confiável. Para anonimato contra adversário
forte, uma única entidade central costuma ser uma premissa inadequada.

## Prática segura

Compare VPN comercial, VPN própria e VPN corporativa em controle, confiança,
metadados, suporte e objetivo. Não escolha uma “melhor” sem declarar a ameaça.

