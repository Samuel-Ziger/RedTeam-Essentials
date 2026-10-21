# Curso de programação: do zero à construção de software

Este curso é a base técnica da formação. Ele começa com raciocínio lógico e
chega à entrega de uma aplicação web com API, banco de dados, testes, Docker e
Nginx. Todo exemplo usa dados locais e sintéticos; não há exploits nem ações
contra sistemas de terceiros.

O objetivo não é fazer você decorar cinco sintaxes. Ao terminar, você deverá
conseguir receber um problema ainda impreciso, esclarecer o comportamento
esperado, modelar dados, implementar uma solução, investigar falhas, escrever
testes e entregar um programa que outra pessoa consiga executar e manter.

## Para quem este curso foi escrito

Você pode começar sem experiência prévia. É suficiente saber instalar um
programa e criar uma pasta. Quem já programa pode usar os checkpoints para
identificar lacunas, mas não deve pular uma etapa apenas porque reconhece os
termos: a evidência prática é o que libera a próxima etapa.

O curso usa cinco linguagens porque cada uma torna visível uma parte diferente
da computação:

| Linguagem | Modelo mental enfatizado | Entrega mínima |
|-----------|---------------------------|----------------|
| Python | legibilidade, automação, módulos e biblioteca padrão | CLI validada e testada |
| JavaScript | navegador, eventos, objetos e assincronicidade | interface web e testes no Node.js |
| Java | tipos estáticos, objetos, interfaces e JVM | aplicação compilada com domínio validado |
| C | representação, memória, ponteiros e toolchain | programa C17 sem avisos e verificado |
| C# | tipos modernos, LINQ, recursos e ecossistema .NET | aplicação de console tipada |

Python é a primeira linguagem e Java é a segunda implementação da rota
canônica, inclusive no Lab 02. Em seguida, reconstrua o domínio em C# para
comparar as duas plataformas tipadas. Estude C quando já compreender funções e
coleções; estude JavaScript antes da parte web. Ao final, execute e explique os
exemplos nas cinco linguagens.

## O que você será capaz de demonstrar

### Fundamentos de programação

- representar entradas como valores e tipos adequados;
- explicar, escrever e testar decisões com `if/else`;
- escolher entre `for`, `while`, recursão e operações de coleção;
- decompor um problema em funções com contratos explícitos;
- distinguir valor, referência, identidade, mutabilidade e escopo;
- selecionar lista, mapa, conjunto, pilha, fila, árvore ou grafo pelo padrão de
  acesso e pelo custo da operação;
- estimar tempo e memória com notação assintótica sem confundir estimativa com
  medição.

### Construção de software

- converter requisitos em casos de uso e critérios de aceite observáveis;
- separar domínio, entrada/saída e infraestrutura;
- validar dados na fronteira e preservar invariantes no núcleo;
- tratar falhas sem ocultar contexto e liberar recursos com segurança;
- escrever testes unitários, de integração e de contrato;
- usar logs, stack traces, depurador e experimentos mínimos para localizar uma
  causa, em vez de alterar código por tentativa aleatória;
- organizar módulos, dependências, configuração e histórico Git.

### Aplicações e operação local

- explicar o fluxo navegador → HTTP → Nginx → API → SQLite → resposta;
- projetar uma API pequena com métodos, status, representações e erros
  consistentes;
- usar transações e índices básicos conscientemente;
- diferenciar processo, thread, tarefa assíncrona, concorrência e paralelismo;
- construir imagens, redes e volumes Docker e diagnosticar o estado do Compose;
- servir arquivos estáticos e configurar proxy reverso e healthcheck no Nginx.

## Mapa completo do curso

As horas incluem leitura, digitação dos exemplos, exercícios, investigação de
erros e projetos. Assistir ou ler passivamente não conta como prática.

