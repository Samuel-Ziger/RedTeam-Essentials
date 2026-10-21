# Lab 02 — CLI, Git e duas linguagens

## Objetivo

Implementar o mesmo contrato em Python e Java, usando o terminal e um histórico
Git que permita revisar a evolução. O percurso formal fixa Java como segunda
linguagem para que o aplicativo consiga verificar um pré-requisito inequívoco;
depois da entrega, repetir em C# ou JavaScript é uma extensão recomendada.

## Tempo e ambiente

- 6 a 9 horas;
- Python e Java 17 ou superior;
- Git;
- nenhum serviço externo.

## Contrato

O programa recebe uma ou mais notas de 0 a 10:

    programa NOTA [NOTA ...]

Ele produz:

- quantidade;
- média com duas casas;
- menor e maior;
- frequências A, B, C e D.

Regras:

- A: nota maior ou igual a 9;
- B: maior ou igual a 7 e menor que 9;
- C: maior ou igual a 5 e menor que 7;
- D: menor que 5;
- pelo menos uma nota é obrigatória;
- valores não finitos, texto parcial e fora da faixa são rejeitados;
- código de saída 0 indica sucesso e 2 indica uso inválido.

## Plano de commits

Crie commits pequenos nesta sequência:

1. contrato e casos em arquivo Markdown;
2. classificação e testes de limite;
3. resumo e testes de coleção;
4. adaptador CLI e códigos de saída;
5. implementação na segunda linguagem;
6. comparação e documentação.

Antes de cada commit, leia o diff. Não misture formatação ampla com mudança de
comportamento.

## Comparação obrigatória

Responda para as duas implementações:

| Aspecto | Pergunta |
|---------|----------|
| parsing | como um argumento se torna número e como a falha aparece? |
| tipo | o que é verificado antes e durante a execução? |
| coleção | como notas e frequências são representadas? |
| função | valor é copiado, referenciado ou depende do tipo? |
| erro | exceção, resultado ou código de retorno? |
| execução | fonte é interpretado, compilado ou executado por runtime? |
| teste | como selecionar e executar um único caso? |

Evite dizer que uma linguagem “não tem tipos” ou que compilação elimina erros
de execução.

## Experimentos Git

1. Crie branch para adicionar mediana.
2. Faça alteração e teste.
3. Compare a branch com a principal.
4. Integre a mudança.
5. Use o histórico para identificar qual commit introduziu uma mutação
   deliberada.
6. Reverta a mutação com um novo commit, preservando a história.

Não reescreva o histórico compartilhado como parte do laboratório.

## Critérios de aceite

- [ ] O mesmo conjunto de casos passa nas duas linguagens.
- [ ] Saída numérica é independente do locale documentado.
- [ ] Entrada inválida nunca é parcialmente aceita.
- [ ] Dados vão para saída normal e erros para saída de erro.
- [ ] O histórico contém os seis marcos planejados.
- [ ] A comparação usa modelos técnicos, não preferência pessoal.
- [ ] Uma regressão foi localizada pelo histórico e corrigida.

## Evidência

Entregue as duas implementações, testes, histórico resumido, comandos exatos de
build/execução e tabela comparativa preenchida.
