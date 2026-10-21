# 11 — `launchd`, agentes, daemons e tarefas

`launchd` inicia e supervisiona jobs descritos por propriedades. Domínios
distinguem sistema, usuário e sessão gráfica. Um arquivo presente não prova que
o job está carregado; o estado do serviço é a evidência principal.

| Local | Uso típico |
|---|---|
| `/System/Library/LaunchDaemons` | sistema Apple protegido |
| `/Library/LaunchDaemons` | daemon de terceiros para o computador |
| `/Library/LaunchAgents` | agente de terceiros para usuários |
| `~/Library/LaunchAgents` | agente da conta atual |

```zsh
launchctl print "gui/$(id -u)"
plutil -lint exemplo.plist
```

Campos importantes incluem `Label`, `ProgramArguments`, gatilhos, ambiente,
saídas e política de reinício. `KeepAlive` mal usado causa loops e consumo.

## Prática

Leia um LaunchAgent conhecido, valide o plist e desenhe quando ele inicia,
qual identidade usa, onde registra saída e como seria removido. Não carregue
jobs persistentes neste capítulo.
