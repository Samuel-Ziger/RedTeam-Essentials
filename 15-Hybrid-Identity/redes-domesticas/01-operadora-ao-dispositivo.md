# 01 — Da operadora ao dispositivo

O caminho pode conter rede de acesso da operadora, modem/ONT, roteador, switch,
ponto de acesso e cliente. A operadora pode entregar IPv4 público, CGNAT,
IPv6 ou combinação. PPPoE, DHCP e IP estático são formas de provisionar a WAN.

Documente demarcação: até onde a operadora responde, quem administra o CPE e
qual equipamento termina fibra/coaxial. Velocidade contratada é diferente de
capacidade Wi-Fi e throughput de um dispositivo.

## Fluxo de dependências

energia -> sinal da operadora -> sincronismo/registro -> endereço WAN -> rota
default -> DNS -> transporte -> aplicação. LEDs ajudam, mas confirme significado
no manual; um LED “Internet” pode refletir apenas um teste do fabricante.

## Exercício

Desenhe o caminho de um notebook até um site. Marque onde ocorre conversão de
meio, NAT, firewall, DNS e Wi-Fi. Indique o responsável por cada trecho.
