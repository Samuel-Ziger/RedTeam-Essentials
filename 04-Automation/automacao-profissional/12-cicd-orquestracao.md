# 12 — CI/CD e orquestração segura

CI/CD é automação que executa código do repositório com acesso a compute,
artifacts e, às vezes, ambientes sensíveis. O workflow deve ser tratado como parte
da aplicação: versionado, testado, observado e revisado por risco.

## Objetivos

- modelar pipeline como DAG com gates e artefatos;
- separar verificação de contribuição e publicação privilegiada;
- produzir uma vez e promover o mesmo artefato;
- aplicar permissões mínimas, OIDC e proveniência;
- operar concorrência, rollback e agendamento sem duplicar efeitos.

## 1. Pipeline como grafo

~~~text
                 -> unit ---------
checkout -> lint -> contract -----+-> package -> verify -> attest
                 -> integration --              |
                                                v
                                      approve -> release -> smoke
~~~

Dependências precisam ser explícitas. Jobs independentes podem rodar juntos; gates
esperam todas as evidências necessárias. Identifique caminho crítico antes de
paralelizar tudo.

Cada job declara entradas, saídas, timeout, permissões e condição de execução.
Um job que depende de arquivo do anterior usa artifact, não a hipótese de workspace
compartilhado.

## 2. Cache não é artifact

- cache acelera material regenerável e pode desaparecer;
- artifact preserva resultado identificado de uma execução;
- release é artifact promovido com versão e proveniência.

Não publique diretamente de cache. Verifique digest do artifact e sua origem. A
chave de cache inclui lockfile e plataforma; restauração parcial não pode inserir
dependência incompatível silenciosamente.

## 3. Build uma vez, promover

Reconstruir em produção cria bytes diferentes dos testados. O fluxo correto:

1. checkout do commit exato;
2. dependências fixadas;
3. build em ambiente controlado;
4. testes e verificação do conteúdo;
5. hash, SBOM e provenance;
6. armazenamento imutável;
7. promoção do mesmo digest entre ambientes.

Reprodutibilidade completa pode exigir controlar timestamps, ordem, locale e
toolchain. Mesmo quando builds ainda não são byte-idênticos, registre entradas e
proveniência para investigar.

## 4. Zonas de confiança

Considere três zonas:

| Zona | Código | Credenciais |
|---|---|---|
| contribuição | PR/fork não confiável | nenhuma de publicação |
| integração | branch protegida | leitura e artifacts limitados |
| release | workflow/ambiente protegido | token curto e escopo mínimo |

Workflow privilegiado não deve executar código arbitrário do PR antes da
aprovação. Artifact vindo de zona menos confiável precisa ser tratado como entrada
não confiável e validado.

## 5. Permissões e OIDC

Defina permissões por job. Checkout geralmente precisa apenas de leitura. Publicar
pacote não implica administrar repositório.

OIDC permite trocar identidade do job por credencial curta no provedor. A relação
de confiança valida issuer, audience e subject, restringindo repositório, branch,
tag ou ambiente. Dar permissão para solicitar ID token não concede por si só acesso
ao recurso; o provedor decide pelo trust policy.

Não torne subject amplo para “fazer funcionar”. Teste claims e documente rotação
ou revogação do vínculo.

## 6. Dependências do workflow

Actions e plugins são dependências executáveis. Fixe revisão imutável, revise origem
e atualize por processo controlado. Uma tag pode mudar. Scripts baixados durante o
job precisam de HTTPS, origem, digest/assinatura e versão.

Evite pipe direto de download para shell. Baixe, verifique e execute. Não inclua
valores de evento em run scripts por interpolação; passe como dado em variável
apropriada e valide.

## 7. Matriz e compatibilidade

Teste combinações suportadas, não o universo. Defina:

- versão mínima e atual do runtime;
- plataformas realmente distribuídas;
- caminho de upgrade de schema;
- dependência externa simulada e, separadamente, sandbox real.

Use fail-fast conforme objetivo. Em matriz de compatibilidade, deixar todas as
células concluírem fornece diagnóstico; em release, falha essencial deve bloquear.

## 8. Concorrência e ambientes

Duas releases simultâneas podem se ultrapassar. Use grupo de concorrência por
ambiente e decida se a antiga é cancelada ou aguardada. Cancelar pipeline não
reverte deploy em andamento; a etapa precisa de commit e reconciliação.

Ambiente protegido pode exigir aprovação, janela e reviewers. Aprovação precisa
mostrar digest, mudanças, evidências e plano de rollback, não apenas um botão.

## 9. Release e rollback

Estratégias: rolling, blue/green, canary ou substituição simples, conforme a
plataforma. Todas precisam de:

- sinal de saúde e critério de abortar;
- compatibilidade entre código e dados;
- artefato anterior disponível;
- controle de tráfego/ativação;
- verificação pós-rollback.

Rollback de binário não desfaz migração de dados. Use mudanças compatíveis em
etapas: expandir, migrar, trocar leitores/escritores e só depois contrair.

## 10. Orquestração de jobs

O orquestrador gerencia agenda e estado de infraestrutura; o job permanece
idempotente. Configure deadline de início, política de concorrência, tentativas,
timeout, histórico e suspensão. Assuma que um agendador pode criar mais de uma
execução em certas condições.

Health check de job não é igual ao de serviço. Exponha progresso, checkpoint e
deadline. Encerrar pod/processo deve acionar cancelamento cooperativo e preservar
estado confirmado.

## 11. Evidências sempre disponíveis

Relatórios de teste e logs sanitizados devem ser enviados mesmo quando um passo
falha, sem executar publicação. Use condição de cleanup/upload cuidadosamente e
limite retenção. Não inclua diretório inteiro do runner como artifact.

## Falhas e diagnóstico

| Sintoma | Causa | Evidência |
|---|---|---|
| release difere do testado | rebuild por ambiente | digest promovido |
| PR acessa segredo | trust zones misturadas | evento e permissões |
| job pendurado | sem timeout/cancelamento | phase e deadline |
| deploys se ultrapassam | concurrency ausente | environment/run ID |
| rollback falha | schema incompatível | matriz código-dado |

## Exercícios

### Nível 1 — DAG

Desenhe pipeline e caminho crítico. **Aceite:** jobs declaram inputs, artifacts,
permissões, timeout e condição de bloqueio.

### Nível 2 — trust zones

Separe PR, integração e release. **Aceite:** código de fork não recebe segredo e
release usa identidade curta restrita ao ambiente.

### Nível 3 — promoção

Produza, verifique, ateste e promova um artifact. **Aceite:** o mesmo digest chega
ao destino, concorrência é controlada e rollback foi ensaiado.

## Checklist

- [ ] Pipeline é DAG explícito, com timeouts.
- [ ] Cache, artifact e release têm papéis distintos.
- [ ] O mesmo artifact verificado é promovido.
- [ ] Permissões são mínimas por job e zona.
- [ ] Dependências de workflow são imutáveis e revisadas.
- [ ] Release, dados e rollback possuem compatibilidade testada.

