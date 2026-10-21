# 00 — Método, laboratório e evidência

## Objetivos

- separar observação, intervenção e conclusão;
- montar um laboratório recuperável e sem rede;
- registrar resultados que outra pessoa consiga reproduzir;
- reconhecer o risco de cada experimento.

## Topologia local

Use duas VMs. A primeira, `analise`, recebe ferramentas e documentos. A
segunda, `sacrificavel`, recebe kernel customizado, boot alternativo, imagens de
bloco e testes de falha. Desative interfaces de rede nas duas configurações do
hypervisor. Transfira previamente fontes e pacotes por ISO somente leitura.

Requisitos sugeridos por VM:

| Recurso | Análise | Sacrificável |
|---------|---------|---------------|
| vCPU | 4 | 4–8 |
| RAM | 8 GiB | 8–16 GiB |
| Disco | 60 GiB | 100 GiB dinâmico |
| Console | serial e gráfico | serial obrigatório |
| Snapshots | antes de cada etapa | antes de cada mudança de baixo nível |

Nested KVM é opcional. Se indisponível, QEMU com TCG ainda permite estudar
boot e dispositivos com menor desempenho.

## Caderno de experimento

Cada registro deve conter:

```text
id: mm-reclaim-01
pergunta: o working set excede a memória efetivamente disponível?
hipotese: PSI full crescerá junto com major faults e latência
ambiente: distro, kernel, arquitetura, config, vCPU, RAM
controle: mesma carga com working set menor
procedimento: comandos exatos e duração
resultado: dados brutos + hash
analise: o que os dados suportam e o que não suportam
reversao: snapshot ou remoção de artefatos
```

Uma captura sem contexto não é evidência reproduzível. Um gráfico sem unidades,
versão e comando de coleta também não.

## Classes de risco

- **A:** leitura de `/proc`, `/sys`, binários e processo próprio.
- **B:** compilação, arquivos temporários e imagens de disco desconectadas.
- **C:** root na VM, mounts, cgroups, tracing privilegiado e nova entrada de boot.
- **D:** falha deliberada, kdump, IOMMU, módulo e kernel customizado.

Experimentos C e D nunca ocorrem no computador principal. Confirme o snapshot
restaurando-o pelo menos uma vez antes de confiar nele.

## Higiene de medição

Controle aquecimento, frequência, processos concorrentes, tamanho de entrada,
cache, ordem das execuções e número de repetições. Mediana e percentis contam
mais que um melhor resultado isolado. Guarde dados brutos; gere gráficos deles.

## Do sintoma à conclusão

Um experimento útil começa com uma variável de resposta. “O sistema ficou
lento” não é mensurável; “o p99 do processamento passou de 40 ms para 180 ms
quando o working set excedeu o limite” é. Em seguida, escolha uma variável
independente, como tamanho da entrada ou política de escalonamento, e mantenha
as demais condições tão constantes quanto possível. O controle negativo mostra
o comportamento sem a condição investigada.

Separe quatro níveis no relatório:

1. **fato:** bytes coletados, versão, contador e código de saída;
2. **interpretação:** significado documentado daquele contador;
3. **inferência:** explicação mais compatível com o conjunto de evidências;
4. **decisão:** mudança proposta e condição para revertê-la.

Correlação temporal ajuda a construir hipótese, mas não estabelece causa. Se PSI
e latência cresceram juntos, repita removendo apenas a pressão de memória. Se a
latência continuar, a hipótese original perdeu força. Resultado nulo também é
resultado e deve permanecer no caderno.

## Artefatos e cadeia de custódia técnica

Crie um diretório por execução, nunca sobrescreva dados anteriores e calcule
hashes depois da coleta. Guarde scripts, stdout, stderr e metadados do ambiente
separadamente. Use UTC e relógio monotônico para duração; horário civil pode
saltar. Não inclua dumps com segredos no repositório.

Uma evidência reprodutível não precisa gerar números idênticos: máquinas virtuais
têm ruído. Ela precisa preservar procedimento, unidades e condições suficientes
para outra pessoa obter a mesma tendência e identificar por que divergiu.

## Falhas comuns

- mudar kernel, carga e limite ao mesmo tempo;
- comparar uma execução fria com outra aquecida;
- descartar erro porque o comando ainda produziu alguma saída;
- restaurar snapshot sem registrar que o estado mudou;
- concluir por média quando o requisito é latência de cauda;
- executar classe C/D sem console e plano de interrupção.

## Prática A

1. Crie as duas VMs sem adaptador de rede.
2. Registre `uname`, `/proc/cmdline`, filesystem raiz e cgroup.
3. Tire e restaure um snapshot de teste.
4. Crie o primeiro caderno e calcule seu SHA-256.

## Exercícios

1. Transforme três sintomas vagos em perguntas falsificáveis, cada uma com
   métrica, unidade, controle e critério de parada.
2. Execute a mesma leitura vinte vezes, calcule mediana, p95 e amplitude e
   explique por que uma amostra isolada não representa a distribuição.
3. Introduza deliberadamente um processo concorrente, identifique-o como
   confundidor e repita o experimento sem ele.
4. Entregue a um colega apenas o caderno e confirme se ele consegue reproduzir
   a coleta sem instrução verbal.

## Checklist de domínio

- [ ] Distingo observação, interpretação, inferência e decisão.
- [ ] Todo experimento possui hipótese refutável, controle e unidade.
- [ ] Sei restaurar snapshot e acessar console sem depender do guest.
- [ ] Preservo dados brutos, comandos, versões, códigos de saída e hashes.
- [ ] Consigo explicar por que snapshot não substitui backup.
- [ ] Defino interrupção e reversão antes de uma prática C ou D.
