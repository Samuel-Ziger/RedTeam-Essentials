# 02 — Apple Silicon, Intel e cadeia de confiança

Macs Apple Silicon integram CPU, GPU, controladores de memória e componentes de
segurança em um SoC arm64. Macs Intel usam x86_64 e podem ter chip T2. Essas
diferenças afetam boot, Recovery, virtualização, binários e diagnóstico.

## Conceitos essenciais

- **universal binary:** contém slices para mais de uma arquitetura;
- **Rosetta 2:** traduz aplicações Intel compatíveis em Apple Silicon;
- **Secure Enclave:** protege operações criptográficas e segredos vinculados;
- **secure boot:** valida componentes antes de transferir controle;
- **RecoveryOS:** ambiente confiável separado do sistema instalado.

```zsh
uname -m
sysctl -n hw.model
file /usr/bin/file
```

Memória unificada não elimina memória virtual. Tradução não torna todo software
Intel compatível, principalmente extensões e dependências de baixo nível.

## Prática

Escolha três aplicativos locais, use `file` no executável interno do bundle e
classifique-os como arm64, x86_64 ou universal. Não instale Rosetta apenas para
cumprir o exercício.
