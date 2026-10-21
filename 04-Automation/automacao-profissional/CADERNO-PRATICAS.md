# Caderno de práticas — Automação profissional

Estas 30 práticas transformam os capítulos em evidência. N1 verifica fundamentos,
N2 combina controles e N3 exige decisão arquitetural, falha injetada e defesa.
Use dados sintéticos, diretórios temporários, fakes e serviços autorizados.

Para cada entrega, registre hipótese, comando, versões, resultado, falha encontrada
e mudança feita. Não comece pelas [respostas orientativas](RESPOSTAS.md).

## Decisão, contrato e efeitos

### 01 — Matriz de candidatos (N1)

Compare cinco tarefas por frequência, variabilidade, verificabilidade,
reversibilidade e impacto. **Aceite:** automatizar, assistir ou manter manual está
justificado com critérios, não preferência pessoal.

### 02 — Mapa do processo (N1)

Desenhe gatilho, validação, decisão, aprovação, efeito, confirmação e recuperação.
**Aceite:** exceções e pessoa responsável aparecem em cada fronteira.

### 03 — Nível de autonomia (N2)

Projete evolução observar → recomendar → planejar → aplicar. **Aceite:** cada
transição exige métrica, teste de falha e condição de voltar.

### 04 — Contrato executável (N1)

Escreva tabela entrada → efeito → pós-condição → código de saída. **Aceite:**
uso inválido, conflito, falha operacional e parcial são distintos.

### 05 — Plan/apply (N2)

Implemente planejador puro e executor fake. **Aceite:** dry-run e apply consomem o
mesmo Plan; um adapter sentinela prova zero mutação na simulação.

### 06 — Idempotência por propriedade (N2)

Execute o mesmo comando duas vezes. **Aceite:** estado final é igual, segunda
execução explica skip e a chave detecta payload divergente.

## Arquivos e pipelines

### 07 — Caminhos hostis (N1)

Teste absoluto, ponto-ponto, segmentos vazios, separadores e Unicode. **Aceite:**
nenhum destino escapa da raiz e todos falham antes de escrever.

### 08 — Corrida de destino (N3)

Pause após o plano, crie o destino por outro ator e continue. **Aceite:** criação
exclusiva preserva o arquivo concorrente e o resultado é conflict.

### 09 — Escrita atômica (N2)

Falhe após N bytes do temporário. **Aceite:** versão final anterior permanece
íntegra e temporário é removido ou identificado para limpeza segura.

### 10 — Manifesto determinístico (N2)

Descubra os mesmos arquivos em ordens distintas. **Aceite:** serialização e digest
são idênticos, sem caminho pessoal nem timestamp no conteúdo canônico.

### 11 — Pipeline CSV para JSONL (N1)

Valide bytes, sintaxe, schema e semântica. **Aceite:** Unicode, linha truncada,
tipo errado e limite + 1 têm causas diferentes.

### 12 — Quarentena e replay (N2)

Separe registros inválidos com ID e razão. **Aceite:** retenção, acesso e replay
estão definidos; replay preserva identidade e proveniência.

### 13 — Streaming limitado (N2)

Processe entrada dez vezes maior que a memória-alvo. **Aceite:** consumo permanece
limitado e recebidos = aceitos + rejeitados.

### 14 — Checkpoint após commit (N3)

Falhe antes e depois de publicar o item 501. **Aceite:** nenhum item é perdido ou
duplicado e a retomada usa a mesma versão de regra.

## Integrações, jobs e resiliência

### 15 — Cliente HTTP defensivo (N2)

Use servidor fake para 200 com HTML, JSON truncado, corpo excessivo e 503. **Aceite:**
timeout, tipo, tamanho, schema e classes de erro são testados.

### 16 — Paginação (N2)

Implemente cursor com limite e detecção de ciclo. **Aceite:** cursor repetido não
gera loop e a política de consistência está declarada.

### 17 — Webhook autenticado (N3)

Verifique HMAC sobre bytes brutos, timestamp e event ID. **Aceite:** segredo em
rotação funciona, replay é recusado e evento válido duplicado não repete efeito.

### 18 — Janela lógica (N1)

Modele job diário com data civil e zona IANA. **Aceite:** atraso do scheduler não
muda a janela e a chave idempotente não usa run ID.

### 19 — Lease e fencing (N3)

Simule worker pausado, lease expirada e novo owner. **Aceite:** token antigo é
rejeitado no sink; lock local não é apresentado como garantia distribuída.

### 20 — Backoff sem esperar (N2)

Injete clock, RNG e sleeper. **Aceite:** full jitter, cap, Retry-After, deadline e
cancelamento são afirmados sem sleep real.

### 21 — Fila e backpressure (N2)

Produza mais rápido que o consumidor. **Aceite:** a fila não cresce sem limite;
idade, rejeição e resultado de cada item são observáveis.

### 22 — Concorrência medida (N2)

Compare 1, 2, 4 e 8 workers. **Aceite:** limite escolhido cita throughput, p95,
erros, memória e recurso limitante.

### 23 — Cancelamento cooperativo (N3)

Cancele com itens esperando, executando e em commit. **Aceite:** novos trabalhos
param, commits têm estado verdadeiro e todos os itens reconciliam.

## Documentos, segurança e operação

### 24 — Jornada de navegador (N2)

Automatize página local por role/label e condição. **Aceite:** nenhum sleep fixo,
zero seletor de layout e resultado confirmado além do clique.

### 25 — CSV resistente (N2)

Exporte aspas, newline, Unicode e prefixos de fórmula. **Aceite:** round-trip
preserva texto e o consumidor suportado não executa a entrada como fórmula.

### 26 — Canário de segredo (N2)

Injete valor sintético e provoque falhas. **Aceite:** o canário não aparece em
stdout, stderr, logs, traces, screenshots, artifacts ou bundle de suporte.

### 27 — Eventos e reconciliação (N2)

Defina schema de eventos por item e resumo. **Aceite:** outcomes fecham, IDs de alta
cardinalidade não viram labels e logs não carregam payload.

### 28 — Fault injection (N3)

Crie matriz antes/depois de cada commit. **Aceite:** cada ponto descreve estado
visível, temporário, retomada e teste automatizado.

### 29 — Artifact fora do checkout (N2)

Empacote e execute em diretório limpo. **Aceite:** help, version, dry-run e apply
controlado funcionam sem dependência global ou caminho do autor.

### 30 — Game day do capstone (N3)

Outra pessoa opera pelo runbook enquanto você injeta conflito, timeout e falha de
audit sink. **Aceite:** ela diagnostica, decide retomar ou parar e verifica a
recuperação sem editar estado manualmente.

## Diário de aprendizagem

Ao concluir cada bloco, responda:

1. Qual invariante agora possui prova automatizada?
2. Que hipótese foi refutada por medição?
3. Qual falha ainda depende de procedimento manual?
4. Que decisão merece ADR?
5. Outra pessoa reproduziu a evidência?

