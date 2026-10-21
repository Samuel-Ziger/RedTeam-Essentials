# Laboratório 01 — Contrato, CLI, configuração e erros

## Objetivo

Transformar uma ideia curta em um produto observável pela linha de comando. A
entrega deve provar precedência de configuração, canais de saída, códigos de
processo e mensagens recuperáveis. Use uma das cinco linguagens como principal
e compare pelo menos um cenário com outra implementação de `exemplos/`.

## Cenário

Crie `focus-report`, uma aplicação que recebe uma lista local de sessões no
formato `assunto,minutos` e calcula total e agrupamento por assunto. A aplicação
não acessa rede nem banco. O problema é intencionalmente pequeno para que o
contrato de uso, e não o algoritmo, seja o centro.

Contrato mínimo:

```text
focus-report INPUT [--profile development|testing|production]
                   [--format text|json] [--min-minutes N]
```

`--profile` tem precedência sobre `APP_PROFILE`, que tem precedência sobre
`development`. Argumento inválido é erro de uso (`2`); arquivo ausente ou
ilegível é erro operacional documentado e diferente; sucesso é `0`.

## Preparação

1. Execute `bash ../testar-curso.sh` a partir da raiz do curso.
2. Leia o contrato comum em `../exemplos/README.md`.
3. Crie duas fixtures válidas, uma vazia e três inválidas.
4. Escreva critérios de aceite antes de implementar.

Não use parser CSV improvisado se o formato aceitar aspas ou vírgulas em campo.
Ou restrinja explicitamente o formato, ou use uma biblioteca apropriada da
linguagem. Uma decisão pequena, declarada e testada é melhor que suporte
acidental e inconsistente.

## Etapa A — Contrato de produto

Escreva uma página contendo:

- pessoa e tarefa principal;
- exemplo completo do primeiro uso;
- gramática dos argumentos e valores padrão;
- tabela `condição → canal → código → próxima ação`;
- limites de tamanho, duração e codificação;
- três não objetivos;
- critérios de aceite observáveis.

Inclua pelo menos estes estados: ajuda, sucesso vazio, sucesso com dados, opção
desconhecida, valor fora do domínio, arquivo ausente, entrada malformada e falha
de escrita. A ajuda deve funcionar mesmo se configuração ou arquivo estiverem
ausentes.

## Etapa B — Núcleo independente

Implemente funções sem acesso ao terminal ou ao ambiente para:

1. converter uma linha em registro validado;
2. filtrar pelo mínimo;
3. agregar minutos;
4. construir um objeto de resultado;
5. apresentar esse objeto como texto ou JSON.

Injete ambiente e argumentos na camada de entrada. Não leia `APP_PROFILE`
dentro do domínio. Teste a precedência com tabela de casos, incluindo string
vazia e valor desconhecido.

## Etapa C — Falhas e automação

Escreva um teste de processo para cada classe de saída. Para uma falha de uso,
prove simultaneamente:

- código exatamente `2`;
- `stdout` vazio;
- mensagem curta em `stderr`;
- nenhuma saída parcial criada;
- ajuda acessível por comando documentado.

Depois provoque uma falha operacional sem alterar permissões de diretórios do
sistema: use caminho inexistente ou um adapter falso que lança erro. Explique
por que ela não é erro de sintaxe.

## Etapa D — Comparação entre linguagens

Execute o mesmo vetor em sua solução e em duas implementações do diretório
`exemplos/`. Registre diferenças de parser, representação de ausência, processo
e teste. Não procure declarar uma linguagem “melhor”; compare como o mesmo
contrato fica visível em cada runtime.

## Testes mínimos

- padrão sem variável;
- ambiente válido;
- CLI sobrepondo ambiente;
- ambiente inválido;
- CLI inválida;
- `--help` com ambiente inválido;
- JSON válido analisado por parser, não por substring;
- Unicode em assunto;
- limite inferior, superior e valor imediatamente fora;
- arquivo vazio e última linha sem quebra.

## Evidências e aceite

Entregue README, matriz de erros, fixtures, testes e transcrição reproduzível.
Outra pessoa deve conseguir clonar, pedir ajuda, executar um caso e entender uma
falha sem abrir o código. O laboratório termina quando todos os testes passam em
ambiente limpo e o contrato corresponde ao comportamento real.

## Extensão avançada

Implemente uma segunda interface que chama o mesmo caso de uso: pode ser uma
função de biblioteca ou formulário mínimo. Demonstre que domínio e presenter
não importam parser de argumentos, ambiente global ou UI.

## Checklist de domínio

- [ ] Posso distinguir erro de uso, domínio e operação pelo resultado.
- [ ] A precedência é testada como contrato, não só descrita.
- [ ] JSON e texto partem do mesmo objeto de resultado.
- [ ] Nenhum segredo ou dado pessoal aparece em evidência.
- [ ] A ajuda funciona sem inicializar dependências desnecessárias.
- [ ] A execução é reproduzível por uma segunda pessoa.
