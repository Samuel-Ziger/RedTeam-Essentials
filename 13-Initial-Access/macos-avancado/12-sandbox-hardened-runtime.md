# 12 — App Sandbox, Hardened Runtime e entitlements

App Sandbox limita recursos conforme container e entitlements. Hardened Runtime
reforça integridade do processo e é requisito para notarização moderna. Eles são
complementares, não sinônimos.

Entitlements são capacidades assinadas. Exceções como memória executável sem
proteção, variáveis `DYLD_*` ou desativação de Library Validation ampliam risco;
use apenas quando a arquitetura exige e documente ameaça/alternativas.

```zsh
codesign --display --entitlements :- Aplicativo.app
codesign --verify --strict --verbose=4 Aplicativo.app
```

Um entitlement presente não garante autorização completa: perfil de provisão,
assinatura, TCC e política podem participar.

## Prática

Compare dois arquivos de entitlements sintéticos. Produza least-privilege diff,
owner para cada capacidade e teste que comprovaria sua necessidade.
