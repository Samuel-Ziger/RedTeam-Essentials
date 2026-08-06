# Initial Access via Phishing (T1566)

> Teoria educacional sobre phishing como vetor de acesso inicial.
> **Nao inclui weaponization de payloads, malware, implants ou templates weaponizados.**

---

## Disclaimer etico

Use apenas em:

- Lab proprio isolado (GoPhish + dominios/contas de teste seus)
- Plataformas autorizadas (TryHackMe, etc.)
- Campanhas de **security awareness** ou red team com contrato e RoE escritos

Enviar phishing a terceiros sem autorizacao e crime. Este documento cobre conceitos, deteccao e labs eticos.

---

## 1. O que e phishing no contexto ATT&CK

**Phishing (T1566)** e a entrega de mensagem fraudulenta (email, chat, SMS, etc.) para induzir a vitima a:

- Abrir um anexo malicioso
- Clicar em um link e autenticar / baixar algo
- Conceder consentimento OAuth / device code
- Revelar credenciais ou tokens

No red team, o objetivo tipico e **foothold controlado** (credencial, sessao, ou callback autorizado) — nao destruicao. No blue team, o objetivo e detectar, bloquear e treinar usuarios.

### Por que ainda funciona

- Confianca humana + urgencia + contexto (spear)
- Cadeia de entrega longa (MTA -> gateway -> mailbox -> cliente)
- Bypass parcial de filtros por infraestrutura "legitima" (SaaS, redirectors)
- MFA fatigue / consent phishing quando a senha sozinha nao basta

---

## 2. Tipos principais (subtecnicas)

### 2.1 Spearphishing Attachment (T1566.001)

Mensagem com **arquivo anexo** que a vitima abre.

**Conceitos de delivery (sem weaponization):**

| Conceito | Descricao educacional |
|----------|----------------------|
| Lure | Texto/contexto que justifica o anexo (fatura, CV, relatorio) |
| Container | Formato do arquivo (documento, arquivo compactado, ISO/IMG em alguns cenarios) |
| Macro / script host | Historicamente: macros Office, LNK, HTA — hoje muitos bloqueados por padrao |
| Mark-of-the-Web (MotW) | Zona de internet no arquivo baixado; afeta execucao em Windows |
| Sandbox detonation | Gateway abre o anexo em sandbox; payloads "dormem" ou checam ambiente |

**Nao cobrimos** geracao de macros, loaders ou droppers. Em lab, use arquivos **inofensivos** (PDF/TXT de teste) so para medir taxa de abertura/click.

### 2.2 Spearphishing Link (T1566.002)

Mensagem com **URL** que leva a:

- Pagina de credential harvesting (clone de login) — so em lab autorizado
- Download de payload (fora do escopo deste repo)
- Consent / OAuth / device code phishing (muito comum em Entra ID / cloud — ver [08-Cloud-RedTeam](../08-Cloud-RedTeam/))
- Redirect chain que mascara o destino final

**Conceitos uteis para defesa e purple team:**

- URL shortening e open redirects
- Homoglyph / lookalike domains (`rn` vs `m`, punycode)
- Branding visual do portal clone
- HTTPS com certificado valido **nao** prova legitimidade

### 2.3 Spearphishing via Service (T1566.003)

Mesma ideia, mas via **servico de terceiros** em vez de email SMTP proprio:

- LinkedIn / Teams / Slack / WhatsApp Business
- Ticketing / vendor portals
- "Share file" de provedores de armazenamento

OPSEC ofensivo e deteccao mudam: menos dependencia de SPF/DKIM do dominio do atacante; mais dependencia de politicas do SaaS e DLP.

### 2.4 Variantes relacionadas (mencao)

| Variante | Nota |
|----------|------|
| Whaling | Spear contra executivos |
| Business Email Compromise (BEC) | Fraude financeira / alteracao de pagamento; muitas vezes sem malware |
| Smishing / Vishing | SMS / voz — fora do foco deste doc, mesmos principios de lure |
| Callback phishing | Vitima liga para numero "de suporte" controlado pelo atacante |

---

## 3. Anatomia de uma campanha (visao conceitual)

```
[OSINT alvo] -> [Lure + canal] -> [Entrega] -> [Acao da vitima]
                                                 |
                    +----------------------------+------------------+
                    v                            v                  v
              Credencial/token            Download/open         Consent OAuth
                    |                            |                  |
                    v                            v                  v
              Valid Accounts (T1078)    Execution (TA0002)*   Cloud foothold
```

