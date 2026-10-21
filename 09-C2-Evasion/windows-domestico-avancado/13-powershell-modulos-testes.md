# 13 — Módulos PowerShell, testes, análise e assinatura

Um script resolve uma tarefa; um módulo mantém uma interface reutilizável. Essa transição exige estrutura, API pública pequena, versionamento, testes e controle de procedência. O objetivo deste capítulo é empacotar automação defensiva local sem transformar a política de execução em falsa fronteira de segurança.

## Objetivos

Ao terminar, você deverá conseguir:

- separar funções públicas e auxiliares internas;
- explicar os papéis de `.psm1` e `.psd1`;
- criar testes Pester por comportamento e casos de falha;
- usar análise estática como uma camada, não como prova total;
- descrever Authenticode, timestamp e cadeia de confiança;
- publicar um módulo versionado sem embutir segredos ou dependências ocultas.

## Estrutura e manifesto

Uma organização mínima é:

```text
RteDiagnostics/
├── RteDiagnostics.psd1
├── RteDiagnostics.psm1
├── Public/
│   └── Get-RteSystemSummary.ps1
├── Private/
│   └── ConvertTo-RteIsoTime.ps1
└── tests/
    └── RteDiagnostics.Tests.ps1
```

O arquivo `.psm1` carrega o código. O manifesto `.psd1` declara metadados como `ModuleVersion`, `GUID`, versões compatíveis e `FunctionsToExport`. Exportar `*` torna qualquer helper acidentalmente parte da API; liste nomes explicitamente.

O manifesto é declarativo, mas ainda deve ser tratado como código confiável. Evite lógica surpreendente e caminhos dependentes da máquina do autor. Valide-o com:

```powershell
Test-ModuleManifest .\RteDiagnostics\RteDiagnostics.psd1
Import-Module .\RteDiagnostics -Force -Verbose
Get-Command -Module RteDiagnostics
```

Versionamento semântico ajuda a comunicar mudança: correção compatível incrementa *patch*; recurso compatível, *minor*; quebra de contrato, *major*. Isso não substitui um changelog que descreva migração.

## API pública e objetos

A API pública deve ser pequena e coerente. Use verbos aprovados, nomes singulares e parâmetros consistentes. Funções internas podem mudar livremente enquanto o comportamento público permanecer compatível. Devolva objetos com propriedades estáveis e, quando útil, `PSTypeName`; não devolva texto já formatado.

Não leia variáveis globais secretas nem altere `$ErrorActionPreference` do chamador. Configuração deve entrar por parâmetro ou arquivo validado. Dependências devem ser declaradas, fixadas dentro de uma faixa compatível e obtidas de repositório confiável.

## Pester por comportamento

Um teste útil separa **Arrange**, **Act** e **Assert**. Ele descreve efeito observável e falha por uma razão clara.

```powershell
Describe 'Get-RteSystemSummary' {
    It 'retorna o contrato mínimo' {
        $result = Get-RteSystemSummary
        $result.SchemaVersion | Should -Be '1.0'
        $result.ComputerName | Should -Not -BeNullOrEmpty
        $result.CollectedAtUtc | Should -Match 'Z$'
    }

    It 'não escreve texto de formatação no pipeline' {
        Get-RteSystemSummary | Should -BeOfType [pscustomobject]
    }
}
```

Mocks isolam dependências instáveis, mas um teste inteiramente mockado pode apenas confirmar o próprio roteiro. Combine testes unitários rápidos com poucos testes de integração em fixture controlada. Teste caminho feliz, limite, entrada inválida e falha da dependência. Cada teste deve limpar somente aquilo que criou.

Pester não prova ausência de bugs. Cobertura informa linhas exercitadas, não qualidade das asserções. Faça revisão de contrato, análise estática e execução real em VM descartável.

## PSScriptAnalyzer e qualidade automatizada

```powershell
Invoke-Pester .\RteDiagnostics\tests -Output Detailed
Invoke-ScriptAnalyzer -Path .\RteDiagnostics -Recurse -Severity Warning,Error
```

PSScriptAnalyzer detecta padrões conhecidos e regras de estilo ou compatibilidade. Registre exceções no repositório com justificativa estreita; não espalhe supressões para obter um relatório verde. Um pipeline confiável fixa versões das ferramentas e falha quando teste ou regra obrigatória falha.

## Authenticode e cadeia de confiança

Authenticode associa o hash do conteúdo à assinatura feita por uma chave privada. A validação depende do certificado, do uso permitido, da cadeia até uma raiz confiável e do estado de revogação. Um timestamp confiável demonstra que a assinatura ocorreu durante a validade do certificado, permitindo avaliação posterior conforme a política.

A chave de assinatura deve ficar protegida fora do repositório e fora dos logs. Assinar um script não torna seu comportamento seguro; garante identidade do signatário e integridade desde a assinatura. Revise antes de assinar e proteja o processo de publicação.

Execution Policy reduz execução acidental e expressa preferência administrativa, mas não é sandbox nem fronteira robusta contra um adversário. Para controle de aplicações, avalie mecanismos próprios de allowlisting em contexto apropriado. Neste módulo, não tente contornar nenhuma política.

## Exercícios

1. Empacote uma função dos exemplos em módulo com manifesto e export explícito.
2. Escreva pelo menos quatro testes: contrato, limite, erro e idempotência.
3. Introduza uma falha de propósito, confirme que o teste a detecta e reverta a alteração.
4. Inspecione uma assinatura existente com `Get-AuthenticodeSignature` e explique cada campo sem alterar a política local.

## Checklist

- [ ] A API pública é menor que o conjunto de helpers internos.
- [ ] Manifesto, compatibilidade e dependências são explícitos.
- [ ] Testes verificam comportamento e também falhas.
- [ ] Lint, testes e revisão são camadas complementares.
- [ ] Chaves, certificados e política de execução têm papéis distintos.

