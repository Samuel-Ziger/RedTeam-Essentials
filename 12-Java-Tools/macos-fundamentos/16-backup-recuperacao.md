# 16 — Time Machine, cópias e recuperação

Backup reduz perda somente quando é independente, verificável e restaurável.
Time Machine cria histórico em destino apropriado e snapshots locais podem
ajudar entre execuções. Snapshot no mesmo armazenamento não cobre falha dele.

```zsh
tmutil status
tmutil latestbackup
tmutil listlocalsnapshots /
```

RPO é quanto dado se aceita perder; RTO é quanto tempo a recuperação pode
levar. Defina ambos antes de escolher frequência e procedimento. FileVault no
Mac e criptografia do destino resolvem riscos diferentes.

## Teste de restauração

Escolha uma fixture, registre hash e permissões, apague somente a cópia de
trabalho, restaure para outro caminho e compare. Não use o documento mais
importante como primeiro teste.

## Prática

Execute o laboratório de backup do curso, calcule RPO/RTO observados e escreva
o que ocorreria se Mac e disco de backup fossem perdidos juntos.
