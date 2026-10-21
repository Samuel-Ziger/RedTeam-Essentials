# Módulo 01 — dados, bancos de dados e APIs avançadas

> A ponte entre saber programar e construir um serviço que preserva dados,
> concorrência e contratos sob falhas reais.

> **Separação curricular:** reconhecimento e OSINT foram realocados para o
> [módulo 29](../29-Reconhecimento-OSINT/README.md), e o laboratório Web/AppSec
> para o [módulo 30](../30-Web-API-AppSec/README.md). Este módulo contém somente
> dados, bancos de dados e APIs.

## Papel na formação

O Módulo 00 termina com uma aplicação local completa. O Módulo 01 pergunta o
que acontece quando o estado deixa de caber em memória, dois clientes alteram o
mesmo recurso, uma consulta degrada, uma resposta se perde ou dois bancos
precisam convergir.

Aqui, banco não é apenas lugar para “salvar JSON” e API não é apenas uma rota.
Você aprenderá a transformar regras em invariantes verificáveis no schema, em
transações, no contrato HTTP, nos testes e na telemetria.

O foco deste módulo é a fronteira **dados ↔ aplicação ↔ API**. A especialização
exclusiva em estilos, governança e operação de APIs continua no
[Módulo 05](../05-DFIR/engenharia-apis/README.md).

| Neste Módulo 01 | No Módulo 05 |
|------------------|---------------|
| Aplica HTTP a uma API orientada a dados e invariantes. | Compara REST, webhooks, eventos, GraphQL, gRPC e streaming. |
| Liga idempotência, ETag e erros à transação e ao estado persistido. | Aprofunda contrato, compatibilidade, segurança e resiliência por estilo. |
| Usa OpenAPI, testes e telemetria para provar o projeto integrador. | Trabalha contract-first, SDKs, SLOs, developer experience e governança. |
| Entrega uma mudança vertical na Inventory API. | Projeta e governa um ecossistema de APIs. |

Assim, a repetição de vocabulário é deliberada: aqui ele protege dados; no
Módulo 05, torna-se o objeto principal de engenharia.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Quem concluiu programação fundamental e quer projetar sistemas orientados a dados. |
| Pré-requisitos | [Módulo 00](../00-Fundamentos/README.md) concluído ou competência equivalente demonstrável. |
| Tempo estimado | 230–350 horas, incluindo leitura, implementação, experimentos, diagnóstico e projeto. |
| Ambiente | Host local e Docker Compose, somente com dados sintéticos. |
| Projeto integrador | Inventory API com PostgreSQL, MongoDB, FastAPI, Nginx e outbox transacional. |
| Evidência final | Contrato, schemas, testes, planos, telemetria, backup/restore, runbook e defesa técnica. |
| Critério de conclusão | Cinco labs comprovados, projeto reproduzível e nota mínima 75/100 sem falha crítica. |
| Fora do escopo | Exploração de sistemas, coleta em terceiros, rede avançada e implantação pública. |

## O que você dominará

Ao concluir, você conseguirá:

- partir de requisitos e produzir modelo conceitual, lógico e físico;
- escolher chaves, cardinalidades, normalização, constraints e migrations;
- escrever e explicar SQL com joins, CTEs, subconsultas e window functions;
- prever anomalias concorrentes e escolher isolamento, lock ou compare-and-set;
- ler `EXPLAIN (ANALYZE, BUFFERS)` sem confundir estimativa com execução;
- justificar banco relacional, documento, chave-valor, colunar ou grafo pelos
  acessos e invariantes, não por moda;
- modelar MongoDB com validação, índices e aggregation pipelines;
- projetar recursos HTTP, erros, paginação, cache, idempotência e concorrência;
- separar transporte, caso de uso, domínio, repositório e driver;
- consumir o mesmo contrato em Python, Java, C, C# e JavaScript;
- testar regra, contrato, integração, concorrência e comportamento de falha;
- correlacionar request, query e evento por logs, métricas e traces;
- explicar consistência eventual e implementar o padrão transactional outbox;
- operar o laboratório com health/readiness, backup, restore e cleanup seguro.

## Arquitetura de aprendizagem

