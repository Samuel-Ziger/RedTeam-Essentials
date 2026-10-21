# 11 — Logs, diagnóstico e observabilidade sem dados sensíveis

Uma aplicação distribuída a usuários precisa explicar por que falhou sem exigir
acesso irrestrito ao ambiente nem coletar tudo “por precaução”. Observabilidade é
a capacidade de inferir o estado relevante do produto a partir de sinais
planejados. Logs são um desses sinais; métricas, rastros, verificações internas e
relatos da pessoa completam o diagnóstico.

No [Study Desk](projetos/study-desk/README.md), os dados principais são títulos,
datas e hábitos de estudo. Eles podem ser pessoais e não precisam aparecer em um
log para responder “a migração falhou?” ou “qual versão do schema foi recebida?”.
O desenho correto registra a **classe da operação e seu resultado**, não o
conteúdo da pessoa.

## Objetivos verificáveis

Ao concluir, você deverá conseguir:

1. definir perguntas operacionais antes de criar eventos;
2. produzir logs estruturados com schema, nível e campos estáveis;
3. correlacionar UI, caso de uso e adaptador com IDs efêmeros;
4. classificar e remover segredos e dados pessoais antes do sink;
5. distinguir logs, métricas, rastros e pacotes de diagnóstico;
6. definir retenção, rotação, consentimento e controle da pessoa;
7. diagnosticar falhas por hipótese, reprodução mínima e evidência;
8. testar a telemetria como qualquer outra saída da aplicação.

## Pré-requisitos e modelo mental

Você deve conhecer erros tipados, estado, persistência e clientes de API dos
capítulos anteriores. Não é necessário administrar coletores ou infraestrutura;
esse assunto pertence a módulos próprios. Aqui, observamos o que a aplicação
produz e como ela protege a pessoa.

```text
pergunta de suporte
  -> evento necessário
  -> campos mínimos e tipos
  -> classificação de sensibilidade
  -> filtragem/redaction
  -> sink local ou telemetria consentida
  -> retenção e descarte
  -> consulta que confirma ou rejeita hipótese
```

Se ninguém consegue dizer que decisão um campo permitirá tomar, não o colete.
Mais dados podem piorar o diagnóstico: aumentam ruído, custo, risco e dificuldade
para localizar o sinal útil.

## Comece por perguntas, não por mensagens

Transforme necessidades de suporte em perguntas verificáveis:

- qual versão da aplicação e do schema tentou importar o arquivo?
- em qual etapa a operação parou: leitura, parse, validação, migração ou gravação?
- o erro é recorrente na mesma versão?
- quantas operações ficaram pendentes após reinício?
- a falha é de entrada inválida, limitação conhecida ou defeito interno?
- a interface apresentou um código de suporte correspondente ao evento?

Depois desenhe eventos que respondem a essas perguntas. “Deu erro aqui” é uma
mensagem humana instável. Um evento estruturado permite filtro e agregação:

```json
{
  "timestamp": "2026-10-05T18:30:00Z",
  "level": "error",
  "event": "document_import_failed",
  "schemaVersion": 1,
  "appVersion": "3.0.0",
  "operationId": "op-a19f",
  "stage": "validation",
  "reason": "unsupported_document_schema",
  "receivedSchema": 7,
  "maximumSupportedSchema": 5,
  "durationMs": 18
}
```

Não há caminho completo, nome do arquivo, título de sessão nem documento. O evento
ainda responde onde e por que a importação falhou.

## Schema de evento e estabilidade

Defina um envelope comum:

| Campo | Função | Regra |
|---|---|---|
| `timestamp` | instante do evento | UTC em formato canônico |
| `level` | severidade | enumeração pequena |
| `event` | tipo estável | `snake_case`, não frase traduzida |
| `schemaVersion` | versão do evento | inteiro evoluído conscientemente |
| `appVersion` | origem | versão pública do produto |
| `operationId` | correlação efêmera | aleatório, sem PII |
| campos específicos | contexto mínimo | tipos e limites documentados |

