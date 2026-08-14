# 23 - Threat intelligence e adversary emulation

> Converter inteligência em hipóteses testáveis, sem copiar malware, infraestrutura
> de ameaça ou procedimentos destrutivos.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Red/Purple Team, CTI e detection engineering avançados. |
| Pré-requisitos | Módulos 05, 09, 15 e 20; MITRE ATT&CK. |
| Tempo estimado | 8 horas de planejamento e 6 horas de microemulação. |
| Ambiente | Fixtures, Atomic/Caldera autorizado ou lab descartável. |
| Evidência final | Intelligence requirement, plano, execução e debrief. |
| Critério de conclusão | Testar hipótese ligada a objetivo, não só técnica. |

## Ciclo

1. **Direção:** defina pergunta, crown jewel e decisão que o teste apoiará.
2. **Coleta:** priorize fontes primárias, data do comportamento e confiança.
3. **Análise:** separe fato, avaliação e lacuna; evite atribuição por ferramenta.
4. **Planejamento:** escolha comportamento seguro, precondição e success criteria.
5. **Emulação:** use canários/fixtures e logging integral do operador.
6. **Debrief:** compare prevenção, observação, detecção e resposta.

## Plano mínimo

| Campo | Exemplo sintético |
|-------|-------------------|
| Objetivo | Validar detecção de concessão IAM administrativa. |
| Hipótese | Audit log contém ator, alvo, role e sucesso. |
| Técnica | Account Manipulation, conforme layer revisado. |
| Execução | Fixture AWS/Azure/GCP do módulo 08. |
| Positivo | Concessão administrativa gera alerta. |
| Negativo | Leitura legítima não gera alerta. |
| Parada | Qualquer credencial/API real detectada. |
| Cleanup | Remover somente resultados derivados. |

## Regras de qualidade

- ATT&CK descreve comportamento, não comprova atribuição.
- Uma técnica executada sem objetivo não mede risco operacional.
- Emulação deve registrar desvios do plano e ações do operador.
- Não baixe amostras, use IoCs ativos ou replique infraestrutura criminosa.

## Próximo passo

Execute a [microemulação Purple Team](../docs/PURPLE-TEAM-MICRO-EMULATION.md),
adicione um intelligence requirement e registre confiança/limitações no debrief.

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [USANDO MITRE ATT&CK - TUTORIAL COMPLETO!](https://www.youtube.com/watch?v=1mf3De-UZkA) — **Gustavo Bessa**.
2. [O que é o MITRE ATT&CK? TTPs & A Pirâmide da Dor - Parte 1/3](https://www.youtube.com/watch?v=TYlx5JSLC-s) — **Flávio Costa - Segurança Descomplicada**.
3. [MITRE ATT&CK® Framework, Com o Prof. Thiago Cunha](https://www.youtube.com/watch?v=BKNNlqxbiS4) — **Academia de Forense Digital**.
4. [Cyber Kill Chain e MITRE ATT&CK na Prática: Como Usar no Dia a Dia](https://www.youtube.com/watch?v=DCzgq9SYte4) — **SecDay**.
5. [Cyber Threat Intelligence e Threat Hunting: O que Aprendi em 10 Dias?](https://www.youtube.com/watch?v=TV6d17bfO1k) — **Kraken Academy**.
