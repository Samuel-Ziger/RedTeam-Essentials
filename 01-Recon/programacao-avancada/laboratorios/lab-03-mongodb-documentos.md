# Lab 03 — documentos, validação e índices no MongoDB

## Resultado esperado

Modelar eventos de auditoria como documentos, impor um contrato mínimo e provar
consultas e agregações com dados reais do laboratório. MongoDB flexível não
significa MongoDB sem schema.

## Pré-requisitos e tempo

- capítulos 06 e 07;
- Labs 01 e 02 recomendados para comparação entre modelos;
- 8 a 12 horas;
- host compatível com a versão do MongoDB descrita no
  [README do laboratório](README.md).

## Materiais

- [`mongodb/001_setup.js`](mongodb/001_setup.js): collection, validator,
  índices e eventos;
- [`mongodb/002_queries.js`](mongodb/002_queries.js): histórico, agregação e
  plano;
- [`mongodb/003_assertions.js`](mongodb/003_assertions.js): contrato executável;
- [`compose.yaml`](compose.yaml): serviço isolado sem porta publicada.
- [guia dos scripts MongoDB](../referencias/GUIA-LAB-MONGODB.md): ordem e
  exercícios adicionais.

Execute todo o fluxo efêmero:

```bash
bash 01-Recon/programacao-avancada/laboratorios/testar-laboratorios.sh \
  --mongo-only
```

O resultado final deve informar dez asserções. O script remove os recursos que
criou mesmo após falha.

## Parte 1 — fronteira do agregado

Para cada campo do evento, classifique:

- identidade/idempotência;
- roteamento para agregado;
- ordenação;
- evolução de contrato;
- conteúdo específico do evento.

Explique por que `eventId` é único e por que o índice de histórico termina com
`eventId`: instantes iguais ainda precisam de uma ordem determinística.

## Parte 2 — validator na prática

No `mongosh`, tente inserir separadamente:

1. evento sem `eventId`;
2. `occurredAt` como string;
3. `schemaVersion` como número de ponto flutuante;
4. `payload` como array;
5. `eventId` já existente.

Registre `code`, `codeName` e trecho relevante de `errInfo`, sem copiar logs
inteiros. Identifique quais falhas vêm do validator e qual vem do índice.

## Parte 3 — shape orientado à leitura

Implemente duas consultas:

1. últimos N eventos de um produto, com projeção mínima;
2. saldo de estoque por produto, contando somente `stock.adjusted`.

Compare sua resposta com [`002_queries.js`](mongodb/002_queries.js). Rode
`explain("executionStats")` com e sem `hint` e descreva `nReturned`,
`totalKeysExamined` e `totalDocsExamined`. Em coleção minúscula o otimizador pode
preferir scan; isso não invalida o índice, mas impede conclusões de performance.

## Parte 4 — evolução de schema idempotente

Em sua cópia, insira evento legado sem `schemaVersion` antes de habilitar o
validator estrito. Escreva migration que:

- seleciona somente documentos sem o campo;
- define `NumberInt(1)`;
- pode rodar duas vezes com segunda modificação igual a zero;
- registra quantidade encontrada e alterada;
- só depois endurece a validação.

Explique diferença entre compatibilidade de leitura e de escrita durante um
rolling deploy.

## Parte 5 — escolha consciente entre embedding e referência

Projete comentários de auditoria em dois formatos: embutidos no evento e em
collection separada. Avalie crescimento, atomicidade, paginação, retenção,
controle de acesso e consultas. Escolha um e escreva a consulta principal.

## Gate de conclusão

- setup, consultas e asserções terminam com código zero;
- cinco entradas inválidas são rejeitadas pela camada esperada;
- migration é idempotente;
- ao menos um plano é interpretado;
- você justifica documento versus relação com padrões de acesso concretos.