\* Execution apos anexo esta **fora do escopo** deste modulo (ver 09-C2 apenas teoria).

### Fases tipicas em engagement autorizado

1. **Autorizacao** — lista de emails/usuarios no escopo; opt-out; janela.
2. **OSINT** — cargos, ferramentas internas, fornecedores (modulo 02).
3. **Infra de lab** — dominio de teste, pagina de captura **em rede isolada**, telemetria.
4. **Envio** — GoPhish ou equivalente; rate baixo; templates **nao weaponizados**.
5. **Metricas** — delivered / opened / clicked / submitted (awareness) ou foothold (red team).
6. **Cleanup** — desligar landing pages; reportar; treinar usuarios.

---

## 4. Payload delivery concepts (SEM weaponization)

O que um red teamer / defensor precisa **entender**, sem construir malware:

| Estagio | Ideia | Controle tipico |
|---------|-------|-----------------|
| Entrega | Mensagem chega na mailbox | SPF, DKIM, DMARC, reputacao IP |
| Filtragem | Gateway analisa URL/anexo | Secure Email Gateway, sandbox |
| Interacao | Usuario clica/abre | Treinamento, banner "external" |
| Pos-click | Browser segue redirect / download | Safe Links, proxy web, EDR |
| Credencial | Usuario digita senha no clone | MFA phishing-resistant, Conditional Access |
| Pos-foothold | Sessao/token abusado | Token protection, sign-in risk |

**Mark-of-the-Web e SmartScreen** — arquivos da internet carregam metadados que restringem execucao; atacantes tentam "remover" MotW (conceito defensivo: monitorar).

**Living-off-the-land** — apos click, abuso de binarios legítimos; cobrir em post-exploitation / evasion, nao aqui.

---

## 5. Deteccao e controles

### 5.1 Email gateway / SEG

Sinais e controles comuns:

- Reputacao de dominio/IP de envio
- Falha SPF / DKIM / DMARC alinhado
- Anexos com tipos bloqueados (`.exe`, `.js`, macros)
- URL rewrite + detonation
- Impersonacao de display name / lookalike domain
- First-time sender / unusual volume

**Checklist blue team (conceitual):**

- [ ] DMARC em `p=reject` (quando maduro)
- [ ] Bloqueio de macros da internet
- [ ] Banner de email externo
- [ ] Quarentena de anexos de alto risco
- [ ] Alertas de lookalike do dominio corporativo

### 5.2 Microsoft Safe Links / Safe Attachments (Defender for Office 365)

**Safe Links** reescreve URLs e verifica no momento do clique (time-of-click), alem de scans em tempo de entrega.

Pontos educacionais:

- Atrasos e "pre-clicks" de scanners podem gerar hits falsos em telemetria ofensiva de lab
- Bypass historicos (redirect chains, allowlists mal configuradas) sao **risco de config**, nao algo a explorar fora de escopo
- Em purple team: compare logs de Safe Links com clicks do GoPhish

**Safe Attachments** detona anexos em sandbox antes da entrega.

### 5.3 Sinais de deteccao (SOC)

| Sinal | Fonte tipica |
|-------|----------------|
| Pico de emails com mesmo lure | SEG / mail flow |
| Multiplos usuarios clicando mesma URL | Safe Links / proxy |
| Login apos click de IP anomalo | IdP / Entra ID / ADFS |
| Device code / consent grant suspeito | Audit logs cloud |
| Anexo executado (se houver) | EDR / Sysmon |

---

## 6. Labs eticos

### 6.1 GoPhish em lab proprio

Objetivo: medir **awareness** ou praticar operacao de campanha **sem payloads maliciosos**.

**Setup generico (lab isolado):**

```bash
# Exemplo generico - ajuste versoes/paths ao seu lab
# 1) Baixe GoPhish do release oficial (getgophish.com / GitHub)
# 2) Rode em VM isolada; nao exponha admin UI na internet
./gophish

# Acesse UI admin (porta padrao documentada na release)
# Configure:
#   - Sending profile (SMTP de teste / MailHog / Mailpit)
#   - Landing page (HTML inocuo: "Isto e um teste de seguranca")
#   - Email template SEM anexos weaponizados
#   - Grupo de usuarios = apenas contas do SEU lab
```

