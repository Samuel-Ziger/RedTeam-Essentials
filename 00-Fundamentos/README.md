# 00 — Fundamentos, programação e segurança do laboratório

O módulo 00 constrói a base técnica usada por todos os módulos seguintes. Ele
parte do primeiro algoritmo e termina quando você consegue desenvolver, testar,
explicar e executar localmente uma aplicação pequena com frontend, API, banco,
Docker e Nginx.

Não há exploração ofensiva neste módulo. Os exemplos usam somente dados
sintéticos, arquivos do curso e serviços publicados no próprio computador.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Pessoas sem experiência em programação ou que precisam reconstruir os fundamentos com rigor. |
| Pré-requisitos | Saber instalar software e administrar a própria máquina; nenhuma linguagem de programação é exigida. |
| Tempo estimado | 250 a 390 horas, incluindo leitura ativa, exercícios, depuração, testes e os cinco projetos. |
| Ambiente | Computador local, editor, terminal, Git e runtimes descritos no curso; Docker é necessário apenas na etapa final. |
| Evidência final | Portfólio com exercícios, exemplos modificados nas cinco linguagens e aplicação web local conteinerizada. |
| Critério de conclusão | Passar a suíte local, concluir os checkpoints e defender as decisões técnicas sem copiar a solução. |

## Limite deste módulo

Aqui você aprende programação e operação local segura. Administração profunda de
sistemas, redes, criptografia e segurança ofensiva/defensiva pertence aos
módulos específicos da formação.

O aprofundamento em governança de laboratório e regras de engajamento começa
no [módulo 27](../27-Operacoes-Seguranca-Avancadas/README.md), depois da base
obrigatória. Aqui vale apenas o conjunto mínimo de segurança descrito abaixo.

## Resultado observável

Ao concluir, você deverá ser capaz de:

- decompor uma necessidade em entradas, regras, saídas e casos de erro;
- rastrear variáveis e explicar o fluxo de um algoritmo;
- implementar condições, repetições, funções, módulos e coleções;
- distinguir tipo, valor, referência, identidade, mutabilidade, escopo e
  lifetime;
- escolher estruturas de dados a partir das operações e analisar custos;
- construir programas executáveis em Python, JavaScript, Java, C e C#;
- compilar, interpretar, testar, depurar e versionar código;
- modelar domínio com invariantes e fronteiras explícitas;
- validar entradas e tratar erros sem esconder a causa;
- escrever testes unitários, de integração, contrato e regressão;
- explicar processo, thread, memória, I/O, concorrência e assincronicidade;
- implementar uma API HTTP pequena com persistência SQLite;
- explicar método, caminho, cabeçalho, corpo e status HTTP;
- construir e observar containers, rede e volume de um Compose local;
- explicar o caminho navegador → Nginx → API → banco → resposta;
- proteger segredos, limitar exposição local e remover os recursos do
  laboratório depois do uso.

## Ordem obrigatória

1. Leia este documento e prepare um diretório exclusivo para exercícios.
2. Faça o diagnóstico inicial abaixo sem consultar respostas.
3. Siga o [curso de programação](programacao/README.md) na ordem das fases e
   conclua cada laboratório quando ele for liberado; não deixe todos para o fim.
4. Use o [guia de depuração](programacao/GUIA-DEPURACAO.md) desde o primeiro
   erro e registre as entregas no
   [caderno de práticas](programacao/CADERNO-PRATICAS.md).
5. Depois do capítulo 08, leia o briefing de
   [projetos e avaliações](programacao/09-projetos.md). O Lab 05 realiza as
   fases guiadas A–B do TaskBoard; reutilize essa evidência e conclua as fases
   autorais C–D, em vez de repetir o mesmo trabalho.
6. Entregue os demais projetos e o projeto final descritos no briefing.
7. Execute a validação completa e faça a defesa final.

As [referências externas](programacao/REFERENCIAS.md) são complementares. O
material local deve ser suficiente para executar os exemplos e cumprir os
critérios.

## Diagnóstico inicial

Faça estas tarefas antes de estudar. O objetivo não é acertar tudo, mas produzir
uma linha de base para comparar no final:

