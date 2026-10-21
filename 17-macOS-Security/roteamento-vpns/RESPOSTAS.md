# Respostas orientativas

## Capítulo 03

Os quatro `/24` contíguos de `.0` a `.3` formam `10.20.0.0/22`. Se apenas `.0`
e `.2` existem, anunciar `/22` também atrai `.1` e `.3`; sem rotas específicas,
esses destinos caem na rota null ou podem criar caminho errado.

## Capítulo 10

Route leaking deve enviar corp/guest/IoT ao firewall para DNS/NTP, não importar
todas as rotas diretamente. O retorno precisa conhecer o segmento de origem na
VRF/política correta.

## Projeto

Uma resposta forte distingue IGP de eBGP, calcula estado de falha, filtra rotas,
trata MTU e rota de retorno, e gerencia identidade/chaves. “Túnel up” não é
critério suficiente; transações e SLOs devem ser medidos.
