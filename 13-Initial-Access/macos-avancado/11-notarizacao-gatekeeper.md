# 11 — Notarização, Gatekeeper e quarentena

Para distribuição fora da App Store, Developer ID identifica o publicador e o
serviço notarial analisa artefato e assinatura. O ticket pode ser consultado ou
stapled. Gatekeeper avalia procedência e política no primeiro uso relevante.

Fluxo moderno: build reprodutível, assinatura com Hardened Runtime, pacote,
`notarytool`, análise do log, staple e avaliação final. Credenciais de Developer
ID não entram em exemplos, fixtures ou repositório.

```zsh
xattr -p com.apple.quarantine arquivo
spctl --assess --type execute --verbose=4 Aplicativo.app
stapler validate Aplicativo.app
```

Quarentena registra procedência para consumidores participantes. Remover xattr
ou desligar avaliação não corrige assinatura, notarização ou confiança.

## Prática

Analise um log notarial sintético: classifique erro de certificado, timestamp,
Hardened Runtime e entitlement. Não envie artefatos ao serviço.
