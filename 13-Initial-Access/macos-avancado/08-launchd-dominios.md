# 08 — `launchd` e bootstrap domains

`launchd` mantém namespaces de serviços e supervisiona jobs. Domínios `system`,
`user/<uid>`, `login/<asid>` e `gui/<uid>` representam contextos diferentes.
Um Label deve ser estável; `ProgramArguments` evita interpretação por shell.

```zsh
launchctl print system
launchctl print "gui/$(id -u)"
plutil -lint job.plist
```

Analise `RunAtLoad`, `KeepAlive`, gatilhos, throttling, working directory,
stdout/stderr, umask e identidade. Reinício infinito costuma ser sintoma de
contrato errado ou dependência ausente.

Jobs empresariais devem ter owner, pacote de instalação, versão, mecanismo de
upgrade e remoção. Presença em LaunchAgents não é automaticamente maliciosa.

## Prática

Modele um job de fixture que grava heartbeat temporário, mas apenas valide o
plist e faça tabletop de ciclo de vida; não o instale persistentemente.
