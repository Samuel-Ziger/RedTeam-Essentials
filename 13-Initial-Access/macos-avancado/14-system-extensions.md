# 14 — System Extensions, DriverKit e Endpoint Security

System Extensions executam funcionalidades privilegiadas fora do kernel quando
possível. DriverKit atende classes de dispositivo; Network Extension pertence à
futura trilha de redes. Endpoint Security entrega eventos para produtos defensivos.

Clientes Endpoint Security precisam de entitlement concedido, assinatura e
empacotamento adequados. Eventos `AUTH` exigem resposta dentro do prazo e podem
impactar disponibilidade; eventos `NOTIFY` informam fatos posteriores.

Um produto deve minimizar eventos, cache, dados pessoais, latência e retenção.
Falha segura depende do evento e do modelo de ameaça; não existe política única.

O curso não cria um cliente ES falso nem pede entitlement. Estuda o contrato da
API, arquitetura, lifecycle e telemetria por diagramas e mensagens sintéticas.

## Prática

Projete um cliente somente `NOTIFY` para execuções: campos mínimos, redaction,
backpressure, deadline, upgrade, desinstalação e métricas.
