# Laboratório 03 — armazenamento, boot e systemd

## Missão

Construir uma pilha de armazenamento sobre arquivo-imagem, relacioná-la ao boot
e operar uma unit validada. O aluno deve recuperar as falhas provocadas sem
reinstalar a VM.

## Pré-requisitos e segurança

Laboratório 02 e capítulos 13 a 16. Use clone descartável, snapshot, console do
hypervisor e ao menos 3 GiB livres. Nunca use um disco físico. Duração esperada:
oito a doze horas.

Preencha antes:

~~~text
Nome da VM:
Snapshot:
Console confirmado:
Arquivo-imagem:
Loop esperado:
Inventário inicial salvo em:
Teardown planejado:
~~~

## Parte 1 — inventário

Registre dispositivos, filesystems, UUID, mounts, PV, VG, LV, linha de boot e
unidades com falha. Desenhe a pilha atual da raiz sem alterar nada.

## Parte 2 — pilha descartável

Siga [armazenamento em loop](armazenamento-loop.md). Pare após cada camada e
prove que:

- o loop aponta exatamente ao arquivo criado;
- o mapeamento criptografado usa o loop correto;
- PV pertence ao VG de prefixo exclusivo;
- LV pertence ao VG correto;
- filesystem está montado somente no ponto do laboratório.

Crie um arquivo sintético, registre hash, cresça LV e ext4 na ordem correta e
confirme o conteúdo. Redução não faz parte da prática.

## Parte 3 — montagem e boot

Em uma segunda imagem pequena, crie entrada persistente por UUID com nofail e
timeout curto. Valide a sintaxe e a unit gerada antes de reiniciar. Troque apenas
o UUID do laboratório por um valor inexistente, reinicie e prove que a VM sobe
com falha controlada. Corrija e repita.

Execute também as partes seguras do
[roteiro de boot e recuperação](boot-recovery.md): mapa do boot, target de
resgate temporário e árvore de decisão. Reinstalar bootloader sem evidência não
é uma solução aceita.

## Parte 4 — serviço e timer

Copie os exemplos de systemd para uma árvore de staging. Ajuste ExecStart apenas
na cópia, valide service e timer e explique usuário dinâmico, StateDirectory,
umask, isolamento e calendário.

Se instalar na VM, mantenha o serviço sem conectividade externa e siga o fluxo:

1. validar;
2. instalar caminhos e modos;
3. recarregar unidades;
4. iniciar;
5. inspecionar status, saída e journal;
6. habilitar timer somente depois do teste;
7. remover unit e estado no teardown.

## Falhas obrigatórias

- UUID inexistente somente na montagem não essencial;
- ExecStart inexistente em cópia da unit;
- diretório ou modo incompatível com a identidade da unit;
- calendário inválido em cópia do timer.

Para cada falha, registre primeira mensagem causal, hipótese, correção, teste e
rollback. Não edite unidades fornecidas por pacote.

## Critérios de aprovação

- alvo destrutivo foi validado como loop criado no próprio lab;
- todas as camadas podem ser narradas e desmontadas em ordem inversa;
- boot continua recuperável por console;
- unit e timer passam no verificador;
- serviço executa com privilégio mínimo e produz estado previsível;
- inventário final coincide com o inicial, salvo evidências declaradas.
