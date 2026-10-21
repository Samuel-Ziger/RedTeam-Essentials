# 04 — Roteamento dinâmico e métricas

Protocolos IGP operam dentro de um domínio administrativo; EGP/BGP troca
alcançabilidade entre sistemas autônomos e aplica política. Distance-vector,
link-state e path-vector distribuem informação de maneiras diferentes.

Convergência é o intervalo entre mudança e visão/encaminhamento estável. Inclui
detecção, propagação, cálculo e instalação. Timers agressivos demais aumentam
CPU/falsos positivos; BFD pode fornecer detecção rápida separada.

Métricas não são comparáveis entre protocolos. Redistribuição exige tagging,
filtros e prevenção de feedback; caso contrário, rotas voltam ao protocolo de
origem e criam loops.

## Decisão

Escolha por escala, topologia, interoperabilidade, política, equipe e operação.
Não introduza roteamento dinâmico onde duas rotas estáticas documentadas resolvem
com menor risco.
