# 12 — QoS e filas

QoS gerencia congestionamento; não cria capacidade. O ciclo inclui classificar,
marcar, policiar, modelar, enfileirar e descartar. DSCP marca IP; PCP marca
802.1Q. Uma fronteira de confiança decide quais marcações aceitar ou reescrever.

Prioridade estrita ajuda tráfego sensível, mas sem limite pode faminto outras
filas. Weighted queuing distribui capacidade; shaping suaviza saída; policing
descarta/remarca acima do contrato. WRED e algoritmos modernos sinalizam/evitam
filas cheias conforme plataforma.

## Processo

Defina aplicação, requisito de latência/jitter/perda, volume, ponto real de
congestionamento e métrica. Marque perto da origem confiável, preserve/revalide
em domínios e confirme que a operadora respeita o contrato.

## Exercício

Crie classes para voz, vídeo interativo, aplicações críticas e best effort em um
uplink de 100 Mbit/s. Explique limites e comportamento quando todas saturam.
