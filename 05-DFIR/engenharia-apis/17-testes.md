# 17 — Estratégia de testes para APIs

Testes devem provar invariantes no nível mais barato e conformidade nas bordas.
Uma grande quantidade de casos felizes não compensa ausência de concorrência,
autorização ou compatibilidade. O plano parte de riscos, não de percentuais.

## Objetivos

- combinar unidade, componente, integração, contrato e E2E;
- testar abuso, propriedades, concorrência e carga;
- controlar relógio, IDs e dependências;
- validar OpenAPI contra respostas reais;
- produzir matriz requisito-risco-teste-sinal.

## 1. Pirâmide orientada a risco

- **unidade:** entidade, política, cursor, canonicalização;
- **componente:** API completa com adapters locais;
- **integração:** banco, broker, IdP e parceiro compatíveis;
- **contrato:** provider e consumer concordam com mensagens;
- **E2E:** poucos fluxos críticos no ambiente controlado;
- **propriedade/fuzz:** invariantes sob entradas geradas;
- **concorrência:** interleavings e compare-and-set;
- **carga/resiliência:** cauda, saturação e recuperação;
- **abuso:** autorização, limites e fluxo de negócio.

Teste unitário rápido localiza regra; teste de componente verifica wiring; E2E
captura integração real, mas é lento e frágil. Nenhum substitui todos.

## 2. Casos mínimos por operação

Além do sucesso:

- corpo ausente, tipo errado, extra e grande;
- Content-Type/Accept incompatíveis;
- identidade ausente, expirada e audiência errada;
- papel insuficiente, objeto de outro tenant e propriedade proibida;
- estado/transição inválida;
- ETag antiga e corrida;
- mesma idempotency key com corpo igual/diferente;
- cursor adulterado, expirado e de outro filtro;
- dependência lenta, resposta inválida e indisponível;
- request ID presente em todos os resultados.

Use tabela de decisão para não esquecer combinações relevantes.

## 3. Determinismo

Injete Clock, IdGenerator e adapters. Cada teste declara dados e não depende da
ordem. Limpe banco por transação/schema isolado. Não use sleep para esperar
evento; consulte condição com prazo ou controle scheduler.

Fixtures pequenas mostram intenção. Factories com defaults ocultos podem criar
testes que passam por atributo não percebido.

## 4. Contrato e drift

Valide:

- OpenAPI é sintaticamente válido;
- exemplos seguem schemas;
- caminhos, métodos, status, media types e headers implementados coincidem;
- response real valida contra schema;
- diff breaking falha no pull request;
- SDK antigo roda contra provider novo.

Consumer-driven contracts capturam expectativas reais, mas podem fragmentar o
contrato se cada consumidor dita comportamento conflitante. Provider mantém
governança e fonte canônica.

## 5. Propriedades e fuzz

Exemplos cobrem casos conhecidos; propriedades cobrem espaço:

- decode(encode(cursor)) preserva posição;
- qualquer cursor alterado é rejeitado;
- normalização é idempotente;
- repetir comando com chave igual não cria novo item;
- autorização nunca atravessa tenant;
- version sempre cresce em escrita aceita.

Geradores precisam de limites para não testar apenas inputs irreais. Preserve
seed do caso que falhou e converta regressão importante em exemplo permanente.

## 6. Concorrência e falha injetada

Use barreiras para controlar interleaving:

~~~text
T1 lê v1
T2 lê v1
T1 grava v2
T2 tenta gravar v2 -> deve falhar
~~~

Injete falha antes/depois do commit, publish, resposta e checkpoint. Verifique
estado real e evidência, não só exceção. Teste crash de relay de outbox após
publish e deduplicação do consumidor.

## 7. Segurança e carga

Teste localmente controles de abuso; não faça scan não autorizado. Propriedade
de isolamento é mais valiosa que listar payloads ofensivos. Verifique que erros e
logs não ecoam segredos.

Teste de carga tem modelo, baseline, SLO e critério de parada. Compare versões e
observe saturação. Uma API rápida em caso feliz pode colapsar após erro de
dependência e retries.

## 8. Matriz de rastreabilidade

| Requisito/risco | Teste | Nível | Sinal em produção |
|---|---|---|---|
| tenant isolado | ID de B como A | componente | denial reason |
| no lost update | duas ETags | integração | 412 rate |
| webhook deduplica | mesmo event ID | componente | duplicate count |
| p99 < 300 ms | workload | carga | histogram |

Se não há teste nem sinal, a garantia desaparece silenciosamente.

## Falhas comuns

| Falha | Consequência | Correção |
|---|---|---|
| mock do framework | testa implementação | caso de uso/adapter |
| só happy path | regressão de controle | matriz negativa |
| sleep em teste | flakiness | clock/barreira |
| spec validada isolada | drift continua | resposta real |
| cobertura como meta única | risco crítico ausente | rastreabilidade |

## Exercícios

### Nível 1 — matriz

Crie casos mínimos de uma operação. **Aceite:** formato, identidade, objeto,
estado, duplicidade e dependência aparecem.

### Nível 2 — propriedades

Implemente cinco propriedades de cursor/idempotência. **Aceite:** seed é
reproduzível e caso reduzido vira regressão.

### Nível 3 — falhas de commit

Injete falha em quatro pontos do fluxo. **Aceite:** estado, resposta, outbox e
retry permanecem coerentes.

## Checklist

- [ ] Riscos críticos têm teste no nível adequado.
- [ ] Relógio, IDs e concorrência são controláveis.
- [ ] Respostas reais validam contra contrato.
- [ ] Há testes negativos entre tenants.
- [ ] Falhas antes/depois do commit foram injetadas.
- [ ] Cada garantia crítica possui sinal em produção.
