# 09 — Aplicativos, bundles, pacotes e procedência

Um `.app` é um bundle com executável, recursos e `Info.plist`. Imagens `.dmg`
transportam arquivos; pacotes `.pkg` executam uma instalação declarada e podem
conter scripts. Extensão visual não prova o tipo real.

```zsh
plutil -p /Applications/TextEdit.app/Contents/Info.plist
codesign --display --verbose=4 /Applications/TextEdit.app
spctl --assess --type execute --verbose=4 /Applications/TextEdit.app
pkgutil --pkgs
```

Antes de instalar, confirme origem oficial, assinatura, notarização, hash
quando publicado, permissões solicitadas, atualizador e desinstalação. Uma
assinatura identifica e protege integridade; não garante qualidade ou intenção.

Evite instaladores repacotados e comandos `curl | sh`. O estudo de Gatekeeper,
quarentena e notarização continua nos módulos 12 e 13.

## Prática

Escolha um app nativo, localize executável e `Info.plist`, registre bundle ID e
avalie assinatura sem modificar o bundle.
