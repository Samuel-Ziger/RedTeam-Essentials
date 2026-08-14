# Ética, escopo e Rules of Engagement

## Regra central

Ter capacidade técnica não significa ter autorização. Uma atividade só deve
começar quando houver autorização escrita, escopo inequívoco e regras de
execução. Em caso de dúvida, pare e peça decisão ao responsável pelo exercício.

## Modelo mínimo de RoE

| Campo | Exemplo exclusivo de laboratório |
|-------|-----------------------------------|
| Objetivo | Validar três falhas no DVWA local e suas detecções. |
| Alvos permitidos | `127.0.0.1:8081` e container `rte-dvwa`. |
| Exclusões | Host, outros containers, internet e dados reais. |
| Janela | 2026-08-12, 14:00–16:00 UTC. |
| Permitido | Navegação, proxy e payloads não destrutivos do roteiro. |
| Proibido | DoS, persistência, exfiltração real e mudança de escopo. |
| Parada | Instabilidade, dado real, alvo inesperado ou pedido do responsável. |
| Evidência | Requisição/resposta sanitizada e timestamp. |
| Cleanup | Reset do app e `docker compose down -v`. |

## Minimização e cadeia de custódia

Colete o mínimo que comprova o achado. Substitua dados sensíveis por canários,
mas nunca altere silenciosamente uma evidência. Registre origem, coletor,
horário UTC, hash SHA-256, armazenamento e cada transferência. Não faça commit
de credenciais, tokens, dumps, chaves privadas ou dados pessoais.

## Critérios de parada

Pare imediatamente quando:

- o endereço resolvido não estiver no escopo;
- surgir dado pessoal ou segredo não previsto;
- houver degradação, indisponibilidade ou efeito destrutivo;
- uma ferramenta tentar pivotar, persistir ou atingir terceiros;
- o contato autorizado revogar ou pausar o teste.

Documente a parada; não tente “terminar rapidamente” antes de comunicar.

