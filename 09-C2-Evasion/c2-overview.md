# Visao Geral de C2 Frameworks

> Conteudo teorico - sem payloads. Mapeamento de design, deteccao e mitigacao.

---

## Arquitetura tipica

```
       Atacante                            Vitima
   +----------------+                  +----------------+
   |  Operator UI   |                  |    Implant /   |
   |  (Sliver,      |   <-- C2 ----->  |    Beacon      |
   |   Mythic, etc) |                  | (assinado/obf.) |
   +----------------+                  +----------------+
           |                                   |
           v                                   v
       Team Server                       Loader/Stager
   (Redirector/CDN/...)              (HTML smuggling, ISO, LNK, .HTA...)
```

Componentes:

1. **Listener.** Endpoint que recebe callbacks - HTTP(S), DNS, SMB pipe, TCP raw, MQTT.
2. **Stager.** Pequeno codigo inicial que baixa o payload completo.
3. **Beacon / Implant.** Codigo persistente que recebe comandos.
4. **Redirector.** Proxy para esconder team server real (Apache mod_rewrite, AWS CloudFront).
5. **Profile.** Como o trafego aparece (Malleable C2 profiles).

---

## Frameworks comuns (2024-2026)

| Framework | Linguagem | Stealth | Licenca | Notas |
|-----------|-----------|---------|---------|-------|
| Cobalt Strike | Java + Beacon | Alto | Comercial | Mais conhecido, malleable profiles. |
| Sliver | Go | Alto | BSD-3 | Multiplos transports, cross-platform implants. |
| Mythic | Python + agents varios | Alto | BSD-3 | Multi-agent, dockerizado. |
| Havoc | C++ + Demon | Alto | GPL-3 | Foco em evasao, modular. |
| Brute Ratel C4 | C/C++ + Badger | Alto | Comercial | EDR-evasion focado. |
| Caldera | Python | Baixo | Apache-2 | MITRE, mais para emulacao adversaria. |
| Empire | Python + agents | Medio | BSD-3 | Reativado por BC Security. |

---

## Transports / Channels (ATT&CK T1071/T1573)

| Transport | Vantagem | Detecao |
|-----------|----------|---------|
| **HTTPS** | Confunde com trafego web normal. | TLS fingerprint (JA3/JA4), SNI suspeito, beaconing periodico. |
| **DNS** | Atravessa firewalls restritivos. | Volume de queries TXT, dominios longos high-entropy. |
| **SMB Pipe** | Lateral movement entre hosts internos. | EDR monitora named pipes; logs de SMB. |
| **TCP raw** | Simples, performance. | Trafego incomum em porta nao-web. |
| **MQTT/IRC/Slack** | Camuflado em SaaS. | Detected por egress DLP / CASB. |
| **Domain Fronting (legacy)** | Esconde via CDN. | Quase todos os providers bloquearam ate 2024. |

---

## Malleable Profiles (conceito)

Permite customizar:

- User-Agent
- URI patterns
- Headers
- Body encoding (`netbios`, `base64url`, `mask`)
- Sleep + jitter
- HTTP method

Defesa olha para **anomalias**: User-Agent comum demais, intervalo de beacon muito regular.

---

## Persistencia (ATT&CK T1547, T1543)

- Run keys (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`).
- Scheduled Task com SYSTEM trigger.
- Servico Windows (binPath aponta para implant).
- WMI Event Subscription.
- COM Hijack.
- Login items / LaunchDaemons no macOS.
- systemd unit / cron no Linux.

---

## Operational Security do C2

1. **Redirector** SEMPRE (nunca expor team server direto).
2. **Domains aged** (12+ meses) com categoria "limpa" via Apivoid/VirusTotal.
3. **Profile especifico** por engagement (nao reuse profiles).
4. **Sleep + jitter** alto (5-15 min) salvo para hands-on.
5. **C2 over CDN** com path validation (Apache mod_rewrite valida URI antes de bater no team server).
6. **TLS:** certificados de CA real (Let's Encrypt), nao self-signed.

---

## Deteccao (defesa)

| Sinal | Tool |
|-------|------|
| Beacon traffic | RITA (active C2 hunting), Zeek. |
| JA3/JA4 anomalo | Suricata + community rulesets. |
| Process injection | Sysmon EID 8, EDR. |
| AMSI bypasses | AMSI logs Event ID 1100+. |
| Named pipes | Sysmon EID 17/18. |
| LSASS dump | EDR sensor, ELAM. |

---

## Referencias

- [MITRE D3FEND](https://d3fend.mitre.org/) - mapeamento defensivo.
- [Sliver wiki](https://github.com/BishopFox/sliver/wiki).
- [Cobalt Strike docs](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/).
- [Active Countermeasures - RITA](https://www.activecountermeasures.com/free-tools/rita/).