Mensagens humanas podem complementar o evento para uso local, mas não substituem
campos. Não use a mensagem como chave de painel ou teste; ela muda com revisão e
idioma. Enumerações como `unsupported_document_schema` são mais estáveis.

Evolua schemas de forma compatível: adicionar campo opcional costuma ser simples;
renomear, mudar tipo ou semântica exige nova versão. Defina limites para strings e
coleções. Um erro que inclui recursivamente a resposta inteira quebra minimização
e pode tornar o próprio logger uma fonte de falha.

## Níveis são um contrato de atenção

- `debug`: detalhe de desenvolvimento ativado de forma controlada;
- `info`: marco operacional útil, como migração concluída;
- `warning`: degradação recuperável ou condição futura que pede atenção;
- `error`: uma operação solicitada não foi concluída;
- `critical`: aplicação ou integridade de dados essenciais está em risco.

Uma validação esperada da pessoa não precisa ser `error`; pode nem precisar de
log. Registrar cada clique ou campo inválido como erro cria alarme falso. Em
contrapartida, engolir uma falha de persistência e mostrar sucesso é grave.

O nível depende do impacto observado, não da classe de exceção. Uma exceção usada
internamente para fluxo controlado pode virar resultado de validação; uma resposta
aparentemente “normal” que confirma perda de dados pode ser crítica.

## Implementação estruturada e testável

Este logger JavaScript recebe um sink e uma função de relógio, limita campos e
redige chaves proibidas. Em produção, a lista deve vir de uma política central:

```javascript
const SENSITIVE_KEYS = /token|password|secret|cookie|authorization/i;
const LEVELS = new Set(["debug", "info", "warning", "error", "critical"]);
const RESERVED_FIELDS = new Set([
  "timestamp", "schemaVersion", "appVersion", "level", "event"
]);

export function createLogger({
  sink,
  appVersion,
  now = () => new Date(),
  fallback = () => {},
}) {
  if (typeof sink !== "function") throw new TypeError("sink deve ser função");
  if (typeof fallback !== "function") throw new TypeError("fallback deve ser função");
  if (typeof appVersion !== "string" || appVersion.length === 0) {
    throw new TypeError("appVersion é obrigatória");
  }
  return function log(level, event, fields = {}) {
    if (!LEVELS.has(level)) throw new TypeError(`nível inválido: ${level}`);
    if (!/^[a-z][a-z0-9_]{0,63}$/.test(event)) {
      throw new TypeError(`evento inválido: ${event}`);
    }

    const safeFields = {};
    for (const [key, value] of Object.entries(fields)) {
      if (RESERVED_FIELDS.has(key)) {
        throw new TypeError(`campo reservado: ${key}`);
      } else if (SENSITIVE_KEYS.test(key)) {
        safeFields[key] = "[REDACTED]";
      } else if (typeof value === "string") {
        safeFields[key] = value.slice(0, 256);
      } else if (["number", "boolean"].includes(typeof value) || value === null) {
        safeFields[key] = value;
      }
    }

    const timestamp = now();
    if (!(timestamp instanceof Date) || !Number.isFinite(timestamp.getTime())) {
      throw new TypeError("relógio inválido");
    }
    const entry = {
      ...safeFields,
      timestamp: timestamp.toISOString(),
      schemaVersion: 1,
      appVersion,
      level,
      event,
    };
    try {
      sink(entry);
      return true;
    } catch (error) {
      try {
        fallback({
          event: "logger_sink_failed",
          originalEvent: event,
          reason: error instanceof Error ? error.name : "unknown",
        });
      } catch {
        // O fallback é terminal: não chama o logger e não tenta de novo.
      }
      return false;
    }
  };
}

const events = [];
const discarded = [];
const log = createLogger({
  sink: (entry) => events.push(entry),
  fallback: (failure) => discarded.push(failure),
  appVersion: "1.1.0",
  now: () => new Date("2026-10-05T18:30:00Z"),
});

log("error", "session_save_failed", {
  operationId: "op-42",
  reason: "storage_unavailable",
  token: "must-not-appear",
});
```

