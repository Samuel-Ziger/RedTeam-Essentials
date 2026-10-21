# 14 — Detecção de proxy e remoção de indicadores

O MITRE ATT&CK T1090 descreve uso adversário de proxies; T1070 descreve remoção
ou alteração de indicadores. Estudamos ambos somente para detecção e resiliência.

## Hipótese de proxy não autorizado

Combine:

- novo processo ou ferramenta de encaminhamento;
- listener, conexão persistente ou destino raro;
- alteração de proxy, rota, firewall ou interface;
- usuário/contexto incomum;
- ausência de ticket ou software aprovado;
- tráfego subsequente de outros hosts pelo ativo.

Ferramentas administrativas e desenvolvimento geram falsos positivos. O nome do
binário sozinho não basta.

## Hipótese de remoção

Procure serviço de logging parado, arquivo/trilha alterado, sequência de comando
privilegiado, gap de eventos, desvio de volume e cópia central preservada. Não
ensinamos comandos de limpeza.

## Controles

Envio remoto de eventos, armazenamento separado/imutável, menor privilégio,
monitoramento de saúde, alerta sobre mudança de política e relógio confiável.

## Teste Purple Team seguro

Em vez de apagar logs, injete um evento sintético “sensor_offline” e valide a
detecção de lacuna. Em vez de proxy real, use fixture com processo e fluxo
fictícios.

## Prática

Escreva regra comportamental com positivo, negativo, campos necessários,
triagem e resposta. Inclua dois falsos positivos.

