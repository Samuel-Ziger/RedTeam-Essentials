# Respostas orientativas e rubrica

Os laboratórios aceitam projetos diferentes. Use esta rubrica para avaliar
raciocínio e evidência, não para copiar uma configuração universal.

## 01 — Modelo e matriz

Uma boa entrega diferencia rede, HTTP, identidade e regra de negócio; inclui
IPv6 e egress; protege a origem e associa cada fluxo a owner e evidência.

## 02 — WAF/CRS

O caso legítimo deve passar após exclusão estreita. Remover uma regra global,
elevar permanentemente o limiar ou permitir a rota inteira reprova o objetivo.

## 03 — Cloudflare/BunkerWeb

A comparação deve tratar plano de dados/controle, origem, logging, rollback,
dependência e operação. Lista de funcionalidades sem risco não é suficiente.

## 04 — Bots

A classificação correta preserva API autenticada e bot verificado, mas reage
progressivamente a taxa, falhas, enumeração e anomaly score combinados. IP ou
user-agent isolado não pode produzir atribuição.

## 05 — Rate limit

Token bucket permite burst até a capacidade e repõe por tempo. Chaves de tenant
devem ser isoladas; eventos fora de ordem precisam ser rejeitados ou definidos.

## 06 — Turnstile/MFA

Exija validação server-side, uso único, idade, hostname e action. Para admins,
prefira MFA resistente a phishing e trate enrollment, recovery e break-glass.

## 07 — Capstone

| Critério | Excelente | Insuficiente |
|---|---|---|
| escopo | limites e parada verificáveis | "ambiente de teste" genérico |
| teste Red | casos positivos/negativos reproduzíveis | volume ou improviso |
| evidência Blue | correlação e motivo da decisão | screenshots sem contexto |
| integração Purple | tuning, rollback e reteste | bloqueio sem validação |
| privacidade | minimização e retenção | coleta indiscriminada |
| risco residual | explícito, com owner | promessa de proteção total |
