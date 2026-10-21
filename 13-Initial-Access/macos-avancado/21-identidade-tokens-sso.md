# 21 — Identidade, Secure Token, Bootstrap Token e Platform SSO

Conta local, Conta Apple, Managed Apple Account e identidade do IdP são objetos
distintos. Platform SSO aproxima credencial organizacional e login conforme
extensão/versão suportadas, mas o lifecycle local continua relevante.

Secure Token participa de operações criptográficas/autorização do volume.
Bootstrap Token é custodiado pelo MDM para autorizar fluxos institucionais.
FileVault recovery key exige escrow, rota de acesso e rotação controlados.

## Controles

- break-glass separado, testado e auditado;
- offboarding remove acesso sem destruir evidência ou dado devido;
- owner e validade para contas de serviço;
- autenticação forte e recuperação verificável;
- nenhum token em script, plist ou log.

## Prática

Modele joiner/mover/leaver offline e identifique transações que dependem de
MDM/IdP/rede. Crie testes de invariantes, não contas reais.
