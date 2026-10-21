# Exercícios MongoDB

Execute [`001_setup.js`](../laboratorios/mongodb/001_setup.js),
[`002_queries.js`](../laboratorios/mongodb/002_queries.js) e
[`003_assertions.js`](../laboratorios/mongodb/003_assertions.js) no container do
laboratório. O [Lab 03](../laboratorios/lab-03-mongodb-documentos.md) explica a
progressão, e o runner
[`testar-laboratorios.sh`](../laboratorios/testar-laboratorios.sh) cria e limpa um
ambiente efêmero. Depois:

1. adicione evento com `payload` inválido e observe a validação;
2. consulte histórico por agregado e leia `executionStats`;
3. agrupe eventos por dia e tipo;
4. crie um índice desnecessário, meça tamanho e remova;
5. escreva migration idempotente que acrescente `schemaVersion` aos documentos antigos.
