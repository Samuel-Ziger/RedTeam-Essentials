# 16 — Kill switch e falhas seguras

Kill switch é um conjunto de regras que impede tráfego protegido de usar a
interface física quando o túnel não está disponível. Ele reduz fallback
acidental, mas pode bloquear administração, DNS, portal cativo e atualizações.

## Requisitos

- permitir o endpoint WireGuard pela interface externa;
- permitir loopback e tráfego local explicitamente necessário;
- encaminhar o restante somente por `wg0`;
- decidir política IPv6 e DNS;
- sobreviver a troca de rede e reinício;
- ter rollback local ou fora de banda.

Não copie uma regra universal. Desktop, servidor e mobile possuem gerenciadores
diferentes. Uma regra baseada no IP do endpoint precisa lidar com mudanças; uma
baseada em marca de pacote exige compreender policy routing.

## Testes

1. túnel ativo;
2. interface derrubada;
3. processo WireGuard parado;
4. endpoint indisponível;
5. troca de Wi-Fi;
6. reinício;
7. rollback.

Para administração remota, não ative antes de provar console de recuperação.

## Prática

Escreva uma tabela de estado e resultado. Implemente somente em VM local e
registre contadores que demonstram bloqueio e exceções.

