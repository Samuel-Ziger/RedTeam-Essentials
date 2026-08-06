# Initial Access via Servicos Externos

> Teoria educacional: VPN, RDP, OWA e outros servicos expostos; password spraying (conceitos);
> exploit de aplicacao publica (ponte para o modulo 07); supply chain em alto nivel.
> **Sem exploits weaponizados, sem wordlists de ataque a alvos reais.**

---

## Disclaimer etico

Testes contra VPN, RDP, OWA, IdP ou qualquer servico externo exigem **autorizacao escrita**.
Password spraying fora do RoE pode causar lockouts (DoS) e e ilegal.
Use labs (HTB, THM, range interno) ou ambientes do cliente com rate limits acordados.

---

## 1. Visao geral (TA0001)

Servicos remotos e contas validas sao vetores classicos de Initial Access quando:

- Ha superficie exposta na internet (ou partner network)
- Autenticacao e fraca / sem MFA
- Credenciais vazam (OSINT, stealer logs, password reuse)
- Ha CVE em componente publico (T1190)

```
Internet / Partner
       |
       +-- VPN concentrator (T1133)
       +-- RDP gateway / jump (T1133)
       +-- OWA / EAS / M365 (T1078)
       +-- App web publica (T1190) --> ver 07-Web-AppSec
       +-- Supply chain / trusted rel (T1195 / T1199)
```

---

## 2. External Remote Services (T1133)

### 2.1 VPN

**O que observar em recon autorizado:**

- Vendor/fingerprint (GlobalProtect, AnyConnect, Pulse, Fortinet, WireGuard portals, etc.)
- Portal web de login + endpoint IKE/SSL
- Versao exposta (banner, JS, paths conhecidos) — so enumeracao no escopo
- MFA: ausente, opcional, ou bypass por legacy clients

**Riscos tipicos (conceituais):**

| Risco | Por que importa |
|-------|-----------------|
| Senha sozinha | Spraying / credential stuffing |
| MFA fraco (SMS) | SIM swap / phishing MFA |
| CVE no appliance | RCE ou auth bypass (patch!) |
| Split tunnel mal configurado | Pos-auth lateral mais facil |
| Contas de servico/VPN legadas | Sem rotacao, sem MFA |

**Lab generico (conceitos de verificacao, nao ataque):**

```bash
# Enumeracao passiva/autorizada - exemplos genericos
# Nmap de servicos conhecidos apenas em lab/alvo autorizado
nmap -sV -p 443,500,4500,1194 <alvo-autorizado>

# Checagem de headers/portal (recon web) - ver tambem 07
curl -sI https://vpn.lab.local/
```

**Controles defensivos:**

- MFA phishing-resistant (FIDO2) onde possivel
- Conditional Access / posture (device compliance)
- Patch SLA para appliances
- Alertas de login geografico impossivel / volume de falhas
- Contas nominais; sem shared VPN user

### 2.2 RDP

RDP exposto na internet continua sendo Initial Access frequente (T1133 + T1078).

**Conceitos:**

- Porta 3389/tcp ou gateway RD Gateway (443)
- NLA (Network Level Authentication) reduz alguns ataques pre-auth, nao substitui MFA
- Contas locais com senha fraca / mesma senha em muitos hosts
- BlueKeep-class e CVEs historicas — **sempre patch**; nao explorar fora de lab

```bash
# Lab: verificar se RDP esta exposto (somente alvo autorizado)
nmap -p 3389 --script rdp-enum-encryption <alvo-autorizado>
```

**Mitigacoes:**

- Nao publicar RDP na internet; preferir VPN + jump host
- MFA / Azure AD + Conditional Access no gateway
- Conta lockout + monitoring 4625
- Restringir por IP allowlist quando inevitavel

### 2.3 OWA / Exchange / Microsoft 365

**OWA (Outlook Web App)** on-prem e portais M365 sao alvos de credential attacks e password spray.

Pontos educacionais:

- Autodiscover / EWS / ActiveSync tambem autenticam
- Legacy auth (Basic) e vetor classico — desabilitar quando possivel
- Em M365: Entra ID Smart Lockout, CA, Identity Protection
- Device code phishing e consent grant: ver [08-Cloud-RedTeam](../08-Cloud-RedTeam/)

```bash
# Lab: fingerprint generico de portal (autorizado)
curl -sI https://mail.lab.local/owa/
# Observe redirects, headers Server/X-OWA-Version (se presentes)
```

**Deteccao:**

- Spike de 401/falhas de logon
- Protocolos legacy inesperados
- Logons bem-sucedidos de ASN/VPN residencial apos spray

---

## 3. Password spraying — conceitos (T1110.003)

### 3.1 O que e (e o que nao e)

| Termo | Ideia |
|-------|-------|
| Brute force | Muitas senhas contra **uma** conta |
| Password spray | **Poucas** senhas comuns contra **muitas** contas |
| Credential stuffing | Pares usuario:senha vazados de outros breaches |

Spray existe para ficar **abaixo** de limiares de lockout por conta, explorando a mesma senha sazonal (`Verao@2026`) em todo o diretorio.

### 3.2 Rate limits e lockout (foco defensivo + RoE)

Antes de qualquer teste autorizado, documente:

- [ ] Quantas falhas geram lockout? Por quanto tempo?
- [ ] Ha smart lockout / cloud lockout diferenciado?
- [ ] Qual janela e taxa maxima o RoE permite?
- [ ] Quem no blue team monitora durante o teste?
- [ ] Contas de servico / break-glass estao **fora** do spray?

**Regra etica:** se o teste pode causar lockout em massa, **pare** — e DoS, nao Initial Access util.

### 3.3 Como pensar o teste (lab / autorizado)

Fluxo conceitual — **sem scripts de spray weaponizados neste repo**:

1. Obter lista de usuarios **no escopo** (OSINT / enum autorizado / fornecido pelo cliente).
2. Escolher 1–3 senhas **fracas e contextuais** (politica do alvo), nao dicionario infinito.
3. Espacar tentativas (horas/dias conforme lockout).
4. Autenticar so o suficiente para provar risco; depois reset/revoke.
5. Registrar evidencias e avisar o cliente.

Ferramentas publicas existem (sprayers para lab); use-as **somente** em ranges autorizados e leia o RoE. Prefira coordenacao purple team.

### 3.4 Controles que quebram spray

- MFA obrigatorio (melhor: resistant)
- Smart lockout + ban de IP/ASN anomalo
- Bloqueio de legacy auth
- Password policy + ban de senhas vazadas (Have I Been Pwned / ban lists)
- Canary / honeypot accounts com alerta de qualquer falha

---

## 4. Exploit Public-Facing Application (T1190)

Quando o acesso inicial vem de **vulnerabilidade em app exposta** (não de phishing nem de senha):

> Detalhes de recon, OWASP, XSS, auth bypass e API security estao em **[07-Web-AppSec](../07-Web-AppSec/)**.

### Ponte para o modulo 07

| Documento em 07 | Relacao com Initial Access |
|-----------------|----------------------------|
| [owasp-top10-2021.md](../07-Web-AppSec/owasp-top10-2021.md) | Classes de vuln exploraveis remotamente |
| [recon-web-pratico.md](../07-Web-AppSec/recon-web-pratico.md) | Descobrir superficie antes do exploit |
| [auth-bypass-patterns.md](../07-Web-AppSec/auth-bypass-patterns.md) | Bypass -> conta valida / admin |
| [api-security-checklist.md](../07-Web-AppSec/api-security-checklist.md) | APIs publicas como porta de entrada |
| [xss-deep-dive.md](../07-Web-AppSec/xss-deep-dive.md) | XSS pode virar sessao / foothold em alguns fluxos |

**Fluxo mental T1190:**

```
Recon (01/07) -> CVE ou logic bug -> PoC controlado -> foothold
                                              |
                                              v
                                    14 Post-Exploitation
```

**Etica T1190:**

