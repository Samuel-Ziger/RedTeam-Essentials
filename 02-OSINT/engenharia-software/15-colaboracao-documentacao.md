# 15 — Colaboração, Git e documentação operacional

Software de equipe é comunicação preservada em código, histórico, testes,
decisões e procedimentos. Código tecnicamente correto que só uma pessoa consegue
entender, publicar ou recuperar continua sendo um risco.

Este capítulo aplica o fluxo ao
[Dependency Planner](projetos/dependency-planner/README.md). Não exige plataforma
específica: pull request (PR) representa qualquer revisão formal antes de integrar.

## Objetivos

Ao concluir, você deverá conseguir:

- organizar mudanças pequenas e um histórico Git explicável;
- comparar trunk-based development e branches longas;
- preparar e revisar PRs por risco;
- evoluir contratos com Semantic Versioning e política de depreciação;
- escrever README, referência, ADR, changelog e runbook;
- coordenar incidente e produzir post-mortem sem culpa;
- deixar evidência suficiente para outra pessoa validar e reverter.

## Pré-requisitos e modelo mental

Conclua [Testes e qualidade](14-testes-qualidade.md). Pense em cada mudança como
um pacote de evidência:

```text
intenção
  + diff pequeno
  + testes
  + compatibilidade
  + impacto operacional
  + revisão
  + plano de reversão
```

Git armazena versões; não substitui comunicação. Documentação descreve contrato e
operação; não substitui testes. Revisão reduz risco; não transfere toda a
responsabilidade ao revisor.

## 1. Estado, diff e histórico

Antes de editar:

```bash
git status --short
git branch --show-current
git log --oneline -5
```

Antes de propor:

```bash
git diff
git diff --check
git status --short
```

Revise arquivos novos, dados gerados, segredos e mudanças não relacionadas.
`git diff` não mostra conteúdo de arquivos ainda não rastreados; `status` é
obrigatório.

### Commit atômico

Um commit útil:

- tem uma intenção;
- mantém build/testes no estado esperado;
- não mistura formatação global e mudança semântica;
- inclui documentação/teste inseparáveis do contrato;
- pode ser revisado e, quando possível, revertido isoladamente.

Mensagem:

```text
planner: preserve cycle path in CLI errors

Expose the closed path already calculated by the domain so CI users can
locate the invalid dependency without reproducing the graph manually.
```

O título diz o que mudou; corpo explica por quê, consequência ou limitação.
`fix`, `changes`, `final` e `WIP2` não ajudam investigação futura.

### Divida mudança verticalmente

Para adicionar adaptador CSV:

1. contrato e casos de teste do CSV;
2. adaptador sob a porta existente;
3. opção da CLI/composition root;
4. documentação e exemplos;
5. observabilidade/limites, se relevantes.

Evite commit “criar todas as interfaces” sem comportamento e outro “fazer
funcionar”. Cada passo deveria contar uma parte verificável da história.

## 2. Estratégias de branch

### Trunk-based development

- integração frequente em `main`/trunk;
- branches curtas, idealmente horas ou poucos dias;
- CI forte;
- mudanças incompletas escondidas por feature flag ou compatibilidade;
- releases derivadas de commits conhecidos.

Reduz divergência e conflitos tardios. Exige disciplina para que trunk permaneça
publicável.

### GitFlow/branches longas

Branches de feature/release/hotfix podem atender produtos com janelas formais e
versões mantidas em paralelo. Custos:

- integração tardia;
- cherry-picks e correções duplicadas;
- diferença entre o que foi testado e publicado;
- conflitos semânticos grandes.

Não escolha pelo nome. Pergunte:

- quantas versões são suportadas simultaneamente?
- com que frequência há integração e release?
- CI consegue validar cada mudança?
- feature flag é operável e removida?
- existe exigência regulatória de estabilização?

Para o Planner pequeno, trunk-based com PR curto é suficiente.

### Feature flags

Flag separa deploy de ativação, mas adiciona estados:

```text
código antigo + flag off
código novo + flag on
rollout parcial
```

Cada estado precisa de teste, proprietário, métrica e data de remoção. Não use
flag para esconder migration incompatível nem deixe flags permanentes sem dono.

