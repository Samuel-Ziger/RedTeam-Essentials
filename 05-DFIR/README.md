# 05 - DFIR

> Modulo de **Digital Forensics & Incident Response**: artefatos Windows, Event Logs, memoria, playbook de ransomware e template de laudo.
> Complementa a visao ofensiva dos modulos 03, 09 e 14 — o que o blue team vera apos o ataque.

## Conteudo

| Documento | Tema |
|-----------|------|
| [forensics_artifacts.md](forensics_artifacts.md) | Artefatos forenses Windows (Registry, Prefetch, Amcache, Jump Lists, etc.). |
| [windows_event_logs.md](windows_event_logs.md) | Event Logs criticos (Security, Sysmon, PowerShell) e IDs uteis. |
| [memory_analysis_teoria.md](memory_analysis_teoria.md) | Analise de memoria: Volatility, processos, handles, injects. |
| [PLAYBOOK_RANSOMWARE.md](PLAYBOOK_RANSOMWARE.md) | Playbook de resposta a incidente de ransomware. |
| [FORENSIC_REPORT_TEMPLATE.md](FORENSIC_REPORT_TEMPLATE.md) | Template de relatorio forense / IR. |

## Fluxo forense recomendado

```
1. Contencao / isolamento
2. Preservacao (imagem disco + memoria + logs)
3. Triagem (Event Logs + artefatos volatilidade media)
4. Analise profunda (memoria, timeline, IOCs)
5. Contencao avancada / eradicação
6. Relatorio (FORENSIC_REPORT_TEMPLATE)
```

1. **Preservar** - nao "consertar" antes de coletar; hash e chain of custody.
2. **Triagem rapida** - [windows_event_logs.md](windows_event_logs.md) + artefatos de [forensics_artifacts.md](forensics_artifacts.md).
3. **Memoria** - dump e analise com Volatility. Ver [memory_analysis_teoria.md](memory_analysis_teoria.md).
4. **Cenario ransomware** - seguir [PLAYBOOK_RANSOMWARE.md](PLAYBOOK_RANSOMWARE.md).
5. **Documentar** - [FORENSIC_REPORT_TEMPLATE.md](FORENSIC_REPORT_TEMPLATE.md); cruzar com ATT&CK do ataque.

## MITRE ATT&CK (visao defesa / deteccao)

Tecnicas frequentemente evidenciadas nos artefatos deste modulo:

- T1059.001 - PowerShell
- T1003 - OS Credential Dumping
- T1021 - Remote Services (lateral)
- T1547.001 - Registry Run Keys / Startup Folder
- T1053 - Scheduled Task/Job
- T1486 - Data Encrypted for Impact (ransomware)
- T1070 - Indicator Removal

## Etica e escopo

- Trate evidencias reais com confidencialidade (LGPD / PII).
- Nao altere sistema em producao sem processo de IR acordado.
- Em labs, use VMs descartaveis; preserve snapshots para repetir a analise.
- Red Team: use este modulo para entender deteccao e reduzir ruido desnecessario no engagement.
