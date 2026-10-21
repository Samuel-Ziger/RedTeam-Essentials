# JavaScript: da linguagem ao navegador e ao Node.js

JavaScript é a linguagem ECMAScript executada dentro de um **host**. O host
define as APIs ao redor dela:

- o navegador fornece DOM, eventos, armazenamento e várias Web APIs;
- Node.js fornece filesystem, processos, streams e módulos próprios;
- outros runtimes podem oferecer superfícies diferentes.

`Array`, `Promise` e `Map` pertencem à linguagem. `document`, `fetch`, `process`
e `readFile` dependem do ambiente. Separar esses conceitos evita código que só
funciona “por acidente” em um host.

## 1. Toolchain e execução

Para o exemplo deste curso:

```bash
node --version
node programa.mjs
node --check programa.mjs
node --test
```

Arquivos `.mjs` usam ES Modules. Em um projeto npm, `.js` também pode ser ESM
quando `package.json` contém `"type": "module"`.

```javascript
// saudacao.mjs
export function greet(name) {
  return `Olá, ${name}!`;
}

// main.mjs
import { greet } from "./saudacao.mjs";
console.log(greet("Ada"));
```

No navegador, carregue um módulo com `<script type="module" src="main.js">`.
Módulos têm escopo próprio, usam modo estrito e são carregados uma vez por URL.

Se usar npm:

```bash
npm init -y
npm pkg set type=module scripts.test="node --test"
npm install --package-lock-only
npm test
npm ci
```

O segundo comando cria um script de teste real; o script padrão gerado apenas
por `npm init` falharia intencionalmente. Versione `package.json` e o
lockfile. `npm ci` exige esse lockfile e instala exatamente o grafo registrado.
Cada dependência aumenta superfície de atualização e risco; a base deste módulo
não requer pacotes externos.

## 2. Valores, variáveis e tipos

```javascript
const name = "Ana";     // string
let attempts = 0;       // number
const active = true;    // boolean
const missing = null;   // ausência intencional
let pending;            // undefined
```

Use `const` por padrão; ele impede reatribuir o nome, não congela o objeto:

```javascript
const task = { title: "Estudar", done: false };
task.done = true;       // permitido
// task = {};           // TypeError
```

Use `let` quando a reatribuição fizer parte do algoritmo. Evite `var`: seu
escopo de função e hoisting tornam o fluxo menos previsível.

Os tipos primitivos são `undefined`, `null`, `boolean`, `number`, `bigint`,
`string` e `symbol`. Todo o restante é objeto, inclusive arrays e funções.

```javascript
typeof 1;               // "number"
typeof "texto";         // "string"
typeof null;            // "object" (legado histórico)
Array.isArray([]);       // true
```

## 3. Números, texto e coerção

`number` segue ponto flutuante IEEE 754. Inteiros são exatos apenas até
`Number.MAX_SAFE_INTEGER`:

```javascript
Number.isSafeInteger(9_007_199_254_740_991); // true
Number.isFinite(10);                         // true
Number.isFinite("10");                       // false
```

`BigInt` representa inteiros maiores, mas não se mistura implicitamente com
`number` e não é serializado por `JSON.stringify` sem uma estratégia definida.

Conversões devem ocorrer na fronteira:

```javascript
function parsePort(text) {
  if (typeof text !== "string" || !/^\d+$/.test(text)) {
    throw new TypeError("port must contain decimal digits");
  }
  const port = Number(text);
  if (!Number.isInteger(port) || port < 1 || port > 65_535) {
    throw new RangeError("port must be between 1 and 65535");
  }
  return port;
}
```

`Number("")` resulta em zero, e `parseInt("10px", 10)` resulta em 10. Essas
regras podem ser úteis, mas são perigosas para validação estrita.

Prefira `===` e `!==`:

```javascript
0 == false;             // true: houve coerção
0 === false;            // false: tipos diferentes
```

Strings são sequências UTF-16. `length` conta unidades de código, não
necessariamente caracteres humanos:

```javascript
"😀".length;             // 2
[..."😀"].length;        // 1 ponto de código
```

