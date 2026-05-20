<#
.SYNOPSIS
    Organiza artefatos (logs, scans, screenshots, exploits) de engajamentos
    de pentest e CTFs em uma estrutura padronizada.

.DESCRIPTION
    Le um diretorio de origem, classifica os arquivos por tipo (heuristica
    de extensao + conteudo conhecido de scans Nmap/Nessus) e move/copia
    para uma estrutura organizada por engajamento.

    Estrutura criada:
        <Base>/<TargetName>/
            Screenshots/   (png, jpg, jpeg, gif, bmp, webp)
            Scans/         (nmap, gnmap, xml, html de scans)
            Exploits/      (py, sh, ps1, c, cpp, exe, dll, jar)
            Notes/         (md, txt, doc, docx, pdf)
            Loot/          (credentials, hashes, dumps, .kdbx, .ovpn)
            Misc/          (qualquer outro)

    Suporta -DryRun (nada e movido), -CopyMode (preserva original) e
    geracao de um indice INDEX.md com metadados.

.PARAMETER SourcePath
    Diretorio contendo os arquivos a organizar.

.PARAMETER TargetName
    Nome do engajamento/lab/maquina (ex: HTB_Forest, ACME_PenTest_2026).

.PARAMETER BasePath
    Diretorio base. Default: ~/Pentest/Labs.

.PARAMETER CopyMode
    Copia em vez de mover.

.PARAMETER DryRun
    Mostra o plano sem mover nada.

.EXAMPLE
    ./organize_logs.ps1 -SourcePath ~/Downloads -TargetName HTB_Forest

.EXAMPLE
    ./organize_logs.ps1 -SourcePath ./raw -TargetName ACME_2026 -CopyMode -DryRun

.NOTES
    Autor:   Samuel Ziger - RedTeam Essentials
    Versao:  2.0.0
    Licenca: MIT
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidateScript({ Test-Path $_ })]
    [string]$SourcePath,

    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Za-z0-9._\- ]+$')]
    [string]$TargetName,

    [string]$BasePath = (Join-Path $HOME 'Pentest/Labs'),

    [switch]$CopyMode,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Import-Module (Join-Path $PSScriptRoot "../lib/powershell/RTECommon.psm1") -Force
Write-RTEBanner -Title "Log Organizer" -Version "2.0.0"

# --- Tabela de classificacao -------------------------------------------------
$classification = [ordered]@{
    'Screenshots' = '\.(png|jpe?g|gif|bmp|webp|tiff?)$'
    'Scans'       = '\.(nmap|gnmap|xml|nessus|html)$|nmap|nessus|masscan'
    'Exploits'    = '\.(py|sh|ps1|psm1|c|cpp|h|rb|go|java|jar|exe|dll|bin)$'
    'Notes'       = '\.(md|txt|rtf|doc|docx|odt|pdf)$'
    'Loot'        = '\.(kdbx|ovpn|pem|key|hash|hashes|pwd|creds)$|passwords?|hashes?'
}

$projectDir = Join-Path $BasePath $TargetName
$subDirs    = @('Screenshots','Scans','Exploits','Notes','Loot','Misc')

Write-RTELog -Level INFO -Message "Origem : $SourcePath"
Write-RTELog -Level INFO -Message "Destino: $projectDir"
Write-RTELog -Level INFO -Message "Modo   : $(if($CopyMode){'COPIA'}else{'MOVER'})$(if($DryRun){' (DRY-RUN)'})"

# --- Cria estrutura ----------------------------------------------------------
if (-not $DryRun) {
    foreach ($d in $subDirs) {
        $p = Join-Path $projectDir $d
        if (-not (Test-Path $p)) { New-Item -ItemType Directory -Path $p -Force | Out-Null }
    }
    Write-RTELog -Level SUCCESS -Message "Estrutura criada em $projectDir"
}

# --- Classifica e move/copia ------------------------------------------------
$index = [System.Collections.ArrayList]@()
$files = Get-ChildItem -Path $SourcePath -File -Recurse:$false
Write-RTELog -Level INFO -Message ("Arquivos encontrados: {0}" -f $files.Count)

foreach ($f in $files) {
    $category = 'Misc'
    foreach ($k in $classification.Keys) {
        if ($f.Name -match $classification[$k]) { $category = $k; break }
    }
    $dest = Join-Path $projectDir $category
    $action = if ($CopyMode) { 'Copy' } else { 'Move' }
    $line   = "{0,-11} -> {1}/{2}" -f $action, $category, $f.Name
    Write-RTELog -Level DEBUG -Message $line

    if (-not $DryRun) {
        try {
            if ($CopyMode) { Copy-Item -Path $f.FullName -Destination $dest -Force }
            else           { Move-Item -Path $f.FullName -Destination $dest -Force }
        } catch {
            Write-RTELog -Level ERROR -Message ("Falhou {0}: {1}" -f $f.Name, $_.Exception.Message)
            continue
        }
    }

    [void]$index.Add([pscustomobject]@{
        category = $category
        file     = $f.Name
        size     = $f.Length
        sha256   = if (-not $DryRun) {
                       try { (Get-FileHash -Path (Join-Path $dest $f.Name) -Algorithm SHA256).Hash }
                       catch { '' }
                   } else { '' }
        modified = $f.LastWriteTime.ToString('o')
    })
}

# --- Gera INDEX.md -----------------------------------------------------------
if (-not $DryRun -and $index.Count -gt 0) {
    $indexPath = Join-Path $projectDir 'INDEX.md'
    $md = New-Object System.Text.StringBuilder
    [void]$md.AppendLine("# Engagement: $TargetName")
    [void]$md.AppendLine("")
    [void]$md.AppendLine("Gerado em: $(Get-Date -Format o)")
    $op = if ($env:USERNAME) { $env:USERNAME } else { $env:USER }
    [void]$md.AppendLine("Operador: $op")
    [void]$md.AppendLine("Total de arquivos: $($index.Count)")
    [void]$md.AppendLine("")
    foreach ($cat in $subDirs) {
        $items = $index | Where-Object { $_.category -eq $cat }
        if (-not $items) { continue }
        [void]$md.AppendLine("## $cat")
        [void]$md.AppendLine("")
        [void]$md.AppendLine("| Arquivo | Tamanho (bytes) | SHA-256 |")
        [void]$md.AppendLine("|---------|-----------------|---------|")
        foreach ($i in $items) {
            [void]$md.AppendLine("| $($i.file) | $($i.size) | ``$($i.sha256)`` |")
        }
        [void]$md.AppendLine("")
    }
    $md.ToString() | Out-File -FilePath $indexPath -Encoding UTF8 -Force
    Write-RTELog -Level SUCCESS -Message "Index gerado: $indexPath"
}

Write-RTELog -Level SUCCESS -Message ("Processados: {0} arquivos." -f $index.Count)
