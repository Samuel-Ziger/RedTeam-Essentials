# Lab 04 — Boot, systemd e cgroups

**Classe:** C/D. **Duração:** 16–24 h.

## Pré-requisitos e gate

Conclua o Lab 03 e os capítulos 19–21. Restaure um snapshot de teste e confirme
console serial antes de alterar boot. Registre espaço em `/boot`, entrada
padrão, kernel ativo, cmdline e controladores cgroup. A entrada funcional anterior
permanece intocada.

## Parte 1 — Boot paralelo

1. Valide console serial e snapshot.
2. Extraia initramfs atual e documente módulos essenciais.
3. Construa kernel/initramfs com sufixo próprio.
4. Adicione entrada de boot sem substituir a padrão.
5. Faça boot once e confirme raiz, storage e shutdown.
6. Simule initramfs sem um componente apenas em cópia.
7. Recupere pelo slot anterior.

Associe hash, config, modules e initramfs à release string exclusiva. Antes do
reboot, valide formato e conteúdo e configure uma tentativa, não promoção
permanente. O health check confirma raiz, volume de estado, serviço e shutdown.

## Parte 2 — Serviço

Instale o `rte-observer` na VM e valide unidade. Teste:

- UID dinâmico e `StateDirectory`;
- filesystem somente leitura;
- ausência de capabilities;
- families restritas a `AF_UNIX`;
- `MemoryHigh`, `MemoryMax` e `TasksMax`;
- falha de escrita fora do state directory.

Aplique uma diretiva de hardening por vez. Para cada mudança, teste startup,
processamento, erro, reload ou reinício e stop. Defina readiness como capacidade
de processar fixture; watchdog deve passar pelo worker. Injete falha permanente e
confirme que rate limit impede loop infinito.

Configure `MemoryHigh` com margem abaixo de `MemoryMax`. Aumente carga
gradualmente, colete `memory.events` e PSI e encerre antes de comprometer a VM.
Compare CPUWeight sob competição; não apresente-o como quota.

## Parte 3 — Grafo

Crie timer local para executar a unidade. Desenhe relações Wants/Requires e
Before/After. Quebre deliberadamente uma dependência, capture o job graph e
corrija.

Inclua caminho de shutdown e mostre a ordem invertida. Nenhum processo pode
escapar do cgroup depois de stop. Credencial de teste entra como arquivo com
escopo da unit e é removida no cleanup; não use argumento ou environment.

## Evidência

- entradas de boot antes/depois;
- hash de kernel/initramfs;
- tempo até health check;
- `systemd-analyze security` interpretado criticamente;
- cgroup path e eventos;
- demonstração de rollback.

O relatório também contém estados da máquina de serviço, negação esperada,
events/PSI, dependência versus ordem e tempo máximo de recuperação. Score de
hardening é interpretado, nunca usado como aprovação isolada.

## Perguntas para defesa

- Por que `After` não ativa outra unit?
- Quem verifica cada artefato de boot e como a confiança é revogada?
- Qual diferença operacional entre `MemoryHigh` e `MemoryMax`?
- Como o sistema retorna ao kernel anterior se o PID 1 não inicia?

## Cleanup

Remova apenas entrada e artefatos com sufixo do lab. Nunca use glob em `/boot`.
Recarregue systemd, remova unidade e confirme ausência de processos.
Compare cmdline e entradas com o inventário inicial e preserve somente os
artefatos de evidência explicitamente listados.
