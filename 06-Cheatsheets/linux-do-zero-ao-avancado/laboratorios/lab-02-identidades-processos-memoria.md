# Laboratório 02 — identidades, processos e memória

## Missão

Operar uma carga de laboratório sob identidade conhecida, acompanhar seu ciclo
de vida e explicar o consumo de memória sem confundir reserva com residência.

## Pré-requisitos

Laboratório 01, capítulos 09 a 12 e compilador C opcional. Duração esperada:
quatro a seis horas. A parte administrativa ocorre somente em VM com snapshot.

## Parte 1 — conta e autorização

Crie, conforme comandos da sua distribuição, uma conta humana fictícia e uma
conta de serviço sem login interativo. Registre UID, GID, grupos, home, shell e
origem NSS. Não reutilize nomes reais.

Crie um diretório de estado pertencente à conta de serviço e permita à conta
humana apenas leitura por grupo. Prove:

1. a conta de serviço escreve;
2. a conta humana lê e não escreve;
3. uma terceira identidade não lê;
4. root não é usado pela aplicação.

Se sua VM não permite criar contas, modele o mesmo contrato com dois grupos e
diretórios pertencentes ao usuário atual e registre a limitação.

## Parte 2 — processo e IPC

Compile [processos.c](../exemplos/c/processos.c) com todos os avisos tratados
como erro. Antes de executar, desenhe:

~~~text
pai → pipe → filho
pai fecha escrita e espera
filho fecha leitura, escreve e termina com status 7
pai lê, coleta status e termina com sucesso
~~~

Durante uma variante que aguarda alguns segundos, encontre PID, PPID, estado,
descritores, cgroup e limites. Explique por que o status do filho não se torna
automaticamente status do programa pai.

## Parte 3 — sinais

Crie um pequeno processo shell que trate TERM e INT, grave somente dados
sintéticos e remova seu temporário ao sair. Compare:

- término normal;
- TERM;
- INT;
- KILL.

O relatório deve indicar quais handlers puderam executar e por que KILL impede
cleanup. Não use processo que pertença a outra aplicação.

## Parte 4 — memória

Compile [memoria.c](../exemplos/c/memoria.c). Execute apenas com 2 e 16 MiB.
Colete page size, faults, mapas, RSS e PSS quando disponíveis. Relacione:

- reserva do endereço;
- primeira escrita por página;
- aumento de minor faults;
- memória residente;
- liberação ao terminar.

Colete ainda MemAvailable, swap I/O e PSI em intervalos curtos. Não use stress
irrestrito, drop caches nem altere política global.

## Parte 5 — offboarding

Encerre os processos, remova autorização, procure arquivos pelos UIDs usados e
apague as contas fictícias. A remoção de conta não é aprovada enquanto ainda
existir processo, tarefa agendada, chave ou arquivo órfão não justificado.

## Falhas obrigatórias

1. Execute a carga com diretório sem escrita e diagnostique o ancestral exato.
2. Envie TERM a um PID previamente confirmado e prove cleanup.
3. Passe tamanho inválido ao exemplo de memória e explique o código de saída.

## Entrega e aprovação

Entregue diagrama de identidades, árvore de processos, tabela de sinais, tabela
de memória e checklist de offboarding. Aprovação exige menor privilégio
comprovado, nenhum processo alheio sinalizado, ausência de pressão perigosa e
remoção completa das identidades de laboratório.
