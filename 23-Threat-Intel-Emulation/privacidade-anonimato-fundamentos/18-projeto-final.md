# 18 — Projeto final: plano de privacidade verificável

O projeto reúne arquitetura, comportamento e governança. Escolha um cenário
legítimo: trabalho remoto, administração de servidor próprio, pesquisa acadêmica
ou proteção de dados de uma aplicação.

## Entregáveis

1. objetivo, escopo e autorização;
2. ativos e relações sensíveis;
3. diagrama com endpoint, DNS, rede, intermediários e destino;
4. matriz de observadores e capacidades;
5. identificadores fornecidos, observados, inferidos e derivados;
6. controles de endpoint, conta, aplicação, transporte e retenção;
7. plano de testes para operação normal, falha e recuperação;
8. riscos residuais e condições que invalidam as conclusões;
9. revisão de privacidade e data de validade do documento.

## Critérios

| Critério | Evidência |
|---|---|
| Correção | cada controle está ligado a uma ameaça específica |
| Cobertura | inclui endpoints e identidade, não só endereço IP |
| Verificabilidade | há resultado esperado e forma segura de testar |
| Proporcionalidade | não coleta mais dados que o necessário |
| Honestidade | riscos residuais e premissas estão explícitos |
| Recuperação | falhas não deixam o administrador sem acesso |

## Revisão final

Execute o analisador offline e trate cada alerta. Uma boa conclusão não diz
“anônimo”; diz contra qual observador, durante qual atividade, com quais
premissas e qual confiança.

