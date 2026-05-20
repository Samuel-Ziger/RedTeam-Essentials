# OpSec Checklist - Engagement Red Team

> Lista de verificacao para minimizar artefatos e ruido durante operacoes. Use junto com o cliente para acordar RoE.

---

## Antes do Engagement

- [ ] **RoE assinado** com escopo, janela, contatos de emergencia.
- [ ] **Out-of-band channel** com cliente (Signal/Teams dedicado).
- [ ] **Lista de IPs/dominios** previstos compartilhada com o blue team se "purple" engagement.
- [ ] **Stop-words** definidas para halt imediato (ex: termo via Signal).
- [ ] **Backup de evidencias** com chain of custody planejado.
- [ ] **Notify legal team** (compliance).

---

## Infraestrutura

- [ ] **Team server** atras de redirector. Nunca exposto direto.
- [ ] **Dominios envelhecidos** (6+ meses, categorizados).
- [ ] **TLS valido** (Let's Encrypt) com SNI valido.
- [ ] **Profile C2 unico** para este engagement.
- [ ] **DNS, HTTPS, SMB pipe** transports preparados para fallback.
- [ ] **VPN/proxy** de saida limpo (nao IP do laptop).

---

## Pre-acesso

- [ ] **OSINT trail** minimizado (nao queimar identidade).
- [ ] **Phishing infra** registrada com privacy.
- [ ] **Implantes assinados** com cert legitimo / EV.
- [ ] **Loader** testado contra Defender/EDR-do-cliente (similares).
- [ ] **Sleep/jitter** alto inicial (15-30 min).

---

## Durante acesso inicial

- [ ] **Foothold** unico - nao gere 5 calls back-to-back.
- [ ] **Process hollow** ou processo "benigno" como container.
- [ ] **Beacon staging** off-disk se possivel.
- [ ] **Imediatamente** estabelecer **canal secundario** (DNS) em sleep alto.

---

## Recon interno

- [ ] **Comandos nativos** primeiro (WMI, PowerShell) - menos barulho que ferramentas droppadas.
- [ ] **BloodHound** com queries seletivas (nao `--collectionmethod all` em prod).
- [ ] **Evitar** `net user /domain` direto - prefira via WinRM/WMIC.
- [ ] **Throttle**: sem 1000 queries LDAP por minuto.
- [ ] **Cache local**: enumerar uma vez, consultar offline.

---

## Lateral movement

- [ ] **Tickets Kerberos**: usar `$krb5tgs` ja obtidos antes de novo `GetUserSPNs`.
- [ ] **PsExec / WMI / WinRM**: rotacionar tecnicas.
- [ ] **SMB pipe C2** entre hosts em vez de calls externas multiplas.
- [ ] **Limpar logs** so se acordado e estritamente necessario (geralmente NAO em red team padrao).

---

## Credentials

- [ ] **LSASS dump**: usar tecnicas modernas (MiniDumpWriteDump alternativas).
- [ ] **Mimikatz** evitado em favor de tools custom / off-the-land.
- [ ] **Hashes/tickets** armazenados criptografados, nunca em texto puro em disco.
- [ ] **Apagar** credentials apos engagement (verbal e via wipe).

---

## Persistencia

- [ ] **Verificar com cliente** se persistencia esta em escopo.
- [ ] Se sim: usar tecnica **claramente removivel** e documentada.
- [ ] Documentar TODA persistencia em **kill list**.
- [ ] Avisar cliente antes de reboot/disconnect testar.

---

## Logs / Telemetria

- [ ] **Antes** de comandos sensiveis, identificar:
  - Se Sysmon esta ligado.
  - Qual EDR.
  - Se Powershell script block logging.
- [ ] **Nao deletar** logs sem aprovacao escrita.
- [ ] **Nao parar servicos de seguranca** sem aprovacao.

---

## Comunicacao com cliente

- [ ] **Daily standup** breve (15 min) com PoC tecnico.
- [ ] **Findings criticos** comunicados em <2h via canal seguro (RCE em prod, exposicao de PII).
- [ ] **Stop sign** respeitado imediatamente.
- [ ] **Reporting cadence** definida (intermitente, final).

---

## Pos-engagement

- [ ] **Remover persistencia** confirmando com cliente.
- [ ] **Apagar implants** de hosts comprometidos.
- [ ] **Wipe** infraestrutura atacante (team server, redirectors).
- [ ] **Rotate** quaisquer creds usadas para acesso.
- [ ] **Final report** com:
  - Resumo executivo.
  - ATT&CK chain mapping.
  - Recomendacoes priorizadas.
  - Artefatos / IoCs entregues.
- [ ] **Lessons learned** com blue team (idealmente).

---

## Kill List (template)

```
| Tipo              | Host             | Caminho/ID                              | Removido em |
|-------------------|------------------|------------------------------------------|-------------|
| Scheduled Task    | DC01             | \Microsoft\Windows\UpdateTask           | yyyy-mm-dd  |
| Registry Run key  | WS-USER-01       | HKCU\...\Run\UpdateApp                  | yyyy-mm-dd  |
| Service           | FILESVR          | Service "WindowsHealthSvc"              | yyyy-mm-dd  |
| File              | DC01             | C:\ProgramData\update.exe               | yyyy-mm-dd  |
```

---

## Referencias

- [Red Team Field Manual](https://github.com/redcanaryco/atomic-red-team)
- [SpecterOps - Red Team OpSec](https://specterops.io/blog)
- [TrustedSec - PenTest OpSec](https://www.trustedsec.com/blog)
