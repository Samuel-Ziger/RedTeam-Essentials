# Respostas orientativas

Estas respostas descrevem propriedades esperadas, não uma implementação única.
Consulte depois de tentar. Uma resposta forte liga decisão, código, teste e
evidência reproduzível.

## Capítulo 00 — O que automatizar

Um bom candidato possui regra estável, pós-condição observável e impacto limitado.
Frequência sozinha não basta: processo frequente, mas ambíguo, deve primeiro ser
assistido ou validado. A proposta madura declara critérios para aumentar autonomia
e para desativar.

Na matriz, diferencie ganho bruto de custo total. Inclua exceções, manutenção,
credenciais, integrações e incidentes. Um checklist pode vencer um serviço.

## Capítulo 01 — Contratos e idempotência

Idempotência é sobre estado final relevante, não ausência total de atividade.
Uma segunda execução pode registrar attempt e retornar skipped. A chave deriva da
intenção e detecta payload diferente.

Dry-run fiel produz o mesmo Plan do apply e bloqueia adapters mutáveis. O executor
revalida pré-condições porque o estado pode mudar. Timeout pós-envio é uncertain,
não failed automático.

## Capítulo 02 — Arquivos

Validar ponto-ponto e resolver caminho reduz risco, mas não elimina troca por
symlink. Criação exclusiva e APIs relativas à raiz fortalecem a garantia. Em
laboratório, documente que um adversário local concorrente está fora do modelo se
as primitivas da plataforma não forem usadas.

Atomicidade, durabilidade e exclusividade são propriedades diferentes. Replace
atômico pode sobrescrever; create-exclusive evita isso. Hash confirma bytes, não
autoria.

## Capítulo 03 — Pipelines

Valide transporte, decode, sintaxe, schema e semântica separadamente. Quarentena
precisa de retenção e replay. Uma reconciliação forte define todas as categorias e
faz as contagens fecharem.

Checkpoint segue efeito confirmado. Se falhar depois do efeito e antes do
checkpoint, haverá replay; o sink deve deduplicar pela mesma chave.

## Capítulo 04 — HTTP e webhooks

Um client responsável limita tempo e bytes, valida status, Content-Type, parse,
schema e invariantes. 200 não é sinônimo de sucesso de domínio.

Webhook é verificado sobre bytes brutos, com timestamp e event ID. Responder 2xx
antes de persistir pode perder o evento; processar dentro da requisição pode
estourar timeout. O caminho comum é verificar, persistir/enfileirar, responder e
consumir idempotentemente.

## Capítulo 05 — Jobs e checkpoints

Run ID identifica tentativa; job + janela identificam intenção. O atraso do
scheduler não altera a janela civil. Uma lease sem fencing não impede worker antigo
de voltar depois da expiração.

Em paralelismo, max ID concluído não é checkpoint seguro se houver lacuna. Use
watermark contíguo ou ranges confirmados.

## Capítulo 06 — Retry e backpressure

Retry exige causa possivelmente transitória, operação repetível e tempo no deadline.
Full jitter distribui clientes; cap limita espera. Client, biblioteca e job não
devem repetir independentemente sem um orçamento total.

Rate limita inícios; semáforo limita concorrência; fila limitada implementa parte
da backpressure; breaker reduz chamadas durante falha. Um não substitui o outro.

## Capítulo 07 — Concorrência

Para I/O, async ou threads limitadas podem ajudar; para CPU, processos ou recursos
nativos podem ser adequados. O limite vem de medição e do recurso mais estreito.

Criar uma task por item com semáforo ainda materializa tasks. Para grande volume,
use fila limitada e workers fixos. Fail-fast cancela trabalho futuro, mas efeitos
já confirmados continuam no relatório.

## Capítulo 08 — Navegador e documentos

Locators por papel/rótulo e espera por pós-condição resistem melhor que CSS e sleep.
Clique sem confirmação deixa estado incerto.

