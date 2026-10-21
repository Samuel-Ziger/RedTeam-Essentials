# Laboratório 01 — shell, arquivos e permissões

## Missão

Construir uma área de trabalho descartável, processar dados com nomes hostis e
entregar uma árvore compartilhada cuja política de acesso pode ser explicada.
Tudo ocorre como usuário comum e deve poder ser repetido sem deixar estado.

## Pré-requisitos

Capítulos 00 a 08 e [exemplos executáveis](../exemplos/README.md). Reserve de
duas a quatro horas. Não use sudo para resolver uma etapa.

## Contrato

Crie um diretório com mktemp. Salve seu caminho em variável específica, valide
que ele está sob o diretório temporário do sistema e instale um trap de limpeza.
O laboratório deve aceitar nomes com espaço, newline e hífen inicial. Não use
eval, divisão de palavras, glob como lista ou loop baseado em substituição de
comando.

## Parte 1 — mapa do ambiente

Registre shell executora, diretório atual, umask, identidade, filesystem do
diretório temporário e descritores padrão. Para cada comando, indique se é
builtin ou programa externo.

## Parte 2 — árvore de entrada

Crie três subdiretórios: entrada, processado e evidencias. Na entrada, produza:

- um arquivo normal com três registros;
- um nome com espaço;
- um nome com newline;
- um nome iniciado por hífen;
- um hard link para o primeiro arquivo;
- um symlink relativo para ele;
- uma FIFO sem escritor permanente.

Liste todos os objetos preservando limites por NUL. Entregue tipo, inode, modo,
UID, GID, tamanho aparente e blocos. Explique por que FIFO e symlink não devem
ser tratados como arquivo regular.

## Parte 3 — pipeline observável

Crie log sintético no formato timestamp, nível, serviço e mensagem. Processe
com [analisar_logs.awk](../exemplos/analisar_logs.awk). O relatório fica em
stdout; avisos e contagem de inválidos ficam em stderr. Execute uma vez com
entrada válida e outra com linha incompleta. Registre o status de saída do
pipeline inteiro.

## Parte 4 — política de acesso

Dentro da própria árvore, crie um diretório equipe. Calcule antes de executar:

- modo final de diretório com umask 027;
- modo de novo arquivo;
- efeito de setgid no grupo de novas entradas;
- diferença entre leitura, listagem e travessia.

Se ACL estiver disponível, aplique uma ACL nomeada ao próprio usuário e mostre
a mask efetiva. Caso não esteja, documente o comando que detectou a ausência e
continue; instalar pacote não faz parte deste lab.

## Parte 5 — código real

Execute [arquivos_seguro.sh](../exemplos/arquivos_seguro.sh) usando como pai o
diretório do laboratório. Antes, leia o script e preveja as quatro linhas de
saída. Depois, associe cada resultado a inode, link ou conteúdo observado.

## Falhas obrigatórias

1. Faça um comando interpretar um nome iniciado por hífen como opção em uma
   cópia isolada; corrija com fim de opções.
2. Execute pipeline em arquivo ausente; prove que pipefail torna a falha visível.
3. Remova travessia de um diretório, reproduza a negação e restaure pelo modo
   previamente registrado.

Não use permissão universal como diagnóstico.

## Entrega

~~~text
lab-01/
├── README.md
├── inventario.tsv
├── stdout.txt
├── stderr.txt
├── permissoes.md
└── teardown.md
~~~

README descreve previsão, execução, divergência e explicação. Teardown mostra
que o diretório foi removido e que o diretório atual saiu dele antes da remoção.

## Critérios de aprovação

- nomes são preservados sem quebra de argumentos;
- hard link, symlink, FIFO e arquivo regular são distinguidos;
- stdout, stderr e status de pipeline são verificáveis;
- acesso é explicado por modo, umask, ACL e diretório ancestral;
- a segunda execução produz o mesmo resultado;
- nenhum arquivo permanece fora da árvore temporária.
