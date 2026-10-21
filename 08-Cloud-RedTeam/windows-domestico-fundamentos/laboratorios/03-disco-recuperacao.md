# Lab 03 — Volume de dados, backup e recuperação

**Classe: C — armazenamento e restauração em discos virtuais descartáveis.**

O objetivo é provar recuperação, não apenas copiar arquivos. Todo particionamento
ocorre no segundo disco virtual. Um terceiro volume ou disco virtual recebe o
backup para que origem e destino não sejam o mesmo objeto.

## Pré-requisitos e critérios de parada

Conclua os Labs 01 e 02 e os capítulos 08–13. Tenha snapshot, segundo disco vazio,
destino separado e scripts do curso revisados. Defina RPO, RTO, tamanho da fixture
e letras esperadas, sabendo que letras não identificam discos.

Pare se `IsBoot` ou `IsSystem` for verdadeiro no alvo, se número/tamanho divergir,
se o destino estiver dentro da origem, se já existir e contiver dados, ou se não
houver rollback comprovado.

## Planejamento

Desenhe `disco → GPT → partição → volume → NTFS → ponto de montagem`. Registre
número, capacidade, estilo e flags. Escreva o resultado esperado de cada etapa e
uma pausa manual antes de inicializar, particionar ou formatar.

O material não fornece um comando pronto de particionamento justamente para
impedir execução cega. Use Disk Management ou cmdlets oficiais depois de conferir
a ajuda e preencher seu runbook com o alvo observado.

## Procedimento

1. Crie snapshot `lab03-antes-armazenamento`.
2. Inventarie todos os discos e destaque boot/sistema.
3. Inicialize somente o disco virtual vazio como GPT.
4. Crie uma partição pequena, formate NTFS e dê rótulo `RTE-DADOS`.
5. Crie fixtures de texto e binário sintético e um manifesto da origem.
6. Revise o script e simule:

```powershell
.\Backup-RteFixture.ps1 -SourcePath 'R:\fixture' `
  -DestinationPath 'S:\RTE-Backup\fixture-001' -WhatIf
```

7. Confirme que o destino não foi criado e execute sem `-WhatIf`.
8. Registre `$LASTEXITCODE` apenas se também usar `robocopy`; não o atribua ao
   script PowerShell.
9. Exclua somente a cópia de trabalho, preservando o backup.
10. Restaure para `R:\restore-test`, nunca sobre a origem.
11. Gere manifesto da restauração e compare caminho relativo, tamanho e SHA-256.
12. Abra amostras, meça o tempo e compare com RTO.

Altere um byte em uma cópia adicional e confirme que a comparação reprova. Isso
demonstra que o teste realmente detecta divergência.

## BitLocker opcional

Se edição e VM suportarem, habilite no volume descartável somente depois de
guardar a recovery key fora do disco e do relatório. Registre presença do
protetor sem seu segredo. Desmonte/remonte e valide acesso normal e procedimento
de recuperação conforme documentação oficial. A atividade opcional não é
necessária para aprovação quando o recurso não existe.

## Evidências

- inventários antes/depois com o alvo destacado;
- diagrama e pausa de confirmação assinada no diário;
- manifests de origem, backup e restore;
- saída `-WhatIf` e prova de que não criou destino;
- RPO/RTO planejados e tempo medido;
- divergência detectada na cópia corrompida;
- estado BitLocker sanitizado, quando aplicável.

## Cleanup e validação

Remova apenas `restore-test` e fixtures pelo caminho resolvido. Desmonte o volume
e restaure `lab03-antes-armazenamento`. Compare `Get-Disk`, `Get-Partition` e
`Get-Volume` com a baseline. A ausência do volume criado é a prova de rollback;
retorne então ao snapshot validado necessário para o próximo gate.

## Aprovação

Passa quando nenhum comando mira o sistema, `-WhatIf` é respeitado, restore
ocorre em caminho novo, manifests equivalem, corrupção é detectada e RPO/RTO são
avaliados. Falha automática: confiar só em letra, sobrescrever destino, publicar
recovery key ou chamar cópia não restaurada de backup validado.

## Questões de defesa

1. Por que três pastas no mesmo volume não seriam independência suficiente?
2. O que hash igual demonstra e o que não demonstra?
3. Como o runbook evita mudança do número/letra do disco?
4. Por que o manifesto não inclui a si próprio?
5. Qual opção de recuperação seria menos destrutiva para um único arquivo?
