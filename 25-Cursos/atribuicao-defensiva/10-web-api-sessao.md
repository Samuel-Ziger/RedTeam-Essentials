# 10 — Web, API e sessão

Aplicações possuem a telemetria mais próxima do efeito: rota, método, status,
tenant, principal, objeto, autorização, request ID e mudança de estado.

## IDs

Gere `request_id` na borda confiável, propague entre serviços e devolva versão
segura ao cliente. Não aceite cegamente um ID fornecido externamente. Diferencie
request, trace, sessão, token e transaction ID.

## Endereço do cliente

Em cadeia de proxies, configure lista de proxies confiáveis. O primeiro endereço
não confiável na cadeia pode representar cliente; `X-Forwarded-For` arbitrário
do usuário não é evidência.

## Autorização

Registre principal, tenant, política/decisão e objeto sem colocar token ou dado
sensível. Um HTTP 200 não diz se a ação era autorizada; o log da camada de
política precisa completar o contexto.

## Idempotência e replay

Chaves de idempotência, nonce e versão ajudam a diferenciar repetição legítima
de replay. Nunca registre segredo completo; use referência e resultado.

## Prática

Defina um schema de audit log para “alterar papel de usuário”. Inclua antes/depois
mínimo, ator, alvo, tenant, decisão e request ID.