1. escreva pseudocódigo que receba três números e informe o maior;
2. explique a diferença entre imprimir um valor e retorná-lo;
3. diga o que um laço precisa para não executar indefinidamente;
4. escolha entre lista e mapa para buscar pessoa por ID e justifique;
5. descreva o que ocorre entre digitar uma URL e receber uma página;
6. explique o que um teste deve provar;
7. interprete, se conseguir, um stack trace simples;
8. diferencie processo, programa e container;
9. descreva onde uma aplicação deveria receber configuração e segredos;
10. implemente o analisador de notas mais simples que conseguir.

Guarde a resposta com data. Refaça ao terminar e compare precisão, vocabulário,
casos de erro e capacidade de produzir evidência.

## Regras mínimas para um ambiente seguro

### 1. Use apenas alvos próprios e locais

Os serviços do módulo devem escutar no loopback:

- <code>127.0.0.1</code> em IPv4;
- <code>::1</code> em IPv6;
- <code>localhost</code> quando a resolução local estiver correta.

<code>0.0.0.0</code> não significa “este computador”: significa todas as
interfaces IPv4 disponíveis para bind. Em Docker, uma publicação como
<code>127.0.0.1:8099:8080</code> limita o acesso pelo host; uma publicação sem o
endereço pode expor o serviço à rede local, dependendo do ambiente.

Antes de iniciar:

    docker compose config
    docker compose ps

Depois, confirme a porta local esperada e não altere a publicação sem entender
o impacto.

### 2. Dados sempre sintéticos

Use nomes como “Pessoa Exemplo”, domínios reservados como
<code>example.test</code> e tokens fictícios. Não importe histórico do navegador,
agenda, e-mail, arquivo corporativo ou dump real para os exercícios.

Um dado não deixa de ser sensível apenas porque o repositório é privado.

### 3. Segredos não pertencem ao código

Senha, token, cookie, chave privada e credencial de nuvem não devem aparecer em:

- arquivo versionado;
- argumento visível na lista de processos;
- log ou captura de tela;
- imagem Docker;
- exemplo enviado a fórum.

O curso demonstra configuração, mas não exige segredo real. Quando uma variável
for necessária, documente o nome e use valor fictício local.

### 4. Menor privilégio

Não execute editor, servidor ou script como administrador/root sem necessidade
específica e compreendida. Um erro em processo privilegiado possui impacto
maior. Containers também devem usar usuário não privilegiado quando o caso
permitir.

### 5. Cleanup é parte do exercício

Saiba exatamente o que será removido. Para o TaskBoard, use o arquivo Compose do
projeto e execute os comandos no diretório indicado. Não use globs, diretórios
amplos ou comandos destrutivos copiados sem inspeção.

O laboratório deve documentar:

- recursos criados;
- estado esperado;
- comando de parada;
- persistência que será preservada;
- remoção explícita de volume quando os dados não forem mais necessários.

## Preparação técnica

Comece com:

    python3 --version
    git --version

Instale os demais runtimes apenas quando chegar ao guia correspondente. Isso
reduz variáveis durante a aprendizagem. O
[script de validação](programacao/testar-curso.sh) pula, no modo incremental,
ferramentas ainda indisponíveis e informa o que não foi executado.

Verificação completa a partir da raiz do repositório:

    bash 00-Fundamentos/programacao/testar-curso.sh --require-all

Sem a opção, o script continua útil durante o estudo: executa o que estiver
disponível e marca ausências como “pulado”. Um resultado pulado não equivale a
aprovado; `--require-all` transforma qualquer ausência em falha. Antes de
concluir o módulo, instale ou use ambiente compatível para executar as cinco
linguagens e a validação do Compose.

## Vídeos em português

Estes vídeos oferecem uma segunda explicação; o texto local, os exemplos e os
laboratórios continuam sendo o percurso completo. Verifique sempre a versão da
ferramenta usada na aula.

