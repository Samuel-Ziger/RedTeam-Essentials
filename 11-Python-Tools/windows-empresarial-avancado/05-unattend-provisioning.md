# 05 — Unattend, configuration passes e provisioning

Answer files automatizam Windows Setup por configuration passes como
`windowsPE`, `offlineServicing`, `specialize` e `oobeSystem`. Um componente
configurado no pass errado pode ser ignorado ou falhar.

## Princípios

- gere/valide com Windows System Image Manager correspondente ao ADK;
- declare arquitetura e imagem alvo;
- minimize valores e documente defaults;
- nunca grave senha/chave/segredo no arquivo ou mídia;
- valide XML e settings contra catálogo da mesma build;
- teste OOBE, locale, disk, rollback e logs de Setup.

Provisioning packages (`.ppkg`) aplicam configurações a dispositivos existentes
ou no OOBE. Trate-os como código privilegiado: origem, assinatura, expiração,
escopo e rollback.

## Disco

Automatizar `DiskConfiguration` é destrutivo. Use seletores inequívocos e somente
VM descartável. Uma imagem genérica não deve adivinhar o disco correto.

## Exercício

Crie answer file sem credenciais para locale/nome sintético, valide estaticamente
e revise cada pass. Execução destrutiva somente em clone.

