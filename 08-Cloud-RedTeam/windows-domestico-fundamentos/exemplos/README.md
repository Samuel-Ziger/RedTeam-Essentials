# Exemplos PowerShell executáveis

Os exemplos são locais, legíveis, sanitizados e conservadores. Leia o código e
execute primeiro com fixtures.

| Arquivo | Função | Mudança de estado |
|---|---|---|
| `Get-RteLocalInventory.ps1` | inventário sem hostname, conta, serial ou endereços | somente leitura; grava JSON opcional |
| `Backup-RteFixture.ps1` | copia fixture para destino novo e gera manifesto | cria destino; suporta `-WhatIf` |
| `Compare-RteManifest.ps1` | compara restore com manifesto SHA-256 | somente leitura |
| `tests/WindowsDomesticFundamentals.Tests.ps1` | suíte Pester offline | usa somente `TestDrive` |

## Inventário

```powershell
.\Get-RteLocalInventory.ps1 -AsJson -OutputPath .\inventario.json
Get-Content .\inventario.json -Raw | ConvertFrom-Json | Out-Null
```

Secure Boot, TPM e Defender retornam `QueryStatus`; isso preserva a diferença
entre disponível, acesso negado, indisponível e cmdlet ausente.

## Backup e comparação

```powershell
.\Backup-RteFixture.ps1 `
  -SourcePath .\fixture `
  -DestinationPath .\backup `
  -WhatIf

.\Backup-RteFixture.ps1 `
  -SourcePath .\fixture `
  -DestinationPath .\backup

.\Compare-RteManifest.ps1 `
  -ManifestPath .\backup\manifest.json `
  -RestoredPath .\backup
```

O backup recusa destino existente, destino dentro da origem e reparse point na
origem. O comparador rejeita caminhos absolutos, `..` e duplicatas no manifesto;
depois relata arquivos ausentes, inesperados ou alterados.

Para um teste real de restore, copie os arquivos esperados para um terceiro
diretório e compare esse diretório ao manifesto. O arquivo `manifest.json` pode
ficar no backup; ele não descreve a si próprio.

## Testes

```powershell
Invoke-Pester .\tests -CI
```

A suíte usa o diretório temporário do Pester. Ela não consulta configuração real,
não cria conta, não executa scan e não altera volume.

## Limites

Os scripts não fazem instalação, particionamento, ACL, Registro ou reparo. Essas
ações exigem decisão contextual e não devem ser escondidas em automação para
iniciante. Expanda o código apenas depois de escrever pré-condições, `-WhatIf`,
validação e rollback.
