# 00 — Laboratório, escopo e entregáveis

Toda infraestrutura é modelada por fixtures. O protocolo RNP/1 usa um par de
sockets local quando permitido e um fluxo fragmentado em memória em sandboxes
restritos; não abre portas nem toca a Internet. Credenciais, chaves privadas, inventário real e configurações de
produção não pertencem ao repositório.

## Entregáveis profissionais

- requisitos e critérios de aceitação;
- HLD (decisões e domínios) e LLD (endereços, interfaces e políticas);
- source of truth e inventário;
- matriz de fluxos, ameaças e controles;
- SLOs, capacidade, telemetria e runbooks;
- MOP, rollback, validação e evidência;
- plano de ciclo de vida.

O laboratório ensina uma disciplina: primeiro especificar, depois validar o
modelo, só então gerar/aplicar configuração em um ambiente autorizado.
