# Lab 05 — capstone Dependency Planner

## Objetivo

Executar, explicar e evoluir o projeto de referência como um produto pequeno.
A conclusão exige mais que a suíte verde: outra pessoa deve conseguir instalar,
operar, diagnosticar, revisar e continuar a evolução sem conhecimento oculto.

## Pré-requisitos e tempo

- capítulos 00–16;
- Labs 01–04 concluídos;
- [README do projeto](../projetos/dependency-planner/README.md);
- [caderno de práticas](../CADERNO-PRATICAS.md);
- 20 a 32 horas.

## Fase 1 — linha de base e mapa

Execute:

```bash
bash 02-OSINT/engenharia-software/testar-curso.sh

PYTHONPATH=02-OSINT/engenharia-software/projetos/dependency-planner/src \
  python3 -m dependency_planner.cli \
  02-OSINT/engenharia-software/projetos/dependency-planner/fixtures/valid-project.json \
  --format json
```

Associe cada responsabilidade a um arquivo e desenhe o fluxo:

```text
argv -> CLI/composition root
          | cria JsonWorkItemRepository e injeta em PlanProject
          v
       PlanProject (caso de uso) -> WorkItemRepository (porta)
                                      ^
                                      | implementa
                              JsonWorkItemRepository -> bytes/JSON -> WorkItem
          |
          +-> build_plan -> domain + graph -> Plan
          |
          +-> CLI formata Plan -> stdout; traduz erro -> stderr + exit code
```

Explique onde nascem validação local, referência desconhecida, ciclo, erro de
I/O e formatação. Localizar cada decisão vale mais que recitar o nome da camada.

## Fase 2 — matriz de comportamento

Automatize uma matriz com:

| Caso | status | stdout | stderr | propriedade |
|---|---:|---|---|---|
| válido/texto | 0 | plano | vazio | ordem válida |
| válido/JSON | 0 | JSON | vazio | schema e determinismo |
| vazio | 0 | plano vazio | vazio | duração zero |
| JSON inválido | 2 | vazio | erro | sem traceback |
| referência ausente | 2 | vazio | erro | ID citado |
| ciclo | 2 | vazio | erro | caminho fechado |
| arquivo ausente | 2 | vazio | erro | caminho citado |

Teste o processo real, não apenas `main()` em memória. Não dependa do
diretório atual nem de locale implícito.

## Fase 3 — mudança vertical obrigatória

Implemente **uma** capacidade completa:

1. adapter CSV rigoroso;
2. exportação Graphviz DOT com escaping correto;
3. calendário com capacidade limitada e política documentada;
4. filtro de subgrafo preservando dependências transitivas necessárias;
5. explicação de bloqueio para cada tarefa ainda não liberada.

Antes do código, entregue:

- requisito e exemplos;
- invariantes e casos-limite;
- efeito sobre complexidade;
- contrato de CLI/arquivo;
- ameaças de entrada e limites;
- ADR se houver decisão duradoura;
- plano de teste e rollback.

A mudança deve atravessar adapter/caso de uso/apresentação somente quando
necessário. Não coloque regra de domínio na CLI para terminar mais rápido.

## Fase 4 — qualidade e desempenho

- adicione pelo menos um teste unitário, um de contrato e um integrado;
- gere DAGs reproduzíveis e verifique propriedades;
- mate cinco mutações relevantes;
- meça duas formas de grafo com `V` e `E` registrados;
- defina um orçamento razoável para seu ambiente;
- valide arquivo e quantidade de itens antes de consumo descontrolado;
- execute as implementações nas cinco linguagens quando as toolchains existirem.

Resultado mais rápido numa execução não autoriza afirmação universal. Guarde
versão, hardware, entrada, repetições e dispersão.

## Fase 5 — operação e diagnóstico

Use o [guia de diagnóstico](../GUIA-DIAGNOSTICO.md) para investigar dois
defeitos controlados: um resultado incorreto e uma regressão de desempenho.
Registre sintoma, menor reprodução, hipótese, evidência, correção e teste.

Acrescente ao projeto:

- instalação e desinstalação;
- exemplos mínimos;
- códigos de saída;
- limites conhecidos;
- procedimento de atualização/rollback;
- política de compatibilidade do formato.

## Fase 6 — defesa técnica

Responda sem consultar o código:

1. qual é o sentido de cada aresta e como ele afeta o grau;
2. por que o heap muda o custo e a saída;
3. como o ciclo é distinguido de referência desconhecida;
4. por que o caminho crítico funciona somente após uma ordem topológica;
5. quais garantias pertencem ao domínio e quais ao adapter;
6. onde uma entrada grande pode esgotar recursos;
7. que alternativa você rejeitou e sob qual gatilho revisaria a decisão;
8. qual teste detectaria uma mudança acidental de determinismo.

## Gate de conclusão

- runner e matriz de CLI passam;
- mudança vertical possui requisito, código, testes e documentação;
- propriedades e mutações demonstram força da suíte;
- benchmark é reproduzível e interpretado com cautela;
- dois diagnósticos chegam à primeira fronteira divergente;
- histórico é revisável e pode ser revertido;
- a defesa alcança pelo menos 75% da rubrica do capítulo 16.