Campos reservados são rejeitados e o envelope é gravado por último; assim um
chamador não consegue trocar `level`, `event`, versão ou timestamp por meio de
`fields`. Em um produto, use também uma allowlist por tipo de evento: a redação
por nome reduz risco, mas não reconhece conteúdo sensível colocado sob uma chave
aparentemente inocente.

Configuração inválida, evento fora do contrato e relógio inválido continuam
falhando cedo como erros de programação. Depois que o logger foi construído, uma
falha operacional do sink retorna `false` e aciona um fallback mínimo, sem
conteúdo do evento. O fallback é terminal e sua própria falha é contida para
evitar recursão. Em desenvolvimento, testes do sink devem continuar expondo seus
defeitos; contenção em runtime não substitui correção.

O exemplo ensina injeção e filtragem, mas uma expressão por nome não é defesa
suficiente. Um segredo pode aparecer em `value`, URL ou mensagem. A política real
deve permitir apenas campos conhecidos por tipo de evento (**allowlist**) e
redaction adicional como rede de segurança.

Nunca construa o objeto perigoso, envie ao sink e tente apagar depois. O sink pode
ter serializado, copiado ou transmitido o valor. Filtre antes. Se o próprio logger
falhar, ele não deve quebrar a operação principal nem entrar em recursão infinita;
use fallback mínimo e contador de descarte.

## Classificação e minimização de dados

Antes de registrar, classifique:

| Classe | Exemplos | Política típica |
|---|---|---|
| segredo | senha, token, cookie, chave | nunca registrar |
| conteúdo pessoal | título, nota, documento | não registrar por padrão |
| identificador estável | e-mail, ID de conta | evitar, pseudonimizar só com propósito |
| contexto técnico | versão, schema, etapa | permitido quando necessário |
| agregado | contagem de falhas | permitido com retenção e limiar adequados |

Hash não torna automaticamente um identificador anônimo. Valores de domínio
pequeno podem ser reidentificados, e um hash estável ainda rastreia a mesma pessoa.
Se correlação permanente não é necessária, use um ID aleatório por operação ou
sessão de suporte.

Caminhos de arquivo podem conter nome de usuário e estrutura pessoal. Registre
apenas categoria, extensão validada, tamanho em faixa ou nome lógico. URLs podem
conter query e credencial; se o destino é relevante, registre uma rota canônica ou
origem aprovada, não a string integral.

Mensagens de exceção de bibliotecas também podem conter entrada. Prefira mapear
tipo/código para `reason` conhecido. Stack traces ficam restritos ao diagnóstico
local controlado e passam pela mesma revisão de sensibilidade.

## Correlação sem rastreamento permanente

Um `operationId` acompanha uma ação da UI ao caso de uso e ao adaptador:

```text
UI: import_started       operationId=op-a19f
use case: migration_run  operationId=op-a19f from=4 to=5
repository: save_failed  operationId=op-a19f reason=quota_exceeded
UI: feedback_presented   operationId=op-a19f supportCode=SD-104
```

O identificador deve ser opaco, imprevisível e efêmero. Não derive de e-mail,
título ou caminho. Mostre um código curto de suporte que permita encontrar o
evento localmente, mas não exponha detalhes internos na mensagem à pessoa.

Quando uma operação chama suboperações, use IDs de correlação e relação pai/filho
se isso responde a uma pergunta real. Não modele um sistema de rastreamento
complexo para uma aplicação local pequena. Para o Study Desk, um ID por importação
ou exportação é suficiente.

## Logs, métricas, rastros e verificações

