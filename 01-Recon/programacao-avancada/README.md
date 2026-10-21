# Engenharia de dados e APIs — do modelo à operação

> Continua diretamente o Módulo 00. A trilha parte de requisitos e termina em
> uma API local que preserva invariantes sob concorrência, retry e falhas de
> dependência. Todo dado é fictício e nenhum serviço é publicado na internet.

## Resultado da formação

Ao concluir este curso, você não apenas escreverá consultas ou endpoints. Você
será capaz de explicar e provar:

- por que um fato pertence ao PostgreSQL, ao MongoDB ou a uma projeção;
- qual invariante é protegida pelo schema, pela transação ou pela aplicação;
- qual consulta determinou cada índice e quanto ele custa nas escritas;
- o que duas transações concorrentes podem observar em cada isolamento;
- por que um retry é seguro, proibido ou condicionado por uma chave;
- como o contrato HTTP representa sucesso, validação, conflito e falha;
- como impedir lost update com precondição e compare-and-set;
- como detectar regressão por testes, planos e sinais observáveis;
- o que permanece inconsistente depois do commit e como ocorre convergência;
- como restaurar dados e reconstruir uma projeção sem improvisação.

O projeto integrador é a
[Inventory API](projetos/inventory-api/README.md): PostgreSQL como fonte de
verdade, MongoDB como histórico derivado, FastAPI na borda de aplicação, Nginx
como gateway e outbox transacional entre os dois modelos de persistência.

## Pré-requisitos verificáveis

Conclua a [programação fundamental](../../00-Fundamentos/programacao/README.md)
ou demonstre competência equivalente. Você deve conseguir:

1. escrever e testar funções com entrada inválida;
2. trabalhar com listas, mapas, objetos, exceções e arquivos;
3. usar branch, commit e diff sem perder alterações existentes;
4. decompor um request HTTP em método, alvo, cabeçalhos e corpo;
5. explicar processo, porta, timeout, JSON e código de status;
6. construir e encerrar um laboratório Docker local;
7. ler um teste que falha e formular uma hipótese antes de editar.

Se você apenas reconhece os termos, mas não consegue demonstrá-los, volte ao
Módulo 00. Este curso aumenta simultaneamente a complexidade do estado, da
concorrência e das fronteiras; uma base instável torna os sintomas enganadores.

Ferramentas principais:

```bash
python3 --version
docker --version
docker compose version
curl --version
git --version
```

Os exemplos conceituais não dependem dos links externos. PostgreSQL e MongoDB
reais entram nos laboratórios para expor comportamento que SQLite, mocks e
pseudocódigo não reproduzem.

## Modelo mental central

```text
regra de negócio
      |
      +--> invariante --> constraint / transação / compare-and-set
      |                         |
      |                         v
request HTTP --> validação --> caso de uso --> repositório --> PostgreSQL
      ^                              |                             |
      |                              +---------- outbox <----------+
      |                                             |
response + ETag <--- representação                 v
                                                MongoDB
                                                    |
                                      projeção eventual e reconstruível
```

Cada seta tem um contrato. Cada contrato possui pelo menos:

- entrada aceita e rejeitada;
- saída e efeitos observáveis;
- limite de tempo e recursos;
- comportamento sob duplicação, concorrência e cancelamento;
- dono da consistência;
- teste e evidência operacional.

Se uma regra existe apenas em um parágrafo, ela ainda não está protegida. O
curso ensina a colocá-la no componente que consegue aplicá-la de forma atômica
e verificável.

## Rota recomendada — 230 a 350 horas

A carga inclui leitura, previsão de resultados, implementação, experimentos de
falha, testes, relatório e defesa. O tempo de leitura exibido pela aplicação é
somente uma parte dessa carga.

### Etapa 1 — transformar requisitos em dados (35–50 h)

1. [Arquitetura de dados e persistência](00-arquitetura-dados.md).
2. [Modelagem relacional](01-modelagem-relacional.md).
3. [SQL: fundamentos](02-sql-fundamentos.md).
4. Execute o primeiro checkpoint descrito no
   [índice de laboratórios](laboratorios/README.md).
