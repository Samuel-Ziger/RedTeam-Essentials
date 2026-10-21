# Projetos, avaliações e portfólio técnico

Projeto não mede quantidade de linhas. Ele comprova que você consegue transformar
um problema em contrato, modelo, implementação, testes e operação reproduzível.
Esta etapa integra o módulo 00 e prepara a transição para os módulos seguintes.

## Objetivos de aprendizagem

Ao concluir os projetos, você deverá conseguir:

- esclarecer requisitos e declarar o que ficou fora do escopo;
- dividir uma entrega em incrementos pequenos e demonstráveis;
- escolher estrutura de dados, linguagem e persistência com justificativa;
- criar testes a partir de riscos e critérios de aceite;
- registrar diagnóstico, decisões e limitações;
- entregar comandos reproduzíveis de build, execução, teste e limpeza;
- operar uma aplicação local e recuperar dados fictícios;
- apresentar o projeto sem esconder falhas ou depender de uma demonstração manual.

## 1. Regra de execução

Para cada incremento use o ciclo:

```text
problema
   -> exemplo concreto
   -> critério observável
   -> teste que falha pela razão esperada
   -> implementação mínima
   -> refatoração
   -> documentação/operação
   -> commit pequeno
```

Não comece pelos extras. Primeiro conclua um fluxo vertical: entrada válida,
regra, persistência/saída e teste. Depois acrescente erros e variações.

### Evidência mínima de toda entrega

- README com problema, escopo, requisitos e limitações;
- versões/ferramentas necessárias;
- comandos de build, execução, teste e limpeza;
- ao menos um exemplo válido e um inválido;
- testes automatizados relevantes;
- dados de demonstração sintéticos;
- decisões técnicas importantes e alternativas consideradas;
- registro de um defeito encontrado e como foi diagnosticado;
- checklist dos critérios de aceite;
- retrospectiva curta: manter, mudar, aprender.

### Estrutura sugerida, não obrigatória

```text
meu-projeto/
|-- README.md
|-- CHANGELOG.md
|-- docs/
|   |-- requisitos.md
|   |-- arquitetura.md
|   `-- operacao.md
|-- src/
|-- tests/
|-- fixtures/
|-- .gitignore
`-- LICENSE
```

Não copie essa árvore se a linguagem possui convenção melhor. Estrutura deve
facilitar navegação e ferramentas, não satisfazer uma forma vazia.

## 2. Projeto 1 — calculadora de orçamento

**Objetivo:** dominar entrada estruturada, validação, dinheiro, funções puras,
saída determinística, testes e códigos de processo.

Implemente primeiro em Python e depois em Java ou C#.

### Contrato da entrada

Arquivo CSV em UTF-8:

```csv
item,quantity,unit_price
Caderno,2,18.90
Caneta,3,4.50
```

Regras:

- cabeçalho exato e documentado;
- `item` normalizado, não vazio e com até 80 caracteres;
- `quantity` inteiro entre 1 e 10.000;
- `unit_price` decimal não negativo com no máximo duas casas;
- arquivo vazio, coluna ausente, linha extra e valor inválido produzem erro claro;
- dinheiro não usa ponto flutuante binário para decisões financeiras.

Use `decimal.Decimal` em Python, `BigDecimal` em Java ou `decimal` em C#. Defina
regra de arredondamento explicitamente.

### Regra de desconto

Escolha e documente uma regra simples, por exemplo:

| Subtotal | Desconto |
|----------|----------|
| abaixo de 100,00 | 0% |
| de 100,00 até 499,99 | 5% |
| a partir de 500,00 | 10% |

Valores de fronteira (`99,99`, `100,00`, `499,99`, `500,00`) são obrigatórios
nos testes.

### Saída

Gere JSON determinístico:

```json
{
  "items": 2,
  "subtotal": "51.30",
  "discountRate": "0.00",
  "discount": "0.00",
  "total": "51.30"
}
```