- **log:** fato discreto com contexto, como migração rejeitada;
- **métrica:** medida agregada ao longo do tempo, como taxa de falha por versão;
- **rastro:** relação temporal entre etapas de uma operação;
- **verificação interna:** teste de integridade, versão e capacidade;
- **relato:** descrição da pessoa, passos e resultado percebido.

Cada sinal responde perguntas diferentes. Uma métrica detecta aumento de falhas,
mas não explica um caso específico. Um log detalha o caso, mas não revela sozinho
se ele é comum. Um rastro mostra onde o tempo foi gasto, sem necessariamente dizer
se a interface era compreensível.

Métricas de produto precisam estar ligadas a decisões: taxa de conclusão da
jornada, falha de migração por versão, tempo até feedback e recuperação após erro.
“Total de cliques” é frequentemente uma vanity metric e pode incentivar coleta
invasiva. Declare propósito, unidade, dimensões permitidas e ação quando ultrapassa
um limiar.

Evite dimensões de alta cardinalidade, como título ou ID de operação, em métricas.
Elas aumentam custo e podem carregar dados pessoais. IDs pertencem a logs/rastros
com retenção controlada, não a rótulos de série temporal.

## Pacote de diagnóstico sob controle da pessoa

Quando suporte exige mais contexto, gere um pacote local com consentimento
explícito. Um contrato seguro inclui:

1. explicar por que o pacote ajuda;
2. mostrar exatamente quais arquivos e campos serão incluídos;
3. filtrar segredos e conteúdo pessoal antes de montar;
4. oferecer prévia legível;
5. permitir salvar localmente, sem envio automático;
6. atribuir validade curta e orientar exclusão;
7. incluir manifesto com versão e hashes dos componentes.

Conteúdo útil:

- versão da aplicação, formato e schema;
- plataforma em granularidade suficiente, sem nome da máquina;
- configuração não sensível e origem de cada valor;
- últimos eventos filtrados por tamanho e tempo;
- resultado de verificações internas;
- contagem de registros, não os títulos;
- passos informados voluntariamente pela pessoa.

O pacote não deve incluir armazenamento completo por conveniência. Se uma amostra
de documento for indispensável, gere uma versão sintética ou ofereça seleção
explícita separada com alerta claro.

## Retenção, rotação, consentimento e modo debug

Dados locais também precisam de ciclo de vida. Defina tamanho máximo, quantidade
de arquivos, idade, comportamento quando o limite é atingido e remoção na
desinstalação. Rotação evita crescimento ilimitado; não deve apagar a única
evidência antes de uma falha ser apresentada.

Telemetria externa requer base legítima, transparência e controles coerentes com
o contexto. Mesmo quando consentimento não é o mecanismo aplicável, minimização e
retenção continuam essenciais. A pessoa deve saber se há coleta, quais categorias,
como desativar quando oferecido e como solicitar exclusão quando pertinente.

Modo debug aumenta detalhe por tempo limitado. Ele precisa de expiração,
indicador visual e política ainda mais rigorosa de dados. Nunca permita que “debug”
desative redaction de segredos. Ao terminar, retorne automaticamente ao nível
normal.

## As cinco linguagens e a mesma disciplina

| Linguagem | Mecanismo possível | Como manter testável |
|---|---|---|
| Python | `logging` com formatter/adapter | handler em memória e relógio injetado |
| Java | facade/API de logging escolhida | appender fake e objetos de evento |
| C | função de logger + contexto | sink por ponteiro de função e structs limitadas |
| C# | `ILogger` e logging estruturado | provider em memória e scopes |
| JavaScript | função estruturada e sink | array sink/spy e clock injetado |

Evite interpolar segredo antes da filtragem. APIs estruturadas devem receber
template estável e campos tipados. Em C, trate tamanho e retorno de formatação; um
logger não pode causar overflow. Em qualquer linguagem, valide que exceções não
serializam objetos enormes ou cíclicos.

## Método de diagnóstico por hipótese

