<#
.SYNOPSIS
Lê um resumo estrutural de uma imagem PE sem executá-la.

.DESCRIPTION
Valida limites do DOS header, COFF header, optional header e section table antes
de interpretar campos. O limite de tamanho evita alocação acidental excessiva.
Este parser didático não substitui uma biblioteca PE completa.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$Path,

    [ValidateRange(1, 512)]
    [int]$MaximumFileSizeMiB = 64
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-RteRange {
    param(
        [Parameter(Mandatory)][long]$Offset,
        [Parameter(Mandatory)][long]$Length,
        [Parameter(Mandatory)][long]$TotalLength,
        [Parameter(Mandatory)][string]$Label
    )

    if ($Offset -lt 0 -or $Length -lt 0 -or
        $Offset -gt $TotalLength -or $Length -gt ($TotalLength - $Offset)) {
        throw "$Label aponta para fora do arquivo."
    }
}

$resolved = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
$file = Get-Item -LiteralPath $resolved -ErrorAction Stop
$maximumBytes = [long]$MaximumFileSizeMiB * 1MB
if ($file.Length -gt $maximumBytes) {
    throw "Arquivo excede o limite de $MaximumFileSizeMiB MiB."
}
if ($file.Length -lt 64) {
    throw 'Arquivo é pequeno demais para conter um DOS header PE.'
}

$bytes = [System.IO.File]::ReadAllBytes($resolved)
if ($bytes[0] -ne 0x4D -or $bytes[1] -ne 0x5A) {
    throw 'Arquivo não possui a assinatura MZ.'
}

$peOffset = [BitConverter]::ToInt32($bytes, 0x3C)
Assert-RteRange -Offset $peOffset -Length 24 -TotalLength $bytes.LongLength `
    -Label 'e_lfanew/COFF header'

if ($bytes[$peOffset] -ne 0x50 -or $bytes[$peOffset + 1] -ne 0x45 -or
    $bytes[$peOffset + 2] -ne 0 -or $bytes[$peOffset + 3] -ne 0) {
    throw 'Assinatura PE não encontrada no offset indicado por e_lfanew.'
}

$machineValue = [BitConverter]::ToUInt16($bytes, $peOffset + 4)
$sectionCount = [BitConverter]::ToUInt16($bytes, $peOffset + 6)
$timestamp = [BitConverter]::ToUInt32($bytes, $peOffset + 8)
$optionalHeaderSize = [BitConverter]::ToUInt16($bytes, $peOffset + 20)
$characteristics = [BitConverter]::ToUInt16($bytes, $peOffset + 22)

if ($sectionCount -lt 1 -or $sectionCount -gt 96) {
    throw "Quantidade de seções fora do limite didático: $sectionCount."
}

$optionalHeaderOffset = [long]$peOffset + 24
Assert-RteRange -Offset $optionalHeaderOffset -Length $optionalHeaderSize `
    -TotalLength $bytes.LongLength -Label 'Optional header'
if ($optionalHeaderSize -lt 70) {
    throw 'Optional header pequeno demais para os campos obrigatórios usados.'
}

$optionalMagic = [BitConverter]::ToUInt16($bytes, [int]$optionalHeaderOffset)
$format = switch ($optionalMagic) {
    0x010B { 'PE32' }
    0x020B { 'PE32+' }
    default { throw ('Optional header magic desconhecido: 0x{0:X4}.' -f $optionalMagic) }
}

$entryPointRva = [BitConverter]::ToUInt32($bytes, [int]$optionalHeaderOffset + 16)
$sectionAlignment = [BitConverter]::ToUInt32($bytes, [int]$optionalHeaderOffset + 32)
$fileAlignment = [BitConverter]::ToUInt32($bytes, [int]$optionalHeaderOffset + 36)
$sizeOfImage = [BitConverter]::ToUInt32($bytes, [int]$optionalHeaderOffset + 56)
$sizeOfHeaders = [BitConverter]::ToUInt32($bytes, [int]$optionalHeaderOffset + 60)
$subsystemValue = [BitConverter]::ToUInt16($bytes, [int]$optionalHeaderOffset + 68)

if ($sizeOfHeaders -gt $bytes.LongLength) {
    throw 'SizeOfHeaders excede o tamanho do arquivo.'
}

$sectionTableOffset = $optionalHeaderOffset + $optionalHeaderSize
$sectionTableLength = [long]$sectionCount * 40
Assert-RteRange -Offset $sectionTableOffset -Length $sectionTableLength `
    -TotalLength $bytes.LongLength -Label 'Section table'

$sections = for ($index = 0; $index -lt $sectionCount; $index++) {
    $offset = [int]($sectionTableOffset + ($index * 40))
    $nameBytes = $bytes[$offset..($offset + 7)]
    $name = [Text.Encoding]::ASCII.GetString($nameBytes).TrimEnd([char]0)
    $virtualSize = [BitConverter]::ToUInt32($bytes, $offset + 8)
    $virtualAddress = [BitConverter]::ToUInt32($bytes, $offset + 12)
    $rawSize = [BitConverter]::ToUInt32($bytes, $offset + 16)
    $rawPointer = [BitConverter]::ToUInt32($bytes, $offset + 20)
    $sectionCharacteristics = [BitConverter]::ToUInt32($bytes, $offset + 36)

    if ($rawSize -gt 0) {
        Assert-RteRange -Offset $rawPointer -Length $rawSize `
            -TotalLength $bytes.LongLength -Label "Dados brutos da seção '$name'"
    }

    [pscustomobject][ordered]@{
        Name = $name
        VirtualAddressRva = $virtualAddress
        VirtualSize = $virtualSize
        RawDataOffset = $rawPointer
        RawDataSize = $rawSize
        Characteristics = ('0x{0:X8}' -f $sectionCharacteristics)
    }
}

$machine = switch ($machineValue) {
    0x014C { 'x86' }
    0x8664 { 'x64' }
    0xAA64 { 'Arm64' }
    default { 'Unknown-0x{0:X4}' -f $machineValue }
}
$subsystem = switch ($subsystemValue) {
    1 { 'Native' }
    2 { 'WindowsGui' }
    3 { 'WindowsConsole' }
    10 { 'EfiApplication' }
    16 { 'WindowsBootApplication' }
    default { 'Unknown-{0}' -f $subsystemValue }
}
$authenticodeCommand = Get-Command -Name Get-AuthenticodeSignature `
    -ErrorAction SilentlyContinue
$signatureStatus = if ($null -ne $authenticodeCommand) {
    [string](Get-AuthenticodeSignature -LiteralPath $resolved).Status
}
else {
    'Unavailable'
}

[pscustomobject][ordered]@{
    SchemaVersion = 'rte.pe-summary/v1'
    Path = $resolved
    Length = $bytes.LongLength
    Machine = $machine
    Format = $format
    Characteristics = ('0x{0:X4}' -f $characteristics)
    SectionCount = $sectionCount
    EntryPointRva = $entryPointRva
    SectionAlignment = $sectionAlignment
    FileAlignment = $fileAlignment
    SizeOfImage = $sizeOfImage
    SizeOfHeaders = $sizeOfHeaders
    Subsystem = $subsystem
    CoffTimestampUtc = [DateTimeOffset]::FromUnixTimeSeconds($timestamp).UtcDateTime
    Sections = @($sections)
    Sha256 = (Get-FileHash -LiteralPath $resolved -Algorithm SHA256).Hash
    SignatureStatus = $signatureStatus
}
