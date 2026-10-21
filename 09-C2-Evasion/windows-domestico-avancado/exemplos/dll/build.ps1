[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command -Name cl.exe -ErrorAction SilentlyContinue)) {
    throw 'cl.exe não encontrado. Abra um Developer PowerShell for VS 2022.'
}

Push-Location $PSScriptRoot
try {
    & cl.exe /nologo /W4 /WX /Zi /sdl /GS /guard:cf /LD /DRTE_MATH_EXPORTS `
        rte_math.c /link /DEBUG /DYNAMICBASE /NXCOMPAT /guard:cf /out:rte_math.dll
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao compilar a DLL: $LASTEXITCODE"
    }

    & cl.exe /nologo /W4 /WX /Zi /sdl /GS /guard:cf dll_consumer.c `
        /link /DEBUG /DYNAMICBASE /NXCOMPAT /guard:cf /out:dll_consumer.exe
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao compilar o consumidor: $LASTEXITCODE"
    }

    & .\dll_consumer.exe
    if ($LASTEXITCODE -ne 0) {
        throw "O consumidor falhou: $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

