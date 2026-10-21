# Lab 09 — Projeto final

**Classe:** B–D. **Duração:** 50–80 h.

## Pré-requisitos e gate

Conclua os Labs 01–08, o guia de diagnóstico, as 72 práticas, o capítulo 34 e o
projeto de referência. A banca aprova design e limites antes de qualquer etapa D.
Console, snapshot restaurado, slot conhecido e backup restaurado numa cópia são
pré-condições, não entregáveis tardios.

Siga os requisitos do [capítulo 34](../34-projeto-final.md). Antes de construir,
entregue uma proposta com:

- diagrama de componentes e boot;
- fronteiras de confiança;
- formato de entrada/saída;
- limites de recursos e modo de falha;
- slots, health check e rollback;
- plano de medição;
- plano de backup e recuperação;
- riscos C/D e checkpoints de snapshot.

## Gates

1. **Design:** ameaças, requisitos e reversão aprovados.
2. **Build:** dois hashes idênticos e dependências arquivadas.
3. **Boot:** console, imagem verificada e slot A funcional.
4. **Serviço:** correção, idempotência, sandbox e limites.
5. **Falhas:** B rejeitado, OOM controlado, imagem alterada rejeitada.
6. **Operação:** backup restaurado e runbook executado por terceira pessoa.
7. **Defesa:** dados brutos sustentam as conclusões.

Cada gate termina com artefato versionado, teste automatizado, hash e decisão de
prosseguir ou reverter. Falha em um gate não é contornada manualmente na imagem;
corrija a fonte, reconstrua e repita.

## Plano de aceitação

| Requisito | Teste mínimo | Evidência |
|-----------|--------------|-----------|
| offline | boot com `-nic none` e inventário guest | comando e devices |
| idempotência | mesma entrada executada duas vezes | uma saída e mesmo hash |
| durabilidade | falha entre write, fsync e rename | antiga ou nova completa |
| sandbox | operação permitida e syscall/path negado | resultado e audit local |
| recursos | carga acima de high e abaixo da margem | PSI e events |
| integridade | alterar cópia da imagem | boot rejeitado |
| A/B | health check de B falha | retorno automático a A |
| recuperação | restaurar volume em imagem limpa | teste funcional |
| performance | regressão conhecida | hipótese, dados e correção |
| build | duas execuções independentes | hashes ou divergência explicada |

## Game day obrigatório

Uma pessoa que não construiu o appliance escolhe dois cenários: storage cheio,
worker travado, imagem alterada ou slot candidato inválido. O operador segue o
runbook, preserva primeira evidência, recupera o requisito e confirma cleanup.
Qualquer orientação oral vira lacuna documental e exige nova execução.

## Avaliação

A nota segue a rubrica do capítulo 34. Zero em correção, boot/rollback ou
recuperação reprova mesmo que a soma exceda 75. Medição sem unidade, janela ou
ambiente não vale. Proteção sem teste negativo não vale. Backup não restaurado
não vale.

## Perguntas para defesa

- Onde termina a cadeia de confiança e como a âncora é atualizada?
- Qual invariante protege publicação da saída?
- Que métrica dispara ação e qual apenas auxilia diagnóstico?
- O que muda em hardware real em relação à VM?
- Como update mantém dados compatíveis com rollback?
- Qual risco foi aceito e por que o controle residual é suficiente?

## Regra final

Nenhuma demonstração pode depender de rede. Pacotes, fontes, ISO, chaves de
laboratório e documentação necessários devem estar preparados antes de isolar o
ambiente.

O pacote entregue inclui fontes, lockfile, config, patches, testes, hashes, SBOM,
dados brutos sanitizados, relatório e recovery. Nenhum core, chave privada,
identificador pessoal ou cache oculto faz parte do artefato.

## Cleanup e encerramento

Desative tracing, remova programs/maps/links do projeto, pare QEMU, descarte
overlays temporários e compare mounts, loops, mappings e units ao inventário
inicial. Preserve base, slots aprovados, backup e dossiê conforme retenção. O
projeto só termina quando uma construção e uma recuperação independentes passam.
