# Referências comentadas

O curso é autocontido. Use estas fontes para confirmar detalhes da versão instalada e aprofundar depois de concluir os exercícios. Links consultados em 11 de outubro de 2026.

## Arquitetura e formatos

- [Windows Internals resources — Microsoft Sysinternals](https://learn.microsoft.com/en-us/sysinternals/resources/windows-internals) — errata, materiais e referência do livro de arquitetura.
- [About Processes and Threads — Microsoft](https://learn.microsoft.com/en-us/windows/win32/procthread/about-processes-and-threads) — recursos do processo e estado específico da thread.
- [Virtual Memory — Microsoft](https://learn.microsoft.com/en-us/windows/win32/memory/virtual-memory) — espaço virtual, páginas e funções de gerenciamento.
- [PE format — Microsoft](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) — estrutura oficial usada pelo parser do curso; valide magic, tamanhos e limites.
- [Dynamic-Link Libraries — Microsoft](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-libraries) — modelo, entry point e ciclo de DLLs.
- [Dynamic-Link Library Security — Microsoft](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-security) — riscos de busca ambígua e uso de caminho qualificado.
- [Understanding executable file signing — Microsoft](https://learn.microsoft.com/en-us/windows/win32/secbp/understanding-pe-signatures) — assinatura embutida, catálogos e bytes protegidos.

## PowerShell e testes

- [Advanced Functions — PowerShell](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced) — `CmdletBinding` e semântica de cmdlet em funções.
- [Functions — PowerShell](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions) — `begin`, `process`, `end` e `clean`.
- [Script Modules — PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/10-script-modules) — organização e importação de módulos.
- [PowerShell security features](https://learn.microsoft.com/en-us/powershell/scripting/security/security-features) — assinatura, logging e limites de Execution Policy.
- [PSScriptAnalyzer](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview) — análise estática e regras.
- [Pester Quick Start](https://pester.dev/docs/v5/quick-start) — fonte oficial do framework de testes e mocking.

## Tracing, desempenho e debugging

- [Event Tracing for Windows — Microsoft](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/event-tracing-for-windows) — providers, sessões e consumo.
- [Windows Performance Toolkit — Microsoft](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/) — WPR, WPA e perfis de desempenho.
- [Sysinternals Process Utilities — Microsoft](https://learn.microsoft.com/en-us/sysinternals/downloads/process-utilities) — índice oficial de Process Explorer, ProcMon, Autoruns, VMMap e ProcDump.
- [Process Monitor — Microsoft Sysinternals](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) — captura e filtros de arquivo, Registro e processos.
- [User-mode dump files — Microsoft](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/user-mode-dump-files) — opções de criação e uso de dumps.
- [Get started with WinDbg, user mode — Microsoft](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/getting-started-with-windbg) — símbolos, stacks e análise de aplicação própria.

## Proteções

- [Attack surface reduction capabilities — Microsoft Defender](https://learn.microsoft.com/en-us/defender-endpoint/overview-attack-surface-reduction) — relação entre ASR, CFA, Exploit Protection e audit mode.
- [Controlled folder access — Microsoft Defender](https://learn.microsoft.com/en-us/defender-endpoint/controlled-folders) — cobertura, allowed apps e monitoramento.
- [Exploit Protection reference — Microsoft](https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection-reference) — mitigações de sistema e aplicativo.
- [Enable memory integrity — Microsoft](https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity) — VBS/HVCI, compatibilidade e interpretação de `Win32_DeviceGuard`.
- [Credential Guard overview — Microsoft](https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/) — cobertura, requisitos e limites.
- [Application Control for Business — Microsoft](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/) — políticas para código autorizado.

## Vídeos oficiais complementares

- [Inside Show — Microsoft](https://learn.microsoft.com/en-us/shows/inside) — episódios curtos sobre internals, exceções e comandos do depurador.
- [Defrag Tools — Microsoft](https://learn.microsoft.com/en-us/shows/defrag-tools/) — série de troubleshooting com ferramentas Windows.
- [WinDbg: basic commands — Defrag Tools #20](https://learn.microsoft.com/en-us/shows/defrag-tools/20-windbg-basic-commands) — sessão e comandos iniciais do depurador.
- [WPT example: CPU — Defrag Tools #77](https://learn.microsoft.com/en-us/shows/defrag-tools/77-wpt-example) — seleção temporal, tabelas e stacks no WPA.

Vídeos podem usar interfaces antigas; compare conceitos e consulte a documentação atual antes de repetir passos. Fóruns e respostas comunitárias são pistas, não fonte normativa: confirme toda recomendação na documentação do produto e na sua VM.

