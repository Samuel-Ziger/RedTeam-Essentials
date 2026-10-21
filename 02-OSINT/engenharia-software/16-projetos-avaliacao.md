# 16 — Projetos, avaliação e defesa técnica

A formação termina com evidência integrada, não memorização. Você fará primeiro
uma evolução guiada do
[Dependency Planner](projetos/dependency-planner/README.md) e depois um projeto
autoral. O objetivo é demonstrar que consegue descobrir, modelar, implementar,
testar, explicar e operar uma mudança.

Um projeto maior não é automaticamente melhor. Prefira escopo pequeno com
invariantes explícitas, testes fortes, decisões honestas e execução reproduzível.

## Objetivos

Ao concluir, você deverá conseguir:

- planejar entrega por milestones verificáveis;
- evoluir uma aplicação sem romper seus limites centrais;
- produzir evidência de requisitos, arquitetura, testes e operação;
- construir um projeto autoral com risco técnico real e escopo controlado;
- avaliar trabalho por rubrica, não por impressão;
- defender decisões, limitações, falhas e próximos passos.

## Pré-requisitos e regras

Conclua os capítulos 00–15 e execute:

```bash
bash 02-OSINT/engenharia-software/testar-curso.sh
```

Ferramenta ausente pode ser registrada como limitação do ambiente; falha de uma
ferramenta instalada precisa ser corrigida. Use somente dados sintéticos,
sistemas próprios ou ambientes formalmente autorizados.

### Princípios da entrega

- todo requisito importante possui evidência;
- toda métrica possui método reproduzível;
- todo desvio/limitação é declarado;
- código de terceiros e assistência são atribuídos;
- segredos, dumps e dados pessoais não entram no repositório;
- demonstração parte de ambiente limpo;
- o avaliador não precisa adivinhar comandos.

## 1. Evidência antes de pontos

Monte uma pasta ou índice de entrega:

```text
README.md
docs/
  requirements.md
  architecture.md
  adr/
  runbook.md
  defense.md
CHANGELOG.md
LICENSE
src/
tests/
fixtures/
scripts de validação
configuração de CI
```

Não crie arquivo apenas para preencher checklist. Cada artefato responde a uma
pergunta:

| Afirmação | Evidência |
|---|---|
| “detecta ciclo” | requisito + fixture + teste + demonstração |
| “é determinístico” | propriedade sobre permutações + resultado |
| “suporta 50 mil tarefas” | protocolo, gerador, ambiente e distribuição |
| “troca JSON por CSV” | porta estável + teste de contrato dos adaptadores |
| “é operável” | runbook ensaiado + sinais + recuperação |
| “é compatível” | política, fixtures antigas/novas e changelog |

Print sem comando, cobertura isolada e vídeo sem fonte não são evidência
suficiente.

## 2. Projeto guiado: baseline do Dependency Planner

Antes de evoluir, compreenda o que existe.

### Comportamento atual

- documento JSON estrito;
- `WorkItem` imutável com duração positiva;
- IDs únicos e referências existentes;
- detecção de ciclo com caminho fechado;
- ordem topológica determinística;
- lotes lógicos com paralelismo ilimitado;
- caminho crítico e duração mínima;
- texto ou JSON;
- código 0 para sucesso e 2 para erro esperado.

### Arquitetura atual

```text
CLI/composition root
  -> PlanProject
      -> WorkItemRepository (porta)
          <- JsonWorkItemRepository
      -> build_plan
          -> WorkItem / Plan
```

`graph.py` e `domain.py` não conhecem arquivo, JSON ou terminal.

### Baseline obrigatório

1. execute a suíte;
2. execute fixtures válida e cíclica;
3. registre versão/toolchain e resultado;
4. leia todos os arquivos do projeto;
5. desenhe o fluxo de sucesso e de erro;
6. explique complexidade;
7. liste cinco riscos/lacunas;
8. confirme worktree antes de editar.

**Evidência:** relatório curto com comandos, saídas resumidas e commit de base.

## 3. Milestone 1 — requisitos e contrato

Escolha uma evolução:

- adaptador CSV;
- API HTTP local;
- exportação DOT;
- persistência SQLite/PostgreSQL;
- limite de recursos por lote;
- schema versionado.

Não combine todas. Escreva:

- problema e ator;
- dentro/fora do escopo;
- linguagem ubíqua;
- requisitos funcionais;
- atributos de qualidade mensuráveis;
- exemplos positivos, negativos e de fronteira;
- compatibilidade;
- ameaças;
- critérios de conclusão.

### Exemplo: adaptador CSV

