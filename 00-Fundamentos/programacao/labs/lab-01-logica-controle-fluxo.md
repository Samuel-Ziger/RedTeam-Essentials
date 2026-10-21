# Lab 01 — lógica, controle de fluxo e limites

## Objetivo

Transformar regras escritas em tabela de decisão, funções, testes e CLI pequena.
O laboratório verifica condições completas, ordem de ramos, laços que terminam
e tratamento explícito de entrada inválida.

## Tempo e ambiente

- 3 a 5 horas;
- Python 3.12 ou superior;
- editor e terminal;
- nenhum pacote externo.

## Cenário

Uma aplicação local recebe leituras horárias de consumo elétrico sintético,
entre 0 e 20 kWh. Ela precisa classificar cada leitura:

| Intervalo | Categoria |
|-----------|-----------|
| 0 até menor que 2 | baixo |
| 2 até menor que 5 | moderado |
| 5 até menor que 10 | alto |
| 10 até 20 | crítico |

O relatório contém quantidade, média com duas casas, maior leitura e frequência
de cada categoria.

## Parte 1 — antes do código

1. Reescreva as regras como intervalos matemáticos.
2. Faça uma tabela para os valores -0.01, 0, 1.99, 2, 4.99, 5, 9.99, 10, 20 e
   20.01.
3. Defina o comportamento de lista vazia, texto, infinito e valor ausente.
4. Escreva pseudocódigo para classificar uma leitura.
5. Identifique uma invariante do laço que calcula total e frequências.

Não programe antes de a tabela não possuir lacuna nem sobreposição.

## Parte 2 — núcleo funcional

Implemente:

- <code>classificar(leitura)</code>;
- <code>resumir(leituras)</code>;
- retorno estruturado em dicionário;
- validação que rejeita booleano, não finito e valor fora do intervalo;
- nenhuma impressão dentro dessas duas funções.

O núcleo deve ser utilizável por CLI ou teste. Não altere a coleção recebida.

## Parte 3 — testes

Use <code>unittest</code>. Cubra:

- todos os limites da tabela;
- um valor comum por categoria;
- coleção com uma leitura;
- coleção com categorias repetidas;
- lista vazia;
- tipo incompatível;
- infinito e NaN;
- prova de que a entrada não foi alterada.

Faça uma mutação manual: troque uma comparação de limite. Pelo menos um teste
deve falhar. Restaure e execute novamente.

## Parte 4 — CLI

Contrato sugerido:

    python3 consumo.py LEITURA [LEITURA ...]

No sucesso:

- escreva JSON em saída normal;
- termine com código 0.

Em erro de uso:

- escreva mensagem curta em saída de erro;
- termine com código 2;
- não imprima stack trace para erro esperado.

## Experimento de depuração

Introduza um erro no divisor da média. Use uma tabela de rastreamento para achar
a primeira divergência. Registre:

- comando de reprodução;
- esperado e observado;
- hipótese;
- estado inspecionado;
- causa;
- teste de regressão.

## Critérios de aceite

- [ ] Todos os intervalos são completos e mutuamente exclusivos.
- [ ] Os dez valores de limite têm comportamento documentado.
- [ ] O núcleo não depende do terminal.
- [ ] A CLI separa dados e diagnóstico.
- [ ] Os testes detectam uma mutação de condição.
- [ ] O laço possui invariante e término explicados.
- [ ] A investigação diferencia sintoma e causa.

## Evidência

Entregue fonte, testes, tabela de decisão, comando de execução, saída de exemplo
e relatório de depuração. Não entregue somente captura de tela.
