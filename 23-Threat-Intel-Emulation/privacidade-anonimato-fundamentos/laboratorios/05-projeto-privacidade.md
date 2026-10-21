# Lab 05 — Projeto integrado de privacidade

Produza o pacote descrito no capítulo 18 para um cenário autorizado. Inclua:

- uma página de escopo e exclusões;
- diagrama de dados e rede;
- matriz de observadores;
- inventário de metadados;
- saída JSON do analisador;
- backlog de controles por impacto e esforço;
- plano de validação e rollback;
- conclusão com risco residual.

## Testes negativos

Modifique uma cópia da fixture para representar:

- endpoint não confiável;
- conta identificada;
- tráfego sem HTTPS;
- VPN com DNS fora do túnel;
- Tor diante de observador global.

O relatório deve detectar todos e nunca afirmar identidade civil.

## Rubrica

São necessários pelo menos dois observadores, três tipos de metadado, três
controles ligados a ameaças e duas limitações. A melhor entrega é verificável e
honesta, não a mais complexa.

