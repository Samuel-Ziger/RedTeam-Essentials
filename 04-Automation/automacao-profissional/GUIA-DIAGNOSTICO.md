# Guia de diagnóstico — Automações e jobs

Diagnosticar é encontrar a primeira fronteira em que o observado diverge do
contrato, preservando evidência. Reexecutar imediatamente pode duplicar efeitos e
apagar a causa.

## Antes de repetir

1. registre job/run ID, janela lógica, versão e digest do plano;
2. preserve manifesto, relatório, checkpoint e primeira falha;
3. classifique itens confirmados, pendentes, incertos e falhos;
4. redija segredos e conteúdo pessoal;
5. verifique se repetir é idempotente;
6. reproduza com fixture em ambiente descartável;
7. altere uma variável por experimento.

Não limpe diretório, fila, dead-letter ou checkpoint antes de copiar o estado.
“Funcionou depois” não identifica a causa.

## Registro mínimo

~~~text
job/run ID e janela:
versão do app/config/schema:
gatilho e comando:
entrada sintética ou digest:
plano/digest:
resultado esperado:
primeira divergência:
efeitos confirmados:
itens incertos:
checkpoint:
hipótese:
experimento de uma variável:
~~~

## Árvore de triagem

~~~text
o gatilho criou a execução?
├─ não -> agenda, deadline, suspensão, permissão
└─ sim -> a entrada foi descoberta e validada?
   ├─ não -> raiz, tamanho, encoding, schema, versão
   └─ sim -> o plano corresponde ao estado?
      ├─ não -> regra, cache, ordem, clock, config
      └─ sim -> o efeito foi tentado?
         ├─ não -> aprovação, lease, rate, cancelamento
         └─ sim -> foi confirmado?
            ├─ não -> failed ou uncertain; reconciliar
            └─ sim -> relatório/checkpoint registraram?
               ├─ não -> evidência parcial, não repetir cegamente
               └─ sim -> verificar resumo e pós-condição
~~~

## Dry-run diferente do apply

Compare digest do plano, configuração efetiva e estado observado. Verifique se o
executor recalcula regras ou se houve mudança entre check e use. Dry-run deve usar
o mesmo planejador e apply deve revalidar pré-condições.

Experimento: execute planner duas vezes com clock/RNG fixos, compare bytes e use
adapter sentinela. Se o dry-run cria audit, diretório ou checkpoint, ele tem efeito.

## Arquivos e integridade

Diagnostique na ordem: raiz → caminho relativo → tipo/lstat → tamanho → bytes
→ hash → temporário → publicação. Preserve fonte e destino; trabalhe em cópia.

| Sintoma | Verifique |
|---|---|
| destino fora da raiz | componentes e symlinks |
| colisão tardia | criação exclusiva e TOCTOU |
| hash divergente | fonte mudou durante cópia |
| arquivo pela metade | publicação não atômica |
| nome muda por SO | case, normalização e reservado |

## Pipeline e contagens

Reconstrua recebidos, aceitos, rejeitados, publicados, duplicados, pendentes e
falhos. Uma categoria ausente é a causa mais comum de contagem que não fecha.
Verifique a definição de cabeçalho, linha vazia e filtro.

Se o resultado muda, fixe ordem, locale, clock, RNG e versão. Compare o primeiro
registro divergente, não apenas o hash final.

## HTTP e webhook

Registre endpoint lógico, método, attempt, timeout, status/classe, content-type,
tamanho e request ID, sem URL assinada, token ou corpo.

- transporte falhou antes da resposta: retry apenas se semântica permitir;
- timeout após escrita: uncertain e reconcile;
- 200 com parse falho: valide tipo, tamanho e schema;
- 429: interprete Retry-After dentro do deadline;
- webhook inválido: bytes brutos, key ID, timestamp e replay store.

## Job duplicado ou travado

Compare janela lógica e chave; run IDs devem diferir entre tentativas. Para
sobreposição, observe owner, expiração e fencing token. Lock local não explica dois
hosts.

Heartbeat sem progresso aponta para espera ou deadlock. Colete lastProgressAt,
fase, fila, conexões e dump seguro. Não renove lease indefinidamente de um job que
não progride.

## Retry e sobrecarga

Desenhe a árvore de tentativas por camada. Multiplique client retry, job retry e
replay. Procure sincronização de delays quando falta jitter.

Meça fila e idade, não só CPU. Mais workers podem piorar rate limit e p95. Reduza
concorrência como experimento, mantendo o mesmo conjunto.

## Concorrência

Para race, substitua sleep por barrier e force a ordem. Registre item, partição,
owner e fase. Resultado fora de ordem não é perda se o relatório ordena por ID;
checkpoint saltando lacuna é perda potencial.

Ao cancelar, separe queued, running, committing, confirmed e uncertain. Cancelled
não deve encobrir efeito confirmado.

## Segredos e artifacts

Se houve vazamento, preserve acesso restrito, revogue/rotacione primeiro e depois
investigue alcance. Remover do log não invalida cópias. Procure o canário em todos
os sinks, caches, screenshots e artifacts.

Não anexe diretório completo ao chamado. Gere bundle por allowlist e mostre prévia.

## CI/CD

Anote commit, workflow, runner, toolchain e digest do artifact. Se local passa e CI
falha, compare ambiente limpo, locale, timezone, permissões e dependência global.
Se o deploy difere do testado, compare digests: reconstrução é uma hipótese forte.

Para release concorrente, identifique qual run possui o ambiente. Cancelar workflow
não garante rollback; consulte estado real e versão implantada.

## Encerramento

Um diagnóstico termina quando há:

- causa demonstrada;
- impacto e efeitos confirmados;
- recuperação verificada;
- teste que falhava antes e passa depois;
- invariantes anteriores ainda verdes;
- ação preventiva e owner.

~~~text
mesma fixture + ambiente controlado
-> falha reproduzível
-> mudança explicada
-> sucesso reproduzível
-> reconciliação verdadeira
~~~

