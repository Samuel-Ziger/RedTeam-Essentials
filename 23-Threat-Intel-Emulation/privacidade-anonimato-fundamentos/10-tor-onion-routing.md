# 10 — Tor e onion routing

O Tor Browser constrói um circuito normalmente composto por guard, relay
intermediário e exit. Camadas criptográficas permitem que cada relay conheça
somente o necessário para encaminhar. O site vê o endereço do exit, não o IP
original; a rede local vê conexão à rede Tor, não o destino final.

## Fronteiras de confiança

- o **guard** conhece o IP de origem, mas não o destino em claro;
- o **relay intermediário** conecta partes do circuito;
- o **exit** conecta ao destino e pode ver tráfego sem criptografia de aplicação;
- o **destino** vê o exit e os dados fornecidos pelo navegador/aplicação;
- um observador amplo pode tentar correlacionar tempo e volume nas extremidades.

Por isso, HTTPS continua obrigatório para sites comuns. Aplicações externas não
são protegidas apenas porque o Tor Browser está aberto. Torrent, plugins e
documentos abertos em aplicativos externos podem criar fluxos fora do modelo.

## Identidade e comportamento

Entrar em uma conta identificada informa a identidade ao serviço. Alterar o Tor
Browser com extensões ou configurações incomuns pode aumentar fingerprinting.
O projeto recomenda seguir a documentação oficial e manter expectativas
realistas: Tor melhora propriedades específicas, não garante anonimato perfeito.

## Prática segura

Produza uma matriz para guard, relay, exit e destino. Depois avalie dois casos:
site HTTPS sem login e site HTTPS com conta pessoal. Explique a diferença.

