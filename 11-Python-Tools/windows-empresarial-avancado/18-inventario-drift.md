# 18 — Inventário, drift e compliance

Inventário responde o que existe; baseline define o desejado; drift é a
diferença; compliance aplica regra/contexto/evidência. Diferente não significa
automaticamente inseguro: pode ser exceção aprovada ou coleta incompleta.

## Schema mínimo

- asset/profile sem identificador sensível desnecessário;
- OS edition/build/lifecycle;
- hardware security capability/state;
- roles/features e software aprovados;
- security settings com source/authority;
- last assessed, collector version e completeness;
- exceptions com owner/expiry.

## Comparador do curso

`Compare-RteBaseline.ps1` recebe JSON desejado e observado, compara settings
escalares e gera `compliant`, `drift` ou `missing`. Não corrige automaticamente.

## Qualidade

Uma coleta parcial deve ser `unknown`, não compliant. Preserve versão do
collector e do schema; compare tipos, não somente texto; ordene para diffs
determinísticos.

## Exercício

Adicione setting e exceção com expiração à fixture. Gere relatório e escreva o
change plan, sem executar correção.

