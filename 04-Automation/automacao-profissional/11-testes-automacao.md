# 11 — Testes de automação e injeção de falhas

Testar automação não é executá-la em produção e observar. A suíte precisa provar
que efeitos são limitados, repetíveis e recuperáveis, inclusive quando a falha
ocorre entre duas linhas que normalmente passam juntas.

## Objetivos

- separar lógica pura de adapters com efeitos;
- construir testes unitários, de contrato, integração e ponta a ponta;
- injetar relógio, RNG, filesystem, HTTP e falhas;
- testar propriedades como idempotência, reconciliação e determinismo;
- validar CLI, pacote e retomada em ambiente limpo.

## 1. Arquitetura testável

~~~text
CLI/scheduler -> application service -> domain planner
                       |                    |
                       v                    v
                 ports/adapters        tipos imutáveis
~~~

O planejador recebe dados e produz Plan sem rede, relógio global ou escrita. O
executor recebe Plan e ports. Isso permite fake pequeno, não mock de cada detalhe
interno.

Exemplo de porta:

~~~python
from typing import Protocol

class ObjectStore(Protocol):
    def stat(self, key: str): ...
    def put_if_absent(self, key: str, content: bytes): ...

class Clock(Protocol):
    def now(self): ...
    def monotonic(self) -> float: ...
~~~

Injete abstrações onde há não determinismo ou efeito. Não crie interface para uma
soma pura apenas por formalismo.

## 2. Camadas de teste

| Camada | Prova | Exemplo |
|---|---|---|
| unidade | regra e transição | copy/skip/conflict |
| propriedade | invariante em muitos casos | repetir preserva estado |
| contrato | adapter e schema | HTTP/JSON suportado |
| integração | primitiva real controlada | filesystem temporário |
| subprocesso | CLI, canais e códigos | stdout JSON, stderr erro |
| end-to-end | artefato e jornada | instalar, planejar, aplicar |
| resiliência | falha entre etapas | queda após commit |

E2E é valioso, mas caro e pouco preciso para diagnosticar. Use poucos fluxos
essenciais e cubra combinações no núcleo.

## 3. Fixtures

Fixtures devem ser pequenas, sintéticas e explicáveis. Inclua:

- vazio e limite mínimo;
- limite exato e limite + 1;
- Unicode, normalização e newline;
- documento truncado;
- campo ausente, desconhecido e tipo errado;
- versão anterior, atual e futura;
- ID duplicado;
- resposta excessiva e Content-Type errado;
- symlink e colisão quando a plataforma permitir.

Fixture capturada de produção pode carregar dados pessoais mesmo após editar um
campo. Prefira gerar do contrato. Se gravar resposta externa, sanitize antes do
commit e mantenha nota de proveniência.

## 4. Fakes, stubs e mocks

- stub devolve resposta programada;
- fake implementa comportamento simplificado, como store em memória;
- spy registra chamadas;
- mock impõe expectativa de interação.

Teste resultado e invariante antes de acoplar à ordem de métodos internos. Mock
excessivo permite que implementação e teste compartilhem o mesmo erro. Para
adapter HTTP, um servidor fake realista encontra problemas de serialização que um
mock do client não vê.

## 5. Propriedades essenciais

### Idempotência

~~~text
state_after_once == state_after_twice
~~~

Compare estado e efeitos de negócio, não timestamps de auditoria.

### Dry-run

O plano é o mesmo; contagem de mutações é zero. Um adapter sentinela falha se
put, delete, mkdir, checkpoint ou audit mutável forem chamados.

### Reconciliação

Todo item termina em exatamente um outcome. Gere sequências com sucesso, skip,
falha, cancelamento e estado incerto.

### Confinamento

Todo destino pertence à raiz autorizada. Gere segmentos com ponto-ponto, absoluto,
separadores alternativos e Unicode.

### Determinismo

Mesma entrada, clock e RNG produzem os mesmos bytes. Rode em ordem de descoberta
diferente para detectar dependência acidental.