Defina ordenação dos campos ou compare o JSON semanticamente nos testes. Valores
monetários como strings preservam representação decimal no contrato proposto.

### Interface de linha de comando

```text
budget INPUT.csv --output result.json
```

Códigos sugeridos:

- `0`: sucesso;
- `2`: uso/argumento inválido;
- `3`: entrada inválida;
- `4`: falha de leitura/escrita.

Saída normal vai para stdout; diagnóstico vai para stderr. Não mostre stack
trace para erro de entrada esperado.

### Plano de implementação

1. modele `Item` e a função pura de total;
2. teste fronteiras do desconto e arredondamento;
3. leia uma linha CSV válida;
4. acumule erros com número da linha ou pare conforme contrato;
5. serialize JSON determinístico;
6. acrescente CLI e códigos de saída;
7. implemente na segunda linguagem;
8. execute as mesmas fixtures nas duas implementações.

### Matriz mínima de testes

| Caso | Resultado esperado |
|------|--------------------|
| um item válido | subtotal e total corretos |
| limite inferior do desconto | regra correta |
| limite superior do desconto | regra correta |
| quantidade zero | rejeição com linha/campo |
| preço com três casas | rejeição ou arredondamento documentado |
| cabeçalho incorreto | código de entrada inválida |
| arquivo inexistente | código de I/O e stderr seguro |
| caracteres UTF-8 | preservados corretamente |
| execução repetida | JSON semanticamente idêntico |

**Concluído quando:** ambas as linguagens passam as mesmas fixtures sem internet,
o JSON é semanticamente equivalente e todos os erros previstos possuem código.

**Estimativa:** 10–16 horas.

## 3. Projeto 2 — agenda CLI persistente

**Objetivo:** separar interface, domínio e repositório; preservar invariantes e
evoluir dados persistidos.

Escolha Java ou C#. Use JSON no primeiro incremento e SQLite no segundo, ou
implemente diretamente SQLite se já domina arquivos.

### Comandos obrigatórios

```text
contacts add --name "Ada Lovelace" --email "ada@example.test"
contacts list
contacts find --query "ada"
contacts update 42 --name "Ada Byron"
contacts remove 42
```

Contrato:

- ID é estável e não é a posição da lista;
- nome é obrigatório, normalizado e limitado;
- email é obrigatório, comparado de acordo com regra documentada e único;
- busca deixa claro se diferencia maiúsculas/acentos;
- atualizar contato inexistente não cria outro;
- remoção exige ID e possui resultado observável;
- persistência sobrevive entre execuções;
- nenhum contato real é usado nos testes.

Não tente validar todos os endereços de email do mundo com uma expressão
regular gigantesca. Aplique regra de formato compatível com o escopo e trate
confirmação de propriedade como problema separado.

### Arquitetura esperada

```text
parser da CLI
     |
     v
casos de uso
     |
     +--> regras/entidades
     |
     v
interface de repositório
     |
     +--> JSON
     `--> SQLite
