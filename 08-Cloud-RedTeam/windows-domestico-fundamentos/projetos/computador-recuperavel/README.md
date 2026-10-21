# Projeto de referência — computador recuperável

Este projeto mostra a arquitetura esperada no capstone sem fornecer uma solução
pronta. Adapte decisões ao usuário fictício, implemente-as na VM e produza suas
próprias evidências. Os scripts reais ficam em [`../../exemplos/`](../../exemplos/README.md).

## Resultado esperado

Uma pessoa deve conseguir:

1. usar documentos locais em conta comum;
2. identificar versão, armazenamento, aplicativos e proteções;
3. recuperar uma versão válida de um documento dentro do RPO/RTO;
4. diagnosticar uma falha de fixture sem reduzir segurança;
5. reconstruir o ambiente usando mídia oficial e runbook.

O projeto é local. Não configura compartilhamentos, firewall, domínio,
administração remota ou serviços empresariais.

## Arquitetura lógica

```text
firmware UEFI + Secure Boot + TPM virtual quando disponível
                         │
               Windows suportado
                         │
          conta comum ───┴─── elevação pontual
                         │
        C: sistema         R: dados sintéticos
                               │
                     fixture + manifesto
                               │
                    S: backup independente
                               │
                      restore-test + validação
```

Letras são rótulos do diagrama, não identidades permanentes. O runbook confirma
disco, volume, tamanho, rótulo e conteúdo antes de operar.

## Estrutura do pacote de entrega

```text
computador-recuperavel/
├── 00-contrato.md
├── 01-arquitetura.md
├── 02-baseline.json
├── 03-aplicativos.csv
├── 04-protecoes.md
├── 05-backup-restore.md
├── 06-incidente.md
├── 07-runbook.md
├── 08-cleanup.md
└── manifests/
```

O contrato descreve pessoa fictícia, documentos, acessibilidade, RPO/RTO,
limites e critérios de aceite. Arquitetura contém boot, discos, contas, dados e
dependências. A baseline usa o schema do script e não contém hostname, usuário,
serial, e-mail, endereço ou segredo.

## Coleta da baseline

Copie os scripts do curso para um caminho conhecido, leia e execute sem elevação
quando possível:

```powershell
.\Get-RteLocalInventory.ps1 -AsJson -OutputPath .\02-baseline.json
Get-Content .\02-baseline.json -Raw | ConvertFrom-Json | Out-Null
Get-FileHash .\02-baseline.json -Algorithm SHA256
```

Acrescente manualmente informações que o schema omite somente quando forem
necessárias e seguras. Ausência intencional é uma propriedade: o inventário não
deve crescer até se transformar em cópia de toda a máquina.

Produza três baselines: estado limpo, estado pronto e estado pós-recuperação.
Compare semanticamente campos estáveis. Hora da coleta e espaço livre podem
mudar; explique tolerâncias em vez de apagar as diferenças.

## Matriz de aplicativos

Para cada um dos dois aplicativos do cenário, registre editor, versão,
arquitetura, origem oficial, status de assinatura, formato, escopo, dados, método
de atualização e rollback. Um aplicativo nativo pode servir como um dos itens.

Não instale software apenas para preencher a matriz. Procedência é mais valiosa
que quantidade. Se houver dependência, relacione-a sem baixar DLL avulsa.

## Proteções e identidade

Documente conta cotidiana comum, conta de elevação, UAC, Secure Boot, TPM,
BitLocker quando suportado, Windows Update e Defender. Cada campo aceita estados
como ativo, inativo, indisponível e não consultável — com evidência. Nunca use
“seguro” como um único valor booleano.

Recovery key fica em local separado e controlado. O relatório registra somente
o teste de disponibilidade. Não crie exclusões, não pause proteção por rotina e
não altere serviço para obter uma saída desejada.

## Fluxo de backup e restore

Primeiro simule:

```powershell
.\Backup-RteFixture.ps1 -SourcePath 'R:\fixture' `
  -DestinationPath 'S:\backup\fixture-001' -WhatIf
```

Depois execute a cópia para destino novo. O script recusa destino existente e
destino dentro da origem. Preserve o manifesto gerado, exclua ou altere apenas a
fixture de trabalho e restaure em `R:\restore-test`. Gere manifesto independente
e compare caminho relativo, tamanho e SHA-256.

Meça o tempo desde a solicitação até a validação funcional; compare com RTO.
Calcule a diferença entre último ponto válido e falha; compare com RPO. “Zero
erros no comando” não substitui abrir documentos e verificar manifests.

## Modelo de runbook

Cada seção contém:

- condição de entrada e sintoma;
- observações e alvo inequívoco;
- critérios de parada;
- ação com privilégio necessário;
- saída esperada e alternativas;
- validação funcional e técnica;
- rollback e responsável.

Inclua rotas para arquivo excluído, ACL incorreta, pouco espaço no volume de
dados, aplicativo que não abre, falha após update e boot indisponível. As últimas
rotas podem terminar em “encaminhar para recuperação especializada” quando o
curso não fornece evidência suficiente.

## Injeção e diagnóstico

O revisor escolhe uma falha permitida e mantém o gabarito separado. O operador
define sintoma, constrói hipóteses, coleta intervalo e aplica o menor teste. O
relatório deve mostrar mudanças de probabilidade e não apenas a resposta final.

Se a causa não for demonstrada, não abra o gabarito prematuramente. Declare o
próximo teste. A finalidade é medir método, não adivinhação.

## Aceite e handoff

Uma terceira pessoa executa restore e consulta de baseline sem ajuda oral. O
projeto passa quando atende a rubrica, RPO/RTO, integridade, privilégio mínimo e
cleanup. O handoff inclui versão/build e data porque menus, propriedades e
ciclos mudam.

Depois, restaure o snapshot limpo e confirme que contas, ACEs, chaves do
Registro, fixtures e volumes temporários não permaneceram. Guarde apenas a
documentação sanitizada e seus hashes.

## Perguntas de revisão

- Qual dependência única pode derrubar todas as cópias?
- Que propriedade do inventário é observação e qual é inferência?
- O runbook identifica volumes sem confiar em letra?
- O restore foi feito em caminho novo e usado pelo aplicativo?
- Uma pessoa com necessidade de acessibilidade consegue concluir a recuperação?
- O sistema final preserva Update, Defender e UAC?
