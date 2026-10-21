# 16 — Observabilidade, SLI e SLO

Uma API observável permite explicar seu comportamento por sinais externos sem
registrar dados sensíveis. Logs contam eventos, métricas mostram tendência e
traces conectam trabalho distribuído. Nenhum sinal isolado substitui os outros.

## Objetivos

- instrumentar RED e dependências;
- projetar logs estruturados seguros;
- propagar contexto de trace/correlação;
- definir SLI, SLO e error budget;
- criar alertas por sintomas e runbooks acionáveis.

## 1. Eventos, métricas e traces

**Logs** registram ocorrência discreta com contexto. **Métricas** agregam valores
de baixa cardinalidade. **Traces** representam caminho e duração de uma
solicitação por spans.

OpenTelemetry define semantic conventions para nomes e atributos; em outubro de
2026 a versão publicada das convenções é 1.44.0 e algumas áreas ainda têm status
misto. Fixe a versão adotada e planeje migração, em vez de misturar atributos
antigos e novos.

## 2. RED e USE

Para cada operação:

- Rate: requisições por tempo;
- Errors: falhas relevantes ao consumidor;
- Duration: distribuição de latência.

Para recursos:

- Utilization;
- Saturation;
- Errors.

Separe 4xx esperado, rejeição por política e 5xx. Métrica com path contendo ID
explode cardinalidade; use route template. Tenant/user/item também não deve virar
label irrestrito.

## 3. Log estruturado

~~~json
{
  "event": "item.update.denied",
  "severity": "INFO",
  "request_id": "req_123",
  "trace_id": "abc",
  "action": "item:update",
  "reason": "wrong_tenant",
  "policy_version": "2026-10"
}
~~~

Use schema e nomes estáveis. Não registre token, cookie, senha, segredo, corpo
inteiro ou PII sem finalidade. Escape quebra de linha, limite tamanho e aplique
redação antes do sink. Teste com canário secreto.

Request ID ajuda suporte; trace ID conecta spans. Aceite ID externo somente com
validação/tamanho e gere um interno quando inválido. Correlação não autentica.

## 4. Tracing

Crie span servidor por rota e cliente por dependência. Propague contexto apenas
para destinos confiáveis e não inclua baggage sensível. Registre status e
error.type conforme convenção. Sampling preserva custo, mas erros e operações
raras podem exigir política adaptativa.

Span não deve armazenar payload. Eventos de domínio importantes pertencem à
auditoria ou log estruturado, com controles próprios.

## 5. SLI e SLO

SLI é medida; SLO é alvo; error budget é a tolerância. Exemplo:

~~~text
SLI: operações GET válidas respondidas 2xx/404 em <= 300 ms
denominador: todas as GET autenticadas aceitas pelo limite
janela: 30 dias rolling
SLO: 99,9%
fonte: métrica no ingress validada contra logs
~~~

Defina exatamente exclusões. Excluir todo 5xx durante incidente falsifica o
indicador. Medição no servidor não captura falha antes dele; combine perspectiva
de borda/cliente quando necessário.

Error budget orienta velocidade de mudança. Burn rate mede consumo rápido ou
lento e produz alertas mais úteis que “um erro ocorreu”.

## 6. Alertas e runbooks

Alerta deve indicar sintoma do consumidor, severidade e ação. Exemplos:

- burn rate alto em janela curta e longa;
- p99 acima do objetivo com volume relevante;
- fila envelhecendo;
- taxa de 401 ou 403 muda anormalmente;
- eventos outbox pendentes ultrapassam janela.

Runbook contém impacto, dashboards, hipóteses, consultas seguras, mitigação,
escalonamento, comunicação, rollback e encerramento. Teste o runbook em game day.

## 7. Auditoria

Auditoria responde quem fez o quê, sobre qual recurso, quando, com qual resultado
e justificativa. Requer integridade, retenção e acesso diferentes do log de debug.
Não registre mais dados que o necessário. Falha do sink de auditoria precisa de
política: bloquear ação de alto risco, buffer durável ou degradar explicitamente.

## Falhas comuns

| Falha | Resultado | Correção |
|---|---|---|
| ID em label | custo/cardinalidade | route e dimensões limitadas |
| payload em trace | vazamento | atributos mínimos |
| SLO sem denominador | número manipulável | definição completa |
| alerta por causa interna | ruído | sintoma/burn rate |
| log e auditoria iguais | retenção/acesso errados | canais distintos |

## Exercícios

### Nível 1 — esquema

Defina eventos para sucesso, negação e falha. **Aceite:** correlação existe e
nenhum dado sensível aparece.

### Nível 2 — SLO

Escreva dois SLIs e calcule budget mensal. **Aceite:** numerador, denominador,
janela, fonte e exclusões são inequívocos.

### Nível 3 — game day

Injete dependência lenta e backlog de outbox. **Aceite:** alerta dispara por
sintoma, operador segue runbook e valida recuperação.

## Checklist

- [ ] Métricas usam dimensões de baixa cardinalidade.
- [ ] Logs têm schema, redação e limite.
- [ ] Traces seguem convenção versionada.
- [ ] SLO possui numerador, denominador, janela e fonte.
- [ ] Alertas medem sintoma e burn rate.
- [ ] Auditoria tem política própria e foi testada.

