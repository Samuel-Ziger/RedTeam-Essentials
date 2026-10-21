# 06 — APFS, containers, volumes, clones e snapshots

APFS separa o dispositivo físico, o esquema de partições, o container e seus
volumes. Volumes do mesmo container compartilham espaço; quota limita máximo e
reserva garante mínimo. Um snapshot registra um ponto no tempo do volume.

## Conceitos

- clone compartilha blocos até ocorrer escrita;
- snapshot não substitui cópia em outro dispositivo;
- purgeable e livre não são idênticos;
- System/Data são apresentados por firmlinks como uma hierarquia coerente;
- erro lógico e falha física exigem respostas diferentes.

```zsh
diskutil list
diskutil apfs list
df -h
tmutil listlocalsnapshots /
```

Não redimensione, apague ou repare o disco de trabalho durante a primeira
passagem. Use uma imagem ou disco descartável e tenha uma cópia fora dele.

## Prática

Desenhe a topologia exibida por `diskutil` removendo nomes e identificadores.
Explique onde uma falha destruiria todas as cópias e proponha separação real.
