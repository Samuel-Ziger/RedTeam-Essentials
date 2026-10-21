# 04 — Processos, threads e IPC local

O `fork`/`exec` Unix convive com launch services, XPC e primitivas Mach. XPC
estrutura comunicação entre componentes e pode impor identidades/entitlements;
pipe, sinal, shared memory e arquivo atendem outros contratos.

## Perguntas de projeto

- quem cria e supervisiona o processo?
- qual UID, grupos, sandbox e assinatura ele possui?
- qual protocolo e esquema de mensagem são aceitos?
- como autentica o peer?
- o que ocorre em timeout, crash ou mensagem inválida?

Não confunda processo pai observado com autoridade de segurança. Services e XPC
podem ter ciclo de vida mediado por `launchd`.

```zsh
ps -axo pid,ppid,uid,gid,state,etime,command
launchctl print "gui/$(id -u)"
```

## Prática

Desenhe processos e canais de um app próprio simples. Marque fronteiras de
confiança, formatos e falhas sem inspecionar IPC de terceiros.