## 6. Fault injection

Crie failpoints antes e depois de cada commit:

~~~text
1 descobrir
2 calcular hash
3 criar temporário
4 copiar bytes
5 validar temporário
6 publicar
7 registrar resultado
8 avançar checkpoint
~~~

Para cada ponto, pergunte: o que ficou visível? O que será repetido? Existe lixo
temporário? O relatório é verdadeiro? Uma matriz evita testar apenas “falha de rede”.

Simule disco cheio por adapter/stream que falha após N bytes, não enchendo o disco
real. Simule timeout com clock controlado, não sleep longo.

## 7. Concorrência determinística

Testes com sleep raramente forçam o interleaving desejado. Use barriers/latches:

~~~text
worker A valida destino ausente -> pausa
worker B cria destino -> sinaliza
worker A tenta publicar -> deve recusar sem sobrescrever
~~~

Teste limite de concorrência com contador atômico de ativos e maxObserved. Teste
cancelamento bloqueando uma dependência falsa até o sinal.

## 8. Testes de processo e CLI

Execute como subprocesso e afirme simultaneamente:

- código exato;
- stdout parseável ou vazio;
- stderr significativo;
- nenhum efeito parcial proibido;
- help funciona sem configurar dependências;
- sinais/cancelamento seguem contrato;
- caminho de trabalho diferente não quebra recursos empacotados.

Não teste JSON com substring; parseie e valide estrutura.

## 9. Ambientes temporários

Cada teste cria diretório isolado e o remove por cleanup mesmo ao falhar. Não use
home, raiz do repositório ou diretório compartilhado como alvo. Para integração
externa, use conta/tenant de teste e nomes únicos com expiração.

Uma suíte paralela não pode compartilhar porta fixa, arquivo ou chave. Reserve
recursos pelo sistema e passe-os ao teste.

## 10. Golden, snapshot e aprovação

Golden file funciona para saída determinística. Uma atualização automática de
snapshot não é prova; revise o diff e explique a mudança. Remova timestamps ou
injete valores fixos. Combine snapshot com invariantes para evitar aprovar saída
completa por acidente.

## 11. Cobertura de risco

Cobertura de linha não mede proteção de efeito. Mantenha uma matriz:

| Risco | Controle | Teste | Evidência |
|---|---|---|---|
| sobrescrita | criação exclusiva | corrida orquestrada | destino preservado |
| duplicata | chave idempotente | timeout pós-commit | um efeito |
| vazamento | allowlist de log | canário | busca vazia |
| perda | checkpoint pós-commit | kill/restart | todos reconciliados |

## Falhas e diagnóstico

| Sintoma | Causa | Melhoria |
|---|---|---|
| passa local, falha CI | dependência global/tempo | ambiente limpo e injeção |
| teste flaky | sleep e recurso compartilhado | coordenação explícita |
| mocks passam, integração falha | protocolo não exercitado | fake server/adapter real |
| snapshot enorme muda | campos variáveis | modelo canônico |
| cobertura alta, sobrescrita | risco sem teste | matriz risco-controle |

## Exercícios

### Nível 1 — propriedades

Teste idempotência, dry-run e reconciliação. **Aceite:** um defeito proposital em
cada propriedade faz o teste correto falhar.

### Nível 2 — falhas

Injete falha em cada fronteira do FileFlow. **Aceite:** versão anterior é preservada,
temporários são tratados e relatório não mente.

### Nível 3 — artefato

Instale em diretório limpo e rode E2E. **Aceite:** funciona fora do checkout,
com configuração mínima, e produz evidência reproduzível.

## Checklist

- [ ] Núcleo de decisão não depende de efeitos globais.
- [ ] Fixtures cobrem limites e versões, sem dados reais.
- [ ] Falhas antes/depois do commit são injetadas.
- [ ] Concorrência é coordenada sem sleep arbitrário.
- [ ] CLI é testada como subprocesso.
- [ ] A matriz de riscos aponta para testes reais.

