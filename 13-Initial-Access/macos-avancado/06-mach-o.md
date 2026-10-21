# 06 — Mach-O e load commands

Mach-O descreve objetos, executáveis, dylibs, bundles e core files. O header
declara magic, CPU, tipo, número e tamanho dos load commands. Cada comando
descreve segmentos, dependências, entry point, UUID, assinatura ou metadados.

## Leitura segura

1. detecte thin/fat e endianness pelo magic;
2. valide tamanho mínimo antes de unpack;
3. valide offsets e somas contra o arquivo;
4. limite quantidade/tamanho de estruturas;
5. trate valores desconhecidos como dados, não como instrução.

```zsh
otool -hv executavel
otool -l executavel
size -m executavel
```

Segmento é unidade de mapeamento; section organiza conteúdo dentro dele. O
`LC_CODE_SIGNATURE` aponta para dados de assinatura, mas não valida confiança.

## Prática

Execute `MachoSummary.py` contra binário próprio e compare com `otool`. Depois
alimente arquivo truncado e confirme falha fechada.
