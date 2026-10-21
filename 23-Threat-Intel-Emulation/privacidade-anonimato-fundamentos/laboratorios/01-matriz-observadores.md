# Lab 01 — Matriz de observadores

## Objetivo

Comparar HTTPS direto, HTTPS sobre VPN e Tor Browser sem gerar tráfego novo.

## Procedimento

1. Desenhe cliente, rede local, ISP, intermediário, DNS e destino.
2. Para cada cenário, marque IP de origem, destino, DNS, conteúdo, conta, tempo
   e volume como `visível`, `parcial` ou `não disponível`.
3. Registre onde TLS e o túnel terminam.
4. Liste uma premissa que, se falsa, muda cada conclusão.
5. Execute o analisador sobre a fixture e compare os achados.

```bash
python3 ../exemplos/privacy_model.py ../fixtures/cenario-pesquisa.json
```

## Aceite

Você deve explicar por que o destino ainda conhece dados da aplicação e por
que uma VPN desloca confiança para o gateway.

