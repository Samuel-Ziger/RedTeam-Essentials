# Lab 04 — evolução segura, arquitetura e testes

## Resultado esperado

Você receberá uma implementação acoplada, preservará seu comportamento com
characterization tests, extrairá fronteiras em passos reversíveis e registrará
as decisões arquiteturais. O objetivo não é produzir um diagrama idealizado: é
demonstrar mudança segura com evidência.

## Pré-requisitos e tempo

- capítulos 11 a 15;
- [guia de diagnóstico](../GUIA-DIAGNOSTICO.md);
- Labs 01–03 concluídos;
- 14 a 22 horas.

## Fixture legado

Crie em branch própria um script pequeno que, numa única função:

1. abre JSON por caminho global;
2. converte campos sem validação explícita;
3. calcula uma ordem;
4. imprime diretamente;
5. chama relógio para compor a saída;
6. captura toda exceção e retorna sucesso.

Ele deve ser deliberadamente ruim, mas benigno e pequeno. Preserve o fixture
no teste, não como nova implementação de produção.

## Parte 1 — caracterize antes de corrigir

Capture para três entradas:

- bytes de `stdout` e `stderr`;
- código de saída;
- arquivos lidos ou criados;
- comportamento com campo ausente;
- dependência do relógio.

Um characterization test descreve o que existe, inclusive comportamento
indesejado. Marque explicitamente o que será preservado e o que é defeito a ser
corrigido por requisito novo. Não transforme acidente em contrato sem decisão.

## Parte 2 — requisitos e rastreabilidade

Escreva uma tabela:

| ID | requisito/cenário | risco | teste | evidência |
|---|---|---|---|---|
| REQ-01 | ordem respeita toda dependência | alto | propriedade topológica | teste |
| QUA-01 | 100 mil itens dentro do orçamento acordado | médio | benchmark | relatório |
| OPS-01 | erro de entrada não gera saída parcial | alto | CLI | status/stderr |

Cada atributo de qualidade precisa de estímulo, ambiente, resposta e medida.
“Rápido”, “escalável” ou “seguro” sem cenário não são verificáveis.

## Parte 3 — passos de refatoração

Faça commits pequenos e verdes:

1. introduza relógio injetável;
2. separe parse de leitura;
3. extraia cálculo puro;
4. transforme `print` em valor retornado;
5. traduza erros somente na borda;
6. substitua globais por composition root;
7. troque o caminho legado pelo caso de uso novo;
8. remova a implementação antiga quando houver equivalência.

Após cada passo, rode a suíte. Registre tempo de rollback e evite misturar
formatação massiva com mudança comportamental.

## Parte 4 — arquitetura e ADR

Desenhe contexto, contêiner/processo e componentes relevantes. Mostre usuário,
CLI, caso de uso, domínio e adapters; não desenhe classes sem ajudar uma decisão.

Escreva um ADR com:

- contexto e forças;
- decisão;
- alternativas reais;
- consequências positivas e negativas;
- gatilho de revisão;
- estado (`proposta`, `aceita`, `substituída`).

Compare monólito modular com serviços separados. Para este projeto local,
serviços distribuídos devem justificar falha parcial, serialização, deploy,
observabilidade e consistência adicionais.

## Parte 5 — qualidade adversarial

Execute:

- testes unitários do núcleo;
- testes de contrato dos adapters;
- teste integrado da CLI;
- propriedades sobre DAGs gerados;
- mutações manuais de regras centrais;
- benchmark fora da suíte funcional;
- entrada malformada e acima do limite.

Introduza um teste flaky usando tempo real ou ordem de hash, observe a falha e
remova a causa. Não resolva com `sleep` maior ou retry indiscriminado.

## Parte 6 — revisão simulada

Prepare uma descrição de pull request com problema, escopo, risco, como testar,
rollback e evidência. Faça uma revisão procurando, nesta ordem:

1. contrato/correção;
2. segurança e perda de dados;
3. concorrência/recursos;
4. operabilidade;
5. clareza;
6. estilo automatizável.

## Gate de conclusão

- comportamento inicial foi caracterizado antes da refatoração;
- requisitos importantes ligam-se a testes/evidências;
- histórico possui passos reversíveis e verdes;
- ADR registra custos e gatilho de revisão;
- a arquitetura desenhada corresponde aos imports e ao runtime;
- teste instável foi corrigido na causa;
- a revisão distingue bloqueio de preferência.

