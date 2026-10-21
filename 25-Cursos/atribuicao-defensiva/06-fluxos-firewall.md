# 06 — Fluxos, firewall e roteamento

NetFlow/IPFIX e logs de firewall resumem comunicações: origem, destino, portas,
protocolo, tempo, bytes, ação e interface. Geralmente não contêm conteúdo.

## Tupla e direção

Uma sessão é descrita por protocolo e tuplas de origem/destino. NAT pode alterar
campos; registre zona/interface e identificador de tradução. “Inbound” depende
do ponto de observação.

## Roteamento

Fluxo mostra que tráfego passou por um exportador, não todo o caminho. ECMP,
assimetria, túnel e balanceamento podem dividir observação. Confirme onde o
sensor está e se amostra pacotes.

## Firewall

`allow` prova decisão da regra, não sucesso da aplicação. `deny` pode ser ruído
de varredura ou erro. Correlacione com handshake, resposta, endpoint e aplicação.

## Baseline

Compare destino raro, porta incomum, periodicidade, volume, primeira ocorrência,
identidade e criticidade. Reputação de IP envelhece e infraestrutura é
reutilizada.

## Prática

Crie três eventos: permitido sem resposta, permitido com aplicação e negado.
Explique por que somente o segundo sustenta uso do serviço.

