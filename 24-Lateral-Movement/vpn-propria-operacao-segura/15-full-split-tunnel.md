# 15 — Full tunnel e split tunnel

Full tunnel encaminha rotas padrão ao gateway. Beneficia política central de
egress e proteção em redes não confiáveis, mas aumenta latência, custo,
capacidade e impacto de falha.

Split tunnel anuncia apenas redes necessárias. Preserva saída local e reduz
carga, mas o dispositivo participa simultaneamente de dois domínios e requer
política clara de DNS e firewall.

## Decisão

| Pergunta | Full | Split |
|---|---|---|
| Todo egress precisa de política central? | favorece | não garante |
| Aplicação depende de origem local? | pode quebrar | favorece |
| Gateway suporta toda banda? | obrigatório | menor carga |
| Queda pode interromper internet? | provável | apenas destinos tunelados |
| DNS corporativo é necessário? | simples | exige roteamento por domínio |

## Rotas estreitas

Não anuncie `10.0.0.0/8` se o serviço usa somente `10.20.4.0/24`. Prefixos
amplos criam colisão com redes locais e acesso desnecessário.

## Aplicações excluídas

Split por aplicação é mais complexo e dependente do sistema. Mantenha inventário
e teste atualizações; um novo processo pode não herdar a política esperada.

## Prática

Produza duas configurações sem chaves, compare a tabela de rotas e justifique a
escolha com requisitos, não com preferência.

