# Engenharia de APIs — do protocolo à operação

Uma API profissional não é uma coleção de rotas. Ela é um compromisso
versionado entre produtores e consumidores: descreve intenção, dados, identidade,
autorização, falhas, limites, consistência, operação e evolução. Este curso ensina
a construir esse compromisso e a provar que implementação e contrato concordam.

O módulo é exclusivamente sobre APIs. HTTP, persistência e criptografia aparecem
como dependências conceituais da interface; administração de redes e sistemas
operacionais pertence aos módulos próprios. Todo exercício usa dados fictícios,
processos locais ou serviços expressamente autorizados.

## Contrato da formação

| Campo | Definição |
|---|---|
| Público | Quem concluiu os módulos 00–04 |
| Carga estimada | 300 a 440 horas |
| Capítulos | 26, do modelo mental à entrega |
| Práticas | 45 exercícios N1, N2 e N3 |
| Laboratórios | 5 entregas cumulativas |
| Linguagens comparadas | Python, Java, C17, C# e JavaScript |
| Projeto de referência | Contract Lab API |
| Padrões centrais | HTTP, RFC 9457, OpenAPI, OAuth/OIDC, AsyncAPI, GraphQL, gRPC |
| Evidência final | contrato, implementação, clientes, testes, SLO e runbook |
| Aprovação | 75/100, sem gate essencial zerado |

## Competências de saída

Ao concluir, você conseguirá:

- transformar necessidades e invariantes em contrato público;
- aplicar corretamente métodos, status, negociação, cache e precondições HTTP;
- modelar recursos, representações, coleções, erros e operações demoradas;
- escolher entre REST, RPC, eventos, webhooks, GraphQL, gRPC e streaming;
- projetar paginação estável, idempotência e concorrência otimista;
- evoluir schemas sem quebrar consumidores silenciosamente;
- separar autenticação de autorização e testar isolamento entre tenants;
- aplicar threat modeling e controles do OWASP API Security Top 10;
- manter OpenAPI como fonte verificável, não documentação ornamental;
- implementar domínio independente de framework e persistência;
- lidar com transações, outbox, duplicidade e consistência eventual;
- definir timeout, retry, rate limit, backpressure e orçamento de latência;
- operar métricas, logs, traces, SLI, SLO, alertas e runbooks;
- testar contrato, propriedades, abuso, concorrência, carga e compatibilidade;
- publicar webhooks e eventos confiáveis e consumir dependências hostis;
- produzir SDKs previsíveis e governança automatizada.

## Modelo mental

~~~text
problema e consumidores
  -> invariantes e limites
  -> contrato observável
  -> ameaça e compatibilidade
  -> implementação e dados
  -> testes de conformidade e abuso
  -> publicação e operação
  -> evolução, depreciação e retirada
~~~

Cada etapa deixa evidência. Uma interface sem owner, contrato publicado,
telemetria ou política de mudança continua sendo dívida, mesmo que responda 200.

## Rota recomendada

### Etapa 1 — contrato e semântica

1. [Mapa das APIs](00-mapa-das-apis.md)
2. [Semântica HTTP](01-http-semantica.md)
3. [Estilos e decisões](02-estilos-e-decisoes.md)
4. [Design REST](03-design-rest.md)
5. [Representações e validação](04-representacoes-validacao.md)
6. [Erros com Problem Details](05-erros-problem-details.md)
7. [Laboratório 01 — contrato HTTP](laboratorios/lab-01-contrato-http.md)

**Gate:** um consumidor consegue prever sucesso, erro e efeito de repetição sem
ler a implementação.

### Etapa 2 — evolução, identidade e segurança

8. [Coleções e paginação](06-colecoes-paginacao.md)
9. [Idempotência, concorrência e cache](07-idempotencia-cache.md)
10. [Versionamento e evolução](08-versionamento-evolucao.md)
11. [Autenticação](09-autenticacao.md)
12. [Autorização e multitenancy](10-autorizacao.md)
13. [Segurança e OWASP](11-seguranca-owasp.md)
14. [OpenAPI contract-first](12-openapi-contract-first.md)
15. [Laboratório 02 — contrato seguro](laboratorios/lab-02-contrato-seguranca.md)

