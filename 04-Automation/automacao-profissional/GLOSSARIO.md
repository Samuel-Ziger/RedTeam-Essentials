# Glossário

**Adapter:** implementação que traduz uma porta interna para filesystem, HTTP,
banco, fila ou outro protocolo externo.

**Artifact:** resultado identificado de build/test preservado entre jobs ou
publicado como release.

**Atomicidade:** propriedade de uma mudança aparecer inteira ou não aparecer.
Não implica durabilidade.

**Audit trail:** registro protegido de ator, ação, alvo, decisão e resultado.

**Backoff:** aumento do intervalo entre tentativas.

**Backpressure:** mecanismo pelo qual consumidor limita ou desacelera produtor.

**Blast radius:** alcance máximo de dano ou efeito de uma falha.

**Bulkhead:** isolamento de pools/recursos para uma falha não consumir tudo.

**Canary:** amostra pequena ou valor sintético usado para validar comportamento
antes de ampliar; também pode detectar vazamento de segredo.

**Cardinalidade:** quantidade de valores distintos de um campo; cardinalidade alta
em labels de métrica costuma elevar custo.

**Checkpoint:** posição durável do último efeito confirmado para retomada.

**Circuit breaker:** máquina de estados que interrompe chamadas a uma dependência
degradada e permite provas controladas de recuperação.

**Commit:** ponto em que um efeito se torna visível/durável conforme o contrato.

**Compensação:** nova operação que reduz ou corrige efeito anterior; não volta o
tempo e pode falhar.

**Concorrência:** progresso sobreposto de trabalhos. Não implica paralelismo real.

**Contrato:** conjunto observável de entradas, efeitos, pós-condições, erros,
limites e compatibilidade.

**Dead-letter:** armazenamento de itens que esgotaram a política normal e precisam
de triagem/replay.

**Deadline:** instante absoluto até o qual a operação precisa terminar.

**Determinismo:** mesma entrada e dependências controladas produzem a mesma saída.

**Dry-run:** descoberta, validação e planejamento reais sem efeitos de aplicação.

**Exactly-once:** promessa frequentemente limitada a uma camada. Em sistemas
distribuídos, costuma ser alcançada no efeito de negócio por entrega repetível,
idempotência e deduplicação.

**Fencing token:** número monotônico usado pelo destino para rejeitar owner antigo
que retornou após perder a lease.

**Fixture:** entrada de teste pequena, estável e versionada.

**Full jitter:** espera aleatória entre zero e o teto calculado do backoff.

**Idempotência:** repetir a mesma intenção produz o mesmo estado final relevante.

**Idempotency key:** identidade estável que permite reconhecer tentativas da mesma
operação.

**Janela lógica:** intervalo/data de negócio processado, separado do horário real
em que o job iniciou.

**Lease:** concessão de ownership com expiração e renovação.

**Manifesto:** documento versionado que descreve plano, artifact ou conjunto de
operações.

**Outbox:** padrão que grava estado de negócio e intenção de mensagem na mesma
transação local.

**Outcome:** estado terminal enumerado de uma operação.

**Paralelismo:** execução simultânea real.

**Plan/apply:** separa decisão revisável da execução de efeitos.

**Port:** interface interna que expressa a capacidade necessária pelo caso de uso.

**Provenance:** evidência da origem e processo que produziram um dado/artifact.

**Quarentena:** armazenamento controlado de registros inválidos para triagem.

**Rate limit:** limite de inícios/operações por unidade de tempo.

**Reconciliação:** compara intenção, evidência e estado observado para decidir
o resultado verdadeiro.

**Replay:** reprocessamento controlado que conserva identidade e proveniência.

**Retry budget:** limite de tentativas e/ou tempo dedicado a repetições.

**Runbook:** procedimento operacional com diagnóstico, decisão, recuperação e
pós-verificação.

**Saga:** sequência de transações locais com compensações explícitas.

**SBOM:** inventário de componentes de software de um artifact.

**Schema:** contrato estrutural de campos, tipos, limites e versão.

**SLO:** objetivo mensurável de nível de serviço em uma janela.

**Staging:** área temporária onde a saída é validada antes de publicar.

**TOCTOU:** corrida entre o momento de verificar e o momento de usar um recurso.

**Uncertain:** estado em que o efeito pode ter ocorrido, mas ainda não foi
confirmado; exige reconciliação antes de retry cego.

**Watermark:** maior posição contígua confirmada em um fluxo ordenado.

**Webhook:** requisição iniciada por um provedor para notificar evento; requer
autenticação, proteção contra replay e processamento idempotente.

