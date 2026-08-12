# 19 - Segurança wireless

> Arquitetura, análise de capturas fornecidas e defesa Wi-Fi. Não transmita,
> deautentique, clone SSIDs ou capture tráfego de terceiros.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Analistas de rede e Purple Team intermediários. |
| Pré-requisitos | Módulo 00; 802.11 e criptografia em nível introdutório. |
| Tempo estimado | 6 horas de teoria e 3 horas de análise offline. |
| Ambiente | Captura sintética/fornecida ou AP próprio em ambiente RF controlado. |
| Evidência final | Diagrama, baseline e recomendações de configuração/detecção. |
| Critério de conclusão | Diferenciar cinco riscos sem transmitir tráfego ofensivo. |

## Fundamentos e controles

- prefira WPA3-Enterprise ou WPA2-Enterprise com EAP-TLS quando suportado;
- use PMF/802.11w, desative WPS e protocolos legados;
- valide certificado do servidor RADIUS nos clientes;
- segmente clientes, administração, convidados e dispositivos IoT;
- mantenha inventário de AP/BSSID/canal e monitore mudanças;
- trate SSID como rótulo, não como identidade confiável.

## Detecção

Monitore APs não autorizados, BSSID/SSID divergentes, mudanças de segurança,
volume anômalo de management frames, falhas EAP e clientes que retornam a
protocolos fracos. Mudança planejada, roaming e eventos RF transitórios são
fontes comuns de falso positivo.

## Exercício offline

Receba do instrutor uma tabela ou captura sanitizada. Produza inventário de
SSID, BSSID, canal, proteção e horário; compare com baseline aprovada. Não tente
recuperar chaves, identificar pessoas ou correlacionar dispositivos externos.

## Cleanup

Remova cópias derivadas e identificadores desnecessários. Em AP próprio, reverta
SSID/canal/credenciais de teste e confirme segmentação e logging esperados.