**Gate:** contrato validado, isolamento entre tenants, compatibilidade analisada
e casos de abuso convertidos em testes.

### Etapa 3 — implementação, dados e operação

16. [Arquitetura de implementação](13-arquitetura-implementacao.md)
17. [Dados, transações e consistência](14-dados-consistencia.md)
18. [Resiliência e desempenho](15-resiliencia-desempenho.md)
19. [Observabilidade, SLI e SLO](16-observabilidade.md)
20. [Estratégia de testes](17-testes.md)
21. [Guia de diagnóstico](GUIA-DIAGNOSTICO.md)
22. [Laboratório 03 — serviço operável](laboratorios/lab-03-servico-operavel.md)

**Gate:** falhas antes e depois do commit têm resultado verdadeiro, telemetria
correlacionada e procedimento de recuperação.

### Etapa 4 — integrações e estilos especializados

23. [Webhooks](18-webhooks.md)
24. [APIs assíncronas](19-apis-assincronas.md)
25. [GraphQL](20-graphql.md)
26. [gRPC e Protocol Buffers](21-grpc.md)
27. [Streaming e tempo real](22-streaming-tempo-real.md)
28. [Clientes e SDKs](23-clientes-sdks.md)
29. [Developer experience e governança](24-governanca-dx.md)
30. [Exemplos nas cinco linguagens](exemplos/README.md)
31. [Laboratório 04 — integração confiável](laboratorios/lab-04-integracoes-clientes.md)

**Gate:** duplicidade, ordem, deadline, custo, backpressure, compatibilidade e
cancelamento possuem políticas explícitas e testes.

### Etapa 5 — consolidação

32. [Caderno de 45 práticas](CADERNO-PRATICAS.md)
33. [Projeto e avaliação](25-projeto-avaliacao.md)
34. [Contract Lab API](projetos/contract-lab-api/README.md)
35. [Laboratório 05 — capstone](laboratorios/lab-05-capstone-contract-lab.md)

**Gate:** outra pessoa integra, opera, diagnostica, migra e remove a API usando
somente contratos, exemplos e runbooks entregues.

## Como estudar

Em cada capítulo:

1. reescreva os invariantes sem copiar o texto;
2. execute o exemplo feliz e pelo menos dois inválidos;
3. conclua uma prática N1 e uma N2;
4. ligue requisito a teste e sinal operacional;
5. registre escolha relevante em ADR;
6. injete uma falha e preserve a evidência;
7. consulte respostas apenas depois da tentativa.

Os exercícios N3 não pedem volume de código; pedem julgamento demonstrável.
Hipótese, versão, entrada, comando, saída e conclusão fazem parte da entrega.

## Código executável

Os exemplos implementam o mesmo contrato de query em cinco linguagens. O
[Contract Lab](projetos/contract-lab-api/README.md) demonstra API local com
schema estrito, autorização sintética, paginação por cursor, Problem Details,
idempotência, ETag, eventos e testes.

~~~bash
bash 05-DFIR/engenharia-apis/testar-curso.sh
~~~

O runner informa toolchain ausente como SKIP. A integração contínua instala as
dependências obrigatórias e também verifica currículo, catálogo e contrato.

## Materiais de apoio

- [Laboratórios](laboratorios/README.md)
- [Caderno de práticas](CADERNO-PRATICAS.md)
- [Guia de diagnóstico](GUIA-DIAGNOSTICO.md)
- [Respostas orientativas](RESPOSTAS.md)
- [Glossário](GLOSSARIO.md)
- [Referências oficiais e complementares](REFERENCIAS.md)

## Limite ético

O laboratório serve para engenharia e validação defensiva. Testes de abuso ficam
restritos ao serviço local ou a alvos com autorização explícita. Reconhecimento,
exploração e operações de segurança especializadas começam nos módulos 27+ e
seguem o [guia de uso ético](../../ETHICAL-USE.md).
