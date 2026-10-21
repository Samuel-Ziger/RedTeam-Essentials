# 11 — SLOs, capacidade e performance

SLI é a medida; SLO é o alvo; SLA é compromisso contratual. Disponibilidade
de caminho não equivale a sucesso da aplicação. Defina SLI ponta a ponta e sinais
por camada para diagnóstico.

Percentis descrevem cauda melhor que média. Meça P50/P95/P99 de RTT e transação,
perda/jitter por classe, utilização no intervalo adequado e microbursts quando a
plataforma permitir. Error budget conecta confiabilidade a velocidade de mudança.

Capacidade considera crescimento, sazonalidade, cabeçalhos, replicação,
oversubscription e estado de falha N-1. Planeje CPU/memória/TCAM, rotas, MACs,
ARP/NDP, ACLs, túneis, sessões, logs e licenças, não apenas Gbit/s.

## Exercício

Para uplinks duplos de 10 Gbit/s, determine capacidade normal e com um link
falho. Se pico previsto é 12 Gbit/s, o estado N-1 viola o SLO mesmo que ECMP
funcione perfeitamente.
