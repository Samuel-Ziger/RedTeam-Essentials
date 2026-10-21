# 18 — Configuration profiles e payloads

Um perfil legado `.mobileconfig` é um plist com payload raiz e payloads internos.
Identifiers e UUIDs devem ser únicos; escopo user/device e canal determinam onde
a configuração vale. Assinatura protege procedência e integridade.

```zsh
plutil -lint perfil.mobileconfig
profiles show -type configuration
```

Não edite perfis exportados de produção: podem conter certificados, endpoints,
identificadores e segredos. O `ProfileAudit.py` do curso usa fixture inerte e
valida estrutura, duplicidade e metadados sem instalar.

Payload conhecido não implica chave suportada na versão alvo. Consulte a
referência e modele `availability`, canal e comportamento de remoção.

## Prática

Audite a fixture, introduza UUID duplicado e payload sem identifier, execute os
testes e corrija o documento. Não use `profiles install`.