5. Resolva as práticas 1–12 do [caderno](CADERNO-PRATICAS.md) conforme avança.

Ao sair desta etapa, você deve produzir modelo, DDL idempotente, fixtures
sintéticas e consultas cujo resultado consegue prever antes da execução.

### Etapa 2 — concorrência e desempenho relacional (45–65 h)

1. [SQL avançado](03-sql-avancado.md).
2. [Transações e concorrência](04-transacoes-concorrencia.md).
3. [Índices e desempenho](05-indices-performance.md).
4. Execute o checkpoint de concorrência e planos.
5. Resolva as práticas 13–17 do [caderno](CADERNO-PRATICAS.md).

Ao sair, você deve reproduzir uma anomalia, explicar o bloqueio, provar
rollback e comparar plano estimado com execução real. “Ficou mais rápido” sem
dataset, plano e medição não é evidência.

### Etapa 3 — modelar documentos conscientemente (35–50 h)

1. [Modelos NoSQL e decisão de arquitetura](06-nosql-modelos.md).
2. [MongoDB em profundidade](07-mongodb.md).
3. Execute o checkpoint MongoDB.
4. Modele o mesmo domínio em relações e documentos.
5. Resolva as práticas 18–22 do [caderno](CADERNO-PRATICAS.md).

Ao sair, você deve justificar embed/reference pelos padrões de acesso,
frequência de mudança, atomicidade e crescimento — nunca pela frase “NoSQL não
tem schema”.

### Etapa 4 — publicar um contrato de dados (55–80 h)

1. [Anatomia completa de uma API](08-anatomia-api.md).
2. [Design HTTP e contratos](09-design-api-http.md).
3. [Implementação em camadas](10-implementacao-api.md).
4. [Autenticação, autorização e segurança](11-seguranca-api.md).
5. [Testes e observabilidade](12-testes-observabilidade.md).
6. [APIs e dados nas cinco linguagens](15-stacks-multilinguagem.md).
7. Estude os [clientes executáveis](exemplos/README.md) e execute o checkpoint
   de contrato.
8. Resolva as práticas 23–30 do [caderno](CADERNO-PRATICAS.md).

Ao sair, você deve conseguir alterar uma regra sem acoplar o domínio ao
framework, documentar erros previsíveis e explicar a diferença entre validar,
autenticar e autorizar.

### Etapa 5 — distribuir, diagnosticar e operar (60–105 h)

1. [Sistemas distribuídos e consistência](13-dados-distribuidos.md).
2. Use o [guia de diagnóstico](GUIA-DIAGNOSTICO.md).
3. Resolva as práticas 31–36 do [caderno](CADERNO-PRATICAS.md).
4. Estude e estenda a [Inventory API](projetos/inventory-api/README.md).
5. Entregue um dos [projetos e avaliações](14-projetos-avaliacao.md).
6. Execute o checkpoint final de falha, convergência e recuperação.

Ao sair, outra pessoa deve conseguir reproduzir sua aplicação, observar a
falha, restaurar os dados e defender as mesmas invariantes somente com o
contrato, os testes e o runbook.

## Método de estudo

Use este ciclo em cada conceito:

```text
prever -> executar -> observar -> explicar -> automatizar -> variar
```

1. **Prever:** escreva resultado, cardinalidade, lock ou status esperado.
2. **Executar:** use o menor fixture capaz de provar a hipótese.
3. **Observar:** capture linhas, plano, headers, logs ou estado persistido.
4. **Explicar:** relacione a evidência à regra, sem apenas narrar a saída.
5. **Automatizar:** converta a descoberta em teste ou validação repetível.
6. **Variar:** mude concorrência, volume, ordem ou falha e reavalie.

Mantenha um caderno de evidências por checkpoint:

