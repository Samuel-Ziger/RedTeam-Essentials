# 03 — Boot, Recovery, instalação e atualização

O boot confiável verifica uma cadeia que termina no sistema selado. O volume de
sistema e o volume de dados formam um grupo APFS apresentado como uma única
hierarquia. RecoveryOS fornece Utilitário de Disco, reinstalação e opções de
recuperação sem depender do sistema principal.

## Antes de instalar

- confirme compatibilidade oficial do modelo;
- teste o backup e conheça credenciais/chaves de recuperação;
- registre FileVault, espaço livre e aplicativos críticos;
- conecte energia estável;
- diferencie reinstalar, apagar e restaurar.

Em Apple Silicon, mantenha o botão de energia para opções de inicialização. Em
Intel, combinações de teclas variam. Consulte o guia do modelo; não improvise
alterações na política de boot.

```zsh
softwareupdate --history
diskutil apfs listVolumeGroups
```

Os comandos acima observam estado local. Busca e download de updates dependem
de rede e ficam fora desta etapa.

## Prática

Escreva um runbook com critérios para continuar, abortar e recuperar uma
atualização. Faça walkthrough; não apague o Mac do dia a dia.
