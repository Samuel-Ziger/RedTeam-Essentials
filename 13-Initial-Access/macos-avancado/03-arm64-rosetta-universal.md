# 03 — arm64, arm64e, Rosetta e universais

Apple Silicon executa arm64; partes da plataforma usam arm64e com pointer
authentication. Um fat/universal Mach-O agrega slices independentes e `lipo`
seleciona ou descreve arquiteturas. Rosetta traduz software x86_64 compatível.

```zsh
file executavel
lipo -info executavel
otool -hv executavel
```

Arquitetura do processo, arquitetura das bibliotecas e deployment target devem
ser compatíveis. Um app universal pode conter helpers com conjunto diferente.
Teste todo o bundle e seus plug-ins, não apenas o binário principal.

Pointer authentication assina ponteiros selecionados para dificultar corrupção;
não é assinatura de arquivo. Tradução e virtualização também são mecanismos
distintos.

## Prática

Use o parser do curso em fixtures thin e fat. Compare magic, endianness, CPU
type e offsets; explique por que validar limites precede ler load commands.
