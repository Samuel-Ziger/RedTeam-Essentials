# 11 — Desempenho e cobertura

Defina requisito antes de medir: videoconferência prioriza latência/jitter;
backup prioriza throughput; automação pode exigir cobertura mais que velocidade.

## Isolamento do gargalo

1. teste cabeado diretamente no roteador em condições controladas;
2. confirme velocidade/duplex dos enlaces;
3. teste Wi-Fi próximo ao AP e depois nos pontos-alvo;
4. observe banda, canal, largura, sinal, ruído e ocupação;
5. compare um e vários clientes;
6. meça em horários diferentes;
7. separe LAN local de Internet.

Bufferbloat é latência excessiva sob carga por filas grandes. SQM pode ajudar
ao controlar taxa pouco abaixo do gargalo e aplicar filas justas, ao custo de
CPU/throughput. QoS não cria banda.

Roaming é em grande parte decisão do cliente. Mesmo SSID/segurança facilitam,
mas excesso de potência e sobreposição podem manter cliente preso ao AP distante.

## Exercício

Crie tabela com local, dispositivo, banda, RSSI/SNR, throughput, RTT sem carga e
sob carga. Proponha uma alteração e um critério de sucesso.
