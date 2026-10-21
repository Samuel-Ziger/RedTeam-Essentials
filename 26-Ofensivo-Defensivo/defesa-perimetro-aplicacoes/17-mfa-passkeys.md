# 17 — 2FA, WebAuthn, passkeys e recuperação

Autenticação multifator combina categorias independentes: algo que você sabe,
possui ou é. Duas senhas não são dois fatores. O controle deve proteger login,
elevação, mudança de fator e recuperação.

## Comparando opções

| Método | Característica | Risco principal |
|---|---|---|
| SMS/voz | amplo alcance | troca de SIM, interceptação e engenharia social |
| TOTP | segredo compartilhado e código curto | phishing/replay em tempo real |
| push | boa UX | fatigue e aprovação indevida |
| WebAuthn/FIDO2 | chave vinculada ao verificador | lifecycle e recuperação |
| passkey | credencial WebAuthn, possivelmente sincronizada | ecossistema e recuperação da conta |

Segundo o NIST, OTP digitado manualmente não é resistente a phishing. WebAuthn
usa binding ao nome do verificador e é o caminho preferencial para contas
administrativas e operações de alto risco.

## Enrollment e recuperação

Exija sessão recente e step-up para cadastrar/remover fator. Notifique mudanças,
permita múltiplos autenticadores, proteja códigos de recuperação e evite que o
help desk reduza toda a segurança a perguntas pessoais. Conta break-glass deve
ser rara, monitorada e testada.

## Purple Team

Red testa fluxo e lógica com contas de laboratório: enrollment sem sessão recente,
remoção de fator, reutilização de recovery code e sessão anterior à troca. Blue
correlaciona eventos e aciona resposta. Purple inclui acessibilidade, perda de
dispositivo e revogação no teste de regressão.
