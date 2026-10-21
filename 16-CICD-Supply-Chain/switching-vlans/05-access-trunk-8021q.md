# 05 — Portas access, trunk e IEEE 802.1Q

Porta **access** associa tráfego do endpoint a uma VLAN, normalmente enviando e
recebendo quadros sem tag. **Trunk** transporta múltiplas VLANs com tag 802.1Q.
A tag inclui PCP (prioridade), DEI e VLAN ID.

A VLAN nativa pode trafegar sem tag em certos desenhos. Divergência entre as
duas pontas cria vazamento ou conectividade imprevisível; prefira tag consistente
quando a plataforma permitir e não use a nativa para dados sensíveis.

Permita no trunk somente VLANs necessárias. Configuração dinâmica de trunk pode
ser inadequada em borda; fixe modo e desative negociação quando aplicável. Um
endpoint comum não deve receber trunk por acidente.

## Checklist de duas pontas

Modo, VLAN access/nativa, VLANs permitidas, MTU, LACP, velocidade/duplex,
descrição e STP precisam concordar. Valide estado operacional, não apenas
configuração pretendida.
