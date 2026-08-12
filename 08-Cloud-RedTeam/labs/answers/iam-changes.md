# Respostas orientativas — mudanças IAM cloud

## Observações

- AWS: `lab-admin` anexou `AdministratorAccess` a `lab-student` com sucesso.
- Azure: `admin@lab.invalid` atribuiu a role `Owner` ao principal sintético.
- GCP: `admin@rte-lab.invalid` adicionou `roles/owner` a outro membro.

Os eventos benignos demonstram que acesso a um recurso não deve ser confundido
automaticamente com concessão de privilégio.

## Hipóteses e contexto

Uma concessão pode ser manutenção aprovada, automação ou abuso. Verifique change
ticket, MFA, dispositivo/origem, identidade humana versus workload, horário e
escopo do recurso. O alerta não prova comprometimento por si só.

## Resposta e prevenção

Preserve o evento e correlation/request ID disponível, confirme o owner atual e
revogue somente a binding/policy indevida. Depois revise atividade da identidade.
Use privilégio just-in-time, approval, MFA, SCP/management group/org policy,
separação de funções e alertas para concessões administrativas.

## Falsos positivos

Provisionamento autorizado e break-glass testado podem gerar o mesmo evento.
Não suprima permanentemente essas identidades; correlacione com janela, ticket e
duração da concessão.

