# 18 — APIs, mobile e service-to-service

CAPTCHA e desafio JavaScript pressupõem navegador e pessoa. APIs de parceiros,
apps mobile, webhooks e workloads precisam de identidade verificável, contrato,
quota e proteção de replay.

## Controles por cliente

- API de usuário: OAuth/OIDC, escopos, autorização por objeto e quota;
- parceiro: credencial por parceiro, mTLS ou assinatura, rota e budget próprios;
- serviço: identidade de workload, credencial curta e policy por serviço;
- webhook: assinatura do corpo canônico, timestamp, nonce e idempotência;
- mobile: PKCE, armazenamento seguro e atestação somente como sinal adicional.

API key identifica um consumidor, mas não deve substituir autorização do
usuário. Chave no aplicativo mobile é recuperável e não pode ser segredo global.

## Gateway e aplicação

O gateway valida formato, tamanho, autenticação, quota e schema. A aplicação
continua responsável por regra de negócio e autorização. Propague uma identidade
assinada ou por canal confiável; não aceite cabeçalho de identidade diretamente
do cliente.

## Automação permitida

Ofereça API oficial para casos válidos, documente limites e use SDK/backoff.
Forçar integração a imitar browser cria incentivos ruins e reduz visibilidade.

## Purple Team

Red usa fixtures para testar token ausente, escopo insuficiente, replay,
idempotência e quota por tenant. Blue distingue erro do cliente, abuso e falha
do provedor de identidade. Purple verifica que a resposta não revela recurso de
outro tenant e que um parceiro não consome o budget de outro.
