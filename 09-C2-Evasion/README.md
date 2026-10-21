# 09 — Windows doméstico II: internals, PowerShell e defesa local

> Aprofundamento seguro do Windows local: arquitetura NT, PE/DLL, automação,
> tracing, desempenho, proteções modernas e debugging de aplicações próprias.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Estudantes que concluíram a administração local básica. |
| Pré-requisitos | Módulo 08 e fundamentos de C/PowerShell do 00. |
| Tempo estimado | 300–440 horas, incluindo 56 práticas e seis gates. |
| Ambiente | Windows 11 Pro/Enterprise em VM isolada, com SDK/Sysinternals/WinDbg. |
| Evidência final | DLL própria, traces, dump de fixture e diagnóstico causal. |
| Critério de conclusão | Concluir labs sem manipular terceiros nem reduzir proteções. |

## Curso principal

Siga a [rota completa de Windows doméstico avançado](windows-domestico-avancado/README.md).
Os 20 capítulos estão divididos em seis blocos e intercalados com seis gates.
O [guia de tracing e debugging](windows-domestico-avancado/GUIA-TRACING-DEBUG.md)
fornece o método transversal; o
[caderno](windows-domestico-avancado/CADERNO-PRATICAS.md) reúne 56 práticas com
critérios de aceite.

A pasta `exemplos/dll/` contém DLL nativa em C e consumidor seguro com caminho
absoluto, `LoadLibraryExW`, contrato de ABI, mitigações de build e testes. O
parser PowerShell valida limites do PE antes de interpretar seções. O projeto
final integra esses artefatos em uma bancada de diagnóstico reproduzível.

Não existe injeção, hooking, bypass, malware ou manipulação de outro processo.
Dumps, traces e ferramentas Sysinternals são limitados às fixtures próprias.

## Fora do escopo

Redes e administração remota continuam reservadas para os módulos 14–18.

## Continuação avançada

Acesso inicial, C2 e OPSEC são estudados no
[módulo 35](../35-Acesso-Inicial-C2/README.md), após a formação-base.

## Recursos complementares

O curso é autocontido; referências e vídeos servem para aprofundamento e para
confirmar detalhes que variam por versão. Consulte a
[bibliografia comentada](windows-domestico-avancado/REFERENCIAS.md) depois de
formar sua própria hipótese, não como substituto dos exercícios.
