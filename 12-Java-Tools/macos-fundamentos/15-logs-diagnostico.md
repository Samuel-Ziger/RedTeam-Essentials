# 15 — Unified Log, relatórios e diagnóstico

Unified Logging armazena mensagens estruturadas por processo, subsystem,
category, nível e tempo. Dados marcados privados podem ser ocultados. Console é
a interface gráfica; `log` permite consultas reproduzíveis.

```zsh
log show --last 5m --style compact --predicate 'process == "Finder"'
log show --last 5m --info --predicate 'eventType == logEvent'
```

Comece por intervalo curto e predicado seletivo. `log collect` gera um arquivo
amplo que pode conter dados sensíveis; não o compartilhe sem minimização.
Relatórios de crash e spin ficam disponíveis no Console e em diretórios de
DiagnosticReports, sujeitos a versão e escopo.

## Diagnóstico em camadas

Reproduza, marque horário, confira processo/recursos, filtre logs, compare uma
execução saudável e formule a causa. Reiniciar pode limpar o sintoma e a prova.

## Prática

Abra e feche TextEdit em uma janela conhecida, consulte apenas esse intervalo e
produza uma linha do tempo sanitizada com hipótese e limitações.
