# 07 — Proxy, reverse proxy e balanceamento

Forward proxy representa clientes e controla saída; reverse proxy representa
servidores e recebe clientes. Ambos podem terminar TLS, autenticar, filtrar,
cachear e registrar, mas ocupam fronteiras de confiança distintas.

Load balancer L4 distribui por conexão/endereço; L7 entende protocolo e pode
rotear por host/path/header. Algoritmos incluem round-robin, least connections,
hash e pesos. Health check deve representar prontidão sem sobrecarregar
dependências; liveness e readiness não são iguais.

Preservar IP do cliente pode usar proxy protocol ou cabeçalho confiável. Nunca
aceite `X-Forwarded-For` de qualquer origem: o proxy de borda deve remover e
reescrever a cadeia. TLS passthrough preserva terminação no backend; termination
centraliza certificados/inspeção e exige proteção até o upstream.

## Falhas

502 aponta resposta inválida/conexão de upstream; 503 falta capacidade/saúde;
504 timeout. Correlacione request ID entre camadas.
