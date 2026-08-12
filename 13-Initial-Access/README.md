# 13 - Initial Access

> Modulo educacional sobre **acesso inicial** (MITRE TA0001): phishing, servicos externos e superficies publicas.
> Foco em **teoria, deteccao e labs eticos**. Nao inclui malware, implants ou scripts de phishing weaponizados.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários e equipes de awareness/purple team. |
| Pré-requisitos | Módulos 00, 01 e 02; contas e SMTP somente de laboratório. |
| Tempo estimado | 6 horas de teoria e 4 horas de simulação. |
| Ambiente | Somente laboratório próprio/isolado ou engagement autorizado. |
| Evidência final | Plano de campanha canário, métricas, detecções e debrief. |
| Critério de conclusão | Demonstrar o objetivo, explicar limitações e registrar o cleanup. |

## Disclaimer etico

Todo conteudo deste modulo e para uso em:

- Labs proprios / isolados
- Plataformas autorizadas (TryHackMe, HackTheBox, etc.)
- Engagements com **autorizacao escrita** e RoE (Rules of Engagement) claros

Phishing, password spraying e exploracao de servicos externos **sem autorizacao** sao ilegais. Use apenas com escopo formal.

## Conteudo

| Documento | Tema |
|-----------|------|
| [phishing-teoria.md](phishing-teoria.md) | Phishing (T1566): tipos, delivery concepts, deteccao, labs eticos, OPSEC. |
| [external-services.md](external-services.md) | VPN/RDP/OWA, password spraying (conceitos), T1190, supply chain high-level. |

## Objetivos de aprendizado

Ao concluir este modulo voce deve ser capaz de:

1. Explicar as principais tecnicas de Initial Access do ATT&CK (TA0001).
2. Diferenciar spear-phishing por link vs anexo vs service (conceitualmente).
3. Descrever controles de email gateway / Safe Links e como o blue team detecta campanhas.
4. Avaliar riscos de autenticacao fraca em VPN, RDP e OWA (sem realizar ataque ilegal).
5. Mapear exploit de aplicacao publica para o modulo [07-Web-AppSec](../07-Web-AppSec/).
6. Aplicar checklist OPSEC etico em lab ou engagement autorizado.

## Fluxo recomendado

```
01/02 Recon + OSINT  -->  13 Initial Access  -->  foothold
                              |                      |
                              v                      v
                     07 Web / 08 Cloud          14 Post-Exploitation
                     (T1190 / cloud)            09 C2 (teoria)
```

1. **Recon** - identificar emails, portais, VPN, OWA, apps publicas (modulos 01-02).
2. **Escolher vetor** - phishing (lab), servicos externos, ou exploit publico (07).
3. **Validar autorizacao** - RoE, escopo, janela, contatos de emergencia.
4. **Executar em lab / alvo autorizado** - documentar evidencias.
5. **Hand-off** - apos foothold, seguir para [14-Post-Exploitation](../14-Post-Exploitation/) e [09-C2-Evasion](../09-C2-Evasion/).

## MITRE ATT&CK (TA0001 - Initial Access)

| Tecnica | Nome | Documento |
|---------|------|-----------|
| T1566 | Phishing | phishing-teoria.md |
| T1566.001 | Spearphishing Attachment | phishing-teoria.md |
| T1566.002 | Spearphishing Link | phishing-teoria.md |
| T1566.003 | Spearphishing via Service | phishing-teoria.md |
| T1133 | External Remote Services | external-services.md |
| T1078 | Valid Accounts | external-services.md |
| T1110.003 | Password Spraying | external-services.md |
| T1190 | Exploit Public-Facing Application | external-services.md -> 07 |
| T1195 | Supply Chain Compromise | external-services.md (high-level) |
| T1199 | Trusted Relationship | external-services.md |

## Pre-requisitos

- Familiaridade com recon DNS/OSINT ([01-Recon](../01-Recon/), [02-OSINT](../02-OSINT/)).
- Noções basicas de autenticacao (senha, MFA, SSO).
- Para labs web: [07-Web-AppSec](../07-Web-AppSec/).

## Etica e escopo (resumo)

- Nunca envie phishing para dominios reais sem contrato e autorizacao.
- Nunca pulverize senhas contra portais de producao fora do RoE.
- Rate limit e lockout devem ser respeitados; coordinate com o blue team em purple team.
- Dados pessoais (LGPD) em campanhas de phishing de engajamento exigem tratamento especial.
- Persistencia e exfiltracao so apos foothold autorizado -> modulo 14.

## Referencias rapidas

- [MITRE ATT&CK - Initial Access](https://attack.mitre.org/tactics/TA0001/)
- [GoPhish](https://getgophish.com/) - framework open source para campanhas de awareness (lab proprio)
- [Microsoft Safe Links](https://learn.microsoft.com/en-us/microsoft-365/security/office-365-security/safe-links-about)
- TryHackMe: salas de phishing / social engineering (buscar catalogo atualizado)
