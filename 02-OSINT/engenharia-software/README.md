# Engenharia de software: do problema ao sistema sustentável

Esta é a terceira etapa da trilha de programação. Os módulos anteriores ensinaram
a programar e a construir APIs orientadas a dados; aqui o foco muda de **fazer o
código funcionar** para **escolher estruturas, desenhar limites, testar decisões e
manter sistemas em equipe**.

O material é autocontido. Vídeos, livros, fóruns e documentação oficial aparecem
em [REFERENCIAS.md](REFERENCIAS.md) como aprofundamento, não como pré-requisito.
Todos os exemplos são benignos e usam um planejador de dependências fictício.

## Contrato de aprendizagem

| Campo | Definição |
|---|---|
| Público | Quem concluiu as trilhas de programação dos módulos 00 e 01 |
| Carga estimada | 260 a 380 horas, incluindo práticas, cinco labs, projeto e revisão |
| Linguagens | Python, Java, C17, C# e JavaScript |
| Ambiente | Linux, macOS ou WSL; Git e toolchains das linguagens |
| Evidência final | Projeto executável, propriedades, testes, medições, ADRs, revisão e defesa técnica |
| Conclusão | Cinco labs concluídos, pelo menos 75% na rubrica e nenhum requisito essencial ausente |

## O que você será capaz de fazer

- decompor problemas antes de escrever código;
- justificar complexidade de tempo e memória;
- implementar e escolher listas, tabelas hash, árvores, heaps e grafos;
- aplicar busca, ordenação, recursão, programação dinâmica e algoritmos gulosos;
- separar domínio, casos de uso e infraestrutura;
- reconhecer trade-offs de SOLID, padrões e arquiteturas;
- refatorar código legado com uma rede de segurança;
- modelar requisitos, escrever ADRs e documentar contratos;
- criar testes úteis e integrar qualidade ao fluxo de colaboração;
- entregar uma aplicação pequena que outra pessoa consegue operar e evoluir.

O objetivo não é decorar catálogos de algoritmos ou padrões. Ao concluir, você
deve conseguir partir de uma necessidade incompleta, explicitar o contrato,
escolher representação e estratégia, construir evidência de correção, medir sem
se enganar e manter a decisão compreensível para a equipe.

## Pré-requisitos verificáveis

Antes de iniciar, confirme que consegue:

- escrever, executar e testar programas pequenos em pelo menos duas linguagens;
- usar Git em branch, interpretar diff e reverter a própria mudança;
- trabalhar com funções, coleções, arquivos, erros e módulos;
- explicar HTTP, persistência e testes no nível dos módulos 00 e 01;
- executar comandos no terminal sem copiar dados ou segredos reais.

Se uma dessas habilidades ainda exigir tentativa aleatória, retome o capítulo
correspondente. Este curso explica os novos conceitos do zero, mas assume a
fluência básica construída nas etapas anteriores.

## Rota de estudo

| Etapa | Capítulos | Entrega sugerida |
|---|---|---|
| 1. Raciocínio | 00–01 + Lab 01 | especificação, oráculo, custo e medição |
| 2. Estruturas e algoritmos | 02–05 + Lab 02 | representações, propriedades e mutações |
| 3. Estratégias e design | 06–10 + projeto-base + Lab 03 | recursão, DP, tipos, portas e padrões |
| 4. Evolução | 11–15 + Lab 04 | requisitos, arquitetura, refatoração e qualidade |
| 5. Síntese | revisita do projeto + 16 + Lab 05 | mudança vertical, portfólio e defesa técnica |

Leia na ordem na primeira passagem:

1. [Pensar problemas](00-como-pensar-problemas.md)
2. [Complexidade](01-complexidade.md)
3. [Lab 01 — contrato e complexidade](laboratorios/lab-01-contrato-complexidade.md)
4. [Estruturas lineares e tabelas hash](02-estruturas-lineares.md)
5. [Árvores, heaps e tries](03-arvores-heaps-tries.md)
6. [Grafos](04-grafos.md)
7. [Busca e ordenação](05-busca-ordenacao.md)
8. [Exemplos comparados nas cinco linguagens](exemplos/README.md)
9. [Lab 02 — estruturas, busca e grafos](laboratorios/lab-02-estruturas-grafos.md)
10. [Recursão e backtracking](06-recursao-backtracking.md)
11. [Programação dinâmica e algoritmos gulosos](07-programacao-dinamica-gulosa.md)
12. [Paradigmas e tipos](08-paradigmas-tipos.md)
13. [Design modular](09-design-modular.md)
14. [SOLID e padrões](10-solid-patterns.md)
15. [Projeto-base Dependency Planner](projetos/dependency-planner/README.md)
16. [Lab 03 — estratégias e design modular](laboratorios/lab-03-estrategias-design.md)
17. [Refatoração e legado](11-refatoracao-legado.md)
18. [Requisitos e modelagem](12-requisitos-modelagem.md)
19. [Arquitetura](13-arquitetura.md)
20. [Testes e qualidade](14-testes-qualidade.md)
21. [Colaboração e documentação](15-colaboracao-documentacao.md)
22. [Guia de diagnóstico](GUIA-DIAGNOSTICO.md)
23. [Lab 04 — evolução, arquitetura e testes](laboratorios/lab-04-evolucao-arquitetura-testes.md)
24. [Caderno de práticas](CADERNO-PRATICAS.md)
25. [Projetos e avaliação](16-projetos-avaliacao.md)
26. [Lab 05 — capstone Dependency Planner](laboratorios/lab-05-dependency-planner.md)

Use também o [índice dos laboratórios](laboratorios/README.md), as
[respostas orientativas](RESPOSTAS.md), o [glossário](GLOSSARIO.md) e as
[referências](REFERENCIAS.md). Respostas são critérios de raciocínio, não
implementações para copiar.

## Código executável

O mesmo problema — ordenar tarefas respeitando dependências e detectar ciclos —
é implementado nas cinco linguagens. Compare modelos de dados, erros e testes:

- [Python](exemplos/python/dependency_graph.py)
- [Java](exemplos/java/DependencyPlanner.java)
- [C17](exemplos/c/dependency_graph.c)
- [C#](exemplos/csharp/Program.cs)
- [JavaScript](exemplos/javascript/dependencyGraph.mjs)

O [guia comparativo](exemplos/README.md) explicita contrato, estruturas, limites,
complexidade e diferenças idiomáticas. A meta não é traduzir sintaxe linha por
linha, mas reconhecer quais garantias precisam sobreviver em cada linguagem.

O [Dependency Planner](projetos/dependency-planner/README.md) é o projeto de
referência. Ele transforma os conceitos em uma aplicação em camadas, com CLI,
adaptador JSON, regras de domínio, testes, caminho crítico e saída reproduzível.

Para validar tudo o que estiver disponível na sua máquina:

```bash
bash 02-OSINT/engenharia-software/testar-curso.sh
```

Toolchains ausentes são informados como `SKIP`; uma ferramenta instalada que
falha torna a validação inválida.

## Ciclo de aprendizagem e evidência

Para cada conceito, percorra quatro níveis:

1. **explicar:** defina contrato, invariante e vocabulário sem depender do código;
2. **prever:** antecipe saída, custo e falha para um fixture novo;
3. **construir:** implemente e teste em uma linguagem;
4. **transferir:** compare outra linguagem ou representação e defenda o trade-off.

Guarde especificação, comandos, testes, medições e decisões no repositório. Uma
explicação posterior sem a hipótese original perde informação sobre seu modelo
mental.

## Método para cada capítulo

1. Leia e reescreva os conceitos com suas palavras.
2. Execute o exemplo antes de modificá-lo.
3. Faça os exercícios sem copiar a solução.
4. Registre hipótese, decisão, resultado e dúvida em um diário técnico.
5. Explique sua solução em voz alta, incluindo custo e limitações.
6. Só então compare abordagens nas outras linguagens.

Memorizar uma implementação não é dominar o assunto. Você domina uma ideia
quando reconhece onde ela se aplica, onde falha e qual evidência sustenta a sua
escolha.

## Gates de progressão

Não avance apenas porque leu o último parágrafo:

- **após 01:** você especifica e analisa antes de medir;
- **após 05:** implementa propriedades de estruturas/grafos e explica custos;
- **após 10:** separa algoritmo, política e adapters sem abstração ornamental;
- **após 15:** evolui comportamento com requisitos, ADR, testes e revisão;
- **após 16:** entrega mudança vertical e defende alternativas e limitações.

Cada laboratório possui um gate verificável. Marcar o documento como lido na
aplicação registra progresso de estudo; concluir o lab exige as evidências nele
descritas.

## Política de uso

O conteúdo ensina engenharia de software de propósito geral. Ao aplicá-lo às
trilhas de segurança, use apenas dados sintéticos, sistemas próprios ou ativos
com autorização formal e siga [ETHICAL-USE.md](../../ETHICAL-USE.md).
