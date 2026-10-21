# 20 — systemd avançado e ciclo de vida

## Objetivos

- modelar dependência separada de ordem;
- usar ativação, readiness, watchdog e shutdown previsíveis;
- entregar credenciais sem variável de ambiente;
- compor hardening e resource control testáveis.

## Dependência não é ordem

`Requires=` e `Wants=` expressam relação de ativação. `After=` e `Before=`
expressam apenas ordem. Um serviço pode precisar de ambos. `BindsTo=` e
`PartOf=` propagam mudanças mais fortes e devem ser usados conscientemente.

```bash
systemctl list-dependencies --all UNIT
systemd-analyze critical-chain UNIT
systemd-analyze dot UNIT > graph.dot
```

## Tipos e readiness

`Type=simple` considera iniciado quando o processo nasce. `Type=notify` permite
que o serviço sinalize readiness real. `Type=oneshot` modela tarefa finita;
`RemainAfterExit` representa estado alcançado, não um daemon invisível.

Watchdog exige heartbeat do processo. Reiniciar sempre pode criar loop; use
limites de start e diferencie exit limpo, falha transitória e erro permanente.

## Ativação

Socket, path, timer, device e D-Bus activation iniciam trabalho sob demanda. Este
módulo não configura sockets de rede; socket activation aparece apenas com
`AF_UNIX` local.

## Credenciais

`LoadCredential=` e mecanismos relacionados entregam segredo como arquivo com
escopo do serviço. Isso evita argumento de processo e variável de ambiente, mas
não resolve origem, rotação e permissão da credencial por si só.

## Hardening

Opções como `DynamicUser`, `NoNewPrivileges`, `ProtectSystem`, `PrivateTmp`,
`ProtectHome`, `RestrictAddressFamilies`, `CapabilityBoundingSet` e filtros de
syscall reduzem superfície. Aplique uma por vez e teste caminhos de leitura,
escrita, logs, reload, stop e upgrade.

O exemplo [`rte-observer.service`](exemplos/systemd/rte-observer.service) usa
somente coleta local e diretório de estado gerenciado pelo systemd.

## Recursos e lifecycle

`CPUWeight`, `MemoryHigh`, `MemoryMax`, `TasksMax` e `IOWeight` mapeiam para
cgroup v2. Limite duro sem margem pode transformar lentidão em falha. Defina
comportamento no OOM e health check antes de ativar.

## Estado, readiness e falha

Modele o serviço como máquina de estados: inactive, activating, ready, stopping e
failed. `Type=notify` só melhora o contrato se a aplicação enviar `READY=1`
depois de adquirir recursos essenciais. Watchdog deve ser emitido pelo caminho
que comprova progresso; uma thread isolada enviando heartbeat enquanto o worker
travou produz falso saudável.

`ExecStartPre` não compartilha processo nem namespace privado de forma arbitrária
com o daemon. Use-o para validações finitas, não para iniciar background. Para
reload, defina se a troca é atômica, como erros preservam configuração anterior
e quando `RELOADING=1` ou ready voltam a representar estado consistente.

## Grafo e parada

Dependência e ordem são eixos separados. Ciclos de ordem impedem transação;
dependência forte demais amplia domínio de falha. Durante shutdown, ordem é
invertida. `TimeoutStopSec` e `KillMode` precisam refletir processo principal,
workers e descendentes; deixar processo fora do cgroup quebra cleanup.

Hardening é cumulativo e precisa de teste funcional. Comece pelo inventário de
leituras, escritas, syscalls, families locais e capabilities. Aplique uma opção,
rode caminhos normal, erro, reload e stop, depois registre a negação. O score de
`systemd-analyze security` é heurística, não threat model.

## Falhas comuns

- usar `After` esperando ativar a outra unidade;
- sinalizar ready antes de abrir recursos essenciais;
- executar daemon em `ExecStartPre`;
- reiniciar erro permanente até atingir rate limit;
- endurecer sem testar upgrade, falha e shutdown;
- colocar segredo em argumento ou variável de ambiente.

## Prática B/C

1. Valide a unidade com `systemd-analyze verify`.
2. Execute-a como unidade transitória ou copie para a VM.
3. Confirme UID dinâmico, diretório e cgroup.
4. Force uma falha prevista e observe restart limit.
5. Revise `systemd-analyze security` sem tratar o score como prova absoluta.

## Exercícios

1. Construa unidades A e B com dependência e ordem corretas; remova cada relação
   separadamente e observe o grafo.
2. Defina readiness e watchdog capazes de detectar worker travado.
3. Aplique cinco opções de hardening ao serviço do curso, uma por vez, e registre
   a primeira negação funcional.
4. Force três tipos de saída e configure restart apenas para falha transitória.

## Checklist de domínio

- [ ] Distingo ativação, ordem, propagação de estado e agrupamento.
- [ ] Defino readiness e watchdog como sinais reais de progresso.
- [ ] Projeto reload, stop, timeout e cleanup do cgroup inteiro.
- [ ] Entrego credenciais por arquivo com escopo e rotação definidos.
- [ ] Explico por que `After=B` sozinho não inicia B.

Fonte: [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html).
