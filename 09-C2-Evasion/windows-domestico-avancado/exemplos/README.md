# Exemplos executáveis e verificáveis

Os exemplos sustentam os capítulos 06, 07 e 13. Leia todo o código antes de executar. Eles não acessam rede, não carregam código em outro processo e não alteram configuração do sistema.

## Pré-requisitos

- Windows 11 em VM;
- Developer PowerShell for Visual Studio 2022 ou Build Tools equivalente;
- PowerShell 7 ou Windows PowerShell compatível;
- Pester 5.7.1 para a suíte do curso.

Confirme origem das ferramentas e use uma pasta do laboratório como conta comum.

## Parser PE defensivo

`Get-RtePeSummary.ps1` abre um arquivo como bytes, sem executá-lo. Antes de interpretar, ele limita tamanho e valida:

- assinatura MZ e offset `e_lfanew`;
- assinatura PE e COFF header;
- quantidade de seções e optional header;
- magic PE32/PE32+;
- section table e intervalos de dados brutos;
- `SizeOfHeaders` contra o tamanho do arquivo.

```powershell
$result = .\Get-RtePeSummary.ps1 `
    -Path "$env:SystemRoot\System32\notepad.exe" `
    -MaximumFileSizeMiB 64

$result | Select-Object SchemaVersion, Machine, Format, Subsystem,
    EntryPointRva, SizeOfImage, SectionCount, Sha256, SignatureStatus
$result.Sections | Format-Table
```

O schema é `rte.pe-summary/v1`. O parser é propositalmente parcial: não interpreta imports, exports, relocations ou certificados. Compare resultados com `dumpbin /headers`; não use o script como validador de segurança de conteúdo não confiável.

## DLL nativa e consumidor seguro

`dll/` contém:

```text
dll/
├── build.ps1
├── dll_consumer.c
├── rte_math.c
└── rte_math.h
```

A DLL exporta `rte_api_version` e `rte_add`. O consumidor calcula o diretório do próprio executável, forma um caminho absoluto, usa `LoadLibraryExW` com `LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR` e `LOAD_LIBRARY_SEARCH_SYSTEM32`, resolve exports, exige ABI versão 1 e chama `FreeLibrary`.

```powershell
Set-Location .\dll
.\build.ps1
```

Saída saudável:

```text
api_version=1
sum=42
```

O build usa warnings como erro, informações de depuração e opções de mitigação `/GS`, `/guard:cf`, `/DYNAMICBASE` e `/NXCOMPAT`. Preserve executável, DLL e PDBs juntos durante debugging, mas não os versione.

Para limpar somente artefatos gerados:

```powershell
Remove-Item -LiteralPath .\rte_math.dll, .\rte_math.lib, .\rte_math.exp,
    .\rte_math.obj, .\rte_math.pdb, .\dll_consumer.exe,
    .\dll_consumer.obj, .\dll_consumer.pdb -ErrorAction SilentlyContinue
```

Revise a lista antes de executar. Não copie a DLL para `System32`, não altere `PATH` e não baixe uma dependência com o mesmo nome.

## Testes

```powershell
Invoke-Pester .\tests -Output Detailed
```

A suíte confirma que o parser preserva o hash do alvo, devolve contrato mínimo, rejeita texto, section table truncada e arquivo acima do limite. Ela também inspeciona o consumidor para assegurar busca restrita, verificação de ABI e ausência das APIs de manipulação remota proibidas no curso.

Testes estáticos do código-fonte não provam o comportamento completo. O pipeline Windows compila e executa a fixture; os labs adicionam inspeção de cabeçalhos, ProcMon e teste de incompatibilidade.

## Falhas esperadas

| Falha | Interpretação | Ação |
|---|---|---|
| `cl.exe não encontrado` | terminal sem toolchain | abrir Developer PowerShell oficial |
| `load_failed` | DLL ausente ou inacessível no diretório permitido | conferir build e ProcMon filtrado |
| `unsupported_api_version=2` | contrato ABI diferente | reconstruir componentes compatíveis |
| seção fora do arquivo | PE truncado ou inconsistente | rejeitar; não tentar corrigir bytes |
| Pester indisponível | dependência de teste ausente | instalar versão documentada em ambiente autorizado |

Nenhuma resolução exige desabilitar Defender, assinatura de drivers, Execution Policy ou mitigação.

