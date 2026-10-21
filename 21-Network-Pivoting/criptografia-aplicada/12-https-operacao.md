# 12 — HTTPS, proxy e operação

HTTPS combina HTTP com TLS; redirects e HSTS ajudam a evitar downgrade inicial,
mas só após configuração e rollout cuidadosos. Cookies precisam de Secure,
HttpOnly e SameSite conforme uso. Proxy reverso deve preservar esquema/host por
canal confiável e proteger o trecho upstream.

Monitore dias até expiração, falhas de handshake, versão/suite, erro de nome,
cadeia incompleta e relógio. Não desabilite validação para “resolver” ambiente;
distribua a CA correta ou use certificado adequado.

## Prática

Escreva runbook para “funciona no curl com -k, falha no cliente” sem manter `-k`.