- Sem DoS (payloads que enchem disco/CPU) salvo se RoE pedir stress test
- Sem ransomware / wipe
- Evidencia minima suficiente (screenshot, ID de objeto criado, whoami)

CVEs em VPN/appliances tambem sao T1190/T1133 — priorize **patch advisory** e lab reproduzivel, nao exploit publico em producao sem autorizacao.

---

## 5. Supply chain (T1195) — high-level

Compromisso da **cadeia de suprimentos** e Initial Access indireto: o atacante nao phisha o usuario final; compromete algo em que a organizacao **ja confia**.

### Categorias (visao)

| Tipo | Exemplo conceitual | Nota |
|------|-------------------|------|
| T1195.001 | Dependencias de software (typosquat, pacote malicioso) | DevSecOps / SCA |
| T1195.002 | Hardware / firmware (mencao) | Fora do foco do repo |
| T1195.003 | Update/compromise de software distribuido | Tipo SolarWinds (historico) |

### Trusted Relationship (T1199)

Parceiro, MSP, IdP federado ou vendor com VPN site-to-site — acesso "legitimo" que vira Initial Access se o parceiro for comprometido.

**Checklist defensivo (alto nivel):**

- [ ] Inventario de vendors com acesso de rede / IdP trust
- [ ] MFA e least privilege em contas de integracao
- [ ] Assinatura e verificacao de updates
- [ ] Pinning / allowlist de pacotes criticos no CI
- [ ] Monitorar consent grants e app registrations (cloud)
- [ ] Questionarios de seguranca + direito de auditoria em contratos

Nao cobrimos como montar supply-chain attack. Foque em **reduzir confianca implicita**.

---

## 6. Valid Accounts (T1078) — fecho do modulo

Independente do vetor (phish, spray, stuffing, leak), o resultado frequentemente e **conta valida**:

- Usuario corporativo VPN
- Conta cloud (T1078.004) — ver modulo 08
- Conta local em jump server
- Service account com RDP

Pos-acesso: nao "sprayar mais"; ir para enumeracao controlada e [14-Post-Exploitation](../14-Post-Exploitation/).

---

## 7. Checklist de estudo / engajamento

### Recon (autorizado)

- [ ] Listei VPN / RDP / OWA / IdP no escopo
- [ ] Identifiquei se MFA esta presente (sem bypass ilegal)
- [ ] Separei alvos T1133 vs T1190 (app web -> 07)

### Password policy test

- [ ] Lockout thresholds documentados com o cliente
- [ ] Taxa e janela no RoE
- [ ] Contas criticas excluidas
- [ ] Plano de unlock / comunicacao se lockout ocorrer

### Exploit publico

- [ ] Segui playbook do modulo 07
- [ ] PoC minimo; sem pivot fora do escopo
- [ ] CVE/patch reportado com evidencia

### Supply chain / trust

- [ ] Mapeei trusts e vendors relevantes (OSINT + entrevista)
- [ ] Incluí achados como risco de Initial Access indireto no relatorio

---

## 8. MITRE (resumo)

| ID | Nome |
|----|------|
| T1133 | External Remote Services |
| T1078 | Valid Accounts |
| T1110.003 | Password Spraying |
| T1190 | Exploit Public-Facing Application |
| T1195 | Supply Chain Compromise |
| T1199 | Trusted Relationship |
| T1078.004 | Cloud Accounts (ver 08) |

---

## 9. Referencias

- [MITRE T1133](https://attack.mitre.org/techniques/T1133/)
- [MITRE T1110.003](https://attack.mitre.org/techniques/T1110/003/)
- [MITRE T1190](https://attack.mitre.org/techniques/T1190/)
- [MITRE T1195](https://attack.mitre.org/techniques/T1195/)
- [Microsoft - Password spray detection](https://learn.microsoft.com/en-us/entra/architecture/security-operations-user-accounts)
- Modulo [07-Web-AppSec](../07-Web-AppSec/)
- Modulo [08-Cloud-RedTeam](../08-Cloud-RedTeam/)
- Modulo [01-Recon](../01-Recon/)
