# 08 — Permissões, ACLs, flags e atributos estendidos

O resultado de acesso pode combinar owner/group/mode Unix, ACL, flags, sandbox,
TCC e proteção do sistema. Alterar apenas `chmod` não explica todas as recusas.

```zsh
ls -ldeO@ arquivo
stat -x arquivo
xattr -l arquivo
```

Bits `rwx` são avaliados para dono, grupo ou outros. Em diretório, `x` permite
atravessar; `w` permite alterar entradas. ACLs adicionam regras ordenadas. Flags
como `uchg` restringem alteração. Xattrs armazenam metadados; um deles pode
registrar quarentena de download.

Não resolva falhas com `chmod -R 777`, remoção recursiva de ACL ou `xattr -cr`.
Essas ações destroem evidência e ampliam acesso. Descubra a camada responsável.

## Prática

Em uma fixture, aplique modos `600`, `640` e `750`; preveja o acesso e teste.
Adicione um xattr didático, leia-o e remova apenas esse atributo. Não use
arquivos baixados nem dados pessoais.