| Fase | Conteúdo | Evidência para avançar | Carga sugerida |
|------|----------|------------------------|----------------|
| 0 | [Como estudar e resolver problemas](00-como-estudar.md) | diário com decomposição, hipótese e retrospectiva | 3–4 h |
| 1 | [Lógica e algoritmos](01-logica-algoritmos.md) | algoritmos rastreados à mão e implementados | 10–15 h |
| 2 | [Terminal, editor e Git](02-ambiente-terminal-git.md) | repositório com commits pequenos e falha reproduzível | 6–10 h |
| 3 | [Fundamentos comuns](03-fundamentos-comuns.md) | comparação do mesmo domínio em duas linguagens | 10–14 h |
| 4 | [Python](linguagens/python.md) | programa de console com validação e testes | 15–22 h |
| 5 | [Estruturas e algoritmos](04-estruturas-dados-algoritmos.md) | decisões justificadas por operações e complexidade | 14–20 h |
| 6 | [Java](linguagens/java.md), Lab 02 e [C#](linguagens/csharp.md) | contrato do lab em Python + Java e domínio reconstruído em C# | 20–30 h |
| 7 | [Engenharia e testes](05-engenharia-software.md) | requisito → teste → implementação → refatoração | 12–18 h |
| 8 | [C](linguagens/c.md) | executável C17 sem warnings, leaks ou acesso inválido | 12–18 h |
| 9 | [JavaScript](linguagens/javascript.md) | módulo assíncrono testado e interface acessível | 12–18 h |
| 10 | [Web, HTTP, APIs e bancos](06-web-http-bancos.md) | API CRUD local com transação e contrato documentado | 15–22 h |
| 11 | [Sistemas, memória e concorrência](07-sistemas-concorrencia.md) | experimento reproduzível de I/O, memória e corrida | 10–15 h |
| 12 | [Docker e Nginx](08-docker-nginx.md) | aplicação conteinerizada, observável e removível | 8–12 h |
| 13 | [Projetos e avaliações](09-projetos.md) | cinco entregas incrementais, portfólio e defesa técnica | 94–150 h |

A soma inclui uma reserva para revisão e repetição e chega, de forma
arredondada, à faixa de 250–390 horas do módulo. A estimativa dos projetos não
pode ser substituída por apenas ler seus enunciados. Isso não é uma meta de velocidade: repita uma
fase se ainda não consegue produzir a evidência sem copiar a demonstração.

## Ambiente mínimo

Comece apenas com terminal, editor, Git e Python 3.12 ou superior. Instale os
outros runtimes quando chegar ao respectivo guia.

```bash
python3 --version
git --version

# Verificações posteriores; não é necessário instalar tudo no primeiro dia.
java --version
javac --version
cc --version
dotnet --version
node --version
docker --version
docker compose version
```

Os exemplos foram projetados para Python 3.12+, Java 17+, C17, JavaScript
moderno em uma linha LTS par do Node.js 22 ou posterior e C#/.NET 10. No Node,
use no mínimo 22.12 para atender também ao toolchain da aplicação de estudos.
Prefira sempre uma versão ainda suportada, leia os avisos e registre a versão
usada; "funcionou na minha máquina" sem esse dado não é evidência reproduzível.

Crie um diretório separado para seus exercícios. Não altere o exemplo original
antes de conseguir executá-lo; copie-o, faça uma mudança por vez e preserve a
falha em um teste.

## Como estudar cada conceito

Use o ciclo **prever → executar → rastrear → quebrar → corrigir → explicar**:

1. leia o problema e escreva entradas, saídas, restrições e exemplos;
2. preveja a saída do trecho antes de executá-lo;
3. digite o código, execute e compare o observado com a previsão;
4. rastreie os valores relevantes linha por linha;
5. mude deliberadamente um limite, tipo ou condição para produzir uma falha;
6. reduza a falha ao menor caso que ainda a reproduz;
7. escreva um teste que falha pelo motivo correto;
8. corrija uma hipótese por vez e execute toda a suíte;
9. explique a causa, a correção e o teste de regressão com suas palavras;
10. faça um commit pequeno com mensagem que descreve a mudança de comportamento.

Esse ciclo separa reconhecimento de domínio. Reconhecer um `if` não significa
saber definir condições completas, testar limites ou perceber um ramo
inalcançável.

Consulte também o [guia prático de depuração](GUIA-DEPURACAO.md) sempre que um
exemplo não se comportar como esperado.

## Como usar os exemplos executáveis

Os diretórios em [`exemplos/`](exemplos/) implementam o mesmo domínio — análise
de notas — nas cinco linguagens. Isso permite comparar tipos, funções,
coleções, validação, erros, CLI e testes sem trocar também o problema.

Execute a verificação automatizada a partir da raiz do repositório:

```bash
bash 00-Fundamentos/programacao/testar-curso.sh
```

O script:

- executa testes Python e JavaScript;
- compila Java e C com diagnósticos rígidos;
- executa C# quando o .NET compatível está instalado;
- valida a API do TaskBoard e a configuração do Docker Compose;
- informa claramente quando um runtime necessário ainda não está disponível.

Durante o estudo, o modo padrão permite progresso parcial. Para a evidência de
conclusão, exija todas as ferramentas e trate qualquer verificação pulada como
falha:

```bash
bash 00-Fundamentos/programacao/testar-curso.sh --require-all
```

Depois de o teste passar, faça três mudanças em sua cópia:

1. adicione uma nova regra de classificação e seus casos de limite;
2. inclua mediana ou maior/menor nota sem alterar a entrada;
3. mude o formato de saída e documente o impacto no contrato da CLI.

Não considere a mudança concluída se apenas o “caminho feliz” funciona.
Entradas vazias, texto inválido, valores não finitos e limites pertencem ao
comportamento do programa.

## Laboratórios progressivos

Os [cinco laboratórios formais](labs/README.md) aparecem no aplicativo conforme
os capítulos necessários são concluídos:

1. depois de ambiente, lógica e Python: controle de fluxo e limites;
2. depois de fundamentos comuns e Java: CLI, Git e o contrato em Python + Java;
3. depois de estruturas e engenharia: persistência e testes;
4. depois de Web, HTTP e bancos: API local e SQLite;
5. depois de sistemas, Docker, Nginx e briefing do projeto: TaskBoard operável.

Cada lab exige código, testes, relatório de depuração e critérios de aceite. O
objetivo é produzir evidência reutilizável no portfólio, não somente executar
comandos.

## Checkpoints obrigatórios

### Checkpoint A — raciocínio e controle de fluxo

- implementar FizzBuzz e uma calculadora de faixa sem consultar solução;
- rastrear manualmente ao menos um laço e uma função;
- demonstrar testes nos limites imediatamente antes, no valor e depois de cada
  mudança de regra;
- explicar por que uma condição mais abrangente pode tornar outra inalcançável.

### Checkpoint B — dados e decomposição

- implementar uma agenda em memória com lista e mapa;
- separar parsing, validação, regra e apresentação;
- justificar a estrutura escolhida pelo padrão de leitura/escrita;
- medir uma hipótese de desempenho em vez de inferi-la apenas por impressão.

### Checkpoint C — qualidade e persistência

- persistir dados localmente sem corromper o arquivo em uma falha simulada;
- criar testes unitários e de integração independentes;
- diagnosticar um erro a partir do stack trace;
- usar configuração externa sem registrar segredo.

### Checkpoint D — aplicação operável

- executar o TaskBoard sem Docker e depois via Compose;
- seguir uma requisição da interface até a transação no banco;
- identificar logs, healthcheck, volume, rede e proxy;
- provocar uma falha segura, explicar o diagnóstico e restaurar o ambiente;
- remover containers e volumes criados para o exercício.

## Convenções pedagógicas

- **Modelo mental:** explicação do mecanismo, não apenas da sintaxe.
- **Rastreamento:** tabela do estado do programa ao longo da execução.
- **Prática guiada:** passos suficientes para o primeiro contato.
- **Exercício:** problema com critérios verificáveis, sem receita completa.
- **Desafio:** combina conceitos e exige decisões justificadas.
- **Critério de aceite:** observação objetiva que define “pronto”.
- **Evidência:** código, teste, medição ou explicação preservada no portfólio.
- **Refatoração:** mudança de estrutura sem mudança intencional de comportamento.

Se um exercício parecer grande, reduza o escopo mantendo uma fatia completa:
uma entrada, uma regra, uma saída e um teste. Depois expanda.

## Como pedir ajuda sem terceirizar o raciocínio

Uma pergunta técnica reproduzível contém:

1. objetivo e comportamento esperado;
2. menor entrada que produz o problema;
3. comportamento observado e mensagem completa de erro;
4. hipótese e experimento já realizados;
5. versões do runtime, dependências e sistema;
6. trecho mínimo de código, sem segredos nem dados pessoais.

Evite “não funciona” e capturas sem texto pesquisável. Não publique `.env`,
tokens, chaves, dumps, nomes de clientes ou código proprietário. Uma resposta
externa é uma hipótese: execute os testes e assuma responsabilidade pelo código
incorporado.

Veja [Referências, vídeos e comunidades](REFERENCIAS.md) para fontes oficiais e
o [glossário](GLOSSARIO.md) quando um termo não estiver claro. Use o
[caderno de práticas](CADERNO-PRATICAS.md) para consolidar cada fase e montar
as evidências do portfólio.

## Avaliação e critério de conclusão

A conclusão exige comportamento demonstrável, não apenas marcar páginas como
lidas. O denominador oficial de prática é o conjunto de **39 exercícios
numerados** do [Caderno de práticas](CADERNO-PRATICAS.md); exercícios adicionais
nos capítulos e guias são reforço e não alteram essa conta.

- [ ] completei pelo menos 28 dos 39 exercícios canônicos, todos os cinco labs
      e todos os checkpoints;
- [ ] consigo transformar um enunciado em casos, algoritmo e testes;
- [ ] implemento condições, laços, funções, coleções e tratamento de erros sem
      depender de uma solução pronta;
- [ ] consigo explicar stack, heap, processo, thread, evento e promessa;
- [ ] justifico uma estrutura de dados e analiso seu custo predominante;
- [ ] executei e modifiquei exemplos nas cinco linguagens;
- [ ] escrevi testes de unidade, integração e contrato pequenos;
- [ ] consigo explicar métodos, status, cabeçalhos e corpo de uma mensagem HTTP;
- [ ] o TaskBoard passa nos testes e responde apenas no endereço local previsto;
- [ ] explico cada instrução relevante dos Dockerfiles, Compose e Nginx;
- [ ] apresentei o projeto final, incluindo decisões, limites, falhas encontradas
      e melhorias futuras;
- [ ] `bash 00-Fundamentos/programacao/testar-curso.sh --require-all` termina
      com sucesso, sem verificação pulada.

Se você não consegue explicar uma linha importante, o artefato ainda não é sua
evidência de aprendizagem. Volte ao menor exemplo, observe-o e reconstrua-o.