## 3. Atualize sua branch com segurança

Fetch traz referências sem alterar seu trabalho:

```bash
git fetch origin
```

Merge preserva o ponto de integração; rebase reescreve commits da branch para um
histórico linear. Não rebase commits compartilhados sem acordo. Em conflito:

1. entenda as duas intenções;
2. resolva semanticamente, não escolhendo “ours/theirs” por conveniência;
3. execute testes das áreas combinadas;
4. revise o diff resultante;
5. continue a operação conforme o comando iniciado.

Conflito resolvido sem marcador ainda pode estar logicamente errado.

Nunca use limpeza/reset destrutivo para resolver dúvida sobre arquivos que podem
conter trabalho de outra pessoa. Inspecione alvo e preserve mudanças.

## 4. Pull request como argumento técnico

Um PR deve responder:

```markdown
## Problema
Qual comportamento/risco motivou a mudança?

## Solução
O que mudou e quais alternativas foram rejeitadas?

## Contratos e compatibilidade
JSON, CLI, API, eventos, schema ou configuração mudaram?

## Evidência
Comandos, testes, benchmark e resultado.

## Risco e operação
Falhas possíveis, observabilidade, rollout e rollback.

## Fora do escopo
O que foi deliberadamente adiado?
```

Para mudança visual, inclua captura; para performance, protocolo e baseline;
para migration, locks/backfill; para segurança, não inclua exploit ou segredo,
mas descreva ameaça e teste seguro.

### Tamanho

PR pequeno reduz carga cognitiva. Linhas não são medida perfeita: refatoração
mecânica pode ser grande e simples; dez linhas num algoritmo concorrente podem
ser arriscadas. Separe mudanças por intenção e peça revisão especializada cedo.

### Draft e design review

Use draft para feedback antes de polir. Decisão de alto custo merece ADR/design
review antes de milhares de linhas. Código pronto demais cria pressão para
aceitar a solução.

## 5. Revisão de código

Ordem recomendada:

1. requisito, escopo e ameaça;
2. correção e invariantes;
3. compatibilidade e dados;
4. arquitetura/dependências;
5. concorrência, falhas e operação;
6. testes e observabilidade;
7. clareza;
8. estilo automatizável.

Perguntas para o Planner:

- dependência ainda significa pré-requisito?
- desempate continua determinístico?
- erro impede plano parcial?
- novo adaptador valida antes do domínio?
- mudança preserva complexidade e limite?
- saída/código de erro quebram CI consumidor?
- teste falharia com a implementação antiga?

### Classifique comentários

- **bloqueador:** correção, segurança, contrato ou risco inaceitável;
- **sugestão:** melhoria não obrigatória;
- **dúvida:** falta contexto;
- **nit:** detalhe pequeno, preferencialmente automatizável.

Exemplo:

```text
[bloqueador] Este retry repete POST sem chave idempotente. Um timeout pode
duplicar a solicitação. Podemos exigir Idempotency-Key ou remover o retry?
```

Critique comportamento/código, não pessoa. Explique impacto e proponha caminho.
Autor responde com evidência, esclarece ou altera; “feito” sem contexto impede
aprendizado.

### Responsabilidade compartilhada

Aprovação não absolve autor. Revisor não precisa redesenhar tudo sozinho.
Discordância persistente usa critérios: requisito, benchmark, ADR, experimento
ou responsável técnico — não autoridade implícita.

## 6. Merge, release e proveniência

Estratégias:

- merge commit preserva estrutura da branch;
- squash cria um commit por PR;
- rebase/fast-forward preserva commits lineares.

Escolha uma política e otimize o histórico que a equipe realmente consulta.
Commits intermediários ruins não viram melhores só porque foram preservados.

Release deve apontar para commit/tag imutável e artefato testado. Registre:

- versão;
- commit;
- toolchain;
- checks;
- checksums/assinatura quando requisito;
- dependências;
- changelog;
- instrução de rollback.

Não reconstrua para produção um artefato diferente do validado sem necessidade.

## 7. Semantic Versioning e contratos

Para API pública com versão `MAJOR.MINOR.PATCH`:

- **MAJOR:** mudança incompatível;
- **MINOR:** funcionalidade compatível;
- **PATCH:** correção compatível.

