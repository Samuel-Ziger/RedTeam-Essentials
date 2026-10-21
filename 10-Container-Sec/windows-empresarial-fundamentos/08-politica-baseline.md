# 08 — Política e baseline local

Política traduz risco em configuração. Baseline é conjunto versionado,
justificado, testado e monitorado. Copiar milhares de settings sem entender o
workload cria indisponibilidade e exceções permanentes.

## Fontes

- Microsoft Security Baselines/Security Compliance Toolkit;
- Windows Server security baseline/OSConfig quando aplicável;
- requisitos regulatórios interpretados pela organização;
- compatibilidade real do workload.

## Ciclo

Inventário → diferença → risco → audit/pilot → enforcement → exceção com
expiração → detecção de drift → revisão por versão.

`secpol.msc` e `gpedit.msc` alteram política local. Exporte estado antes; não
aplique templates no host principal. GPO de domínio e precedência serão
aprofundadas no módulo 11 após a base de redes/identidade.

## Evidência

Cada controle precisa de identificador, valor desejado, fonte, motivo, escopo,
teste, evento de falha, rollback, owner e data de revisão.

## Exercício

Escolha cinco controles locais, escreva uma matriz acima e simule avaliação
somente leitura no clone.