```text
requisito
   |
   v
modelo e invariantes ---> schema PostgreSQL ---> transação
   |                                               |
   |                                               v
   +----------------> contrato HTTP ---> caso de uso/outbox
                                                |          |
                                                v          v
                                             resposta   MongoDB
                                                |
                                                v
                                      teste + telemetria + runbook
```

Cada etapa exige quatro perguntas:

1. qual estado válido precisa ser preservado?
2. qual componente é a fonte de verdade dessa regra?
3. como a operação falha ou concorre?
4. qual evidência permite provar o comportamento?

## Rota oficial

Siga a ordem da [formação completa](programacao-avancada/README.md). A aplicação
de estudos intercala cinco checkpoints práticos:

1. modelagem e SQL verificável;
2. transações, concorrência e planos;
3. modelagem documental e MongoDB;
4. contrato e clientes de API;
5. Inventory API, falhas e operação.

Não marque um laboratório como concluído por ter lido sua instrução. Concluir
significa executar, guardar evidência sintética e explicar por que o resultado
confirma ou rejeita sua hipótese.

## Diagnóstico de entrada

Antes de começar, confirme que você consegue, sem copiar uma solução:

- escrever função, coleção, tratamento de erro e teste automatizado;
- usar Git em branch e interpretar diff;
- explicar request, response, JSON, status HTTP e timeout;
- executar programa por terminal e investigar stack trace;
- distinguir memória do processo de persistência;
- construir e encerrar o TaskBoard do Módulo 00.

Se dois ou mais itens ainda forem incertos, retorne ao
[curso fundamental](../00-Fundamentos/programacao/README.md). O objetivo não é
decorar sintaxe, mas reduzir a quantidade de conceitos novos simultâneos.

## Ambiente seguro e reproduzível

Todos os exemplos usam produtos, livros, usuários e eventos fictícios. Os
bancos dos laboratórios não publicam portas no host; no projeto integrador,
somente o gateway liga uma porta em `127.0.0.1`.

Antes de executar:

```bash
python3 --version
docker --version
docker compose version
git status --short
```

Use diretório e projeto Compose conferidos. `docker compose down --volumes`
remove os dados daquele laboratório; comandos globais de `prune` não fazem
parte do curso.

## Como validar

Validação local disponível:

```bash
bash 01-Recon/programacao-avancada/testar-curso.sh
```

Validação completa do projeto integrador:

```bash
cd 01-Recon/programacao-avancada/projetos/inventory-api
docker compose up --build --detach --wait
bash smoke-test.sh
docker compose down --volumes
```

O primeiro comando precisa distinguir aprovação de verificação pulada. A CI
instala todas as toolchains exigidas e trata qualquer skip como falha.

## Definição de concluído

O módulo termina quando você consegue apresentar, sem depender do texto:

- o modelo e as invariantes protegidas por cada constraint;
- consultas e planos antes/depois de índices justificados;
- evidência de rollback, conflito e retry seguro;
- decisão documentada entre relação, embed e reference;
- um contrato HTTP versionado com Problem Details e precondições;
- testes unitários e integração com PostgreSQL/MongoDB reais;
- clientes funcionais nas cinco linguagens;
- falha do MongoDB seguida de convergência do outbox;
- backup restaurado em destino limpo;
- runbook que outra pessoa consegue executar.

Use a [rubrica de projetos](programacao-avancada/14-projetos-avaliacao.md). A
conclusão exige pelo menos 75/100, nenhuma invariante crítica quebrada e todas
as evidências obrigatórias reproduzíveis.

## Vídeos em português

Estes vídeos complementam a formação autocontida. Conceitos e comandos
dependentes de versão devem ser confirmados nas referências oficiais do curso.

1. [Curso completo de SQL com PostgreSQL — do zero ao avançado](https://www.youtube.com/watch?v=9cAKQWodpvM) — **Stack Mobile**.
2. [O que é um banco de dados?](https://www.youtube.com/watch?v=Ofktsne-utM) — **Curso em Vídeo**.
3. [Como criar API em Python usando FastAPI](https://www.youtube.com/watch?v=R26iojTwUv8) — **Hashtag Programação**.
4. [Curso de MongoDB fundamental](https://www.youtube.com/watch?v=x9tC0eK0GtA) — **Matheus Battisti - Hora de Codar**.
5. [Curso API REST completo](https://www.youtube.com/watch?v=5mMuX8AWxxs) — **While True**.