Antes de 1.0, SemVer permite instabilidade adicional, mas a política precisa
dizer o que consumidores podem esperar. SemVer não determina sozinho:

- frequência de release;
- duração do suporte;
- migração de dados;
- protocolo de eventos;
- versão da CLI;
- comportamento operacional.

### Superfícies do Planner

- formato do arquivo;
- saída JSON;
- texto/códigos/canais da CLI;
- imports públicos do pacote;
- comportamento determinístico;
- nomes e categorias de erro.

Adicionar campo pode quebrar consumidor que rejeita desconhecidos. Renomear texto
de erro pode quebrar automação mal desenhada, embora o ideal seja código
estruturado. Inventarie consumidores antes de chamar algo de compatível.

### Depreciação

1. anuncie alternativa e motivo;
2. suporte convivência;
3. emita sinal mensurável sem expor dados;
4. ofereça ferramenta/documento de migração;
5. defina versão/data de remoção;
6. remova após evidência.

Para alterar `duration`:

```text
v1: duration inteiro em unidades abstratas
v2: durationMinutes decimal
```

Leitor dual e escritor novo permitem transição. Aceitar ambos sem precedência
definida cria ambiguidade.

## 8. Changelog

Changelog é para consumidores, não cópia do log Git. Categorias:

- Added;
- Changed;
- Deprecated;
- Removed;
- Fixed;
- Security.

Exemplo:

```markdown
## [1.2.0] — 2026-10-03

### Added
- Saída JSON agora inclui `schemaVersion`.

### Deprecated
- Documentos sem `schemaVersion`; suporte previsto até 2.0.0.

### Fixed
- Ciclos agora retornam caminho fechado determinístico.
```

Inclua ação exigida e link para migração. Em item de segurança, publique detalhe
suficiente para atualizar com segurança sem facilitar abuso prematuro.

## 9. Documentação em camadas

| Artefato | Pergunta |
|---|---|
| README | o que é e como executar/verificar? |
| tutorial | como aprender em sequência? |
| how-to | como concluir uma tarefa específica? |
| referência | quais contratos/opções existem? |
| explicação | por que o sistema funciona assim? |
| ADR | por que esta decisão foi tomada? |
| changelog | o que mudou para consumidores? |
| runbook | como diagnosticar, mitigar e recuperar? |

Misturar tudo em um README torna cada público incapaz de localizar informação.
Use links e uma fonte de verdade.

### Documentação executável

- comandos de README rodam em CI;
- exemplos usam fixtures versionadas;
- schema/OpenAPI é validado;
- links locais são verificados;
- snippet crítico vira teste quando possível;
- versão mínima e saída esperada são explícitas.

Comentários no código explicam por que, restrição, workaround ou invariante. Não
repita `index += 1` como “incrementa index”.

### Definition of Done documental

Uma mudança só termina quando:

- contrato e exemplos refletem comportamento;
- ADR foi adicionado/substituído se decisão mudou;
- runbook cobre novo modo de falha;
- changelog informa consumidor;
- links/comandos foram executados.

## 10. Runbook

Mesmo uma CLI pode ter runbook:

```markdown
# Runbook — Planner encerra com código 2

## Impacto
O pipeline não recebeu um plano; nenhuma tarefa foi executada pelo Planner.

## Sinais
Exit code 2; stdout vazio; categoria em stderr.

## Diagnóstico seguro
1. registre versão e hash da fixture, não conteúdo sensível;
2. valide JSON e campos;
3. procure referência ausente, duplicata ou ciclo;
4. reproduza com fixture mínima sanitizada.

## Mitigação
Corrigir entrada ou restaurar última fixture válida.

## Escalada
Mantenedor do contrato se uma entrada documentada for rejeitada.

## Recuperação
Reexecutar; confirmar exit 0, stderr vazio e JSON válido.
```

Todo passo deve ser seguro, reversível quando possível e conter resultado
esperado. Não escreva “investigue logs” sem consulta, intervalo e interpretação.

Runbook precisa ser exercitado. Um comando perigoso ou desatualizado durante
incidente amplia impacto.

## 11. Gestão de incidentes

Incidente é degradação não planejada que exige coordenação. Elementos:

