# Lab 05 — Defender, assinatura e integridade

**Classe: A/B — consulta de proteção e quick scan controlado.**

O laboratório constrói uma baseline de segurança local sem malware, EICAR,
exclusões ou desativação. Um executável nativo conhecido serve apenas para
interpretar assinatura e hash; não se cria uma lista universal de hashes.

## Pré-requisitos e critérios de parada

Conclua o Lab 04 e os capítulos 14–16. Registre snapshot, edição/build e produto
de segurança ativo. Se outro produto gerenciar o endpoint, faça somente consultas
compatíveis e documente o estado; não force Defender a assumir controle.

Pare diante de prompt inesperado, propriedade que exigiria reduzir proteção,
alerta real preexistente, arquivo desconhecido ou instrução para restaurar item.
Um incidente real deve sair do laboratório e seguir resposta apropriada.

## Hipótese e baseline

Preveja quais propriedades estarão disponíveis: serviço, antivírus, proteção em
tempo real, monitoramento de comportamento, versão/data da inteligência e idade
dos scans. Declare como diferenciar `$false`, `$null`, cmdlet ausente e acesso
negado.

```powershell
$status = Get-MpComputerStatus
$preference = Get-MpPreference
$status | Select-Object AntivirusEnabled, AMServiceEnabled,
  RealTimeProtectionEnabled, BehaviorMonitorEnabled,
  AntivirusSignatureVersion, AntivirusSignatureLastUpdated,
  QuickScanAge, FullScanAge
$preference | Select-Object PUAProtection, EnableControlledFolderAccess,
  DisableRealtimeMonitoring
```

Converta a saída selecionada para JSON, reabra e sanitize. Não exporte toda a
preferência: princípio de minimização também vale para configuração.

## Artefato conhecido

Escolha um executável nativo obtido pelo caminho do próprio sistema e registre
versão, assinatura e hash:

```powershell
$file = Join-Path $env:SystemRoot 'System32\notepad.exe'
Get-Item -LiteralPath $file | Select-Object FullName, Length, VersionInfo
Get-AuthenticodeSignature -FilePath $file |
  Select-Object Status, StatusMessage, SignerCertificate
Get-FileHash -LiteralPath $file -Algorithm SHA256
```

A localização ou implementação pode variar por build. Se o caminho não existir,
escolha outro componente nativo documentado e registre a adaptação. Não baixe uma
cópia “para comparar”. Explique por que hash muda entre versões legítimas e por
que assinatura válida não promete ausência de vulnerabilidade.

## Quick scan e observação

Marque horário UTC, CPU/memória aproximadas e versão da inteligência. Inicie quick
scan pela interface ou `Start-MpScan -ScanType QuickScan`. Não execute scans
simultâneos nem altere preferências. Observe o sistema e registre término,
resultado, duração e eventuais eventos no intervalo. Verifique novamente o estado.

Se a varredura não puder iniciar, preserve o erro e diagnostique contexto;
ausência de resultado não autoriza desligar outro produto ou criar exclusão.

## Simulação em papel de resposta

Sem criar detecção, receba um cartão de cenário com alerta fictício contendo
hora, categoria e caminho sintético. Escreva a ordem de resposta: parar interação,
preservar contexto, não restaurar, atualizar pelo mecanismo suportado, executar
scan adequado, avaliar contas/dados e recuperar de fonte conhecida. Diferencie
quarentena, bloqueio, remoção e permissão.

## Evidências

- baseline antes/depois com estados interpretados;
- produto responsável e limitações de consulta;
- hash, versão e status de assinatura do artefato nativo;
- duração e resultado da quick scan;
- linha do tempo curta dos eventos relevantes;
- runbook do cartão de alerta;
- confirmação de zero exclusões e zero redução de proteção pelo laboratório.

## Cleanup e aprovação

O scan não exige cleanup; remova apenas exportações temporárias após arquivar a
evidência sanitizada. Compare preferências antes/depois e prove que são iguais.
Restaure snapshot se qualquer estado não planejado mudou.

Passa quando os componentes são diferenciados, resultados são proporcionais e
nenhuma proteção é reduzida. Reprova se usar malware/teste de detecção, adicionar
exclusão, desativar produto, restaurar alerta, interpretar erro como desativação
ou publicar detalhes sensíveis.

## Questões de defesa

1. Qual diferença entre inteligência, engine, tempo real e scan?
2. Por que quick scan recente não prova segurança completa?
3. O que a assinatura do binário demonstra?
4. Como produto de terceiros altera a interpretação?
5. Por que formatar imediatamente pode ser resposta inadequada a um alerta?
