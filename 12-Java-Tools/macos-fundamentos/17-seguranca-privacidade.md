# 17 — Segurança e privacidade nativas

macOS combina hardware, boot verificado, SSV, SIP, assinatura, notarização,
Gatekeeper, XProtect, MRT, sandbox, TCC e FileVault. Nenhuma camada isolada é
garantia absoluta; desativar uma para "testar" muda o sistema avaliado.

```zsh
fdesetup status
csrutil status
spctl --status
profiles status -type enrollment
```

TCC decide acesso a recursos como câmera, microfone e dados protegidos. Conceda
somente ao app identificado e revise depois. FileVault protege dados em repouso;
uma sessão desbloqueada exige controles de tela e conta.

Gatekeeper avalia software obtido fora da App Store. XProtect fornece detecção
nativa atualizada pelo sistema. SIP e SSV protegem componentes mesmo diante de
processos privilegiados.

## Prática

Crie uma matriz: controle, ativo protegido, ameaça, forma de verificar e plano
de recuperação. Apenas observe; não redefina TCC nem altere política de boot.
