# Laboratório 02 — Dados locais, estado e fronteira de GUI

## Objetivo

Evoluir um produto sem transformar arquivo, widgets ou armazenamento no modelo
de domínio. Você criará documento versionado, importação atômica, máquina de
estados e uma fronteira de apresentação que possa alimentar GUI desktop ou web.

Use o Study Desk como referência executável. Não copie suas funções sem explicar
invariantes e diferenças do seu domínio.

## Cenário

Adicione ao `focus-report` do Lab 01 um histórico local de execuções. Cada
registro contém ID, instante UTC, perfil, total de minutos e quantidade de
assuntos. O produto pode listar, filtrar, importar e exportar snapshots. A CLI
continua funcionando, enquanto uma camada de apresentação oferece comandos
reutilizáveis por uma GUI futura.

## Etapa A — Documento versionado

Defina primeiro um exemplo canônico:

```json
{
  "schemaVersion": 1,
  "exportedAt": "2026-10-05T12:00:00.000Z",
  "runs": []
}
```

Especifique campos permitidos, tipos, faixas, formato temporal, limite de
registros, limite total e política para campos desconhecidos. Implemente a mesma
validação na leitura e antes da escrita: o sistema não deve exportar estado que
recusaria importar.

Crie fixtures para versão atual, versão futura, JSON inválido, ID duplicado,
data impossível, campo extra, limite excedido e item parcialmente válido.

## Etapa B — Importação transacional

Separe estas fases:

```text
bytes → limite → decodificação → parse → schema → domínio
      → resumo → confirmação → persistência → novo estado
```

Durante qualquer falha anterior ao commit, o histórico anterior deve continuar
idêntico. Prove isso com teste que guarda o snapshot original, tenta importar um
documento cujo último item é inválido e compara o estado depois.

Se usar arquivo temporário e rename, documente limites da atomicidade da
plataforma. Se usar Storage do navegador, explique por que uma chave única
reduz, mas não elimina, riscos. Não simule transação apenas limpando antes.

## Etapa C — Estado e eventos

Modele ao menos estes estados da importação:

```text
idle → reading → validating → awaiting_confirmation → committing → success
                   └────────→ error       committing ───────────→ error
qualquer operação ativa ────────────────────────────────────────→ cancelled
```

Liste eventos válidos e rejeite transições impossíveis importantes. O reducer
ou função de transição deve ser puro: recebe estado/evento, devolve novo estado
e não acessa relógio, arquivo, DOM ou widget.

Inclua request ID quando duas leituras podem concorrer. Uma resposta antiga não
pode substituir a seleção mais nova.

## Etapa D — Fronteira para GUI

Crie um presenter/view-model com:

- dados já formatados para lista;
- comandos `importar`, `exportar`, `filtrar`, `cancelar` e `excluir`;
- estado de habilitação e mensagem de status;
- nenhuma referência a widget concreto;
- adapter falso para testar tarefa longa, cancelamento e erro.

Faça um protótipo de GUI apenas se a toolchain estiver disponível. Caso não
esteja, entregue o presenter com teste de contrato e um wireframe de foco. O
objetivo é a fronteira, não escolher um framework.

## Falhas obrigatórias

1. armazenamento recusa escrita;
2. documento excede tamanho antes do parse;
3. versão futura;
4. dois IDs iguais;
5. cancelamento durante leitura;
6. fechamento com alteração ainda não salva.

Para cada falha, registre estado anterior, estado depois, mensagem ao usuário e
ação de recuperação. Uma mensagem “erro desconhecido” não satisfaz o aceite.

## Evidências e aceite

- schema e invariantes versionados;
- tabela de transições;
- fixtures válidas e inválidas;
- testes de round-trip e rollback;
- contrato do adapter de persistência;
- mapa de foco e política de fechamento;
- ADR explicando JSON, SQLite ou outra persistência.

A aprovação exige que domínio rode sem GUI, armazenamento real ou relógio real;
importação inválida preserve o estado; e a camada de apresentação represente
carregamento, confirmação, erro e cancelamento sem combinações contraditórias.

## Extensão avançada

Implemente migração pura `v1 → v2`, conservando fixture original. A migração
deve validar entrada, produzir novo documento, validar saída e nunca sobrescrever
o único backup. Registre como uma versão antiga se comporta diante de `v2`.

## Checklist de domínio

- [ ] O schema possui limites semânticos e não só nomes de campos.
- [ ] Importação faz commit somente após validação integral.
- [ ] Estado e eventos podem ser testados sem efeito externo.
- [ ] Falha de persistência não confirma sucesso na interface.
- [ ] O mapa de foco cobre teclado, cancelamento e fechamento.
- [ ] A decisão de armazenamento possui trade-offs e recuperação.
