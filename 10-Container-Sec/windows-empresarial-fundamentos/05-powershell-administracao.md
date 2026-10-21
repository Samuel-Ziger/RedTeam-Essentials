# 05 — PowerShell para administração de servidores

Administração profissional separa **Get/Test/Set**. `Get` observa, `Test`
compara com estado desejado, `Set` converge e valida. Scripts mutantes usam
`SupportsShouldProcess` e nunca escondem o alvo.

```powershell
function Set-RteDirectory {
    [CmdletBinding(SupportsShouldProcess)]
    param([Parameter(Mandatory)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        if ($PSCmdlet.ShouldProcess($Path, 'Criar diretório')) {
            New-Item -ItemType Directory -Path $Path | Out-Null
        }
    }
}
```

## Padrões

- parâmetros tipados/validados;
- `-LiteralPath` para entrada;
- erros terminantes e `try/finally`;
- objeto no pipeline, formatação na borda;
- JSON com schema/version;
- logs sem secrets;
- Pester para sucesso, erro e idempotência;
- PSScriptAnalyzer no CI.

PowerShell 5.1 e 7 coexistem e têm engines/módulos diferentes. Declare a
versão suportada e teste na mesma edição do servidor.

## Exercício

Execute o baseline do curso, altere somente a ordenação da saída e prove que
duas execuções mudam apenas o timestamp.