```

A CLI converte texto em tipos e apresenta o resultado. Ela não implementa
unicidade. O caso de uso coordena; o repositório persiste; constraints reforçam
invariantes no banco.

### Plano de implementação

1. defina cinco cenários de aceite;
2. modele contato imutável/validado;
3. crie repositório em memória para testes dos casos de uso;
4. implemente `add` e `list` verticalmente;
5. acrescente `find`, `update` e `remove`;
6. implemente persistência real e testes em diretório temporário;
7. simule arquivo corrompido/banco indisponível;
8. crie backup/migração do formato inicial;
9. documente limites de concorrência.

### Testes obrigatórios

- nome vazio, máximo e acima do máximo;
- email duplicado com variação de caixa conforme regra definida;
- busca com zero, um e vários resultados;
- update preserva ID;
- remove inexistente;
- grava, encerra, reabre e lista;
- falha durante persistência não deixa arquivo parcial quando aplicável;
- duas instâncias concorrentes possuem comportamento documentado.

### Extensões entre linguagens

- **C:** implemente leitor/escritor de um formato simples, com limites, ownership
  e testes sob sanitizer. Não replique a aplicação inteira.
- **JavaScript:** importe contatos assincronamente, com timeout/cancelamento e
  limite de concorrência.
- **Python:** escreva uma ferramenta de migração e validação das fixtures.

**Concluído quando:** domínio é testado sem CLI/banco, persistência possui teste
de integração, dados sobrevivem e falhas não expõem stack trace ou dados.

**Estimativa:** 16–24 horas.

## 4. Projeto 3 — biblioteca de estruturas de dados em C

**Objetivo:** compreender layout, capacidade, ownership, erro de alocação,
invariantes e custo de operações.

Implemente:

- vetor dinâmico de inteiros;
- pilha sobre vetor;
- fila circular;
- busca linear;
- busca binária em entrada ordenada;
- testes e build com sanitizers.

### Contrato sugerido do vetor

```c
typedef struct {
    int *data;
    size_t length;
    size_t capacity;
} IntVector;

bool vector_init(IntVector *vector);
bool vector_push(IntVector *vector, int value);
bool vector_get(const IntVector *vector, size_t index, int *out);
void vector_destroy(IntVector *vector);
```

Invariantes:

```text
length <= capacity
capacity == 0 implica data == NULL
elementos válidos ocupam [0, length)
destroy pode ser chamado em vetor inicializado, inclusive vazio
se push falhar, o vetor anterior permanece válido
```

Antes de aumentar capacidade, verifique overflow do cálculo de bytes. Use
temporário para `realloc`; atribuir diretamente pode perder o ponteiro original
em falha.

```c
int *new_data = realloc(vector->data, new_capacity * sizeof *new_data);
if (new_data == NULL) {
    return false; /* vector->data original continua válido */
}
vector->data = new_data;
vector->capacity = new_capacity;
```

O código completo ainda precisa validar `new_capacity * sizeof *new_data` contra
overflow antes de chamar `realloc`.

### Fila circular

Use índices `head`, `length` e `capacity`. A posição física do item lógico `i`
pode ser:

```text
(head + i) % capacity
```

Teste o wrap-around: enfileire, remova parte, enfileire novamente até atravessar
o fim do array.

### Build de diagnóstico

```bash
cc -std=c17 -Wall -Wextra -Wpedantic -Werror \
  -fsanitize=address,undefined -g \
  vector.c queue.c test_main.c -o structures_test

