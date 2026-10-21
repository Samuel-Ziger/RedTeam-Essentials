# 15 — Unified Logging, privacidade e signposts

O sistema unificado centraliza mensagens e signposts. `subsystem` separa o
produto; `category` organiza o tema; nível expressa finalidade. Interpolações
podem ser privadas por padrão para reduzir vazamento.

```zsh
log show --last 5m --style json --predicate 'subsystem == "com.example.rte"'
log stream --style compact --predicate 'process == "RteFixture"'
```

`log stream` é observação em tempo real e precisa de limite operacional.
`log show` consulta persistência conforme retenção. `log collect` é amplo e
sensível. Signposts marcam intervalos para Instruments sem imprimir segredos.

## Prática

Desenhe esquema de logging para um updater: correlação aleatória, fases,
duração, resultado e erro categorizado. Exclua nomes, tokens e documentos.
