# 09 — Proxies, relays e bastions

Um proxy encaminha tráfego para uma aplicação ou protocolo. Um proxy HTTP
entende HTTP; um proxy SOCKS transporta conexões de forma mais genérica; um
reverse proxy recebe tráfego em nome de servidores. Bastion é um ponto
administrativo controlado, não uma ferramenta de anonimato.

## Cobertura é decisiva

Configurar um navegador para usar proxy não altera automaticamente atualizador,
cliente de e-mail, DNS do sistema ou outros processos. Aplicações também podem
ignorar configuração global. Portanto, a pergunta correta é: quais fluxos
entram no intermediário, por qual regra e como a falha se comporta?

## Cadeias e complexidade

Adicionar intermediários aumenta dependências, latência e possibilidades de
erro. Não há soma automática de confiança: cada relay pode registrar metadados,
ser configurado incorretamente ou observar um trecho. Este curso não ensina
cadeias para ocultar origem; ensina a reconhecer arquiteturas, testar cobertura
e mapear observáveis defensivos.

## Sinais para Blue Team

Destinos de proxy não autorizados, alterações de configuração, novos processos
de tunelamento, padrões de conexão persistentes e desvios do baseline merecem
investigação. Um indicador isolado também pode representar suporte legítimo,
desenvolvimento ou acesso corporativo.

## Prática segura

Escolha navegador, sistema operacional e uma aplicação. Documente onde cada um
obtém a configuração de proxy e qual tráfego ficaria fora. Não conecte a proxies
públicos desconhecidos.

