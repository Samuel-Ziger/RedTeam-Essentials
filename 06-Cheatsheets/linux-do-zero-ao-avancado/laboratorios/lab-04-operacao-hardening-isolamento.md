# Laboratório 04 — operação, hardening e isolamento

## Missão

Transformar a unit didática em um serviço local operável: automatizado,
observável, restaurável e endurecido por incrementos. O laboratório não ensina
arquitetura de redes; todo acesso ocorre por loopback ou console da VM.

## Pré-requisitos

Laboratório 03, capítulos 17 a 23 e
[guia de diagnóstico](../GUIA-DIAGNOSTICO.md). Duração esperada: seis a dez
horas.

## Parte 1 — contrato operacional

Defina dono, objetivo, entrada, saída, estado persistente, código de sucesso,
falhas esperadas, frequência, RPO, RTO e teste funcional. Um processo em
execução não é suficiente: a saída precisa obedecer ao schema e ter horário,
kernel e UID válidos.

## Parte 2 — conectividade estritamente local

Se usar uma aplicação HTTP para healthcheck, faça bind somente em loopback.
Caso contrário, use socket Unix ou verificação do arquivo de estado. Registre
processo, descritor, socket e unit responsáveis.

SSH é opcional e apenas contra localhost ou uma segunda VM privada. Valide a
host key por console, use chave exclusiva do laboratório e remova-a no teardown.
Não configure túneis, rotas ou firewall aqui; eles pertencem aos módulos 14 a
18.

## Parte 3 — automação

Escreva um invólucro Bash que:

- valide zero ou um conjunto explícito de argumentos;
- confirme dependências;
- use temporário criado com segurança;
- preserve dados como argumentos;
- não sobrescreva saída válida antes da validação;
- trate TERM e INT;
- produza log em stderr e resultado em stdout;
- converja na segunda execução.

Teste com shellcheck quando disponível. Bash trace só pode usar dados sintéticos
porque pode revelar valores.

## Parte 4 — observabilidade

Construa uma linha do tempo com status da unit, journal e arquivo produzido.
Defina quatro alertas locais: falha da unit, saída antiga, espaço insuficiente e
backup ausente. Não é necessário instalar plataforma de monitoramento; cada
alerta deve ter expressão, limiar, janela, impacto e primeira ação.

Use [comparar_diagnosticos.py](../exemplos/comparar_diagnosticos.py) para
comparar dois snapshots do host. Classifique diferenças como esperada,
investigar ou ignorada por volatilidade.

## Parte 5 — backup e restore

Execute [backup_versionado.sh](../exemplos/backup_versionado.sh) sobre
configuração e estado sintéticos. Verifique o checksum e restaure em destino
vazio. O serviço deve passar no mesmo teste funcional usando a cópia restaurada.
Registre RPO e RTO observados.

## Parte 6 — hardening incremental

Capture baseline e aplique somente uma mudança por vez:

1. identidade dedicada ou dinâmica;
2. umask restritiva;
3. filesystem do sistema protegido;
4. home e dispositivos privados;
5. proibição de novos privilégios;
6. limites de tarefas e memória compatíveis;
7. política MAC da distribuição, se houver perfil apropriado.

Depois de cada mudança, valide configuração, comportamento, logs e rollback.
Pontuação de ferramenta é pista, não prova.

## Parte 7 — isolamento explicado

Execute a mesma carga em escopo de usuário ou container rootless. Compare PID,
UID, namespaces, cgroup, mounts, capabilities e seccomp. A conclusão precisa
dizer o que foi isolado e o que continua compartilhado com o host.

## Incidentes

O avaliador escolhe três:

- variável de ambiente ausente;
- diretório sem escrita;
- processo encerra com status não zero;
- saída antiga apesar de unit ativa;
- limite de tarefas incompatível;
- archive de backup corrompido;
- negação MAC em dado sintético.

## Aprovação

Entregue runbook de saúde, mudança, rollback e restore. O serviço passa no teste
após reboot, a restauração funciona em destino vazio, cada controle tem
justificativa e nenhum diagnóstico depende de desativar segurança.
