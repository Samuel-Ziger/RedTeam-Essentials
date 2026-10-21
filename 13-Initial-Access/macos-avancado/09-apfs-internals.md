# 09 — APFS, snapshots, clones, firmlinks e SSV

APFS usa copy-on-write e organiza containers/volumes com papéis. Clones
compartilham blocos até mudança; snapshots fixam a visão lógica. Firmlinks unem
partes do volume System e Data na hierarquia apresentada.

O Signed System Volume usa uma árvore de hashes e selo para verificar conteúdo
do sistema. Atualizações preparam uma nova visão e trocam o estado de boot com
capacidade de recuperação. Não edite o sistema selado.

```zsh
diskutil apfs list
diskutil apfs listVolumeGroups
tmutil listlocalsnapshots /
```

Copy-on-write não significa "custo zero": divergência consome blocos e retenção
de snapshots afeta espaço recuperável.

## Prática

Modele o ciclo criar arquivo→clone→alterar→snapshot em diagrama. Identifique
o que protege contra erro lógico e o que ainda exige outro dispositivo.