Segmentação de grafemas e regras de idioma pedem `Intl` quando relevante.

## 4. Truthiness, decisões e laços

São falsy: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined` e `NaN`. Arrays
e objetos vazios são truthy.

```javascript
if (score >= 9) {
  concept = "A";
} else if (score >= 7) {
  concept = "B";
} else {
  concept = "C";
}
```

Não use `if (!value)` quando zero ou string vazia são valores distintos de
ausência. O operador `??` só usa o fallback para `null`/`undefined`:

```javascript
const limit = options.limit ?? 20;
```

Percorra valores com `for...of` e propriedades enumeráveis com muito cuidado em
`for...in`:

```javascript
for (const [index, task] of tasks.entries()) {
  console.log(index, task.title);
}

for (const [key, value] of Object.entries(configuration)) {
  console.log(key, value);
}
```

`break` encerra; `continue` avança. Métodos funcionais são úteis quando a
intenção é simples:

```javascript
const pendingTitles = tasks
  .filter((task) => !task.done)
  .map((task) => task.title);
```

Use laço explícito quando precisar de early return, várias condições ou efeitos.

## 5. Funções, closures e parâmetros

```javascript
export function calculateTotal(values, { discount = 0 } = {}) {
  if (!Array.isArray(values)) throw new TypeError("values must be an array");
  if (!Number.isInteger(discount) || discount < 0 || discount > 100) {
    throw new RangeError("discount must be an integer from 0 to 100");
  }
  const subtotal = values.reduce((sum, value) => sum + value, 0);
  return Math.trunc((subtotal * (100 - discount)) / 100);
}
```

O objeto de opções evita uma sequência de booleanos/números sem nome. Defaults
são avaliados por chamada.

Uma closure retém acesso ao escopo léxico:

```javascript
function createCounter(initial = 0) {
  let value = initial;
  return {
    current: () => value,
    increment: () => ++value,
  };
}
```

Enquanto as funções retornadas existirem, `value` permanece alcançável. Closure
é útil para encapsulamento, mas também pode reter muita memória acidentalmente.

### Arrow function e `this`

Arrow functions não criam seu próprio `this`, `arguments` ou `new.target`.

```javascript
const counter = {
  value: 0,
  increment() {
    this.value += 1;
  },
};
```

Use método comum quando o receptor importa. Ao passar um método como callback,
o binding pode ser perdido; prefira função que recebe dados explicitamente ou
use `bind` conscientemente.

## 6. Arrays, objetos, Map e Set

```javascript
const tasks = [
  { id: 1, title: "Estudar", done: false },
  { id: 2, title: "Praticar", done: true },
];

const updated = tasks.map((task) =>
  task.id === 1 ? { ...task, done: true } : task,
);
```

Spread cria cópia rasa; objetos internos ainda são compartilhados. Para dados
aninhados, modele atualizações de cada nível ou use `structuredClone` apenas
quando seus tipos e custo forem adequados.

- `Array`: sequência ordenada, índice e métodos de transformação;
- objeto comum: registro com chaves string/symbol;
- `Map`: chaves de qualquer tipo e iteração explícita;
- `Set`: unicidade e pertencimento;
- `WeakMap`/`WeakSet`: associações que não impedem coleta das chaves.

```javascript
const byId = new Map(tasks.map((task) => [task.id, task]));
const uniqueTags = new Set(["js", "web", "js"]);
```

Busca em `Map`/`Set` é, em média, mais apropriada que repetir `array.find` em
grandes coleções. Meça antes de otimizar.

## 7. Objetos, protótipos e classes

Objetos delegam busca de propriedades pela cadeia de protótipos. `class` é uma
sintaxe organizada sobre esse modelo:

```javascript
class Account {
  #balance;

  constructor(initialBalance = 0) {
    if (!Number.isSafeInteger(initialBalance) || initialBalance < 0) {
      throw new RangeError("invalid initial balance");
    }
    this.#balance = initialBalance;
  }

