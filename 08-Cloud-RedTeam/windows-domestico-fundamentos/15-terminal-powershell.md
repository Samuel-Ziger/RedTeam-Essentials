# 15 — Windows Terminal, CMD e PowerShell seguro

Windows Terminal é um aplicativo hospedeiro; CMD e PowerShell são shells. CMD
trabalha principalmente com texto e convenções históricas. PowerShell envia
objetos pelo pipeline, o que permite consultar propriedades sem analisar colunas
formatadas. Saber qual camada está em uso evita copiar sintaxe incompatível.

## Objetivos

- distinguir terminal, shell, comando, cmdlet e processo;
- explorar ajuda, tipos, propriedades e pipeline de objetos;
- usar variáveis, condições, laços e funções pequenas;
- tratar erros e validar parâmetros antes de mudar estado;
- exportar JSON/CSV determinístico sem dados desnecessários.

## Descoberta antes de execução

```powershell
Get-Command -Noun Process
Get-Help Get-Process -Full
Get-Help Get-Process -Examples
Get-Process | Get-Member
```

`Get-Command` resolve aliases, funções, cmdlets e executáveis. Antes de usar um
nome curto, confira o `CommandType` e a origem. Aliases facilitam interação, mas
scripts didáticos devem preferir nomes completos e legíveis.

PowerShell pode executar programas nativos. A saída deles normalmente chega como
texto, enquanto cmdlets produzem objetos .NET. Código de saída nativo aparece em
`$LASTEXITCODE`; falhas de cmdlets usam o sistema de erros do PowerShell. Não
trate os dois mecanismos como idênticos.

## Pipeline de objetos

```powershell
Get-Process |
  Where-Object WorkingSet64 -gt 100MB |
  Sort-Object WorkingSet64 -Descending |
  Select-Object Name, Id, @{ Name = 'WorkingSetMiB'; Expression = {
    [math]::Round($_.WorkingSet64 / 1MB, 2)
  }}
```

Filtre cedo, selecione propriedades e formate apenas para apresentação.
`Format-Table` produz objetos de formatação e deve ficar no final; enviar sua
saída para CSV resulta em dados inúteis. Para persistir, use `Export-Csv` ou
`ConvertTo-Json` antes da formatação.

## Variáveis, condições e repetição

```powershell
$freeGiB = [math]::Round((Get-PSDrive -Name C).Free / 1GB, 2)
if ($freeGiB -lt 20) {
    "ATENCAO: $freeGiB GiB livres"
} else {
    "OK: $freeGiB GiB livres"
}

foreach ($service in (Get-Service | Select-Object -First 3)) {
    [pscustomobject]@{
        Name = $service.Name
        Status = [string]$service.Status
    }
}
```

Parênteses tornam a coleção explícita. Converta unidades e tipos na fronteira,
não no texto final. Evite `Write-Host` como saída de dados; objetos podem ser
testados e exportados.

## Função segura

```powershell
function Get-RteVolumeSummary {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidatePattern('^[A-Z]$')]
        [string]$DriveLetter
    )

    $volume = Get-Volume -DriveLetter $DriveLetter -ErrorAction Stop
    [pscustomobject]@{
        Schema = 'rte.volume-summary/v1'
        DriveLetter = $volume.DriveLetter
        FileSystem = $volume.FileSystem
        FreeGiB = [math]::Round($volume.SizeRemaining / 1GB, 2)
    }
}
```

Validação rejeita formato inesperado; `-ErrorAction Stop` permite tratar falha de
forma consistente. Funções que alteram estado devem usar `SupportsShouldProcess`
e respeitar `-WhatIf`, como o exemplo de backup. Isso não substitui validação do
alvo, mas torna intenção e teste visíveis.

## Erros e invariantes

Em scripts do curso, use `Set-StrictMode -Version Latest` e
`$ErrorActionPreference = 'Stop'`. Trate apenas erros sobre os quais pode agir:

```powershell
try {
    Get-Item -LiteralPath 'C:\RTE-Lab\fixture.txt' -ErrorAction Stop
} catch [System.Management.Automation.ItemNotFoundException] {
    Write-Error 'A fixture esperada não existe; nenhuma mudança foi feita.'
}
```

Não use `catch {}` vazio. Ele transforma ausência de evidência em sucesso
aparente. Mensagens devem explicar contexto sem vazar segredo.

## Execução e confiança

Execution Policy ajuda a prevenir execução acidental e expressa política de
scripts, mas não é fronteira de segurança. `Bypass` não torna código confiável.
Leia o script, valide origem, assinatura e dependências, execute sem elevação e
use VM. Nunca cole uma linha que baixa e executa conteúdo.

Separar código de dados é essencial. Passe caminhos por parâmetros e use
`-LiteralPath`; não monte comandos como strings para depois avaliá-los. Este
curso não usa `Invoke-Expression`.

## Exportação reproduzível

Selecione somente propriedades necessárias, ordene quando a ordem importar,
inclua schema e UTC e defina profundidade JSON. Nome de usuário, hostname, serial,
e-mail e recovery keys ficam fora. Valide o JSON reabrindo-o com
`ConvertFrom-Json`.

## Exercícios

1. Mostre a diferença entre objeto antes e depois de `Format-Table`.
2. Transforme uma consulta em função com validação e erro terminante.
3. Exporte o inventário do curso em JSON e CSV com a mesma semântica.
4. Provoque caminho ausente e trate sem esconder a falha.
5. Explique por que Execution Policy, assinatura e revisão de código são camadas distintas.

## Checklist de domínio

- [ ] Diferencio Terminal, PowerShell, CMD, cmdlet e executável nativo.
- [ ] Consulto ajuda e tipo antes de automatizar.
- [ ] Pipeline preserva objetos até a etapa de exportação/apresentação.
- [ ] Parâmetros e caminhos são validados; entrada não vira comando.
- [ ] Erros não são ocultados e têm contexto útil.
- [ ] Scripts de mudança suportam intenção e `-WhatIf` quando apropriado.
- [ ] Saídas são versionadas, determinísticas e sanitizadas.
