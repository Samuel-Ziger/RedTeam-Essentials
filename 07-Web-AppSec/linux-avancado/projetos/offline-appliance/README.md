# Projeto de referência — offline appliance

Este documento é a referência de arquitetura para o capítulo 34 e o Lab 09. Ele
não entrega uma imagem pronta: mostra como compor os exemplos reais do curso sem
esconder decisões de kernel, boot, serviço, recursos e recuperação.

## Contrato do produto

O appliance recebe arquivos sintéticos por volume local, valida tamanho e
formato, produz saída determinística e registra resultado. Não possui NIC,
serviço remoto nem login de rede. Console serial é o único canal administrativo.

Invariantes:

- entrada nunca é modificada;
- saída completa aparece uma vez ou não aparece;
- reprocessamento não duplica resultado;
- raiz do sistema é somente leitura e verificável;
- estado mutável ocupa volume separado;
- falha do worker não impede console e rollback;
- nenhum build consulta a internet;
- slot só é promovido depois de health check funcional.

## Mapa dos componentes existentes

| Necessidade | Material reutilizado |
|------------|-----------------------|
| inventário local | [`proc_snapshot.c`](../../exemplos/c/proc_snapshot.c) |
| teste de page faults | [`page_faults.c`](../../exemplos/c/page_faults.c) |
| sandbox de syscall | [`seccomp_demo.c`](../../exemplos/c/seccomp_demo.c) |
| serviço endurecido | [unit e worker](../../exemplos/systemd/) |
| pressão e PSI | [`pressure_report.sh`](../../exemplos/pressure_report.sh) |
| config do kernel | [`kernel_config_diff.sh`](../../exemplos/kernel_config_diff.sh) |
| archive determinístico | [`reproducible_archive.sh`](../../exemplos/reproducible_archive.sh) |
| observação BPF opcional | [`exec_counter.bpf.c`](../../exemplos/bpf/exec_counter.bpf.c) |

Copie código para o projeto somente se precisar modificá-lo; preserve a origem e
adicione teste. O módulo de kernel e o programa BPF nunca são carregados pelo
build automático.

## Layout esperado

```text
offline-appliance/
├── README.md
├── threat-model.md
├── architecture.md
├── Makefile
├── sources.lock
├── kernel/
│   ├── defconfig
│   └── patches/
├── rootfs/
│   ├── overlay/
│   └── package/
├── service/
│   ├── worker/
│   └── offline-worker.service
├── image/
│   ├── slot-a/
│   ├── slot-b/
│   └── boot-policy/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── failure/
│   └── acceptance/
├── measurements/
│   ├── raw/
│   └── report.md
├── recovery.md
├── sbom/
└── hashes.txt
```

`sources.lock` registra arquivo, versão, origem documental, licença e SHA-256
de toda entrada já arquivada. O build falha quando um arquivo falta ou diverge;
ele não tenta fazer download.

## Pipeline de dados

O worker abre um directory fd de entrada confiável e resolve o nome relativamente
a ele. Rejeita symlink, arquivo não regular, tamanho acima do limite e formato
inválido. O identificador é SHA-256 do conteúdo mais versão do schema.

A saída é escrita em temporário exclusivo dentro do diretório final. O worker
trata escrita parcial, sincroniza o arquivo, renomeia e sincroniza o diretório.
Um índice de resultados torna a operação idempotente. Erro deixa temporário
identificável para cleanup, mas nunca publica saída parcial.

## Unidade e sandbox

Parta da unit do curso e justifique cada permissão. Estado recomendado:

- `DynamicUser=yes` e nenhum grupo suplementar;
- bounding set vazio e `NoNewPrivileges=yes`;
- raiz somente leitura, entrada somente leitura e saída explícita;
- diretórios de estado criados pelo systemd;
- families limitadas ao IPC local indispensável;
- seccomp com architecture check e default documentado;
- LSM ou Landlock para restringir objetos;
- `MemoryHigh` com margem antes de `MemoryMax`;
- `TasksMax`, CPU weight e limite de arquivos;
- timeout e stop que encerram todos os processos do cgroup.

Readiness ocorre depois de abrir diretórios e validar schema. Health check
processa fixture conhecida e compara hash, não verifica apenas PID.

## Imagem, boot e slots

Gere rootfs somente leitura e autentique root hash pela cadeia de boot. Uma
imagem nova é gravada no slot inativo. Estado de boot registra slot conhecido,
candidato e tentativas restantes:

```text
instalar B → verificar assinatura/hash → marcar B uma vez → boot B
→ health check aprovado → promover B
→ health check falhou/timeout → decrementar e retornar A
```

O schema do volume de dados permanece compatível com A até a promoção. Migração
irreversível exige fase posterior e backup restaurável. Console e slot A são
testados antes de escrever B.

## Observabilidade com orçamento

Em operação normal, grave apenas resultado, duração, bytes, código de erro e
contadores de recurso. Para diagnóstico, habilite por janela curta:

- PSI e eventos do cgroup;
- faults e RSS/PSS;
- CPU e context switches;
- latência do arquivo e diskstats;
- tracepoint ou eBPF local com filtro e contador de perda.

Dados brutos incluem unidade, clock, duração, kernel e hash do workload.
Instrumentação é removida mesmo após falha.

## Testes obrigatórios

1. mesma entrada duas vezes produz uma única saída correta;
2. short read/write injetado não perde nem duplica bytes;
3. symlink, arquivo grande e formato inválido são rejeitados;
4. escrita fora dos diretórios permitidos falha;
5. syscall não necessária é negada e a unit continua operável;
6. pressão acima de high aparece em events/PSI sem corromper saída;
7. storage cheio preserva entrada e não publica temporário;
8. imagem alterada falha na verificação;
9. slot B defeituoso retorna a A sem ação manual;
10. backup de dados é restaurado numa imagem limpa;
11. dois builds independentes geram hashes iguais ou divergência explicada;
12. boot ocorre com `-nic none` e nenhum device de rede no guest.

## Evidência de conclusão

O dossiê contém diagrama, threat model, decisões, hashes, SBOM, logs de teste,
dados brutos, relatório de performance e runbook. Uma segunda pessoa recebe
somente repositório e dependências arquivadas, reconstrói, inicia, injeta uma
falha e recupera.

O projeto não está concluído se depender da memória do autor, de um cache não
inventariado, de acesso à rede ou de um snapshot que nunca foi restaurado.
