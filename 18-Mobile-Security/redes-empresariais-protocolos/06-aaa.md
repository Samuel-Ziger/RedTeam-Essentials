# 06 — AAA, RADIUS, TACACS+ e administração

AAA separa autenticação, autorização e accounting. RADIUS é comum em acesso de
rede/802.1X; TACACS+ é frequente em administração de equipamentos, com controle
de comandos segundo implementação. Use versões/transporte protegido adequados e
não dependa apenas de segredo compartilhado em redes não confiáveis.

Administração deve passar por rede/VRF de gestão, bastion/PAM, MFA, RBAC,
sessões registradas conforme política e contas nominativas. Conta break-glass
fica protegida, monitorada e testada, com uso excepcional.

Planeje falha AAA: autenticação local de emergência controlada, cache limitado ou
negação conforme criticidade. Teste antes de aplicar a todos os equipamentos.

Accounting precisa de tempo sincronizado e correlação, mas deve minimizar dados
pessoais e ter retenção definida.