Quando chega um relato “não consigo importar”, siga um processo:

1. defina o resultado esperado e observado;
2. obtenha versão, código de suporte e passos mínimos;
3. formule hipóteses ordenadas por evidência e impacto;
4. reproduza com dados sintéticos e mesma versão de schema;
5. encontre a primeira transição divergente;
6. injete falha no limite suspeito;
7. corrija a causa e adicione teste de regressão;
8. valide que novos eventos explicam a classe de falha sem expor dados.

Não altere cinco componentes ao mesmo tempo. Compare um caso que funciona com o
menor caso que falha. Inspecione entrada e saída de cada fronteira usando metadados
seguros. A observabilidade deve reduzir o espaço de busca, não substituir leitura
do contrato.

## Falhas frequentes e diagnóstico

| Sintoma | Causa provável | Correção |
|---|---|---|
| logs enormes e inúteis | evento por clique/objeto inteiro | perguntas, allowlist e amostragem |
| token aparece mascarado tarde | filtragem depois do sink | redaction antes de construir/enviar |
| não é possível unir etapas | ausência de operation ID | correlação efêmera propagada |
| painel quebra após release | mensagem usada como schema | evento/campos versionados |
| métrica custa muito | dimensão de alta cardinalidade | agregação e dimensões finitas |
| suporte pede banco completo | pacote sem desenho | manifesto, prévia e dados mínimos |
| modo debug fica permanente | ativação sem prazo | expiração e indicador visível |

Uma falha silenciosa do sink também merece contador interno limitado. Se o disco
ou armazenamento estiver indisponível, a aplicação não deve entrar em loop ao
tentar registrar que não conseguiu registrar.

## Exercícios em três níveis

### Nível 1 — Eventos estruturados

Converta cinco mensagens textuais do Study Desk em eventos tipados. Implemente o
logger do exemplo com allowlist por evento e testes de redaction.

**Critérios de aceite:** eventos têm schema e níveis coerentes; relógio é
determinístico; senha, token, título, caminho e corpo são rejeitados ou redigidos
antes do sink; strings têm limite; mensagem humana não é usada como chave.

### Nível 2 — Correlação e pacote local

Correlacione importação desde o clique até persistência. Injete falhas em leitura,
schema, migração e gravação. Gere um pacote com manifesto e prévia.

**Critérios de aceite:** cada falha tem `reason` distinguível; um ID efêmero une as
etapas; feedback mostra código de suporte; pacote contém versão, verificações e
eventos mínimos; nada é enviado automaticamente; títulos e documentos não
aparecem; testes verificam o conteúdo do arquivo gerado.

### Nível 3 — Plano de observabilidade do produto

Defina três perguntas operacionais, eventos, métricas e política de retenção para
uma versão sincronizável do Study Desk. Simule um aumento de falha de migração e
documente o diagnóstico até o teste de regressão.

**Critérios de aceite:** cada campo justifica uma decisão; métricas não usam alta
cardinalidade; modo debug expira; consentimento/controle está documentado; alerta
leva a um runbook; investigação usa dados sintéticos; correção adiciona evento ou
teste somente quando melhora uma pergunta real.

## Checklist de conclusão

- [ ] Cada evento responde a uma pergunta de operação ou suporte.
- [ ] Logs possuem envelope, tipos, níveis e schema versionado.
- [ ] Mensagens humanas não substituem campos estáveis.
- [ ] Segredos e conteúdo pessoal são bloqueados antes do sink.
- [ ] IDs de correlação são opacos, efêmeros e sem PII.
- [ ] Logs, métricas, rastros e verificações têm papéis distintos.
- [ ] Métricas evitam dimensões de alta cardinalidade.
- [ ] Retenção, rotação, descarte e modo debug têm limites.
- [ ] Pacote de diagnóstico oferece prévia e não é enviado automaticamente.
- [ ] Testes tratam observabilidade como saída funcional da aplicação.
