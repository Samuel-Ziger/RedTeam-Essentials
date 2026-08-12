# Guia de detecção verificável

> Padrão mínimo para ligar uma ação de laboratório à perspectiva defensiva.

## Unidade de detecção

Cada exercício de detecção deve registrar:

| Campo | Pergunta |
|-------|----------|
| Ação | O que ocorreu, em qual alvo e com qual identidade? |
| Fonte | Qual log registra a ação? Está habilitado por padrão? |
| Seleção | Quais campos identificam o comportamento? |
| Contexto | Que dado diferencia uso esperado de suspeito? |
| Teste positivo | Qual fixture deve alertar? |
| Teste negativo | Qual atividade parecida não deve alertar? |
| Resposta | Qual ação proporcional preserva evidência? |
| Mitigação | Qual controle previne ou reduz o comportamento? |

## Exemplos por domínio

### Active Directory

- **Ação:** falhas 4625 seguidas de 4624 e 4672.
- **Fontes:** Security Event Log, EDR e logs do serviço de origem.
- **Contexto:** logon ID, tipo de logon, conta de serviço, workstation e change.
- **Fixture:** [lab DFIR de autenticação](../05-DFIR/labs/README.md).

### Web e API

- **Ação:** principal A acessa objeto pertencente a B.
- **Fontes:** access log, application audit e decisão de autorização.
- **Contexto:** principal, tenant, object owner, ação e correlation ID.
- **Exercício:** [respostas orientativas Web](../07-Web-AppSec/labs/answers/README.md).

### Cloud

- **Ação:** mudança de política IAM ou acesso incomum a storage.
- **Fontes:** CloudTrail, Azure Activity/Entra sign-in ou Cloud Audit Logs.
- **Contexto:** identidade humana/workload, origem, MFA, recurso e change ticket.
- **Teste seguro:** evento sintético que representa `allow`, sem credencial real.

### Containers

- **Ação:** criação de pod privilegiado.
- **Fonte:** Kubernetes audit log e decisão do admission controller.
- **Contexto:** namespace, usuário, pipeline, securityContext e janela de mudança.
- **Fixture:** [lab Kubernetes audit](../10-Container-Sec/labs/README.md).

## Critério de aceite

Uma detecção é verificável quando possui pelo menos um evento positivo, um
evento negativo, campos de correlação, hipótese de falso positivo, resposta e
mitigação. Uma busca sem fixture ou resultado esperado é apenas uma ideia de
detecção, não um controle validado.

