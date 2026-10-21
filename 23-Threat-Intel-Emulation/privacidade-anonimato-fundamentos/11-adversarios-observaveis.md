# 11 — Comportamentos adversários vistos pela defesa

Agentes de ameaça podem abusar de proxies, VPNs comprometidas, relays e
infraestrutura adquirida para intermediar comunicações. O MITRE ATT&CK descreve
isso em **T1090 — Proxy**. Também podem tentar remover artefatos, comportamento
catalogado em **T1070 — Indicator Removal**.

Aqui esses temas são estudados do lado defensivo. Não implementamos cadeias
furtivas nem remoção de indicadores. Perguntamos quais sinais permanecem:

- processo que abriu a conexão e identidade que o executou;
- alteração de proxy, rota, firewall ou interface;
- destino novo, ASN, reputação e frequência;
- DNS anterior, TLS, duração, bytes e periodicidade;
- autenticação, sessão de aplicação e ações realizadas;
- lacuna inesperada ou interrupção no envio de logs;
- evento central que sobrevive à alteração do host.

| Intenção adversária (abstrata) | Rastros que podem permanecer | Resposta Blue Team |
|---|---|---|
| intermediar a origem | processo, configuração, handshake, flow e sessão | correlacionar endpoint, rede e identidade |
| usar infraestrutura descartável | criação cloud, DNS, certificado, ASN e padrão temporal | preservar histórico e agrupar por comportamento |
| misturar-se a serviços comuns | destino permitido com processo/volume incomum | usar contexto e baseline, não bloqueio cego |
| cifrar o conteúdo | metadados, endpoint, autenticação e efeito na aplicação | detectar comportamento nas extremidades |
| reduzir telemetria | heartbeat ausente, política alterada, cópia central divergente | separar falha de coleta de adulteração |
| abusar de ativo legítimo comprometido | login, mudança administrativa e desvio do ativo | conter conta/host e cooperar pelo processo correto |

## O custo da certeza

Um IP de VPN ou Tor não prova malícia. Bloqueio absoluto pode prejudicar
pesquisadores e usuários legítimos. Detecção útil combina contexto: processo
incomum, destino raro, sequência temporal, privilégio, ativo crítico e desvio de
política.

## Resiliência de evidência

Encaminhe logs relevantes para armazenamento central com controle de acesso e
integridade. Monitore saúde da coleta. A ausência súbita de telemetria é um
sinal a investigar, não uma autorização para concluir autoria.

## Prática segura

Crie uma hipótese de detecção com um sinal de rede, um de endpoint e um de
identidade. Liste dois falsos positivos e um teste negativo.
