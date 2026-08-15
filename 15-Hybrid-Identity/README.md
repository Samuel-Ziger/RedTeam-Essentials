# 15 - Identidade híbrida

> Relações defensivas e caminhos de risco entre Active Directory, Entra ID,
> federação e identidades de workload. Pratique somente em tenant sandbox.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes avançados de AD, cloud e IAM. |
| Pré-requisitos | Módulos 03 e 08; OAuth/OIDC básico. |
| Tempo estimado | 10 horas de leitura e 6 horas de análise offline. |
| Ambiente | Fixtures cloud do módulo 08 ou tenant descartável autorizado. |
| Evidência final | Diagrama de trust, hipótese de ataque e controles/detecções. |
| Critério de conclusão | Explicar dois caminhos híbridos sem usar credenciais reais. |

## Conteúdo essencial

1. **Identidades:** usuário sincronizado, guest, service principal, managed
   identity e workload identity possuem ciclos de vida e controles diferentes.
2. **Trust:** sincronização de hash, pass-through authentication, federação,
   application consent e credenciais de workload criam fronteiras adicionais.
3. **Privilégio:** Global Administrator, Privileged Role Administrator, owner de
   subscription e privilégios do AD não são equivalentes, mas podem formar
   caminhos compostos.
4. **Controles:** MFA resistente a phishing, Conditional Access, PIM/JIT,
   segregação de contas administrativas, revisão de consent e credenciais
   efêmeras para pipelines.
5. **Telemetria:** Entra sign-in/audit, provisioning, AD Security Logs, eventos
   do provedor cloud e logs do workload precisam de correlation IDs e relógio
   sincronizado.

## Exercício offline

Use as fixtures de [mudanças IAM cloud](../08-Cloud-RedTeam/labs/README.md) e
desenhe um grafo contendo ator, identidade de destino, role, recurso e controle.
Adicione um elo hipotético com AD, marcando-o explicitamente como hipótese.

### Perguntas

- Qual evento provaria sincronização, consent ou atribuição de role?
- Qual política bloquearia o caminho sem quebrar workloads legítimos?
- Como distinguir identidade humana de workload?
- Que credencial deve ser revogada e como preservar evidência?

## Cleanup

O exercício offline não altera tenant. Em sandbox real, remova assignments,
consents e credenciais criados, confirme em audit logs e encerre custos.


## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [SINCRONIZANDO USUÁRIOS DE DOMÍNIO LOCAL COM O AZURE AD / MICROSOFT ENTRA! Microsoft Active Directory](https://www.youtube.com/watch?v=3gqWZoi0Mg0) — **SecInfra | Matheus Azzi**.
2. [Certificação SC-900: O quê é o Microsoft Entra ID](https://www.youtube.com/watch?v=NIsbQz-Zeto) — **Wellington Agápto**.
3. [Tutorial para iniciantes do Microsoft Entra ID (Azure Active Directory)](https://www.youtube.com/watch?v=0qZzcK1mHwA) — **Microsoft Mechanics**.
4. [Gerenciamento de Identidade e Acesso no Microsoft Entra ID | AO VIVASSO MARZI #01](https://www.youtube.com/watch?v=iiwcHy4WphE) — **Denilson Marzi**.
5. [Entendendo o Microsoft Entra ID e ambientes híbridos](https://www.youtube.com/watch?v=rffL74UTpnE) — **ZineTek**.