```text
RF-CSV-01: ler cabeçalho id,title,duration,dependencies.
RN-CSV-02: dependencies usa lista delimitada cuja codificação é documentada.
QA-DET-01: CSV e JSON semanticamente equivalentes produzem o mesmo Plan.
QA-ERR-02: linha inválida informa número sem emitir plano parcial.
RES-01: arquivo máximo de 10 MiB no projeto guiado.
```

Decida escaping, encoding, linha vazia, BOM, delimitador e lista de dependências.
“Suporta CSV” sem dialeto é ambíguo.

**Gate:** revisão dos requisitos encontra entradas e saídas suficientes para
escrever testes antes da implementação.

## 4. Milestone 2 — modelo e arquitetura

Entregue:

- C4 contexto, contêiner e componentes;
- sequência de sucesso e falha;
- invariantes locais/globais;
- threat model das novas fronteiras;
- ADR com pelo menos duas alternativas;
- análise de impacto;
- plano de observabilidade.

Para adaptador:

```text
--input-format csv
  -> CsvWorkItemRepository
      -> tuple[WorkItem, ...]
          -> PlanProject (inalterado)
```

Questione se a porta atual é ideal. Se HTTP recebe itens já em memória, forçar um
repositório pode ser cerimônia; talvez um caso de uso aceite uma coleção e outro
orquestre leitura. Uma mudança de arquitetura é válida quando motivada e testada.

### Invariantes arquiteturais

- núcleo não importa adaptadores;
- DTO externo não atravessa a fronteira;
- erro externo é traduzido uma vez;
- composition root escolhe implementação;
- mesmo conjunto semântico produz o mesmo `Plan`.

**Gate:** teste de mudança demonstra que uma nova borda não exige alterar
algoritmo e domínio, salvo requisito explícito.

## 5. Milestone 3 — implementação vertical

Implemente fatias que terminam em comportamento utilizável:

1. menor caso válido;
2. validações/erros;
3. integração na CLI ou outra entrada;
4. saída/observabilidade;
5. limites e compatibilidade.

Cada fatia inclui teste e documentação necessária. Evite preparar dezenas de
abstrações antes de entregar um fluxo.

### Definition of Done por fatia

- requisito/critério ligado;
- código formatado e analisado;
- unidade/integração apropriada;
- erro e limite testados;
- nenhuma informação sensível em log;
- documentação/contrato atualizados;
- diff revisado;
- rollback conhecido.

**Gate:** comando documentado demonstra a fatia em checkout limpo.

## 6. Milestone 4 — estratégia de qualidade

Inclua:

- exemplos unitários;
- integração real da borda;
- contrato entre formatos/consumidores;
- pelo menos duas propriedades;
- duas relações metamórficas;
- campanha de mutation testing ou cinco mutações manuais;
- fuzzing seguro do parser, se houver;
- benchmark com formas de grafo;
- E2E de sucesso e erro.

Para adaptadores equivalentes:

```text
parse(JSON fixture) -> Plan A
parse(CSV fixture)  -> Plan B
assert A == B
```

Isso é teste de contrato semântico. Também teste erros próprios de cada formato.

### Orçamento

```text
local rápido: <= 10 s
PR obrigatório: <= 3 min
campanha noturna: propriedades extensas, mutação, fuzz e desempenho
```

Adapte números à infraestrutura e registre. Não reduza qualidade escondendo
flaky test.

**Gate:** ao menos cinco defeitos deliberados relevantes são detectados, e todo
teste instável foi corrigido ou isolado com dono/prazo.

## 7. Milestone 5 — colaboração e release

Entregue:

- histórico de commits por intenção;
- PR preenchido e revisão registrada;
- política de versão;
- changelog;
- guia de migração, se houver incompatibilidade;
- runbook;
- release/tag simulado ou real localmente;
- checksums quando fizer parte do requisito.

### Ensaio de operação

Escolha uma falha:

- arquivo inválido;
- regressão de performance;
- incompatibilidade de schema;
- dependência indisponível;
- configuração incorreta.

Execute o runbook, cronometre diagnóstico/recuperação e corrija passos ambíguos.

**Gate:** uma pessoa que não implementou a mudança consegue instalar, demonstrar,
diagnosticar o cenário e restaurar o serviço/fluxo.

## 8. Milestone 6 — entrega e defesa

Pacote final:

- commit/tag exato;
- instrução de ambiente limpo;
- script/comandos de validação;
- requisitos e rastreabilidade;
- arquitetura e ADRs;
- relatório de testes;
- benchmark reproduzível;
- runbook ensaiado;
- changelog/licença;
- riscos, limitações e dívida;
- roteiro de defesa.

Não edite silenciosamente após congelar a versão avaliada. Se corrigir, gere
nova versão e registre o delta.

## 9. Projeto autoral

Escolha um problema legítimo e limitado:

- agenda de salas com conflitos;
- biblioteca e empréstimos;
- coletor local de métricas;
- trilha de estudos com pré-requisitos;
- pipeline de arquivos;
- estoque/reposição;
- agendador de jobs local;
- catálogo pesquisável.

### Proposta de uma página

```markdown
# Nome
Problema e público
Resultado observável
Três invariantes
Três operações críticas
Cinco casos-limite
Integração/persistência real
Atributos de qualidade
Fora do escopo
Riscos
Milestones
```

Rejeite proposta que é apenas clone de tutorial ou CRUD sem regra. O projeto
precisa de pelo menos um risco técnico: concorrência, grafo, scheduling,
consistência, busca, migration, contrato ou desempenho.

### Requisitos mínimos

- especificação com exemplos e dez casos-limite;
- linguagem/modelo de domínio;
- duas estruturas de dados justificadas;
- análise de tempo e espaço de operação central;
- domínio separado de I/O;
- persistência ou integração real;
- interface utilizável: CLI, API ou UI;
- unidades, integração, contrato e E2E essencial;
- ao menos uma propriedade;
- CI e build reproduzível;
- README, referência, ADR, changelog, runbook e licença;
- configuração externa e segredos fora do código;
- logs sem conteúdo sensível;
- threat model;
- backup/restore se houver estado durável;
- demonstração em ambiente limpo.

### Controle de escopo

Use MoSCoW:

- **Must:** indispensável à tese do projeto;
- **Should:** alto valor, pode adiar;
- **Could:** opcional;
- **Won't now:** explicitamente fora.

Congele Must antes de polir Could. Uma UI bonita não compensa invariante central
incorreta.

## 10. Milestones do projeto autoral

| Marco | Entrega | Saída verificável |
|---|---|---|
| A — descoberta | proposta, atores, invariantes | revisão aprova problema |
| B — walking skeleton | fluxo mínimo ponta a ponta | comando retorna resultado |
| C — núcleo | regra/algoritmo | propriedades e complexidade |
| D — integração | banco/protocolo/arquivo real | teste de integração |
| E — robustez | erros, segurança, observabilidade | cenários de falha |
| F — operação | CI, release, runbook, restore | ensaio por terceiro |
| G — defesa | evidências e limitações | apresentação reproduzível |

Cada marco termina num estado executável. Walking skeleton atravessa bordas com
regra mínima; não é estrutura vazia.

### Registro semanal

```text
objetivo
hipótese
mudança
evidência
resultado inesperado
decisão
risco/próximo passo
```

Esse diário sustenta a defesa e evita reconstruir decisões por memória.

## 11. Rubrica de 100 pontos

| Dimensão | Pontos | Evidência esperada |
|---|---:|---|
| problema e requisitos | 12 | atores, exemplos, limites, rastreabilidade |
| domínio e correção | 15 | invariantes, estados e erros |
| algoritmos/estruturas | 13 | escolha, complexidade e propriedades |
| arquitetura | 15 | limites, qualidades, ADRs e threat model |
| testes e qualidade | 18 | níveis, contratos, mutação/propriedade e CI |
| dados/integração | 8 | mecanismo real, consistência e migrations |
| operação e segurança | 9 | sinais, segredos, runbook e recuperação |
| colaboração/documentação | 5 | histórico, PR, README e changelog |
| defesa e reprodutibilidade | 5 | demo limpa, limites e respostas |
| **Total** | **100** | |

### Níveis por dimensão

- **0%:** ausente ou não executável;
- **25%:** existe como afirmação, sem evidência;
- **50%:** caminho feliz funciona, limites/erros frágeis;
- **75%:** atende critérios, possui testes e trade-offs;
- **100%:** evidencia casos adversos, operação, revisão e aprendizado.

O avaliador multiplica o nível pelos pontos da dimensão, registrando justificativa
e link para evidência.

### Gates essenciais

Independentemente da soma, não conclui enquanto houver:

- projeto não executável por instrução limpa;
- violação conhecida de invariante central;
- teste obrigatório falhando;
- segredo/dado sensível versionado;
- licença de dependência incompatível ignorada;
- autoria/fonte omitida;
- operação destrutiva sem aviso;
- ausência completa de integração real;
- defesa incapaz de explicar código essencial.

Conclusão recomendada: pelo menos 75 pontos e todos os gates resolvidos. Acima de
90 exige profundidade real, não funcionalidades extras sem acabamento.

## 12. Autoavaliação e revisão cruzada

Antes da banca:

1. pontue-se com links;
2. peça avaliação cega a outra pessoa;
3. compare divergências acima de 25%;
4. execute do zero seguindo apenas README;
5. remova cache/estado implícito em ambiente descartável;
6. escolha três limitações honestas;
7. congele versão.

Revisor não deve corrigir durante a avaliação inicial. Registre onde precisou
perguntar: isso revela documentação implícita.