```text
hipótese:
fixture e versões:
comando reproduzível:
resultado essencial:
explicação:
limitação:
teste permanente criado:
cleanup confirmado:
```

Não registre senhas, connection strings reais, tokens, dumps de terceiros ou
dados pessoais. Use os valores sintéticos do repositório.

O [caderno de práticas](CADERNO-PRATICAS.md) fornece 36 experimentos curtos. O
[guia de diagnóstico](GUIA-DIAGNOSTICO.md) organiza a investigação entre
cliente, gateway, aplicação, pool, PostgreSQL, outbox e MongoDB.

## As cinco linguagens

Python implementa o projeto integrador porque reduz ruído de framework, mas o
contrato não pertence a Python. Os
[clientes executáveis](exemplos/README.md) mostram o mesmo recurso em:

| Linguagem | Aspecto observado |
|-----------|-------------------|
| Python | contexto, exceção, tipos e cliente de alto nível |
| Java | tipos explícitos, `HttpClient` e ciclo de vida |
| C | framing HTTP, buffers, ownership e leitura parcial |
| C# | `HttpClient`, cancelamento e desserialização tipada |
| JavaScript | promises, `fetch`, abort e event loop |

Compare timeout, validação de status, limite de corpo, parse de JSON e cleanup.
Um cliente robusto precisa tratar rede parcial e resposta inválida; “funcionou
uma vez” não define seu contrato.

## Projeto integrador como fonte de evidência

A Inventory API deve ser lida em quatro perspectivas:

1. **contrato:** rotas, schemas, headers, status e Problem Details;
2. **estado:** constraints, transações, versão, idempotência e outbox;
3. **falha:** timeout, banco indisponível, retry e dependência degradada;
4. **operação:** liveness, readiness, logs, backup, restore e cleanup.

Primeiro execute a versão de referência sem editar. Depois implemente uma
mudança vertical: migration, modelo, repositório, caso de uso, contrato, teste,
telemetria e documentação. Uma mudança incompleta entre camadas é justamente o
tipo de defeito que este módulo ensina a evitar.

## Validação executável

Execute as verificações disponíveis:

```bash
bash 01-Recon/programacao-avancada/testar-curso.sh
```

O runner compila os clientes, valida scripts e Compose e executa testes da API
quando as dependências estão presentes. A saída deve separar claramente
aprovação de verificação pulada.

Para a integração com bancos reais:

```bash
cd 01-Recon/programacao-avancada/projetos/inventory-api
docker compose up --build --detach --wait
bash smoke-test.sh
docker compose down --volumes
```

O último comando remove os volumes daquele projeto. Confirme diretório e
projeto antes de executá-lo. Os containers não devem permanecer ativos após o
laboratório.

## Critério de conclusão

- [ ] Modelei um domínio e justifiquei chaves, cardinalidades e constraints.
- [ ] Escrevi consultas com join, CTE, agregação e window function.
- [ ] Demonstrei rollback, conflito e ao menos dois níveis de isolamento.
- [ ] Comparei `EXPLAIN (ANALYZE, BUFFERS)` antes e depois de um índice.
- [ ] Modelei documentos por acessos e apliquei schema validation.
- [ ] Implementei contrato HTTP com paginação e Problem Details.
- [ ] Demonstrei retry por idempotency key sem duplicar efeito.
- [ ] Impedi lost update usando `ETag` e `If-Match`.
- [ ] Testei regras isoladas e integração com bancos reais.
- [ ] Compilei e executei os clientes nas cinco linguagens.
- [ ] Expliquei e medi a janela de consistência do outbox.
- [ ] Restaurei backup em destino limpo e reconciliei a projeção.
- [ ] Entreguei runbook, ADRs e evidências sem segredos.
- [ ] Obtive no mínimo 75/100 na rubrica, sem falha crítica.

O [glossário](GLOSSARIO.md) serve para revisão rápida. As
[referências externas](REFERENCIAS.md) são complementares e ajudam a confirmar
comportamentos dependentes de versão; o curso local permanece autocontido.
