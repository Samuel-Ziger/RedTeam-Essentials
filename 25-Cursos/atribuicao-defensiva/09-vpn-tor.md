# 09 — VPN, Tor e infraestrutura intermediária

Quando há VPN, o destino vê o gateway; o provedor VPN pode relacionar cliente e
saída conforme arquitetura e retenção. Uma VPN própria associa atividade à VPS,
mas conta do provedor, administração e logs são fontes separadas.

No Tor, o destino vê um exit. Lista de exits pode contextualizar origem, não
identificar usuário. Um observador amplo pode estudar correlação temporal, mas
isso permanece análise probabilística sujeita a falsos positivos.

## Resposta defensiva

- classifique IP como infraestrutura, não pessoa;
- correlacione conta, sessão, dispositivo e ação;
- procure processo e alteração de configuração no endpoint corporativo;
- compare destino, frequência e política;
- preserve registros centrais;
- contenha sessão/ativo em vez de “caçar” indivíduos externos.

## Bloqueio

Bloquear VPN/Tor pode ser requisito de um ambiente, mas afeta usuários legítimos
e é contornável. Prefira autenticação forte, autorização contextual, proteção de
aplicação e rate limiting. Registre exceções e monitore impacto.

## Infraestrutura adquirida

Provedores cloud hospedam uso legítimo e abusivo. ASN/cloud isolado não prova
ameaça. Atribuição ao locatário exige cooperação e processo adequado.

## Prática

Reavalie um alerta “login via Tor”: proponha contenção de baixo impacto, fontes
adicionais e linguagem que não acusa o titular da conta.

