# 14 — IPsec e IKE

IPsec protege pacotes IP. ESP oferece confidencialidade/integridade; tunnel mode
encapsula o pacote IP original e é comum em site-to-site. IKE autentica peers,
negocia algoritmos, cria IKE SA e Child SAs e gerencia rekey.

Defina propostas modernas compatíveis, grupos de troca de chaves, identidades,
lifetimes, PFS, seletores de tráfego e DPD. Não use combinações obsoletas apenas
porque um template antigo funciona. PSKs devem ser fortes, exclusivas por peer e
armazenadas como segredo; certificados são preferíveis em escala.

NAT-T encapsula ESP em UDP quando NAT está no caminho. MTU/MSS, fragmentação,
rotas e política são fontes comuns de “túnel up, aplicação down”.

## Diagnóstico

Separe IKE SA, Child SA, contadores de encaps/decaps, seletores, replay/drop,
rota, NAT exemption, firewall, MTU e retorno. Compare as duas pontas e horários.
