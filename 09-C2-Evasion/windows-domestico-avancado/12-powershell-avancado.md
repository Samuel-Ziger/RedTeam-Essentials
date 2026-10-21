# 12 — PowerShell avançado e automação confiável

PowerShell é linguagem, shell e ambiente de automação sobre .NET. Seu diferencial é transportar objetos pelo pipeline, mas isso não elimina conversões, erros ou efeitos colaterais. Automação madura torna contratos explícitos, preserva tipos, controla mutações e produz informação que outro programa consegue consumir.

## Objetivos

Ao final, você deverá conseguir:

- escrever funções avançadas com validação e ajuda;
- explicar *pipeline binding* e as fases `begin`, `process` e `end`;
- separar saída de dados, mensagens informativas e erros;
- tratar falhas preservando contexto e recursos;
- projetar operações idempotentes com `ShouldProcess`;
- serializar dados considerando profundidade, cultura e versão de esquema.

## Funções como contratos

`[CmdletBinding()]` transforma uma função em função avançada e habilita parâmetros comuns. O bloco `param` é uma fronteira: declare tipos, obrigatoriedade, intervalos e conjuntos válidos ali, antes do corpo principal.

```powershell
function Get-RteLargeFile {
    [CmdletBinding()]
    [OutputType([pscustomobject])]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [System.IO.FileInfo]$File,

        [ValidateRange(1, 10240)]
        [int]$MinimumMiB = 100
    )

    process {
        if (-not $File.Exists) {
            Write-Error "Arquivo não existe: $($File.FullName)"
            return
        }
        if ($File.Length -ge ($MinimumMiB * 1MB)) {
            [pscustomobject]@{
                PSTypeName = 'Rte.LargeFile'
                Path       = $File.FullName
                Bytes      = $File.Length
                MiB        = [math]::Round($File.Length / 1MB, 2)
            }
        }
    }
}
```

`ValueFromPipeline` permite que cada objeto recebido seja associado ao parâmetro. O binding pode ocorrer por valor ou por nome de propriedade; regras excessivamente permissivas tornam comportamento surpreendente. Prefira contratos claros e testes que cubram entrada direta e pipeline.

`begin` executa uma vez antes do primeiro item e serve para preparar recursos; `process` executa por item; `end` finaliza agregações ou libera trabalho. Não acumule todo o pipeline em memória sem necessidade. Se um recurso for aberto em `begin`, garanta encerramento mesmo diante de erro.

## Streams e erros

PowerShell possui streams distintos: sucesso, erro, aviso, verboso, debug, informação e progresso. `Write-Output` ou uma expressão envia dados ao pipeline; `Write-Verbose` descreve diagnóstico opcional; `Write-Host` é interface humana e não deve carregar o resultado principal.

Erros podem ser terminantes ou não terminantes. Em um trecho que precisa abortar para manter consistência, use `-ErrorAction Stop` e trate com `try/catch/finally`:

```powershell
try {
    $item = Get-Item -LiteralPath $Path -ErrorAction Stop
    # trabalho somente leitura
}
catch [System.Management.Automation.ItemNotFoundException] {
    throw "Entrada não encontrada: $Path"
}
catch {
    throw "Falha ao inspecionar '$Path': $($_.Exception.Message)"
}
finally {
    # descarte recursos criados pelo bloco
}
```

Um `catch` vazio destrói o sinal de falha. Ao relançar, acrescente contexto sem publicar tokens, credenciais ou conteúdo sensível.

## Tipos, serialização e portabilidade

Formatação é a última etapa. `Format-Table` produz instruções de apresentação e não objetos úteis para CSV ou JSON. Devolva propriedades tipadas; deixe o chamador escolher a visualização.

JSON representa hierarquia, mas `ConvertTo-Json` requer profundidade adequada. CSV é tabular e achata estruturas. Datas devem usar ISO 8601, por exemplo `(Get-Date).ToUniversalTime().ToString('o')`. Para contratos estáveis, inclua `SchemaVersion` e documente campos obrigatórios. Evite depender da cultura local para interpretar decimal e data.

Objetos que atravessam processos ou sessões podem ser desserializados e perder métodos. Trate a fronteira como dados, não como um objeto .NET vivo.

## Idempotência e mutação segura

Uma operação idempotente converge ao mesmo estado quando repetida. O padrão é: observar estado atual, calcular diferença, aplicar apenas a diferença e verificar. Isso é diferente de “ignorar erros porque talvez já estivesse pronto”.

Funções que alteram estado devem oferecer `SupportsShouldProcess`:

```powershell
function Set-RteLabMarker {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
    param([Parameter(Mandatory)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        if ($PSCmdlet.ShouldProcess($Path, 'Criar marcador vazio')) {
            New-Item -ItemType File -Path $Path -ErrorAction Stop | Out-Null
        }
    }
}
```

`-WhatIf` mostra a intenção, mas não substitui testes ou backup. Valide caminhos com `-LiteralPath`, imponha raiz permitida e registre mudança e reversão.

## Exercícios

1. Adicione ajuda baseada em comentários e testes de pipeline a `Get-RteLargeFile`.
2. Construa uma função que exporte inventário em JSON com `SchemaVersion`, UTC e saída determinística.
3. Crie uma mutação limitada a `RTE-Lab`, implemente `-WhatIf` e prove idempotência executando duas vezes.
4. Demonstre a diferença entre erro terminante e não terminante sem esconder nenhum deles.

## Checklist

- [ ] Minha função possui contrato de entrada e saída verificável.
- [ ] Dados e mensagens operacionais usam streams diferentes.
- [ ] Falhas incluem contexto sem expor informação sensível.
- [ ] Serialização declara formato, tempo e versão.
- [ ] Toda mutação possui escopo, `-WhatIf`, verificação e reversão.