**Regras do lab:**

- Dominio e SMTP sob seu controle
- Landing page informa que e teste (em awareness) ou esta no RoE (red team)
- Sem coleta de senhas reais de producao
- Sem anexos executaveis

### 6.2 TryHackMe / plataformas

Procure salas atualizadas de:

- Phishing analysis (headers, IOC)
- Social engineering fundamentals
- Email header forensics

Use para praticar **deteccao e analise**, nao para enviar campanhas externas.

### 6.3 Exercicio purple (autorizado)

1. Blue team configura alertas de Safe Links / SEG.
2. Red team envia campanha GoPhish so para grupo piloto.
3. Compare timeline: envio -> rewrite -> click -> alerta.
4. Retrospectiva sem culpar usuarios; melhore controle + treino.

---

## 7. Checklist OPSEC etico (ofensivo autorizado)

Use em engagement **com RoE**. Objetivo: nao queimar o teste e nao causar dano.

### Antes

- [ ] Lista de alvos aprovada por escrito (inclui exclusoes)
- [ ] Canal de emergencia / stop-word com o cliente
- [ ] Infra separada da identidade pessoal do operador
- [ ] Landing / coleta apenas no escopo; TLS e logging definidos
- [ ] Acordo sobre captura de credenciais vs so click tracking
- [ ] Aviso legal / privacy (LGPD) revisado se houver PII

### Durante

- [ ] Rate de envio baixo; evite parecer spam em massa nao autorizado
- [ ] Nao pivotar para sistemas fora do escopo apos credencial
- [ ] Nao reutilizar senhas capturadas fora do ambiente do cliente
- [ ] Documentar cada foothold obtido
- [ ] Respeitar "do not phish" / VIP exclusions do RoE

### Depois

- [ ] Desligar landing pages e SMTP de campanha
- [ ] Entregar lista de usuarios que submeteram dados (se aplicavel)
- [ ] Forcar reset / session revoke conforme acordo
- [ ] Relatorio com IOCs para o blue team (dominios, URLs, IPs)
- [ ] Nao manter copias de credenciais apos o engagement

### Anti-padroes (nao faca)

- Weaponizar anexos neste repo ou em material compartilhado publicamente
- Phishing a fornecedores do alvo sem autorizacao explicita
- Usar dados vazados de breaches para alvos reais sem base legal/RoE
- Ignorar MFA fatigue em massa (pode ser DoS humano)

---

## 8. Mapeamento MITRE

| ID | Nome | Uso neste doc |
|----|------|---------------|
| TA0001 | Initial Access | Tatica pai |
| T1566 | Phishing | Tecnica principal |
| T1566.001 | Spearphishing Attachment | Secao 2.1 |
| T1566.002 | Spearphishing Link | Secao 2.2 |
| T1566.003 | Spearphishing via Service | Secao 2.3 |
| T1078 | Valid Accounts | Credencial obtida via lure |
| T1556 | Modify Authentication Process | Mencao (adversario avancado) |
| T1204 | User Execution | Pos-click / pos-open (conceitual) |

Proximos passos apos foothold: [14-Post-Exploitation](../14-Post-Exploitation/), [09-C2-Evasion](../09-C2-Evasion/).

---

## 9. Checklist rapido (estudo)

- [ ] Sei explicar T1566.001 vs .002 vs .003
- [ ] Sei o papel de SPF/DKIM/DMARC na entrega
- [ ] Sei o que Safe Links faz no momento do clique
- [ ] Montei GoPhish so com alvos de lab
- [ ] Tenho OPSEC etico escrito antes de qualquer campanha real
- [ ] Nao produzi nem distribuí payload weaponizado

---

## 10. Referencias

- [MITRE ATT&CK T1566](https://attack.mitre.org/techniques/T1566/)
- [GoPhish](https://getgophish.com/)
- [OWASP - Phishing](https://owasp.org/www-community/attacks/Phishing)
- [Microsoft - Safe Links](https://learn.microsoft.com/en-us/microsoft-365/security/office-365-security/safe-links-about)
- [DMARC.org](https://dmarc.org/)
- Modulo relacionado: [08-Cloud-RedTeam](../08-Cloud-RedTeam/) (device code / consent phishing em cloud)
- Modulo relacionado: [02-OSINT](../02-OSINT/) (recon para spear)
