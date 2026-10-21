# 05 — IP, NAT, CGNAT e atribuição

Um IP público identifica um ponto de conectividade em certo intervalo, não uma
pessoa. Endereços podem ser dinâmicos, compartilhados, traduzidos ou usados por
gateways. Para sessões TCP/UDP, a combinação relevante inclui protocolo, IPs,
portas e tempo.

## NAT e NAPT

O roteador mantém mapeamentos entre origem interna e origem externa. Vários
dispositivos podem compartilhar um IP público por portas diferentes. O RFC 4787
define comportamentos de mapeamento e filtragem para UDP; NAT não deve ser
tratado como controle de segurança equivalente a firewall.

## CGNAT

Provedores podem compartilhar um IPv4 entre assinantes. O RFC 6598 reserva
`100.64.0.0/10` para esse espaço. Uma correlação tecnicamente útil pode exigir
IP público, porta de origem, protocolo, instante preciso, fuso e registros do
provedor — sujeitos a processo legal e retenção aplicável.

## IPv6

IPv6 reduz a necessidade de NAT, mas não elimina firewall nem questões de
privacidade. Endereços temporários podem reduzir a estabilidade do identificador
de interface; prefixo, conta, aplicação e outros sinais continuam disponíveis.

## Erros comuns

- atribuir autoria porque dois eventos usam o mesmo IP;
- ignorar porta e relógio em CGNAT;
- interpretar geolocalização de IP como posição física exata;
- assumir que VPN remove logs de endpoint ou aplicação.

## Prática segura

Explique três pessoas ou dispositivos que podem aparecer sob o mesmo IP sem
serem o mesmo autor. Liste evidências adicionais e limitações jurídicas.

