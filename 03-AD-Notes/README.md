# 03 - Active Directory Notes

> Modulo de enumeracao, Kerberoasting, attack paths (BloodHound CE) e tecnicas modernas de AD.
> Labs: GOAD, DetectionLab, HTB Pro Labs ou AD proprio — **nunca** dominio de terceiros sem RoE.

## Conteudo

| Documento | Tema |
|-----------|------|
| [ad_enum_commands.md](ad_enum_commands.md) | Comandos essenciais de enumeracao AD (PowerShell, LDAP, NetExec). |
| [kerberoasting_teoria.md](kerberoasting_teoria.md) | Kerberoasting: SPNs, tickets, cracking, deteccao (T1558.003). |
| [bloodhound_teoria.md](bloodhound_teoria.md) | BloodHound CE: SharpHound, import, queries e paths ate Domain Admin. |
| [modern-ad-attacks-2026.md](modern-ad-attacks-2026.md) | Ataques modernos: ADCS, RBCD, SCCM, coercion; stack com NetExec. |

## Fluxo recomendado

```
enum (ad_enum)  -->  roast (kerberoasting)  -->  paths (BloodHound CE)  -->  modern (ADCS/RBCD/...)
```

1. **Enum** - usuarios, grupos, SPNs, shares, trusts. Preferir **NetExec (`nxc`)** em vez de CrackMapExec (legado). Ver [ad_enum_commands.md](ad_enum_commands.md).
2. **Roast** - identificar contas com SPN e praticar Kerberoasting em lab. Ver [kerberoasting_teoria.md](kerberoasting_teoria.md).
3. **Paths** - coletar com SharpHound e analisar no **BloodHound CE** (nao so a UI antiga). Ver [bloodhound_teoria.md](bloodhound_teoria.md).
4. **Modern** - ADCS (ESC1–ESC8), RBCD, coercion, SCCM. Ver [modern-ad-attacks-2026.md](modern-ad-attacks-2026.md).
5. **Report** - evidencias minimas + caminho de ataque; cruzar com [05-DFIR](../05-DFIR/) (o que o blue ve) e [14-Post-Exploitation](../14-Post-Exploitation/).

## Stack recomendada (2026)

| Ferramenta | Uso |
|------------|-----|
| **NetExec (`nxc`)** | Enum SMB/LDAP/WinRM; substitui CrackMapExec. |
| **BloodHound CE** | Grafo + paths (ADCS, RBCD, etc.). |
| Impacket / Rubeus | Kerberos, secrets, lateral em lab. |
| Certipy | ADCS abuse em lab. |

## MITRE ATT&CK (parcial)

- T1087.002 - Account Discovery: Domain Account
- T1069.002 - Permission Groups Discovery: Domain Groups
- T1482 - Domain Trust Discovery
- T1558.003 - Steal or Forge Kerberos Tickets: Kerberoasting
- T1558.001 - Golden Ticket
- T1649 - Steal or Forge Authentication Certificates (ADCS)
- T1134.001 / T1134.005 - Access Token Manipulation / SID-History

## Etica e escopo

- Apenas em AD de lab ou engagement com autorizacao escrita.
- Kerberoasting e coleta BloodHound geram ruido e tickets — alinhar janela com o cliente.
- Nao dumpar NTDS.dit / hashes fora do RoE; prove impacto com evidencia minima.
- Preferir contas de teste; cleanup de SPNs, certs e paths criados no lab.
