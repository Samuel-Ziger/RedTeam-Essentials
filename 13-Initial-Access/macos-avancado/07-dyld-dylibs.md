# 07 — `dyld`, dylibs, install names e rpaths

`dyld` mapeia dependências Mach-O e resolve símbolos conforme load commands e
política. Install names podem usar `@executable_path`, `@loader_path` e
`@rpath`; cada token possui base distinta.

```zsh
otool -L executavel
dyld_info -dependents executavel
nm -gU biblioteca.dylib
```

Busca ambígua em diretório gravável cria risco. O exemplo usa uma dylib própria
ao lado do consumidor e `@loader_path`, sem procurar pelo diretório atual. Use
`RTLD_NOW | RTLD_LOCAL`, verifique cada símbolo e feche o handle.

Library Validation, Hardened Runtime e assinatura limitam combinações em apps
distribuídos. Não adicione exceções apenas para "fazer funcionar".

## Prática

Compile a dylib didática, confira install name/dependências, execute o consumidor
e prove que mover o par para outro diretório mantém a resolução local.