## 13. Defesa técnica

Formato sugerido de 30–40 minutos:

1. problema, ator e não objetivos — 4 min;
2. demonstração de sucesso e falha — 6 min;
3. domínio/algoritmo/complexidade — 6 min;
4. arquitetura e alternativas — 6 min;
5. testes/evidência — 5 min;
6. operação/segurança — 4 min;
7. limitações/próximos passos — 3 min;
8. perguntas.

A demo deve ser curta e reproduzível. Tenha fixture válida e inválida; não
dependa de internet quando o produto é local.

### Perguntas obrigatórias

1. Qual invariante mais influenciou o design?
2. O que uma linha/objeto representa?
3. Qual operação domina tempo e memória?
4. Qual alternativa foi rejeitada e por quê?
5. Que mudança atravessaria mais limites?
6. O que acontece sob timeout após efeito?
7. Onde há consistência forte e eventual?
8. Qual teste encontrou defeito real?
9. Qual mutante sobreviveu e por quê?
10. Como o sistema falha com entrada grande/malformada?
11. Como observar, mitigar, restaurar e reverter?
12. O que quebra com 100 vezes a carga?
13. Como migrar um contrato sem flag day?
14. Qual decisão você mudaria com nova evidência?

### Pergunta surpresa

O avaliador propõe uma mudança, por exemplo “tarefas agora consomem recursos
limitados”. Não implemente ao vivo. Analise:

- requisito e não objetivo;
- mudança do problema algorítmico;
- impacto no modelo/contrato;
- arquitetura;
- testes;
- migration/compatibilidade;
- risco e experimento.

Capacidade de dizer “preciso medir/descobrir X” vale mais que improvisar certeza.

## 14. Falhas comuns de projeto

| Sintoma | Causa | Recuperação |
|---|---|---|
| muitas funcionalidades, núcleo frágil | escopo sem prioridade | congelar Must e remover Could |
| arquitetura genérica | padrão antes de driver | voltar a cenários de qualidade |
| cobertura alta, poucos bugs detectados | asserções fracas | propriedades e mutação |
| benchmark “rápido” | método não reproduzível | protocolo, baseline e distribuição |
| README funciona só na máquina do autor | estado implícito | teste em ambiente limpo |
| documentação promete mais que código | artefatos sem gate | rastreabilidade e exemplos executáveis |
| defesa esconde limitações | avaliação confundida com marketing | registrar risco/dívida honestamente |
| runbook não recupera | nunca ensaiado | exercício e revisão por terceiro |

## 15. Exercícios em três níveis

### Nível 1 — projeto guiado

1. Execute baseline e explique cada módulo.
2. Escolha uma evolução e escreva requisitos.
3. Produza diagramas/ADR.
4. Implemente uma fatia vertical com testes.
5. Demonstre sucesso e erro em checkout limpo.

**Conclusão:** todos os gates dos milestones 1–3 possuem links e comandos.

### Nível 2 — endurecimento

1. Complete propriedades, contrato e integração.
2. Injete cinco defeitos.
3. Faça benchmark reproduzível.
4. Modele ameaça e teste limites.
5. Escreva/ensaie runbook.
6. Prepare release/changelog/revisão.

**Conclusão:** outra pessoa executa milestone 4–6 sem orientação oral.

### Nível 3 — projeto autoral e defesa

1. Aprove proposta e milestones.
2. Entregue walking skeleton cedo.
3. Registre decisões semanais.
4. Faça revisão cruzada pela rubrica.
5. Corrija gates, congele versão e defenda.
6. Responda à mudança surpresa por análise de impacto.

**Conclusão:** pelo menos 75 pontos, nenhum gate essencial e evidência navegável.

## Checklist de domínio

- [ ] Transformo um problema em escopo, invariantes e critérios.
- [ ] Entrego milestones executáveis, não camadas vazias.
- [ ] Justifico estruturas e complexidade com operação dominante.
- [ ] Limites arquiteturais resistem à troca de uma borda.
- [ ] Testes combinam exemplos, propriedades, integração e contrato.
- [ ] Qualidade inclui performance, segurança e operação.
- [ ] Histórico, PR e documentação permitem revisão.
- [ ] Release é reproduzível e rastreável.
- [ ] Runbook foi usado por outra pessoa.
- [ ] Rubrica aponta evidência, não opinião.
- [ ] Defesa explica alternativas, falhas e limitações.
- [ ] Sei recusar escopo que não cabe ou muda o problema sem descoberta.

## Encerramento

Engenharia madura alterna descoberta, decisão, implementação, evidência e
operação. Continue aprofundando sistemas operacionais, redes, dados e segurança,
mas mantenha este ciclo: **declare a invariante, escolha o limite, teste a falha,
observe o sistema e registre o aprendizado**.
