# Lab 03 — APFS e plano de Recovery

## Objetivo

Ler a topologia de armazenamento e ensaiar decisões sem alterar volumes.

## Procedimento

1. Colete `diskutil list`, `diskutil apfs list` e `df -h`.
2. Remova serial, UUID e nomes pessoais da evidência.
3. Desenhe device, partition, container, volume group e Recovery.
4. Escreva condições para First Aid, reinstalação, restauração e erase.
5. Faça tabletop de update interrompido e volume de dados indisponível.

## Critério

O runbook distingue ações destrutivas, exige backup antes delas e contém um
ponto de parada. Não execute `erase`, `partition` ou `restore` neste lab.
