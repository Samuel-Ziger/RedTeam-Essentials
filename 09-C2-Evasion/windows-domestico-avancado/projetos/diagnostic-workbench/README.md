# Projeto de referência — Diagnostic Workbench

Este documento define uma arquitetura de referência para o capstone. Ele não entrega a solução completa: você implementa o aplicativo, o módulo PowerShell e os testes usando as fixtures do curso. O resultado é uma bancada local capaz de reproduzir, observar e corrigir uma falha benigna.

## Resultado esperado

O sistema recebe um diretório de arquivos sintéticos, calcula SHA-256 e tamanho de cada item, usa a DLL `rte_math` para agregar uma soma de verificação simples e grava um relatório JSON versionado. Uma opção exclusiva de build de laboratório dispara uma exceção controlada em entrada marcada, permitindo mini dump do próprio processo.

O projeto deve:

- funcionar como conta comum e sem rede;
- carregar DLL somente pelo diretório do executável;
- rejeitar ABI incompatível antes da chamada;
- limitar quantidade e tamanho total da entrada;
- produzir logs estruturados em UTC com correlation ID;
- preservar mitigações padrão da toolchain;
- oferecer testes e cleanup idempotente.

## Arquitetura

```text
fixture sintética
      │
      ▼
rte_workbench.exe ── valida limites e enumera arquivos
      │
      ├── rte_math.dll ── ABI v1, soma simples
      │
      ├── report.json ── schema rte.workbench/report-v1
      │
      └── events.jsonl ── UTC, correlationId, etapa, resultado
                              │
                   módulo PowerShell de orquestração
                              │
                   Pester + benchmark + cleanup
```

Nenhum componente abre processo externo, instala serviço, altera proteção ou acessa credenciais. O aplicativo não aceita URL nem caminho de rede. Reparse points são rejeitados para impedir que a fixture saia da raiz prevista.

## Contrato de entrada

Receba `--input`, `--output` e `--correlation-id`. Resolva caminhos absolutos e confirme que saída não está dentro da entrada. Defina limites, por exemplo 1.000 arquivos, 64 MiB por arquivo e 256 MiB totais. Recuse symlink/reparse point, arquivo que muda durante leitura e nome duplicado após normalização escolhida.

O modo de falha deve exigir duas condições: build compilado com `RTE_LAB_CRASH` e argumento explícito `--lab-crash`. A versão normal não contém esse caminho. A documentação deixa claro que ele só usa dados artificiais e existe para depuração.

## Contrato da DLL

Reaproveite a ABI do exemplo:

```c
unsigned int rte_api_version(void);
int rte_add(int left, int right);
```

O consumidor calcula seu diretório, combina o nome fixo, carrega com flags seguras, resolve exports e verifica `rte_api_version() == 1`. Toda falha retorna código distinto e mensagem operacional sem revelar dados. `DllMain` não realiza I/O, alocação complexa ou sincronização.

O agregado não é mecanismo criptográfico e não substitui SHA-256. Ele existe para demonstrar fronteira ABI. O relatório deve nomeá-lo `DidacticAggregate`, evitando interpretação de integridade forte.

## Schema de saída

Um relatório mínimo:

```json
{
  "schemaVersion": "rte.workbench/report-v1",
  "collectedAtUtc": "2026-01-01T00:00:00.0000000Z",
  "correlationId": "lab-0001",
  "inputManifestSha256": "...",
  "fileCount": 3,
  "totalBytes": 1200,
  "didacticAggregate": 42,
  "files": [
    {"relativePath": "a.txt", "bytes": 400, "sha256": "..."}
  ]
}
```

Ordene `files` por caminho relativo ordinal antes de serializar. Não inclua usuário, hostname, caminho absoluto, serial de volume ou argumento completo. JSON deve reabrir e validar contra o contrato.

## Módulo PowerShell

Implemente funções públicas:

- `New-RteWorkbenchFixture`: cria dados determinísticos sob uma raiz permitida;
- `Invoke-RteWorkbench`: executa com timeout, captura streams e valida código;
- `Test-RteWorkbenchReport`: verifica schema, limites, caminhos e hashes;
- `Remove-RteWorkbenchFixture`: usa `SupportsShouldProcess`, rejeita reparse point e remove apenas raiz marcada.

Helpers de data, hash e validação ficam privados. O manifesto exporta somente essas quatro funções. Nenhuma função muda política, execução ou Defender. Use `-LiteralPath`, modo estrito, erros terminantes e objetos como saída.

## Plano de testes

Pester deve cobrir:

1. fixture determinística e idempotente;
2. relatório saudável com schema e ordem;
3. entrada ausente, grande demais e com reparse point;
4. DLL ausente e ABI incompatível;
5. timeout e código de saída diferente;
6. caminho relativo com espaço e caracteres Unicode;
7. cleanup em `-WhatIf` e rejeição de raiz sem marcador;
8. regressão da exceção escolhida.

Use mocks somente para isolamento de chamadas externas; mantenha teste de integração com executável real. Um teste não deve acessar Registro, internet ou processo fora da fixture.

## Observabilidade

Cada etapa emite JSON Lines com `timestampUtc`, `correlationId`, `event`, `durationMs` e `result`. Não grave conteúdo dos arquivos. O correlation ID liga log, relatório e execução do PowerShell.

Para falha de DLL, use ProcMon filtrado pelo executável. Para desempenho, capture no máximo uma execução com WPR. Para exceção controlada, produza mini dump. Não use todas as ferramentas em toda falha; selecione a evidência que discrimina a hipótese.

## Orçamento

Defina orçamento antes de medir. Exemplo: 500 arquivos de 4 KiB, p95 abaixo de 1 segundo e private bytes abaixo do limite observado mais margem justificada. Faça duas rodadas de aquecimento e vinte medições. Preserve resultado funcional em todas.

Uma otimização só entra quando reduz métrica relevante sem enfraquecer validação, determinismo ou segurança. Registre também custo em memória e complexidade.

## Falha, análise e correção

O revisor escolhe uma falha e guarda o gabarito. O estudante escreve hipóteses antes da coleta. Para exceção, confirme PDBs com `.reload /f`, registre exception code e encontre o primeiro frame próprio. `!analyze -v` não basta.

Faça uma correção focal, acrescente teste que reproduza o defeito e repita linha de base, benchmark e inventário defensivo. Se a causa não puder ser confirmada, entregue limitações e próximo teste em vez de alterar várias partes.

## Estrutura da entrega

```text
diagnostic-workbench-entrega/
├── 00-contrato.md
├── 01-build.json
├── 02-arquitetura.md
├── 03-baseline.json
├── 04-hipoteses.md
├── 05-evidencia-sanitizada.md
├── 06-correcao-regressao.md
├── 07-performance.csv
├── 08-defesa-local.md
├── 09-runbook.md
└── 10-cleanup.md
```

Binários, PDBs, ETL, PML e DMP não entram no pacote público. O manifesto de build informa como reconstruí-los. Em ambiente fechado, artefatos sensíveis ficam em armazenamento separado, com acesso e expiração.

## Aceite e handoff

Uma terceira pessoa parte de checkout limpo e consegue compilar, criar fixture, executar cenário saudável, ativar a falha designada, confirmar a correção e limpar tudo. Cada afirmação causal aponta para uma evidência. O relatório diferencia fato, inferência e lacuna.

O projeto falha se exigir elevação rotineira, rede, exclusão do Defender, caminho global de DLL, dump de outro processo, segredo no log ou instrução oral indispensável.

## Perguntas de revisão

- Qual informação liga relatório e logs sem identificar a máquina?
- Como o programa prova que não atravessou um reparse point?
- O PDB corresponde exatamente ao binário do dump?
- A correção resolve o mecanismo ou apenas esconde a mensagem?
- O benchmark preserva entrada, aquecimento e função?
- O cleanup se recusa a apagar uma raiz sem marcador?
- Que artefato contém dado sensível e quando será removido?

