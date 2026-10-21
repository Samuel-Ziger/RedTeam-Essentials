# 13 — Microsoft Defender Antivirus no Windows Server

No Server, Defender pode ser gerenciado por PowerShell e política. Presença,
modo ativo/passivo, plataforma, engine e intelligence precisam ser verificados
na versão/integração usada.

```powershell
Get-MpComputerStatus
Get-MpPreference
Get-WindowsFeature Windows-Defender*
```

## Baseline

- proteção em tempo real/comportamento/script conforme suporte;
- PUA, cloud-delivered protection e sample submission conforme política;
- scans e updates com janela/capacidade;
- ASR/CFA/exploit protection pilotados;
- alertas, eventos e owners;
- exclusões mínimas, justificadas e revisadas.

Exclusões recomendadas variam por workload e muitas são automáticas. Não copie
listas antigas ou exclua volumes inteiros para ganhar desempenho. Use o
Performance Analyzer do Defender para medir antes de propor uma exceção.

## Exercício

Colete estado e modele um rollout auditado. Use somente scan de fixtures; não
desabilite componentes e não introduza malware.