1. [Primeiros passos na carreira de programação](https://www.youtube.com/watch?v=Oj26AOVuLYw) — **Curso em Vídeo**.
2. [Python #01 — Seja um Programador](https://www.youtube.com/watch?v=S9uPNppGsGo) — **Curso em Vídeo**.
3. [POO Java — instalação e primeiro ambiente](https://www.youtube.com/watch?v=Ucyx_QPfDng) — **Curso em Vídeo**.
4. [Linguagem C — curso completo](https://www.youtube.com/watch?v=2dPbemvBwW4) — **Prof. Saulo Santos**.
5. [Curso completo de C# — aula 1](https://www.youtube.com/watch?v=dVzJ3bx68FA) — **CFB Cursos**.
6. [JavaScript — primeiros passos](https://www.youtube.com/watch?v=Ptbk2af68e8) — **Curso em Vídeo**.

## Como produzir evidência

Cada checkpoint deve deixar um artefato verificável:

| Aprendizado | Evidência forte | Evidência fraca |
|-------------|-----------------|-----------------|
| condição | tabela de decisão, código e testes de limite | captura da saída comum |
| algoritmo | invariante, análise de custo e casos | dizer que “parece rápido” |
| correção | teste que falha antes e passa depois | alterar até parar de falhar |
| depuração | reprodução mínima, hipótese e primeira divergência | somente stack trace |
| API | contrato, testes de status/schema e logs | coleção manual sem asserções |
| container | build reproduzível, healthcheck e cleanup | container que iniciou uma vez |

Mantenha commits pequenos. Uma mensagem como “corrige limite de conceito B e
adiciona regressão para nota 7” preserva mais informação que “ajustes”.

## Projeto integrador

O [TaskBoard](programacao/projetos/taskboard/README.md) conecta os conceitos:

    navegador
        |
        v
    Nginx (arquivos estáticos e proxy /api)
        |
        v
    API Python (validação e contrato HTTP)
        |
        v
    SQLite (transações e persistência)

Você deve conseguir executar a API sem Docker antes de executar a pilha
conteinerizada. Essa separação evita atribuir ao Docker um erro da aplicação.

Na defesa, escolha uma requisição e explique:

1. qual evento do navegador a iniciou;
2. qual mensagem HTTP foi criada;
3. como Nginx selecionou o destino;
4. onde a API validou a entrada;
5. qual transação ocorreu;
6. como status e corpo foram definidos;
7. onde observar uma falha;
8. quais recursos permanecem após reiniciar;
9. como remover tudo com segurança.

## Autoavaliação final

Marque apenas depois de demonstrar:

- [ ] transformo requisitos em exemplos e critérios de aceite;
- [ ] explico cada ramo de um <code>if/else</code> e seus limites;
- [ ] escolho um laço e demonstro por que termina;
- [ ] separo parsing, validação, domínio e apresentação;
- [ ] justifico lista, conjunto, mapa, fila ou pilha pelas operações;
- [ ] sei quando uma estimativa Big O não substitui medição;
- [ ] leio código de saída, <code>stdout</code>, <code>stderr</code> e stack trace;
- [ ] escrevo teste que detecta uma mutação da regra;
- [ ] executo e modifico programas nas cinco linguagens;
- [ ] explico stack, heap e lifetime sem afirmar que funcionam igualmente em
      todas as linguagens;
- [ ] diferencio concorrência, paralelismo e assincronicidade;
- [ ] explico método, URL, status, cabeçalho, JSON e idempotência;
- [ ] uso transação e justifico ao menos um índice;
- [ ] consigo seguir uma requisição completa no TaskBoard;
- [ ] sei por que <code>127.0.0.1</code> e <code>0.0.0.0</code> não são
      equivalentes;
- [ ] nenhum segredo ou dado real aparece no portfólio;
- [ ] a suíte do curso passa nos runtimes exigidos;
- [ ] consigo destruir somente os recursos criados para o laboratório.

## Depois do módulo 00

Siga a ordem canônica da formação pelo [catálogo de módulos](../README.md). Os
módulos 01–26 aprofundam dados, engenharia, sistemas operacionais, redes,
criptografia, privacidade e proteção de aplicações. A especialização prática de
segurança começa no módulo 27 somente depois da base obrigatória.
