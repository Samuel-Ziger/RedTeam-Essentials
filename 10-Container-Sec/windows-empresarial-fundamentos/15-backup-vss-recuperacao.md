# 15 — Backup, VSS e recuperação

Volume Shadow Copy Service coordena writer, requester e provider para snapshots
consistentes. Shadow copy não é por si só uma cópia independente nem garante
consistência de todo aplicativo.

```powershell
vssadmin.exe list writers
vssadmin.exe list providers
Get-WindowsFeature Windows-Server-Backup
```

## Camadas de recuperação

- arquivo/pasta;
- volume;
- System State quando aplicável;
- bare metal;
- aplicação/workload;
- servidor reconstruído por código + dados restaurados.

Windows Server Backup/`wbadmin` atende cenários locais, mas escolha corporativa
depende de retenção, imutabilidade, catálogo, testes e suporte do workload.

## Teste

Backup bem-sucedido não prova restore. Restaure em clone isolado, meça RPO/RTO,
valide hashes/consistência e documente dependências. Não conecte o clone como se
fosse produção.

## Exercício

Faça backup do volume de fixtures, exclua um conjunto e restaure em caminho
alternativo. Para bare metal, apenas escreva runbook e use VM descartável.