./structures_test
```

Quando disponível, execute também analisador estático e ferramenta de leak da sua
plataforma. Nenhuma ferramenta isolada prova ausência de falhas.

### Matriz mínima de testes

- estrutura vazia;
- primeiro elemento;
- crescimento de capacidade;
- acesso em `length - 1` e em `length`;
- muitas expansões;
- fila cheia/vazia e wrap-around;
- busca binária: ausente, primeiro, meio, último e duplicado conforme contrato;
- destruição de estrutura vazia e preenchida;
- falha de alocação injetada ou abstraída, se possível.

Compare complexidade e ergonomia com `list`/`deque` em Python, `ArrayList` em
Java, `List<T>`/`Queue<T>` em C# e `Array` em JavaScript. O objetivo não é
substituir bibliotecas maduras; é compreender seus custos e contratos.

**Concluído quando:** testes e sanitizers passam, cada alocação possui ownership
documentado e você consegue justificar complexidade de cada operação.

**Estimativa:** 18–28 horas.

## 5. Projeto 4 — TaskBoard full stack

**Objetivo:** integrar navegador, JavaScript, HTTP, Python, SQLite, containers,
Nginx, testes e operação.

O código base e o laboratório completo estão em
[projetos/taskboard](projetos/taskboard/README.md).

O [Lab 05](labs/lab-05-taskboard-docker-nginx.md) é a execução guiada das
fases A e B abaixo. Use os mesmos logs, diagramas e testes como evidência; não
repita mecanicamente o laboratório. O projeto começa de fato a exigir autoria
nas fases C e D, quando você especifica e entrega uma mudança vertical.

### Fase A — compreender antes de mudar

1. execute os testes da API;
2. leia `server.py`, `app.js`, `nginx.conf`, Dockerfiles e Compose;
3. desenhe navegador → Nginx → API → SQLite;
4. mapeie cada endpoint até a função e SQL correspondente;
5. liste invariantes e limites;
6. explique por que a API não publica uma porta.

**Gate:** você consegue prever status e corpo para request válido e cinco erros.

### Fase B — operar a versão base

1. suba via Compose;
2. teste health do Nginx e da API;
3. crie, conclua e remova tarefas pelo navegador e por `curl`;
4. acompanhe logs;
5. recrie containers e confirme persistência;
6. crie, verifique e restaure backup com dados fictícios;
7. encerre preservando o volume.

**Gate:** outra pessoa repete seus comandos sem conhecimento implícito.

### Fase C — implementar uma melhoria vertical

Escolha **uma** antes de combinar extras:

- prioridade `low|normal|high`;
- prazo opcional com data/fuso definidos;
- edição do título;
- busca textual com semântica, limite e custo documentados;
- arquivamento reversível, distinto de exclusão;
- etiquetas com quantidade e tamanho limitados;
- exportação JSON.

Para qualquer escolha:

1. escreva história, cenários e fora de escopo;
2. defina contrato HTTP e compatibilidade;
3. planeje migração e rollback se o schema mudar;
4. escreva teste que falha;
5. implemente backend;
6. implemente interface acessível;
7. teste erro, teclado e estado vazio;
8. reconstrua containers;
9. valide persistência e backup;
10. atualize contrato e runbook.

### Exemplo de especificação: prioridade

```text
Entrada aceita: "low", "normal" ou "high"
Ausente em criação: usa "normal"
Outro tipo/valor: 422, sem inserir
Resposta: sempre inclui "priority"
Migração: tarefas antigas recebem "normal"
Interface: label textual; significado não depende apenas de cor
Ordenação: permanece por ID até requisito explícito
```

Testes devem cobrir default, três valores, valor inválido, persistência,
serialização e renderização segura.

### Fase D — observar e defender

- registre latência de forma que possa ser agregada;
- audite a propagação de `request_id` do gateway até resposta e logs, testando
  tanto um identificador válido fornecido pelo cliente quanto a geração de um
  novo para entrada ausente ou inválida, sem registrar o corpo;
- teste API parada e banco não gravável em cópia descartável;
- documente limite de concorrência do SQLite;
- execute a rubrica e faça demonstração de 8 minutos.

Não adicione login improvisado. Autenticação exige modelo de ameaça,
armazenamento de credencial, sessão, expiração, recuperação, autorização,
CSRF/rate limit e operação. Isso pertence a uma etapa dedicada.

**Concluído quando:** base compreendida, operação reproduzível, uma melhoria
vertical testada, migração segura quando aplicável e limitações documentadas.

**Estimativa:** 20–32 horas.

## 6. Projeto final autoral

Escolha um problema não ofensivo e com dados fictícios:

- biblioteca pessoal;
- finanças sintéticas;
- hábitos;
- estoque doméstico;
- agenda de estudos;
- receitas e planejamento de refeições;
- empréstimo fictício de equipamentos.

O projeto deve ser pequeno o suficiente para ficar completo. Três fluxos
terminados ensinam mais do que vinte telas inacabadas.

### Etapa 1 — descoberta

Entregue:

- problema em um parágrafo;
- usuário/persona fictícia;
- cinco histórias com critérios;
- glossário do domínio;
- entradas, saídas e limites;
- fora de escopo;
- três riscos principais.

Pergunta de gate: cada critério pode ser demonstrado sem opinião subjetiva?

### Etapa 2 — projeto técnico

Entregue:

- diagrama simples de componentes e fluxo;
- modelo de dados com invariantes;
- contrato da API ou CLI;
- estratégia de erros;
- fronteiras de confiança;
- plano de testes;
- duas decisões registradas.

Formato curto para decisão:

```markdown
# ADR-001: usar SQLite

