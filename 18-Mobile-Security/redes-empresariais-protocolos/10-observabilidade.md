# 10 — Observabilidade: SNMP, syslog e fluxos

Métricas dizem quanto/como; logs registram eventos; traces conectam uma transação;
flow records resumem conversas; configuração/topologia fornecem contexto.

SNMPv3 oferece autenticação/privacidade quando configurado; prefira-o a
communities legadas. Syslog precisa de severidade, hostname/ID, timestamp
sincronizado e transporte/armazenamento adequados. NetFlow/IPFIX/sFlow mostram
quem conversa com quem em graus/amostragem diferentes, geralmente sem payload.

Streaming telemetry envia estado estruturado e frequente; polling continua útil.
Defina cardinalidade e retenção para não colapsar a plataforma. Não colete
payload ou identificadores pessoais sem necessidade.

## Golden signals de rede

Disponibilidade, latência, perda, jitter, utilização/saturação, erros/discards,
rotas/vizinhos e mudanças. Alertas precisam de impacto, owner, severidade,
deduplicação e runbook.
