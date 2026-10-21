# 34 — Projeto final: appliance Linux offline

## Objetivos

- integrar kernel, boot, storage, serviço, sandbox e observabilidade;
- transformar requisitos em invariantes e testes automatizados;
- construir e atualizar sem dependência de rede;
- provar recuperação, reprodutibilidade e limites do resultado.

## Missão

Construa um appliance Linux local, sem qualquer interface de rede, que executa
uma carga de processamento de arquivos, inicia por imagem verificável, aplica
limites e sandbox, produz telemetria local e suporta update A/B com rollback.

O objetivo não é criar uma distribuição universal. É integrar hipóteses e
evidências de todos os subsistemas estudados.

## Arquitetura de referência

```text
firmware → UKI/kernel+initramfs → raiz verificada A ou B
                                      │
                          systemd → worker sem privilégio
                                      │
entrada imutável → validação → arquivo temporário → fsync/rename → saída
                                      │
                  journal local + métricas + health check
```

O worker recebe um arquivo sintético, valida tamanho e formato, produz resultado
determinístico e registra um identificador de conteúdo. Reprocessar a mesma
entrada não duplica saída. Diretórios de entrada, saída e estado têm ownership e
políticas separados; a raiz não é gravável.

## Decisões obrigatórias

Para cada componente, registre uma decisão, alternativa rejeitada e evidência:

- formato da imagem e âncora do root hash;
- política de slot, contador de tentativas e promoção;
- protocolo de escrita durável e idempotência;
- UID, capabilities, LSM ou Landlock e seccomp;
- budgets de CPU, memória, tarefas e storage;
- sinais de saúde e limiar de rollback;
- dados preservados em backup e ensaio de restauração;
- observabilidade normal versus captura temporária de diagnóstico.

Nenhuma métrica pode ser coletada “porque é interessante”. Relacione-a a SLO ou
hipótese. Nenhuma proteção pode ser aceita só porque a unidade inicia; teste uma
operação permitida e uma negada.

## Plano de construção incremental

1. **Workload:** implemente processamento e testes sem imagem.
2. **Serviço:** adicione lifecycle, diretórios, logs e health check.
3. **Contenção:** aplique cgroup e sandbox uma camada por vez.
4. **Imagem:** produza raiz offline e dois builds independentes.
5. **Boot:** configure verificação, console e slot conhecido.
6. **Update:** instale B, falhe health check e demonstre rollback.
7. **Operação:** injete pressão, corrupção e regressão de performance.
8. **Reprodução:** terceira pessoa executa runbook em VM limpa.

Cada fase possui artefato funcional e rollback. Não espere a imagem final para
descobrir que o worker não é idempotente.

## Requisitos funcionais

- boot em QEMU por console serial;
- nenhuma NIC no modelo da VM;
- root filesystem imutável ou verificável;
- volume separado para entrada, saída e logs;
- serviço que processa arquivos sintéticos de forma idempotente;
- health check local com código de saída;
- shutdown limpo e recuperação pelo console.

## Requisitos de engenharia

- kernel/config e user space versionados;
- build offline reproduzível em duas execuções;
- manifesto SHA-256 e SBOM;
- systemd com `DynamicUser`, filesystem restrito e credencial de teste;
- cgroup com `MemoryHigh`, `MemoryMax`, CPU weight e TasksMax;
- filtro seccomp derivado do comportamento real;
- coleta de PSI, faults, CPU, I/O e latência da carga;
- tracepoint ou eBPF local por janela curta;
- slots A/B e rollback após health check falhar;
- runbook de backup, restauração e kdump.

## Entregáveis

```text
appliance/
├── README.md
├── threat-model.md
├── architecture.md
├── configs/
├── package/
├── image/
├── tests/
├── measurements/raw/
├── measurements/report.md
├── recovery.md
├── sbom/
└── hashes.txt
```

## Cenários obrigatórios

1. boot normal do slot A;
2. processamento repetido sem duplicar saída;
3. pressão acima de `MemoryHigh` sem corromper dados;
4. tentativa de syscall negada pela sandbox;
5. imagem alterada rejeitada pela verificação;
6. slot B com health check falho e rollback para A;
7. restauração do volume de dados a partir de backup;
8. diagnóstico de uma regressão de desempenho inserida deliberadamente.

## Rubrica (100 pontos)

| Dimensão | Pontos |
|----------|-------:|
| Reprodutibilidade e supply chain | 20 |
| Boot, integridade e rollback | 20 |
| Isolamento e resource control | 15 |
| Correção e testes | 15 |
| Observabilidade e diagnóstico | 15 |
| Recuperação e operação | 10 |
| Clareza da defesa técnica | 5 |

Nota mínima: 75, sem zero em boot/rollback, correção ou recuperação.

## Defesa oral

Em 30 minutos, demonstre uma execução limpa e uma falha. Responda:

- qual é a fronteira de confiança;
- onde uma medida vira decisão;
- qual ajuste foi rejeitado e por quê;
- o que muda entre VM e hardware real;
- qual parte depende da versão do kernel;
- como recuperar sem rede e sem reconstruir manualmente.

## Exercícios

1. Faça threat model limitado ao appliance: ativos, fronteiras, falhas acidentais
   e abuso de input local; não inclua cenários de rede.
2. Escreva testes de aceitação para cada requisito antes de montar a imagem.
3. Execute um game day com slot inválido, storage cheio e worker travado,
   preservando a primeira evidência e recuperando pelo runbook.
4. Peça a outra pessoa para reproduzir build, boot e restauração sem orientação
   oral; transforme toda dúvida em melhoria do documento.

## Checklist de domínio

- [ ] Todos os requisitos possuem teste, evidência e critério de aceitação.
- [ ] Dois builds limpos produzem artefatos equivalentes e explicáveis.
- [ ] O serviço é idempotente, limitado e funcional sob negação esperada.
- [ ] Boot A/B retorna ao slot conhecido após falha controlada.
- [ ] Backup foi restaurado, não apenas criado.
- [ ] Nenhuma etapa depende de interface ou serviço de rede.
- [ ] Outra pessoa conclui build e recovery usando apenas o repositório.

## Conclusão

O projeto está pronto quando outra pessoa recebe somente fontes, dependências
previamente arquivadas e runbook; gera os mesmos hashes, inicia a imagem, executa
os testes e recupera uma falha sem instrução verbal adicional.
