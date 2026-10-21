# 10 — Suites, grupos e negociação

Em TLS 1.3, suite escolhe AEAD e hash; grupos de acordo e algoritmos de assinatura
são negociados separadamente. Política deve considerar clientes suportados,
hardware, compliance e prazo de migração, sem ordenar opções apenas pelo nome.

Desative alternativas fora da allowlist e observe o que foi realmente negociado.
Fallback de versão precisa de mecanismos próprios do protocolo; tentar novamente
com opção fraca após erro cria downgrade. Alterações passam por canário e matriz
de compatibilidade.

## Prática

Crie política atual, exceção temporária com dono e métrica que prova sua remoção.