- severidade baseada em impacto;
- incident commander coordenando;
- responsável técnico pela investigação;
- comunicação com atualizações regulares;
- registro cronológico;
- mitigação antes de perfeição;
- critério de recuperação;
- handoff e encerramento.

Evite várias pessoas executando comandos sem coordenação. Preserve evidência,
mas não copie dados pessoais para canais amplos.

### Linha do tempo

```text
14:02 alerta: taxa de erro > SLO
14:05 confirmado: entrada v2 rejeitada por leitores v1
14:08 rollout pausado
14:12 tráfego restaurado para versão anterior
14:20 erro abaixo do limiar; monitoramento continua
```

Marque horário e fonte. Diferencie fato observado de hipótese.

## 12. Post-mortem sem culpa

Estrutura:

- resumo e impacto;
- detecção;
- linha do tempo;
- fatores contribuintes;
- o que ajudou/atrapalhou;
- ações com dono, prazo e critério;
- aprendizados.

“Pessoa publicou configuração errada” não explica por que revisão, validação,
rollout e rollback permitiram impacto. Procure condições sistêmicas sem apagar
responsabilidade profissional.

Ação fraca:

```text
ter mais cuidado
```

Ação verificável:

```text
até 2026-10-15, CI deve executar leitores v1 e v2 contra fixtures de convivência;
dono: equipe Planner; concluído quando o gate bloqueia campo incompatível.
```

Priorize poucas ações de alto impacto; backlog infinito não melhora o sistema.

## 13. Falhas comuns e diagnóstico

| Sinal | Causa | Correção |
|---|---|---|
| PR enorme | integração tardia/escopo misto | fatias verticais e design review |
| histórico sem contexto | commits genéricos | intenção + motivo + contrato |
| revisão discute só estilo | automação ausente | lint e checklist por risco |
| docs divergem | sem dono/gate | exemplos executáveis e DoD |
| consumidor quebra em “minor” | superfície não inventariada | contratos + política SemVer |
| runbook piora incidente | nunca ensaiado | game day seguro e revisão |
| post-mortem culpa pessoa | análise termina no operador | controles e fatores sistêmicos |

## 14. Exercícios em três níveis

### Nível 1 — mudança revisável

1. Divida “adaptador CSV” em commits independentes.
2. Escreva mensagens com intenção e motivo.
3. Prepare PR com evidência, risco e rollback.
4. Revise-o com comentários classificados.

**Evidência:** outra pessoa entende o histórico e valida cada passo.

### Nível 2 — contrato e documentação

1. Inventarie todas as superfícies públicas do Planner.
2. Classifique dez mudanças como patch, minor, major ou dependente da política.
3. Escreva plano de depreciação de `duration`.
4. Produza README, changelog e ADR coerentes.
5. Automatize conceitualmente a execução dos exemplos.

**Evidência:** um consumidor sabe se precisa agir e como migrar.

### Nível 3 — operação colaborativa

Simule incidente de leitor v1 incompatível:

1. defina severidade e papéis;
2. produza linha do tempo;
3. use runbook para mitigar/recuperar;
4. comunique estado sem dados sensíveis;
5. escreva post-mortem;
6. crie três ações com dono, prazo e teste de conclusão.

**Evidência:** observador consegue reconstruir decisões e confirmar recuperação.

## Checklist de domínio

- [ ] Mudanças são pequenas por intenção, não apenas por linhas.
- [ ] Branches integram cedo e flags têm teste/dono/remoção.
- [ ] PR explica problema, contrato, evidência, risco e rollback.
- [ ] Revisão começa por correção e risco, não estilo.
- [ ] Política de merge produz histórico útil.
- [ ] Release referencia exatamente o artefato validado.
- [ ] SemVer está ligado a uma API pública e política de suporte.
- [ ] Depreciação possui convivência, telemetria e prazo.
- [ ] Documentos têm público/pergunta e exemplos verificáveis.
- [ ] Runbooks foram ensaiados e têm sinais/resultados.
- [ ] Incidentes têm coordenação, comunicação e evidência.
- [ ] Post-mortems geram ações sistêmicas verificáveis.

Finalize a formação em [Projetos, avaliação e encerramento](16-projetos-avaliacao.md).
