# 12 — Preferences, `defaults` e property lists

Property lists representam strings, números, booleanos, datas, dados, arrays e
dicionários em XML ou binário. O sistema de Preferences adiciona cache e escopo;
editar o arquivo por trás dele enquanto o processo roda pode perder mudanças.

```zsh
defaults read com.apple.finder
plutil -lint arquivo.plist
plutil -p arquivo.plist
```

`defaults` não é um editor universal de todo plist. Antes de escrever, confirme
domínio, chave, tipo, processo consumidor e valor anterior. Preferências
gerenciadas por organização podem ter precedência sobre valores locais.

## Procedimento seguro

1. Exporte ou copie a fixture.
2. Valide sua sintaxe.
3. Altere uma chave documentada.
4. Releia com ferramenta independente.
5. Teste comportamento e restaure.

## Prática

Crie um plist de fixture com dicionário e array, converta entre XML e binário,
valide e compare o modelo lógico. Não edite preferências globais.
