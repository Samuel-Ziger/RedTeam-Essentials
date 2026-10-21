# Automação profissional e engenharia de ferramentas

Este curso ensina a transformar processos repetitivos em ferramentas seguras,
reproduzíveis, retomáveis e operáveis. Automatizar não é juntar comandos: é definir
entrada, identidade, efeitos, limites, idempotência, evidência e recuperação.

Sistemas Operacionais e redes permanecem fora do escopo. Filesystem, processos,
HTTP e agendamento aparecem somente como contratos usados pela aplicação; kernel,
administração de servidores e infraestrutura serão estudados em módulos próprios.

## Contrato da formação

| Campo | Definição |
|---|---|
| Público | Quem concluiu os módulos 00–03 |
| Carga estimada | 220 a 320 horas |
| Linguagens | Python, Java, C17, C# e JavaScript |
| Capítulos | 15, da decisão à operação |
| Práticas | 30 exercícios N1/N2/N3 |
| Laboratórios | 5 entregas cumulativas |
| Projeto de referência | FileFlow: cópia local segura e auditável |
| Evidência final | Artifact, testes, manifesto, runbook e game day |
| Conclusão | 75% na rubrica, sem gate essencial zerado |

## Competências

Ao concluir, você conseguirá:

- decidir o que automatizar e qual autonomia conceder;
- projetar plan/apply, dry-run fiel e idempotência;
- manipular arquivos sem traversal ou sobrescrita silenciosa;
- construir pipelines com schema, streaming e reconciliação;
- integrar HTTP e webhooks com timeout, limite e autenticação;
- operar jobs, leases, checkpoints e janelas lógicas;
- controlar retry, jitter, rate limit, filas e backpressure;
- aplicar concorrência limitada e cancelamento cooperativo;
- automatizar navegador e documentos sem burlar controles;
- proteger segredos, permissões, dados e supply chain;
- projetar logs, métricas, traces, auditoria, alertas e runbooks;
- testar falhas antes/depois do commit e distribuir artifacts verificáveis.

## Modelo mental

~~~text
processo compreendido
  -> contrato e limites
  -> plano imutável
  -> aprovação
  -> efeito condicionado
  -> confirmação
  -> evidência reconciliada
  -> retomada, suporte e evolução
~~~

O mesmo ciclo aparece em arquivos, APIs, jobs e CI. A tecnologia muda; os
invariantes permanecem.

## Rota recomendada

### Etapa 1 — Decidir e controlar efeitos

1. [O que automatizar](00-o-que-automatizar.md)
2. [Contratos, idempotência e dry-run](01-contratos-idempotencia-dry-run.md)
3. [Arquivos e publicação segura](02-arquivos-caminhos-seguros.md)
4. [Contrato comum nas cinco linguagens](exemplos/README.md)
5. [Laboratório 01](laboratorios/lab-01-contrato-plan-apply.md)

**Gate:** provar que dry-run não muta, apply revalida e conflito não sobrescreve.

### Etapa 2 — Dados, integrações e retomada

6. [Pipelines de dados](03-pipelines-dados.md)
7. [Integrações HTTP e webhooks](04-integracoes-http-webhooks.md)
8. [Jobs, agendamento e checkpoints](05-jobs-agendamento-checkpoints.md)
9. [Laboratório 02](laboratorios/lab-02-pipeline-job-checkpoint.md)

**Gate:** falhar antes/depois do commit e retomar sem perder ou duplicar.

### Etapa 3 — Carga, concorrência e documentos

10. [Retry, backoff e rate limit](06-retry-backoff-rate-limit.md)
11. [Lotes e concorrência](07-lotes-paralelismo.md)
12. [Navegador e documentos](08-navegador-documentos.md)
13. [Laboratório 03](laboratorios/lab-03-resiliencia-concorrencia-documentos.md)

**Gate:** demonstrar limites de fila/workers, cancelamento e relatório seguro.

### Etapa 4 — Confiança e entrega

14. [Segurança, segredos e supply chain](09-seguranca-segredos.md)
15. [Observabilidade e auditoria](10-observabilidade-auditoria.md)
16. [Testes de automação](11-testes-automacao.md)
17. [CI/CD e orquestração](12-cicd-orquestracao.md)
18. [Guia de diagnóstico](GUIA-DIAGNOSTICO.md)
19. [Laboratório 04](laboratorios/lab-04-seguranca-observabilidade-ci.md)

**Gate:** matriz risco-controle-teste, canário ausente e artifact rastreável.

### Etapa 5 — Operação e capstone

20. [Distribuição e operação](13-distribuicao-operacao.md)
21. [Caderno de 30 práticas](CADERNO-PRATICAS.md)
22. [Projeto e avaliação](14-projetos-avaliacao.md)
23. [Projeto FileFlow](projetos/fileflow/README.md)
24. [Laboratório 05](laboratorios/lab-05-capstone-fileflow.md)

**Gate:** outra pessoa instala, aplica, repete, diagnostica, recupera e remove.

## Como estudar

Para cada capítulo:

1. declare os invariantes com suas palavras;
2. execute o exemplo e um caso inválido;
3. conclua pelo menos uma prática N1 e uma N2;
4. injete uma falha e preserve a evidência;
5. compare o observado com o contrato;
6. consulte respostas somente após a tentativa;
7. registre a decisão importante em ADR.

## Código executável

As cinco linguagens implementam o mesmo batch-plan: validação, normalização,
deduplicação, ordem determinística, texto/JSON e códigos de processo.

O [FileFlow](projetos/fileflow/README.md) aplica os conceitos a arquivos com plano,
hashes, dry-run, colisões e audit JSONL.

~~~bash
bash 04-Automation/automacao-profissional/testar-curso.sh
~~~

O script executa Python, Java, C17, JavaScript, C# quando .NET 10+ estiver
disponível e Ruff quando instalado. CI instala as toolchains obrigatórias.

## Materiais de apoio

- [Caderno de práticas](CADERNO-PRATICAS.md)
- [Guia de diagnóstico](GUIA-DIAGNOSTICO.md)
- [Laboratórios](laboratorios/README.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Glossário](GLOSSARIO.md)
- [Referências](REFERENCIAS.md)

## Escopo e ética

Use somente dados sintéticos, serviços próprios, sandboxes oficiais e integrações
autorizadas. Automação de navegador não contorna CAPTCHA, autenticação ou rate
limit. Ferramentas ofensivas e de reconhecimento pertencem aos módulos avançados
27+ e obedecem ao [uso ético](../../ETHICAL-USE.md).

