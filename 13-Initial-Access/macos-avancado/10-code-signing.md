# 10 — Assinatura de código e requirements

Code signing vincula código, recursos selecionados, entitlements e identidade.
Assinatura ad hoc sustenta integridade local, mas não uma identidade Developer
ID. `codesign --verify` verifica estrutura; `spctl` avalia política.

```zsh
codesign --display --verbose=4 binario
codesign --display --entitlements :- binario
codesign --verify --strict --verbose=4 Aplicativo.app
codesign -d -r- Aplicativo.app
```

Designated Requirement expressa a identidade esperada ao longo de atualizações.
Team ID, bundle ID e cadeia ajudam a definir confiança, mas a política deve
considerar canal de distribuição e comportamento.

Assine de dentro para fora, preserve estrutura do bundle e não use `--deep` como
substituto de compreender componentes na etapa de assinatura.

## Prática

Assine ad hoc somente os binários didáticos em diretório temporário, verifique,
altere uma cópia e observe a falha de integridade.