  deposit(amount) {
    if (!Number.isSafeInteger(amount) || amount <= 0) {
      throw new RangeError("invalid amount");
    }
    const nextBalance = this.#balance + amount;
    if (!Number.isSafeInteger(nextBalance)) {
      throw new RangeError("balance exceeds the safe integer range");
    }
    this.#balance = nextBalance;
  }

  get balance() {
    return this.#balance;
  }
}
```

Campos `#private` são privados em runtime. Ainda assim, prefira funções e
composição quando não há identidade/estado que justifique uma classe.
Validar apenas cada operando não basta: dois inteiros seguros podem produzir uma
soma fora da faixa exata de `Number`. Por isso o estado só muda depois que o
resultado também passa por `Number.isSafeInteger`.

Nunca misture objetos não confiáveis ao protótipo da aplicação. Ao copiar
configurações externas, aceite apenas chaves conhecidas.

## 8. Erros e desenho de falhas

Lance instâncias de `Error`, não strings:

```javascript
class ValidationError extends Error {
  constructor(message, options) {
    super(message, options);
    this.name = "ValidationError";
  }
}

function loadConfiguration(text) {
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new ValidationError("configuration is not valid JSON", { cause: error });
  }
}
```

Tipos usuais:

- `TypeError`: tipo/forma incompatível;
- `RangeError`: valor fora do intervalo;
- erro de domínio próprio: falha esperada que o chamador diferencia.

Capture onde houver decisão: tentar novamente, responder com status, adicionar
contexto ou finalizar. Não converta todo erro em “deu errado”. Preserve `cause`
e stack, sem expor segredos ao usuário.

## 9. Promises, async/await e event loop

Uma Promise representa conclusão futura, não uma thread:

```javascript
async function getJson(url, { signal } = {}) {
  const response = await fetch(url, { signal });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  return validatePayload(data);
}
```

`await` pausa a função assíncrona e devolve controle ao host. Depois da pilha
atual, microtasks de promises são processadas antes de muitas filas de tarefas.

```javascript
console.log("A");
queueMicrotask(() => console.log("C"));
console.log("B");
// A, B, C
```

Código CPU-bound continua bloqueando a thread mesmo dentro de `async`.
Web Workers, worker threads ou processos isolam cálculo quando medido.

Concorrência explícita:

```javascript
const [users, tasks] = await Promise.all([loadUsers(), loadTasks()]);
```

`Promise.all` rejeita no primeiro erro observado; `Promise.allSettled` devolve
todos os resultados. Nenhum deles limita concorrência: disparar milhares de
requisições pode esgotar sockets e memória. Implemente fila/limite.

Use `AbortController` para cancelamento e um timer para timeout quando a API não
o fornece. Remova listeners quando o ciclo termina.

## 10. DOM seguro e acessível

```javascript
function renderTask(task) {
  const item = document.createElement("li");
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = task.title;
  button.setAttribute("aria-pressed", String(task.done));
  item.append(button);
  return item;
}
```

`textContent` trata entrada como texto. Não coloque dado não confiável em
`innerHTML`. Se HTML for realmente necessário, use política e sanitização
robustas adequadas ao projeto.

HTML semântico primeiro; ARIA complementa, não substitui. Mantenha teclado,
foco, rótulos e mensagens de erro. Validação do navegador melhora UX, mas o
servidor valida de novo.

Delegação reduz listeners em listas dinâmicas:

```javascript
list.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-task-id]");
  if (!button || !list.contains(button)) return;
  toggleTask(Number(button.dataset.taskId));
});
```

## 11. Node.js: processos, arquivos e streams

```javascript
import { readFile, writeFile } from "node:fs/promises";

const text = await readFile("tasks.json", "utf8");
const raw = JSON.parse(text);
const tasks = validateTasks(raw);
await writeFile("tasks.tmp", `${JSON.stringify(tasks, null, 2)}\n`, "utf8");
```

Use APIs assíncronas em servidores para não bloquear o event loop. Para arquivos
grandes, streams aplicam backpressure e evitam carregar tudo em memória.