## Contexto
Aplicação local, um usuário, dados relacionais e operação simples.

## Decisão
Usar SQLite com constraints e migrações versionadas.

## Alternativas
JSON: simples, mas pior para unicidade/transações.
Servidor SQL: mais operação do que o escopo justifica.

## Consequências
Boa portabilidade local; escrita concorrente limitada.
```

### Etapa 3 — construção incremental

Ordem recomendada:

1. regra central pura;
2. persistência real e teste de integração;
3. API/CLI com um fluxo vertical;
4. interface com acessibilidade básica;
5. erros e limites;
6. demais fluxos;
7. migração;
8. observação;
9. empacotamento.

Faça commits que respondam “qual comportamento mudou?”. Não use commit gigante
com código, formatação e renomeação sem relação.

### Etapa 4 — operação

Obrigatório:

- configuração externa validada ao iniciar;
- logs estruturados sem dados sensíveis;
- healthcheck quando for serviço;
- Docker e Nginx se for aplicação web;
- persistência fora da camada do container;
- backup e restauração demonstrados;
- encerramento e cleanup documentados;
- limites de corpo, tempo e recursos;
- nenhum segredo ou dado pessoal no repositório.

### Etapa 5 — qualidade de entrega

- CI executa testes e verificações disponíveis;
- versões de ferramentas estão documentadas;
- changelog descreve comportamento;
- licença é compatível com seu objetivo;
- README permite começar do zero;
- limitações e dívida técnica estão visíveis;
- uma release local/tag possui critérios atendidos.

**Estimativa:** 30–50 horas, com escopo controlado.

## 7. Estratégia de testes do portfólio

Não persiga porcentagem isolada. Mapeie risco para evidência:

| Risco | Teste/evidência |
|-------|------------------|
| regra calcula resultado errado | unidade com fronteiras |
| SQL não preserva invariante | integração com banco real temporário |
| API muda formato/status | contrato HTTP |
| fluxo não funciona montado | ponta a ponta representativo |
| migração perde dado | fixture de versão anterior + verificação |
| backup não restaura | ensaio de restauração |
| entrada consome recurso demais | teste de limite de tamanho/tempo |
| erro vaza detalhe interno | teste da resposta externa e inspeção de log |

Para todo defeito real corrigido, acrescente um teste de regressão que falharia
antes da correção.

## 8. Revisão de segurança da entrega

Antes da avaliação:

- [ ] fixtures usam apenas `example.test` e identidades fictícias;
- [ ] histórico não contém `.env`, token, chave ou banco pessoal;
- [ ] entrada possui limite de tamanho, tipo e faixa;
- [ ] SQL é parametrizado;
- [ ] HTML não é montado com texto não confiável;
- [ ] erros externos não expõem stack, SQL ou caminhos internos;
- [ ] processos/containers usam privilégio mínimo;
- [ ] serviço local liga em loopback quando possível;
- [ ] timeout e capacidade de filas são explícitos;
- [ ] limpeza destrutiva é claramente marcada e limitada ao projeto;
- [ ] limitações de autenticação/TLS estão declaradas.

## 9. Rubrica de avaliação (100 pontos)

| Dimensão | Pontos | Evidência esperada |
|----------|--------|---------------------|
| Correção | 20 | critérios essenciais passam; invariantes preservadas |
| Requisitos e escopo | 10 | cenários, limites e fora de escopo claros |
| Modelagem | 10 | tipos, IDs, relações e constraints coerentes |
| Design | 10 | responsabilidades coesas e dependências explícitas |
| Testes | 15 | unidade, integração, fronteiras e regressões |
| Robustez e segurança | 10 | validação, limites, erros e menor privilégio |
| Operação | 10 | build, config, logs, health, persistência e cleanup |
| Dados e evolução | 5 | migração, backup/restauração, compatibilidade |
| Documentação | 5 | README/runbook reproduzíveis e limitações |
| Defesa e retrospectiva | 5 | explica escolhas, evidência e próximos passos |

### Gates obrigatórios

Mesmo com 75 pontos, a entrega não é concluída se:

- função essencial está incorreta;
- testes principais não executam pelo comando documentado;
- existe segredo/dado pessoal no repositório;
- SQL concatena entrada ou a interface injeta HTML não confiável;
- não é possível iniciar a aplicação do zero;
- uma migração destrutiva não possui aviso/backup;
- o autor não consegue explicar o código apresentado.

Meta: pelo menos 75 pontos, todos os gates atendidos. Refaça a avaliação após
corrigir; a rubrica serve para guiar aprendizado, não apenas dar nota.

## 10. Demonstração técnica de 8 minutos

1. **1 min:** problema, usuário e fora de escopo;
2. **1 min:** arquitetura e principal invariante;
3. **2 min:** fluxo feliz completo;
4. **1 min:** entrada inválida e resposta;
5. **1 min:** teste automatizado e falha que ele evita;
6. **1 min:** logs/health e persistência;
7. **1 min:** limitação e próximo passo.

Prepare dados sintéticos e um caminho alternativo caso a interface falhe. Uma
demonstração não substitui testes; ela comunica as evidências.

## 11. Perguntas da defesa

1. Qual é a invariante mais importante e em quais camadas ela é protegida?
2. Qual entrada de fronteira revelou um defeito?
3. Por que escolheu esta linguagem, banco e estrutura?
4. Onde existe estado e quem pode alterá-lo?
5. O que ocorre se o processo parar no meio de uma escrita?
6. Como um erro de dependência aparece para usuário e operador?
7. Qual teste usa dependência real e por que um mock não bastaria?
8. Como o sistema se comporta com dez vezes mais dados e concorrência?
9. Como restaurar os dados depois de uma falha?
10. O que foi deliberadamente excluído e qual seria a próxima decisão?
11. Qual mudança quebraria consumidores existentes?
12. Qual decisão você mudaria depois do que aprendeu?

Se você não sabe, diga e explique como obteria evidência. Inventar certeza é
pior do que declarar uma hipótese.

## 12. Antipadrões de portfólio

- README promete recursos que não existem;
- screenshot sem comando reproduzível;
- dezenas de dependências para uma regra simples;
- arquivo único mistura interface, regra, SQL e configuração;
- teste chama internet ou depende da ordem;
- `except Exception: pass` esconde falha;
- credencial de exemplo parece real ou funciona;
- Docker apenas envolve um processo sem health, dados ou explicação;
- “microserviços” locais sem necessidade aumentam pontos de falha;
- autenticação caseira usada para alegar segurança;
- tecnologia listada sem decisão demonstrada;
- projeto enorme que não possui um fluxo concluído.

## 13. Checklist final do módulo

- [ ] Projeto 1 produz o mesmo resultado em duas linguagens.
- [ ] Projeto 2 separa CLI, domínio e persistência e sobrevive entre execuções.
- [ ] Projeto 3 passa em testes e sanitizers sem vazamento conhecido.
- [ ] Eu consigo desenhar e operar o TaskBoard sem consultar a implementação a cada passo.
- [ ] Implementei uma melhoria vertical no TaskBoard com teste e documentação.
- [ ] O projeto autoral possui cinco cenários completos e escopo controlado.
- [ ] Build, testes, execução, backup, restauração e cleanup são reproduzíveis.
- [ ] Nenhum segredo, dado pessoal ou dependência de internet existe nos testes.
- [ ] Consigo responder às perguntas da defesa com evidência.
- [ ] Registrei retrospectiva honesta e próximos passos.

Conclusão não significa que o software está “pronto para qualquer produção”.
Significa que o escopo declarado está correto, testado, operável e compreendido.
