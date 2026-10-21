# 06 — Gerações 802.11 e capacidade

Nomes comerciais simplificam famílias: Wi-Fi 4 (802.11n), 5 (ac), 6/6E (ax) e
7 (be). Novas gerações melhoram eficiência, uso simultâneo e latência, mas o
resultado depende de AP, cliente, banda, largura, streams e ambiente.

Não some taxas de todas as bandas para prometer velocidade a um único cliente.
O PHY rate exibido inclui codificação e overhead; throughput útil é menor.
OFDMA divide recursos entre clientes; MU-MIMO permite transmissões paralelas em
condições adequadas; BSS coloring ajuda coexistência no 802.11ax.

Clientes antigos podem impor modos de compatibilidade. Separe decisão de compra
de decisão de projeto: mais antenas, streams ou número na caixa não corrige AP
mal posicionado nem uplink de 100 Mbit/s.

## Medição

Compare teste cabeado, teste próximo ao AP e teste no local problemático. Registre
RSSI/SNR quando disponível, banda, canal, largura, taxa de link, throughput,
latência e perda. Mude uma variável por vez.
