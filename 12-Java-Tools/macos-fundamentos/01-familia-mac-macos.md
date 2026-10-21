# 01 — Família Mac, macOS e suporte

Mac é o hardware; macOS é o sistema operacional. Modelo, ano, arquitetura,
memória e armazenamento determinam quais versões e recursos podem ser usados.
Nomes comerciais de versão ajudam pessoas; número de versão e build ajudam a
reproduzir diagnósticos.

## Escolha responsável

Considere compatibilidade de hardware e aplicativos, atualizações de segurança,
capacidade de backup e custo de recuperação. Não presuma que "o Mac mais novo"
é o requisito: o curso aceita qualquer versão ainda suportada que ofereça as
ferramentas do capítulo.

```zsh
sw_vers -productVersion
sw_vers -buildVersion
uname -m
```

Atualização de ponto corrige e evolui uma linha; upgrade muda a versão principal.
Leia notas de versão e verifique compatibilidade, espaço livre e backup antes de
ambos. Em empresa, aplique anéis de teste; isso será aprofundado no módulo 13.

## Prática

Produza uma ficha sem serial: arquitetura, versão, build, memória, espaço livre,
aplicativos essenciais e caminho de recuperação. Explique por que cada campo é
necessário para uma decisão de upgrade.