`process.argv` contém argumentos textuais. Saída normal vai para `stdout`, erros
para `stderr`, e status zero significa sucesso. Não chame `process.exit` antes
de buffers assíncronos terminarem; prefira `process.exitCode`.

Ao trabalhar com caminhos, use `node:path`, fixe um diretório-base e recuse
escapes quando a entrada vem de usuário.

## 12. Organização em camadas

Uma aplicação pequena pode evoluir assim:

```text
src/
├── domain/
│   └── task.mjs
├── application/
│   └── task-service.mjs
├── infrastructure/
│   └── json-repository.mjs
└── interfaces/
    ├── cli.mjs
    └── web.mjs
test/
└── task-service.test.mjs
```

Domínio não deve importar DOM, filesystem nem framework. Passe dependências:

```javascript
export function createTaskService(repository, clock = () => new Date()) {
  return {
    async add(title) {
      const task = { id: crypto.randomUUID(), title, createdAt: clock() };
      await repository.save(task);
      return task;
    },
  };
}
```

Em teste, forneça repositório e relógio controlados.

## 13. Memória, garbage collection e vazamentos

O coletor libera objetos inalcançáveis; não há `free` manual. Vazamento ainda
ocorre quando uma referência permanece alcançável sem necessidade:

- cache sem limite;
- listener nunca removido;
- timer/intervalo permanente;
- closure retendo grande grafo;
- coleção global que só cresce.

Coleta não fecha deterministicamente arquivos, sockets ou locks. Use APIs de
cleanup (`finally`, `close`, `Symbol.dispose` quando suportado pelo alvo) e
documente ownership.

## 14. Testes e depuração

Node possui runner e assertions nativos:

```javascript
import assert from "node:assert/strict";
import test from "node:test";

test("classifies boundary", () => {
  assert.equal(concept(7), "B");
});

test("rejects invalid score", () => {
  assert.throws(() => concept(11), RangeError);
});
```

Execute testes determinísticos e independentes. Para promises, retorne/aguarde
a promise; um teste que termina antes da rejeição produz falso positivo.

```bash
node --test
node --inspect-brk programa.mjs
```

No navegador, use breakpoints, painel de rede, inspeção de acessibilidade e
performance. `console.log` ajuda a explorar, mas logs estruturados com contexto
são melhores em aplicações. Nunca registre tokens ou dados pessoais.

## 15. Leitura guiada do exemplo real

Abra [`exemplos/javascript/fundamentos.mjs`](../exemplos/javascript/fundamentos.mjs):

1. `validateScore` centraliza tipo, finitude e intervalo;
2. `ScoreValidationError` permite distinguir falha de domínio;
3. `concept` é pura;
4. `summarize` aceita qualquer iterável e não muta a fonte;
5. `parseScores` trata peculiaridades de conversão na fronteira;
6. `main` recebe saídas por injeção, então é testável sem subprocesso;
7. o guard por `import.meta.url` evita executar a CLI ao importar.

```bash
node 00-Fundamentos/programacao/exemplos/javascript/fundamentos.mjs 10 8 4
node --test 00-Fundamentos/programacao/exemplos/javascript/fundamentos.test.mjs
```

Leia também os testes. Eles cobrem limites, gerador, imutabilidade da entrada,
erros de tipo, causa encadeada e status da CLI.

## 16. Exercícios progressivos

1. Adicione conceito `A+` para nota 10, começando pelo teste.
2. Calcule mediana sem ordenar/mutar o array recebido.
3. Leia notas de JSON e valide esquema manualmente.
4. Crie uma página acessível que renderiza o resumo sem `innerHTML`.
5. Implemente fetch com timeout, cancelamento e estados loading/vazio/erro.
6. Processe um arquivo grande com stream e compare memória com `readFile`.
7. Construa repositório em memória e em JSON para a mesma camada de serviço.
8. Crie um worker para cálculo CPU-bound e meça o custo de serialização.

Critério de conclusão: você deve prever coerções, explicar a ordem assíncrona,
validar toda fronteira externa e provar funções de domínio com testes nativos.
