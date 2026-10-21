# 25 — Rastreabilidade e atribuição defensiva

Este módulo fecha a trilha mostrando como Blue Teams investigam atividades em
ambientes próprios ou formalmente autorizados. O foco é correlacionar sinais de
rede, identidade, endpoint, aplicação e nuvem sem transformar coincidência em
certeza e sem invadir a privacidade de terceiros.

IP não é identidade. NAT, CGNAT, VPN, Tor, proxies, dispositivos compartilhados,
relógios desalinhados e credenciais comprometidas tornam a atribuição uma
hipótese graduada. A conclusão responsável declara evidências, lacunas,
explicações alternativas e autoridade legal.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | SOC, Blue Team, DFIR, detection engineering, privacidade e resposta a incidentes. |
| Pré-requisitos | Módulos 05, 14–18 e 23–24. |
| Tempo estimado | 180–280 horas. |
| Ambiente | Eventos totalmente sintéticos ou telemetria da própria organização sob autorização. |
| Evidência final | Linha do tempo, grafo de correlação, pacote de evidências, hipóteses concorrentes e plano de contenção. |
| Critério de conclusão | Correlacionar fontes com relógio e proveniência, graduar confiança e rejeitar conclusões além da evidência. |

## Comece aqui

- [Curso completo](atribuicao-defensiva/README.md)
- [Laboratórios](atribuicao-defensiva/laboratorios/README.md)
- [Correlator e cadeia de evidência](atribuicao-defensiva/exemplos/README.md)
- [Consulta rápida](atribuicao-defensiva/CHEATSHEET.md)

## Limites obrigatórios

- investigar somente sistemas e dados sob autoridade explícita;
- não perseguir, doxxear ou tentar identificar pessoas fora do incidente;
- não atribuir autoria com base apenas em IP, ferramenta, idioma ou fuso;
- preservar logs centralmente e registrar toda transformação;
- envolver jurídico, privacidade e autoridades competentes quando necessário.

## Vídeos em português

Os exemplos externos complementam as fixtures locais e não autorizam coleta
em sistemas de terceiros.

1. [Resolvendo os principais incidentes de segurança das redes brasileiras](https://www.youtube.com/watch?v=n2Yi0c76x4c) — **NIC.br**.
2. [O que é o MITRE ATT&CK? TTPs e Pirâmide da Dor](https://www.youtube.com/watch?v=TYlx5JSLC-s) — **Segurança Descomplicada**.
3. [MITRE ATT&CK Framework](https://www.youtube.com/watch?v=BKNNlqxbiS4) — **Academia de Forense Digital**.
4. [Cyber Kill Chain e MITRE ATT&CK na prática](https://www.youtube.com/watch?v=DCzgq9SYte4) — **SecDay**.
5. [Cyber Threat Intelligence e Threat Hunting](https://www.youtube.com/watch?v=TV6d17bfO1k) — **Kraken Academy**.