CSV deve ser gerado por biblioteca e pela política do consumidor. Prefixos de
fórmula exigem tratamento; trocar delimitador ou envolver em aspas não impede
necessariamente interpretação como fórmula.

## Capítulo 09 — Segurança

Entrada permanece dado quando APIs recebem argumentos separados. Ainda assim,
valide tamanho e semântica. Menor privilégio deve existir na credencial, não apenas
na UI.

Segredo em variável de ambiente não é automaticamente seguro. Evite propagar a
filhos e nunca despeje ambiente. O melhor teste usa canário em todas as saídas.

## Capítulo 10 — Observabilidade

JSON só é estruturado quando nomes, tipos e semântica são estáveis. EventName
identifica classe; message é apresentação. Item ID fica no log/trace, não em label
irrestrita de métrica.

Falha do logger precisa de caminho terminal sanitizado. Auditoria essencial pode
exigir outbox ou falha do commit; a escolha deve ser contratual.

## Capítulo 11 — Testes

Teste efeitos por propriedade: segunda execução preserva estado, dry-run não
muta, contagens fecham, caminhos ficam na raiz e falha pré-commit preserva estado.

Use barrier para forçar race, clock/RNG falsos para retry e stream que falha após N
bytes para disco. Sleep e disco cheio real tornam a suíte lenta e instável.

## Capítulo 12 — CI/CD

Cache acelera; artifact transfere resultado; release promove artifact identificado.
Build uma vez e promova o mesmo digest. Código de PR não recebe segredo de release.

OIDC fornece identidade curta, mas a trust policy do provedor precisa restringir
claims. id-token write sozinho não concede acesso ao recurso.

## Capítulo 13 — Distribuição

Versão da aplicação, config, manifesto, dados e plugin API evoluem separadamente.
Versão futura deve ser preservada e recusada. Migração só publica depois de
converter e validar tudo.

O smoke test definitivo executa o artifact em diretório limpo sem checkout. O fim
de vida remove agenda, token, webhook, dados, alerts e ownership.

## Capítulo 14 — Projeto

Uma entrega forte não maximiza features. Ela demonstra invariantes e limites.
Falha parcial precisa aparecer na defesa; se toda demonstração é caminho feliz,
os controles essenciais não foram provados.

## Laboratório 01

O desenho esperado separa Planner e Executor. Operation carrega caminho relativo,
hash, action e reason. A corrida é orquestrada: planeje, crie destino externo e
aplique. Passar significa preservar o arquivo concorrente, não apenas lançar erro.

## Laboratório 02

O fake deve exercitar protocolo real o suficiente para validar headers e corpo. O
job persiste checkpoint depois do sink. Config ou schema divergente impede retomada
mista; uma nova run começa com regra consistente.

## Laboratório 03

O teste de retry injeta sleeper e registra delays. A escolha de workers vem da
curva, não do maior throughput isolado: p95, 429 e memória podem justificar limite
menor. CSV é validado por round-trip e pelo consumidor declarado.

## Laboratório 04

A matriz risco-controle-teste deve apontar para casos executáveis. Canário é
procurado em todos os artifacts, inclusive caminho de erro do logger. O pipeline
produz artifact uma vez e verifica digest antes da promoção.

## Laboratório 05

No game day, não informe a causa; forneça apenas o alerta. A pessoa operadora deve
preservar evidência e localizar a primeira fronteira divergente. O relatório final
separa confirmed de uncertain e inclui melhoria no runbook/teste.

## Perguntas para defesa

1. Qual é o ponto de commit e como ele é testado?
2. Como a mesma intenção é reconhecida depois de reiniciar?
3. Que efeito um cancelamento pode deixar?
4. Como o sistema reage a versão futura?
5. Qual limite evita blast radius ilimitado?
6. Que dado aparece em log e por quê?
7. Como provar que artifact testado é o publicado?
8. Como remover credenciais e agenda no fim de vida?

