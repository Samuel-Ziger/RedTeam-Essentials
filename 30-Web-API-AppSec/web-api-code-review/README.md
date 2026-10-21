# Web, APIs e revisão segura de código

O percurso usa aplicações vulneráveis locais para ligar comportamento externo,
causa no código, correção e teste de regressão.

## Sequência

1. Prepare o [laboratório Docker](../docker-lab/README.md) e confirme
   que os alvos estão publicados somente em `127.0.0.1`.
2. Revise [reconhecimento web](../acervo/web/recon-web-pratico.md),
   [enumeração](../acervo/web/enum-web-avancado.md) e o
   [OWASP Top 10](../acervo/web/owasp-top10-2021.md).
3. Estude causa-raiz e defesa para
   [SQLi](../acervo/web/sqli-deep-dive.md),
   [XSS](../acervo/web/xss-deep-dive.md),
   [SSRF](../acervo/web/ssrf-deep-dive.md),
   [traversal/LFI](../acervo/web/path-traversal-lfi.md) e
   [autenticação](../acervo/web/auth-bypass-patterns.md).
4. Aplique o [checklist de APIs](../acervo/web/api-security-checklist.md)
   e o material de [APIs modernas](../acervo/web/api-moderna-oauth-graphql-grpc.md).
5. Execute os labs [DVWA](../acervo/labs/lab-01-dvwa-sqli.md),
   [Juice Shop](../acervo/labs/lab-02-juice-xss.md) e
   [VAmPI](../acervo/labs/lab-03-vampi-api.md); consulte respostas
   somente depois em [answers](../acervo/labs/answers/README.md).
6. Feche com [revisão segura de código](../acervo/code-review/LEGADO-SECURE-CODE-REVIEW.md).

## Entrega

Documente ameaça, reprodução mínima, causa-raiz, patch, teste automatizado,
risco residual e reteste. Não envie payloads a sistemas externos.
