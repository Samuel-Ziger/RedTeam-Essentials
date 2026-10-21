# Consulta rápida

Todos os comandos abaixo são locais e de leitura, salvo indicação.

```zsh
sw_vers
uname -m
sysctl -n hw.model
pwd
ls -laOe@
stat -x arquivo
id
groups
ps -axo pid,ppid,user,%cpu,%mem,command
df -h
diskutil apfs list
tmutil status
fdesetup status
csrutil status
spctl --status
log show --last 10m --style compact --predicate 'process == "Finder"'
```

Preferências e bundles:

```zsh
defaults read com.apple.finder
plutil -lint arquivo.plist
mdls -name kMDItemContentType arquivo
codesign --display --verbose=4 /Applications/TextEdit.app
spctl --assess --type execute --verbose=4 /Applications/TextEdit.app
```

Antes de qualquer mudança: registre estado inicial, confirme backup, teste em
fixture, use caminho absoluto e escreva o procedimento de reversão.
