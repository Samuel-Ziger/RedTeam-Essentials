# 02 - OSINT

> Modulo de **Open Source Intelligence**: coleta etica de informacoes publicas, ferramentas e automacao leve em PowerShell.
> Complementa [01-Recon](../01-Recon/) e alimenta vetores de [13-Initial-Access](../13-Initial-Access/).

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Iniciantes após os módulos 00 e 01. |
| Pré-requisitos | Módulos 00 e 01; fontes públicas e conta de laboratório. |
| Tempo estimado | 3 horas de leitura e 3 horas de prática. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Dossiê sintético com fontes, limitações e PII minimizada. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

## Conteudo

| Documento / Script | Tema |
|--------------------|------|
| [osint-tools-list.md](osint-tools-list.md) | Catalogo de ferramentas OSINT (dominios, pessoas, redes sociais, leaks, geo). |
| [osint_automation.ps1](osint_automation.ps1) | Script PowerShell para automacao basica de coleta (WHOIS, DNS, headers). |

## Fluxo recomendado

```
01 Recon (DNS/portas)  -->  02 OSINT (pessoas, org, leaks)
                                    |
                                    v
                           13 Initial Access (phishing / servicos)
```

1. **Escopo e etica** - confirmar que a coleta e so de fontes publicas e autorizada no engagement.
2. **Dominio e infraestrutura** - WHOIS, DNS, certificados, historico (Wayback, crt.sh). Ver [osint-tools-list.md](osint-tools-list.md).
3. **Pessoas e org** - emails, cargos, redes sociais, vazamentos publicos (haveibeenpwned-style, sem credential stuffing).
4. **Automacao** - rodar [osint_automation.ps1](osint_automation.ps1) em lab e documentar saidas.
5. **Hand-off** - cruzar achados com [01-Recon](../01-Recon/) e preparar narrativa para [13-Initial-Access](../13-Initial-Access/).

## Exercicios

1. Escolher um **dominio proprio** ou de lab (TryHackMe / HackTheBox / CTF) e montar um dossier OSINT de 1 pagina.
2. Executar `osint_automation.ps1` contra alvo autorizado e comparar com coleta manual.
3. Listar 5 ferramentas da [osint-tools-list.md](osint-tools-list.md) e registrar o que cada uma adiciona ao relatório.
4. Mapear pelo menos um email ou cargo publico encontrado para um cenario de phishing **apenas em lab** (modulo 13).

## MITRE ATT&CK (parcial)

- T1592 - Gather Victim Host Information
- T1589 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information
- T1591 - Gather Victim Org Information
- T1593 - Search Open Websites/Domains
- T1596 - Search Open Technical Databases

## Etica e escopo

OSINT usa fontes **publicas**, mas ainda exige:

- Autorizacao / RoE quando feito em nome de cliente.
- Nao atravessar paywalls, contas hackeadas ou engenharia social sem escopo.
- Nao publicar PII desnecessaria; minimize no report.
- Nunca usar achados para atacar sistemas sem autorizacao escrita.

Links uteis: [01-Recon](../01-Recon/) · [13-Initial-Access](../13-Initial-Access/).
