# 17 — Crash reports, LLDB e diagnóstico

Crash report registra processo, versão, arquitetura, exceção, thread acionada,
imagens e stacks. Symbolication transforma endereços em funções quando binário,
UUID e dSYM correspondem.

```zsh
lldb -- ./programa-fixture
(lldb) breakpoint set --name main
(lldb) run
(lldb) thread backtrace all
```

Depure apenas código próprio. Não altere SIP, entitlements ou `get-task-allow`
de software distribuído para anexar. Em release, remova entitlement de debug e
armazene dSYMs com controle de acesso.

## Prática

Use um crash sintético com null dereference em build de laboratório. Identifique
thread, frame, entrada, causa, correção e teste de regressão; depois remova dump.
