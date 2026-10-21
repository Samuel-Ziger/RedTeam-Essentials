# 05 — OSPF: estado de enlace

OSPF forma vizinhanças, inunda LSAs e cada roteador calcula shortest-path tree
com uma base de estado de enlace coerente. Custo normalmente deriva de largura
de banda de referência; ajuste consistente evita empates inesperados.

Hello parameters, area, autenticação, timers, MTU e tipo de rede precisam ser
compatíveis para adjacência plena. Em redes multiacesso, DR/BDR reduz adjacências
e flooding; não é o “roteador principal” de dados.

Router ID identifica a instância e deve ser estável/planejado. Interfaces
passivas anunciam a rede sem formar vizinho com endpoint. Autenticação protege
participação, mas deve usar mecanismos atuais suportados e chaves gerenciadas.

## Diagnóstico

Estado down/init/2-way/exstart/exchange/loading/full aponta fases distintas.
Confirme alcance L2/L3, parâmetros, MTU, LSDB, SPF, rota instalada e retorno.
