# 12 — BunkerWeb

BunkerWeb é um reverse proxy/WAF aberto que integra recursos de segurança e
pode ser implantado em Docker, Linux e orquestradores. A documentação oficial
deve ser consultada para versão, requisitos e variáveis atuais.

## Arquitetura

Separe três planos:

1. dados: cliente → BunkerWeb → aplicação;
2. gestão: scheduler/API/UI e configuração;
3. observabilidade: logs, métricas e alertas.

A Web UI é sensível porque altera configuração. Mantenha-a atrás do próprio
controle ou em rede administrativa, com credencial forte, TOTP, trusted proxy
correto, segredos persistentes e backup testado.

## Antibot

Modos documentados incluem cookie, JavaScript e integrações CAPTCHA. Eles não
devem ser ligados globalmente sem medir APIs, acessibilidade, crawlers
verificados e clientes sem JavaScript. Uma API de máquina precisa de identidade,
quota e contrato, não de desafio visual.

## Implantação

- fixe versão e verifique integridade da imagem;
- use redes dedicadas entre proxy, UI e aplicação;
- publique somente portas necessárias;
- monte segredos fora do repositório;
- comece em detecção, execute testes e prepare rollback;
- persista apenas dados necessários e restaure um backup em teste.

O arquivo `fixtures/bunkerweb-compose.exemplo.yml` é um modelo didático que não
contém segredo nem é iniciado pela automação. Resolva a imagem para digest antes
de qualquer uso e ajuste conforme o guia oficial.

## Exercício Purple

Red revisa exposição, headers, rotas e resultados do conjunto de casos local.
Blue ajusta uma exceção estreita, prova os logs e reverte. Purple compara o
resultado com a mesma matriz aplicada ao WAF gerenciado: controle e evidência
devem ser portáveis, mesmo quando a sintaxe não é.
