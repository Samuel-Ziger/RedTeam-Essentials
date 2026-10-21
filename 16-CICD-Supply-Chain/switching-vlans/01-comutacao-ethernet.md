# 01 — Comutação Ethernet

Um switch recebe quadros, aprende origem e encaminha conforme MAC de destino e
VLAN. Cada porta full-duplex é um enlace independente. Switching reduz colisões,
mas não elimina broadcast nem cria isolamento entre dispositivos na mesma VLAN.

Store-and-forward recebe e valida o quadro antes de transmitir; cut-through
pode iniciar encaminhamento antes, reduzindo latência e potencialmente passando
quadros corrompidos. Implementações variam.

O pipeline pode aplicar ingress classification, VLAN, ACL, QoS, lookup e egress
rewrite. Capacidade de switching, buffers, quantidade/velocidade de portas e
oversubscription determinam desempenho, não apenas taxa nominal por porta.

## Exercício

Desenhe quatro hosts em um switch. Mostre entrega unicast conhecida, unicast
desconhecida e broadcast. Indique por quais portas cada quadro sai e por quê.
